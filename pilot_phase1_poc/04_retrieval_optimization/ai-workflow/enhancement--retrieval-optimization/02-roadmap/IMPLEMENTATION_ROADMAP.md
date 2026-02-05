# Retrieval Optimization - Implementation Roadmap

**Initiative**: Retrieval Optimization (Week 3)
**Status**: 🔄 In Progress
**Last Updated**: 2026-02-05

---

## Progress Tracker

| Phase | Tasks | Completed | Status |
|-------|-------|-----------|--------|
| Phase 1: Audit | 3 | 1 | 🔄 In Progress |
| Phase 2: Infrastructure | 2 | 0 | ⬜ Pending |
| Phase 3: KB Rebuild | 2 | 0 | ⬜ Pending |
| Phase 4: Refinement | 3 | 0 | ⬜ Pending |
| **Total** | **10** | **1** | **10%** |

---

## Phase 1: Audit

### Task 1: Root Cause Analysis of Retrieval Failures
- **Status**: ✅ Complete
- **Dependencies**: None
- **Blocks**: Task 3
- **Completed**: 2026-02-05

**Objective**: Analyze 9 failing queries to classify root causes as (a) content missing, (b) content buried, or (c) terminology mismatch.

**Checklist**:
- [x] Parse retrieval quality report for 9 failing queries
- [x] For each query: search raw markdown files
- [x] For each query: search ChromaDB chunks
- [x] Classify root cause (a/b/c) for each
- [x] Propose specific fix for each
- [x] Save report to `reports/01_audit_report.md`

