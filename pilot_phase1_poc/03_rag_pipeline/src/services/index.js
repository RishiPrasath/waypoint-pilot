/**
 * Service exports
 * Central export point for all service modules.
 */

export { processQuery, calculateConfidence } from './pipeline.js';
export { retrieveChunks } from './retrieval.js';
export { generateResponse } from './llm.js';
export { getQueryEmbedding } from './embedding.js';
export {
  extractCitations,
  matchCitationToChunk,
  enrichCitations,
  formatCitationsMarkdown,
  deduplicateCitations,
  processCitations,
  similarity,
} from './citations.js';
