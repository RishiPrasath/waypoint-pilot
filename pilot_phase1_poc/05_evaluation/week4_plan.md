# Week 4 Plan: Evaluation & Documentation

**Project**: Waypoint Phase 1 POC  
**Phase**: Week 4 (Days 22–30)  
**Created**: 2026-02-08  
**Status**: DRAFTING — Decisions being captured via Q&A

---

## Confirmed Decisions

| # | Decision | Date | Context |
|---|----------|------|---------|
| 1 | Keep ai-workflow pattern (prompt → review → execute → report) | 2026-02-08 | Same as Weeks 1–3; ai-workflow folder structure will be created in 05_evaluation/ but only after plan is finalized |
| 2 | Codebase fork excludes all W3-specific artifacts | 2026-02-08 | Exclude: `ai-workflow/`, `ai-workflow-bootstrap-prompt-v3.md`, `Retrieval_Optimization_Plan.md`, `REVISED_DOCUMENT_LIST.md`, `reports/` (all W3 reports), `chroma_db/` (rebuild fresh via ingestion), `venv/`, `node_modules/`, `.pytest_cache/`, `__pycache__/`. Carry forward: `backend/`, `client/`, `kb/`, `scripts/`, `tests/`, `data/`, `logs/`, root config files |
| 3 | Automated test harness for Round 2 | 2026-02-08 | Script hits POST /api/query for all 50 queries, captures full response, retrieved chunks, citations, and latency into JSON. |
| 4 | Fully automated testing via code — no LLM-as-judge, no manual scoring | 2026-02-08 | All evaluation done through programmatic assertions: retrieval hit/miss checks, citation presence/format validation, response structure checks, latency threshold assertions, OOS detection verification. Same pattern as Week 3's `retrieval_quality_test.py` but extended to cover the full pipeline. No 0–5 manual rubric. |
| 5 | Define expected-answer baselines (keywords + expected docs) for all 50 queries | 2026-02-09 | **REVISED** — Each query gets `must_contain` keywords, `should_contain` keywords, `must_not_contain` hallucination signals, and expected doc IDs (already exist in EXPECTED_SOURCES). Enables automated approximation of deflection rate, citation accuracy, and partial hallucination detection. ~5 hours upfront, reusable for all future runs. All 50 baselines must be complete before Round 2 runs — the harness needs complete data for meaningful aggregate metrics. "Build incrementally" refers to authoring order (start with top 10 priority queries, extend to all 50), not partial evaluation runs. |
| 6 | Fix-and-retest loop after Round 2 | 2026-02-08 | Same pattern as Week 3 Task 8: identify failures, apply fixes (prompt tuning, KB content gaps, threshold adjustments), re-run tests, repeat until targets met or Rishi decides to stop. No day-based time box — Claude Code executes iterations rapidly. |
| 7 | All 5 documentation deliverables required | 2026-02-08 | Technical architecture (final state), known limitations, user guide, deployment notes, and POC evaluation report — all needed. |
| 8 | Demo: React presentation app (Vite + Tailwind + Framer Motion) + Selenium automated live demo | 2026-02-09 | **REVISED** — standalone React app in `demo/presentation/` (own Vite project, own `package.json`). Replaces PPTX. Selenium script automates the live demo separately — runs selected queries through the Waypoint React UI, capturing screenshots and screen recording. Screenshots/video embedded as static assets in the presentation slides. No live API calls from the presentation itself. |
| 9 | Selenium captures both screenshots and screen recording | 2026-02-09 | **REVISED** — Screenshots at each step (query typed, response displayed) for embedding in React presentation slides as `<img>` assets. Separate screen recording (OBS or similar) of the full Selenium run embedded as `<video>` in the demo slide. All assets saved to `demo/presentation/public/demo/`. |
| 10 | Demo runs 8–10 queries: 5–7 happy path + 2–3 failure/OOS | 2026-02-08 | Specific queries selected after Round 2 testing based on best showcase results and graceful failure examples. |
| 11 | UI improvements needed: source URLs + response formatting | 2026-02-08 | Two fixes: (1) Responses must include clickable source URLs pulled from KB frontmatter `source_urls` field — not just document names. (2) Response formatting needs improvement — proper bullet points, structured lists, markdown rendering in the React frontend. Claude Code to implement both. |
| 12 | Response UX redesign: 4-section structured response card | 2026-02-09 | **REVISED** — Redesign response display into 4 distinct sections: (1) **Answer** — markdown-rendered via `react-markdown` (with `remark-gfm` for tables/strikethrough) with headers, numbered lists, bullets, bold, blockquotes. System prompt updated to enforce structured formatting. (2) **Sources** — clickable external URLs from KB frontmatter `source_urls`, showing org name, section, domain. Only shown when external sources exist. (3) **Related Documents** — color-coded chips showing all retrieved KB documents by category, with external link where URL exists. Icons derived from static category-to-icon mapping based on KB folder structure: `01_regulatory/` → 🏛️, `02_carriers/` → 🚢, `03_reference/` → 📚, `04_internal_synthetic/` → 📋. Category metadata already exists in ChromaDB chunks. (4) **Confidence Footer** — colored badge (High/Medium/Low) + reason + retrieval stats. Requires changes to: system prompt (formatting instructions), backend (pass source_urls + category in response), React frontend (new section components). Interactive mockup created as reference artifact. |
| 13 | UX redesign implemented before Round 2 testing | 2026-02-08 | System prompt, backend, and frontend UX changes are applied first. Round 2 tests run against the improved system so metrics reflect the final user experience. |
| 14 | Phase 2 recommendations: light 1-page bullet list | 2026-02-08 | No detailed scoping. Just a concise list of what Phase 2 could include based on POC results and gaps identified during evaluation. |
| 15 | CLAUDE.md Week 4 section — confirmed contents | 2026-02-09 | **REVISED** — Add Week 4 section covering: (1) Workspace: `05_evaluation/`, (2) Protected paths: `01_knowledge_base/`, `02_ingestion_pipeline/`, `03_rag_pipeline/`, `04_retrieval_optimization/` — all frozen, (3) AI workflow: same prompt → review → execute pattern, (4) Key commands: npm start, client dev, venv, test harness, ingestion, (5) Targets: deflection ≥40%, citation accuracy ≥80%, hallucination <15%, OOS ≥90%, system stability, (6) Task order: UX redesign → testing → fix loop → documentation → demo, (7) Test harness commands: automated 50-query evaluation script, (8) New deps: Selenium for demo capture, Framer Motion + react-mermaidjs + html2canvas for React presentation, (9) UX reference: point to mockup artifact as frontend design spec, (10) Presentation: `demo/presentation/` — standalone Vite app, `npm run dev` to preview, `npm run build` for static deploy. |
| 16 | Layer 1 — Ingestion Pipeline: re-run existing + add new tests | 2026-02-08 | Re-run all 87 existing unit tests to confirm nothing broke during copy. Add new tests to validate `source_urls` and `category` metadata is preserved through chunking into ChromaDB — critical for the new UX Sources and Related Documents sections. |
| 17 | Layer 2 — RAG Pipeline: retrieval + generation + citations all tested | 2026-02-08 | Three areas: (1) Re-run 50-query retrieval hit rate test to confirm 92% holds after copy. (2) Generation unit tests — context assembly, prompt formatting, LLM call handling, error cases. (3) Citation service tests — update existing `citations.test.js` to validate `source_urls` and `category` flow through enrichment into the response. |
| 18 | Layer 3 — Express Backend: update existing + new endpoint + error tests | 2026-02-08 | Three areas: (1) Update existing tests (`api.test.js`, `pipeline.test.js`, `retrieval.test.js`, `llm.test.js`) to match new response structure with `sources`, `relatedDocs`, `answer`, `citations`, `confidence`. (2) New endpoint tests validating `/api/query` returns all 4 sections with correct data types. (3) Error/edge case tests — empty query, very long query, Groq API timeout, ChromaDB connection failure. |
| 19 | Layer 4 — React Frontend: TDD workflow with Chrome DevTools MCP, autonomous | 2026-02-09 | **REVISED** — Component unit tests (React Testing Library / Vitest) + visual verification via Chrome DevTools MCP (not Selenium). Selenium is only used in Phase 5 for demo capture. Claude Code executes autonomously with review at checkpoints. TDD workflow per section: (1) Launch app (Express + React dev server, open in Chrome). (2) Write failing unit tests for the section. (3) Implement/modify the component to pass tests — Chrome DevTools MCP for live visual verification. (4) Run tests, iterate until green. (5) Visual check at desktop resolution via Chrome DevTools MCP. Repeat for each section: Answer → Sources → Related Documents → Confidence Footer. Docfork/Context7 MCP for library docs (React Testing Library, Vitest, Tailwind). |
| 20 | Layer 5 — E2E Evaluation: JSON + Markdown report + CSV | 2026-02-08 | 50-query full pipeline test outputs three formats: (1) `data/evaluation_results.json` — raw results for programmatic use. (2) `reports/evaluation_report.md` — human-readable report with metrics, per-category breakdown, failure analysis. (3) `data/evaluation_results.csv` — one row per query with columns for query ID, category, query text, response (truncated), expected docs, actual docs, must_contain hits, must_not_contain flags, citation present, latency, pass/fail. |
| 21 | 3 review checkpoints | 2026-02-08 | **CP1**: After workspace setup + codebase copy — run ALL existing tests (Python + Jest) and confirm they pass before any changes. **CP2**: After UX redesign complete — review the new frontend in browser before testing begins. **CP3**: After Round 2 testing + fix loop complete — review metrics before moving to documentation and demo. |
| 22 | Lessons learned: full retrospective | 2026-02-08 | Covers all three areas: (1) Technical — stack choices (ChromaDB, Groq, chunking, embeddings), what worked/didn't. (2) Process — ai-workflow pattern effectiveness, Claude Code autonomy, time management, documentation approach. (3) What you'd do differently if starting the POC over. |
| 23 | React presentation: 16 slides with 10 diagrams (mix approach) | 2026-02-09 | **REVISED** — Standalone Vite + React + Tailwind + Framer Motion app in `demo/presentation/`. Navigation: keyboard arrows + click, progress bar + slide counter, exportable to PDF (browser print / html2canvas). **Diagram approach — mix**: Mermaid (via `react-mermaidjs`) for 5–6 flow diagrams (ingestion pipeline, RAG pipeline, data flow, data collection flow, KB composition); Framer Motion animated SVG/CSS for 3–4 hero visuals (tech stack blocks, before/after comparison, metrics dashboard, week-by-week timeline). Slide plan unchanged: (1) Title, (2) Problem statement, (3) Industry/regional map, (4) Solution overview before/after, (5) Tech stack blocks, (6) Knowledge base composition, (7a) Data collection flow, (7b) Ingestion pipeline flow, (8) RAG pipeline architecture, (9) Response UX mockup annotated, (10) Live demo (Selenium screenshots/video), (11) Results metrics dashboard, (12) Week-by-week journey timeline, (13) Known limitations, (14) Phase 2 recommendations, (15) Q&A. |
| 24 | Codebase documentation: all 4 layers | 2026-02-08 | **Layer 1 — Inline**: JSDoc on all exported backend functions (services, routes, utils, middleware). Python docstrings on all script functions (ingest.py, chunker.py, config.py, pdf_extractor.py, retrieval_quality_test.py). Standardize existing inconsistent comments. **Layer 2 — Module READMEs**: `backend/README.md` (services, routes, config), `client/README.md` (component tree, props, adding new sections), `scripts/README.md` (each script, usage, parameters), `kb/README.md` (folder structure, frontmatter schema, how to add docs). **Layer 3 — Project-level**: Root `README.md` with quick start, architecture overview, folder structure, all commands. Overlaps with deployment notes deliverable. **Layer 4 — ADRs**: Architecture Decision Records for key choices — ChromaDB over Pinecone, Groq/Llama over OpenAI, 600/90 chunk config, Python ingestion + Node backend split, all-MiniLM-L6-v2 embedding model, ChromaDB default embeddings. Stored as standalone files or section in technical architecture doc. |
| 25 | ADRs as standalone files in `documentation/adrs/` | 2026-02-08 | Standard ADR format. Each decision in its own file: `ADR-001-vector-database.md`, `ADR-002-llm-provider.md`, `ADR-003-chunk-config.md`, `ADR-004-python-node-split.md`, `ADR-005-embedding-model.md`, etc. Each file covers: context, decision, alternatives considered, consequences. |
| 26 | Documentation timing: split approach | 2026-02-08 | Layer 1 (inline JSDoc/docstrings) added during UX build — as Claude Code touches each file, it adds documentation at the same time. Layers 2–4 (module READMEs, project README, ADRs) done as a dedicated phase after testing is complete. |
| 27 | Final `05_evaluation/` folder structure confirmed | 2026-02-09 | **REVISED** — `ai-workflow/`, `backend/`, `client/`, `kb/`, `scripts/`, `tests/`, `chroma_db/`, `data/`, `logs/`, `reports/`, `documentation/` (with `adrs/` subfolder), `demo/` (with `presentation/` Vite sub-project and `selenium/` scripts + screenshots), plus root config files (.env, package.json, jest.config.js, requirements.txt, README.md). |
| 28 | Short pointer READMEs in code folders | 2026-02-08 | Add short READMEs inside `backend/README.md`, `client/README.md`, `scripts/README.md`, `tests/README.md`, `kb/README.md` — each with a brief summary and link to the detailed docs in `documentation/codebase/`. |
| 29 | Pipeline flow docs added to architecture/ | 2026-02-08 | Add two detailed process flow documents: `documentation/architecture/ingestion_pipeline_flow.md` (document sources → frontmatter extraction → chunking → embedding → ChromaDB storage, with step-by-step detail per stage) and `documentation/architecture/rag_pipeline_flow.md` (query → embedding → retrieval → context assembly → LLM generation → citation extraction → response formatting, with step-by-step detail per stage). These go deeper than system_overview.md — they explain the actual process, data transformations at each step, config parameters that affect behavior, and error handling. |
| 30 | Success criteria checklist as a formal task | 2026-02-08 | Create a checkable success criteria document covering all three areas from the roadmap: **Technical** (ChromaDB running 25+ docs, retrieval returns relevant results, LLM generates sourced responses, API functional, UI working), **Quality** (50 test queries executed, 40% deflection, 80% citation accuracy, graceful OOS handling), **Documentation** (architecture documented, user guide complete, known limitations listed, demo script prepared). Checklist populated from automated test results where possible, manually verified otherwise. Output: `reports/success_criteria_checklist.md`. |
| 31 | Fresh ingestion — no ChromaDB data copied | 2026-02-08 | Do NOT copy `chroma_db/` from `04_retrieval_optimization/`. Instead, run the ingestion pipeline fresh in `05_evaluation/` from the copied KB documents. Then run ingestion pipeline tests to validate: correct document count, correct chunk count (~709), metadata integrity (source_urls, category, retrieval_keywords preserved), embedding dimensions. This proves the pipeline is fully reproducible and the KB is self-contained. |
| 32 | Excluded from scope: demo feedback template, Go/No-Go formal process, 00_docs/ update | 2026-02-08 | Not needed for Week 4. Demo feedback, Go/No-Go decision process, and updating original planning docs in 00_docs/ are all excluded. |

