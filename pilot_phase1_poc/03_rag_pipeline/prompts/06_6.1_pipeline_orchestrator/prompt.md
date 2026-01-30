# Task 6.1: Create Pipeline Orchestrator

## Persona

> You are a backend developer with expertise in building data pipelines and orchestration systems.
> You follow TDD principles and create well-structured, maintainable code.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. All individual services are complete:
- Retrieval service queries ChromaDB for relevant chunks
- LLM service generates responses via Groq API
- Citation extractor parses and enriches citations

Now we need a pipeline orchestrator that ties everything together into a single `processQuery()` function.

### Current State
- `src/services/retrieval.js` - `retrieveChunks()`, `formatContext()`, `getMetadataForCitation()`
- `src/services/llm.js` - `generateResponse()`, `buildSystemPrompt()`
- `src/services/citations.js` - `processCitations()`, `formatCitationsMarkdown()`
- `src/services/pipeline.js` - Placeholder with `throw new Error('Not implemented')`

### Reference Documents
- `03_rag_pipeline/docs/00_week2_rag_pipeline_plan.md` - Pipeline flow
- `03_rag_pipeline/docs/01_implementation_roadmap.md` - Task specifications

### Dependencies
- Task 4.1: Retrieval Service ✅
- Task 5.1: LLM Service ✅
- Task 5.2: System Prompt ✅
- Task 5.3: Citation Extractor ✅

---

## Task

### Objective
Implement the pipeline orchestrator that coordinates the full RAG flow: retrieve → format context → generate response → extract citations → return structured result.

### Requirements

1. **Implement `processQuery` function**
   - Accept query string as input
   - Orchestrate full RAG pipeline
   - Return structured response with answer, citations, metadata
   - Handle errors gracefully at each stage

2. **Collect metrics**
   - Track latency for each stage (retrieval, generation, citation extraction)
   - Count chunks retrieved vs used
   - Record token usage from LLM

3. **Determine confidence level**
   - Based on number of matching chunks
   - Based on relevance scores
   - Return High/Medium/Low with reason

4. **Handle edge cases**
   - No relevant chunks found
   - LLM generation fails
   - Citation extraction finds no citations

5. **Write comprehensive tests**
   - Mock all dependent services
   - Test happy path
   - Test error scenarios
   - Test confidence calculation

### Specifications

