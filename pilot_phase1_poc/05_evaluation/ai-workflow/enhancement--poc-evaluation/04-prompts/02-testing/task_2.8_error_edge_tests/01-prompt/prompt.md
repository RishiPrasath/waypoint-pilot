# Task 2.8 Prompt — Add Error/Edge Case Tests

## Persona
Senior QA engineer adding error condition and edge-case tests for the Express backend.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Phase**: Phase 2 — Systematic Testing (Layer 3: Express Backend)
- **Dependencies**: T2.6 (complete)
- **Current test count**: 154 tests, 7 suites (all passing)

### What's Already Tested (avoid duplication)

**api.test.js** (endpoint level):
- Missing query → 400 ✅
- Empty query → 400 ✅
- Whitespace-only query → 400 ✅
- Non-string query (number) → 400 ✅
- Query exceeding 1000 chars → 400 ✅
- Pipeline errors (generic) → 500 ✅

**pipeline.test.js** (service level):
- Empty query → throws ✅
- ChromaDB unavailable → throws "Pipeline error: ChromaDB unavailable" ✅
- Groq API error → throws "Pipeline error: Groq API error" ✅

**generation.test.js** (LLM level):
- 429 rate limit → retries ✅
- 503 server error → retries ✅
- 400 client error → throws without delay ✅
- Exhausting retries → throws ✅

### Real Gaps to Fill

| # | Gap | Layer | Why Not Covered |
|---|-----|-------|-----------------|
| 1 | Very long query (10K+ chars) | API endpoint | Only 1001 tested; extreme case untested |
| 2 | Malformed JSON body | API endpoint | No test sends invalid JSON (syntax error) |
| 3 | Wrong Content-Type | API endpoint | No test sends non-JSON Content-Type |
| 4 | Groq timeout → 500 via API | API endpoint | Pipeline-level mock exists but not through HTTP |
| 5 | ChromaDB failure → 500 via API | API endpoint | Pipeline-level mock exists but not through HTTP |
| 6 | Array/object as query value | API endpoint | Only number tested, not other non-string types |
| 7 | Special characters in query | Pipeline | Unicode, SQL injection, XSS payloads should be handled safely |

### Key Source Files
- `backend/routes/query.js` — route handler with validation (1000 char limit, type checks)
- `backend/index.js` — `express.json({ limit: '10kb' })` body size limit
- `backend/middleware/errorHandler.js` — global error handler
- `backend/services/pipeline.js` — processQuery orchestrator

## Task

Add error/edge case tests to `tests/api.test.js` in a new `describe('Error and edge cases')` block. Target the **actual gaps** listed above — do NOT duplicate existing tests.

### Tests to Write

1. **Very long query (10,000 chars)** — rejected by route validation (>1000 chars) with 400
2. **Malformed JSON body** — send raw string `"not json"` with `Content-Type: application/json` → Express returns 400
3. **Wrong Content-Type** — send `text/plain` body → Express handles gracefully
4. **Groq timeout through endpoint** — mock processQuery to reject with timeout error → 500
5. **ChromaDB failure through endpoint** — mock processQuery to reject with connection error → 500
6. **Array as query value** — `{ query: ['a', 'b'] }` → 400
7. **Object as query value** — `{ query: { nested: true } }` → 400
8. **Query with special characters** — Unicode, angle brackets, SQL-like input → processed normally (200)

### Important Notes
- Express `json({ limit: '10kb' })` rejects bodies >10KB with a 413 status — a 10K char query is within 10KB so it will pass body parsing and hit the 1000-char route validation
- The malformed JSON test needs `.set('Content-Type', 'application/json').send('not json')` — supertest's `.send(string)` with content-type set
- For infrastructure failure tests (4, 5), reuse the existing `processQuery` mock — just set different error messages
- Test 8 verifies the app doesn't crash or return errors on unusual-but-valid input

## Format
- **Modify**: `tests/api.test.js` — add new describe block
- **Output**: `TASK_2.8_OUTPUT.md` in the output directory
- **Validation**: `npm test` — all suites green, 154+ tests