---

## Phase 0: Workspace Setup

### Task 0.1 — Create `05_evaluation/` folder structure

```
pilot_phase1_poc/05_evaluation/
├── ai-workflow/                  # Week 4 prompt/roadmap/checkpoint workflow
├── backend/                      # Express API server
├── client/                       # React frontend (new UX)
├── kb/                           # Knowledge base (01_regulatory/, 02_carriers/, 03_reference/, 04_internal_synthetic/)
├── scripts/                      # Python ingestion + evaluation scripts
├── tests/                        # Unit + E2E tests (Python + Jest)
├── chroma_db/                    # Vector store (built fresh via ingestion — NOT copied)
├── data/                         # Test results JSON, CSV, scoring data
├── logs/                         # System logs
├── reports/                      # Evaluation reports, failure analysis, success criteria
├── documentation/                # Full documentation suite (34 files)
│   ├── adrs/                     # Architecture Decision Records (6 files)
│   ├── architecture/             # System overview, data flow, pipeline flows, KB schema, API contract (6 files)
│   ├── codebase/                 # Backend, frontend, scripts, tests docs (18 files)
│   └── guides/                   # User guide, deployment notes, known limitations (3 files)
├── demo/                         # Presentation app + Selenium demo capture
│   ├── presentation/             # Standalone Vite + React + Tailwind + Framer Motion app
│   │   ├── src/                  # Slide components, diagrams, layout
│   │   ├── public/demo/          # Selenium screenshots + screen recording video
│   │   ├── package.json          # Independent deps (framer-motion, react-mermaidjs, html2canvas)
│   │   └── vite.config.js
│   └── selenium/                 # Selenium scripts + raw captures
├── .env / .env.example
├── package.json
├── jest.config.js
├── requirements.txt
└── README.md
```

