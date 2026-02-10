# Task 2.6 Prompt — Update Existing Backend Tests

## Persona
Senior QA engineer auditing existing Jest test suites for alignment with the Phase 1 UX redesign response structure.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Phase**: Phase 2 — Systematic Testing (Layer 3: Express Backend)
- **Dependencies**: CP2 (UX Redesign complete), Tasks 2.4-2.5 complete
- **Blocks**: T2.7 (new endpoint tests), T2.8 (error/edge case tests)

### Background
Phase 1 (Tasks 1.1-1.4) redesigned the response structure to include `sources`, `relatedDocs`, `answer`, `citations`, and `confidence`. The question is whether the existing test files were updated during Phase 1 or still reference the old structure.

### New Response Structure (from pipeline.js)
```javascript
{
  answer: string,
  sources: Array<{title, org, url, section}>,      // from buildSources()
  relatedDocs: Array<{title, category, docId, url}>, // from buildRelatedDocs()
  citations: Array<matched citations only>,
  confidence: { level: 'High'|'Medium'|'Low', reason: string },
  metadata: { query, chunksRetrieved, chunksUsed, latencyMs, model }
}
```

### Files to Audit
1. `tests/api.test.js` — 11 tests (API endpoint integration)
2. `tests/pipeline.test.js` — 19 tests (pipeline orchestrator + calculateConfidence)
3. `tests/retrieval.test.js` — 16 tests (filtering, formatting, metadata)
4. `tests/llm.test.js` — 18 tests (prompt loading, parsing, retry logic)

## Task
1. Read each of the 4 test files
2. Verify every assertion references the current response structure
3. Verify mock data shapes match current service signatures
4. Check confidence thresholds match current `calculateConfidence()` implementation (0.6 High, 0.4 Medium)
5. If any assertions or mocks are misaligned, update them
6. Run `npm test` to confirm all suites pass
7. Report findings

## Format
- Output: `TASK_2.6_OUTPUT.md` with audit findings per file
- If no changes needed, document the verification as a pass
- Run full `npm test` as validation
