# Backend Tests (Jest)

All Jest test files are located in `pilot_phase1_poc/05_evaluation/tests/`.

Every file uses `jest.unstable_mockModule()` for ESM mocking, following the pattern of declaring mocks before dynamic imports. Tests clear mocks in `beforeEach` via `jest.clearAllMocks()`.

---

## api.test.js (11 tests)

**What it tests**: Express HTTP endpoints via `supertest`.

**Mock setup**: Mocks `pipeline.js` (the `processQuery` function). Imports the Express `app` after mock registration.

```javascript
jest.unstable_mockModule('../backend/services/pipeline.js', () => ({
  processQuery: jest.fn(),
  calculateConfidence: jest.fn(),
}));
const { default: app } = await import('../backend/index.js');
```

**Test groups**:

| Group | Tests | Description |
|-------|-------|-------------|
| `GET /api/health` | 1 | Returns 200 with `status: "ok"`, timestamp, and uptime |
| `POST /api/query` | 8 | Valid query processing, 400 for missing/empty/whitespace/non-string/too-long queries, 500 on pipeline errors, content-type header |
| `404 handling` | 1 | Unknown routes return 404 with `error: "Not Found"` |
| `CORS` | 1 | OPTIONS preflight returns `access-control-allow-origin` header |

**Key validation details**:
- Maximum query length: 1000 characters (returns 400 above that)
- Query must be a non-empty string (rejects numbers, arrays, objects)
- Pipeline errors are caught and returned as 500

---

## pipeline.test.js (19 tests)

**What it tests**: `processQuery` orchestration flow and `calculateConfidence` scoring logic.

**Mock setup**: Mocks three service modules -- `retrieval.js`, `llm.js`, and `citations.js`.

```javascript
jest.unstable_mockModule('../backend/services/retrieval.js', () => ({
  retrieveChunks: jest.fn(),
  formatContext: jest.fn(),
  getMetadataForCitation: jest.fn(),
}));
jest.unstable_mockModule('../backend/services/llm.js', () => ({
  generateResponse: jest.fn(),
}));
jest.unstable_mockModule('../backend/services/citations.js', () => ({
  processCitations: jest.fn(),
  buildSources: jest.fn(),
  buildRelatedDocs: jest.fn(),
}));
```

**Test groups**:

| Group | Tests | Description |
|-------|-------|-------------|
| `processQuery` | 12 | Full pipeline flow, structured response shape, no-chunks handling, empty/invalid query rejection, latency tracking, error propagation, options passthrough, query trimming, citation filtering |
| `calculateConfidence` | 7 | High/Medium/Low confidence levels based on chunk scores and citation counts |

**Confidence scoring thresholds** (T3.2 values):
- **High**: avgScore >= 0.5 and >= 2 chunks with matched citations
- **Medium**: avgScore >= 0.3
- **Low**: below Medium threshold, or single source only

**Key behaviors verified**:
- When zero chunks are retrieved, LLM is NOT called (short-circuit to Low confidence)
- Query whitespace is trimmed before passing to retrieval
- Only `matched: true` citations are included in the response
- Errors from retrieval/LLM are wrapped as `"Pipeline error: ..."` messages

---

## retrieval.test.js (15 tests)

**What it tests**: Pure retrieval functions -- `filterByThreshold`, `formatContext`, `getMetadataForCitation`, and `initChromaClient`.

**Mock setup**: No mocking required -- these are pure functions imported directly from `retrieval.js`.

```javascript
import { filterByThreshold, formatContext, getMetadataForCitation, initChromaClient }
  from '../backend/services/retrieval.js';
```

**Test groups**:

| Group | Tests | Description |
|-------|-------|-------------|
| `initChromaClient` | 1 | Returns true (bridge ready) |
| `filterByThreshold` | 4 | Filters chunks below score threshold; handles empty arrays; threshold=0 returns all |
| `formatContext` | 6 | Formats `[Title > Section]` headers; handles missing section/metadata; respects max character limit; separates chunks with double newlines |
| `getMetadataForCitation` | 4 | Extracts citation metadata from chunks; parses comma-separated `source_urls`; handles missing fields; handles empty/multiple chunks |

**Key formatting rules**:
- Title with section: `[Export Guide > Documents]`
- Title without section: `[Customs Overview]`
- Missing title: `[Unknown Document]`
- `source_urls` stored as comma-separated string in ChromaDB, split into array on retrieval

