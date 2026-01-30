# Task 5.3: Create Citation Extractor

## Persona

> You are a backend developer with expertise in text parsing and data extraction.
> You follow TDD principles and create robust, well-tested code.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. The LLM service generates responses with inline citations like `[Document Title > Section]`. Now we need a citation extractor that parses these citations and links them to source metadata (URLs, doc IDs) from the retrieved chunks.

### Current State
- LLM generates responses with `[Document Title > Section]` citations
- Retrieval service returns chunks with metadata including `source_urls`, `doc_id`, `title`, `section`
- `getMetadataForCitation()` extracts citation metadata from chunks
- No citation parsing or linking implemented yet

### Reference Documents
- `03_rag_pipeline/src/services/retrieval.js` - `getMetadataForCitation()` function
- `03_rag_pipeline/src/services/llm.js` - Response generation
- `03_rag_pipeline/docs/01_implementation_roadmap.md` - Task specifications

### Dependencies
- Task 5.1: Create LLM Service ✅
- Task 5.2: Create System Prompt ✅

---

## Task

### Objective
Create a citation extractor module that parses citations from LLM responses and enriches them with source metadata (URLs, document IDs) from the retrieved chunks.

### Requirements

1. **Parse Citations from Response**
   - Extract `[Document Title > Section]` patterns
   - Handle variations: `[Title]`, `[Title > Section]`, `According to [Title]...`
   - Return list of parsed citations with positions

2. **Match Citations to Source Chunks**
   - Match citation titles to chunk metadata
   - Fuzzy matching for slight variations
   - Handle multiple matches (return best match)

3. **Enrich Citations with Metadata**
   - Add source URLs from chunk metadata
   - Add document ID for internal tracking
   - Add relevance score from retrieval

4. **Format Citations for Response**
   - Create structured citation objects
   - Generate markdown-formatted citation list
   - Support both inline and footnote styles

5. **Write comprehensive tests**
   - Test citation parsing patterns
   - Test matching logic
   - Test edge cases (no citations, malformed citations)

### Specifications

**src/services/citations.js**:
```javascript
/**
 * Citation Extractor Service
 * Parses and enriches citations from LLM responses.
 */

import { logger } from '../utils/logger.js';

/**
 * Citation pattern for extracting references from text.
 * Matches: [Title], [Title > Section], According to [Title]...
 */
const CITATION_PATTERN = /\[([^\]]+)\]/g;

/**
 * Extract citations from LLM response text.
 *
 * @param {string} text - LLM response text
 * @returns {Array<Object>} Extracted citations with text and position
 */
export function extractCitations(text) {
  const citations = [];
  let match;

  while ((match = CITATION_PATTERN.exec(text)) !== null) {
    const fullMatch = match[0];
    const content = match[1];

    // Parse title and section
    const parts = content.split('>').map(p => p.trim());
    const title = parts[0];
    const section = parts[1] || null;

    citations.push({
      raw: fullMatch,
      title,
      section,
      position: match.index,
    });
  }

  // Reset regex state
  CITATION_PATTERN.lastIndex = 0;

  return citations;
}

/**
 * Match a citation to source chunks by title.
 *
 * @param {Object} citation - Parsed citation object
 * @param {Array} chunks - Retrieved chunks with metadata
 * @returns {Object|null} Best matching chunk or null
 */
export function matchCitationToChunk(citation, chunks) {
  if (!chunks || chunks.length === 0) return null;

  // Try exact title match first
  let match = chunks.find(chunk =>
    chunk.metadata?.title?.toLowerCase() === citation.title.toLowerCase()
  );

  if (match) return match;

  // Try partial/fuzzy match
  match = chunks.find(chunk => {
    const chunkTitle = chunk.metadata?.title?.toLowerCase() || '';
    const citationTitle = citation.title.toLowerCase();

    return chunkTitle.includes(citationTitle) ||
           citationTitle.includes(chunkTitle) ||
           similarity(chunkTitle, citationTitle) > 0.7;
  });

  return match || null;
}

/**
 * Simple string similarity (Dice coefficient).
 *
 * @param {string} a - First string
 * @param {string} b - Second string
 * @returns {number} Similarity score 0-1
 */
export function similarity(a, b) {
  if (!a || !b) return 0;
  if (a === b) return 1;

  const aBigrams = getBigrams(a.toLowerCase());
  const bBigrams = getBigrams(b.toLowerCase());

  let matches = 0;
  for (const bigram of aBigrams) {
    if (bBigrams.has(bigram)) matches++;
  }

  return (2 * matches) / (aBigrams.size + bBigrams.size);
}

/**
 * Get bigrams (character pairs) from string.
 *
 * @param {string} str - Input string
 * @returns {Set<string>} Set of bigrams
 */
function getBigrams(str) {
  const bigrams = new Set();
  for (let i = 0; i < str.length - 1; i++) {
    bigrams.add(str.slice(i, i + 2));
  }
  return bigrams;
}

/**
 * Enrich citations with source metadata from chunks.
 *
 * @param {Array} citations - Parsed citations
 * @param {Array} chunks - Retrieved chunks with metadata
 * @returns {Array<Object>} Enriched citations
 */
export function enrichCitations(citations, chunks) {
  return citations.map(citation => {
    const matchedChunk = matchCitationToChunk(citation, chunks);

    if (!matchedChunk) {
      logger.warn('No chunk match for citation', { title: citation.title });
      return {
        ...citation,
        matched: false,
        sourceUrls: [],
        docId: null,
        score: null,
      };
    }

    const sourceUrls = matchedChunk.metadata?.source_urls
      ?.split(',')
      .filter(Boolean) || [];

    return {
      ...citation,
      matched: true,
      sourceUrls,
      docId: matchedChunk.metadata?.doc_id || null,
      score: matchedChunk.score || null,
      fullTitle: matchedChunk.metadata?.title || citation.title,
    };
  });
}

/**
 * Format citations as markdown list.
 *
 * @param {Array} citations - Enriched citations
 * @returns {string} Markdown formatted citation list
 */
export function formatCitationsMarkdown(citations) {
  const uniqueCitations = deduplicateCitations(citations);

  if (uniqueCitations.length === 0) {
    return '';
  }

  const lines = ['', '---', '**Sources:**'];

  uniqueCitations.forEach((citation, index) => {
    const title = citation.fullTitle || citation.title;
    const section = citation.section ? ` > ${citation.section}` : '';

    if (citation.sourceUrls && citation.sourceUrls.length > 0) {
      lines.push(`${index + 1}. [${title}${section}](${citation.sourceUrls[0]})`);
    } else {
      lines.push(`${index + 1}. ${title}${section} *(Internal Document)*`);
    }
  });

  return lines.join('\n');
}

/**
 * Remove duplicate citations by title.
 *
 * @param {Array} citations - Citations array
 * @returns {Array} Deduplicated citations
 */
export function deduplicateCitations(citations) {
  const seen = new Set();
  return citations.filter(citation => {
    const key = citation.title.toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

/**
 * Process LLM response to extract and enrich all citations.
 *
 * @param {string} responseText - LLM response text
 * @param {Array} chunks - Retrieved chunks used for context
 * @returns {Object} Processed result with citations
 */
export function processCitations(responseText, chunks) {
  const extracted = extractCitations(responseText);
  const enriched = enrichCitations(extracted, chunks);
  const markdown = formatCitationsMarkdown(enriched);

  logger.info('Citations processed', {
    found: extracted.length,
    matched: enriched.filter(c => c.matched).length,
  });

  return {
    citations: enriched,
    markdown,
    stats: {
      total: extracted.length,
      matched: enriched.filter(c => c.matched).length,
      unmatched: enriched.filter(c => !c.matched).length,
    },
  };
}
```

