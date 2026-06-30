# Waypoint Co-Pilot Evaluation Codebase Review

---

## 1. Document Metadata

- **Project:** Waypoint Co-Pilot
- **Target folder:** `pilot_phase1_poc/05_evaluation`
- **Review date:** 2026-06-28
- **Reviewer:** Codex
- **Scope:** Backend API, React client, Python ingestion/retrieval/evaluation scripts, knowledge base structure, tests, reports, documentation, demo artifacts, and Week 4 workflow records.
- **Out of scope:** Full 50-query live LLM evaluation rerun. This review uses the existing Round 4 live evaluation artifacts and reruns local non-LLM validation.

## 2. Executive Summary

- **What the system does:** `05_evaluation` is the final Phase 1 POC package for a freight-forwarding RAG co-pilot. It ingests a curated logistics knowledge base into ChromaDB, exposes an Express `/api/query` endpoint, retrieves relevant chunks through a Python subprocess bridge, calls Groq/Llama through an OpenAI-compatible client, extracts citations, and renders a 4-section React response card.
- **Current maturity:** Strong POC / evaluation-ready prototype. It is well documented and test-heavy, but it still has production gaps around portability, authentication, provider fallback, live integrations, and evaluation methodology.
- **Primary strengths:** Clear subsystem boundaries, strong documentation, repeatable evaluation artifacts, and broad unit/component test coverage.
- **Primary risks:** Python subprocess bridge is Windows-specific, confidence and evaluation metrics can overstate quality, retrieval edge cases remain, and there is no production-grade security or operational control plane.
- **Bottom line:** This is a credible final POC codebase and a good base for Phase 2. It should not be treated as production-ready without replacing or hardening the subprocess bridge, adding auth/rate limits/logging, recalibrating evaluation, and improving retrieval regressions.

## 3. Repository Map

| Path | Role | Notes |
| --- | --- | --- |
| `backend/` | Express API and RAG orchestration | Main user-facing API. Clean service split, but ChromaDB access is delegated to a Windows-specific Python subprocess. |
| `client/` | React/Vite UI | 4-section response card with answer, sources, related documents, and confidence footer. Component tests are present. |
| `scripts/` | Python ingestion, retrieval, PDF extraction, evaluation | Owns ChromaDB ingestion, quality checks, and report generation. This is the data and evaluation backbone. |
| `tests/` | Jest and pytest tests | 162 backend/service tests and 55 Python tests passed locally. E2E node helpers exist but are not collected as regular pytest tests. |
| `kb/` | Frozen 30-document knowledge base | 4 categories, 709 ingested chunks, PDF extracts excluded from ingestion. |
| `documentation/` | Architecture, ADRs, codebase docs, guides | Very complete for a POC. Now includes this review report and the reusable review template. |
| `reports/` | Evaluation outputs and retrospectives | Contains Round 4 metrics, failure analysis, success checklist, lessons learned, and Phase 2 recommendations. |
| `data/` | JSON/CSV evaluation data | Contains baselines, retrieval results, and full evaluation outputs. |
| `demo/` | Presentation and Selenium demo captures | Useful stakeholder/demo layer, separate from runtime app. |
| `ai-workflow/` | Prompt-review-execute workflow history | Strong process trace with prompts, outputs, and checkpoint reviews. |

## 4. System Overview

- **User entry points:** React client at Vite dev server, Express API at `/api/query` and `/api/health`, Python scripts for ingestion/evaluation, and demo presentation assets.
- **Backend responsibilities:** Request validation, pipeline orchestration, retrieval invocation, LLM call, citation enrichment, confidence calculation, and API response shaping.
- **Frontend responsibilities:** Query input, loading/error states, markdown answer rendering, source links, related document chips, and confidence metadata display.
- **Python responsibilities:** Discover and parse markdown KB files, chunk documents, write ChromaDB records, query ChromaDB, verify ingestion, run retrieval quality tests, and run the 50-query evaluation harness.
- **Data stores:** `kb/` markdown files, `chroma_db/` persistent ChromaDB collection, `data/*.json`, `data/*.csv`, `reports/*.md`, and logs.
- **External services:** Groq API via the OpenAI SDK client. ChromaDB embeddings run locally through ChromaDB's default ONNX embedding function.

## 5. How It Works

### 5.1 Request Flow

