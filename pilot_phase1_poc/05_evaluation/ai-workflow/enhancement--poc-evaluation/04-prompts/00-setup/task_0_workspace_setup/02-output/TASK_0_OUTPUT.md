# Task 0 Output Report: Workspace Setup

**Task:** 0 — Workspace Setup (Sub-tasks 0.1–0.6)
**Phase:** Phase 0 — Setup
**Executed:** 2026-02-09
**Status:** ✅ COMPLETE

---

## Summary

Created the `05_evaluation/` workspace by forking the Week 3 codebase, fixing the ingestion pipeline to store `source_urls`, `retrieval_keywords`, and `use_cases` in ChromaDB metadata, running a fresh ingestion (30 docs, 709 chunks), and validating all existing tests pass. Retrieval hit rate improved from 92% (Week 3) to 94% on fresh ingestion.

---

## Folder Structure

```
pilot_phase1_poc/05_evaluation/
├── ai-workflow/                  # Week 4 workflow (enhancement--poc-evaluation)
├── backend/                      # Express API server (copied from W3)
├── client/                       # React frontend (copied from W3)
├── kb/                           # Knowledge base — 30 docs, 4 categories
├── scripts/                      # Python ingestion + evaluation scripts
├── tests/                        # Unit + E2E tests (Python + Jest)
├── chroma_db/                    # Vector store (built fresh — 709 chunks)
├── data/                         # Test results (retrieval_test_results.json)
├── logs/                         # System logs
├── reports/                      # retrieval_quality_REPORT.md
├── documentation/                # (empty — to be filled in Phase 4)
│   ├── adrs/
│   ├── architecture/
│   ├── codebase/
│   └── guides/
├── demo/                         # (empty — to be filled in Phase 5)
│   ├── presentation/
│   └── selenium/
├── .env / .env.example / .gitignore
├── package.json / package-lock.json
├── jest.config.js / requirements.txt
├── start.ps1 / start.sh
└── week4_plan.md
```

---

## Copy Manifest

### Copied from `04_retrieval_optimization/`
- `backend/` — Express server (services, routes, middleware, prompts, utils)
- `client/` — React frontend (src, public, package.json)
- `kb/` — 30 documents across 4 categories + pdfs/ reference
- `scripts/` — ingest.py, process_docs.py, chunker.py, config.py, pdf_extractor.py, retrieval_quality_test.py, query_chroma.py, verify_ingestion.py
- `tests/` — 6 Jest test files + Python test files + e2e_node/
- `data/` — retrieval_test_results.json
- Root configs: .env, .env.example, .gitignore, package.json, package-lock.json, jest.config.js, requirements.txt, start.ps1, start.sh

### Excluded (per Decision #2)
- `ai-workflow/` — W3 workflow
- `ai-workflow-bootstrap-prompt-v3.md` — W3 bootstrap
- `Retrieval_Optimization_Plan.md` — W3 planning
- `REVISED_DOCUMENT_LIST.md` — W3 tracker
- `reports/` — W3 reports (retrieval quality report regenerated fresh)
- `chroma_db/` — rebuilt fresh via ingestion
- `venv/` — recreated
- `node_modules/` — reinstalled

---

## Metadata Fix

### Files Modified

**`scripts/process_docs.py`** — Added `retrieval_keywords` field to document parsing:
```python
"retrieval_keywords": metadata.get("retrieval_keywords") or [],
```

**`scripts/chunker.py`** — Added `retrieval_keywords` to chunk inheritance:
```python
"retrieval_keywords": doc.get("retrieval_keywords", []),
```

**`scripts/ingest.py`** — Added 3 new metadata fields to ChromaDB storage:
```python
"source_urls": ",".join(chunk.get("source_urls", [])),
"retrieval_keywords": ",".join(chunk.get("retrieval_keywords", []) or []),
"use_cases": ",".join(chunk.get("use_cases", []) or []),
```

### Metadata Spot-Check

```
doc_id: 01_regulatory_asean_rules_of_origin
  source_urls: 'https://asean.org/...,https://asean.org/...'
  retrieval_keywords: 'rules of origin,ROO,RVC,regional value content,...'
  use_cases: 'UC-2.2,UC-2.3'

doc_id: 01_regulatory_sg_export_procedures
  source_urls: 'https://www.customs.gov.sg/businesses/exporting-goods/overview/'
  retrieval_keywords: 'Singapore export,export permit,...'
  use_cases: 'UC-1.1,UC-2.1'
```

---

## Ingestion Results

| Metric | Value |
|--------|-------|
| Documents ingested | 30 |
| Chunks generated | 709 |
| Documents failed | 0 |
| Ingestion time | 10.05s |
| New metadata fields | source_urls, retrieval_keywords, use_cases |

---

## Test Results

| Test Suite | Result | Details |
|------------|--------|---------|
| Python pytest | **29/29 passed** | All ingestion pipeline tests |
| Jest backend | **105/105 passed** | api, pipeline, retrieval, llm, citations, placeholder |
| Retrieval quality | **94% hit rate** (47/50) | Exceeds 92% Week 3 target |

### Retrieval Quality by Category
- booking_documentation: 100%
- customs_regulatory: 100%
- carrier_info: 100%
- incoterms_trade: 100%
- edge_cases_out_of_scope: 90%

### 3 Failed Queries (out of scope)
- Q36: "What's the current freight rate to Jakarta?" — expected OOS, retrieval returned Indonesia import doc
- Q38: (similar OOS query)
- Q41: (similar OOS query)

---

## Issues Encountered

1. **Jest ESM config** — Running `npx jest` directly fails with ESM import errors. Must use `npm test` which includes `--experimental-vm-modules` flag. Not a bug — just need to use the correct command.

2. **YAML None handling** — Empty `retrieval_keywords:` in frontmatter parses as Python None, not empty list. Fixed with `or []` guard in process_docs.py.

---

## Next Steps

**→ CHECKPOINT 1 REACHED**

All existing tests pass on fresh ingestion with new metadata fields:
- pytest: 29/29
- Jest: 105/105
- Retrieval: 94% (exceeds 92% target)
- Metadata: source_urls, retrieval_keywords, use_cases verified in ChromaDB

Ready for Phase 1: UX Redesign (Task 1.1 — Update system prompt)

To proceed: "Generate prompt for Task 1.1"

---

## Tracking Updates

- [x] Checklist: Tasks 0.1–0.6 marked complete
- [x] Roadmap: Phase 0 status updated