---

## llm.test.js (18 tests)

**What it tests**: LLM service pure functions -- `loadSystemPrompt`, `buildSystemPrompt`, `parseCompletion`, `isRetryableError`, `calculateBackoff`.

**Mock setup**: No external mocks. Uses `resetLLMClient()` and `resetSystemPrompt()` between tests to clear cached state.

```javascript
import {
  loadSystemPrompt, buildSystemPrompt, parseCompletion,
  isRetryableError, calculateBackoff, resetLLMClient, resetSystemPrompt,
} from '../backend/services/llm.js';
```

**Test groups**:

| Group | Tests | Description |
|-------|-------|-------------|
| `loadSystemPrompt` | 5 | Returns non-empty string; contains expected sections (Role, Guidelines, Citations, Out of Scope); has `{context}` placeholder; caches template; reset clears cache |
| `buildSystemPrompt` | 3 | Replaces `{context}` placeholder with actual context; includes guidelines; places context after `KNOWLEDGE BASE CONTEXT:` marker |
| `parseCompletion` | 5 | Parses valid OpenAI-format completion; throws on missing/empty choices; handles missing usage stats; handles empty message content |
| `isRetryableError` | 5 | Retries on 429 (rate limit), 5xx server errors, ECONNRESET/ETIMEDOUT network errors; does NOT retry on 4xx client errors |
| `calculateBackoff` | 3 | Exponential increase (1s, 2s, 4s base); caps at 10s max delay; applies 0-25% random jitter |

**Backoff formula**: `min(1000 * 2^(attempt-1), 10000) + random(0, 25%)`

---

## citations.test.js (47 tests)

**What it tests**: The full citation extraction, matching, enrichment, and formatting pipeline.

**Mock setup**: No mocking -- all functions are pure. Imported directly from `citations.js`.

```javascript
import {
  extractCitations, matchCitationToChunk, similarity,
  enrichCitations, formatCitationsMarkdown, deduplicateCitations,
  processCitations, buildSources, buildRelatedDocs,
} from '../backend/services/citations.js';
```

**Test groups**:

| Group | Tests | Description |
|-------|-------|-------------|
| `extractCitations` | 8 | Regex extraction of `[Title]` and `[Title > Section]` patterns; position tracking; multiple citations; no-match returns empty; ignores non-bracket formats |
| `similarity` | 6 | String similarity scoring (0-1); identical=1, completely different=0; case-insensitive; handles empty strings |
| `matchCitationToChunk` | 7 | Exact title match, case-insensitive match, partial title match, fuzzy matching with typos, null/empty chunk handling |
| `enrichCitations` | 7 | Adds `docId`, `sourceUrls`, `score`, `fullTitle` to matched citations; marks unmatched; handles multi-URL docs, empty URLs, N/A filtering, whitespace trimming |
| `formatCitationsMarkdown` | 5 | Generates `**Sources:**` markdown; links external URLs `[Title](url)`; marks internal docs `*(Internal Document)*`; deduplicates output; handles missing section |
| `deduplicateCitations` | 4 | Removes duplicate titles (case-insensitive); preserves first occurrence; handles empty arrays |
| `processCitations` | 3 | End-to-end: extracts, matches, enriches, formats; returns `citations`, `stats`, `markdown`; handles mixed matched/unmatched; no-citation case |
| `buildSources` | 7 | Produces `{title, org, url, section}` objects; deduplicates by URL; excludes unmatched citations; excludes citations with no sourceUrls; handles multiple URLs per citation; sets null section |
| `buildRelatedDocs` | 9 | Produces `{title, category, docId, url}` objects; maps category prefixes (`01_regulatory` -> `regulatory`, `02_carriers` -> `carrier`, `03_reference` -> `reference`, `04_internal_synthetic` -> `internal`); deduplicates by docId; null URL for internal docs; preserves order; handles missing metadata; falls back to raw value for unknown category; null URL for N/A source_urls |
| End-to-end enrichment flow | 2 | Full pipeline with mixed external/internal sources; full pipeline with internal-only sources |

---

## generation.test.js (50 tests)

**What it tests**: Three distinct groups covering the generation layer comprehensively.

### Group 1: generateResponse with mocked OpenAI client (10 tests)

**Mock setup**: Mocks `openai`, `config.js`, and `logger.js` modules before importing `llm.js`.

