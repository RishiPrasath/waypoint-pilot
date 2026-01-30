# Task 5.1: Create LLM Service

## Persona

> You are a backend developer with expertise in LLM integrations and API design.
> You follow TDD principles and create robust, well-tested code with proper error handling.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. The retrieval service is complete (Task 4.1). Now we implement the LLM service that calls Groq API to generate responses based on retrieved context.

### Current State
- Retrieval service complete: `src/services/retrieval.js`
- ChromaDB returns chunks with 0.15+ relevance scores
- System prompt placeholder at `src/prompts/system.txt`
- No LLM integration implemented yet

### Reference Documents
- `03_rag_pipeline/docs/00_week2_rag_pipeline_plan.md` - Architecture details
- `03_rag_pipeline/docs/01_implementation_roadmap.md` - Task specifications
- `03_rag_pipeline/src/services/llm.js` - Placeholder to implement

### Dependencies
- Task 4.1: Create Retrieval Service Module ✅

### MCP Tools Available
If you need documentation for OpenAI SDK or Groq:
```
mcp__context7__resolve-library-id: Find library ID for documentation lookup
mcp__context7__query-docs: Query library documentation
```

---

## Task

### Objective
Implement the LLM service that generates responses using Groq API (via OpenAI-compatible SDK) with proper error handling, retry logic, and response parsing.

### Requirements

1. **Initialize OpenAI Client for Groq**
   - Use `openai` npm package with Groq base URL
   - Configure from environment variables
   - Singleton pattern for client reuse

2. **Implement `generateResponse` function**
   - Accept query, context, and optional system prompt
   - Call Groq API with chat completions
   - Return structured response with answer and usage stats
   - Handle rate limits and errors gracefully

3. **Implement retry logic**
   - Retry on transient errors (429, 500, 503)
   - Exponential backoff with jitter
   - Max 3 retries

4. **Create response parser**
   - Extract answer from completion
   - Parse usage statistics
   - Handle malformed responses

5. **Write comprehensive tests**
   - Mock OpenAI client for unit tests
   - Test error handling scenarios
   - Test retry logic

### Specifications

**src/services/llm.js**:
```javascript
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
```

**tests/llm.test.js**:
```javascript
/**
 * LLM Service Tests
 */

import { jest } from '@jest/globals';
import {
  buildSystemPrompt,
  parseCompletion,
  isRetryableError,
  calculateBackoff,
} from '../src/services/llm.js';

describe('LLM Service', () => {
  describe('buildSystemPrompt', () => {
    test('includes context in prompt', () => {
      const context = 'Test context about exports';
      const prompt = buildSystemPrompt(context);

      expect(prompt).toContain('Test context about exports');
      expect(prompt).toContain('customer service assistant');
      expect(prompt).toContain('freight forwarding');
    });

    test('includes guidelines', () => {
      const prompt = buildSystemPrompt('context');

      expect(prompt).toContain('cite your sources');
      expect(prompt).toContain('OUT OF SCOPE');
    });
  });

  describe('parseCompletion', () => {
    test('parses valid completion', () => {
      const completion = {
        choices: [{
          message: { content: 'Test answer' },
          finish_reason: 'stop',
        }],
        usage: {
          prompt_tokens: 100,
          completion_tokens: 50,
          total_tokens: 150,
        },
        model: 'llama-3.1-8b-instant',
      };

      const result = parseCompletion(completion);

      expect(result.answer).toBe('Test answer');
      expect(result.finishReason).toBe('stop');
      expect(result.usage.promptTokens).toBe(100);
      expect(result.usage.completionTokens).toBe(50);
      expect(result.model).toBe('llama-3.1-8b-instant');
    });

    test('throws on missing choices', () => {
      const completion = { choices: [] };

      expect(() => parseCompletion(completion)).toThrow('No completion choice');
    });

    test('handles missing usage stats', () => {
      const completion = {
        choices: [{ message: { content: 'Answer' }, finish_reason: 'stop' }],
      };

      const result = parseCompletion(completion);

      expect(result.usage.promptTokens).toBe(0);
      expect(result.usage.completionTokens).toBe(0);
    });
  });

  describe('isRetryableError', () => {
    test('retries on rate limit (429)', () => {
      expect(isRetryableError({ status: 429 })).toBe(true);
    });

    test('retries on server errors (5xx)', () => {
      expect(isRetryableError({ status: 500 })).toBe(true);
      expect(isRetryableError({ status: 503 })).toBe(true);
    });

    test('retries on network errors', () => {
      expect(isRetryableError({ code: 'ECONNRESET' })).toBe(true);
      expect(isRetryableError({ code: 'ETIMEDOUT' })).toBe(true);
    });

    test('does not retry on client errors', () => {
      expect(isRetryableError({ status: 400 })).toBe(false);
      expect(isRetryableError({ status: 401 })).toBe(false);
    });
  });

  describe('calculateBackoff', () => {
    test('increases with attempts', () => {
      const delay1 = calculateBackoff(1);
      const delay2 = calculateBackoff(2);
      const delay3 = calculateBackoff(3);

      // Base delays before jitter: 1000, 2000, 4000
      expect(delay1).toBeGreaterThanOrEqual(1000);
      expect(delay1).toBeLessThanOrEqual(1250); // with 25% jitter

      expect(delay2).toBeGreaterThanOrEqual(2000);
      expect(delay3).toBeGreaterThanOrEqual(4000);
    });

    test('caps at max delay', () => {
      const delay = calculateBackoff(10); // Would be 512s without cap
      expect(delay).toBeLessThanOrEqual(12500); // 10s + 25% jitter
    });
  });
});
```

