/**
 * ChromaDB Retrieval Service
 * Handles vector similarity search against the knowledge base.
 *
 * Uses Python subprocess to query ChromaDB (since JS client requires a server).
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { config } from '../config.js';
import { logger } from '../utils/logger.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Path to Python query script
const QUERY_SCRIPT = join(__dirname, '..', '..', 'scripts', 'query_chroma.py');

// Path to Python venv
const PYTHON_PATH = join(__dirname, '..', '..', 'venv', 'Scripts', 'python.exe');

/**
 * Execute Python script for ChromaDB query.
 *
 * @param {Object} params - Query parameters
 * @returns {Promise<Object>} Query results
 */
async function executePythonQuery(params) {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();

    // Try venv python first, fall back to system python
    const pythonPaths = [PYTHON_PATH, 'python', 'python3', 'py'];
    let pythonCmd = pythonPaths[0];

    // Check if we're in test environment (mocked)
    if (process.env.NODE_ENV === 'test') {
      reject(new Error('Python bridge not available in test environment'));
      return;
    }

    const proc = spawn(pythonCmd, [QUERY_SCRIPT], {
      stdio: ['pipe', 'pipe', 'pipe'],
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    proc.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    proc.on('close', (code) => {
      const elapsed = Date.now() - startTime;

      if (code !== 0) {
        logger.error('Python query failed', { code, stderr, latencyMs: elapsed });
        reject(new Error(`Python query failed: ${stderr || 'Unknown error'}`));
        return;
      }

      try {
        const result = JSON.parse(stdout);
        logger.debug('Python query completed', { latencyMs: elapsed });

        if (!result.success) {
          reject(new Error(result.error || 'Query failed'));
          return;
        }

        resolve(result);
      } catch (e) {
        logger.error('Failed to parse Python output', { stdout, error: e.message });
        reject(new Error(`Failed to parse query result: ${e.message}`));
      }
    });

    proc.on('error', (err) => {
      logger.error('Failed to spawn Python process', { error: err.message });
      reject(new Error(`Failed to execute Python: ${err.message}`));
    });

    // Send query parameters to stdin
    proc.stdin.write(JSON.stringify(params));
    proc.stdin.end();
  });
}

/**
 * Initialize ChromaDB client (no-op for Python bridge, kept for interface compatibility).
 *
 * @returns {Promise<boolean>} Always returns true
 */
export async function initChromaClient() {
  logger.info('ChromaDB bridge ready (Python subprocess)');
  return true;
}

/**
 * Reset the ChromaDB client instance (no-op for Python bridge). Used in tests.
 * @returns {void}
 */
export function resetClient() {
  // No-op for Python bridge
}

/**
 * Retrieve relevant chunks from ChromaDB.
 *
 * @param {string} query - The search query
 * @param {Object} options - Retrieval options
 * @param {number} options.topK - Number of results to return (default from config)
 * @param {number} options.threshold - Minimum relevance score (default from config)
 * @returns {Promise<Array>} Retrieved chunks with metadata and scores
 * @throws {Error} If retrieval fails
 */
export async function retrieveChunks(query, options = {}) {
  const topK = options.topK ?? config.retrievalTopK;
  const threshold = options.threshold ?? config.relevanceThreshold;

  const startTime = Date.now();

  try {
    const result = await executePythonQuery({
      query,
      top_k: topK,
      collection_name: config.collectionName,
    });

    const chunks = result.chunks || [];

    // Filter by threshold
    const filtered = filterByThreshold(chunks, threshold);

    const elapsed = Date.now() - startTime;
    logger.info('Chunks retrieved', {
      query: query.substring(0, 50),
      retrieved: chunks.length,
      afterFilter: filtered.length,
      threshold,
      latencyMs: elapsed,
    });

    return filtered;
  } catch (error) {
    logger.error('Retrieval failed', { query, error: error.message });
    throw new Error(`Retrieval failed: ${error.message}`);
  }
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
    const title = chunk.metadata?.title || 'Unknown Document';
    const section = chunk.metadata?.section || '';
    const header = section ? `[${title} > ${section}]` : `[${title}]`;
    const entry = `${header}\n${chunk.content}\n\n`;

    if (charCount + entry.length > maxChars) {
      logger.debug('Context truncated', { charCount, maxChars, chunksIncluded: chunks.indexOf(chunk) });
      break;
    }

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
    title: chunk.metadata?.title || 'Unknown',
    section: chunk.metadata?.section || null,
    sourceUrls: chunk.metadata?.source_urls?.split(',').filter(Boolean) || [],
    docId: chunk.metadata?.doc_id || null,
    score: chunk.score,
  }));
}
