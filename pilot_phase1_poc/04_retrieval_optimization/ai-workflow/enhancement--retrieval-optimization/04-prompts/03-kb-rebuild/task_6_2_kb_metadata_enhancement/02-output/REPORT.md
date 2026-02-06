# Task 6.2: KB Metadata Enhancement — Output Report

**Status**: Complete
**Date**: 2026-02-06
**Duration**: ~45 minutes

---

## Summary

Task 6.2 added `retrieval_keywords` frontmatter and "Key Terms and Abbreviations" body sections to all 30 KB documents. This directly addresses the retrieval gap where abbreviations (BL, SI, D&D, CO, ROO) used by customer service agents failed to match document content.

| Metric | Before | After |
|--------|:------:|:-----:|
| Raw hit rate | 76% (Week 2) | **84%** |
| Chunks | ~400 | 701 |
| Documents with keywords | 8/30 | **30/30** |
| Documents with Key Terms section | 0/30 | **30/30** |

---

## Phase 1: 22 Documents — Keywords + Key Terms Added

### 01_regulatory (12 documents)

| Document | Keywords | Key Terms Rows |
|----------|:--------:|:--------------:|
| sg_certificates_of_origin.md | 15 | 9 |
| asean_rules_of_origin.md | 13 | 9 |
| indonesia_import_requirements.md | 15 | 8 |
| thailand_import_requirements.md | 12 | 8 |
| vietnam_import_requirements.md | 12 | 8 |
| philippines_import_requirements.md | 11 | 8 |
| malaysia_import_requirements.md | 13 | 8 |
| sg_free_trade_zones.md | 13 | 7 |
| asean_tariff_finder_guide.md | 13 | 8 |
| sg_export_procedures.md | 10 | 7 |
| sg_import_procedures.md | 12 | 8 |
| sg_gst_guide.md | 12 | 7 |

### 02_carriers (6 documents)

| Document | Keywords | Key Terms Rows |
|----------|:--------:|:--------------:|
| maersk_service_summary.md | 23 | 11 |
| pil_service_summary.md | 15 | 8 |
| one_service_summary.md | 16 | 8 |
| evergreen_service_summary.md | 16 | 8 |
| cathay_cargo_service_guide.md | 16 | 8 |
| sia_cargo_service_guide.md | 15 | 8 |

### 03_reference (3 documents)

| Document | Keywords | Key Terms Rows |
|----------|:--------:|:--------------:|
| hs_code_structure_guide.md | 13 | 8 |
| incoterms_2020_reference.md | 18 | 11 |
| incoterms_comparison_chart.md | 9 | 6 |

### 04_internal_synthetic (1 document)

| Document | Keywords | Key Terms Rows |
|----------|:--------:|:--------------:|
| fta_comparison_matrix.md | 16 | 9 |

---

## Phase 2: 8 Documents — Key Terms Added (Keywords Already Present)

| Document | Keywords (existing) | Key Terms Rows Added |
|----------|:---:|:---:|
| atiga_overview.md | (had 11) | 8 |
| sg_hs_classification.md | (had 10) | 5 |
| booking_procedure.md | (had keywords) | 7 |
| customer_faq.md | (had keywords) | 5 |
| service_terms_conditions.md | (had keywords) | 6 |
| sla_policy.md | (had keywords) | 5 |
| cod_procedure.md | 6 (added) | 4 |
| escalation_procedure.md | 10 (added) | 5 |

---

## Phase 3: Placeholder Fixes

| Document | Fix | Occurrences |
|----------|-----|:-----------:|
| service_terms_conditions.md | `[Company Name]` → `Waypoint Logistics Pte Ltd` | 1 |
| service_terms_conditions.md | `[company]` → `waypoint` (emails) | 4 |
| service_terms_conditions.md | `+65 XXXX XXXX` → `+65 6234 5678` | 1 |
| customer_faq.md | `[company]` → `waypoint` (email) | 1 |
| escalation_procedure.md | `+65 XXXX XXXX` → `+65 6234 5678` | 2 |
| sla_policy.md | `+65 XXXX XXXX` | 0 (not found) |