```javascript
jest.unstable_mockModule('openai', () => ({
  default: class MockOpenAI {
    constructor() {
      this.chat = { completions: { create: mockCreate } };
    }
  },
}));
jest.unstable_mockModule('../backend/config.js', () => ({
  config: {
    llmApiKey: 'test-api-key',
    llmModel: 'llama-3.1-8b-instant',
    llmTemperature: 0.3,
    llmMaxTokens: 500,
  },
}));
```

| Test | Description |
|------|-------------|
| Returns parsed result on success | Verifies answer, finishReason, usage, model fields |
| Constructs messages with system/user roles | 2-message array: system prompt + user query |
| Passes config values to API call | model, temperature, max_tokens from config |
| Uses custom systemPrompt when provided | Options override default prompt |
| Calls buildSystemPrompt when no custom prompt | Context inserted via `{context}` placeholder |
| Retries on 429 rate limit and succeeds | 2 attempts: fail then succeed |
| Retries on 503 server error and succeeds | Same retry behavior for server errors |
| Throws on non-retryable 400 client error | Fails fast (< 500ms) without backoff delay |
| Throws after exhausting retries | Respects maxRetries limit |
| Respects custom maxRetries option | `maxRetries: 1` limits to single attempt |

### Group 2: formatContext (6 tests)

**Mock setup**: Mocks `config.js` and `logger.js`, imports real `formatContext` from `retrieval.js`.

| Test | Description |
|------|-------------|
| Formats single chunk with title and section | `[Title > Section]` + content |
| Formats multiple chunks with double newline separator | Correct ordering |
| Omits section separator when section is empty | `[Title]` only |
| Falls back to Unknown Document | When title is missing from metadata |
| Truncates when chunks exceed maxChars | Only includes chunks that fit within limit |
| Returns empty string for empty chunks array | Edge case handling |

### Group 3: System Prompt Content Validation (5 tests)

**Mock setup**: Mocks `logger.js` and `config.js`, imports real `loadSystemPrompt` and `buildSystemPrompt`.

| Test | Description |
|------|-------------|
| Contains T1.1 formatting sections | "Be Direct and Scannable", "Cite Your Sources", "Handle Limitations", "Format with Markdown" |
| Contains citation format instruction with bracket pattern | `[Document Title > Section Name]` pattern, `MANDATORY` keyword |
| Contains out-of-scope handling | "Real-time tracking", "Live freight rates", "Booking changes" |
| Contains action request handling | "Action Request Handling", "knowledge assistant" |
| buildSystemPrompt replaces context completely | No `{context}` placeholder remains |

---

## placeholder.test.js (2 tests)

**What it tests**: Basic Jest and environment setup verification.

| Test | Description |
|------|-------------|
| Jest is configured correctly | `expect(true).toBe(true)` |
| Environment can be loaded | Imports `config.js` and verifies `config.port` is a defined number |

---

## Response Shape Validation (in api.test.js)

A dedicated `describe('Response shape validation')` block in `api.test.js` validates the full API response contract with a rich mock result:

| Test | Validates |
|------|-----------|
| Response contains all 6 top-level keys | `answer`, `sources`, `relatedDocs`, `citations`, `confidence`, `metadata` |
| Sources items have correct shape | `title: string`, `org: string`, `url: string (https://)`, `section: string|null` |
| RelatedDocs items have correct shape | `title: string`, `category: string`, `docId: string`, `url: string|null` |
| Confidence level is valid enum | `High`, `Medium`, or `Low` |
| Confidence reason is non-empty string | Always populated |
| Metadata contains required fields | `query`, `chunksRetrieved`, `chunksUsed`, `latencyMs`, `model` -- all correct types |
| Citations only contains matched items | `matched: true`, `title: string`, `raw: string`, `position: number` |

## Error and Edge Cases (in api.test.js)

| Test | Validates |
|------|-----------|
| Very long query (10,000 chars) | Returns 400 with "maximum length" message |
| Malformed JSON body | Returns 400 |
| Plain text body | Returns 400 (Express cannot parse text/plain as JSON) |
| Groq API timeout | Returns 500 with "timed out" in message |
| ChromaDB connection failure | Returns 500 with "ChromaDB" in message |
| Array as query value | Returns 400 |
| Object as query value | Returns 400 |
| Special characters (XSS, SQL) | Returns 200 -- safely processed by pipeline |