**Results**:
- (a) Content Missing: 5 queries (#2, #5, #19, #31, #32)
- (b) Content Buried: 3 queries (#6, #7, #37)
- (c) Terminology Mismatch: 1 query (#15)

**Output**: `04_retrieval_optimization/reports/01_audit_report.md`

---

### Task 2: Scope Reclassification of All 50 Test Queries
- **Status**: ⬜ Pending
- **Dependencies**: None (can run parallel with Task 1)
- **Blocks**: Task 3
- **Estimated Time**: 45 min - 1 hour

**Objective**: Map all 50 queries to use cases and priority levels, apply pre-confirmed reclassifications.

**Pre-confirmed reclassifications**:
- Query #36 → out-of-scope
- Query #38 → out-of-scope
- Query #44 → out-of-scope

**Checklist**:
- [ ] Map each query to a use case (UC-X.X)
- [ ] Assign priority level (P1/P2/P3/Out-of-scope)
- [ ] Apply 3 pre-confirmed reclassifications
- [ ] Flag additional mismatches for review
- [ ] Save report to `reports/02_scope_reclassification.md`

**Output**: `04_retrieval_optimization/reports/02_scope_reclassification.md`

---

### ⏸ REVIEW POINT 1
**Reviewer**: Rishi
**Items to Review**:
- Task 1 audit report
- Task 2 reclassification report
**Decisions Needed**:
- Approve/adjust proposed fixes
- Accept/reject additional reclassifications
- Confirm direction for Task 3

---

### Task 3: Define the Revised Document List
- **Status**: ⬜ Pending
- **Dependencies**: Task 1, Task 2, Review Point 1
- **Blocks**: Task 6
- **Estimated Time**: 1-1.5 hours

**Objective**: Produce definitive document list for KB rebuild with actions per document.

**Checklist**:
- [ ] Start from existing 29-document list
- [ ] Apply Task 1 fixes (new docs, restructure, enrich)
- [ ] Apply Task 2 reclassifications
- [ ] Identify 1-2 new synthetic documents for gaps
- [ ] Ensure every P1/P2 use case has a document
- [ ] Specify action per doc (RE-SCRAPE/RESTRUCTURE/CREATE/CARRY FORWARD)
- [ ] Include retrieval-first guidelines
- [ ] Include updated frontmatter template
- [ ] Save to `REVISED_DOCUMENT_LIST.md`

**Output**: `04_retrieval_optimization/REVISED_DOCUMENT_LIST.md`

---

## Phase 2: Infrastructure

### Task 4: Set Up 04_retrieval_optimization Folder
- **Status**: ⬜ Pending
- **Dependencies**: None
- **Blocks**: Task 5, Task 6
- **Estimated Time**: 30-45 min

**Objective**: Create folder structure and fork ingestion pipeline with parameterized chunking.

**Checklist**:
- [ ] Create directory structure per plan
- [ ] Copy scripts from `02_ingestion_pipeline/`
- [ ] Copy `retrieval_quality_test.py` from `03_rag_pipeline/scripts/`
- [ ] Update `config.py` paths to point to new locations
- [ ] Parameterize CHUNK_SIZE and CHUNK_OVERLAP via .env
- [ ] Create empty `kb/` category folders with `pdfs/` subfolders
- [ ] Set up Python virtual environment
- [ ] Verify pipeline runs on empty KB

**Output**: Working forked pipeline in `04_retrieval_optimization/`

---

### Task 5: Build PDF Extraction Script
- **Status**: ⬜ Pending
- **Dependencies**: Task 4
- **Blocks**: Task 6
- **Estimated Time**: 1-1.5 hours

**Objective**: Create `pdf_extractor.py` for PDF-to-markdown conversion.

**Checklist**:
- [ ] Add `pymupdf4llm` to `requirements.txt`
- [ ] Create `scripts/pdf_extractor.py`
- [ ] Implement single file mode
- [ ] Implement batch mode
- [ ] Add frontmatter template to output
- [ ] Clean extraction artifacts
- [ ] Generate quality flags (HIGH/MEDIUM/LOW)
- [ ] Output batch summary CSV
- [ ] Write tests in `tests/test_pdf_extractor.py`
- [ ] All tests pass

**Output**: `scripts/pdf_extractor.py` + tests

---

## Phase 3: Knowledge Base Rebuild

### Task 6: Execute Scraping with Improved Strategy
- **Status**: ⬜ Pending
- **Dependencies**: Task 3, Task 4, Task 5
- **Blocks**: Task 7
- **Estimated Time**: 4-6 hours

**Objective**: Rebuild KB from scratch using revised document list and retrieval-first guidelines.

**Sub-tasks**:
- [ ] 6a: Singapore Customs documents
- [ ] 6b: ASEAN Trade documents
- [ ] 6c: Country-specific documents
- [ ] 6d: Ocean carrier documents
- [ ] 6e: Air carrier documents
- [ ] 6f: Reference documents (restructure)
- [ ] 6g: Synthetic internal documents (restructure + create 1-2 new)

**Checklist per document**:
- [ ] Navigate to source URL
- [ ] Scrape page content
- [ ] Scan for downloadable PDFs
- [ ] Download relevant PDFs
- [ ] Run pdf_extractor.py on PDFs
- [ ] Create markdown with retrieval-first guidelines
- [ ] Complete frontmatter (no placeholders)
- [ ] Auto-review for quality
- [ ] Log issues to `reports/scraping_issues_log.md`

**Output**: Rebuilt `kb/` folder

---

### Task 7: Initial Ingestion and Retrieval Validation
- **Status**: ⬜ Pending
- **Dependencies**: Task 6
- **Blocks**: Task 8
- **Estimated Time**: 1 hour

**Objective**: Ingest new KB and validate retrieval improvement.

**Parameters** (same as Week 2 for clean comparison):
- CHUNK_SIZE=600, CHUNK_OVERLAP=90
- top_k=5, threshold=0.15

**Checklist**:
- [ ] Run `ingest.py` on new KB
- [ ] Verify ingestion (doc count, chunk count)
- [ ] Run `retrieval_quality_test.py` with all 50 queries
- [ ] Compare to Week 2 baseline (76% raw, 82% adjusted)
- [ ] Identify new failures and fixed queries
- [ ] Save report to `reports/03_retrieval_validation.md`

**Target**: ≥80% adjusted hit rate (must not regress)

**Output**: `04_retrieval_optimization/reports/03_retrieval_validation.md`

---

### ⏸ REVIEW POINT 2
**Reviewer**: Rishi
**Items to Review**:
- Task 7 validation results
- KB quality spot-check (3-5 documents)
**Decisions Needed**:
- Proceed to Phase 4 if ≥80%
- Loop back for fixes if <80%
- Approve parameter experiments

---

## Phase 4: Ingestion Refinement & Final Validation

### Task 8: Fix Remaining Failures + Parameter Experiments
- **Status**: ⬜ Pending
- **Dependencies**: Task 7, Review Point 2
- **Blocks**: Task 9
- **Estimated Time**: 2-4 hours

**Objective**: Address remaining failures through content fixes and parameter experiments.

**Track A: Content Fixes**
- [ ] Add missing content where needed
- [ ] Adjust section structure for bad chunks
- [ ] Add synonyms for terminology mismatches

**Track B: Parameter Experiments**
- [ ] Baseline: CHUNK_SIZE=600, CHUNK_OVERLAP=90, top_k=5
- [ ] Experiment A: CHUNK_SIZE=800, CHUNK_OVERLAP=120, top_k=5
- [ ] Experiment B: CHUNK_SIZE=1000, CHUNK_OVERLAP=150, top_k=5
- [ ] Experiment C: Best chunk config + top_k=10

**Stop Condition**: 90% adjusted OR Sunday evening buffer exhausted

**Output**: Updated `reports/03_retrieval_validation.md` with all rounds

---

### Task 9: Update RAG Pipeline to Use New KB
- **Status**: ⬜ Pending
- **Dependencies**: Task 8
- **Blocks**: Task 10
- **Estimated Time**: 30-45 min

**Objective**: Point RAG pipeline at new ChromaDB for E2E use.

**Checklist**:
- [ ] Stop running server
- [ ] Backup existing ChromaDB
- [ ] Copy final `chroma_db/` to RAG pipeline location
- [ ] Update config if params changed
- [ ] Start server
- [ ] Manual smoke test
- [ ] Run E2E test suite

**Output**: RAG pipeline serving from new KB

---

### Task 10: Final Comparison Report (Week 3 Retrospective)
- **Status**: ⬜ Pending
- **Dependencies**: Task 9
- **Blocks**: None
- **Estimated Time**: 1-1.5 hours

**Objective**: Comprehensive Week 3 retrospective with before/after comparison.

**Report Sections**:
- [ ] Executive Summary
- [ ] Retrieval Quality Comparison
- [ ] Knowledge Base Changes
- [ ] Query-Level Detail
- [ ] Parameter Experiments
- [ ] E2E Test Results
- [ ] Time Spent
- [ ] Decisions Made
- [ ] Lessons Learned
- [ ] Recommendations for Week 4

**Output**: `04_retrieval_optimization/reports/04_final_comparison.md`

---

### ⏸ REVIEW POINT 3
**Reviewer**: Rishi
**Items to Review**:
- Final comparison report
- E2E test results
**Outcome**: Week 3 complete

---

## Validation Commands

```bash
cd pilot_phase1_poc/04_retrieval_optimization

# Activate venv
venv\Scripts\activate

# Run ingestion
python scripts/ingest.py --clear

# Verify ingestion
python scripts/verify_ingestion.py

# Run retrieval quality test
python scripts/retrieval_quality_test.py

# Run PDF extraction (single)
python scripts/pdf_extractor.py path/to/file.pdf

# Run PDF extraction (batch)
python scripts/pdf_extractor.py --batch path/to/pdfs/

# Run tests
python -m pytest tests/ -v
```