### Task 0.2 — Copy codebase from `04_retrieval_optimization/`

**Copy:**
- `backend/` — full Express server
- `client/` — React frontend
- `kb/` — all 4 KB subdirectories including `pdfs/`
- `scripts/` — Python ingestion, chunking, retrieval test, PDF extractor
- `tests/` — all JS and Python test files
- `data/` — `retrieval_test_results.json`
- `logs/`
- Root config: `.env`, `.env.example`, `.gitignore`, `package.json`, `package-lock.json`, `jest.config.js`, `requirements.txt`, `start.ps1`, `start.sh`

**Exclude:**
- `ai-workflow/` — W3 workflow
- `ai-workflow-bootstrap-prompt-v3.md` — W3 bootstrap
- `Retrieval_Optimization_Plan.md` — W3 planning
- `REVISED_DOCUMENT_LIST.md` — W3 tracker
- `reports/` — all W3 reports
- `chroma_db/` — rebuild fresh via ingestion
- `venv/` — recreate
- `node_modules/` — reinstall
- `.pytest_cache/`, `__pycache__/` — transient

### Task 0.3 — Setup environment
- `npm install`
- Create Python venv, `pip install -r requirements.txt`

### Task 0.4 — Fix ingestion pipeline metadata
The current `ingest.py` does NOT store `source_urls`, `retrieval_keywords`, or `use_cases` in ChromaDB metadata. These fields are parsed by `process_docs.py` but dropped during `ingest_document()`. This is a blocker for the UX redesign (Sources and Related Documents sections depend on `source_urls` and `category` being in chunk metadata).

