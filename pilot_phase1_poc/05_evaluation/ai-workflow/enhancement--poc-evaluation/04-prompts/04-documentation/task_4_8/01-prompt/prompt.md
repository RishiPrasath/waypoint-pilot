# Task 4.8 Prompt — Lessons Learned (Full Retrospective)

## Persona
Technical lead writing a comprehensive retrospective after completing a 4-week AI-assisted POC development sprint.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Task**: 4.8 — Lessons learned (full retrospective)
- **Phase**: 4 (Documentation)
- **Dependencies**: CP3 (Fix loop complete)
- **Blocks**: T4.9 (Phase 2 recommendations)
- **Workspace**: `pilot_phase1_poc/05_evaluation/`

### Project Timeline
| Week | Phase | Workspace | Key Outcome |
|------|-------|-----------|-------------|
| Week 1 | Ingestion Pipeline | `02_ingestion_pipeline/` | Python pipeline: 29 docs, ~400 chunks, 87 tests passing |
| Week 2 | RAG Pipeline | `03_rag_pipeline/` | Node.js API + React UI, full query flow working |
| Week 3 | Retrieval Optimization | `04_retrieval_optimization/` | 30 docs, 709 chunks, 92% hit rate (94% adjusted) |
| Week 4 | Evaluation & Documentation | `05_evaluation/` | UX redesign, 217 tests, all 6 eval targets met, 38 docs |

### Week-by-Week Data Points

**Week 1 — Ingestion Pipeline:**
- Built Python ingestion: `process_docs.py` (discovery + parsing), `chunker.py` (RecursiveCharacterTextSplitter), `ingest.py` (ChromaDB storage)
- ChromaDB with all-MiniLM-L6-v2 via ONNX — no API key, fully local
- YAML frontmatter with 9 metadata fields per document
- PDF extraction with `pymupdf4llm` — extracted 53 PDFs from customs.gov.sg and Maersk
- Key lesson: PDF extracts must NOT be ingested — they're reference material already merged into main docs. Including them (3,853 chunks) dropped hit rate from 84% to 74%.
- Web scraping challenges: ASEAN site uses Elementor tab widgets (need accessibility tree UIDs), curl to CDN requires User-Agent header, customs.gov.sg sitemap.xml had 2,315 PDFs
- TDD approach: pytest tests written alongside each module

**Week 2 — RAG Pipeline:**
- Built Node.js/Express API with 6 services (pipeline, retrieval, llm, citations, embedding, index)
- Python subprocess bridge (`query_chroma.py`) for ChromaDB queries via JSON stdin/stdout
- Groq API with Llama 3.1 8B Instant — free tier, avg 1.2s response
- React + Tailwind frontend — initial basic UI
- Jest tests for backend, Vitest for frontend
- Key challenge: bridging Python (ChromaDB) and Node.js (API) — subprocess approach proved reliable

**Week 3 — Retrieval Optimization:**
- KB grew from 29 to 30 documents (added `fta_comparison_matrix.md`)
- Chunk config tested: 400/60, 600/90, 800/120, 1000/150 — 600/90 optimal
- Content fixes >> parameter tuning: +10pp hit rate from 2 content additions + 3 test fixes; 4 parameter experiments all performed equal or worse
- Key Terms body sections > frontmatter keywords (frontmatter stripped before embedding)
- Final: 92% raw hit rate, 709 chunks, 30 docs
- AI workflow pattern established: prompt -> human review -> execute -> report

**Week 4 — Evaluation & Documentation:**
- UX redesign: 4-section response card (answer, sources, related docs, confidence)
- 5-layer testing: ingestion (pytest), RAG pipeline (pytest), backend (Jest), frontend (Vitest + Chrome DevTools MCP), E2E evaluation (automated harness)
- 217 total tests across 3 frameworks
- 4 evaluation rounds: Round 2 (3/6 pass → failure analysis → fixes) → Round 3 (5/6 pass) → Round 4 (6/6 PASS)
- Citation accuracy improvement: 36.6% → 82.1% → 96.0% (prompt fixes + harness measurement fix)
- 38 documentation files across 4 layers
- AI workflow: 45 tasks, 7 phases, 3 checkpoints, ai-workflow-bootstrap-prompt pattern

