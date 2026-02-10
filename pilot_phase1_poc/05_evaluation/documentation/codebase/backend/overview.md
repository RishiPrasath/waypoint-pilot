# Backend Architecture Overview

## Purpose

The Waypoint backend is an Express.js API server that exposes a single RAG (Retrieval-Augmented Generation) pipeline endpoint for the customer service co-pilot. It receives natural-language queries, retrieves relevant knowledge base chunks via a Python subprocess bridge to ChromaDB, generates LLM responses through Groq, and returns enriched answers with citations, confidence scores, and source metadata.

## File Structure

```
backend/
├── index.js                   # Express application entry point
├── config.js                  # Environment variable loader
├── prompts/
│   └── system.txt             # LLM system prompt template
├── routes/
│   ├── index.js               # Route aggregator (mounts /query, /health)
│   ├── query.js               # POST /api/query handler
│   └── health.js              # GET /api/health handler
├── services/
│   ├── index.js               # Barrel export for all services
│   ├── pipeline.js            # RAG pipeline orchestrator
│   ├── retrieval.js           # ChromaDB retrieval via Python subprocess
│   ├── llm.js                 # Groq LLM client (OpenAI-compatible)
│   ├── citations.js           # Citation extraction and enrichment
│   └── embedding.js           # Stub (not implemented)
├── middleware/
│   └── errorHandler.js        # Global error + 404 handlers
└── utils/
    └── logger.js              # Structured logging utility
```

## Application Bootstrap (`index.js`)

| Step | Description |
|------|-------------|
| 1 | Import Express, CORS, config, routes, middleware, logger |
| 2 | Create Express app |
| 3 | Mount CORS middleware (permissive, no origin restriction) |
| 4 | Mount `express.json()` with 10 KB body limit |
| 5 | Mount request logger (skips `GET /api/health` to reduce noise) |
| 6 | Mount `/api` router (aggregates query + health routes) |
| 7 | Mount `notFoundHandler` for unmatched routes |
| 8 | Mount `errorHandler` as final error-catching middleware |
| 9 | Start listening on configured PORT (skipped in test environment) |
| 10 | Register SIGTERM handler for graceful shutdown |

### Middleware Stack (execution order)

```
cors() -> express.json({ limit: '10kb' }) -> requestLogger -> apiRouter -> notFoundHandler -> errorHandler
```

### Graceful Shutdown

When `SIGTERM` is received, the server stops accepting new connections, finishes in-flight requests, logs closure, and exits with code 0. The server instance is only created when `NODE_ENV !== 'test'`, allowing the app to be imported for testing without binding a port.

```js
process.on('SIGTERM', () => {
  server.close(() => {
    process.exit(0);
  });
});
```

## Request Flow

```
Client
  |
  v
POST /api/query { query: "..." }
  |
  v
[CORS] -> [JSON Parser] -> [Request Logger]
  |
  v
routes/query.js
  ├── Validate: non-empty string, max 1000 chars
  └── Call processQuery() from services/pipeline.js
        |
        ├── Stage 1: retrieveChunks() -> Python subprocess -> ChromaDB
        ├── Stage 2: formatContext()   -> Build LLM context string
        ├── Stage 3: generateResponse() -> Groq API (Llama 3.1 8B)
        └── Stage 4: processCitations() -> Extract, match, enrich citations
  |
  v
JSON Response {
  answer, sources, relatedDocs, citations, confidence, metadata
}
```

## Database Connections

The backend has **no direct database connections**. ChromaDB is accessed exclusively through a Python subprocess bridge (`scripts/query_chroma.py`). The Node.js process spawns a Python child process for each query, passing parameters via JSON on stdin and reading results from stdout. This design avoids the need for a running ChromaDB server instance, since the Python client can access the persistent local storage directly.

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Python subprocess bridge | ChromaDB JS client requires a running server; Python client works directly with local storage |
| Singleton LLM client | Avoids re-initializing the OpenAI client on every request |
| System prompt from file | Allows prompt iteration without code changes; cached after first load |
| No authentication | POC scope; no user-facing deployment |
| Test isolation via `NODE_ENV` | Server binding skipped in test mode; services export `reset*()` functions for test cleanup |

## Dependencies

| Package | Purpose |
|---------|---------|
| `express` | HTTP server framework |
| `cors` | Cross-Origin Resource Sharing |
| `dotenv` | Environment variable loading from `.env` |
| `openai` | OpenAI-compatible client (used for Groq API) |

## Exported Module

`index.js` exports the Express `app` instance as the default export, enabling test frameworks to make requests against the application without starting a server.

```js
export default app;
```
