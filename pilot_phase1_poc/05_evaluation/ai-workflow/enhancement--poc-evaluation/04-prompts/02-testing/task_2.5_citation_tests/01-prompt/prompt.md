# Task 2.5: Update Citation Service Tests

**Phase:** Phase 2 — Systematic Testing
**Initiative:** enhancement--poc-evaluation

---

## Persona

You are a **QA Engineer** with expertise in:
- Jest testing for pure-function service modules
- Edge case identification for data parsing pipelines
- Citation and metadata enrichment flows

You identify coverage gaps in existing tests and fill them precisely without duplicating what's already tested.

---

## Context

### Initiative
Waypoint Phase 1 POC — Week 4 Evaluation & Documentation. This task updates `citations.test.js` to validate the new enrichment flow added in Phase 1 (T1.2): `source_urls` and `category` flowing from chunk metadata into `sources` and `relatedDocs`.

### Reference Documents
- Master rules: `./CLAUDE.md`
- Citation service: `./backend/services/citations.js`
- Existing tests: `./tests/citations.test.js` (47 tests)

### Working Directory
`./pilot_phase1_poc/05_evaluation/`

### Current State — Existing Test Coverage (47 tests)

| Describe Group | Tests | Coverage |
|----------------|-------|----------|
| `extractCitations` | 7 | Primary `[Title]` and `[Title > Section]` patterns, position, raw text, duplicates |
| `similarity` | 6 | Identical, different, partial, empty, case-insensitive |
| `matchCitationToChunk` | 7 | Exact, case-insensitive, no match, empty/null, partial, fuzzy |
| `enrichCitations` | 4 | Matched citation, unmatched, multiple URLs, empty source_urls |
| `formatCitationsMarkdown` | 5 | URLs, internal docs, empty, dedup, no section |
| `deduplicateCitations` | 4 | Duplicates, case-insensitive, preserves first, empty |
| `processCitations` | 3 | Complete response, unmatched citations, no citations |
| `buildSources` | 7 | Shape, dedup by URL, unmatched, no URLs, empty, multiple URLs, null section |
| `buildRelatedDocs` | 7 | Shape, category mapping, dedup by docId, null URL for internal, order, empty, missing metadata |

### Coverage GAP Analysis

The roadmap's 5 stated requirements (source_urls parsing, category extraction, source dedup, relatedDocs dedup, missing source_urls) are **already covered** by Phase 1 tests. The actual gaps are:

1. **N/A source_urls filtering** — `enrichCitations` and `buildRelatedDocs` both filter `u !== 'N/A'`, but no test verifies that `'N/A'` values are excluded from the sourceUrls array (only empty string `''` is tested)
2. **URL trimming with spaces** — The code does `.map(u => u.trim())` on comma-separated URLs. No test verifies that ` https://url.com , https://url2.com ` (with spaces) is parsed correctly
3. **Alternative citation patterns** — The code has `ALT_PATTERNS` for `Source: Title` and `Reference: Title` formats, but NO tests exist for these patterns
4. **Unknown category fallback** — `buildRelatedDocs` uses `CATEGORY_MAP[rawCategory] || rawCategory`. No test verifies that an unknown category falls through to the raw value
5. **buildRelatedDocs with N/A source_urls** — Existing test uses empty string `''`. No test for `'N/A'` specifically (code should produce `url: null`)
6. **End-to-end enrichment flow** — No test verifies the combined flow: `processCitations` result → `buildSources` + `buildRelatedDocs` using the same chunks, validating that all three outputs are consistent

### Dependencies
- **Requires**: T2.3 (PASSED)
- **Blocks**: None

---

## Task

### Objective
Add tests to `tests/citations.test.js` that cover the 6 gaps identified above. Do NOT duplicate existing tests. Add new `test()` calls within the existing `describe()` groups.

### Tests to Add