**src/services/pipeline.js**:
```javascript
/**
 * RAG Pipeline Orchestrator
 * Coordinates the retrieval-augmented generation flow.
 */

import { retrieveChunks, formatContext, getMetadataForCitation } from './retrieval.js';
import { generateResponse } from './llm.js';
import { processCitations } from './citations.js';
import { logger } from '../utils/logger.js';
import { config } from '../config.js';

/**
 * Process a customer query through the RAG pipeline.
 *
 * @param {string} query - The customer's question
 * @param {Object} options - Pipeline options
 * @param {number} options.topK - Number of chunks to retrieve
 * @param {number} options.threshold - Relevance threshold
 * @returns {Promise<Object>} Complete response with answer, citations, metadata
 */
export async function processQuery(query, options = {}) {
  const startTime = Date.now();
  const metrics = {
    retrievalMs: 0,
    generationMs: 0,
    citationMs: 0,
    totalMs: 0,
  };

  try {
    // Validate input
    if (!query || typeof query !== 'string' || query.trim().length === 0) {
      throw new Error('Query must be a non-empty string');
    }

    const trimmedQuery = query.trim();

    // Stage 1: Retrieve relevant chunks
    const retrievalStart = Date.now();
    const chunks = await retrieveChunks(trimmedQuery, {
      topK: options.topK || config.retrievalTopK,
      threshold: options.threshold || config.relevanceThreshold,
    });
    metrics.retrievalMs = Date.now() - retrievalStart;

    // Handle no results
    if (chunks.length === 0) {
      logger.info('No relevant chunks found', { query: trimmedQuery });
      return buildNoResultsResponse(trimmedQuery, metrics, startTime);
    }

    // Stage 2: Format context for LLM
    const context = formatContext(chunks);

    // Stage 3: Generate LLM response
    const generationStart = Date.now();
    const llmResult = await generateResponse(trimmedQuery, context);
    metrics.generationMs = Date.now() - generationStart;

    // Stage 4: Extract and enrich citations
    const citationStart = Date.now();
    const citationResult = processCitations(llmResult.answer, chunks);
    metrics.citationMs = Date.now() - citationStart;

    // Calculate confidence
    const confidence = calculateConfidence(chunks, citationResult);

    // Build final response
    metrics.totalMs = Date.now() - startTime;

    const response = {
      answer: llmResult.answer,
      citations: citationResult.citations.filter(c => c.matched),
      sourcesMarkdown: citationResult.markdown,
      confidence,
      metadata: {
        query: trimmedQuery,
        chunksRetrieved: chunks.length,
        chunksUsed: citationResult.stats.matched,
        model: llmResult.model,
        usage: llmResult.usage,
        latency: metrics,
      },
    };

    logger.info('Pipeline completed', {
      query: trimmedQuery.substring(0, 50),
      chunks: chunks.length,
      confidence: confidence.level,
      totalMs: metrics.totalMs,
    });

    return response;

  } catch (error) {
    metrics.totalMs = Date.now() - startTime;
    logger.error('Pipeline failed', {
      query: query?.substring(0, 50),
      error: error.message,
      totalMs: metrics.totalMs,
    });

    throw new Error(`Pipeline error: ${error.message}`);
  }
}

/**
 * Build response when no relevant chunks are found.
 *
 * @param {string} query - Original query
 * @param {Object} metrics - Timing metrics
 * @param {number} startTime - Pipeline start time
 * @returns {Object} No results response
 */
function buildNoResultsResponse(query, metrics, startTime) {
  metrics.totalMs = Date.now() - startTime;

  return {
    answer: "I don't have specific information about that topic in my knowledge base. Please try rephrasing your question or contact our customer service team for assistance.",
    citations: [],
    sourcesMarkdown: '',
    confidence: {
      level: 'Low',
      reason: 'No relevant documents found',
    },
    metadata: {
      query,
      chunksRetrieved: 0,
      chunksUsed: 0,
      model: null,
      usage: null,
      latency: metrics,
    },
  };
}

/**
 * Calculate confidence level based on retrieval and citation results.
 *
 * @param {Array} chunks - Retrieved chunks
 * @param {Object} citationResult - Citation processing result
 * @returns {Object} Confidence level and reason
 */
export function calculateConfidence(chunks, citationResult) {
  const avgScore = chunks.reduce((sum, c) => sum + c.score, 0) / chunks.length;
  const matchedCitations = citationResult.stats.matched;

  // High confidence: 3+ chunks with good scores and citations match
  if (chunks.length >= 3 && avgScore >= 0.7 && matchedCitations >= 2) {
    return {
      level: 'High',
      reason: `${chunks.length} relevant sources with ${matchedCitations} citations`,
    };
  }

  // Medium confidence: Some chunks found with decent scores
  if (chunks.length >= 2 && avgScore >= 0.5) {
    return {
      level: 'Medium',
      reason: `${chunks.length} sources found, average relevance ${(avgScore * 100).toFixed(0)}%`,
    };
  }

  // Low confidence: Few chunks or low scores
  return {
    level: 'Low',
    reason: chunks.length === 1
      ? 'Only 1 source found'
      : `Low relevance scores (avg ${(avgScore * 100).toFixed(0)}%)`,
  };
}

/**
 * Format context from chunks (re-export for convenience).
 */
export { formatContext } from './retrieval.js';
```

