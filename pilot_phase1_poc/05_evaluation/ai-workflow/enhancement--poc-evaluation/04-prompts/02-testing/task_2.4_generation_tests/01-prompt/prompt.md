# Task 2.4: Add Generation Unit Tests

**Phase:** Phase 2 — Systematic Testing
**Initiative:** enhancement--poc-evaluation

---

## Persona

You are a **QA Engineer** with expertise in:
- Jest testing with ESM modules
- Mocking async APIs (OpenAI/Groq client)
- LLM service testing patterns
- Node.js testing best practices

You write precise unit tests that validate behavior boundaries, not implementation details.

---

## Context

### Initiative
Waypoint Phase 1 POC — Week 4 Evaluation & Documentation. This task adds unit tests for the LLM generation layer to complete the test coverage for the backend pipeline.

### Reference Documents
- Master rules: `./CLAUDE.md`
- LLM service: `./backend/services/llm.js`
- Retrieval service: `./backend/services/retrieval.js` (for `formatContext`)
- System prompt: `./backend/prompts/system.txt`
- Config: `./backend/config.js`
- Existing LLM tests: `./tests/llm.test.js` (18 tests)
- Existing pipeline tests: `./tests/pipeline.test.js` (19 tests)

### Working Directory
`./pilot_phase1_poc/05_evaluation/`

### Current State
- `tests/llm.test.js` has **18 tests** covering:
  - `loadSystemPrompt()` — 5 tests (load, sections, placeholder, cache, reset)
  - `buildSystemPrompt()` — 3 tests (placeholder replacement, guidelines, context location)
  - `parseCompletion()` — 5 tests (valid parse, missing choices, undefined, missing usage, empty content)
  - `isRetryableError()` — 5 tests (429, 5xx, network, client errors, other)
  - `calculateBackoff()` — 3 tests (exponential, cap, jitter)
- `tests/pipeline.test.js` has **19 tests** covering the full pipeline flow with mocked services
- **GAP**: `generateResponse()` is NOT tested — it requires mocking the OpenAI client
- **GAP**: `formatContext()` has no dedicated tests (only tested indirectly via pipeline)
- **GAP**: System prompt content validation for T1.1 formatting instructions is minimal (only checks section headers exist)

### Existing Mocking Pattern (from pipeline.test.js)
```javascript
import { jest } from '@jest/globals';

// ESM mock pattern — must use jest.unstable_mockModule BEFORE dynamic import
jest.unstable_mockModule('../backend/services/llm.js', () => ({
  generateResponse: jest.fn(),
}));

// Dynamic import AFTER mock setup
const { processQuery } = await import('../backend/services/pipeline.js');
const { generateResponse } = await import('../backend/services/llm.js');
```

### Key Implementation Details

**`generateResponse(query, context, options)`** (`llm.js:89-150`):
- Calls `initLLMClient()` which creates an OpenAI client singleton
- Builds messages array: `[{role:'system', content: systemPrompt}, {role:'user', content: query}]`
- Uses `options.systemPrompt` if provided, otherwise calls `buildSystemPrompt(context)`
- Retry loop: up to `options.maxRetries` (default 3) with exponential backoff
- Calls `client.chat.completions.create()` with model, messages, temperature, max_tokens from config
- Returns `parseCompletion(completion)` result
- On retryable error: waits with backoff, tries again
- On non-retryable error or exhausted retries: throws `Error('LLM request failed: ...')`

**`formatContext(chunks, maxChars)`** (`retrieval.js:174-194`):
- Iterates chunks, building `[Title > Section]\ncontent\n\n` entries
- Truncates when `charCount + entry.length > maxChars`
- Returns trimmed context string

**Config values used** (`config.js`):
- `config.llmModel` = 'llama-3.1-8b-instant'
- `config.llmTemperature` = 0.3
- `config.llmMaxTokens` = 500
- `config.maxContextTokens` = 2000

### Dependencies
- **Requires**: T2.3 (PASSED — 94% hit rate confirmed)
- **Blocks**: None

---

## Task

### Objective
Create `tests/generation.test.js` with unit tests covering the untested generation layer functions. Focus on the gaps NOT covered by existing `llm.test.js` and `pipeline.test.js`.

### Test Groups to Write

#### Group 1: `generateResponse` with mocked OpenAI client (~8-10 tests)
Mock the OpenAI client to test `generateResponse()` without real API calls:

