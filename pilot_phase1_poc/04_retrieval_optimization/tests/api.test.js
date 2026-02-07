/**
 * API Integration Tests
 */

import { jest } from '@jest/globals';
import request from 'supertest';

// Mock the pipeline service
jest.unstable_mockModule('../backend/services/pipeline.js', () => ({
  processQuery: jest.fn(),
  calculateConfidence: jest.fn(),
}));

const { default: app } = await import('../backend/index.js');
const { processQuery } = await import('../backend/services/pipeline.js');

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
      expect(response.body.message).toContain('required');
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
