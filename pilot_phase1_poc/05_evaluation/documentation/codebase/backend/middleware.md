# Middleware Documentation

## Purpose

The `backend/middleware/` directory contains the global error handling middleware for the Express application. It provides two handlers: a catch-all error handler for exceptions thrown during request processing, and a 404 handler for unmatched routes. Both return consistent JSON error responses.

## File Index

| File | Purpose |
|------|---------|
| `middleware/errorHandler.js` | Exports `errorHandler` and `notFoundHandler` |

---

## Error Handler (`errorHandler`)

Catches all errors thrown or passed via `next(error)` during request processing. This is the final middleware in the Express stack.

### Signature

```js
function errorHandler(err, req, res, next)
```

### Behavior

**1. Logging:**

Logs every error with structured context via the logger:

```js
logger.error('API error', {
  path: req.path,
  method: req.method,
  error: err.message,
  stack: process.env.NODE_ENV === 'development' ? err.stack : undefined,
});
```

The stack trace is only included in log output when `NODE_ENV` is `development`.

**2. Status Code Resolution:**

The handler checks for a status code on the error object using this priority:

| Priority | Property | Description |
|----------|----------|-------------|
| 1 | `err.statusCode` | Custom status code (e.g., set by services) |
| 2 | `err.status` | Alternative property (used by some libraries) |
| 3 | `500` | Default fallback for unhandled errors |

**3. Response Format:**

```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "stack": "(development only)"
}
```

| Field | Condition | Value |
|-------|-----------|-------|
| `error` | `statusCode >= 500` | `"Internal Server Error"` |
| `error` | `statusCode < 500` | `"Request Error"` |
| `message` | Always | `err.message` or `"An unexpected error occurred"` |
| `stack` | `NODE_ENV === 'development'` only | Full stack trace string |

The `stack` field is completely omitted (not set to `null` or empty) in non-development environments, using object spread with a conditional:

```js
...(process.env.NODE_ENV === 'development' && { stack: err.stack })
```

### Error Sources

Errors reach this handler from:

| Source | How |
|--------|-----|
| Route handlers | Via `next(error)` in catch blocks |
| Pipeline service | Thrown errors from `processQuery()` |
| LLM service | API errors after retry exhaustion |
| Retrieval service | Python subprocess failures |
| Express built-in | JSON parse errors (malformed body) |

---

## Not Found Handler (`notFoundHandler`)

Catches requests to routes that do not match any defined endpoint. Mounted after all route definitions but before the error handler.

### Signature

```js
function notFoundHandler(req, res)
```

### Response

**Status:** `404`

```json
{
  "error": "Not Found",
  "message": "Route GET /api/nonexistent not found"
}
```

| Field | Value |
|-------|-------|
| `error` | `"Not Found"` (always) |
| `message` | `"Route {METHOD} {path} not found"` (dynamic) |

The message includes the HTTP method and request path, making it clear which route was attempted.

---

## Middleware Stack Position

The handlers are mounted in a specific order in `backend/index.js`:

```
app.use(cors());                    // 1. CORS
app.use(express.json(...));         // 2. Body parser
app.use(requestLogger);             // 3. Request logging
app.use('/api', apiRouter);         // 4. Routes
app.use(notFoundHandler);           // 5. 404 catch-all  <--
app.use(errorHandler);              // 6. Error catch-all <--
```

**Key ordering rules:**
- `notFoundHandler` must come after all route definitions so it only catches truly unmatched routes
- `errorHandler` must be last because Express identifies error-handling middleware by its 4-parameter signature `(err, req, res, next)`
- Both handlers are mounted at the app level (not under `/api`), so they catch errors from any path

---

## Dependencies

| Module | Import | Purpose |
|--------|--------|---------|
| `utils/logger.js` | `logger` | Structured error logging |
