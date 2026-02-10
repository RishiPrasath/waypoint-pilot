# Checkpoint 1: Workspace Setup + Fresh Ingestion

**After Task:** 0.6
**Feature:** Workspace ready with validated fresh ingestion
**Precondition for:** Phase 1 (UX Redesign)

---

## Overview

Validates that the `05_evaluation/` workspace is fully functional with a fresh ChromaDB ingestion from copied KB documents. Proves the pipeline is reproducible and the knowledge base is self-contained.

---

## Requirements Reference

- Decision #31: Fresh ingestion — no ChromaDB data copied
- Decision #2: Codebase fork excludes all W3-specific artifacts
- Decision #16: Re-run existing + add new tests for metadata

---

## Tasks Included

| Task | Title | Status |
|------|-------|--------|
| 0.1 | Create 05_evaluation/ folder structure | ⬜ |
| 0.2 | Copy codebase from 04_retrieval_optimization/ | ⬜ |
| 0.3 | Setup environment (npm install, venv) | ⬜ |
| 0.4 | Fix ingestion pipeline metadata | ⬜ |
| 0.5 | Run fresh ingestion | ⬜ |
| 0.6 | Run ALL existing tests | ⬜ |

---

## Acceptance Criteria

### Folder Structure
1. `05_evaluation/` contains: backend/, client/, kb/, scripts/, tests/, data/, logs/, chroma_db/
2. No W3-specific artifacts present (ai-workflow/, reports/, Retrieval_Optimization_Plan.md)

### Fresh Ingestion
1. 30 documents ingested
2. ~709 chunks generated
3. `source_urls` metadata present in ChromaDB chunks (comma-separated string)
4. `retrieval_keywords` metadata present in ChromaDB chunks
5. `use_cases` metadata present in ChromaDB chunks
6. `category` metadata preserved per chunk

### All Tests Pass
1. Python pytest — all ingestion unit tests pass
2. Jest — all backend tests pass
3. Retrieval quality — 92% hit rate maintained
4. End-to-end — backend starts, test query returns response with citations

---

## Validation Checklist

- [ ] `05_evaluation/` folder structure matches Decision #27
- [ ] Codebase copied (backend, client, kb, scripts, tests, configs)
- [ ] W3-specific artifacts excluded
- [ ] npm install succeeds
- [ ] Python venv created, requirements installed
- [ ] ingest.py updated with source_urls, retrieval_keywords, use_cases metadata
- [ ] Fresh ingestion: 30 docs, ~709 chunks
- [ ] Spot-check: source_urls present in ChromaDB chunks
- [ ] pytest passes (all ingestion tests)
- [ ] npm test passes (all backend tests)
- [ ] retrieval_quality_test.py: 92% hit rate
- [ ] Backend starts, test query succeeds

---

## Demo Script

    # Step 1: Verify folder structure
    ls pilot_phase1_poc/05_evaluation/

    # Step 2: Verify fresh ingestion
    cd pilot_phase1_poc/05_evaluation
    venv/Scripts/activate
    python scripts/ingest.py --clear

    # Step 3: Run tests
    python -m pytest tests/ -v
    npm test
    python scripts/retrieval_quality_test.py

    # Step 4: Smoke test
    npm start
    # In another terminal: curl POST /api/query with test query

---

## Success Criteria

Checkpoint complete when:
1. All 6 setup tasks marked complete
2. Fresh ingestion produces correct document/chunk counts
3. New metadata fields (source_urls, retrieval_keywords, use_cases) verified in ChromaDB
4. All existing tests pass (pytest + Jest + 92% retrieval)
5. Backend starts and returns response with citations

---

## Next Steps

After this checkpoint, proceed to:
- Phase 1: UX Redesign (Task 1.1 — Update system prompt)
