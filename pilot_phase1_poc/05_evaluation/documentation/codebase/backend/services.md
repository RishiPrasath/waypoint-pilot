# Services Documentation

## Purpose

The `backend/services/` directory contains the core business logic for the RAG pipeline. Each service handles one stage of the pipeline: retrieval, context formatting, LLM generation, and citation processing. A pipeline orchestrator coordinates the stages and returns the final response.

## File Index

| File | Purpose |
|------|---------|
| `pipeline.js` | RAG pipeline orchestrator; coordinates all 4 stages |
| `retrieval.js` | ChromaDB vector search via Python subprocess |
| `llm.js` | Groq LLM client with retry logic |
| `citations.js` | Citation extraction, matching, and enrichment |
| `embedding.js` | Stub module (not implemented) |
| `index.js` | Barrel export aggregating all service functions |

---

## 1. pipeline.js -- RAG Pipeline Orchestrator

Coordinates the full retrieval-augmented generation flow in 4 sequential stages.

### Key Functions

#### `processQuery(query, options)`

Main entry point for the RAG pipeline.

```js
async function processQuery(query, options = {})
```

**Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | `string` | (required) | The customer's question |
| `options.topK` | `number` | `config.retrievalTopK` | Number of chunks to retrieve |
| `options.threshold` | `number` | `config.relevanceThreshold` | Minimum relevance score |

**Returns:** `Promise<Object>` with shape:

```js
{
  answer: string,          // LLM-generated response
  sources: Array,          // External URLs from matched citations
  relatedDocs: Array,      // Unique parent documents from all chunks
  citations: Array,        // Matched citation objects only
  confidence: {            // Confidence assessment
    level: 'High' | 'Medium' | 'Low',
    reason: string
  },
  metadata: {
    query: string,
    chunksRetrieved: number,
    chunksUsed: number,    // Citations that matched a chunk
    latencyMs: number,
    model: string | null
  }
}
```

**Pipeline Stages:**

1. **Retrieve** -- `retrieveChunks(query, { topK, threshold })` fetches and filters chunks from ChromaDB
2. **Format Context** -- `formatContext(chunks)` builds the context string for the LLM prompt
3. **Generate** -- `generateResponse(query, context)` calls Groq API with the system prompt
4. **Process Citations** -- `processCitations(answer, chunks)` extracts, matches, and enriches citations

**Error handling:** Wraps all errors as `Pipeline error: <original message>` and re-throws. Timing metrics (`retrievalMs`, `generationMs`, `citationMs`, `totalMs`) are tracked for each stage.

#### `calculateConfidence(chunks, citationResult)`

Determines the confidence level for a response based on retrieval quality.

```js
function calculateConfidence(chunks, citationResult)
```

| Level | Condition |
|-------|-----------|
| **High** | `chunks.length >= 3` AND `avgScore >= 0.5` |
| **Medium** | `chunks.length >= 2` AND `avgScore >= 0.3` |
| **Low** | Everything else (1 chunk, or low average scores) |

`avgScore` is computed as the arithmetic mean of all chunk `.score` values. The reason string includes chunk count and, for High confidence, the number of matched citations if any exist.

#### `buildNoResultsResponse(query, metrics, startTime)`

Returns a structured response when zero chunks survive threshold filtering.

```js
function buildNoResultsResponse(query, metrics, startTime)
```

Returns the standard response shape with a canned answer message, empty arrays for sources/citations/relatedDocs, `Low` confidence, and `model: null`.

**Dependencies:** `retrieval.js`, `llm.js`, `citations.js`, `config.js`, `logger.js`

---

## 2. retrieval.js -- ChromaDB Retrieval Service

Handles vector similarity search against the knowledge base using a Python subprocess bridge.

### Architecture

The Node.js backend does not connect to ChromaDB directly. Instead, it spawns a Python child process that runs `scripts/query_chroma.py`. Communication is JSON over stdin/stdout:

```
Node.js                    Python subprocess
  |                              |
  |-- JSON params (stdin) -----> |
  |                              |-- ChromaDB query
  |                              |-- Format results
  |<---- JSON results (stdout) --|
```

### Key Functions

#### `executePythonQuery(params)`

Internal function that spawns the Python subprocess.

```js
async function executePythonQuery(params)
```

**Behavior:**
- Tries venv Python first (`venv/Scripts/python.exe`), with fallback paths: `python`, `python3`, `py`
- Sends JSON parameters via stdin, reads JSON from stdout
- Rejects immediately in test environment (`NODE_ENV === 'test'`)
- Logs stderr output on non-zero exit codes

**Params sent to Python:**

```json
{
  "query": "user question text",
  "top_k": 10,
  "collection_name": "waypoint_kb"
}
```

#### `retrieveChunks(query, options)`

Public retrieval function. Calls Python bridge, then filters results by threshold.

