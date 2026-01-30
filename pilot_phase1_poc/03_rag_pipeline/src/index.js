/**
 * Waypoint RAG Pipeline API
 *
 * Express server that provides the /api/query endpoint
 * for the customer service co-pilot.
 */

import express from 'express';
import cors from 'cors';
import { config } from './config.js';
import { queryRouter } from './routes/index.js';

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api', queryRouter);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start server
const PORT = config.port;
app.listen(PORT, () => {
  console.log(`Waypoint RAG Pipeline running on port ${PORT}`);
});

export default app;