1. **Successful generation** — mock `client.chat.completions.create` to return valid completion, verify `generateResponse` returns parsed result with answer, usage, model
2. **Messages construction** — verify the messages array sent to the API has system + user roles with correct content
3. **Config values passed** — verify model, temperature, max_tokens from config are passed to create()
4. **Custom system prompt** — when `options.systemPrompt` is provided, it's used instead of calling buildSystemPrompt
5. **Retry on 429** — mock first call to throw {status: 429}, second call succeeds. Verify it retries and returns success.
6. **Retry on 5xx** — mock first call to throw {status: 503}, second call succeeds
7. **No retry on 4xx** — mock to throw {status: 400}. Verify it throws immediately (only 1 call made)
8. **Exhausted retries** — mock all calls to throw {status: 429}. Verify it throws after maxRetries
9. **Custom maxRetries** — pass `options.maxRetries = 1`. Verify only 1 attempt is made
10. **Missing API key** — ensure `initLLMClient` throws when `config.llmApiKey` is falsy

**Mocking strategy**: Since `generateResponse` calls `initLLMClient()` internally, you need to mock the OpenAI constructor or the module so that `initLLMClient` returns a client with a mock `chat.completions.create`. Use `jest.unstable_mockModule('openai', ...)` to mock the OpenAI default export.

#### Group 2: `formatContext` tests (~5-6 tests)
Direct unit tests for the context assembly function:

1. **Basic formatting** — single chunk produces `[Title > Section]\ncontent`
2. **Multiple chunks** — concatenated with double newlines
3. **Missing section** — produces `[Title]` without `>` separator
4. **Missing title** — falls back to 'Unknown Document'
5. **Truncation** — when chunks exceed maxChars, later chunks are dropped
6. **Empty chunks array** — returns empty string

#### Group 3: System prompt content validation (~3-4 tests)
Validate the T1.1 formatting instructions are present in the system prompt:

1. **Contains T1.1 formatting sections** — "Be Direct and Scannable", "Cite Your Sources Inline", "Handle Limitations Honestly"
2. **Contains citation format instruction** — `[Title > Section]` pattern
3. **Contains out-of-scope handling** — instructions for declining live rates, tracking, bookings
4. **Context placeholder is properly replaced** — after buildSystemPrompt, no `{context}` remains

### Constraints
- Use ESM imports and `jest.unstable_mockModule` pattern
- Mock `sleep` in generateResponse tests to avoid real delays (or use `jest.useFakeTimers`)
- Do NOT modify any source files — tests only
- All existing tests must still pass after adding new tests
- Follow the naming convention: `tests/generation.test.js`

---

## Format

### Output File
Create `tests/generation.test.js` in the working directory.

### Test Structure
```javascript
import { jest } from '@jest/globals';

describe('Generation Layer', () => {
  describe('generateResponse', () => { /* Group 1 */ });
  describe('formatContext', () => { /* Group 2 */ });
  describe('System Prompt Content', () => { /* Group 3 */ });
});
```

### Running Tests
```bash
cd pilot_phase1_poc/05_evaluation
npx jest tests/generation.test.js --experimental-vm-modules
# Then verify all tests:
npx jest --experimental-vm-modules
```

### Output Report
Create `TASK_2.4_OUTPUT.md` in the `02-output/` folder with:

```markdown
# Task 2.4 Output — Add Generation Unit Tests

**Task:** 2.4 — Add generation unit tests
**Phase:** Phase 2 — Systematic Testing
**Status:** [PASS/FAIL]
**Date:** [Date]

---

## Summary

[1-2 sentence overview: number of new tests, what they cover, all green?]

---

## New File

### `tests/generation.test.js` — [N] tests across 3 groups

| Group | Tests | What It Validates |
|-------|-------|-------------------|
| generateResponse | [N] | Mocked OpenAI client, retry logic, error handling |
| formatContext | [N] | Context assembly, truncation, edge cases |
| System Prompt Content | [N] | T1.1 formatting instructions present |

---

## Test Results

| Metric | Value |
|--------|-------|
| New Tests | [N] |
| Passed | [N] |
| Failed | [N] |
| Existing Jest Tests | [N]/[N] |
| **Combined Jest Total** | **[N]/[N]** |

---

## Issues Encountered

[Any mocking challenges, test fixes, etc.]

---

## Validation

| Criterion | Status |
|-----------|--------|
| generateResponse tests pass with mocked client | [PASS/FAIL] |
| formatContext tests pass | [PASS/FAIL] |
| System prompt content tests pass | [PASS/FAIL] |
| All existing tests still pass | [PASS/FAIL] |

---

## Next Steps

- Task 2.5: Update citation service tests
- Task 2.6: Update existing backend tests
```

### Tracking Updates
After completion:
1. Update `IMPLEMENTATION_CHECKLIST.md` — mark Task 2.4 `[x]`
2. Update `IMPLEMENTATION_ROADMAP.md` — set Task 2.4 status to `✅ Complete`
3. Update progress totals (Phase 2: 4/13, Overall: 14/43, 33%)