#### In `enrichCitations` group (2 new tests):
1. **Filters out N/A from source_urls** — chunk has `source_urls: 'https://real.com,N/A'` → enriched citation should have `sourceUrls: ['https://real.com']` (N/A excluded)
2. **Trims spaces from source_urls** — chunk has `source_urls: ' https://url1.com , https://url2.com '` → enriched citation should have trimmed URLs

#### In `extractCitations` group (2 new tests):
3. **Extracts alternative "Source: Title" pattern** — text `'Source: Singapore Customs Guide is relevant'` → extracts citation with title `'Singapore Customs Guide'`
4. **Extracts alternative "Reference: Title" pattern** — text `'Reference: Export Documentation Guide should be consulted'` → extracts citation

#### In `buildRelatedDocs` group (2 new tests):
5. **Falls back to raw value for unknown category** — chunk with `category: 'custom_category'` → `category: 'custom_category'` (not mapped)
6. **Sets url to null when source_urls is N/A** — chunk has `source_urls: 'N/A'` → `url: null`

#### New `describe('End-to-end enrichment flow')` group (2 new tests):
7. **Full flow with mixed sources** — Process a response text citing 2 docs, with chunks containing real URLs, N/A URLs, and different categories. Verify `processCitations` → `buildSources` → `buildRelatedDocs` produce consistent results
8. **Full flow with internal-only sources** — All chunks are internal (empty/N/A source_urls). Verify `buildSources` returns empty array while `buildRelatedDocs` returns entries with `url: null`

### Constraints
- Add tests to the EXISTING `tests/citations.test.js` file — do NOT create a new file
- Add new `test()` calls within existing `describe()` blocks where possible
- Add a new `describe('End-to-end enrichment flow')` block for tests 7-8
- Do NOT modify the citation service source code
- All existing 47 tests must still pass
- Run full Jest suite to confirm no regressions

---

## Format

### Running Tests
```bash
cd pilot_phase1_poc/05_evaluation
npx jest tests/citations.test.js --experimental-vm-modules --verbose
# Then verify all tests:
npx jest --experimental-vm-modules
```

### Output Report
Create `TASK_2.5_OUTPUT.md` in the `02-output/` folder with:

```markdown
# Task 2.5 Output — Update Citation Service Tests

**Task:** 2.5 — Update citation service tests
**Phase:** Phase 2 — Systematic Testing
**Status:** [PASS/FAIL]
**Date:** [Date]

---

## Summary

[1-2 sentence overview: tests added, gaps filled, all green?]

---

## Tests Added

| # | Group | Test Name | Gap Covered |
|---|-------|-----------|-------------|
| 1 | enrichCitations | [name] | N/A filtering |
| 2 | enrichCitations | [name] | URL trimming |
| ... | ... | ... | ... |

---

## Test Results

| Metric | Value |
|--------|-------|
| New Tests | [N] |
| Existing Tests | 47/47 |
| **Combined citations.test.js** | **[N]/[N]** |
| **Combined Jest Total** | **[N]/[N]** |

---

## Validation

| Criterion | Status |
|-----------|--------|
| N/A source_urls filtering tested | [PASS/FAIL] |
| URL trimming tested | [PASS/FAIL] |
| Alternative citation patterns tested | [PASS/FAIL] |
| Unknown category fallback tested | [PASS/FAIL] |
| N/A source_urls → null URL tested | [PASS/FAIL] |
| End-to-end flow tested | [PASS/FAIL] |
| All existing tests still pass | [PASS/FAIL] |

---

## Next Steps

- Task 2.6: Update existing backend tests
- Task 2.7: Add new endpoint tests
```

### Tracking Updates
After completion:
1. Update `IMPLEMENTATION_CHECKLIST.md` — mark Task 2.5 `[x]`
2. Update `IMPLEMENTATION_ROADMAP.md` — set Task 2.5 status to `✅ Complete`
3. Update progress totals (Phase 2: 5/13, Overall: 15/43, 35%)
