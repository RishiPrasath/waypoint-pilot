# Task 2.2 Output — Add New Metadata Preservation Tests

**Task:** 2.2 — Add new metadata preservation tests
**Phase:** Phase 2 — Systematic Testing
**Status:** COMPLETE
**Date:** 2026-02-09

---

## Summary

Created `tests/test_metadata_preservation.py` with 26 integration tests validating that `source_urls`, `retrieval_keywords`, `use_cases`, and `category` are correctly preserved in ChromaDB chunk metadata. All 26 tests pass. Combined with existing tests: 55/55 pytest green.

---

## New File

### `tests/test_metadata_preservation.py` — 26 tests across 5 classes

| Class | Tests | What It Validates |
|-------|-------|-------------------|
| `TestFieldPresence` | 6 | All 3 new fields exist on every chunk and are strings |
| `TestFieldFormat` | 4 | Comma-separated formats, category values, UC-N.N pattern |
| `TestKnownValues` | 9 | Spot-checks on 4 specific documents across all categories |
| `TestEdgeCases` | 5 | N/A URLs for internal docs, multi-URL commas, same-doc consistency |
| `TestCategoryCoverage` | 2 | All 4 categories present with >=10 chunks each |

---

## Test Results

| Metric | Value |
|--------|-------|
| New Tests | 26 |
| Passed | 26 |
| Failed | 0 |
| Existing Tests (pdf_extractor) | 29/29 |
| **Combined pytest Total** | **55/55** |

---

## Issues Encountered During Development

1. **Incoterms doc_id mismatch** — The roadmap referenced `03_reference_incoterms_comparison` but the actual doc_id is `03_reference_incoterms_comparison_chart`. Fixed the test expectation.

2. **Internal docs: mixed N/A and empty string** — Not all `synthetic_internal` docs have `source_urls: "N/A"`. Three docs (`cod_procedure`, `escalation_procedure`, `fta_comparison_matrix`) have empty string `""` because their frontmatter lacks `source_urls` entirely. Updated the test to accept both `"N/A"` and `""` as valid for internal docs, while asserting no real URLs are present.

---

## Validation

| Criterion | Status |
|-----------|--------|
| `source_urls` preservation test passes | PASS |
| `category` preservation test passes | PASS |
| `retrieval_keywords` preservation test passes | PASS |
| `use_cases` preservation test passes | PASS |
| Comma-separated string format test passes | PASS |
| Missing field fallback test passes | PASS |
| All existing tests still pass | PASS (29/29) |

---

## Next Steps

- Task 2.3: Re-run 50-query retrieval hit rate test (formal)
