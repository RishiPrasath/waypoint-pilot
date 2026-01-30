/**
 * Embedding Service
 * Generates query embeddings using Python subprocess (ChromaDB default model).
 */

import { config } from '../config.js';
import { logger } from '../utils/logger.js';

/**
 * Generate embedding for a query using Python subprocess.
 *
 * @param {string} query - The text to embed
 * @returns {Promise<Array<number>>} 384-dimensional embedding vector
 * @throws {Error} If embedding generation fails
 */
export async function getQueryEmbedding(query) {
  // TODO: Implement in Task 4.1 or use ChromaDB's built-in embedding
  throw new Error('Not implemented: getQueryEmbedding');
}

/**
 * Batch embed multiple queries.
 *
 * @param {Array<string>} queries - Array of texts to embed
 * @returns {Promise<Array<Array<number>>>} Array of embedding vectors
 * @throws {Error} If embedding generation fails
 */
export async function batchEmbed(queries) {
  // TODO: Implement if needed
  throw new Error('Not implemented: batchEmbed');
}