**tests/citations.test.js**:
```javascript
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
} from '../src/services/citations.js';

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
    });

    test('marks unmatched citation', () => {
      const citations = [{ title: 'Unknown Doc' }];
      const enriched = enrichCitations(citations, chunks);

      expect(enriched[0].matched).toBe(false);
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
      expect(result.markdown).toContain('**Sources:**');
    });
  });
});
```

### Constraints
- Use ES modules (import/export)
- No external NLP libraries (keep it simple)
- Handle edge cases gracefully
- Log warnings for unmatched citations

### Acceptance Criteria
- [ ] `src/services/citations.js` implements all functions
- [ ] `extractCitations` parses `[Title]` and `[Title > Section]` patterns
- [ ] `matchCitationToChunk` finds best matching chunk
- [ ] `enrichCitations` adds URLs and doc IDs
- [ ] `formatCitationsMarkdown` creates formatted source list
- [ ] `processCitations` orchestrates the full flow
- [ ] All tests pass: `npm test -- --testPathPattern=citations`

### TDD Requirements
- [ ] Write tests first
- [ ] Implement functions to pass tests
- [ ] Run `npm test` to verify all pass

---

## Format

### Output Structure
- `src/services/citations.js` - Full implementation
- `tests/citations.test.js` - Complete test file
- Update `src/services/index.js` to export citation functions

### Validation Commands

```bash
cd pilot_phase1_poc/03_rag_pipeline

# Run citation tests only
npm test -- --testPathPattern=citations

# Run all tests
npm test
```

### Expected Test Output
```
PASS tests/citations.test.js
  Citation Extractor
    extractCitations
      ✓ extracts simple citation
      ✓ extracts citation with section
      ✓ extracts multiple citations
      ✓ returns empty array for no citations
      ✓ captures position of citation
    similarity
      ✓ returns 1 for identical strings
      ✓ returns 0 for completely different strings
      ✓ returns partial match for similar strings
      ✓ handles empty strings
    matchCitationToChunk
      ✓ matches exact title
      ✓ matches case-insensitive
      ✓ returns null for no match
      ✓ handles empty chunks array
    enrichCitations
      ✓ enriches matched citation
      ✓ marks unmatched citation
    formatCitationsMarkdown
      ✓ formats citations with URLs
      ✓ formats internal documents
      ✓ returns empty string for no citations
    deduplicateCitations
      ✓ removes duplicate titles
      ✓ is case-insensitive
    processCitations
      ✓ processes complete response

Test Suites: 1 passed, 1 total
Tests:       21 passed, 21 total
```