1. The user submits a question in `client/src/App.jsx`.
2. `client/src/api/query.js` sends `POST /api/query` with `{ query }`.
3. `backend/routes/query.js` validates the payload and calls `processQuery()`.
4. `backend/services/pipeline.js` calls `retrieveChunks()`, formats context, calls the LLM, extracts citations, builds sources and related docs, and calculates confidence.
5. `backend/services/retrieval.js` spawns `scripts/query_chroma.py`, passing query params through stdin and reading JSON from stdout.
6. `backend/services/llm.js` builds the system prompt with retrieved context and calls Groq.
7. The API returns `{ answer, sources, relatedDocs, citations, confidence, metadata }`.
8. `ResponseCard.jsx` renders the answer, source links, related document chips, and confidence footer.

### 5.2 Data Flow

- **Input data:** Markdown KB documents with YAML frontmatter under `kb/`.
- **Transformations:** `process_docs.py` parses frontmatter and content; `chunker.py` splits text into chunks; `ingest.py` stores text and metadata in ChromaDB; `query_chroma.py` retrieves chunks; backend formats chunks into LLM context.
- **Outputs:** API JSON responses, frontend response card, evaluation JSON, evaluation CSV, evaluation report markdown, retrieval quality report, and success criteria checklist.
- **Persistence:** ChromaDB persists vector data in `chroma_db/`; evaluation outputs persist in `data/` and `reports/`.

### 5.3 Control Flow

- **Happy path:** Valid query -> chunks found -> context built -> LLM answer -> citations extracted -> source/related-doc arrays built -> response rendered.
- **Validation/error path:** Empty, non-string, oversized, malformed, or failed pipeline requests return structured HTTP errors through Express middleware.
- **Fallback path:** LLM retry logic handles 429, 5xx, `ECONNRESET`, and `ETIMEDOUT` with exponential backoff.
- **Out-of-scope path:** If retrieval returns no chunks, the pipeline returns a polite no-results response without calling the LLM.

## 6. Component Breakdown

### 6.1 Backend

- **Entry point:** `backend/index.js`
- **Core services:** `backend/services/pipeline.js`, `backend/services/retrieval.js`, `backend/services/llm.js`, `backend/services/citations.js`
- **Routes:** `backend/routes/query.js`, `backend/routes/health.js`
- **Config:** `backend/config.js`
- **Prompting:** `backend/prompts/system.txt`
- **Observed design decisions:** Service boundaries are clear. The API contract is intentionally shaped for the 4-section frontend. Retrieval stays in Python to reuse ChromaDB/local embedding tooling.
- **Issues or gaps:** The Python bridge is hardcoded to `venv/Scripts/python.exe` and does not actually iterate over fallback Python commands. There is also no subprocess timeout, so a stuck query script can hang an API request.

### 6.2 Frontend

- **Component tree:** `App.jsx` -> `QueryInput`, `Loading`, `ResponseCard` -> `SourcesSection`, `RelatedDocsSection`, `ConfidenceFooter`.
- **State flow:** `App.jsx` owns `response`, `loading`, and `error`; `QueryInput` emits a trimmed query; `submitQuery()` calls the API.
- **Response rendering:** `ResponseCard.jsx` uses `react-markdown` and `remark-gfm` for answer formatting.
- **Styling system:** Tailwind classes, with compact operational UI styling.
- **Observed design decisions:** The UX mirrors the evaluation target: answer, sources, related documents, confidence. This is much stronger than a raw chatbot transcript for source-grounded support work.
- **Issues or gaps:** AbortController is created per submit but not retained or used for cancellation on new submissions/unmount. Slow overlapping requests can race and show stale responses. The confidence footer can crowd on narrow screens because it uses a single `justify-between` row with unbounded reason text and stats.

### 6.3 Scripts

- **Ingestion:** `scripts/ingest.py`, `scripts/process_docs.py`, `scripts/chunker.py`
- **Chunking:** `scripts/chunker.py` with `RecursiveCharacterTextSplitter`, 600 char chunks, 90 char overlap.
- **Evaluation harness:** `scripts/evaluation_harness.py`
- **PDF extraction:** `scripts/pdf_extractor.py`
- **Utility scripts:** `scripts/query_chroma.py`, `scripts/verify_ingestion.py`, `scripts/view_chroma.py`, `scripts/retrieval_quality_test.py`
- **Observed design decisions:** The scripts are the strongest reproducibility layer in the repo. They can rebuild the vector store, inspect retrieval, verify ingestion, and regenerate evaluation reports.
- **Issues or gaps:** The evaluation harness is keyword-based and can pass/penalize based on string presence rather than semantic correctness. The dry-run found 11 in-scope baselines with fewer than two `must_contain` keywords.

### 6.4 Tests

