/**
 * Health check endpoint
 */

import { Router } from 'express';

const router = Router();
const startTime = Date.now();

/**
 * GET /api/health
 * Returns server health status.
 */
router.get('/', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: Math.floor((Date.now() - startTime) / 1000),
    version: process.env.npm_package_version || '1.0.0',
  });
});

export default router;