**tests/pipeline.test.js**:
```javascript
/**
 * Pipeline Orchestrator Tests
 */

import { jest } from '@jest/globals';

// Mock all dependent services
jest.unstable_mockModule('./retrieval.js', () => ({
  retrieveChunks: jest.fn(),
  formatContext: jest.fn(),
  getMetadataForCitation: jest.fn(),
}));

jest.unstable_mockModule('./llm.js', () => ({
  generateResponse: jest.fn(),
}));

jest.unstable_mockModule('./citations.js', () => ({
  processCitations: jest.fn(),
}));

const { processQuery, calculateConfidence } = await import('../src/services/pipeline.js');
const { retrieveChunks, formatContext } = await import('../src/services/retrieval.js');
const { generateResponse } = await import('../src/services/llm.js');
const { processCitations } = await import('../src/services/citations.js');

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
      expect(result.metadata.latency.totalMs).toBeGreaterThan(0);
    });

    test('propagates retrieval errors', async () => {
      retrieveChunks.mockRejectedValue(new Error('ChromaDB unavailable'));

      await expect(processQuery('Test')).rejects.toThrow('Pipeline error: ChromaDB unavailable');
    });

    test('propagates LLM errors', async () => {
      generateResponse.mockRejectedValue(new Error('Groq API error'));

      await expect(processQuery('Test')).rejects.toThrow('Pipeline error: Groq API error');
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
    });

    test('returns Medium for decent results', () => {
      const chunks = [
        { score: 0.6 },
        { score: 0.5 },
      ];
      const citationResult = { stats: { matched: 1 } };

      const confidence = calculateConfidence(chunks, citationResult);

      expect(confidence.level).toBe('Medium');
    });

    test('returns Low for poor results', () => {
      const chunks = [{ score: 0.3 }];
      const citationResult = { stats: { matched: 0 } };

      const confidence = calculateConfidence(chunks, citationResult);

      expect(confidence.level).toBe('Low');
    });

    test('includes reason in confidence', () => {
      const chunks = [{ score: 0.9 }];
      const citationResult = { stats: { matched: 1 } };

      const confidence = calculateConfidence(chunks, citationResult);

      expect(confidence.reason).toBeDefined();
      expect(typeof confidence.reason).toBe('string');
    });
  });
});
```

### Constraints
- Use ES modules (import/export)
- Do not modify the existing service modules
- Handle all errors gracefully with informative messages
- Log all pipeline stages with timing

### Acceptance Criteria
- [ ] `src/services/pipeline.js` implements `processQuery`
- [ ] Pipeline calls retrieval → LLM → citation services in order
- [ ] Returns structured response with answer, citations, confidence, metadata
- [ ] Handles no-results case gracefully
- [ ] Calculates confidence level (High/Medium/Low)
- [ ] Includes latency metrics for each stage
- [ ] All tests pass: `npm test -- --testPathPattern=pipeline`

### TDD Requirements
- [ ] Write tests first with mocked services
- [ ] Implement functions to pass tests
- [ ] Run `npm test` to verify all pass

---

## Format

### Output Structure
- `src/services/pipeline.js` - Full implementation
- `tests/pipeline.test.js` - Complete test file
- Update `src/services/index.js` to export `processQuery`

### Response Format
```json
{
  "answer": "For Singapore export, you need...",
  "citations": [
    {
      "title": "Singapore Export Guide",
      "section": "Required Documents",
      "sourceUrls": ["https://..."],
      "matched": true
    }
  ],
  "sourcesMarkdown": "**Sources:**\n1. [Singapore Export Guide](https://...)",
  "confidence": {
    "level": "High",
    "reason": "3 relevant sources with 2 citations"
  },
  "metadata": {
    "query": "What documents for Singapore export?",
    "chunksRetrieved": 5,
    "chunksUsed": 3,
    "model": "llama-3.1-8b-instant",
    "usage": {
      "promptTokens": 450,
      "completionTokens": 120
    },
    "latency": {
      "retrievalMs": 150,
      "generationMs": 800,
      "citationMs": 5,
      "totalMs": 960
    }
  }
}
```

### Validation Commands

```bash
cd pilot_phase1_poc/03_rag_pipeline

# Run pipeline tests only
npm test -- --testPathPattern=pipeline

# Run all tests
npm test

# Manual integration test
node -e "
  import('./src/services/pipeline.js').then(async ({ processQuery }) => {
    const result = await processQuery('What documents for Singapore export?');
    console.log('Answer:', result.answer.substring(0, 200));
    console.log('Confidence:', result.confidence);
    console.log('Latency:', result.metadata.latency);
  });
"
```

### Expected Test Output
```
PASS tests/pipeline.test.js
  Pipeline Orchestrator
    processQuery
      ✓ processes query through full pipeline
      ✓ returns structured response with all fields
      ✓ handles no chunks found
      ✓ throws on empty query
      ✓ throws on invalid query type
      ✓ includes latency metrics
      ✓ propagates retrieval errors
      ✓ propagates LLM errors
    calculateConfidence
      ✓ returns High for many good chunks with citations
      ✓ returns Medium for decent results
      ✓ returns Low for poor results
      ✓ includes reason in confidence

Test Suites: 1 passed, 1 total
Tests:       12 passed, 12 total
```
