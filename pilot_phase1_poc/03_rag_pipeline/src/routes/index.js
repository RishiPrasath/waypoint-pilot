/**
 * Route aggregator
 * Exports all API routes for the application.
 */

import { Router } from 'express';
import queryRoutes from './query.js';

const router = Router();

// Mount query routes
router.use('/query', queryRoutes);

export { router as queryRouter };
