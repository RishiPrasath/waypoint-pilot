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
      sources: [],
      relatedDocs: [],
      citations: [],
      confidence: { level: 'Medium', reason: 'Test' },
      metadata: { chunksRetrieved: 2, chunksUsed: 0, latencyMs: 150, model: 'llama-3.1-8b-instant' },
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

  describe('Response shape validation', () => {
    const richMockResult = {
      answer: 'For Singapore exports, you need a trade declaration [Export Guide > Documents].',
      sources: [
        { title: 'Export Guide', org: 'Singapore Customs', url: 'https://customs.gov.sg/export', section: 'Documents' },
        { title: 'Trade Procedures', org: 'Singapore Customs', url: 'https://customs.gov.sg/trade', section: null },
      ],
      relatedDocs: [
        { title: 'Export Guide', category: 'regulatory', docId: 'sg_export_guide', url: 'https://customs.gov.sg/export' },
        { title: 'Booking SOP', category: 'internal', docId: 'booking_sop', url: null },
      ],
      citations: [
        { raw: '[Export Guide > Documents]', title: 'Export Guide', section: 'Documents', position: 55, matched: true, sourceUrls: ['https://customs.gov.sg/export'], docId: 'sg_export_guide', score: 0.85, fullTitle: 'Export Guide' },
      ],
      confidence: { level: 'High', reason: '3 relevant sources with 2 citations' },
      metadata: { query: 'What documents for export?', chunksRetrieved: 3, chunksUsed: 2, latencyMs: 250, model: 'llama-3.1-8b-instant' },
    };

    beforeEach(() => {
      processQuery.mockResolvedValue(richMockResult);
    });

    test('response contains all 6 top-level keys', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: 'What documents for export?' })
        .expect(200);

      expect(response.body).toHaveProperty('answer');
      expect(response.body).toHaveProperty('sources');
      expect(response.body).toHaveProperty('relatedDocs');
      expect(response.body).toHaveProperty('citations');
      expect(response.body).toHaveProperty('confidence');
      expect(response.body).toHaveProperty('metadata');
    });

    test('sources items have correct shape', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: 'Export docs' })
        .expect(200);

      expect(response.body.sources).toHaveLength(2);
      for (const source of response.body.sources) {
        expect(typeof source.title).toBe('string');
        expect(typeof source.org).toBe('string');
        expect(typeof source.url).toBe('string');
        expect(source.url).toMatch(/^https?:\/\//);
        expect(source.section === null || typeof source.section === 'string').toBe(true);
      }
    });

    test('relatedDocs items have correct shape', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: 'Export docs' })
        .expect(200);

      expect(response.body.relatedDocs).toHaveLength(2);
      for (const doc of response.body.relatedDocs) {
        expect(typeof doc.title).toBe('string');
        expect(typeof doc.category).toBe('string');
        expect(typeof doc.docId).toBe('string');
        expect(doc.url === null || typeof doc.url === 'string').toBe(true);
      }
    });

    test('confidence.level is a valid enum value', async () => {
      const validLevels = ['High', 'Medium', 'Low'];

      const response = await request(app)
        .post('/api/query')
        .send({ query: 'Export docs' })
        .expect(200);

      expect(validLevels).toContain(response.body.confidence.level);
    });

    test('confidence.reason is a non-empty string', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: 'Export docs' })
        .expect(200);

      expect(typeof response.body.confidence.reason).toBe('string');
      expect(response.body.confidence.reason.length).toBeGreaterThan(0);
    });

    test('metadata contains all required fields with correct types', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: 'Export docs' })
        .expect(200);

      const { metadata } = response.body;
      expect(typeof metadata.query).toBe('string');
      expect(typeof metadata.chunksRetrieved).toBe('number');
      expect(typeof metadata.chunksUsed).toBe('number');
      expect(typeof metadata.latencyMs).toBe('number');
      expect(typeof metadata.model).toBe('string');
    });

    test('citations only contains matched items', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: 'Export docs' })
        .expect(200);

      expect(response.body.citations.length).toBeGreaterThan(0);
      for (const citation of response.body.citations) {
        expect(citation.matched).toBe(true);
        expect(typeof citation.title).toBe('string');
        expect(typeof citation.raw).toBe('string');
        expect(typeof citation.position).toBe('number');
      }
    });
  });

  describe('Error and edge cases', () => {
    const mockResult = {
      answer: 'Test answer',
      sources: [],
      relatedDocs: [],
      citations: [],
      confidence: { level: 'Medium', reason: 'Test' },
      metadata: { chunksRetrieved: 2, chunksUsed: 0, latencyMs: 150, model: 'llama-3.1-8b-instant' },
    };

    beforeEach(() => {
      processQuery.mockResolvedValue(mockResult);
    });

    test('rejects very long query (10,000 chars) with 400', async () => {
      const longQuery = 'a'.repeat(10000);
      const response = await request(app)
        .post('/api/query')
        .send({ query: longQuery })
        .expect(400);

      expect(response.body.error).toBe('Bad Request');
      expect(response.body.message).toContain('maximum length');
    });

    test('rejects malformed JSON body with 400', async () => {
      const response = await request(app)
        .post('/api/query')
        .set('Content-Type', 'application/json')
        .send('{ invalid json }')
        .expect(400);

      expect(response.body).toBeDefined();
    });

    test('rejects body sent as plain text', async () => {
      const response = await request(app)
        .post('/api/query')
        .set('Content-Type', 'text/plain')
        .send('What documents for export?');

      // Express won't parse text/plain as JSON, so req.body is undefined → query is missing
      expect(response.status).toBe(400);
      expect(response.body.error).toBe('Bad Request');
    });

    test('returns 500 for Groq API timeout through endpoint', async () => {
      processQuery.mockRejectedValue(new Error('Pipeline error: LLM request failed: Request timed out'));

      const response = await request(app)
        .post('/api/query')
        .send({ query: 'What is GST rate?' })
        .expect(500);

      expect(response.body.error).toBe('Internal Server Error');
      expect(response.body.message).toContain('timed out');
    });

    test('returns 500 for ChromaDB connection failure through endpoint', async () => {
      processQuery.mockRejectedValue(new Error('Pipeline error: Retrieval failed: ChromaDB connection refused'));

      const response = await request(app)
        .post('/api/query')
        .send({ query: 'What is GST rate?' })
        .expect(500);

      expect(response.body.error).toBe('Internal Server Error');
      expect(response.body.message).toContain('ChromaDB');
    });

    test('rejects array as query value with 400', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: ['what', 'is', 'gst'] })
        .expect(400);

      expect(response.body.error).toBe('Bad Request');
    });

    test('rejects object as query value with 400', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: { text: 'what is gst' } })
        .expect(400);

      expect(response.body.error).toBe('Bad Request');
    });

    test('handles query with special characters safely', async () => {
      const response = await request(app)
        .post('/api/query')
        .send({ query: 'What is <script>alert("xss")</script> & SELECT * FROM users?' })
        .expect(200);

      expect(response.body.answer).toBeDefined();
      expect(processQuery).toHaveBeenCalled();
    });
  });
});