### Technical Decisions That Worked Well
1. ChromaDB + ONNX embeddings — local, no API key, fast
2. Groq free tier — sufficient for POC, good Llama 3.1 citation compliance
3. Hybrid Python/Node — clean separation, subprocess bridge reliable
4. 600/90 chunk config — validated through 5-config experiment
5. YAML frontmatter — rich metadata for source attribution
6. Automated evaluation harness — repeatable, caught measurement issues

### Technical Decisions That Caused Friction
1. Confidence scoring thresholds too strict — 86% of queries got Low confidence
2. Citation regex matching — LLM nondeterminism caused inconsistent citation format
3. PDF extraction scope creep — 53 PDFs extracted but couldn't be ingested
4. Windows path handling — forward/backward slash issues in Git Bash
5. ChromaDB distance-to-similarity conversion — scores in 0.2-0.4 range, not intuitive

### Process Observations
- AI workflow pattern (prompt → review → execute) prevented runaway work
- Claude Code handled 45 tasks across 7 phases with 3 checkpoints
- TDD was effective for Python and Jest; Chrome DevTools MCP replaced Selenium for visual testing
- Documentation as dedicated phase (Week 4) was more efficient than inline-only approach
- 7-location tracking updates were tedious but prevented drift between checklist/roadmap/progress files
- Context window management was a challenge — large sessions required continuation

## Task

Create **1 lessons learned document** at `reports/lessons_learned.md`.

**Structure (5 sections):**

### 1. Executive Summary (1 paragraph)
- 4-week sprint, what was built, key outcomes

### 2. Technical Lessons (organized by week)
For each week (W1-W4):
- What was built
- Key technical decisions and their outcomes
- Specific data points (hit rates, test counts, chunk counts, latency)
- What worked well vs. what caused friction

### 3. Process Lessons
- AI workflow pattern effectiveness (prompt → review → execute → report)
- Claude Code as development partner (autonomy level, context management, parallel execution)
- TDD approach across 3 frameworks
- Documentation timing (inline Layer 1 during build vs. dedicated Layers 2-4 phase)
- 7-location tracking overhead and alternatives
- Checkpoint-based review cadence

### 4. What We'd Do Differently
- Specific, actionable items (not generic advice)
- Architecture changes (e.g., confidence scoring, citation matching)
- Tool choices (e.g., embedding model evaluation, LLM provider)
- Process improvements (e.g., tracking consolidation, testing strategy)
- Scope adjustments (e.g., PDF extraction, documentation timing)

### 5. Key Takeaways (5-7 bullet points)
- The most important lessons distilled into actionable principles

**Style:**
- Honest and specific — include what didn't work as well as what did
- Data-driven — reference specific metrics, counts, and comparisons
- Actionable — each lesson should inform future project decisions
- Target length: 200-300 lines

## Validation
- [ ] Technical section covers all major tech choices
- [ ] Process section covers AI workflow pattern
- [ ] "Do differently" section is substantive and specific
- [ ] Organized chronologically (W1-W4)
- [ ] Includes specific data points and examples

## Output

Create output report: `04-prompts/04-documentation/task_4_8/02-output/TASK_4.8_OUTPUT.md`

## Update on Completion

**MANDATORY — Update ALL 7 tracking locations:**
1. **Checklist**: `03-checklist/IMPLEMENTATION_CHECKLIST.md` — mark T4.8 `[x]`, update Phase 4 progress (8/9), Total (36/45, 80%)
2. **Roadmap Progress Tracker**: Phase 4 → `8`, Total → `36 | 80%`
3. **Roadmap Quick Reference**: T4.8 → `✅ Complete`
4. **Roadmap Detailed Entry**: T4.8 Status → `✅ Complete`, validation checkboxes `[x]`
5. **Bootstrap file**: `ai-workflow-bootstrap-prompt-v3.md` → `36/45 -- 80%`
6. **CLAUDE.md** (root): → `36/45 — 80%`
7. **AGENTS.md** (root): → `36/45 -- 80%`