Update `scripts/ingest.py` `ingest_document()` metadata dict to include:
- `source_urls` — joined as comma-separated string (ChromaDB metadata only supports string/int/float, not arrays)
- `retrieval_keywords` — joined as comma-separated string
- `use_cases` — joined as comma-separated string

This aligns with the existing `citations.js` pattern which already splits `source_urls` by comma: `matchedChunk.metadata?.source_urls?.split(',')`.

### Task 0.5 — Run fresh ingestion
- Execute `python scripts/ingest.py --clear` against copied KB
- Validate: correct document count (30), chunk count (~709), metadata integrity
- **Verify new metadata fields**: spot-check that `source_urls`, `retrieval_keywords` are present in ChromaDB chunks

### Task 0.6 — Run ALL existing tests
- Python: `pytest` — all ingestion pipeline tests
- Jest: `npm test` — all backend tests
- Retrieval: `python scripts/retrieval_quality_test.py` — confirm 92% hit rate holds
- Verify end-to-end: start backend, submit test query, confirm response with citations

**→ CHECKPOINT 1: All existing tests pass on fresh ingestion with new metadata fields. Rishi reviews before proceeding.**

---

## Phase 1: UX Redesign — 4-Section Response Card

Implemented **before** testing so Round 2 metrics reflect the final user experience.

