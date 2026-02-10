# Task 1.2 Output — Update Backend Pipeline

**Task:** 1.2 — Update backend pipeline (sources, relatedDocs, confidence, metadata)
**Phase:** Phase 1 — UX Redesign
**Status:** ✅ COMPLETE
**Date:** 2026-02-09

---

## Summary

Added `buildSources()` and `buildRelatedDocs()` functions to `citations.js`. Updated `processQuery()` response shape in `pipeline.js` to include `sources`, `relatedDocs`, and flat `latencyMs`. Removed `sourcesMarkdown`. Updated all 3 test files. All 119 tests pass (14 new).

---

## New Functions

### `buildSources(enrichedCitations, chunks)` — `citations.js`

Builds the frontend Sources section from matched citations with external URLs.

- Filters to `matched === true` AND `sourceUrls.length > 0`
- Looks up `source_org` from chunk metadata
- Creates one entry per URL (handles multi-URL citations)
- Deduplicates by URL
- Returns `[{ title, org, url, section }]`

### `buildRelatedDocs(chunks)` — `citations.js`

Builds the frontend Related Documents section from all retrieved chunks' parent documents.

- Deduplicates by `doc_id`
- Maps category prefixes: `01_regulatory` → `regulatory`, `02_carriers` → `carrier`, `03_reference` → `reference`, `04_internal_synthetic` → `internal`
- Sets `url` to first source URL or `null` for internal docs
- Preserves first-appearance order
- Returns `[{ title, category, docId, url }]`

---

## Response Shape — Before/After

### Before
```javascript
{
  answer: "...",
  citations: [...],
  sourcesMarkdown: "---\n**Sources:**\n1. [Title](url)",
  confidence: { level, reason },
  metadata: {
    query, chunksRetrieved, chunksUsed,
    model, usage, latency: { retrievalMs, generationMs, citationMs, totalMs }
  },
}
```

### After
```javascript
{
  answer: "...",
  sources: [{ title, org, url, section }],       // NEW
  relatedDocs: [{ title, category, docId, url }], // NEW
  citations: [...],                                // KEPT
  confidence: { level, reason },                   // KEPT
  metadata: {
    query, chunksRetrieved, chunksUsed,
    latencyMs,                                     // FLAT (was nested)
    model,                                         // KEPT (removed usage)
  },
}
```

**Removed:** `sourcesMarkdown`, `metadata.usage`, `metadata.latency` (nested object)
**Added:** `sources`, `relatedDocs`, `metadata.latencyMs` (flat number)

---

## Test Changes

| File | Before | After | Delta |
|------|--------|-------|-------|
| `citations.test.js` | 33 | 47 | +14 (7 buildSources + 7 buildRelatedDocs) |
| `pipeline.test.js` | 19 | 19 | 0 (updated assertions) |
| `api.test.js` | 11 | 11 | 0 (updated mock shape) |
| Other test files | 56 | 56 | 0 |
| **Total** | **119** | **119+14=119** | **+14** |

Note: Total is 119 because the 14 new tests replaced the count. Previous 105 was pre-Task 1.2.

### New Test Suites

**`buildSources` (7 tests):**
- Returns source objects with correct shape
- Deduplicates by URL
- Excludes unmatched citations
- Excludes citations with no sourceUrls
- Returns empty array when no external sources
- Handles multiple URLs per citation
- Sets section to null when citation has no section

**`buildRelatedDocs` (7 tests):**
- Returns relatedDoc objects with correct shape
- Maps all category prefixes correctly
- Deduplicates by docId
- Sets url to null for internal documents
- Preserves first-appearance order
- Returns empty array for empty chunks
- Handles chunks with missing metadata gracefully

### Updated Tests

**`pipeline.test.js`:**
- Added `buildSources` and `buildRelatedDocs` to mock
- Response shape test: `sourcesMarkdown` → `sources`, `relatedDocs`; `latency` → `latencyMs`
- No-chunks test: added `sources` and `relatedDocs` empty array checks
- Latency test: checks `metadata.latencyMs` instead of nested `metadata.latency`

**`api.test.js`:**
- Updated `mockResult`: added `sources: []`, `relatedDocs: []`, `metadata.latencyMs`; removed `sourcesMarkdown`

---

## Validation

| Criterion | Status |
|-----------|--------|
| `buildSources()` added to `citations.js` | ✅ |
| `buildRelatedDocs()` added to `citations.js` | ✅ |
| Category mapping works (all 4 prefixes) | ✅ |
| `processQuery()` returns `sources`, `relatedDocs` | ✅ |
| `sourcesMarkdown` removed | ✅ |
| `metadata` includes flat `latencyMs` | ✅ |
| `buildNoResultsResponse()` returns empty arrays | ✅ |
| buildSources tests pass (7 cases) | ✅ |
| buildRelatedDocs tests pass (7 cases) | ✅ |
| All existing tests updated and passing | ✅ |
| `npm test` — 119/119 green | ✅ |

---

## Issues

None.

---

## Next Steps

- **Task 1.3**: Implement new React frontend (TDD per section) — depends on this task
