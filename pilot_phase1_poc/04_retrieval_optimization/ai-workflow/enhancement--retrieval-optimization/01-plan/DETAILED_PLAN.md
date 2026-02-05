# Retrieval Optimization - Detailed Plan

**Project**: Waypoint Phase 1 POC — Week 3
**Initiative**: Retrieval Optimization
**Time Box**: Thursday 5 Feb (evening) → Sunday 9 Feb (end of day)
**Executor**: Rishi (directing) + Claude Code (executing)

---

## Executive Summary

Week 3 focuses on improving retrieval quality from the 76% baseline (82% adjusted) to ≥80% minimum, with a 90% stretch goal. This involves auditing failing queries, rebuilding the knowledge base with retrieval-first guidelines, and optimizing chunking/retrieval parameters.

---

## Baseline & Targets

| Metric | Week 2 (Raw) | Week 2 (Adjusted) | Minimum Target | Stretch Target |
|--------|--------------|-------------------|----------------|----------------|
| Hit Rate | 76% (38/50) | 82% (41/50) | 80% (40/50) | 90% (45/50) |

**Reclassified Queries** (now out-of-scope):
- #36: "refused deliveries"
- #38: "upgrade to express service"
- #44: "file a claim for damaged cargo"

**Remaining Failures to Fix (9)**:
| Query # | Topic | Category | Current Score |
|---------|-------|----------|---------------|
| 2 | LCL booking advance time | Booking | 0.057 |
| 5 | Commercial invoice for zero-value samples | Booking | -0.253 |
| 6 | Bill of Lading explanation | Booking | -0.070 |
| 7 | Shipping without packing list | Booking | -0.024 |
| 15 | ATIGA preferential duty rate | Customs | 0.029 |
| 19 | Customs ruling on HS code | Customs | 0.340 |
| 31 | Standard delivery SLA for Singapore | SLA | 0.185 |
| 32 | Customs clearance in door-to-door | SLA | -0.038 |
| 37 | Import permit applications | SLA | 0.203 |

---

## Confirmed Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Queries #36, #38, #44 reclassified as out-of-scope | Per 01_scope_definition.md |
| 2 | 80% target measured on adjusted query set | Reclassified queries pass if appropriately declined |
| 3 | Full KB rebuild from scratch | PDF discovery justifies full pass |
| 4 | Build pdf_extractor.py with pymupdf4llm | Repeatable PDF-to-markdown tooling |
| 5 | Claude Code scrapes autonomously | Rishi spot-checks 3-5 docs at review |
| 6 | Keep current chunking config initially | Test against baseline first |
| 7 | Start with top_k=5 for retrieval | Clean comparison with Week 2 |
| 8 | Fork ingestion pipeline, don't modify original | Keep 02_ingestion_pipeline stable |
| 9 | Parameterize chunking in forked pipeline | Enable experiments via .env |
| 10 | Task 8 iterates until 90% or time exhausted | Sunday evening is buffer |

---

## Phases Overview

### Phase 1: Audit (Tasks 1-3)
**Goal**: Understand why queries fail, reclassify scope, define document list
**Time**: Thursday evening - Friday morning
**Deliverables**:
- `reports/01_audit_report.md` - Root cause analysis
- `reports/02_scope_reclassification.md` - All 50 queries mapped
- `REVISED_DOCUMENT_LIST.md` - Documents for KB rebuild

### Phase 2: Infrastructure (Tasks 4-5)
**Goal**: Set up forked pipeline and PDF extraction tooling
**Time**: Friday
**Deliverables**:
- Forked ingestion pipeline in `04_retrieval_optimization/`
- `scripts/pdf_extractor.py` with tests

### Phase 3: KB Rebuild (Tasks 6-7)
**Goal**: Scrape and rebuild all documents, validate retrieval
**Time**: Friday evening - Saturday
**Deliverables**:
- Rebuilt `kb/` with retrieval-first content
- Initial retrieval validation results

### Phase 4: Refinement (Tasks 8-10)
**Goal**: Fix remaining failures, experiment with params, final validation
**Time**: Sunday
**Deliverables**:
- Content and parameter fixes
- Final comparison report
- RAG pipeline updated with new KB

---

## Review Gates

| Gate | After | Reviewer | Decisions |
|------|-------|----------|-----------|
| **Review 1** | Tasks 1-3 | Rishi | Approve fixes, accept reclassifications, confirm doc list |
| **Review 2** | Task 7 | Rishi | Accept results ≥80%, decide on parameter experiments |
| **Review 3** | Task 10 | Rishi | Final approval, Week 3 complete |

---

## Key Technical Details

### Retrieval-First Content Guidelines
1. Key Facts summary in first 600 characters
2. Customer-language section headers
3. Self-contained paragraphs for critical facts
4. Synonym/alias mentions in first occurrence
5. Cross-references to related documents

### Updated Frontmatter Template
```yaml
---
title: [Document Title]
source_organization: [Org Name]
source_urls:
  - url: https://...
    description: [what this page covers]
    retrieved_date: YYYY-MM-DD
source_pdfs:
  - filename: [local filename in pdfs/]
    source_url: https://...
    description: [what this PDF covers]
    retrieved_date: YYYY-MM-DD
source_type: [public_regulatory | public_carrier | synthetic_internal]
last_updated: YYYY-MM-DD
jurisdiction: [SG | MY | ID | TH | VN | PH | ASEAN | Global]
category: [customs | carrier | policy | procedure | reference]
use_cases: [UC-1.1, UC-2.3]
keywords: [keyword1, keyword2, keyword3]
answers_queries:
  - "Query text this document should answer"
related_documents: [other_doc_id_1, other_doc_id_2]
---
```

### Chunking Parameters (Configurable via .env)
- `CHUNK_SIZE`: Default 600 (experiment: 800, 1000)
- `CHUNK_OVERLAP`: Default 90 (experiment: 120, 150)
- `top_k`: Default 5 (experiment: 10)

---

## Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Adjusted hit rate | ≥80% | retrieval_quality_test.py |
| No regressions | 0 new failures | Comparison with Week 2 |
| E2E tests pass | 30/30 | e2e_test.py |
| All docs follow guidelines | 100% | Auto-review during Task 6 |
| Documentation complete | All reports | Check 04_final_comparison.md |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| PDFs are image-only | Flag as LOW quality, manual review |
| Scraping blocked | Use cached content, document gap |
| 80% not achievable | Investigate additional reclassifications |
| Time overrun | Sunday buffer for Task 8 iterations |

---

## Related Documents

- Source Plan: `./04_retrieval_optimization/Retrieval_Optimization_Plan.md`
- Scope Definition: `./00_docs/01_scope_definition.md`
- Use Cases: `./00_docs/02_use_cases.md`
- KB Blueprint: `./00_docs/03_knowledge_base_blueprint.md`
- Week 2 Baseline: `./03_rag_pipeline/reports/retrieval_quality_REPORT.md`
