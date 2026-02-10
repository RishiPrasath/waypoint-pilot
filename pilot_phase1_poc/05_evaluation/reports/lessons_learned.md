# Waypoint Co-Pilot — Lessons Learned

**Date**: 2026-02-10
**Scope**: Full 4-week Phase 1 POC retrospective

---

## 1. Executive Summary

Over 4 weeks, the Waypoint POC progressed from an empty repository to a fully functional RAG-based customer service co-pilot with a 30-document knowledge base, Python ingestion pipeline, Node.js API server, React frontend, 217 automated tests, and 38 documentation files. The system met all 6 evaluation targets (87.2% deflection, 96.0% citation accuracy, 2.0% hallucination, 100% OOS handling, 1,182ms latency, zero crashes). The development was driven by an AI-assisted workflow using Claude Code, with human review at each task boundary. This retrospective captures what worked, what didn't, and what we'd change for Phase 2.

---

## 2. Technical Lessons

### Week 1 — Ingestion Pipeline

**What was built**: Python pipeline (`process_docs.py`, `chunker.py`, `ingest.py`) that discovers Markdown documents, parses YAML frontmatter, chunks text, and stores embeddings in ChromaDB. 29 documents produced ~400 chunks. 87 pytest tests written alongside.

**What worked**:
- **ChromaDB with default ONNX embeddings** was the right choice. Zero configuration, no API key, fast local inference. The all-MiniLM-L6-v2 model (384-d) provided sufficient semantic quality for a 30-document KB.
- **YAML frontmatter metadata** (9 fields per document) enabled rich source attribution later in Week 4. The upfront investment in structured metadata paid off across all subsequent phases.
- **TDD with pytest** caught chunking edge cases early — empty documents, documents without frontmatter, very short sections.

**What caused friction**:
- **PDF extraction scope creep**: Extracted 53 PDFs from customs.gov.sg (via sitemap.xml — 2,315 PDFs discovered) and Maersk. But ingesting them (3,853 chunks) dropped hit rate from 84% to 74%. The fix was merging key content into main docs and excluding PDF extracts from ingestion. Lesson: more content is not always better — curation matters more than volume.
- **Web scraping was brittle**: ASEAN site used Elementor tab widgets requiring accessibility tree UIDs. Curl to CDN/Maersk required User-Agent headers. Each source needed custom handling.
- **Windows path handling**: Forward vs. backward slashes in Git Bash caused failures. `venv/Scripts/python` works; `venv\Scripts\python` does not.

### Week 2 — RAG Pipeline

**What was built**: Node.js/Express API with 6 services, Python subprocess bridge for ChromaDB queries, Groq LLM integration, React + Tailwind frontend. Full query-to-response pipeline functional.

**What worked**:
- **Hybrid Python/Node.js architecture** was the right call. Python has superior NLP library support (ChromaDB, langchain-text-splitters); Node.js is better for API servers and React integration. The subprocess bridge (`query_chroma.py` via JSON stdin/stdout) proved reliable across hundreds of queries with zero failures.
- **Groq API with Llama 3.1 8B Instant** — free tier was sufficient for the entire POC (200+ queries across 4 evaluation rounds). Average 1.2s response time. Good instruction compliance for citation formatting.
- **Jest mocking strategy** — backend tests use full mocks (no real ChromaDB or Groq calls), making them fast and deterministic. 162 Jest tests run in ~3 seconds.

**What caused friction**:
- **Citation format compliance was unreliable from the start**. The system prompt asked for `[Title > Section]` citations, but the LLM frequently ignored this, especially for Low-confidence responses. This became the primary failure mode in Week 4 evaluation (11 of 37 Round 2 failures were Citation Gap).
- **Confidence scoring was poorly calibrated**: High threshold (>=3 chunks, avgScore >=0.5) was almost never met because ChromaDB distance-to-similarity conversion produces scores in the 0.2-0.4 range. Result: 86% of queries got Low confidence. Should have been calibrated against actual score distribution.

### Week 3 — Retrieval Optimization

**What was built**: Expanded KB from 29 to 30 documents, tested 5 chunk configurations, optimized retrieval from 76% to 92% hit rate (94% adjusted).