- **Backend tests:** `tests/api.test.js`, `tests/pipeline.test.js`, `tests/retrieval.test.js`, `tests/llm.test.js`, `tests/citations.test.js`, `tests/generation.test.js`
- **Python tests:** `tests/test_metadata_preservation.py`, `tests/test_pdf_extractor.py`
- **Frontend tests:** `client/src/components/__tests__/*.test.jsx`
- **What the tests protect:** API validation, response shape, service orchestration, citation matching, generation retries, context formatting, metadata preservation, PDF extraction, and component rendering.
- **What is not covered:** Live LLM behavior, live 50-query evaluation in CI, real browser layout regression, concurrent frontend request races, production deployment paths, and security controls.

### 6.5 Knowledge Base

- **Content structure:** `01_regulatory`, `02_carriers`, `03_reference`, `04_internal_synthetic`.
- **Metadata schema:** Title, source organization, source URLs, source type, last updated, jurisdiction, category, use cases, retrieval keywords.
- **Ingestion assumptions:** Markdown docs outside `pdfs/` are ingested; PDF extract markdown is reference material and excluded.
- **Constraints:** KB is frozen for evaluation. It is intentionally static and does not update regulatory/carrier content automatically.

### 6.6 Documentation and Workflow

- **Docs structure:** `documentation/architecture`, `documentation/codebase`, `documentation/adrs`, `documentation/guides`.
- **Workflow rules:** `ai-workflow/enhancement--poc-evaluation` captures prompt-review-execute outputs and checkpoint reviews.
- **Operational guidance:** Root README and pointer READMEs give setup commands and link deeper docs. ADRs document major POC design choices.

## 7. Evaluation Process

### 7.1 Setup

- **Prerequisites:** Node.js, Python 3.11 venv, installed npm packages, installed Python requirements, `.env` with `LLM_API_KEY` for live LLM runs, populated `chroma_db/`.
- **How to start the stack:** `npm start` from `05_evaluation`; `npm run dev` from `client`.
- **How to prepare data:** `venv\Scripts\python.exe scripts\ingest.py --clear`

### 7.2 Automated Checks

- **Ingestion checks:** `scripts/verify_ingestion.py` validates total chunk count, category distribution, metadata integrity, and three retrieval tiers.
- **Unit tests:** `npm test -- --runInBand`, `venv\Scripts\python.exe -m pytest tests -v`, and `client\npm test`.
- **Integration checks:** Existing Round 4 evaluation artifacts run through the live API and capture 50 query responses.
- **Evaluation harness:** `scripts/evaluation_harness.py` calculates deflection, citation accuracy, hallucination rate, OOS handling, latency, and stability.

### 7.3 Metrics

| Metric | Target | Current Result | Evidence |
| --- | --- | --- | --- |
| Deflection rate | >= 40% | 87.2% | `reports/evaluation_report.md`, Round 4 |
| Citation accuracy | >= 80% | 96.0% adjusted, 97.4% raw | `reports/evaluation_report.md`, Round 4 |
| Hallucination rate | < 15% | 2.0% | `reports/evaluation_report.md`, noted as Q-39 measurement artifact |
| Out-of-scope handling | >= 90% | 100.0% | `reports/evaluation_report.md`, 11/11 OOS |
| Latency | < 5000ms average | 1182ms average, 100% under 5s | `reports/evaluation_report.md` |
| Stability | No crashes | 50/50 successful | `reports/evaluation_report.md` |
| Retrieval hit rate | >= 75% | 92.0% in current rerun | `scripts/retrieval_quality_test.py` rerun on 2026-06-28 |

### 7.4 Checkpoints

- **Checkpoint 1:** Workspace setup, fresh ingestion, and baseline tests before UX changes.
- **Checkpoint 2:** 4-section UX implementation and browser review.
- **Checkpoint 3:** Round 2/Round 3/Round 4 evaluation and fix loop before documentation/demo.
- **Any blockers:** Early citation failures, baseline mismatch, low confidence skew, and retrieval misses were the main blockers. These are documented in `reports/failure_analysis.md`.

## 8. Design Decisions

