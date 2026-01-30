# Task 6.2: Create Express API

## Persona

> You are a backend developer with expertise in Express.js APIs and RESTful design.
> You follow TDD principles and create robust, well-documented APIs.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. The pipeline orchestrator is complete (Task 6.1). Now we need to expose it via an Express API that the frontend can call.

### Current State
- Pipeline orchestrator: `src/services/pipeline.js` - `processQuery()`
- Express app placeholder: `src/index.js` - basic server with health check
- Routes placeholder: `src/routes/query.js` - throws "Not implemented"
- Server runs on port 3000

### Reference Documents
- `03_rag_pipeline/docs/00_week2_rag_pipeline_plan.md` - API specifications
- `03_rag_pipeline/docs/01_implementation_roadmap.md` - Task specifications
- `03_rag_pipeline/src/index.js` - Current Express setup

### Dependencies
- Task 6.1: Create Pipeline Orchestrator ✅

---

## Task

### Objective
Implement the Express API endpoints that expose the RAG pipeline to clients, with proper error handling, request validation, and CORS support.

### Requirements

1. **Implement POST /api/query endpoint**
   - Accept JSON body with `query` field
   - Call `processQuery()` from pipeline service
   - Return structured response
   - Validate request body

2. **Implement GET /api/health endpoint**
   - Return server status
   - Include uptime and timestamp
   - Check ChromaDB connectivity (optional)

3. **Implement GET /api/stats endpoint (optional)**
   - Return basic usage statistics
   - Query count, average latency, etc.

4. **Add error handling middleware**
   - Catch and format all errors consistently
   - Log errors with context
   - Return appropriate HTTP status codes

5. **Add request validation**
   - Validate query is non-empty string
   - Validate request content type
   - Return 400 for invalid requests

6. **Write API integration tests**
   - Test happy path
   - Test error cases
   - Test validation
   - Use supertest for HTTP testing

### Specifications

**src/routes/query.js**:
```javascript
/**
 * Query endpoint routes
 * Handles POST /api/query for RAG pipeline queries.
 */

import { Router } from 'express';
import { processQuery } from '../services/pipeline.js';
import { logger } from '../utils/logger.js';

const router = Router();

/**
 * POST /api/query
 * Process a customer service query through the RAG pipeline.
 *
 * @body {string} query - The customer query text
 * @returns {Object} Response with answer, citations, confidence, metadata
 */
router.post('/', async (req, res, next) => {
  const startTime = Date.now();

  try {
    const { query } = req.body;

    // Validate request
    if (!query || typeof query !== 'string') {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'Query parameter is required and must be a string',
      });
    }

    if (query.trim().length === 0) {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'Query cannot be empty',
      });
    }

    if (query.length > 1000) {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'Query exceeds maximum length of 1000 characters',
      });
    }

    // Process query through pipeline
    const result = await processQuery(query);

    // Log successful request
    logger.info('Query processed via API', {
      queryLength: query.length,
      confidence: result.confidence.level,
      latencyMs: Date.now() - startTime,
    });

    res.json(result);

  } catch (error) {
    next(error);
  }
});

export default router;
```

**src/routes/health.js**:
```javascript
/**
 * Health check endpoint
 */

import { Router } from 'express';

const router = Router();
const startTime = Date.now();

/**
 * GET /api/health
 * Returns server health status.
 */
router.get('/', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: Math.floor((Date.now() - startTime) / 1000),
    version: process.env.npm_package_version || '1.0.0',
  });
});

export default router;
```

**src/routes/index.js**:
```javascript
/**
 * Route aggregator
 * Exports all API routes for the application.
 */

import { Router } from 'express';
import queryRoutes from './query.js';
import healthRoutes from './health.js';

const router = Router();

// Mount routes
router.use('/query', queryRoutes);
router.use('/health', healthRoutes);

export { router as apiRouter };
```