**What worked**:
- **Content fixes vastly outperformed parameter tuning**. The +10 percentage point improvement came from 2 content additions (abbreviation tables in body text, key query terms) and 3 test expectation fixes. Four parameter experiments (400/60, 600/90, 800/120, 1000/150) all performed equal or worse than the baseline.
- **600/90 chunk configuration** was the sweet spot for this KB size. Larger chunks (800, 1000) lost carrier-specific precision when multiple carriers appeared in the same chunk. Smaller chunks (400) fragmented tables and lists.
- **Frontmatter is stripped before embedding** — this was a critical discovery. Adding retrieval keywords to frontmatter had zero impact. Adding the same terms to body text (Key Terms sections, abbreviation tables) immediately improved retrieval.

**What caused friction**:
- **Test expectations drifted as content moved**. When FAQ answers covered a booking question, the expected source should have been updated from `booking_procedure.md` to `customer_faq.md`. Treating these as retrieval failures wasted investigation time.
- **`verify_ingestion.py` had hardcoded chunk ranges** (450-520) that broke when KB grew to 709 chunks. Small maintenance items like this consumed time disproportionate to their complexity.

### Week 4 — Evaluation & Documentation

**What was built**: 4-section response card UX, 5-layer test suite (217 tests), automated evaluation harness (6 metrics, 50 queries), 4 evaluation rounds, 38 documentation files.

**What worked**:
- **Iterative fix-and-retest loop** was highly effective. Round 2 surfaced citation format issues; Round 3 revealed harness measurement problems; Round 4 confirmed all fixes. Each round caught a distinct issue category that couldn't have been predicted upfront.
- **Root cause classification** (6 categories: Citation Gap, OOS Citation, Retrieval Miss, KB Content Gap, Baseline Mismatch, Latency Spike) enabled targeted fixes. Without classification, we would have applied broad changes instead of surgical corrections.
- **Automated evaluation harness** with JSON baselines made evaluation repeatable. The harness caught LLM nondeterminism (3 queries flipped pass/fail between rounds) that manual testing would have missed.
- **Chrome DevTools MCP replaced Selenium** for visual verification during development. Faster feedback loop, no driver management, direct accessibility tree inspection.

**What caused friction**:
- **Citation accuracy measurement was ambiguous**. Raw citation rate (60.5% in Round 3) included 0-chunk queries in the denominator — queries where citation is not applicable because the system correctly declined. The adjusted rate (82.1%) excluded these. The harness had to be fixed between Round 3 and Round 4 to calculate this correctly. Measurement methodology should have been defined precisely before Round 2.
- **LLM nondeterminism** at temperature 0.3 still produced variable citation formatting. Queries Q-03, Q-23, Q-29 flipped between pass and fail across rounds with identical configuration. This makes absolute pass/fail thresholds fragile.
- **Q-39 hallucination false positive** persisted through all rounds — a baseline issue where "I don't have" was flagged as hallucination for a correctly-declined query. The 2.0% hallucination rate is entirely this one artifact.

---

## 3. Process Lessons

### AI Workflow Pattern

The **prompt → human review → execute → report** pattern (implemented via ai-workflow-bootstrap-prompt-v3) was the most valuable process decision of the project.

- **Prompt generation as design review**: Writing the prompt forced explicit specification of inputs, outputs, validation criteria, and dependencies before any code was written. This prevented scope drift and caught ambiguities early.
- **Human review gate**: The mandatory stop between prompt generation and execution gave the human reviewer a natural decision point. Several prompts were adjusted before execution.
- **Parallel agent execution**: Claude Code launched multiple background agents for independent file creation (e.g., 6 architecture docs in parallel). This significantly reduced wall-clock time for documentation phases.

### Claude Code as Development Partner

- **Autonomy level was well-calibrated**: Claude Code executed within clearly scoped tasks but stopped at human review boundaries. The 45-task breakdown provided enough granularity for meaningful checkpoints without excessive overhead.
- **Context window management was a real constraint**: Large sessions (50+ tool calls) approached context limits, requiring conversation continuation. The MEMORY.md persistent file mitigated this by preserving key learnings across sessions.
- **7-location tracking was tedious but necessary**: Every task required updating checklist, roadmap (4 locations), bootstrap file, CLAUDE.md, and AGENTS.md. This was the most error-prone part of the workflow — updates were missed multiple times early on. A single-source-of-truth approach would be better.

### TDD Across 3 Frameworks

