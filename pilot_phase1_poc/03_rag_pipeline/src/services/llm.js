/**
 * LLM Service
 * Handles API calls to Groq for response generation.
 */

import OpenAI from 'openai';
import { config } from '../config.js';
import { logger } from '../utils/logger.js';

// Singleton client instance
let openaiClient = null;

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
 * Reset client (for testing).
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
  return `You are a helpful customer service assistant for a freight forwarding company in Singapore.

Your role is to answer questions about:
- Shipment booking procedures and documentation requirements
- Customs regulations (Singapore and Southeast Asia)
- Carrier information and services
- Service terms, SLAs, and policies

IMPORTANT GUIDELINES:
1. Only answer questions based on the provided context
2. Always cite your sources when providing information
3. If the information is not in the context, say "I don't have information about that in my knowledge base"
4. Be concise and professional
5. Do not make up information or provide speculative answers

OUT OF SCOPE (politely decline these):
- Real-time shipment tracking
- Live freight rates and quotes
- Booking modifications or reservations
- Account-specific information
- Weather or market predictions

Context from knowledge base:
${context}`;
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