### Task 1.1 — Update system prompt
Modify `backend/prompts/system.txt` to enforce structured response formatting:
- Use markdown headers (`###`) for multi-part answers
- Use numbered lists for sequential steps or required documents
- Use bold for key terms, thresholds, deadlines
- Keep each bullet to one line
- Explicit citation format instructions for the new Sources section

### Task 1.2 — Update backend pipeline
Modify `backend/services/pipeline.js` and `backend/services/citations.js` to return:
- `sources` — external URLs from KB frontmatter `source_urls` with org name, section
- `relatedDocs` — all retrieved chunks' parent documents with `category`, `title`, `url`, `docId`
- Updated `answer`, `citations`, `confidence` structure

### Task 1.3 — Implement new React frontend (TDD per section)

For each of the 4 sections, follow the TDD workflow:

1. **Launch app** — Express backend + React dev server, open in Chrome
2. **Write failing unit tests** (React Testing Library / Vitest)
3. **Implement component** — Chrome DevTools MCP for live visual verification
4. **Run tests, iterate until green**
5. **Visual check** — verify layout at desktop resolution (1280px+) via Chrome DevTools MCP

**Section order:**
- Answer section — markdown rendering (headers, lists, bold, blockquotes)
- Sources section — clickable external URLs with org name, domain
- Related Documents section — color-coded category chips (🏛️ regulatory, 🚢 carrier, 📚 reference, 📋 internal)
- Confidence Footer — colored badge, reason, retrieval stats

Library docs via Docfork/Context7 MCP (React Testing Library, Vitest, Tailwind).

### Task 1.4 — Add Layer 1 inline documentation
As each file is touched during the UX build:
- JSDoc on all modified/new backend functions
- Component prop documentation in React files

**→ CHECKPOINT 2: New UX complete. Rishi reviews frontend in browser before testing begins.**

---

## Phase 2: Systematic Testing — All 5 Layers

### Layer 1: Ingestion Pipeline (Python/pytest)

**Task 2.1 — Re-run existing ingestion tests**
- Confirm all 87 existing unit tests pass after fresh ingestion

**Task 2.2 — Add new metadata preservation tests**
- Validate `source_urls` preserved through chunking into ChromaDB
- Validate `category` field preserved per chunk
- Validate `retrieval_keywords` preserved per chunk
- These are critical for the new UX Sources and Related Documents sections

### Layer 2: RAG Pipeline (retrieval + generation)

**Task 2.3 — Re-run 50-query retrieval hit rate test**
- Confirm 92% hit rate holds on freshly ingested data

**Task 2.4 — Add generation unit tests**
- Context assembly / formatting
- Prompt construction with new formatting instructions
- LLM call handling and error cases

**Task 2.5 — Update citation service tests**
- Update `citations.test.js` to validate `source_urls` and `category` flow through enrichment
- Test new response structure (sources, relatedDocs)

### Layer 3: Express Backend (Node/Jest)

**Task 2.6 — Update existing backend tests**
- Modify `api.test.js`, `pipeline.test.js`, `retrieval.test.js`, `llm.test.js` to match new response structure