- **pytest (Python)**: Most natural TDD fit. Tests written alongside code, fast execution, good assertion patterns for data pipeline validation.
- **Jest (Node.js backend)**: Mocking strategy was essential — no real API calls in tests. 162 tests run in ~3 seconds. Good for service-level unit testing.
- **Vitest + Testing Library (React)**: Component testing caught rendering issues but was less valuable than Chrome DevTools MCP visual verification for layout/styling validation.

### Documentation Timing

- **Layer 1 (inline JSDoc/docstrings) during build**: Adding documentation while touching files was efficient — context was fresh, no second pass needed.
- **Layers 2-4 (READMEs, codebase docs, ADRs) as dedicated phase**: More efficient than inline because the full system was stable. Writing architecture docs against a changing codebase would have required constant updates.
- **38 files in a dedicated documentation phase** was ambitious but achievable with parallel agent execution. Without AI assistance, this volume of documentation would have taken significantly longer.

---

## 4. What We'd Do Differently

### Architecture Changes

1. **Calibrate confidence scoring against actual score distribution** — Analyze ChromaDB similarity scores before setting High/Medium/Low thresholds. The current thresholds were set theoretically and never matched real data (86% Low).

2. **Add citation post-processing** — Instead of relying entirely on the LLM to format citations correctly, add a post-processing step that matches response text against retrieved chunk titles using fuzzy matching. This would eliminate the Citation Gap failure mode (11 of 37 Round 2 failures).

3. **Design the evaluation harness measurement methodology before Round 1** — Define exactly how each metric is calculated (especially citation accuracy denominator for 0-chunk queries) before running any evaluation. The Round 3 → Round 4 harness fix cost an entire evaluation round.

### Tool Choices

4. **Evaluate 2-3 embedding models before committing** — all-MiniLM-L6-v2 was chosen because it's ChromaDB's default. It worked well enough, but we never compared it against alternatives (e.g., BGE-small, E5-small). A 30-minute benchmark at the start of Week 1 could have informed a better decision.

5. **Consider a structured output format from the LLM** — Instead of parsing free-text responses for citations, use Groq's JSON mode or structured output to enforce response format. This would eliminate citation format inconsistency.

### Process Improvements

6. **Consolidate tracking to 2 locations maximum** — The 7-location update requirement (checklist, roadmap x4, bootstrap, CLAUDE.md, AGENTS.md) was the highest-friction part of the workflow. A single roadmap file with auto-generated checklist view would eliminate this overhead.

7. **Run a smoke evaluation (10 queries) before the full 50-query round** — A quick smoke test would have caught the citation format issue in minutes instead of requiring a full Round 2 analysis.

### Scope Adjustments

8. **Limit PDF extraction to 10-15 high-value documents** — Instead of extracting 53 PDFs, curate a short list based on known query coverage gaps. The bulk extraction produced reference material that couldn't be ingested and consumed significant time.

9. **Start multi-turn conversation design in Phase 1** — Even if not implemented, designing the session memory architecture early would inform API design decisions (stateless vs. stateful endpoints, session storage).

---

## 5. Key Takeaways

1. **Content quality beats quantity and parameter tuning.** A curated 30-document KB with precise body text achieved 94% retrieval hit rate. Adding 53 PDF extracts (3,853 chunks) dropped performance. Content fixes improved hit rate by +10pp; four parameter experiments improved it by 0pp.

2. **Iterative evaluation with root cause classification is essential.** The fix-and-retest loop (3 rounds) caught three distinct issue categories that couldn't have been predicted. Without systematic failure analysis, fixes would have been unfocused.

3. **Measurement methodology must be defined before measurement.** The citation accuracy denominator ambiguity (should 0-chunk queries count?) cost an entire evaluation round. Define metrics precisely, including edge cases, before collecting data.

4. **The prompt → review → execute workflow prevents scope drift.** Writing prompts as design documents forced explicit specifications. Human review gates caught issues before implementation. This pattern is worth reusing in Phase 2.

5. **Local-first architecture reduces friction.** ChromaDB + ONNX embeddings required zero API keys, zero cloud setup, and zero network dependencies for retrieval. The only external dependency (Groq API) was the only source of nondeterminism.

6. **Bridge architectures work when interfaces are clean.** The Python/Node.js subprocess bridge (JSON stdin/stdout) handled 200+ queries without failure. Clean interface contracts (defined input/output schemas) made the hybrid architecture reliable.

7. **Documentation is a deliverable, not an afterthought.** The dedicated documentation phase (38 files) would not have happened if treated as "do it when you have time." Scheduling it as explicit tasks with validation criteria ensured completeness.
