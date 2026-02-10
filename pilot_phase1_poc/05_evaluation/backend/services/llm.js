/**
 * LLM Service
 * Handles API calls to Groq for response generation.
 */

import OpenAI from 'openai';
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { config } from '../config.js';
import { logger } from '../utils/logger.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Singleton client instance
let openaiClient = null;

// System prompt template cache
let systemPromptTemplate = null;
const SYSTEM_PROMPT_PATH = join(__dirname, '..', 'prompts', 'system.txt');

/**
 * Load system prompt template from file.
 * Caches the template for reuse.
 *
 * @returns {string} System prompt template
 */
export function loadSystemPrompt() {
  if (!systemPromptTemplate) {
    systemPromptTemplate = readFileSync(SYSTEM_PROMPT_PATH, 'utf-8');
  }
  return systemPromptTemplate;
}

/**
 * Reset the cached system prompt template. Used in tests to force re-load.
 * @returns {void}
 */
export function resetSystemPrompt() {
  systemPromptTemplate = null;
}

/**
 * Initialize OpenAI-compatible client for Groq.
 *
 * @returns {OpenAI} OpenAI client configured for Groq
 */
export function initLLMClient() {
  if (openaiClient) return openaiClient;

  if (!config.llmApiKey) {
    throw new Error('LLM_API_KEY environment variable is required');
  }

  openaiClient = new OpenAI({
    apiKey: config.llmApiKey,
    baseURL: config.llmBaseUrl,
  });

  logger.info('LLM client initialized', {
    provider: config.llmProvider,
    model: config.llmModel,
    baseUrl: config.llmBaseUrl,
  });

  return openaiClient;
}

/**
 * Reset the LLM client instance. Used in tests to force re-initialization.
 * @returns {void}
 */
export function resetLLMClient() {
  openaiClient = null;
}

/**
 * Generate a response using the LLM.
 *
 * @param {string} query - The customer's question
 * @param {string} context - Formatted context from retrieved chunks
 * @param {Object} options - Generation options
 * @param {string} options.systemPrompt - Custom system prompt (optional)
 * @param {number} options.maxRetries - Max retry attempts (default: 3)
 * @returns {Promise<Object>} Generated response with metadata
 * @throws {Error} If generation fails after retries
 */
export async function generateResponse(query, context, options = {}) {
  const client = initLLMClient();
  const maxRetries = options.maxRetries ?? 3;

  const systemPrompt = options.systemPrompt || buildSystemPrompt(context);
  const userMessage = query;

  const messages = [
    { role: 'system', content: systemPrompt },
    { role: 'user', content: userMessage },
  ];

  let lastError = null;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const startTime = Date.now();

      const completion = await client.chat.completions.create({
        model: config.llmModel,
        messages,
        temperature: config.llmTemperature,
        max_tokens: config.llmMaxTokens,
      });

      const elapsed = Date.now() - startTime;

      const result = parseCompletion(completion);

      logger.info('LLM response generated', {
        model: config.llmModel,
        latencyMs: elapsed,
        promptTokens: result.usage.promptTokens,
        completionTokens: result.usage.completionTokens,
      });

      return result;
    } catch (error) {
      lastError = error;
      const shouldRetry = isRetryableError(error) && attempt < maxRetries;

      logger.warn('LLM request failed', {
        attempt,
        maxRetries,
        error: error.message,
        willRetry: shouldRetry,
      });

      if (shouldRetry) {
        const delay = calculateBackoff(attempt);
        await sleep(delay);
      }
    }
  }

  logger.error('LLM request failed after retries', {
    error: lastError.message,
    maxRetries,
  });

  throw new Error(`LLM request failed: ${lastError.message}`);
}

/**
 * Build system prompt with context.
 *
 * @param {string} context - Retrieved context
 * @returns {string} Complete system prompt
 */
export function buildSystemPrompt(context) {
  const template = loadSystemPrompt();
  return template.replace('{context}', context);
}

/**
 * Parse completion response into structured format.
 *
 * @param {Object} completion - OpenAI completion response
 * @returns {Object} Parsed response
 */
export function parseCompletion(completion) {
  const choice = completion.choices?.[0];

  if (!choice) {
    throw new Error('No completion choice returned');
  }

  return {
    answer: choice.message?.content || '',
    finishReason: choice.finish_reason,
    usage: {
      promptTokens: completion.usage?.prompt_tokens || 0,
      completionTokens: completion.usage?.completion_tokens || 0,
      totalTokens: completion.usage?.total_tokens || 0,
    },
    model: completion.model,
  };
}

/**
 * Check if error is retryable.
 *
 * @param {Error} error - Error object
 * @returns {boolean} Whether to retry
 */
export function isRetryableError(error) {
  // Rate limit errors
  if (error.status === 429) return true;

  // Server errors
  if (error.status >= 500 && error.status < 600) return true;

  // Network errors
  if (error.code === 'ECONNRESET' || error.code === 'ETIMEDOUT') return true;

  return false;
}

/**
 * Calculate exponential backoff with jitter.
 *
 * @param {number} attempt - Current attempt number (1-based)
 * @returns {number} Delay in milliseconds
 */
export function calculateBackoff(attempt) {
  const baseDelay = 1000; // 1 second
  const maxDelay = 10000; // 10 seconds

  // Exponential backoff: 1s, 2s, 4s...
  const exponentialDelay = baseDelay * Math.pow(2, attempt - 1);

  // Add jitter (0-25% of delay)
  const jitter = Math.random() * 0.25 * exponentialDelay;

  return Math.min(exponentialDelay + jitter, maxDelay);
}

/**
 * Sleep for specified milliseconds.
 *
 * @param {number} ms - Milliseconds to sleep
 * @returns {Promise<void>}
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
