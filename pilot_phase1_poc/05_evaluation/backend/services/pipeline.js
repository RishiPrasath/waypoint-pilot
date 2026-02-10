/**
 * RAG Pipeline Orchestrator
 * Coordinates the retrieval-augmented generation flow.
 */

import { retrieveChunks, formatContext } from './retrieval.js';
import { generateResponse } from './llm.js';
import { processCitations, buildSources, buildRelatedDocs } from './citations.js';
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
      sources: buildSources(citationResult.citations, chunks),
      relatedDocs: buildRelatedDocs(chunks),
      citations: citationResult.citations.filter(c => c.matched),
      confidence,
      metadata: {
        query: trimmedQuery,
        chunksRetrieved: chunks.length,
        chunksUsed: citationResult.stats.matched,
        latencyMs: metrics.totalMs,
        model: llmResult.model,
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
    sources: [],
    relatedDocs: [],
    citations: [],
    confidence: {
      level: 'Low',
      reason: 'No relevant documents found',
    },
    metadata: {
      query,
      chunksRetrieved: 0,
      chunksUsed: 0,
      latencyMs: metrics.totalMs,
      model: null,
    },
  };
}

/**
 * Calculate confidence level based on retrieval and citation results.
 * Updated thresholds for better calibration based on E2E test findings.
 *
 * @param {Array} chunks - Retrieved chunks
 * @param {Object} citationResult - Citation processing result
 * @returns {Object} Confidence level and reason
 */
export function calculateConfidence(chunks, citationResult) {
  const avgScore = chunks.reduce((sum, c) => sum + c.score, 0) / chunks.length;
  const matchedCitations = citationResult.stats.matched;

  // High confidence: 3+ chunks with good scores (citations optional)
  // Lowered avgScore threshold from 0.6 to 0.5 — no queries achieved High in Round 2
  if (chunks.length >= 3 && avgScore >= 0.5) {
    const citationInfo = matchedCitations > 0 ? ` with ${matchedCitations} citations` : '';
    return {
      level: 'High',
      reason: `${chunks.length} relevant sources${citationInfo}`,
    };
  }

  // Medium confidence: 2+ chunks with decent scores
  // Lowered avgScore threshold from 0.4 to 0.3 for better citation behavior
  if (chunks.length >= 2 && avgScore >= 0.3) {
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