**Task 2.7 — Add new endpoint tests**
- Validate `/api/query` response contains all 4 sections with correct data types
- Validate `sources` array shape (title, org, url, section)
- Validate `relatedDocs` array shape (title, category, docId, url)

**Task 2.8 — Add error/edge case tests**
- Empty query, very long query
- Groq API timeout
- ChromaDB connection failure
- Malformed input

### Layer 4: React Frontend (Vitest)

**Task 2.9 — Component unit tests**
- Already written during Phase 1 TDD workflow
- Confirm all pass after any post-UX adjustments

**Task 2.10 — Visual verification via Chrome DevTools MCP**
- Manual visual checks during frontend development (already done in Phase 1 TDD workflow)
- Confirm all 4 sections render correctly at desktop resolution
- Not automated — Chrome DevTools MCP used interactively during build, not Selenium

### Layer 5: End-to-End Evaluation (50 queries)

**Task 2.11 — Define expected-answer baselines**
Create `data/evaluation_baselines.json` — single file containing all 50 queries with baseline fields. The evaluation harness reads this file directly.
```json
[
  {
    "id": "Q-01",
    "category": "booking",
    "query": "What documents do I need for an FCL export from Singapore?",
    "must_contain": ["bill of lading", "packing list"],
    "should_contain": ["commercial invoice"],
    "must_not_contain": ["import permit"],
    "expected_docs": ["doc_id_1", "doc_id_2"]
  }
]
```
All 50 baselines must be complete before Round 2 runs. Author incrementally (start with top 10 priority queries, extend to all 50) but do not run the harness until all 50 are defined.

**Task 2.12 — Build automated evaluation harness**
Script that hits `POST /api/query` for all 50 queries, capturing:
- Full response text, retrieved chunks, citations, latency
- Runs expected-answer baseline checks (must_contain, must_not_contain, expected docs)
- Calculates metrics: deflection rate, citation accuracy, hallucination rate, OOS handling, avg latency
- **30-second delay between requests** — Groq free tier limits for `llama-3.1-8b-instant`: 30 RPM but only 6,000 TPM. Each query consumes ~3,000 tokens (system prompt + context + query + response), so effective throughput is ~2 req/min. 50 queries ≈ 25 minutes per full run. Daily token budget (500K) supports ~3 full runs per day.
- Delay should be configurable via environment variable (e.g., `EVAL_DELAY_SECONDS=30`) for easy adjustment if tier changes
- Script should handle 429 responses gracefully with exponential backoff

**Task 2.13 — Execute Round 2 and generate reports**
Three output formats:
- `data/evaluation_results.json` — raw results
- `reports/evaluation_report.md` — human-readable report with metrics, per-category breakdown, failure analysis
- `data/evaluation_results.csv` — one row per query (query ID, category, query text, response, expected docs, actual docs, must_contain hits, must_not_contain flags, citation present, latency, pass/fail)

---

## Phase 3: Fix-and-Retest Loop

### Task 3.1 — Failure analysis
For every query failing expected-answer baselines:
- Identify root cause: retrieval miss, hallucination, generation error, missing knowledge, prompt issue
- Prioritize fixes by impact

### Task 3.2 — Apply fixes
- **Prompt tuning** — strengthen citation instructions, reduce hallucination
- **KB content gaps** — add content to documents if critical gaps found
- **Retrieval threshold adjustments** — if good docs aren't surfacing
- **Response formatting** — if answers too verbose or too brief

### Task 3.3 — Re-run evaluation
Re-execute the automated harness. Repeat until targets met or Rishi decides to stop. No day-based time box — Claude Code executes iterations rapidly.

**Targets (must be met to proceed to Phase 4):**

| Metric | Target |
|--------|--------|
| Deflection Rate | ≥ 40% |
| Citation Accuracy | ≥ 80% |
| Hallucination Rate | < 15% |
| OOS Handling | ≥ 90% |
| Avg Latency | < 5s |
| System Stability | No crashes |

All targets are hard gates. Fix loop continues until all are met. No "Min Viable" fallback — if targets cannot be met, escalate to Rishi for scope/approach discussion before proceeding.

**→ CHECKPOINT 3: Round 2 metrics finalized. Rishi reviews before moving to documentation and demo.**

---

## Phase 4: Documentation

### Task 4.1 — Codebase documentation (Layers 2–4)

**Layer 2 — Module READMEs** (5 pointer files):
- `backend/README.md` → links to `documentation/codebase/backend/`
- `client/README.md` → links to `documentation/codebase/frontend/`
- `scripts/README.md` → links to `documentation/codebase/scripts/`
- `tests/README.md` → links to `documentation/codebase/tests/`
- `kb/README.md` → links to `documentation/architecture/kb_schema.md`

