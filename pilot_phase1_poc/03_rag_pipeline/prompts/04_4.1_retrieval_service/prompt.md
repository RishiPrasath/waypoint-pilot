# Task 4.1: Create Retrieval Service Module

## Persona

> You are a backend developer with expertise in vector databases and semantic search.
> You follow TDD principles and create well-tested, production-ready code.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. The Node.js project structure is complete. Now we implement the retrieval service that queries ChromaDB for relevant knowledge base chunks.

### Current State
- Node.js project created at `03_rag_pipeline/` (Task 3.1 complete)
- ChromaDB populated with 483 chunks in `ingestion/chroma_db/`
- Collection name: `waypoint_kb`
- Metadata includes: doc_id, title, category, source_urls, section, chunk_index, etc.
- Retrieval quality tested at 76% hit rate (PROCEED decision)

### Reference Documents
- `03_rag_pipeline/docs/00_week2_rag_pipeline_plan.md` - Architecture details
- `03_rag_pipeline/docs/01_implementation_roadmap.md` - Task specifications
- `03_rag_pipeline/prompts/02_2.1_retrieval_quality_test/REPORT.md` - Retrieval test results

### Dependencies
- Task 3.1: Create Node.js Project Structure ✅

### MCP Tools Available
If you need documentation for ChromaDB or other libraries:
```
mcp__context7__resolve-library-id: Find library ID for documentation lookup
mcp__context7__query-docs: Query library documentation
mcp__docfork__docfork_search_docs: Search documentation across repositories
```

---

## Task

### Objective
Implement the ChromaDB retrieval service that queries the knowledge base and returns relevant chunks with metadata for context assembly.

### Requirements

1. **Implement ChromaDB Client**
   - Initialize persistent client pointing to `./ingestion/chroma_db`
   - Get `waypoint_kb` collection
   - Handle connection errors gracefully
   - Use singleton pattern for client

2. **Implement `retrieveChunks` function**
   - Accept query string and options (topK, threshold)
   - Query ChromaDB using the query text (let ChromaDB handle embedding)
   - Return top-K results with documents, metadata, and distances
   - Convert distances to similarity scores (1 - distance for cosine)

3. **Implement `filterByThreshold` function**
   - Filter chunks below relevance threshold
   - Default threshold from config (0.15)
   - Return filtered array

4. **Implement `formatContext` function**
   - Format retrieved chunks into context string for LLM
   - Include document title, section, and content
   - Respect max token limit (approximate by chars)

5. **Write comprehensive tests**
   - Test ChromaDB connection
   - Test retrieval returns expected format
   - Test filtering by threshold
   - Test context formatting
   - Mock ChromaDB for unit tests

### Specifications

