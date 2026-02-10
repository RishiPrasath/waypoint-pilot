# Task 2.7 Output — Add New Endpoint Tests

**Task:** 2.7 — Add new endpoint tests
**Phase:** Phase 2 — Systematic Testing
**Status:** PASS
**Date:** 2026-02-09

---

## Summary

Added **7 new response shape validation tests** to `tests/api.test.js` in a new `describe('Response shape validation')` block. These tests use a rich mock with populated `sources`, `relatedDocs`, and `citations` arrays to verify the full `/api/query` response structure end-to-end through the Express endpoint.

**Full suite: 154/154 tests pass across 7 suites (was 147).**

---

## Tests Added

| # | Test Name | What It Validates |
|---|-----------|-------------------|
| 1 | response contains all 6 top-level keys | `answer`, `sources`, `relatedDocs`, `citations`, `confidence`, `metadata` all present |
| 2 | sources items have correct shape | Each source has `title` (string), `org` (string), `url` (valid HTTP URL), `section` (string\|null) |
| 3 | relatedDocs items have correct shape | Each doc has `title` (string), `category` (string), `docId` (string), `url` (string\|null) |
| 4 | confidence.level is a valid enum value | Level is one of 'High', 'Medium', 'Low' |
| 5 | confidence.reason is a non-empty string | Reason exists and has content |
| 6 | metadata contains all required fields with correct types | `query` (string), `chunksRetrieved` (number), `chunksUsed` (number), `latencyMs` (number), `model` (string) |
| 7 | citations only contains matched items | All citations have `matched: true`, `title` (string), `raw` (string), `position` (number) |

---

## Rich Mock Data

The tests use a realistic mock with populated arrays (vs the existing empty-array mock):

```javascript
{
  answer: 'For Singapore exports, you need a trade declaration [Export Guide > Documents].',
  sources: [
    { title: 'Export Guide', org: 'Singapore Customs', url: 'https://customs.gov.sg/export', section: 'Documents' },
    { title: 'Trade Procedures', org: 'Singapore Customs', url: 'https://customs.gov.sg/trade', section: null },
  ],
  relatedDocs: [
    { title: 'Export Guide', category: 'regulatory', docId: 'sg_export_guide', url: 'https://customs.gov.sg/export' },
    { title: 'Booking SOP', category: 'internal', docId: 'booking_sop', url: null },
  ],
  citations: [{ raw: '[Export Guide > Documents]', title: 'Export Guide', section: 'Documents', ... }],
  confidence: { level: 'High', reason: '3 relevant sources with 2 citations' },
  metadata: { query: 'What documents for export?', chunksRetrieved: 3, chunksUsed: 2, latencyMs: 250, model: 'llama-3.1-8b-instant' },
}
```

---

## Test Results

| Metric | Value |
|--------|-------|
| New Tests Added | 7 |
| Existing Tests (unchanged) | 147/147 |
| **Combined api.test.js** | **18/18** (11 + 7 new) |
| **Combined Jest Total** | **154/154** |

---

## Validation

| Criterion | Status |
|-----------|--------|
| Response shape validation tests pass | PASS |
| Source URL format tests pass | PASS |
| Related doc category validation tests pass | PASS |
| Confidence level enum tests pass | PASS |
| All existing tests still pass | PASS (147/147) |

---

## Next Steps

- Task 2.8: Add error/edge case tests
- Task 2.9: Component unit tests