| Decision | Why it was chosen | Tradeoff | Evidence |
| --- | --- | --- | --- |
| ChromaDB local vector store | Simple local POC deployment, no managed vector DB dependency | Not production-scalable as a local file store | `documentation/adrs/ADR-001-vector-database.md` |
| Groq + Llama 3.1 8B | Low-cost, fast inference, OpenAI-compatible SDK | Single external provider, no failover | `documentation/adrs/ADR-002-llm-provider.md` |
| 600/90 chunking | Best tested balance of precision and context | Still sensitive to query phrasing and table fragmentation | `documentation/adrs/ADR-003-chunk-config.md` |
| Python ingestion/query + Node API | Python has better ChromaDB/NLP tooling, Node is ergonomic for API/UI | Subprocess bridge adds portability and latency risk | `documentation/adrs/ADR-004-python-node-split.md` |
| all-MiniLM-L6-v2 default embeddings | Local, no API key, fast enough for POC | Weaker domain matching than larger or specialized embeddings | `documentation/adrs/ADR-005-embedding-model.md` |
| 4-section response card | Makes answer provenance and confidence visible | Requires backend response enrichment and citation compliance | `documentation/adrs/ADR-006-response-ux.md` |

## 9. What Went Well

- **The project is unusually well documented for a POC.** Evidence: 39 documentation files after adding this review/template, plus pointer READMEs. Impact: A new engineer can orient quickly.
- **The evaluation package is reproducible.** Evidence: `verify_ingestion.py` passed 33/33 checks; retrieval quality rerun produced 709 chunks and 92.0% hit rate. Impact: The POC is not just a demo recording.
- **Testing is broad across languages.** Evidence: 162 Jest, 55 pytest, and 33 Vitest tests passed locally. Impact: Most service contracts and UI sections have guardrails.
- **The 4-section response UX is the right shape for support work.** Evidence: `ResponseCard.jsx`, `SourcesSection.jsx`, `RelatedDocsSection.jsx`, `ConfidenceFooter.jsx`. Impact: Users can inspect answer, sources, supporting docs, and confidence separately.
- **The workflow history is inspectable.** Evidence: `ai-workflow/enhancement--poc-evaluation`. Impact: The project has an audit trail of prompts, outputs, and checkpoints.

## 10. What Did Not Go Well

- **Python bridge portability is weak.** Evidence: `backend/services/retrieval.js:20-43` hardcodes `venv/Scripts/python.exe`; the fallback list is declared but unused. Risk: This breaks on macOS/Linux and on Windows machines without the expected venv path. Severity: High for multi-machine use.
- **The API can hang on a stuck Python subprocess.** Evidence: `backend/services/retrieval.js:43-80` spawns the process and waits for close without timeout/kill handling. Risk: ChromaDB or Python hangs can consume API capacity indefinitely. Severity: High for production-like use.
- **Evaluation metrics are useful but not definitive.** Evidence: `evaluation_harness.py:357-360` checks keyword presence, expected doc IDs, and citation presence; dry-run warned that 11 in-scope queries have fewer than two `must_contain` terms. Risk: A response can pass with shallow keyword coverage or fail for correct paraphrase. Severity: Medium.
- **Confidence is not well calibrated.** Evidence: Round 4 has 43/50 Low confidence in `documentation/guides/known_limitations.md` and `reports/evaluation_report.md`, even though aggregate quality gates pass. Risk: Users may ignore good answers or distrust the system. Severity: Medium.
- **Frontend request cancellation is incomplete.** Evidence: `client/src/App.jsx:19-35` creates an AbortController per request but does not retain or abort it. Risk: Overlapping slow requests can race and overwrite newer state. Severity: Medium.
- **Live system controls are absent.** Evidence: Known limitations list no auth, no rate limiting, no query persistence, and no audit trail. Risk: Cannot safely expose outside local/internal demo use. Severity: High for deployment.

## 11. Regression-Level Critique

### 11.1 High-Risk Regression Areas

- Python subprocess retrieval bridge: path assumptions, process lifetime, stdout JSON parsing, and ChromaDB compatibility.
- Citation format compliance: source rendering depends on the LLM emitting bracket citations that match chunk titles.
- Evaluation baselines: keyword and doc-id expectations can drift from actual KB content.
- Knowledge base edits: adding content requires re-ingestion and can shift retrieval rankings unpredictably.
- Frontend response contract: sources, related docs, citations, confidence, and metadata must stay aligned with backend shape.

### 11.2 Likely Regression Modes

- A repo clone on another machine fails because `venv/Scripts/python.exe` does not exist.
- A ChromaDB query hangs and leaves the API request open.
- An LLM answer is correct but lacks bracket citations, causing empty sources.
- A KB document update changes retrieval ranking and breaks previously passing queries.
- An evaluation pass looks strong because broad keyword checks do not test answer completeness.
- A user submits two queries quickly and sees the slower first response overwrite the newer response.

### 11.3 Missing Safeguards