**src/middleware/errorHandler.js**:
```javascript
/**
 * Global error handling middleware
 */

import { logger } from '../utils/logger.js';

/**
 * Error handler middleware
 * Catches all errors and returns consistent JSON responses.
 */
export function errorHandler(err, req, res, next) {
  // Log the error
  logger.error('API error', {
    path: req.path,
    method: req.method,
    error: err.message,
    stack: process.env.NODE_ENV === 'development' ? err.stack : undefined,
  });

  // Determine status code
  const statusCode = err.statusCode || err.status || 500;

  // Send error response
  res.status(statusCode).json({
    error: statusCode >= 500 ? 'Internal Server Error' : 'Request Error',
    message: err.message || 'An unexpected error occurred',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  });
}

/**
 * Not found handler
 * Returns 404 for unmatched routes.
 */
export function notFoundHandler(req, res) {
  res.status(404).json({
    error: 'Not Found',
    message: `Route ${req.method} ${req.path} not found`,
  });
}
```

**src/index.js** (updated):
```javascript
/**
 * Waypoint RAG Pipeline API
 *
 * Express server that provides the /api/query endpoint
 * for the customer service co-pilot.
 */

import express from 'express';
import cors from 'cors';
import { config } from './config.js';
import { apiRouter } from './routes/index.js';
import { errorHandler, notFoundHandler } from './middleware/errorHandler.js';
import { logger } from './utils/logger.js';

const app = express();

// Middleware
app.use(cors());
app.use(express.json({ limit: '10kb' }));

// Request logging (optional)
app.use((req, res, next) => {
  if (req.path !== '/api/health') {
    logger.debug('Incoming request', {
      method: req.method,
      path: req.path,
    });
  }
  next();
});

// Routes
app.use('/api', apiRouter);

// Error handling
app.use(notFoundHandler);
app.use(errorHandler);

// Start server
const PORT = config.port;

const server = app.listen(PORT, () => {
  logger.info('Server started', {
    port: PORT,
    env: config.nodeEnv,
  });
});

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');
  server.close(() => {
    logger.info('Server closed');
    process.exit(0);
  });
});

export default app;
```

**tests/api.test.js**:
```javascript
/**
 * API Integration Tests
 */

import { jest } from '@jest/globals';
import request from 'supertest';

// Mock the pipeline service
jest.unstable_mockModule('../src/services/pipeline.js', () => ({
  processQuery: jest.fn(),
}));

const { default: app } = await import('../src/index.js');
const { processQuery } = await import('../src/services/pipeline.js');

describe('API Endpoints', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('GET /api/health', () => {
    test('returns health status', async () => {
      const response = await request(app)
        .get('/api/health')
        .expect(200);

      expect(response.body.status).toBe('ok');
      expect(response.body.timestamp).toBeDefined();
      expect(response.body.uptime).toBeGreaterThanOrEqual(0);
    });
  });

  describe('POST /api/query', () => {
    const mockResult = {
      answer: 'Test answer',
      citations: [],
      sourcesMarkdown: '',
      confidence: { level: 'Medium', reason: 'Test' },
      metadata: { chunksRetrieved: 2 },
    };

    beforeEach(() => {
      processQuery.mockResolvedValue(mockResult);
    });

    test('processes valid query', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: 'What documents for export?' })
        .expect(200);

      expect(response.body.answer).toBe('Test answer');
      expect(processQuery).toHaveBeenCalledWith('What documents for export?');
    });

    test('returns 400 for missing query', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({})
        .expect(400);

      expect(response.body.error).toBe('Bad Request');
      expect(response.body.message).toContain('required');
    });

    test('returns 400 for empty query', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: '' })
        .expect(400);

      expect(response.body.error).toBe('Bad Request');
      expect(response.body.message).toContain('empty');
    });

    test('returns 400 for whitespace-only query', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: '   ' })
        .expect(400);

      expect(response.body.error).toBe('Bad Request');
    });

    test('returns 400 for non-string query', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: 123 })
        .expect(400);

      expect(response.body.error).toBe('Bad Request');
    });

    test('returns 400 for query exceeding max length', async () => {
      const longQuery = 'a'.repeat(1001);
      const response = await request(app)
        .post('/api/query')
        .send({ query: longQuery })
        .expect(400);

      expect(response.body.message).toContain('maximum length');
    });

    test('handles pipeline errors gracefully', async () => {
      processQuery.mockRejectedValue(new Error('Pipeline failed'));

      const response = await request(app)
        .post('/api/query')
        .send({ query: 'Test query' })
        .expect(500);

      expect(response.body.error).toBe('Internal Server Error');
    });

    test('sets correct content-type', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: 'Test' })
        .expect(200);

      expect(response.headers['content-type']).toMatch(/json/);
    });
  });

  describe('404 handling', () => {
    test('returns 404 for unknown routes', async () => {
      const response = await request(app)
        .get('/api/unknown')
        .expect(404);

      expect(response.body.error).toBe('Not Found');
    });
  });

  describe('CORS', () => {
    test('allows cross-origin requests', async () => {
      const response = await request(app)
        .options('/api/query')
        .set('Origin', 'http://localhost:5173')
        .expect(204);

      expect(response.headers['access-control-allow-origin']).toBeDefined();
    });
  });
});
```