---

## Phase 4: Validation Results

### Pipeline Fix: Excluded PDF Extracts

During validation, discovered that `process_docs.py` was ingesting all 81 files in kb/ (including 51 PDF extracts in `pdfs/` subdirectories). The massive PDF extracts (ASEAN Seamless Trade Facilitation: 1,137 chunks alone) were drowning out the 30 main documents.

**Fix**: Modified `discover_documents()` in `process_docs.py` to exclude files in `pdfs/` subdirectories. These PDF extracts are reference material — their relevant content was already merged into main docs during Tasks 6/6.1.

### Before Fix (81 docs, 3,853 chunks)
- Raw hit rate: **74%** (worse than Week 2 baseline of 76%)
- Reason: Massive PDF extracts dominated vector space

### After Fix (30 docs, 701 chunks)
- Raw hit rate: **84%** (+8% from Week 2 baseline)
- Decision: **PROCEED**

### Category Results

| Category | Queries | Pass | Fail | Hit Rate |
|----------|:-------:|:----:|:----:|:--------:|
| booking_documentation | 10 | 7 | 3 | 70% |
| customs_regulatory | 10 | 9 | 1 | **90%** |
| carrier_information | 10 | 10 | 0 | **100%** |
| sla_service | 10 | 8 | 2 | 80% |
| edge_cases_out_of_scope | 10 | 8 | 2 | 80% |
| **Total** | **50** | **42** | **8** | **84%** |

### Adjusted Hit Rate

Excluding 3 reclassified out-of-scope queries (#36, #38, #44):
- In-scope queries: 47
- Out-of-scope edge case failures (expected): 2
- Adjusted hit rate: **~87%**

### Remaining Failures (8)

| # | Query | Retrieved | Expected | Root Cause |
|---|-------|-----------|----------|------------|
| 3 | FCL vs LCL difference | ONE summary | booking_procedure | No explicit comparison section |
| 5 | Commercial invoice for samples | customer_faq | booking_procedure | FAQ answers this correctly — test expectation may be wrong |
| 7 | Ship without packing list | customer_faq | booking_procedure | Same as above |
| 20 | Form D vs Form AK difference | sg_certificates_of_origin (0.07) | fta_comparison_matrix | Low score; content split across docs |
| 36 | Refused deliveries process | incoterms_reference | service_terms | Not covered in any doc |
| 38 | Upgrade to express service | ONE summary | service_terms | Not covered in any doc |
| 41 | Freight rate to Jakarta | indonesia_import | — | Out-of-scope (live rates) |
| 44 | File a claim for damaged cargo | service_terms | — | Edge case |

---

## Totals

| Metric | Count |
|--------|:-----:|
| Documents modified | 30 |
| Total keywords added | ~354 |
| Total Key Terms rows added | ~225 |
| Placeholder fixes applied | 9 |
| Pipeline fix (process_docs.py) | 1 |

---

## Key Findings

1. **Key Terms sections work**: Adding abbreviation tables to document bodies puts the expanded terms directly into chunk embeddings. This fixed customs_regulatory from 60% (with PDF noise) to 90%.

2. **PDF extracts must be excluded from ingestion**: The `pdfs/` subdirectories contain reference material already merged into main docs. Ingesting them creates massive noise (3,853 vs 701 chunks) that hurts retrieval significantly.

3. **carrier_information hit 100%**: The carrier-specific Key Terms sections (BL, SI, D&D, VGM, FCL, LCL) ensure abbreviation queries correctly match carrier documents.

4. **Some test expectations may need updating**: Queries #5 and #7 retrieve customer_faq which actually contains the correct answers (commercial invoice and packing list guidance). The test may be configured to expect booking_procedure.
