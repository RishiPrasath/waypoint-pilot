/**
 * Waypoint RAG Pipeline API
 *
 * Express server that provides the /api/query endpoint
 * for the customer service co-pilot.
 */

import express from 'express';
import cors from 'cors';
import { config } from './config.js';
import { apiRouter } from './routes/index.js';
import { errorHandler, notFoundHandler } from './middleware/errorHandler.js';
import { logger } from './utils/logger.js';

const app = express();

// Middleware
app.use(cors());
app.use(express.json({ limit: '10kb' }));

// Request logging (optional)
app.use((req, res, next) => {
  if (req.path !== '/api/health') {
    logger.debug('Incoming request', {
      method: req.method,
      path: req.path,
    });
  }
  next();
});

// Routes
app.use('/api', apiRouter);

// Error handling
app.use(notFoundHandler);
app.use(errorHandler);

// Start server only when run directly (not imported for testing)
const PORT = config.port;
let server;

if (process.env.NODE_ENV !== 'test') {
  server = app.listen(PORT, () => {
    logger.info('Server started', {
      port: PORT,
      env: config.nodeEnv,
    });
  });

  // Graceful shutdown
  process.on('SIGTERM', () => {
    logger.info('SIGTERM received, shutting down gracefully');
    server.close(() => {
      logger.info('Server closed');
      process.exit(0);
    });
  });
}

export default app;