**Layer 3 — Detailed codebase docs** (18 files in `documentation/codebase/`):
- `backend/` — overview, services, routes, middleware, config, prompts (6 files)
- `frontend/` — overview, components, api_client (3 files)
- `scripts/` — overview, ingestion, pdf_extraction, evaluation, utilities (5 files)
- `tests/` — overview, backend_tests, python_tests, e2e_tests (4 files)

**Layer 4 — Architecture Decision Records** (6 files in `documentation/adrs/`):
- ADR-001-vector-database.md
- ADR-002-llm-provider.md
- ADR-003-chunk-config.md
- ADR-004-python-node-split.md
- ADR-005-embedding-model.md
- ADR-006-response-ux.md

### Task 4.2 — Architecture documentation (6 files in `documentation/architecture/`)
- `system_overview.md` — final-state architecture, component diagram, tech stack with versions
- `data_flow.md` — end-to-end query flow with sequence diagram
- `ingestion_pipeline_flow.md` — detailed step-by-step ingestion process
- `rag_pipeline_flow.md` — detailed step-by-step RAG process
- `kb_schema.md` — frontmatter schema, categories, chunk metadata
- `api_contract.md` — API endpoints, request/response shapes (new UX)

### Task 4.3 — User-facing guides (3 files in `documentation/guides/`)
- `user_guide.md` — how a CS agent uses the co-pilot (starting system, effective questions, understanding 4-section response, when to escalate)
- `deployment_notes.md` — prerequisites, installation, environment config, commands, troubleshooting
- `known_limitations.md` — no live data, single model, no multi-turn, no auth, query gaps

### Task 4.4 — Documentation index
- `documentation/README.md` — links to all 34 documents with one-line descriptions

### Task 4.5 — Project-level README
- `05_evaluation/README.md` — quick start, architecture overview, folder structure, all commands

### Task 4.6 — POC Evaluation Report
- `reports/poc_evaluation_report.md` — executive summary, metrics (target vs. achieved), what worked, areas for improvement, known limitations, recommendation

### Task 4.7 — Success criteria checklist
- `reports/success_criteria_checklist.md` — Technical, Quality, Documentation checklists populated from test results

### Task 4.8 — Lessons learned (full retrospective)
- `reports/lessons_learned.md` — technical decisions, process effectiveness, what you'd do differently

### Task 4.9 — Phase 2 recommendations
- `reports/phase2_recommendations.md` — light 1-page bullet list based on POC results

---

## Phase 5: Demo Capture & Presentation

### Task 5.1 — Select demo queries
Pick 8–10 queries: 5–7 happy path + 2–3 failure/OOS. Selected after Round 2 testing based on best showcase results and graceful failure examples.
- 1–2 booking/documentation queries
- 1–2 customs/regulatory queries
- 1 carrier information query
- 1 out-of-scope query (graceful decline)
- 1 complex multi-source query (if it works well)
- 2–3 failure/edge case examples

### Task 5.2 — Build Selenium demo script
Selenium dependencies live in `demo/selenium/requirements.txt` (separate from core pipeline `requirements.txt`). Install via `pip install -r demo/selenium/requirements.txt`. Requires `selenium` package + ChromeDriver matching installed Chrome version.

Automated browser script in `demo/selenium/` that:
- Opens Waypoint React frontend (the actual co-pilot UI)
- Types each demo query
- Waits for response
- Captures screenshot at each step (query typed, response displayed)
- All screenshots saved to `demo/presentation/public/demo/screenshots/`
- Separate screen recording (OBS or similar) saved to `demo/presentation/public/demo/recording.mp4`

### Task 5.3 — Record demo
Run Selenium script with screen recording (OBS or similar). Screenshots and video must be captured **before** the presentation app is built — they are static assets embedded in the slides.

### Task 5.4 — Create React presentation app (16 slides, 10 diagrams)

Standalone Vite + React + Tailwind + Framer Motion project in `demo/presentation/`.

**Tech stack:**
- `react`, `react-dom`, `vite` — base
- `tailwindcss` — styling (independent config, not shared with Waypoint client)
- `framer-motion` — slide transitions + animated hero diagrams
- `react-mermaidjs` or `mermaid` — flow diagrams rendered at runtime
- `html2canvas` — PDF export via browser print

**Navigation features:**
- Keyboard arrow keys (left/right) + click navigation
- Progress bar at bottom + slide counter (e.g., "3 / 15")
- Exportable to PDF via browser print / html2canvas fallback

**Diagram approach (mix):**
- **Mermaid** (5–6 diagrams): ingestion pipeline flow, RAG pipeline flow, data flow, data collection flow, KB composition
- **Framer Motion animated SVG/CSS** (3–4 diagrams): tech stack blocks, before/after comparison, metrics dashboard, week-by-week timeline

