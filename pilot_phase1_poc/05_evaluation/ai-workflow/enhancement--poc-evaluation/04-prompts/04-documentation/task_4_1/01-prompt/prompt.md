# Task 4.1 Prompt — Codebase Documentation (Layers 2-4)

## Persona
Technical writer producing comprehensive codebase documentation for a RAG-based freight forwarding co-pilot. You understand the full stack (Python ingestion, Node.js backend, React frontend) and can explain both what the code does and why it was built that way.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Task**: 4.1 — Codebase documentation (Layers 2-4)
- **Phase**: 4 (Documentation)
- **Dependencies**: CP3 (PASSED — all 6 evaluation targets met)
- **Blocks**: T4.4 (Documentation index)
- **Workspace**: `pilot_phase1_poc/05_evaluation/`

### Documentation Layer Model (Decision #24)
| Layer | Type | Location | Purpose |
|-------|------|----------|---------|
| Layer 1 | Inline (JSDoc/docstrings) | In source files | Already done (T1.4) |
| Layer 2 | Pointer READMEs | In code folders | Brief summary + link to detailed docs |
| Layer 3 | Detailed codebase docs | `documentation/codebase/` | Full module documentation |
| Layer 4 | ADRs | `documentation/adrs/` | Architecture decision records |

### Codebase to Document

**Backend** (`backend/`):
- `config.js` — Environment config (ChromaDB, Groq, thresholds)
- `index.js` — Express server entry point
- `middleware/` — Error handler, request logger
- `prompts/system.txt` — LLM system prompt (T1.1 formatting + T3.2 citation MANDATORY)
- `routes/api.js` — POST /api/query endpoint
- `services/citations.js` — Citation extraction + source building
- `services/embedding.js` — ONNX embedding bridge
- `services/index.js` — Service barrel export
- `services/llm.js` — Groq LLM client (retry, buildSystemPrompt)
- `services/pipeline.js` — Query orchestrator (retrieve → generate → cite → confidence)
- `services/retrieval.js` — ChromaDB query via Python subprocess
- `utils/logger.js` — Winston logger

**Frontend** (`client/src/`):
- `App.jsx` — Main app shell (header, query input, response card)
- `main.jsx` — React entry point
- `api/queryApi.js` — Fetch wrapper for /api/query
- `components/QueryInput.jsx` — Search bar with submit handling
- `components/ResponseCard.jsx` — 4-section response card (answer, sources, related, confidence)
- `components/SourcesSection.jsx` — Sources list with org grouping
- `components/RelatedDocsSection.jsx` — Related documents panel
- `components/ConfidenceFooter.jsx` — Confidence indicator (High/Medium/Low)
- `components/Loading.jsx` — Loading skeleton

**Scripts** (`scripts/`):
- `ingest.py` — Main ingestion entry point (--clear flag)
- `process_docs.py` — Markdown parsing, frontmatter extraction, discover_documents()
- `chunker.py` — Text chunking (600/90 config)
- `config.py` — Python-side config (paths, chunk params)
- `pdf_extractor.py` — PDF text extraction utility
- `query_chroma.py` — JSON stdin → ChromaDB query → JSON stdout (Node.js bridge)
- `retrieval_quality_test.py` — 50-query hit rate test (92% baseline)
- `evaluation_harness.py` — Automated 50-query evaluation (6 metrics, citation applicable logic)
- `verify_ingestion.py` — Post-ingestion chunk count + metadata checks
- `view_chroma.py` — Debug utility to inspect ChromaDB contents

**Tests** (`tests/`):
- `api.test.js` — Express API endpoint tests (11 tests)
- `pipeline.test.js` — Pipeline orchestrator tests (19 tests)
- `retrieval.test.js` — Retrieval service tests (15 tests)
- `llm.test.js` — LLM service tests (18 tests)
- `citations.test.js` — Citation service tests (47 tests)
- `generation.test.js` — Generation layer tests (50 tests)
- `placeholder.test.js` — Placeholder tests (2 tests)
- `e2e_node/` — Node E2E test directory
- `test_metadata_preservation.py` — Python metadata tests
- `test_pdf_extractor.py` — PDF extractor tests (22 tests)
- Python ingestion/retrieval tests in `scripts/` pytest discovery

## Task

Create **29 documentation files** across three layers. Read the actual source files before writing docs — do not guess or hallucinate code details.

