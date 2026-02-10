# Task 2.8 Output — Add Error/Edge Case Tests

**Task:** 2.8 — Add error/edge case tests
**Phase:** Phase 2 — Systematic Testing
**Status:** PASS
**Date:** 2026-02-09

---

## Summary

Added **8 new error/edge case tests** to `tests/api.test.js` in a new `describe('Error and edge cases')` block. Each test targets a gap not covered by existing tests (careful dedup analysis performed first). All tests pass on first run.

**Full suite: 162/162 tests pass across 7 suites (was 154).**

---

## Gap Analysis (What Was Already Covered)

Before this task, the following error scenarios were already tested:
- `api.test.js`: empty query, whitespace, non-string (number), 1001-char query, generic pipeline error
- `pipeline.test.js`: empty query throw, ChromaDB unavailable throw, Groq API error throw
- `generation.test.js`: 429/503 retries, 400 client error, retry exhaustion

**These were NOT duplicated.** The 8 new tests target distinct gaps.

---

## Tests Added

| # | Test Name | Gap Covered | Assertion |
|---|-----------|-------------|-----------|
| 1 | rejects very long query (10,000 chars) with 400 | Extreme length (only 1001 tested before) | 400 + "maximum length" |
| 2 | rejects malformed JSON body with 400 | Invalid JSON syntax | 400 from Express parser |
| 3 | rejects body sent as plain text | Wrong Content-Type | 400 (body not parsed → query missing) |
| 4 | returns 500 for Groq API timeout through endpoint | Timeout error via HTTP (not just service level) | 500 + "timed out" in message |
| 5 | returns 500 for ChromaDB connection failure through endpoint | Connection error via HTTP (not just service level) | 500 + "ChromaDB" in message |
| 6 | rejects array as query value with 400 | Non-string type: array (only number tested) | 400 |
| 7 | rejects object as query value with 400 | Non-string type: object (only number tested) | 400 |
| 8 | handles query with special characters safely | XSS/SQL injection payloads | 200 (processed normally) |

---

## Test Results

| Metric | Value |
|--------|-------|
| New Tests Added | 8 |
| Existing Tests (unchanged) | 154/154 |
| **Combined api.test.js** | **26/26** (18 + 8 new) |
| **Combined Jest Total** | **162/162** |

---

## Validation

| Criterion | Status |
|-----------|--------|
| Very long query test passes | PASS |
| Malformed JSON test passes | PASS |
| Wrong Content-Type test passes | PASS |
| Groq timeout via endpoint test passes | PASS |
| ChromaDB failure via endpoint test passes | PASS |
| Array/object query type tests pass | PASS |
| Special characters safety test passes | PASS |
| All existing tests still pass | PASS (154/154) |

---

## Next Steps

- Task 2.9: Component unit tests (frontend validation)
- Task 2.10: Visual verification via Chrome DevTools MCP
