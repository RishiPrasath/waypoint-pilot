# Task 2.7 Prompt — Add New Endpoint Tests

## Persona
Senior QA engineer writing response-shape validation tests for the `/api/query` endpoint.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Phase**: Phase 2 — Systematic Testing (Layer 3: Express Backend)
- **Dependencies**: T2.6 (complete — existing tests verified aligned)
- **Current test count**: 147 tests, 7 suites (all passing)

### Background
The existing `api.test.js` has 11 tests covering basic endpoint behavior (valid query, 400 errors, 500 errors, CORS). But it uses a minimal mock (`sources: [], relatedDocs: []`) and doesn't validate the **shape** of populated response sections. We need tests that verify:
1. A rich mock response flows correctly through the endpoint
2. Each response section has the correct data types and field names
3. Enum values (confidence.level, relatedDocs[].category) are valid

### Current Response Structure (from pipeline.js → query.js → client)
```javascript
{
  answer: string,                    // LLM response text
  sources: [{                        // External sources with URLs
    title: string,
    org: string,
    url: string,                     // Valid HTTP URL
    section: string|null,
  }],
  relatedDocs: [{                    // All retrieved parent documents
    title: string,
    category: string,                // 'regulatory'|'carrier'|'reference'|'internal' (or raw)
    docId: string,
    url: string|null,                // URL or null for internal docs
  }],
  citations: [{                      // Matched citations only
    raw: string,
    title: string,
    section: string|null,
    position: number,
    matched: true,
    sourceUrls: string[],
    docId: string|null,
    score: number|null,
    fullTitle: string,
  }],
  confidence: {
    level: 'High'|'Medium'|'Low',
    reason: string,
  },
  metadata: {
    query: string,
    chunksRetrieved: number,
    chunksUsed: number,
    latencyMs: number,
    model: string,
  },
}
```

### Files to Read
- `tests/api.test.js` — existing endpoint tests (extend this file)
- `backend/routes/query.js` — route handler
- `backend/services/pipeline.js` — processQuery return shape

## Task

Add a new `describe('Response shape validation')` block to `tests/api.test.js` with these tests:

1. **Full response contains all 6 top-level keys** — use a rich mock with populated sources/relatedDocs/citations
2. **`sources` array items have correct shape** — each has `title` (string), `org` (string), `url` (string starting with http), `section` (string or null)
3. **`relatedDocs` array items have correct shape** — each has `title` (string), `category` (string), `docId` (string), `url` (string or null)
4. **`confidence` has valid level enum** — `level` is one of 'High', 'Medium', 'Low'
5. **`confidence` has reason string** — non-empty string
6. **`metadata` has all required fields** — `query`, `chunksRetrieved`, `chunksUsed`, `latencyMs`, `model`
7. **`citations` only contains matched items** — `matched` is true for all items

Use a richer mock than the existing one, with populated arrays:
```javascript
const richMockResult = {
  answer: 'For Singapore exports, you need...',
  sources: [
    { title: 'Export Guide', org: 'Singapore Customs', url: 'https://customs.gov.sg/export', section: 'Documents' },
  ],
  relatedDocs: [
    { title: 'Export Guide', category: 'regulatory', docId: 'sg_export_guide', url: 'https://customs.gov.sg/export' },
    { title: 'Booking SOP', category: 'internal', docId: 'booking_sop', url: null },
  ],
  citations: [
    { raw: '[Export Guide > Documents]', title: 'Export Guide', section: 'Documents', position: 30, matched: true, sourceUrls: ['https://customs.gov.sg/export'], docId: 'sg_export_guide', score: 0.85, fullTitle: 'Export Guide' },
  ],
  confidence: { level: 'High', reason: '3 relevant sources with 2 citations' },
  metadata: { query: 'What documents for export?', chunksRetrieved: 3, chunksUsed: 2, latencyMs: 250, model: 'llama-3.1-8b-instant' },
};
```

## Format
- **Modify**: `tests/api.test.js` — add new describe block
- **Output**: `TASK_2.7_OUTPUT.md` in the output directory
- **Validation**: `npm test` — all suites green
