/**
 * Configuration module
 * Loads environment variables and exports typed config object.
 */

import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load .env from project root
dotenv.config({ path: join(__dirname, '..', '.env') });

export const config = {
  // Server
  port: parseInt(process.env.PORT || '3000', 10),
  nodeEnv: process.env.NODE_ENV || 'development',

  // ChromaDB
  chromaPath: process.env.CHROMA_PATH || './chroma_db',
  collectionName: process.env.COLLECTION_NAME || 'waypoint_kb',

  // Retrieval
  retrievalTopK: parseInt(process.env.RETRIEVAL_TOP_K || '10', 10),
  relevanceThreshold: parseFloat(process.env.RELEVANCE_THRESHOLD || '0.15'),
  maxContextTokens: parseInt(process.env.MAX_CONTEXT_TOKENS || '2000', 10),

  // LLM
  llmProvider: process.env.LLM_PROVIDER || 'groq',
  llmApiKey: process.env.LLM_API_KEY,
  llmBaseUrl: process.env.LLM_BASE_URL || 'https://api.groq.com/openai/v1',
  llmModel: process.env.LLM_MODEL || 'llama-3.1-8b-instant',
  llmTemperature: parseFloat(process.env.LLM_TEMPERATURE || '0.3'),
  llmMaxTokens: parseInt(process.env.LLM_MAX_TOKENS || '500', 10),
};
