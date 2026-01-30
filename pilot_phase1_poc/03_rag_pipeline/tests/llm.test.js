/**
 * LLM Service Tests
 */

import { jest } from '@jest/globals';
import {
  loadSystemPrompt,
  buildSystemPrompt,
  parseCompletion,
  isRetryableError,
  calculateBackoff,
  resetLLMClient,
  resetSystemPrompt,
} from '../src/services/llm.js';

describe('LLM Service', () => {
  beforeEach(() => {
    resetLLMClient();
    resetSystemPrompt();
  });

  describe('loadSystemPrompt', () => {
    test('returns non-empty string', () => {
      const prompt = loadSystemPrompt();
      expect(typeof prompt).toBe('string');
      expect(prompt.length).toBeGreaterThan(0);
    });

    test('contains expected sections', () => {
      const prompt = loadSystemPrompt();
      expect(prompt).toContain('Your Role');
      expect(prompt).toContain('Response Guidelines');
      expect(prompt).toContain('Cite Your Sources');
      expect(prompt).toContain('Out of Scope');
    });

    test('contains context placeholder', () => {
      const prompt = loadSystemPrompt();
      expect(prompt).toContain('{context}');
    });

    test('caches the template', () => {
      const prompt1 = loadSystemPrompt();
      const prompt2 = loadSystemPrompt();
      expect(prompt1).toBe(prompt2);
    });

    test('reset clears the cache', () => {
      const prompt1 = loadSystemPrompt();
      resetSystemPrompt();
      const prompt2 = loadSystemPrompt();
      expect(prompt1).toBe(prompt2); // Content should be same
    });
  });

  describe('buildSystemPrompt', () => {
    test('replaces context placeholder', () => {
      const context = 'Test context about exports';
      const prompt = buildSystemPrompt(context);

      expect(prompt).toContain('Test context about exports');
      expect(prompt).not.toContain('{context}');
    });

    test('includes guidelines from file', () => {
      const prompt = buildSystemPrompt('test context');

      expect(prompt).toContain('customer service assistant');
      expect(prompt).toContain('Cite Your Sources');
      expect(prompt).toContain('Out of Scope');
    });

    test('includes context in correct location', () => {
      const context = 'Singapore Export Procedures content';
      const prompt = buildSystemPrompt(context);

      expect(prompt).toContain('KNOWLEDGE BASE CONTEXT:');
      expect(prompt).toContain('Singapore Export Procedures content');
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
      expect(result.usage.totalTokens).toBe(150);
      expect(result.model).toBe('llama-3.1-8b-instant');
    });

    test('throws on missing choices', () => {
      const completion = { choices: [] };

      expect(() => parseCompletion(completion)).toThrow('No completion choice');
    });

    test('throws on undefined choices', () => {
      const completion = {};

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

    test('handles empty message content', () => {
      const completion = {
        choices: [{ message: {}, finish_reason: 'stop' }],
        usage: { prompt_tokens: 10, completion_tokens: 0, total_tokens: 10 },
      };

      const result = parseCompletion(completion);

      expect(result.answer).toBe('');
      expect(result.finishReason).toBe('stop');
    });
  });

  describe('isRetryableError', () => {
    test('retries on rate limit (429)', () => {
      expect(isRetryableError({ status: 429 })).toBe(true);
    });

    test('retries on server errors (5xx)', () => {
      expect(isRetryableError({ status: 500 })).toBe(true);
      expect(isRetryableError({ status: 502 })).toBe(true);
      expect(isRetryableError({ status: 503 })).toBe(true);
      expect(isRetryableError({ status: 504 })).toBe(true);
    });

    test('retries on network errors', () => {
      expect(isRetryableError({ code: 'ECONNRESET' })).toBe(true);
      expect(isRetryableError({ code: 'ETIMEDOUT' })).toBe(true);
    });

    test('does not retry on client errors', () => {
      expect(isRetryableError({ status: 400 })).toBe(false);
      expect(isRetryableError({ status: 401 })).toBe(false);
      expect(isRetryableError({ status: 403 })).toBe(false);
      expect(isRetryableError({ status: 404 })).toBe(false);
    });

    test('does not retry on other errors', () => {
      expect(isRetryableError({})).toBe(false);
      expect(isRetryableError({ status: 200 })).toBe(false);
      expect(isRetryableError({ code: 'UNKNOWN' })).toBe(false);
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
      expect(delay2).toBeLessThanOrEqual(2500);

      expect(delay3).toBeGreaterThanOrEqual(4000);
      expect(delay3).toBeLessThanOrEqual(5000);
    });

    test('caps at max delay', () => {
      const delay = calculateBackoff(10); // Would be 512s without cap
      expect(delay).toBeLessThanOrEqual(12500); // 10s + 25% jitter
      expect(delay).toBeGreaterThanOrEqual(10000);
    });

    test('adds jitter variation', () => {
      // Run multiple times to verify jitter is applied
      const delays = [];
      for (let i = 0; i < 10; i++) {
        delays.push(calculateBackoff(1));
      }

      // Not all delays should be identical (jitter varies)
      const uniqueDelays = new Set(delays);
      expect(uniqueDelays.size).toBeGreaterThan(1);

      // All should be within expected range
      delays.forEach(delay => {
        expect(delay).toBeGreaterThanOrEqual(1000);
        expect(delay).toBeLessThanOrEqual(1250);
      });
    });
  });
});
