# API Routes Documentation

## Purpose

The `backend/routes/` directory defines the HTTP endpoints exposed by the Express API. Routes are aggregated into a single router mounted at the `/api` prefix. The backend exposes two endpoints: a query endpoint for the RAG pipeline and a health check endpoint.

## File Index

| File | Purpose |
|------|---------|
| `routes/index.js` | Route aggregator; mounts sub-routers under `/api` |
| `routes/query.js` | `POST /api/query` -- RAG pipeline query handler |
| `routes/health.js` | `GET /api/health` -- Server health check |

---

## Route Aggregation (`routes/index.js`)

Creates an Express `Router` and mounts the two sub-routers:

```js
const router = Router();
router.use('/query', queryRoutes);
router.use('/health', healthRoutes);
export { router as apiRouter };
```

This `apiRouter` is mounted at `/api` in the main `index.js`:

```js
app.use('/api', apiRouter);
```

**Resulting route table:**

| Method | Path | Handler |
|--------|------|---------|
| `POST` | `/api/query` | `routes/query.js` |
| `GET` | `/api/health` | `routes/health.js` |

---

## POST /api/query (`routes/query.js`)

Processes a customer service query through the RAG pipeline.

### Request

**Method:** `POST`
**Path:** `/api/query`
**Content-Type:** `application/json`

**Body:**

```json
{
  "query": "What documents are required for importing goods into Singapore?"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `query` | `string` | Yes | Non-empty, max 1000 characters |

### Validation Rules

The handler performs three validation checks before calling the pipeline:

| Check | Condition | HTTP Status | Error Message |
|-------|-----------|-------------|---------------|
| Presence & type | `!query \|\| typeof query !== 'string'` | 400 | `Query parameter is required and must be a string` |
| Non-empty | `query.trim().length === 0` | 400 | `Query cannot be empty` |
| Max length | `query.length > 1000` | 400 | `Query exceeds maximum length of 1000 characters` |

### Success Response (200)

```json
{
  "answer": "To import goods into Singapore, you need...",
  "sources": [
    {
      "title": "Singapore Customs Import Procedures",
      "org": "Singapore Customs",
      "url": "https://www.customs.gov.sg/...",
      "section": "Documentation Requirements"
    }
  ],
  "relatedDocs": [
    {
      "title": "Singapore Customs Import Procedures",
      "category": "regulatory",
      "docId": "01_regulatory/singapore_customs_import",
      "url": "https://www.customs.gov.sg/..."
    }
  ],
  "citations": [
    {
      "raw": "[Singapore Customs Import Procedures > Documentation Requirements]",
      "title": "Singapore Customs Import Procedures",
      "section": "Documentation Requirements",
      "position": 45,
      "matched": true,
      "sourceUrls": ["https://www.customs.gov.sg/..."],
      "docId": "01_regulatory/singapore_customs_import",
      "score": 0.72,
      "fullTitle": "Singapore Customs Import Procedures"
    }
  ],
  "confidence": {
    "level": "High",
    "reason": "5 relevant sources with 2 citations"
  },
  "metadata": {
    "query": "What documents are required for importing goods into Singapore?",
    "chunksRetrieved": 5,
    "chunksUsed": 2,
    "latencyMs": 2340,
    "model": "llama-3.1-8b-instant"
  }
}
```

### Error Responses

**400 Bad Request -- Invalid Input:**

```json
{
  "error": "Bad Request",
  "message": "Query parameter is required and must be a string"
}
```

**500 Internal Server Error -- Pipeline Failure:**

Errors from the pipeline are passed to the `errorHandler` middleware via `next(error)`. The response shape follows the global error format:

```json
{
  "error": "Internal Server Error",
  "message": "Pipeline error: Retrieval failed: ...",
  "stack": "(development only)"
}
```

### Implementation Details

- Measures latency from request start to response
- Logs successful queries with query length, confidence level, and latency
- Delegates all processing to `processQuery()` from `services/pipeline.js`
- Errors are forwarded to Express error middleware via `next(error)`

---

## GET /api/health (`routes/health.js`)

Returns server health status. Used by monitoring tools and frontend connectivity checks.

### Request

**Method:** `GET`
**Path:** `/api/health`

No request body or query parameters.

### Response (200)

```json
{
  "status": "ok",
  "timestamp": "2026-02-09T14:30:00.000Z",
  "uptime": 3600,
  "version": "1.0.0"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `"ok"` |
| `timestamp` | `string` | ISO 8601 timestamp of the response |
| `uptime` | `number` | Server uptime in seconds (integer, floored) |
| `version` | `string` | From `npm_package_version` env var, defaults to `"1.0.0"` |

### Implementation Details

- Uptime is calculated from a module-level `startTime` captured at import time: `Math.floor((Date.now() - startTime) / 1000)`
- The request logger in `index.js` skips `/api/health` requests to reduce log noise
- No external dependencies are checked (ChromaDB, Groq) -- this is a liveness check only

---

## Route Dependencies

```
routes/index.js
├── routes/query.js
│   ├── services/pipeline.js  (processQuery)
│   └── utils/logger.js
└── routes/health.js
    └── (no external dependencies)
```
