/**
 * Route aggregator
 * Exports all API routes for the application.
 */

import { Router } from 'express';
import queryRoutes from './query.js';
import healthRoutes from './health.js';

const router = Router();

// Mount routes
router.use('/query', queryRoutes);
router.use('/health', healthRoutes);

export { router as apiRouter };
