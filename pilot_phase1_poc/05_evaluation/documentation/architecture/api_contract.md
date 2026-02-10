# API Contract

## Base Configuration

| Setting | Value |
|---------|-------|
| Base URL | `http://localhost:3000` |
| Content-Type | `application/json` |
| CORS | Enabled (all origins) |
| Body limit | 10kb |

## Endpoints

### POST /api/query

Process a customer service query through the RAG pipeline.

#### Request

```json
{
  "query": "string"
}
```

| Field | Type | Constraints |
|-------|------|-------------|
| `query` | string | Required, non-empty, max 1000 characters |

#### Response (200 OK)

```json
{
  "answer": "string — markdown-formatted response text with inline [citations]",
  "sources": [
    {
      "title": "string — document title",
      "org": "string — source organization",
      "url": "string — external URL",
      "section": "string|null — section within document"
    }
  ],
  "relatedDocs": [
    {
      "title": "string — document title",
      "category": "string — regulatory|carrier|reference|internal",
      "docId": "string — unique document ID",
      "url": "string|null — external URL if available"
    }
  ],
  "citations": [
    {
      "raw": "string — original bracketed text e.g. [Title > Section]",
      "title": "string — extracted title",
      "section": "string|null — extracted section",
      "matched": true,
      "sourceUrls": ["string — enriched URLs"],
      "docId": "string — matched document ID",
      "score": 0.85
    }
  ],
  "confidence": {
    "level": "High|Medium|Low",
    "reason": "string — human-readable explanation"
  },
  "metadata": {
    "query": "string — original query",
    "chunksRetrieved": 7,
    "chunksUsed": 3,
    "latencyMs": 1234,
    "model": "string|null — LLM model ID"
  }
}
```

#### Response Fields Detail

**`answer`** (string)
- Markdown-formatted response text
- Contains inline citations in `[Document Title > Section]` format
- Rendered by the frontend using `react-markdown` with `remark-gfm`

**`sources`** (array)
- External reference links extracted from matched citations
- Only includes citations that have external URLs (not internal documents)
- Deduplicated by URL

**`relatedDocs`** (array)
- Unique parent documents from all retrieved chunks
- Category is mapped from folder names: `01_regulatory` → `regulatory`, `02_carriers` → `carrier`, `03_reference` → `reference`, `04_internal_synthetic` → `internal`
- Includes documents even if not directly cited in the answer

**`citations`** (array)
- Only includes matched citations (`matched: true`)
- Each citation links to the source chunk with similarity score
- Unmatched citations are filtered out of the response

**`confidence`** (object)
- `level`: One of `High`, `Medium`, `Low`
- `reason`: Explains the confidence determination (e.g., chunk count, average score)
- Scoring rules:
  - **High**: ≥3 chunks AND average score ≥ 0.5
  - **Medium**: ≥2 chunks AND average score ≥ 0.3
  - **Low**: Everything else

**`metadata`** (object)
- `chunksRetrieved`: Number of chunks after threshold filter
- `chunksUsed`: Number of citations matched to chunks
- `latencyMs`: Total pipeline duration in milliseconds
- `model`: LLM model identifier (null if LLM was not called, e.g., no-results path)

#### Error Responses

**400 Bad Request** — Invalid input

```json
{
  "error": "Bad Request",
  "message": "Query parameter is required and must be a string"
}
```

| Condition | Message |
|-----------|---------|
| Missing or non-string query | `"Query parameter is required and must be a string"` |
| Empty query (whitespace only) | `"Query cannot be empty"` |
| Query > 1000 characters | `"Query exceeds maximum length of 1000 characters"` |

**500 Internal Server Error** — Pipeline failure

```json
{
  "error": "Internal Server Error",
  "message": "Pipeline error: <details>"
}
```

Causes: ChromaDB unavailable, Groq API failure after retries, Python subprocess crash.

---

### GET /api/health

Returns server health status. Used for monitoring and readiness checks.

#### Response (200 OK)

```json
{
  "status": "ok",
  "timestamp": "2026-02-10T08:30:00.000Z",
  "uptime": 3600,
  "version": "1.0.0"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Always `"ok"` when server is running |
| `timestamp` | string | ISO 8601 timestamp |
| `uptime` | number | Server uptime in seconds |
| `version` | string | From `package.json` or default `"1.0.0"` |

---

## No-Results Response Shape

When the pipeline finds zero chunks above the relevance threshold, it returns a special response without calling the LLM:

```json
{
  "answer": "I don't have specific information about that topic in my knowledge base. Please try rephrasing your question or contact our customer service team for assistance.",
  "sources": [],
  "relatedDocs": [],
  "citations": [],
  "confidence": {
    "level": "Low",
    "reason": "No relevant documents found"
  },
  "metadata": {
    "query": "original query",
    "chunksRetrieved": 0,
    "chunksUsed": 0,
    "latencyMs": 205,
    "model": null
  }
}
```

## Server Configuration

| Setting | Default | Environment Variable |
|---------|---------|---------------------|
| Port | 3000 | `PORT` |
| Node environment | development | `NODE_ENV` |
| CORS | All origins | — (hardcoded) |
| Body limit | 10kb | — (hardcoded) |
| Request logging | All non-health requests | — (debug level) |
| Graceful shutdown | SIGTERM handler | — |

## Related Documentation

- [Data Flow](data_flow.md) — End-to-end sequence diagram
- [RAG Pipeline Flow](rag_pipeline_flow.md) — Pipeline stage details
- See [routes.md](../codebase/backend/routes.md) for route implementation details
