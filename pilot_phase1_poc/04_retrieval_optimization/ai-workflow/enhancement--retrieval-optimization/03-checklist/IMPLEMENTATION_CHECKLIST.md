# Retrieval Optimization - Implementation Checklist

**Initiative**: Retrieval Optimization (Week 3)
**Status**: 🔄 In Progress
**Last Updated**: 2026-02-05

---

## Overview

| Phase | Status | Tasks |
|-------|--------|-------|
| Phase 1: Audit | ⬜ Pending | 1, 2, 3 |
| Phase 2: Infrastructure | ⬜ Pending | 4, 5 |
| Phase 3: KB Rebuild | ⬜ Pending | 6, 7 |
| Phase 4: Refinement | ⬜ Pending | 8, 9, 10 |

---

## Phase 1: Audit

### Task 1: Root Cause Analysis
**Status**: ⬜ Pending

- [ ] Parse retrieval quality report
- [ ] Analyze Query #2 (LCL booking)
- [ ] Analyze Query #5 (Commercial invoice samples)
- [ ] Analyze Query #6 (Bill of Lading)
- [ ] Analyze Query #7 (Packing list)
- [ ] Analyze Query #15 (ATIGA duty rate)
- [ ] Analyze Query #19 (HS code ruling)
- [ ] Analyze Query #31 (SLA Singapore)
- [ ] Analyze Query #32 (Customs in door-to-door)
- [ ] Analyze Query #37 (Import permit)
- [ ] Classify all root causes (a/b/c)
- [ ] Propose fixes for all 9
- [ ] Save `reports/01_audit_report.md`

### Task 2: Scope Reclassification
**Status**: ⬜ Pending

- [ ] Read `01_scope_definition.md`
- [ ] Read `02_use_cases.md`
- [ ] Map all 50 queries to use cases
- [ ] Apply reclassification: Query #36
- [ ] Apply reclassification: Query #38
- [ ] Apply reclassification: Query #44
- [ ] Flag additional mismatches
- [ ] Save `reports/02_scope_reclassification.md`

### ⏸ Review Point 1
- [ ] Rishi reviewed audit report
- [ ] Rishi reviewed reclassification report
- [ ] Fixes approved
- [ ] Reclassifications approved
- [ ] Direction confirmed for Task 3

### Task 3: Revised Document List
**Status**: ⬜ Pending

- [ ] Start from existing 29-doc list
- [ ] Apply Task 1 fixes
- [ ] Apply Task 2 reclassifications
- [ ] Identify new synthetic documents
- [ ] Ensure P1/P2 coverage
- [ ] Specify actions per document
- [ ] Document retrieval-first guidelines
- [ ] Document frontmatter template
- [ ] Save `REVISED_DOCUMENT_LIST.md`

---

## Phase 2: Infrastructure

### Task 4: Folder Setup
**Status**: ⬜ Pending

- [ ] Create directory structure
- [ ] Copy `scripts/` from Week 1
- [ ] Copy `retrieval_quality_test.py` from Week 2
- [ ] Update `config.py` paths
- [ ] Parameterize CHUNK_SIZE in .env
- [ ] Parameterize CHUNK_OVERLAP in .env
- [ ] Create `kb/` folders
- [ ] Create `pdfs/` subfolders
- [ ] Set up venv
- [ ] Test pipeline on empty KB

### Task 5: PDF Extractor
**Status**: ⬜ Pending

- [ ] Add pymupdf4llm to requirements.txt
- [ ] Create `pdf_extractor.py`
- [ ] Implement single file mode
- [ ] Implement batch mode
- [ ] Add frontmatter template
- [ ] Clean extraction artifacts
- [ ] Generate quality flags
- [ ] Output summary CSV
- [ ] Write tests
- [ ] All tests pass

---

## Phase 3: KB Rebuild

### Task 6: Scraping
**Status**: ⬜ Pending

**6a: Singapore Customs**
- [ ] Documents created
- [ ] PDFs downloaded
- [ ] Auto-review passed

**6b: ASEAN Trade**
- [ ] Documents created
- [ ] PDFs downloaded
- [ ] Auto-review passed

**6c: Country-specific**
- [ ] Documents created
- [ ] PDFs downloaded
- [ ] Auto-review passed

**6d: Ocean Carriers**
- [ ] Documents created
- [ ] PDFs downloaded
- [ ] Auto-review passed

**6e: Air Carriers**
- [ ] Documents created
- [ ] PDFs downloaded
- [ ] Auto-review passed

**6f: Reference**
- [ ] Documents restructured
- [ ] Auto-review passed

**6g: Synthetic Internal**
- [ ] Documents restructured
- [ ] 1-2 new documents created
- [ ] Auto-review passed

**Overall**
- [ ] All documents follow retrieval-first guidelines
- [ ] All frontmatter complete
- [ ] Issues logged

### Task 7: Initial Validation
**Status**: ⬜ Pending

- [ ] Run ingest.py
- [ ] Verify doc count
- [ ] Verify chunk count
- [ ] Run retrieval_quality_test.py
- [ ] Compare to 76% raw baseline
- [ ] Compare to 82% adjusted baseline
- [ ] Identify fixed queries
- [ ] Identify new failures
- [ ] Save `reports/03_retrieval_validation.md`
- [ ] Hit rate ≥80% adjusted

### ⏸ Review Point 2
- [ ] Rishi reviewed validation results
- [ ] Rishi spot-checked KB (3-5 docs)
- [ ] Proceed to Phase 4 approved
- [ ] Parameter experiments approved

---

## Phase 4: Refinement

### Task 8: Fixes + Experiments
**Status**: ⬜ Pending

**Content Fixes**
- [ ] Missing content added
- [ ] Section structure adjusted
- [ ] Synonyms added

**Parameter Experiments**
- [ ] Baseline measured
- [ ] Experiment A completed
- [ ] Experiment B completed
- [ ] Experiment C completed
- [ ] Best config identified

**Final Result**
- [ ] Target ≥90% OR time exhausted
- [ ] Validation report updated

### Task 9: RAG Pipeline Update
**Status**: ⬜ Pending

- [ ] Server stopped
- [ ] ChromaDB backed up
- [ ] New ChromaDB copied
- [ ] Config updated (if params changed)
- [ ] Server started
- [ ] Manual smoke test passed
- [ ] E2E tests passed

### Task 10: Final Report
**Status**: ⬜ Pending

- [ ] Final retrieval test run
- [ ] Final E2E test run
- [ ] Executive Summary written
- [ ] Retrieval Comparison documented
- [ ] KB Changes documented
- [ ] Query-Level Detail documented
- [ ] Parameter Experiments documented
- [ ] E2E Results documented
- [ ] Time Spent documented
- [ ] Decisions Made documented
- [ ] Lessons Learned documented
- [ ] Week 4 Recommendations written
- [ ] Save `reports/04_final_comparison.md`

### ⏸ Review Point 3
- [ ] Rishi reviewed final report
- [ ] Rishi approved results
- [ ] Week 3 complete

---

## Summary

**Total Tasks**: 10
**Completed**: 0
**Progress**: 0%

**Targets**:
- Minimum: 80% adjusted hit rate
- Stretch: 90% adjusted hit rate
- Current: Not yet measured
