/**
 * Pipeline Orchestrator Tests
 */

import { jest } from '@jest/globals';

// Mock all dependent services
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
}));

const { processQuery, calculateConfidence } = await import('../backend/services/pipeline.js');
const { retrieveChunks, formatContext } = await import('../backend/services/retrieval.js');
const { generateResponse } = await import('../backend/services/llm.js');
const { processCitations } = await import('../backend/services/citations.js');

describe('Pipeline Orchestrator', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('processQuery', () => {
    const mockChunks = [
      { content: 'Export docs info', metadata: { title: 'Export Guide' }, score: 0.85 },
      { content: 'More export info', metadata: { title: 'Customs Guide' }, score: 0.75 },
    ];

    const mockLLMResult = {
      answer: 'You need [Export Guide] documents.',
      model: 'llama-3.1-8b-instant',
      usage: { promptTokens: 100, completionTokens: 50 },
    };

    const mockCitationResult = {
      citations: [{ title: 'Export Guide', matched: true }],
      markdown: '**Sources:**\n1. Export Guide',
      stats: { total: 1, matched: 1, unmatched: 0 },
    };

    beforeEach(() => {
      retrieveChunks.mockResolvedValue(mockChunks);
      formatContext.mockReturnValue('Formatted context');
      generateResponse.mockResolvedValue(mockLLMResult);
      processCitations.mockReturnValue(mockCitationResult);
    });

    test('processes query through full pipeline', async () => {
      const result = await processQuery('What documents for export?');

      expect(retrieveChunks).toHaveBeenCalledWith('What documents for export?', expect.any(Object));
      expect(formatContext).toHaveBeenCalledWith(mockChunks);
      expect(generateResponse).toHaveBeenCalled();
      expect(processCitations).toHaveBeenCalled();

      expect(result.answer).toBe(mockLLMResult.answer);
      expect(result.citations).toHaveLength(1);
      expect(result.metadata.chunksRetrieved).toBe(2);
    });

    test('returns structured response with all fields', async () => {
      const result = await processQuery('Test query');

      expect(result).toHaveProperty('answer');
      expect(result).toHaveProperty('citations');
      expect(result).toHaveProperty('sourcesMarkdown');
      expect(result).toHaveProperty('confidence');
      expect(result).toHaveProperty('metadata');
      expect(result.metadata).toHaveProperty('latency');
    });

    test('handles no chunks found', async () => {
      retrieveChunks.mockResolvedValue([]);

      const result = await processQuery('Unknown topic query');

      expect(result.confidence.level).toBe('Low');
      expect(result.citations).toHaveLength(0);
      expect(generateResponse).not.toHaveBeenCalled();
    });

    test('throws on empty query', async () => {
      await expect(processQuery('')).rejects.toThrow('Query must be a non-empty string');
      await expect(processQuery('   ')).rejects.toThrow('Query must be a non-empty string');
    });

    test('throws on invalid query type', async () => {
      await expect(processQuery(null)).rejects.toThrow();
      await expect(processQuery(123)).rejects.toThrow();
    });

    test('includes latency metrics', async () => {
      const result = await processQuery('Test query');

      expect(result.metadata.latency).toHaveProperty('retrievalMs');
      expect(result.metadata.latency).toHaveProperty('generationMs');
      expect(result.metadata.latency).toHaveProperty('totalMs');
      expect(result.metadata.latency.totalMs).toBeGreaterThanOrEqual(0);
    });

    test('propagates retrieval errors', async () => {
      retrieveChunks.mockRejectedValue(new Error('ChromaDB unavailable'));

      await expect(processQuery('Test')).rejects.toThrow('Pipeline error: ChromaDB unavailable');
    });

    test('propagates LLM errors', async () => {
      generateResponse.mockRejectedValue(new Error('Groq API error'));

      await expect(processQuery('Test')).rejects.toThrow('Pipeline error: Groq API error');
    });

    test('passes options to retrieveChunks', async () => {
      await processQuery('Test', { topK: 5, threshold: 0.2 });

      expect(retrieveChunks).toHaveBeenCalledWith('Test', {
        topK: 5,
        threshold: 0.2,
      });
    });

    test('uses default config when no options provided', async () => {
      await processQuery('Test');

      expect(retrieveChunks).toHaveBeenCalledWith('Test', {
        topK: expect.any(Number),
        threshold: expect.any(Number),
      });
    });

    test('filters citations to only matched ones', async () => {
      const mixedCitationResult = {
        citations: [
          { title: 'Matched Doc', matched: true },
          { title: 'Unmatched Doc', matched: false },
        ],
        markdown: '**Sources:**',
        stats: { total: 2, matched: 1, unmatched: 1 },
      };
      processCitations.mockReturnValue(mixedCitationResult);

      const result = await processQuery('Test');

      expect(result.citations).toHaveLength(1);
      expect(result.citations[0].matched).toBe(true);
    });

    test('trims whitespace from query', async () => {
      await processQuery('  Test query  ');

      expect(retrieveChunks).toHaveBeenCalledWith('Test query', expect.any(Object));
    });
  });

  describe('calculateConfidence', () => {
    test('returns High for many good chunks with citations', () => {
      const chunks = [
        { score: 0.9 },
        { score: 0.8 },
        { score: 0.75 },
      ];
      const citationResult = { stats: { matched: 3 } };

      const confidence = calculateConfidence(chunks, citationResult);

      expect(confidence.level).toBe('High');
      expect(confidence.reason).toContain('3 relevant sources');
    });

    test('returns Medium for decent results', () => {
      const chunks = [
        { score: 0.6 },
        { score: 0.5 },
      ];
      const citationResult = { stats: { matched: 1 } };

      const confidence = calculateConfidence(chunks, citationResult);

      expect(confidence.level).toBe('Medium');
      expect(confidence.reason).toContain('sources found');
    });

    test('returns Low for poor results', () => {
      const chunks = [{ score: 0.3 }];
      const citationResult = { stats: { matched: 0 } };

      const confidence = calculateConfidence(chunks, citationResult);

      expect(confidence.level).toBe('Low');
    });

    test('returns Low for single source', () => {
      const chunks = [{ score: 0.9 }];
      const citationResult = { stats: { matched: 1 } };

      const confidence = calculateConfidence(chunks, citationResult);

      expect(confidence.level).toBe('Low');
      expect(confidence.reason).toContain('Only 1 source');
    });

    test('includes reason in confidence', () => {
      const chunks = [{ score: 0.9 }];
      const citationResult = { stats: { matched: 1 } };

      const confidence = calculateConfidence(chunks, citationResult);

      expect(confidence.reason).toBeDefined();
      expect(typeof confidence.reason).toBe('string');
    });

    test('calculates average score correctly', () => {
      const chunks = [
        { score: 0.6 },
        { score: 0.55 },
        { score: 0.5 },
      ];
      const citationResult = { stats: { matched: 1 } };

      const confidence = calculateConfidence(chunks, citationResult);
      const avgScore = (0.6 + 0.55 + 0.5) / 3;

      expect(confidence.level).toBe('Medium');
      expect(confidence.reason).toContain(`${(avgScore * 100).toFixed(0)}%`);
    });

    test('handles low average score case', () => {
      const chunks = [
        { score: 0.4 },
        { score: 0.35 },
      ];
      const citationResult = { stats: { matched: 1 } };

      const confidence = calculateConfidence(chunks, citationResult);

      expect(confidence.level).toBe('Low');
      expect(confidence.reason).toContain('Low relevance scores');
    });
  });
});