### Constraints
- Use ES modules (import/export)
- Use OpenAI npm package with Groq base URL
- Do not hardcode API keys
- Log all API calls with timing
- Handle all error cases gracefully

### Acceptance Criteria
- [ ] `src/services/llm.js` implements all functions
- [ ] OpenAI client configured for Groq
- [ ] `generateResponse` returns structured response
- [ ] Retry logic with exponential backoff
- [ ] `buildSystemPrompt` creates complete prompt
- [ ] `parseCompletion` handles all response formats
- [ ] All tests pass: `npm test -- --testPathPattern=llm`

### TDD Requirements
- [ ] Write tests first
- [ ] Implement functions to pass tests
- [ ] Run `npm test` to verify all pass

---

## Format

### Output Structure
- `src/services/llm.js` - Full implementation
- `tests/llm.test.js` - Complete test file

### Code Style
- ES modules (import/export)
- JSDoc comments for all exported functions
- camelCase for variables/functions
- 2-space indentation
- Async/await for all async operations

### Validation Commands

```bash
cd pilot_phase1_poc/03_rag_pipeline

# Run LLM tests only
npm test -- --testPathPattern=llm

# Manual test (requires GROQ API key in .env)
node -e "
  import('./src/services/llm.js').then(async ({ generateResponse }) => {
    const response = await generateResponse(
      'What documents are needed for export?',
      '[Singapore Export] Commercial invoice required.'
    );
    console.log('Answer:', response.answer.substring(0, 200));
    console.log('Tokens:', response.usage);
  });
"
```

### Expected Test Output
```
PASS tests/llm.test.js
  LLM Service
    buildSystemPrompt
      ✓ includes context in prompt
      ✓ includes guidelines
    parseCompletion
      ✓ parses valid completion
      ✓ throws on missing choices
      ✓ handles missing usage stats
    isRetryableError
      ✓ retries on rate limit (429)
      ✓ retries on server errors (5xx)
      ✓ retries on network errors
      ✓ does not retry on client errors
    calculateBackoff
      ✓ increases with attempts
      ✓ caps at max delay

Test Suites: 1 passed, 1 total
Tests:       11 passed, 11 total
```
