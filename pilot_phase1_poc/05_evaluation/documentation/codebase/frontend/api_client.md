# API Client Documentation

**File**: `pilot_phase1_poc/05_evaluation/client/src/api/query.js`

## Overview

Minimal fetch-based API client for the Waypoint RAG pipeline. Two exported functions handle query submission and health checks. No external HTTP libraries are used -- the client relies on the native `fetch` API.

No authentication is required for any endpoint.

---

## Functions

### submitQuery(query, signal)

Submits a user query to the RAG pipeline and returns the full response.

**Signature**:
```js
export async function submitQuery(query: string, signal: AbortSignal): Promise<QueryResponse>
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | `string` | Yes | The user's question text |
| `signal` | `AbortSignal` | Yes | AbortController signal for request cancellation and cleanup |

**Returns**: `Promise<QueryResponse>` -- the parsed JSON response body.

**Request Details**:

| Property | Value |
|----------|-------|
| Method | `POST` |
| URL | `/api/query` |
| Content-Type | `application/json` |
| Body | `{ "query": "<user query>" }` |

**Error Handling**:

1. If `response.ok` is false (status >= 400):
   - Attempts to parse the response body as JSON.
   - If parsing succeeds, throws `new Error(error.message)`.
   - If parsing fails (non-JSON error response), throws `new Error("Request failed: {status}")`.
2. If the fetch is aborted via the signal, fetch throws a native `AbortError` (not caught here -- propagates to the caller).
3. Network errors propagate as-is.

**Example Usage**:
```js
const controller = new AbortController();
try {
  const result = await submitQuery('What are the customs requirements for Singapore?', controller.signal);
  console.log(result.answer);
} catch (err) {
  if (err.name !== 'AbortError') {
    console.error(err.message);
  }
}
```

---

### checkHealth()

Checks the API server health status.

**Signature**:
```js
export async function checkHealth(): Promise<Object>
```

**Parameters**: None.

**Returns**: `Promise<Object>` -- the parsed JSON health status response.

**Request Details**:

| Property | Value |
|----------|-------|
| Method | `GET` |
| URL | `/api/health` |

**Error Handling**:

No explicit error handling. Network errors and non-ok responses propagate as-is. The response is parsed as JSON unconditionally.

**Example Usage**:
```js
const health = await checkHealth();
console.log(health.status); // e.g., "ok"
```

---

## Response Types

### QueryResponse

The full response object returned by `submitQuery()`:

```js
{
  answer: string,             // Markdown-formatted answer from LLM
  sources: Source[],          // External URLs for the Sources section
  relatedDocs: RelatedDoc[],  // KB documents for the Related Docs section
  citations: Object[],       // Raw matched citations (internal use)
  confidence: Confidence,    // Confidence assessment
  metadata: ResponseMetadata  // Pipeline metadata and stats
}
```

### Source

```js
{
  title: string,              // Document title
  org: string,                // Source organization name
  url: string,                // Full external URL (https://...)
  section: string | null      // Document section, if applicable
}
```

### RelatedDoc

```js
{
  title: string,              // Document title
  category: string,           // "regulatory" | "carrier" | "internal" | "reference"
  docId: string,              // Unique document identifier
  url: string | null          // External URL, or null for internal docs
}
```

### Confidence

```js
{
  level: "High" | "Medium" | "Low",
  reason: string              // Explanation for the confidence level
}
```

### ResponseMetadata

```js
{
  query: string,              // Original query text
  chunksRetrieved: number,    // Total chunks retrieved from ChromaDB
  chunksUsed: number,         // Chunks matched by citation extraction
  latencyMs: number,          // Total pipeline latency in milliseconds
  model: string               // LLM model identifier
}
```

Type definitions are documented as JSDoc typedefs in `src/types.js`.

---

## Dev Server Proxy Configuration

During development, the Vite dev server proxies all `/api/*` requests to the Express backend. This is configured in `vite.config.js`:

```js
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:3000',
      changeOrigin: true,
    },
  },
}
```

**How it works**:

| Request from browser | Proxied to |
|---------------------|------------|
| `http://localhost:5173/api/query` | `http://localhost:3000/api/query` |
| `http://localhost:5173/api/health` | `http://localhost:3000/api/health` |

- `changeOrigin: true` modifies the `Host` header to match the target, preventing host-based routing issues on the backend.
- No path rewriting is applied -- `/api` prefix is preserved as-is.
- In production, the proxy is not used. The built static files are typically served by the same Express server or placed behind a reverse proxy.

---

## Integration with App.jsx

The API client is used exclusively in `App.jsx.handleSubmit`:

```
User submits query
  -> App creates AbortController
  -> App calls submitQuery(query, controller.signal)
  -> submitQuery POSTs to /api/query
  -> Vite proxy forwards to Express backend at localhost:3000
  -> Backend processes query through RAG pipeline
  -> JSON response returned
  -> App sets response state
  -> ResponseCard renders the 4-section card
```

`checkHealth()` is exported but not currently called from any component. It is available for future use (e.g., health indicator in the header, startup check).

---

## Design Decisions

1. **No Axios**: The client uses native `fetch` to minimize dependencies. The project has no HTTP client library.
2. **AbortSignal**: Passed through to `fetch()` for request cancellation. This prevents stale responses from overwriting newer ones if the user submits a new query before the previous one completes.
3. **JSON error extraction**: The client attempts to parse error responses as JSON to extract a `message` field. This allows the backend to return structured error messages (e.g., `{ "message": "Query text is required" }`).
4. **No retry logic**: Failed requests are not retried. The user can manually re-submit.
5. **No caching**: Responses are not cached. Each submission triggers a fresh API call.
6. **No base URL**: All paths are relative (`/api/query`, `/api/health`), relying on the Vite proxy in development and same-origin hosting in production.
