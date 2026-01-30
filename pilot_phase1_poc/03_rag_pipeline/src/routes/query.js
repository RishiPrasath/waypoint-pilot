/**
 * Query endpoint routes
 * Handles POST /api/query for RAG pipeline queries.
 */

import { Router } from 'express';
import { processQuery } from '../services/pipeline.js';
import { logger } from '../utils/logger.js';

const router = Router();

/**
 * POST /api/query
 * Process a customer service query through the RAG pipeline.
 *
 * @body {string} query - The customer query text
 * @returns {Object} Response with answer, citations, confidence, metadata
 */
router.post('/', async (req, res, next) => {
  const startTime = Date.now();

  try {
    const { query } = req.body;

    // Validate request
    if (!query || typeof query !== 'string') {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'Query parameter is required and must be a string',
      });
    }

    if (query.trim().length === 0) {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'Query cannot be empty',
      });
    }

    if (query.length > 1000) {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'Query exceeds maximum length of 1000 characters',
      });
    }

    // Process query through pipeline
    const result = await processQuery(query);

    // Log successful request
    logger.info('Query processed via API', {
      queryLength: query.length,
      confidence: result.confidence.level,
      latencyMs: Date.now() - startTime,
    });

    res.json(result);

  } catch (error) {
    next(error);
  }
});

export default router;