**src/services/retrieval.js**:
```javascript
/**
 * ChromaDB Retrieval Service
 * Handles vector similarity search against the knowledge base.
 */

import { ChromaClient } from 'chromadb';
import { config } from '../config.js';
import { logger } from '../utils/logger.js';

// Singleton client instance
let chromaClient = null;
let collection = null;

/**
 * Initialize ChromaDB client and collection.
 * Uses singleton pattern to reuse connection.
 *
 * @returns {Promise<Object>} ChromaDB collection instance
 * @throws {Error} If initialization fails
 */
export async function initChromaClient() {
  if (collection) return collection;

  try {
    chromaClient = new ChromaClient({
      path: config.chromaPath,
    });
    collection = await chromaClient.getCollection({
      name: config.collectionName,
    });
    logger.info('ChromaDB initialized', {
      collection: config.collectionName,
      path: config.chromaPath,
    });
    return collection;
  } catch (error) {
    logger.error('ChromaDB initialization failed', { error: error.message });
    throw error;
  }
}

/**
 * Retrieve relevant chunks from ChromaDB.
 *
 * @param {string} query - The search query
 * @param {Object} options - Retrieval options
 * @param {number} options.topK - Number of results to return (default from config)
 * @param {number} options.threshold - Minimum relevance score (default from config)
 * @returns {Promise<Array>} Retrieved chunks with metadata and scores
 */
export async function retrieveChunks(query, options = {}) {
  const topK = options.topK || config.retrievalTopK;
  const threshold = options.threshold || config.relevanceThreshold;

  const col = await initChromaClient();

  // Query ChromaDB - it handles embedding internally
  const results = await col.query({
    queryTexts: [query],
    nResults: topK,
    include: ['documents', 'metadatas', 'distances'],
  });

  // Transform results to standardized format
  const chunks = results.documents[0].map((doc, i) => ({
    content: doc,
    metadata: results.metadatas[0][i],
    distance: results.distances[0][i],
    score: 1 - results.distances[0][i], // Convert distance to similarity
  }));

  // Filter by threshold and return
  return filterByThreshold(chunks, threshold);
}

/**
 * Filter chunks by relevance threshold.
 *
 * @param {Array} chunks - Chunks with scores
 * @param {number} threshold - Minimum score to keep
 * @returns {Array} Filtered chunks
 */
export function filterByThreshold(chunks, threshold) {
  return chunks.filter(chunk => chunk.score >= threshold);
}

/**
 * Format retrieved chunks into context string for LLM.
 *
 * @param {Array} chunks - Retrieved chunks with metadata
 * @param {number} maxChars - Maximum characters (approximate token limit)
 * @returns {string} Formatted context string
 */
export function formatContext(chunks, maxChars = config.maxContextTokens * 4) {
  let context = '';
  let charCount = 0;

  for (const chunk of chunks) {
    const title = chunk.metadata.title || 'Unknown Document';
    const section = chunk.metadata.section || '';
    const header = section ? `[${title} > ${section}]` : `[${title}]`;
    const entry = `${header}\n${chunk.content}\n\n`;

    if (charCount + entry.length > maxChars) break;

    context += entry;
    charCount += entry.length;
  }

  return context.trim();
}

/**
 * Get metadata for citations from chunks.
 *
 * @param {Array} chunks - Retrieved chunks
 * @returns {Array} Citation metadata objects
 */
export function getMetadataForCitation(chunks) {
  return chunks.map(chunk => ({
    title: chunk.metadata.title,
    section: chunk.metadata.section,
    sourceUrls: chunk.metadata.source_urls?.split(',') || [],
    docId: chunk.metadata.doc_id,
    score: chunk.score,
  }));
}
```