```js
async function retrieveChunks(query, options = {})
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | `string` | (required) | Search query text |
| `options.topK` | `number` | `config.retrievalTopK` (10) | Number of results from ChromaDB |
| `options.threshold` | `number` | `config.relevanceThreshold` (0.15) | Minimum score to keep |

**Returns:** `Promise<Array>` of chunk objects that pass the threshold filter.

#### `filterByThreshold(chunks, threshold)`

Filters an array of chunks, keeping only those with `chunk.score >= threshold`.

```js
function filterByThreshold(chunks, threshold)
```

#### `formatContext(chunks, maxChars)`

Formats retrieved chunks into a context string for the LLM system prompt.

```js
function formatContext(chunks, maxChars = config.maxContextTokens * 4)
```

**Format per chunk:**

```
[Document Title > Section Name]
chunk content text here

```

If no section metadata exists, the header is `[Document Title]` without the section part. Concatenation stops when adding the next chunk would exceed `maxChars` (default: `2000 * 4 = 8000` characters).

#### `getMetadataForCitation(chunks)`

Extracts citation-relevant metadata from chunk objects.

```js
function getMetadataForCitation(chunks)
```

**Returns:** Array of `{ title, section, sourceUrls, docId, score }` objects. Source URLs are parsed by splitting the `source_urls` metadata string on commas.

#### `initChromaClient()` / `resetClient()`

No-op functions maintained for interface compatibility. The Python bridge requires no initialization. `resetClient()` is used in tests.

**Dependencies:** `child_process.spawn`, `config.js`, `logger.js`

---

## 3. llm.js -- LLM Service

Handles API calls to Groq (via OpenAI-compatible client) for response generation, with retry logic for transient failures.

### Key Functions

#### `initLLMClient()`

Singleton factory for the OpenAI client configured for Groq.

```js
function initLLMClient()
```

Returns the cached client if it exists. On first call, validates that `LLM_API_KEY` is set (throws if missing), then creates an `OpenAI` instance with `apiKey` and `baseURL` from config. Logs provider, model, and base URL on initialization.

#### `resetLLMClient()`

Sets the singleton client to `null`, forcing re-initialization on next call. Used in tests.

#### `generateResponse(query, context, options)`

Generates an LLM response with automatic retry for transient errors.

```js
async function generateResponse(query, context, options = {})
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | `string` | (required) | Customer question |
| `context` | `string` | (required) | Formatted context from `formatContext()` |
| `options.systemPrompt` | `string` | (auto-built) | Override system prompt |
| `options.maxRetries` | `number` | `3` | Maximum retry attempts |

**Message structure sent to Groq:**

```js
[
  { role: 'system', content: buildSystemPrompt(context) },
  { role: 'user', content: query }
]
```

**Retry behavior:**
- Retries on HTTP 429 (rate limit), 5xx (server errors), `ECONNRESET`, and `ETIMEDOUT`
- Exponential backoff with jitter: base 1s, doubling per attempt, max 10s
- Jitter adds 0--25% of the exponential delay
- After all retries exhausted, throws `LLM request failed: <message>`

#### `buildSystemPrompt(context)`

Loads the system prompt template from `prompts/system.txt` and replaces the `{context}` placeholder with the provided context string.

```js
function buildSystemPrompt(context)
```

The template is cached after first load via `loadSystemPrompt()`.

#### `loadSystemPrompt()` / `resetSystemPrompt()`

`loadSystemPrompt()` reads `prompts/system.txt` synchronously and caches it. `resetSystemPrompt()` clears the cache (used in tests).

#### `parseCompletion(completion)`

Extracts structured data from the OpenAI completion response.

```js
function parseCompletion(completion)
```

**Returns:**

```js
{
  answer: string,        // choices[0].message.content
  finishReason: string,  // choices[0].finish_reason
  usage: {
    promptTokens: number,
    completionTokens: number,
    totalTokens: number
  },
  model: string          // completion.model
}
```

Throws if `completion.choices` is empty or missing.

#### `isRetryableError(error)`

Returns `true` for errors that warrant a retry:

| Condition | Check |
|-----------|-------|
| Rate limit | `error.status === 429` |
| Server error | `error.status >= 500 && error.status < 600` |
| Network reset | `error.code === 'ECONNRESET'` |
| Network timeout | `error.code === 'ETIMEDOUT'` |

#### `calculateBackoff(attempt)`

Computes delay in milliseconds for retry attempt (1-based).

```js
function calculateBackoff(attempt)
```

Formula: `min(1000 * 2^(attempt-1) + jitter, 10000)` where jitter is `random() * 0.25 * exponentialDelay`.

| Attempt | Base Delay | Range with Jitter |
|---------|------------|-------------------|
| 1 | 1,000 ms | 1,000 -- 1,250 ms |
| 2 | 2,000 ms | 2,000 -- 2,500 ms |
| 3 | 4,000 ms | 4,000 -- 5,000 ms |
| 4+ | capped | max 10,000 ms |

**Dependencies:** `openai`, `fs.readFileSync`, `config.js`, `logger.js`

---

## 4. citations.js -- Citation Extractor Service

Parses bracket-format citations from LLM responses, matches them to retrieved chunks, and enriches them with source metadata.

### Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `CITATION_PATTERN` | `/\[([^\]]+)\]/g` | Regex matching `[Title]` and `[Title > Section]` |
| `SIMILARITY_THRESHOLD` | `0.5` | Minimum Dice coefficient for fuzzy title matching |
| `CATEGORY_MAP` | (see below) | Maps KB folder names to frontend category names |

**CATEGORY_MAP:**

```js
{
  '01_regulatory': 'regulatory',
  '02_carriers': 'carrier',
  '03_reference': 'reference',
  '04_internal_synthetic': 'internal'
}
```

### Key Functions

#### `extractCitations(text)`

Extracts all bracket-format citations from the LLM response text.

```js
function extractCitations(text)
```

**Behavior:**
- Matches all `[...]` patterns using the global regex
- Splits on `>` to separate title from section: `[Title > Section]`
- Deduplicates by lowercase title (first occurrence wins)
- Resets regex `lastIndex` after iteration (required for global regex reuse)

**Returns:** Array of `{ raw, title, section, position }` objects.

#### `matchCitationToChunk(citation, chunks)`

Matches a citation to the best matching chunk by title. Uses a three-tier strategy:

```js
function matchCitationToChunk(citation, chunks)
```

| Priority | Strategy | Description |
|----------|----------|-------------|
| 1 | Exact match | Case-insensitive title equality |
| 2 | Partial/contains | Either title contains the other |
| 3 | Dice similarity | `similarity() > 0.5` threshold |

Returns the first matching chunk or `null`.

#### `similarity(a, b)`

Computes Dice coefficient between two strings using character bigrams.

```js
function similarity(a, b)
```

Formula: `(2 * |intersection|) / (|A_bigrams| + |B_bigrams|)`

Returns a score between 0 and 1. Exact match returns 1, empty strings return 0.

#### `enrichCitations(citations, chunks)`

Enriches parsed citations with source metadata from matched chunks.

```js
function enrichCitations(citations, chunks)
```

For each citation, calls `matchCitationToChunk()`. If matched, extracts:
- `sourceUrls`: parsed from `metadata.source_urls` (comma-separated), filtered for valid HTTP URLs (excludes `N/A`)
- `docId`: from `metadata.doc_id`
- `score`: the chunk's relevance score
- `fullTitle`: from the chunk's metadata title

Unmatched citations get `matched: false` with empty/null fields.

#### `processCitations(responseText, chunks)`

Main entry point for the citation pipeline.

```js
function processCitations(responseText, chunks)
```

Calls `extractCitations()` -> `enrichCitations()` -> `formatCitationsMarkdown()`.

**Returns:**

```js
{
  citations: Array,   // Enriched citation objects
  markdown: string,   // Formatted markdown citation list
  stats: {
    total: number,    // Total citations found
    matched: number,  // Citations matched to a chunk
    unmatched: number // Citations with no chunk match
  }
}
```

#### `buildSources(enrichedCitations, chunks)`

Builds the `sources` array for the frontend Sources section.

```js
function buildSources(enrichedCitations, chunks)
```

Iterates matched citations, resolves `source_org` from the chunk metadata, and returns deduplicated objects:

```js
{ title: string, org: string, url: string, section: string | null }
```

URLs are deduplicated via a `Set`.

#### `buildRelatedDocs(chunks)`

Builds the `relatedDocs` array from all retrieved chunks (not just cited ones).

```js
function buildRelatedDocs(chunks)
```

Extracts unique parent documents by `doc_id` and maps the raw KB folder category through `CATEGORY_MAP`.

```js
{ title: string, category: string, docId: string, url: string | null }
```

#### `formatCitationsMarkdown(citations)` / `deduplicateCitations(citations)`

Formatting utilities. `formatCitationsMarkdown` produces a markdown list with numbered entries, external URLs as links, and internal documents marked with `*(Internal Document)*`. `deduplicateCitations` filters by lowercase title uniqueness.

**Dependencies:** `logger.js`

---

## 5. embedding.js -- Embedding Service (Stub)

Placeholder module for direct embedding generation. Not implemented because ChromaDB handles embeddings internally through its default model (all-MiniLM-L6-v2 via ONNX).

### Functions

#### `getQueryEmbedding(query)`

```js
async function getQueryEmbedding(query)
```

**Throws:** `Error('Not implemented: getQueryEmbedding')`

#### `batchEmbed(queries)`

```js
async function batchEmbed(queries)
```

**Throws:** `Error('Not implemented: batchEmbed')`

**Dependencies:** `config.js`, `logger.js` (imported but unused)

---

## 6. index.js -- Barrel Export

Central export point aggregating all public service functions.

```js
export { processQuery, calculateConfidence } from './pipeline.js';
export { retrieveChunks } from './retrieval.js';
export { generateResponse } from './llm.js';
export { getQueryEmbedding } from './embedding.js';
export {
  extractCitations,
  matchCitationToChunk,
  enrichCitations,
  formatCitationsMarkdown,
  deduplicateCitations,
  processCitations,
  similarity,
} from './citations.js';
```

This allows consumers to import from a single path:

```js
import { processQuery, retrieveChunks } from '../services/index.js';
```
