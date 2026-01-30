/**
 * RAG Pipeline Orchestrator
 * Coordinates the retrieval-augmented generation flow.
 */

import { retrieveChunks } from './retrieval.js';
import { generateResponse } from './llm.js';
import { logger } from '../utils/logger.js';

/**
 * Process a customer query through the RAG pipeline.
 *
 * @param {string} query - The customer's question
 * @returns {Promise<Object>} Response with answer, sources, and metadata
 * @throws {Error} If processing fails
 */
export async function processQuery(query) {
  // TODO: Implement in Task 5.1
  throw new Error('Not implemented: processQuery');
}

/**
 * Format retrieved chunks into context for the LLM.
 *
 * @param {Array} chunks - Retrieved chunks with metadata
 * @returns {string} Formatted context string
 */
export function formatContext(chunks) {
  // TODO: Implement in Task 5.1
  throw new Error('Not implemented: formatContext');
}