### Constraints
- Use ES modules (import/export)
- Keep JSON body size limit at 10kb
- Return consistent error format
- Log all requests and errors
- Support CORS for browser clients

### Acceptance Criteria
- [ ] POST /api/query endpoint implemented
- [ ] GET /api/health endpoint returns status
- [ ] Request validation for query field
- [ ] Error handling middleware catches all errors
- [ ] 404 handler for unknown routes
- [ ] All tests pass: `npm test -- --testPathPattern=api`
- [ ] Manual test with curl works

### TDD Requirements
- [ ] Write tests first with supertest
- [ ] Implement endpoints to pass tests
- [ ] Run `npm test` to verify all pass

---

## Format

### Output Structure
- `src/routes/query.js` - Query endpoint
- `src/routes/health.js` - Health endpoint
- `src/routes/index.js` - Route aggregator
- `src/middleware/errorHandler.js` - Error handling
- `src/index.js` - Updated Express app
- `tests/api.test.js` - API tests

### API Response Format

**Success (POST /api/query)**:
```json
{
  "answer": "For Singapore export...",
  "citations": [...],
  "sourcesMarkdown": "**Sources:**\n...",
  "confidence": {
    "level": "High",
    "reason": "3 sources found"
  },
  "metadata": {
    "query": "...",
    "chunksRetrieved": 5,
    "latency": {...}
  }
}
```

**Error**:
```json
{
  "error": "Bad Request",
  "message": "Query parameter is required"
}
```

**Health**:
```json
{
  "status": "ok",
  "timestamp": "2026-01-30T12:00:00.000Z",
  "uptime": 3600,
  "version": "1.0.0"
}
```

### Validation Commands

```bash
cd pilot_phase1_poc/03_rag_pipeline

# Run API tests only
npm test -- --testPathPattern=api

# Run all tests
npm test

# Manual test with curl
npm start &
sleep 2

# Health check
curl http://localhost:3000/api/health

# Query test
curl -X POST http://localhost:3000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What documents for Singapore export?"}'

# Error test
curl -X POST http://localhost:3000/api/query \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Expected Test Output
```
PASS tests/api.test.js
  API Endpoints
    GET /api/health
      ✓ returns health status
    POST /api/query
      ✓ processes valid query
      ✓ returns 400 for missing query
      ✓ returns 400 for empty query
      ✓ returns 400 for whitespace-only query
      ✓ returns 400 for non-string query
      ✓ returns 400 for query exceeding max length
      ✓ handles pipeline errors gracefully
      ✓ sets correct content-type
    404 handling
      ✓ returns 404 for unknown routes
    CORS
      ✓ allows cross-origin requests

Test Suites: 1 passed, 1 total
Tests:       11 passed, 11 total
```
