/**
 * Citation Extractor Tests
 */

import {
  extractCitations,
  matchCitationToChunk,
  similarity,
  enrichCitations,
  formatCitationsMarkdown,
  deduplicateCitations,
  processCitations,
} from '../backend/services/citations.js';

describe('Citation Extractor', () => {
  describe('extractCitations', () => {
    test('extracts simple citation', () => {
      const text = 'According to [Singapore Export Guide], you need...';
      const citations = extractCitations(text);

      expect(citations).toHaveLength(1);
      expect(citations[0].title).toBe('Singapore Export Guide');
      expect(citations[0].section).toBeNull();
    });

    test('extracts citation with section', () => {
      const text = 'As stated in [Export Guide > Documents]...';
      const citations = extractCitations(text);

      expect(citations).toHaveLength(1);
      expect(citations[0].title).toBe('Export Guide');
      expect(citations[0].section).toBe('Documents');
    });

    test('extracts multiple citations', () => {
      const text = '[Doc A] and [Doc B > Section] are relevant.';
      const citations = extractCitations(text);

      expect(citations).toHaveLength(2);
    });

    test('returns empty array for no citations', () => {
      const text = 'No citations here.';
      const citations = extractCitations(text);

      expect(citations).toHaveLength(0);
    });

    test('captures position of citation', () => {
      const text = 'See [Document] for details.';
      const citations = extractCitations(text);

      expect(citations[0].position).toBe(4);
    });

    test('captures raw citation text', () => {
      const text = 'According to [Test Doc > Section]...';
      const citations = extractCitations(text);

      expect(citations[0].raw).toBe('[Test Doc > Section]');
    });

    test('handles citations at start of text', () => {
      const text = '[Doc Title] is important.';
      const citations = extractCitations(text);

      expect(citations).toHaveLength(1);
      expect(citations[0].position).toBe(0);
    });
  });

  describe('similarity', () => {
    test('returns 1 for identical strings', () => {
      expect(similarity('hello', 'hello')).toBe(1);
    });

    test('returns 0 for completely different strings', () => {
      expect(similarity('abc', 'xyz')).toBe(0);
    });

    test('returns partial match for similar strings', () => {
      const score = similarity('Singapore Export', 'Singapore Exports');
      expect(score).toBeGreaterThan(0.8);
    });

    test('handles empty strings', () => {
      expect(similarity('', 'hello')).toBe(0);
      expect(similarity('hello', '')).toBe(0);
    });

    test('handles both empty strings', () => {
      expect(similarity('', '')).toBe(0);
    });

    test('is case-insensitive', () => {
      const score = similarity('HELLO', 'hello');
      expect(score).toBe(1);
    });
  });

  describe('matchCitationToChunk', () => {
    const chunks = [
      { metadata: { title: 'Singapore Export Guide', doc_id: 'sg_export' }, score: 0.9 },
      { metadata: { title: 'Customs Overview', doc_id: 'customs' }, score: 0.8 },
    ];

    test('matches exact title', () => {
      const citation = { title: 'Singapore Export Guide' };
      const match = matchCitationToChunk(citation, chunks);

      expect(match).not.toBeNull();
      expect(match.metadata.doc_id).toBe('sg_export');
    });

    test('matches case-insensitive', () => {
      const citation = { title: 'singapore export guide' };
      const match = matchCitationToChunk(citation, chunks);

      expect(match).not.toBeNull();
    });

    test('returns null for no match', () => {
      const citation = { title: 'Unknown Document' };
      const match = matchCitationToChunk(citation, chunks);

      expect(match).toBeNull();
    });

    test('handles empty chunks array', () => {
      const citation = { title: 'Test' };
      const match = matchCitationToChunk(citation, []);

      expect(match).toBeNull();
    });

    test('handles null chunks', () => {
      const citation = { title: 'Test' };
      const match = matchCitationToChunk(citation, null);

      expect(match).toBeNull();
    });

    test('matches partial title', () => {
      const citation = { title: 'Export Guide' };
      const match = matchCitationToChunk(citation, chunks);

      expect(match).not.toBeNull();
      expect(match.metadata.doc_id).toBe('sg_export');
    });

    test('uses fuzzy matching for typos', () => {
      const citation = { title: 'Singapure Export Guide' }; // typo
      const match = matchCitationToChunk(citation, chunks);

      expect(match).not.toBeNull();
      expect(match.metadata.doc_id).toBe('sg_export');
    });
  });

  describe('enrichCitations', () => {
    const chunks = [
      {
        metadata: {
          title: 'Export Guide',
          doc_id: 'export_guide',
          source_urls: 'https://example.com/export',
        },
        score: 0.85,
      },
    ];

    test('enriches matched citation', () => {
      const citations = [{ title: 'Export Guide', section: 'Docs' }];
      const enriched = enrichCitations(citations, chunks);

      expect(enriched[0].matched).toBe(true);
      expect(enriched[0].docId).toBe('export_guide');
      expect(enriched[0].sourceUrls).toContain('https://example.com/export');
      expect(enriched[0].score).toBe(0.85);
      expect(enriched[0].fullTitle).toBe('Export Guide');
    });

    test('marks unmatched citation', () => {
      const citations = [{ title: 'Unknown Doc' }];
      const enriched = enrichCitations(citations, chunks);

      expect(enriched[0].matched).toBe(false);
      expect(enriched[0].sourceUrls).toEqual([]);
      expect(enriched[0].docId).toBeNull();
      expect(enriched[0].score).toBeNull();
    });

    test('handles multiple source URLs', () => {
      const multiUrlChunks = [{
        metadata: {
          title: 'Multi Source Doc',
          doc_id: 'multi',
          source_urls: 'https://url1.com,https://url2.com',
        },
        score: 0.9,
      }];

      const citations = [{ title: 'Multi Source Doc' }];
      const enriched = enrichCitations(citations, multiUrlChunks);

      expect(enriched[0].sourceUrls).toHaveLength(2);
      expect(enriched[0].sourceUrls).toContain('https://url1.com');
      expect(enriched[0].sourceUrls).toContain('https://url2.com');
    });

    test('handles empty source_urls', () => {
      const emptyUrlChunks = [{
        metadata: {
          title: 'Internal Doc',
          doc_id: 'internal',
          source_urls: '',
        },
        score: 0.8,
      }];

      const citations = [{ title: 'Internal Doc' }];
      const enriched = enrichCitations(citations, emptyUrlChunks);

      expect(enriched[0].matched).toBe(true);
      expect(enriched[0].sourceUrls).toEqual([]);
    });
  });

  describe('formatCitationsMarkdown', () => {
    test('formats citations with URLs', () => {
      const citations = [{
        title: 'Export Guide',
        fullTitle: 'Singapore Export Guide',
        section: 'Documents',
        sourceUrls: ['https://example.com'],
        matched: true,
      }];

      const markdown = formatCitationsMarkdown(citations);

      expect(markdown).toContain('**Sources:**');
      expect(markdown).toContain('[Singapore Export Guide > Documents](https://example.com)');
    });

    test('formats internal documents', () => {
      const citations = [{
        title: 'Internal Policy',
        fullTitle: 'Internal Policy',
        sourceUrls: [],
        matched: true,
      }];

      const markdown = formatCitationsMarkdown(citations);

      expect(markdown).toContain('Internal Policy');
      expect(markdown).toContain('*(Internal Document)*');
    });

    test('returns empty string for no citations', () => {
      const markdown = formatCitationsMarkdown([]);
      expect(markdown).toBe('');
    });

    test('deduplicates in output', () => {
      const citations = [
        { title: 'Doc A', sourceUrls: ['https://a.com'] },
        { title: 'Doc A', sourceUrls: ['https://a.com'] },
        { title: 'Doc B', sourceUrls: ['https://b.com'] },
      ];

      const markdown = formatCitationsMarkdown(citations);
      const matches = markdown.match(/Doc A/g);
      expect(matches).toHaveLength(1);
    });

    test('handles citation without section', () => {
      const citations = [{
        title: 'Simple Doc',
        fullTitle: 'Simple Document',
        sourceUrls: ['https://example.com'],
        matched: true,
      }];

      const markdown = formatCitationsMarkdown(citations);
      expect(markdown).toContain('[Simple Document](https://example.com)');
    });
  });

  describe('deduplicateCitations', () => {
    test('removes duplicate titles', () => {
      const citations = [
        { title: 'Doc A' },
        { title: 'Doc B' },
        { title: 'Doc A' },
      ];

      const unique = deduplicateCitations(citations);

      expect(unique).toHaveLength(2);
    });

    test('is case-insensitive', () => {
      const citations = [
        { title: 'Document' },
        { title: 'DOCUMENT' },
      ];

      const unique = deduplicateCitations(citations);

      expect(unique).toHaveLength(1);
    });

    test('preserves first occurrence', () => {
      const citations = [
        { title: 'Doc A', section: 'Section 1' },
        { title: 'Doc A', section: 'Section 2' },
      ];

      const unique = deduplicateCitations(citations);

      expect(unique).toHaveLength(1);
      expect(unique[0].section).toBe('Section 1');
    });

    test('handles empty array', () => {
      const unique = deduplicateCitations([]);
      expect(unique).toHaveLength(0);
    });
  });

  describe('processCitations', () => {
    test('processes complete response', () => {
      const text = 'Based on [Export Guide > Docs], you need invoices.';
      const chunks = [{
        metadata: { title: 'Export Guide', doc_id: 'eg', source_urls: 'https://ex.com' },
        score: 0.9,
      }];

      const result = processCitations(text, chunks);

      expect(result.citations).toHaveLength(1);
      expect(result.stats.matched).toBe(1);
      expect(result.stats.total).toBe(1);
      expect(result.markdown).toContain('**Sources:**');
    });

    test('processes response with unmatched citations', () => {
      const text = '[Known Doc] and [Completely Different Guide] are cited.';
      const chunks = [{
        metadata: { title: 'Known Doc', doc_id: 'known', source_urls: 'https://known.com' },
        score: 0.8,
      }];

      const result = processCitations(text, chunks);

      expect(result.stats.total).toBe(2);
      expect(result.stats.matched).toBe(1);
      expect(result.stats.unmatched).toBe(1);
    });

    test('processes response with no citations', () => {
      const text = 'No citations in this response.';
      const chunks = [];

      const result = processCitations(text, chunks);

      expect(result.citations).toHaveLength(0);
      expect(result.stats.total).toBe(0);
      expect(result.markdown).toBe('');
    });
  });
});