**tests/retrieval.test.js**:
```javascript
/**
 * Retrieval Service Tests
 */

import { jest } from '@jest/globals';

// Mock chromadb before importing the module
jest.unstable_mockModule('chromadb', () => ({
  ChromaClient: jest.fn().mockImplementation(() => ({
    getCollection: jest.fn().mockResolvedValue({
      query: jest.fn().mockResolvedValue({
        documents: [['Doc 1 content', 'Doc 2 content']],
        metadatas: [[
          { title: 'Doc 1', section: 'Section A', doc_id: 'doc1' },
          { title: 'Doc 2', section: 'Section B', doc_id: 'doc2' },
        ]],
        distances: [[0.1, 0.3]],
      }),
    }),
  })),
}));

const { retrieveChunks, filterByThreshold, formatContext, getMetadataForCitation } = await import('../src/services/retrieval.js');

describe('Retrieval Service', () => {
  describe('retrieveChunks', () => {
    test('returns chunks with expected format', async () => {
      const chunks = await retrieveChunks('test query');

      expect(Array.isArray(chunks)).toBe(true);
      expect(chunks.length).toBeGreaterThan(0);
      expect(chunks[0]).toHaveProperty('content');
      expect(chunks[0]).toHaveProperty('metadata');
      expect(chunks[0]).toHaveProperty('score');
    });

    test('converts distances to similarity scores', async () => {
      const chunks = await retrieveChunks('test query', { threshold: 0 });

      // Distance of 0.1 should become score of 0.9
      expect(chunks[0].score).toBeCloseTo(0.9, 1);
    });
  });

  describe('filterByThreshold', () => {
    const testChunks = [
      { score: 0.9, content: 'high' },
      { score: 0.5, content: 'medium' },
      { score: 0.1, content: 'low' },
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
  });

  describe('formatContext', () => {
    const testChunks = [
      { content: 'Content 1', metadata: { title: 'Doc 1', section: 'Sec A' } },
      { content: 'Content 2', metadata: { title: 'Doc 2' } },
    ];

    test('formats chunks with title and section', () => {
      const context = formatContext(testChunks);
      expect(context).toContain('[Doc 1 > Sec A]');
      expect(context).toContain('Content 1');
    });

    test('handles missing section', () => {
      const context = formatContext(testChunks);
      expect(context).toContain('[Doc 2]');
    });

    test('respects max character limit', () => {
      const context = formatContext(testChunks, 50);
      expect(context.length).toBeLessThanOrEqual(100); // Some buffer for headers
    });
  });

  describe('getMetadataForCitation', () => {
    test('extracts citation metadata', () => {
      const chunks = [{
        metadata: {
          title: 'Test Doc',
          section: 'Test Section',
          source_urls: 'https://example.com,https://example2.com',
          doc_id: 'test_doc',
        },
        score: 0.9,
      }];

      const citations = getMetadataForCitation(chunks);

      expect(citations[0].title).toBe('Test Doc');
      expect(citations[0].sourceUrls).toHaveLength(2);
      expect(citations[0].score).toBe(0.9);
    });
  });
});
```

### Constraints
- Use ES modules (import/export)
- ChromaDB handles embeddings - do NOT call Python for query embedding
- Keep retrieval latency under 200ms for single query
- Handle ChromaDB connection errors gracefully
- Log all retrieval operations with timing

### Acceptance Criteria
- [ ] `src/services/retrieval.js` implements all functions
- [ ] ChromaDB client initializes with singleton pattern
- [ ] `retrieveChunks` returns chunks with content, metadata, score
- [ ] `filterByThreshold` filters by relevance score
- [ ] `formatContext` creates LLM-ready context string
- [ ] `getMetadataForCitation` extracts citation data
- [ ] All tests pass: `npm test -- --testPathPattern=retrieval`
- [ ] Manual test: query returns relevant chunks

### TDD Requirements
- [ ] Write tests first (mock ChromaDB)
- [ ] Implement functions to pass tests
- [ ] Run `npm test` to verify all pass

---

## Format

### Output Structure
- `src/services/retrieval.js` - Full implementation
- `tests/retrieval.test.js` - Complete test file
- Update any imports in `src/services/index.js` if needed

### Code Style
- ES modules (import/export)
- JSDoc comments for all exported functions
- camelCase for variables/functions
- 2-space indentation
- Async/await for all async operations

### Validation Commands

```bash
cd pilot_phase1_poc/03_rag_pipeline

# Run retrieval tests only
npm test -- --testPathPattern=retrieval

# Manual integration test
node -e "
  import('./src/services/retrieval.js').then(async ({ retrieveChunks }) => {
    const chunks = await retrieveChunks('Singapore export documents');
    console.log('Retrieved:', chunks.length, 'chunks');
    console.log('Top result:', chunks[0]?.metadata?.title, 'Score:', chunks[0]?.score);
  });
"
```

### Expected Test Output
```
PASS tests/retrieval.test.js
  Retrieval Service
    retrieveChunks
      ✓ returns chunks with expected format
      ✓ converts distances to similarity scores
    filterByThreshold
      ✓ filters chunks below threshold
      ✓ returns empty array when all below threshold
    formatContext
      ✓ formats chunks with title and section
      ✓ handles missing section
      ✓ respects max character limit
    getMetadataForCitation
      ✓ extracts citation metadata

Test Suites: 1 passed, 1 total
Tests:       8 passed, 8 total
```
