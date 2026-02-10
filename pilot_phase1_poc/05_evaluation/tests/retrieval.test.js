/**
 * Retrieval Service Tests
 *
 * Tests for filtering and formatting functions.
 * Integration tests use the Python bridge (skipped in CI).
 */

import { filterByThreshold, formatContext, getMetadataForCitation, initChromaClient } from '../backend/services/retrieval.js';

describe('Retrieval Service', () => {
  describe('initChromaClient', () => {
    test('returns true (bridge ready)', async () => {
      const result = await initChromaClient();
      expect(result).toBe(true);
    });
  });

  describe('filterByThreshold', () => {
    const testChunks = [
      { score: 0.9, content: 'high relevance' },
      { score: 0.5, content: 'medium relevance' },
      { score: 0.1, content: 'low relevance' },
    ];

    test('filters chunks below threshold', () => {
      const filtered = filterByThreshold(testChunks, 0.5);
      expect(filtered.length).toBe(2);
      expect(filtered.every(c => c.score >= 0.5)).toBe(true);
    });

    test('returns empty array when all below threshold', () => {
      const filtered = filterByThreshold(testChunks, 0.95);
      expect(filtered.length).toBe(0);
    });

    test('returns all chunks when threshold is 0', () => {
      const filtered = filterByThreshold(testChunks, 0);
      expect(filtered.length).toBe(3);
    });

    test('handles empty array', () => {
      const filtered = filterByThreshold([], 0.5);
      expect(filtered.length).toBe(0);
    });
  });

  describe('formatContext', () => {
    const testChunks = [
      { content: 'Content about exports', metadata: { title: 'Export Guide', section: 'Documents' } },
      { content: 'Content about customs', metadata: { title: 'Customs Overview' } },
    ];

    test('formats chunks with title and section', () => {
      const context = formatContext(testChunks);
      expect(context).toContain('[Export Guide > Documents]');
      expect(context).toContain('Content about exports');
    });

    test('handles missing section', () => {
      const context = formatContext(testChunks);
      expect(context).toContain('[Customs Overview]');
      expect(context).not.toContain('[Customs Overview >');
    });

    test('separates chunks with newlines', () => {
      const context = formatContext(testChunks);
      expect(context).toContain('\n\n');
    });

    test('respects max character limit', () => {
      const longChunks = [
        { content: 'A'.repeat(500), metadata: { title: 'Doc 1' } },
        { content: 'B'.repeat(500), metadata: { title: 'Doc 2' } },
        { content: 'C'.repeat(500), metadata: { title: 'Doc 3' } },
      ];
      const context = formatContext(longChunks, 600);
      // Should only include first chunk due to limit
      expect(context.length).toBeLessThan(700);
    });

    test('handles missing metadata', () => {
      const chunks = [{ content: 'Some content', metadata: {} }];
      const context = formatContext(chunks);
      expect(context).toContain('[Unknown Document]');
      expect(context).toContain('Some content');
    });

    test('handles null metadata', () => {
      const chunks = [{ content: 'Some content' }];
      const context = formatContext(chunks);
      expect(context).toContain('[Unknown Document]');
    });
  });

  describe('getMetadataForCitation', () => {
    test('extracts citation metadata', () => {
      const chunks = [{
        metadata: {
          title: 'Test Document',
          section: 'Test Section',
          source_urls: 'https://example.com,https://example2.com',
          doc_id: 'test_doc',
        },
        score: 0.85,
      }];

      const citations = getMetadataForCitation(chunks);

      expect(citations.length).toBe(1);
      expect(citations[0].title).toBe('Test Document');
      expect(citations[0].section).toBe('Test Section');
      expect(citations[0].sourceUrls).toEqual(['https://example.com', 'https://example2.com']);
      expect(citations[0].docId).toBe('test_doc');
      expect(citations[0].score).toBe(0.85);
    });

    test('handles missing source_urls', () => {
      const chunks = [{
        metadata: { title: 'Doc', doc_id: 'doc1' },
        score: 0.9,
      }];

      const citations = getMetadataForCitation(chunks);
      expect(citations[0].sourceUrls).toEqual([]);
    });

    test('handles missing metadata fields', () => {
      const chunks = [{
        metadata: {},
        score: 0.9,
      }];

      const citations = getMetadataForCitation(chunks);
      expect(citations[0].title).toBe('Unknown');
      expect(citations[0].section).toBeNull();
      expect(citations[0].docId).toBeNull();
    });

    test('handles multiple chunks', () => {
      const chunks = [
        { metadata: { title: 'Doc 1', doc_id: 'd1' }, score: 0.9 },
        { metadata: { title: 'Doc 2', doc_id: 'd2' }, score: 0.8 },
      ];

      const citations = getMetadataForCitation(chunks);
      expect(citations.length).toBe(2);
      expect(citations[0].title).toBe('Doc 1');
      expect(citations[1].title).toBe('Doc 2');
    });

    test('handles empty array', () => {
      const citations = getMetadataForCitation([]);
      expect(citations.length).toBe(0);
    });
  });
});