- Cross-platform Python path resolution and subprocess timeout tests.
- CI job that runs ingestion verification and retrieval quality on a clean clone.
- Semantic or human-reviewed evaluation layer to complement keyword checks.
- Browser screenshot/visual regression test for narrow mobile layouts.
- API rate limiting, auth, request IDs, persistent query logs, and audit trail.
- Provider fallback tests for Groq outage or model unavailability.

## 12. Improvement Recommendations

### 12.1 Quick Wins

- Add a configurable `PYTHON_PATH` env var and actually iterate fallback Python commands.
- Add a subprocess timeout and kill path in `retrieveChunks()`.
- Add a frontend in-flight request ref to abort prior requests and prevent stale responses.
- Add a dry-run quality gate that fails if in-scope baselines have too few required checks.
- Recalibrate confidence thresholds based on actual score distribution.

### 12.2 Medium Effort

- Add a persistent local Python service or ChromaDB HTTP server instead of spawning Python per query.
- Add query/result logging with request IDs for traceability.
- Add semantic evaluation using LLM-as-judge or human review sampling for the 50-query suite.
- Add regression tests for representative retrieval misses from Round 4 and the current 92% retrieval rerun.
- Add visual regression screenshots for the response card at desktop and mobile widths.

### 12.3 Structural Improvements

- Replace local ChromaDB file storage with managed vector infrastructure or a deployable Chroma service for Phase 2.
- Add authentication, authorization, rate limiting, and tenant separation.
- Add live data adapters for shipment tracking, rates, bookings, and TMS/WMS status behind a stable contract.
- Add multi-turn session memory with explicit citation boundaries.
- Build a content refresh pipeline for regulatory and carrier data.

## 13. Open Questions

- Should Phase 2 preserve ChromaDB or move directly to a managed vector store?
- Should Groq remain the primary provider, or should Phase 2 introduce fallback to OpenAI/Anthropic?
- What is the expected deployment target: local demo, internal server, or customer-facing pilot?
- Which queries should become permanent regression fixtures from Round 4 and the current retrieval rerun?
- Should the evaluation harness report "correct decline" separately from deflection for in-scope-but-missing-content queries?

## 14. Evidence Appendix

| Evidence Type | Reference | Notes |
| --- | --- | --- |
| File | `backend/services/pipeline.js` | Main RAG orchestration and confidence calculation. |
| File | `backend/services/retrieval.js` | Python subprocess bridge and ChromaDB query path. |
| File | `backend/services/llm.js` | Groq/OpenAI-compatible client, prompt construction, retry logic. |
| File | `backend/services/citations.js` | Citation extraction, fuzzy matching, sources, related docs. |
| File | `client/src/App.jsx` | Frontend query state and API submission. |
| File | `client/src/components/ResponseCard.jsx` | 4-section response rendering. |
| File | `scripts/ingest.py` | Reproducible ChromaDB ingestion. |
| File | `scripts/evaluation_harness.py` | 50-query evaluation metrics and report writing. |
| File | `reports/evaluation_report.md` | Round 4 final live evaluation metrics. |
| File | `reports/failure_analysis.md` | Root cause analysis from Round 2. |
| Command | `npm test -- --runInBand` | 162 Jest tests passed. |
| Command | `venv\Scripts\python.exe -m pytest tests -v` | 55 pytest tests passed, 1 collection warning. |
| Command | `cd client; npm test` | 33 Vitest tests passed. |
| Command | `venv\Scripts\python.exe scripts\verify_ingestion.py` | 33/33 ingestion verification checks passed. |
| Command | `venv\Scripts\python.exe scripts\retrieval_quality_test.py` | 50-query retrieval rerun produced 92.0% hit rate. |
| Command | `venv\Scripts\python.exe scripts\evaluation_harness.py --dry-run` | Baselines loaded; warning for 11 in-scope queries with fewer than 2 `must_contain` terms. |

## 15. Final Verdict

- **Overall assessment:** The `05_evaluation` folder is a strong final POC package. It combines working code, reproducible data, automated tests, evaluation evidence, ADRs, user docs, and demo material. Its structure is better than many prototypes because the evaluation artifacts are first-class, not an afterthought.
- **Recommended next steps:** Harden the Python bridge, improve evaluation semantics, fix frontend request races, add production controls, and promote the highest-value failed/edge queries into permanent regression fixtures.
- **If I had one week to improve this codebase:** I would replace the one-shot Python subprocess path with a configurable, timeout-protected bridge; add CI for ingestion verification, retrieval quality, Jest, pytest, and Vitest; recalibrate confidence; and add semantic review to the 50-query evaluation suite.

