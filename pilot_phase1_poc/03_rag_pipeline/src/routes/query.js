/**
 * Query endpoint routes
 * Handles POST /api/query for RAG pipeline queries.
 */

import { Router } from 'express';
import { processQuery } from '../services/index.js';

const router = Router();

/**
 * POST /api/query
 * Process a customer service query through the RAG pipeline.
 *
 * @param {Object} req.body - Request body
 * @param {string} req.body.query - The customer query text
 * @returns {Object} Response with answer, sources, and metadata
 */
router.post('/', async (req, res) => {
  try {
    const { query } = req.body;

    if (!query || typeof query !== 'string') {
      return res.status(400).json({
        error: 'Invalid request',
        message: 'Query parameter is required and must be a string',
      });
    }

    const result = await processQuery(query);
    res.json(result);
  } catch (error) {
    console.error('Query processing error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: error.message,
    });
  }
});

export default router;