| Slide | Content | Diagram | Diagram Type |
|-------|---------|---------|-------------|
| 1 | Title — Waypoint Co-Pilot, CYAIRE, date | — | — |
| 2 | Problem statement — fragmented sources, 30+ min research | Pain point visual | Framer Motion SVG |
| 3 | Industry — SEA logistics $390B, Singapore focus, 6 markets | Regional map with stats | Static SVG / image |
| 4 | Solution — RAG co-pilot, before/after | Before/after comparison | Framer Motion animated |
| 5 | Tech stack — ChromaDB, Groq, sentence-transformers, Express, React | Tech stack blocks | Framer Motion animated |
| 6 | Knowledge base — 30 docs, 709 chunks, 4 categories | KB composition chart | Mermaid |
| 7a | Data collection — Claude Code + Chrome DevTools MCP, PDF discovery | Data collection flow | Mermaid |
| 7b | Ingestion pipeline — markdown → chunking → embedding → ChromaDB | Ingestion pipeline flow | Mermaid |
| 8 | RAG pipeline — query → retrieval → generation → citations → response | RAG architecture diagram | Mermaid |
| 9 | Response UX — 4-section card annotated | Mockup with callouts | Screenshot / component |
| 10 | Live demo — Selenium screenshots + embedded video | — | `<img>` + `<video>` |
| 11 | Results & metrics — target vs. achieved | Metrics dashboard | Framer Motion animated |
| 12 | Journey — W1→W2→W3→W4 milestones | Timeline | Framer Motion animated |
| 13 | Known limitations | — | — |
| 14 | Phase 2 recommendations | — | — |
| 15 | Q&A | — | — |

### Task 5.5 — Prepare Q&A responses
Anticipate likely questions about cost, architecture choices, production path, multi-language, TMS integration.

---

## Phase 6: Buffer, Polish & Finalize

### Task 6.1 — Final smoke test
- Start system from cold
- Run all demo queries
- Verify citations render correctly
- Confirm latency within target
- Test error handling (API down, empty query, very long query)

### Task 6.2 — Backup
- Git commit all work
- Confirm ingestion pipeline is reproducible (KB + scripts = complete system)

### Task 6.3 — Update CLAUDE.md
Add Week 4 section to root `CLAUDE.md`:
- Workspace: `pilot_phase1_poc/05_evaluation/`
- Protected paths: `01_knowledge_base/`, `02_ingestion_pipeline/`, `03_rag_pipeline/`, `04_retrieval_optimization/`
- AI workflow: same prompt → review → execute pattern
- Key commands: `npm start`, `cd client && npm run dev`, venv activation, `python scripts/ingest.py`, `python scripts/evaluation_test.py`, `npm test`, `pytest`
- Targets: deflection ≥40%, citation accuracy ≥80%, hallucination <15%, OOS ≥90%, system stability
- Task order: UX redesign → testing → fix loop → documentation → demo
- New deps: Selenium for demo capture, framer-motion + react-mermaidjs + html2canvas for React presentation
- UX reference: mockup artifact as design spec
- Presentation: `demo/presentation/` — `npm run dev` to preview, `npm run build` for static deploy
- Active initiative status: Week 4 complete

---

## Checkpoints

| # | Gate | Condition | Rishi Action |
|---|------|-----------|--------------|
| CP1 | After workspace setup + fresh ingestion | All existing tests pass (pytest + Jest + retrieval 92%) | Review, approve to proceed |
| CP2 | After UX redesign complete | New 4-section response card working in browser | Review in browser, approve to proceed to testing |
| CP3 | After Round 2 + fix loop | Final metrics calculated, targets assessed | Review metrics, approve to proceed to docs/demo |

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| 0 — Setup | 0.1–0.6 | Create folder, copy codebase, fix ingestion metadata, fresh ingestion, run existing tests |
| 1 — UX Redesign | 1.1–1.4 | System prompt, backend pipeline, React frontend (TDD), inline docs |
| 2 — Testing | 2.1–2.13 | 5-layer testing: ingestion, RAG, backend, frontend, E2E evaluation |
| 3 — Fix Loop | 3.1–3.3 | Failure analysis, apply fixes, re-run until targets met |
| 4 — Documentation | 4.1–4.9 | 39 doc files: codebase (4 layers), architecture, guides, ADRs, reports |
| 5 — Demo | 5.1–5.5 | Query selection, Selenium script, demo recording, React presentation (16 slides, Vite + Tailwind + Framer Motion), Q&A prep |
| 6 — Finalize | 6.1–6.3 | Smoke test, backup, CLAUDE.md update |
| **Total** | **~39 tasks** | |

---