### Deliverable 1: Layer 2 — Pointer READMEs (5 files)

Create brief README.md files in each code folder. Each should contain:
- 1-2 sentence module description
- File listing with one-line descriptions
- Link to detailed docs: `See [detailed documentation](../documentation/codebase/<module>/overview.md)`
- Key commands (if applicable)

Files:
1. `backend/README.md` — Backend API overview
2. `client/README.md` — Frontend overview (NOTE: file exists from Vite scaffold — replace content)
3. `scripts/README.md` — Python scripts overview
4. `tests/README.md` — Test suite overview
5. `kb/README.md` — Knowledge base overview + link to `documentation/architecture/kb_schema.md`

### Deliverable 2: Layer 3 — Detailed Codebase Docs (18 files)

Create in `documentation/codebase/`. Each file should include:
- Module purpose and responsibility
- File-by-file breakdown (public API, key functions, parameters, return types)
- Configuration options
- Dependencies (internal + external)
- Usage examples where relevant

**Backend** (6 files):
1. `documentation/codebase/backend/overview.md` — Architecture, request flow, middleware stack
2. `documentation/codebase/backend/services.md` — All 6 services: pipeline, retrieval, llm, citations, embedding, index
3. `documentation/codebase/backend/routes.md` — API endpoints, request/response schema
4. `documentation/codebase/backend/middleware.md` — Error handler, request logger
5. `documentation/codebase/backend/config.md` — Environment variables, defaults, config.js
6. `documentation/codebase/backend/prompts.md` — System prompt structure, citation rules, OOS handling

**Frontend** (3 files):
7. `documentation/codebase/frontend/overview.md` — Component tree, state management, styling
8. `documentation/codebase/frontend/components.md` — Each component: props, behavior, rendering logic
9. `documentation/codebase/frontend/api_client.md` — queryApi.js: endpoint, error handling, response parsing

**Scripts** (5 files):
10. `documentation/codebase/scripts/overview.md` — Script categories, Python environment, common patterns
11. `documentation/codebase/scripts/ingestion.md` — ingest.py + process_docs.py + chunker.py pipeline
12. `documentation/codebase/scripts/pdf_extraction.md` — pdf_extractor.py usage, output format
13. `documentation/codebase/scripts/evaluation.md` — evaluation_harness.py: metrics, checks, citation applicable logic, report generation
14. `documentation/codebase/scripts/utilities.md` — query_chroma.py, verify_ingestion.py, view_chroma.py, config.py

**Tests** (4 files):
15. `documentation/codebase/tests/overview.md` — Test pyramid, coverage summary (55 pytest + 162 Jest)
16. `documentation/codebase/tests/backend_tests.md` — Jest test files: what each covers, mock patterns
17. `documentation/codebase/tests/python_tests.md` — pytest files: ingestion, metadata, PDF, retrieval
18. `documentation/codebase/tests/e2e_tests.md` — E2E approach (Chrome DevTools MCP visual verification)

### Deliverable 3: Layer 4 — Architecture Decision Records (6 files)

Create in `documentation/adrs/`. Use standard ADR format:
```markdown
# ADR-NNN: [Title]
**Status**: Accepted
**Date**: [When decision was made]
**Context**: [Why this decision was needed]
**Decision**: [What was decided]
**Alternatives Considered**: [What else was evaluated]
**Consequences**: [Positive and negative impacts]
```

