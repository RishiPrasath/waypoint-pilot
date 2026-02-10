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
  buildSources,
  buildRelatedDocs,
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

    test('ignores non-bracket citation formats (by design)', () => {
      // System prompt enforces [Title > Section] format.
      // Unbracketed references like "Source: Title" are intentionally NOT extracted
      // to avoid greedy regex captures that produce garbage titles.
      const text = 'Source: Singapore Customs Guide is relevant. Reference: Export Guide too.';
      const citations = extractCitations(text);

      expect(citations).toHaveLength(0);
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

    test('filters out N/A from source_urls', () => {
      const naChunks = [{
        metadata: {
          title: 'Mixed URLs Doc',
          doc_id: 'mixed',
          source_urls: 'https://real.com,N/A',
        },
        score: 0.9,
      }];

      const citations = [{ title: 'Mixed URLs Doc' }];
      const enriched = enrichCitations(citations, naChunks);

      expect(enriched[0].sourceUrls).toEqual(['https://real.com']);
    });

    test('trims spaces around source_urls', () => {
      const spacyChunks = [{
        metadata: {
          title: 'Spacy Doc',
          doc_id: 'spacy',
          source_urls: ' https://url1.com , https://url2.com ',
        },
        score: 0.85,
      }];

      const citations = [{ title: 'Spacy Doc' }];
      const enriched = enrichCitations(citations, spacyChunks);

      expect(enriched[0].sourceUrls).toHaveLength(2);
      expect(enriched[0].sourceUrls[0]).toBe('https://url1.com');
      expect(enriched[0].sourceUrls[1]).toBe('https://url2.com');
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

  describe('buildSources', () => {
    const chunks = [
      {
        metadata: {
          title: 'Singapore Import Procedures',
          doc_id: 'sg_import',
          source_org: 'Singapore Customs',
          source_urls: 'https://customs.gov.sg/import,https://customs.gov.sg/docs',
        },
        score: 0.9,
      },
      {
        metadata: {
          title: 'Booking Procedure',
          doc_id: 'booking_proc',
          source_org: '',
          source_urls: '',
        },
        score: 0.8,
      },
    ];

    test('returns source objects with correct shape', () => {
      const citations = [{
        title: 'Singapore Import Procedures',
        fullTitle: 'Singapore Import Procedures',
        section: 'Documentation',
        matched: true,
        sourceUrls: ['https://customs.gov.sg/import'],
        docId: 'sg_import',
      }];

      const sources = buildSources(citations, chunks);

      expect(sources).toHaveLength(1);
      expect(sources[0]).toEqual({
        title: 'Singapore Import Procedures',
        org: 'Singapore Customs',
        url: 'https://customs.gov.sg/import',
        section: 'Documentation',
      });
    });

    test('deduplicates by URL', () => {
      const citations = [
        {
          title: 'Doc A', fullTitle: 'Doc A', section: 'S1',
          matched: true, sourceUrls: ['https://example.com'], docId: 'sg_import',
        },
        {
          title: 'Doc A', fullTitle: 'Doc A', section: 'S2',
          matched: true, sourceUrls: ['https://example.com'], docId: 'sg_import',
        },
      ];

      const sources = buildSources(citations, chunks);

      expect(sources).toHaveLength(1);
    });

    test('excludes unmatched citations', () => {
      const citations = [{
        title: 'Unknown', matched: false, sourceUrls: [], docId: null,
      }];

      const sources = buildSources(citations, chunks);

      expect(sources).toHaveLength(0);
    });

    test('excludes citations with no sourceUrls', () => {
      const citations = [{
        title: 'Booking Procedure', fullTitle: 'Booking Procedure',
        matched: true, sourceUrls: [], docId: 'booking_proc',
      }];

      const sources = buildSources(citations, chunks);

      expect(sources).toHaveLength(0);
    });

    test('returns empty array when no external sources', () => {
      const sources = buildSources([], chunks);

      expect(sources).toEqual([]);
    });

    test('handles multiple URLs per citation', () => {
      const citations = [{
        title: 'Singapore Import Procedures',
        fullTitle: 'Singapore Import Procedures',
        section: null,
        matched: true,
        sourceUrls: ['https://customs.gov.sg/import', 'https://customs.gov.sg/docs'],
        docId: 'sg_import',
      }];

      const sources = buildSources(citations, chunks);

      expect(sources).toHaveLength(2);
      expect(sources[0].url).toBe('https://customs.gov.sg/import');
      expect(sources[1].url).toBe('https://customs.gov.sg/docs');
      expect(sources[0].org).toBe('Singapore Customs');
    });

    test('sets section to null when citation has no section', () => {
      const citations = [{
        title: 'Doc', fullTitle: 'Doc',
        matched: true, sourceUrls: ['https://example.com'], docId: 'sg_import',
      }];

      const sources = buildSources(citations, chunks);

      expect(sources[0].section).toBeNull();
    });
  });

  describe('buildRelatedDocs', () => {
    test('returns relatedDoc objects with correct shape', () => {
      const chunks = [{
        metadata: {
          title: 'Singapore Import Procedures',
          doc_id: 'sg_import',
          category: '01_regulatory',
          source_urls: 'https://customs.gov.sg/import',
        },
        score: 0.9,
      }];

      const docs = buildRelatedDocs(chunks);

      expect(docs).toHaveLength(1);
      expect(docs[0]).toEqual({
        title: 'Singapore Import Procedures',
        category: 'regulatory',
        docId: 'sg_import',
        url: 'https://customs.gov.sg/import',
      });
    });

    test('maps all category prefixes correctly', () => {
      const chunks = [
        { metadata: { title: 'A', doc_id: 'a', category: '01_regulatory', source_urls: '' }, score: 0.9 },
        { metadata: { title: 'B', doc_id: 'b', category: '02_carriers', source_urls: '' }, score: 0.8 },
        { metadata: { title: 'C', doc_id: 'c', category: '03_reference', source_urls: '' }, score: 0.7 },
        { metadata: { title: 'D', doc_id: 'd', category: '04_internal_synthetic', source_urls: '' }, score: 0.6 },
      ];

      const docs = buildRelatedDocs(chunks);

      expect(docs[0].category).toBe('regulatory');
      expect(docs[1].category).toBe('carrier');
      expect(docs[2].category).toBe('reference');
      expect(docs[3].category).toBe('internal');
    });

    test('deduplicates by docId', () => {
      const chunks = [
        { metadata: { title: 'Doc', doc_id: 'same_doc', category: '01_regulatory', source_urls: '' }, score: 0.9 },
        { metadata: { title: 'Doc', doc_id: 'same_doc', category: '01_regulatory', source_urls: '' }, score: 0.8 },
      ];

      const docs = buildRelatedDocs(chunks);

      expect(docs).toHaveLength(1);
    });

    test('sets url to null for internal documents with no source_urls', () => {
      const chunks = [{
        metadata: {
          title: 'Internal Policy',
          doc_id: 'internal_policy',
          category: '04_internal_synthetic',
          source_urls: '',
        },
        score: 0.8,
      }];

      const docs = buildRelatedDocs(chunks);

      expect(docs[0].url).toBeNull();
    });

    test('preserves first-appearance order', () => {
      const chunks = [
        { metadata: { title: 'First', doc_id: 'first', category: '01_regulatory', source_urls: '' }, score: 0.9 },
        { metadata: { title: 'Second', doc_id: 'second', category: '02_carriers', source_urls: '' }, score: 0.8 },
        { metadata: { title: 'First Again', doc_id: 'first', category: '01_regulatory', source_urls: '' }, score: 0.7 },
      ];

      const docs = buildRelatedDocs(chunks);

      expect(docs).toHaveLength(2);
      expect(docs[0].docId).toBe('first');
      expect(docs[1].docId).toBe('second');
    });

    test('returns empty array for empty chunks', () => {
      const docs = buildRelatedDocs([]);

      expect(docs).toEqual([]);
    });

    test('handles chunks with missing metadata gracefully', () => {
      const chunks = [
        { metadata: { title: 'Doc', doc_id: 'doc1', category: '01_regulatory', source_urls: 'https://example.com' }, score: 0.9 },
        { metadata: {}, score: 0.5 },
      ];

      const docs = buildRelatedDocs(chunks);

      expect(docs).toHaveLength(1);
      expect(docs[0].docId).toBe('doc1');
    });

    test('falls back to raw value for unknown category', () => {
      const chunks = [{
        metadata: { title: 'Custom Doc', doc_id: 'custom', category: 'custom_category', source_urls: '' },
        score: 0.8,
      }];

      const docs = buildRelatedDocs(chunks);

      expect(docs[0].category).toBe('custom_category');
    });

    test('sets url to null when source_urls is N/A', () => {
      const chunks = [{
        metadata: {
          title: 'Internal Policy',
          doc_id: 'internal_na',
          category: '04_internal_synthetic',
          source_urls: 'N/A',
        },
        score: 0.75,
      }];

      const docs = buildRelatedDocs(chunks);

      expect(docs[0].url).toBeNull();
    });
  });

  describe('End-to-end enrichment flow', () => {
    test('full flow with mixed external and internal sources', () => {
      const responseText = 'According to [Singapore GST Guide > Rates], GST is 9%. See also [Booking Procedure > Steps].';
      const chunks = [
        {
          metadata: {
            title: 'Singapore GST Guide',
            doc_id: 'sg_gst',
            source_org: 'Singapore Customs',
            source_urls: 'https://customs.gov.sg/gst',
            category: '01_regulatory',
          },
          score: 0.92,
        },
        {
          metadata: {
            title: 'Booking Procedure',
            doc_id: 'booking_proc',
            source_org: '',
            source_urls: '',
            category: '04_internal_synthetic',
          },
          score: 0.78,
        },
      ];

      const citationResult = processCitations(responseText, chunks);
      const sources = buildSources(citationResult.citations, chunks);
      const relatedDocs = buildRelatedDocs(chunks);

      // processCitations: both citations matched
      expect(citationResult.stats.total).toBe(2);
      expect(citationResult.stats.matched).toBe(2);

      // buildSources: only external URLs appear
      expect(sources).toHaveLength(1);
      expect(sources[0].url).toBe('https://customs.gov.sg/gst');
      expect(sources[0].org).toBe('Singapore Customs');

      // buildRelatedDocs: both docs appear with correct categories
      expect(relatedDocs).toHaveLength(2);
      expect(relatedDocs[0].category).toBe('regulatory');
      expect(relatedDocs[0].url).toBe('https://customs.gov.sg/gst');
      expect(relatedDocs[1].category).toBe('internal');
      expect(relatedDocs[1].url).toBeNull();
    });

    test('full flow with internal-only sources', () => {
      const responseText = 'Per [COD Procedure > Payment], cash on delivery requires approval. See [Escalation Procedure].';
      const chunks = [
        {
          metadata: {
            title: 'COD Procedure',
            doc_id: 'cod_procedure',
            source_org: '',
            source_urls: 'N/A',
            category: '04_internal_synthetic',
          },
          score: 0.88,
        },
        {
          metadata: {
            title: 'Escalation Procedure',
            doc_id: 'escalation_procedure',
            source_org: '',
            source_urls: '',
            category: '04_internal_synthetic',
          },
          score: 0.72,
        },
      ];

      const citationResult = processCitations(responseText, chunks);
      const sources = buildSources(citationResult.citations, chunks);
      const relatedDocs = buildRelatedDocs(chunks);

      // All citations matched
      expect(citationResult.stats.matched).toBe(2);

      // No external sources (all internal)
      expect(sources).toHaveLength(0);

      // relatedDocs still lists both with null URLs
      expect(relatedDocs).toHaveLength(2);
      expect(relatedDocs[0].url).toBeNull();
      expect(relatedDocs[1].url).toBeNull();
      expect(relatedDocs[0].category).toBe('internal');
    });
  });
});