ADRs to create:
1. `ADR-001-vector-database.md` — ChromaDB selection (vs Pinecone, Weaviate, pgvector)
2. `ADR-002-llm-provider.md` — Groq + Llama 3.1 8B (vs OpenAI, local Ollama, Claude)
3. `ADR-003-chunk-config.md` — 600/90 chunk size + top_k=5 retrieval (tested 400/60, 800/120, 1000/150 chunk configs and top_k=10 — all performed equal or worse. Content fixes >> parameter tuning. Decision #10 from Week 3 Task 8)
4. `ADR-004-python-node-split.md` — Hybrid Python/Node architecture (Python ingestion, Node API)
5. `ADR-005-embedding-model.md` — all-MiniLM-L6-v2 via ONNX (ChromaDB default, no GPU needed)
6. `ADR-006-response-ux.md` — 4-section response card design (Decision #9 from Week 4)

### Key Source Files to Read

Read these files to extract accurate documentation content:

| Priority | File | Purpose |
|----------|------|---------|
| HIGH | `backend/services/pipeline.js` | Core orchestration — confidence scoring, query flow |
| HIGH | `backend/services/retrieval.js` | ChromaDB bridge — subprocess, formatContext |
| HIGH | `backend/services/llm.js` | LLM client — buildSystemPrompt, retry logic |
| HIGH | `backend/services/citations.js` | Citation parsing — processCitations, buildSources |
| HIGH | `backend/config.js` | All config values and defaults |
| HIGH | `backend/routes/api.js` | API contract — request/response schema |
| HIGH | `backend/prompts/system.txt` | Full system prompt text |
| HIGH | `scripts/evaluation_harness.py` | Evaluation: checks, metrics, citation applicable |
| HIGH | `scripts/process_docs.py` | Doc processing: frontmatter, discover_documents |
| HIGH | `scripts/chunker.py` | Chunking algorithm |
| MED | `scripts/ingest.py` | Ingestion entry point |
| MED | `scripts/query_chroma.py` | JSON stdin/stdout bridge |
| MED | `client/src/App.jsx` | App shell and state |
| MED | `client/src/components/ResponseCard.jsx` | 4-section card |
| MED | `client/src/api/queryApi.js` | API client |
| LOW | `backend/middleware/` | Error handler, logger |
| LOW | `backend/utils/logger.js` | Winston config |
| LOW | Remaining test files | For test docs |

### Reference Documents for ADRs

| ADR | Source |
|-----|--------|
| ADR-001 | `00_docs/04_technical_architecture.md` — vector DB selection |
| ADR-002 | `00_docs/04_technical_architecture.md` — LLM provider |
| ADR-003 | `04_retrieval_optimization/ai-workflow/.../task_8_fix_failures_parameter_experiments/02-output/REPORT.md` (experiment matrix: 600/90/5 vs 800/120/5 vs 1000/150/5 vs 400/60/5 vs 600/90/10) AND `04_retrieval_optimization/reports/04_final_comparison.md` (conclusion: "600/90/top_k=5 is optimal") |
| ADR-004 | `00_docs/04_technical_architecture.md` — hybrid architecture |
| ADR-005 | `00_docs/04_technical_architecture.md` — embedding model |
| ADR-006 | `05_evaluation/ai-workflow/.../01-plan/DETAILED_PLAN.md` — Decision #9 |

## Execution Strategy

This is a large task (29 files). Execute in this order:
1. **Read all HIGH priority source files first** — build mental model before writing
2. **Layer 2 pointer READMEs** (5 files) — fast, establishes structure
3. **Layer 3 backend docs** (6 files) — most complex, do first
4. **Layer 3 scripts docs** (5 files) — second most complex
5. **Layer 3 frontend docs** (3 files) — simpler (fewer files)
6. **Layer 3 tests docs** (4 files) — reference test files
7. **Layer 4 ADRs** (6 files) — reference planning docs
8. **Verify all internal links** — pointer READMEs → detailed docs

## Validation
- [ ] 5 pointer READMEs created with correct links
- [ ] 18 detailed codebase docs created (6 backend + 3 frontend + 5 scripts + 4 tests)
- [ ] 6 ADR files created in standard format
- [ ] All internal links resolve correctly
- [ ] Each ADR covers: context, decision, alternatives considered, consequences
- [ ] Documentation reflects actual code (not guessed — source files were read)
- [ ] Total: 29 files created

## Output

Create output report: `04-prompts/04-documentation/task_4_1/02-output/TASK_4.1_OUTPUT.md`

## Update on Completion

**MANDATORY — Update ALL 7 tracking locations:**
1. **Checklist**: `03-checklist/IMPLEMENTATION_CHECKLIST.md` — mark T4.1 `[x]`, update Phase 4 progress (1/9), Total (29/45, 64%)
2. **Roadmap Progress Tracker**: Phase 4 → `1 | 1`, Total → `29 | 64%`
3. **Roadmap Quick Reference**: T4.1 → `✅ Complete`
4. **Roadmap Detailed Entry**: T4.1 Status → `✅ Complete`, validation checkboxes `[x]`
5. **Bootstrap file**: `ai-workflow-bootstrap-prompt-v3.md` → `29/45 -- 64%`
6. **CLAUDE.md** (root): → `29/45 — 64%`
7. **AGENTS.md** (root): → `29/45 -- 64%`
