/**
 * Generation Layer Tests
 *
 * Covers gaps not addressed by llm.test.js (pure functions) or pipeline.test.js (orchestration):
 * - generateResponse with mocked OpenAI client (retry logic, message construction)
 * - formatContext (context assembly, truncation)
 * - System prompt content validation (T1.1 formatting instructions)
 */

import { jest } from '@jest/globals';

// ─── Group 1: generateResponse with mocked OpenAI client ───────────────

describe('generateResponse', () => {
  let generateResponse, resetLLMClient, resetSystemPrompt, buildSystemPrompt;
  let mockCreate;

  beforeAll(async () => {
    // Mock the openai module so initLLMClient returns a controlled client
    mockCreate = jest.fn();

    jest.unstable_mockModule('openai', () => ({
      default: class MockOpenAI {
        constructor() {
          this.chat = {
            completions: {
              create: mockCreate,
            },
          };
        }
      },
    }));

    // Mock config to provide an API key and known values
    jest.unstable_mockModule('../backend/config.js', () => ({
      config: {
        llmApiKey: 'test-api-key',
        llmBaseUrl: 'https://api.groq.com/openai/v1',
        llmProvider: 'groq',
        llmModel: 'llama-3.1-8b-instant',
        llmTemperature: 0.3,
        llmMaxTokens: 500,
      },
    }));

    // Mock logger to suppress output
    jest.unstable_mockModule('../backend/utils/logger.js', () => ({
      logger: {
        info: jest.fn(),
        warn: jest.fn(),
        error: jest.fn(),
        debug: jest.fn(),
      },
    }));

    // Import AFTER mocks are set up
    const llm = await import('../backend/services/llm.js');
    generateResponse = llm.generateResponse;
    resetLLMClient = llm.resetLLMClient;
    resetSystemPrompt = llm.resetSystemPrompt;
    buildSystemPrompt = llm.buildSystemPrompt;
  });

  beforeEach(() => {
    mockCreate.mockReset();
    resetLLMClient();
  });

  const validCompletion = {
    choices: [{
      message: { content: 'Singapore requires a Bill of Lading for all sea freight.' },
      finish_reason: 'stop',
    }],
    usage: { prompt_tokens: 200, completion_tokens: 40, total_tokens: 240 },
    model: 'llama-3.1-8b-instant',
  };

  test('returns parsed result on successful generation', async () => {
    mockCreate.mockResolvedValue(validCompletion);

    const result = await generateResponse('What documents for export?', 'context here');

    expect(result.answer).toBe('Singapore requires a Bill of Lading for all sea freight.');
    expect(result.finishReason).toBe('stop');
    expect(result.usage.promptTokens).toBe(200);
    expect(result.usage.completionTokens).toBe(40);
    expect(result.model).toBe('llama-3.1-8b-instant');
  });

  test('constructs messages with system and user roles', async () => {
    mockCreate.mockResolvedValue(validCompletion);

    await generateResponse('Test query', 'context', { systemPrompt: 'Custom prompt' });

    const callArgs = mockCreate.mock.calls[0][0];
    expect(callArgs.messages).toHaveLength(2);
    expect(callArgs.messages[0].role).toBe('system');
    expect(callArgs.messages[0].content).toBe('Custom prompt');
    expect(callArgs.messages[1].role).toBe('user');
    expect(callArgs.messages[1].content).toBe('Test query');
  });

  test('passes config values to API call', async () => {
    mockCreate.mockResolvedValue(validCompletion);

    await generateResponse('Test', 'context', { systemPrompt: 'prompt' });

    const callArgs = mockCreate.mock.calls[0][0];
    expect(callArgs.model).toBe('llama-3.1-8b-instant');
    expect(callArgs.temperature).toBe(0.3);
    expect(callArgs.max_tokens).toBe(500);
  });

  test('uses custom systemPrompt when provided', async () => {
    mockCreate.mockResolvedValue(validCompletion);

    await generateResponse('query', 'context', { systemPrompt: 'My custom prompt' });

    const callArgs = mockCreate.mock.calls[0][0];
    expect(callArgs.messages[0].content).toBe('My custom prompt');
  });

  test('calls buildSystemPrompt when no custom prompt provided', async () => {
    mockCreate.mockResolvedValue(validCompletion);

    await generateResponse('query', 'test context data');

    const callArgs = mockCreate.mock.calls[0][0];
    // buildSystemPrompt replaces {context} with the provided context
    expect(callArgs.messages[0].content).toContain('test context data');
    expect(callArgs.messages[0].content).not.toContain('{context}');
  });

  test('retries on 429 rate limit and succeeds', async () => {
    const rateLimitError = new Error('Rate limited');
    rateLimitError.status = 429;

    mockCreate
      .mockRejectedValueOnce(rateLimitError)
      .mockResolvedValueOnce(validCompletion);

    const result = await generateResponse('query', 'context', {
      systemPrompt: 'prompt',
      maxRetries: 2,
    });

    expect(mockCreate).toHaveBeenCalledTimes(2);
    expect(result.answer).toBe('Singapore requires a Bill of Lading for all sea freight.');
  });

  test('retries on 503 server error and succeeds', async () => {
    const serverError = new Error('Service unavailable');
    serverError.status = 503;

    mockCreate
      .mockRejectedValueOnce(serverError)
      .mockResolvedValueOnce(validCompletion);

    const result = await generateResponse('query', 'context', {
      systemPrompt: 'prompt',
      maxRetries: 2,
    });

    expect(mockCreate).toHaveBeenCalledTimes(2);
    expect(result.answer).toContain('Bill of Lading');
  });

  test('throws on non-retryable 400 client error without delay', async () => {
    const clientError = new Error('Bad request');
    clientError.status = 400;

    mockCreate.mockRejectedValue(clientError);

    const start = Date.now();
    await expect(
      generateResponse('query', 'context', { systemPrompt: 'prompt', maxRetries: 3 })
    ).rejects.toThrow('LLM request failed: Bad request');
    const elapsed = Date.now() - start;

    // Non-retryable errors still loop but without backoff delay
    // Should complete near-instantly (< 500ms) vs retryable which would take 3+ seconds
    expect(elapsed).toBeLessThan(500);
  });

  test('throws after exhausting retries', async () => {
    const rateLimitError = new Error('Rate limited');
    rateLimitError.status = 429;

    mockCreate.mockRejectedValue(rateLimitError);

    await expect(
      generateResponse('query', 'context', { systemPrompt: 'prompt', maxRetries: 2 })
    ).rejects.toThrow('LLM request failed: Rate limited');

    expect(mockCreate).toHaveBeenCalledTimes(2);
  });

  test('respects custom maxRetries option', async () => {
    const rateLimitError = new Error('Rate limited');
    rateLimitError.status = 429;

    mockCreate.mockRejectedValue(rateLimitError);

    await expect(
      generateResponse('query', 'context', { systemPrompt: 'prompt', maxRetries: 1 })
    ).rejects.toThrow('LLM request failed');

    expect(mockCreate).toHaveBeenCalledTimes(1);
  });
});

// ─── Group 2: formatContext ─────────────────────────────────────────────

describe('formatContext', () => {
  let formatContext;

  beforeAll(async () => {
    // Import the real retrieval module (formatContext is a pure function)
    // Need to mock the Python bridge parts that break in test env
    jest.unstable_mockModule('../backend/config.js', () => ({
      config: {
        retrievalTopK: 10,
        relevanceThreshold: 0.15,
        maxContextTokens: 2000,
        collectionName: 'waypoint_kb',
      },
    }));

    jest.unstable_mockModule('../backend/utils/logger.js', () => ({
      logger: {
        info: jest.fn(),
        warn: jest.fn(),
        error: jest.fn(),
        debug: jest.fn(),
      },
    }));

    const retrieval = await import('../backend/services/retrieval.js');
    formatContext = retrieval.formatContext;
  });

  test('formats single chunk with title and section', () => {
    const chunks = [{
      content: 'GST rate is 9% for imported goods.',
      metadata: { title: 'Singapore GST Guide', section: 'Rates' },
      score: 0.85,
    }];

    const result = formatContext(chunks, 10000);

    expect(result).toContain('[Singapore GST Guide > Rates]');
    expect(result).toContain('GST rate is 9% for imported goods.');
  });

  test('formats multiple chunks separated by double newlines', () => {
    const chunks = [
      { content: 'First chunk', metadata: { title: 'Doc A', section: 'S1' }, score: 0.9 },
      { content: 'Second chunk', metadata: { title: 'Doc B', section: 'S2' }, score: 0.8 },
    ];

    const result = formatContext(chunks, 10000);

    expect(result).toContain('[Doc A > S1]');
    expect(result).toContain('First chunk');
    expect(result).toContain('[Doc B > S2]');
    expect(result).toContain('Second chunk');
  });

  test('omits section separator when section is empty', () => {
    const chunks = [{
      content: 'Content here',
      metadata: { title: 'My Document', section: '' },
      score: 0.7,
    }];

    const result = formatContext(chunks, 10000);

    expect(result).toContain('[My Document]');
    expect(result).not.toContain('>');
  });

  test('falls back to Unknown Document when title is missing', () => {
    const chunks = [{
      content: 'Some content',
      metadata: {},
      score: 0.6,
    }];

    const result = formatContext(chunks, 10000);

    expect(result).toContain('[Unknown Document]');
    expect(result).toContain('Some content');
  });

  test('truncates when chunks exceed maxChars', () => {
    const longContent = 'A'.repeat(500);
    const chunks = [
      { content: longContent, metadata: { title: 'Doc 1', section: 'S1' }, score: 0.9 },
      { content: longContent, metadata: { title: 'Doc 2', section: 'S2' }, score: 0.8 },
      { content: longContent, metadata: { title: 'Doc 3', section: 'S3' }, score: 0.7 },
    ];

    // Set maxChars so only first 2 chunks fit
    const result = formatContext(chunks, 1100);

    expect(result).toContain('[Doc 1 > S1]');
    expect(result).toContain('[Doc 2 > S2]');
    expect(result).not.toContain('[Doc 3 > S3]');
  });

  test('returns empty string for empty chunks array', () => {
    const result = formatContext([], 10000);

    expect(result).toBe('');
  });
});

// ─── Group 3: System Prompt Content Validation ──────────────────────────

describe('System Prompt Content', () => {
  let loadSystemPrompt, buildSystemPrompt, resetSystemPrompt;

  beforeAll(async () => {
    // Use the real llm module for system prompt tests (no mocks needed for file reads)
    // But we still need to mock logger
    jest.unstable_mockModule('../backend/utils/logger.js', () => ({
      logger: {
        info: jest.fn(),
        warn: jest.fn(),
        error: jest.fn(),
        debug: jest.fn(),
      },
    }));

    // Use real config for system prompt tests
    jest.unstable_mockModule('../backend/config.js', () => ({
      config: {
        llmApiKey: 'test-key',
        llmBaseUrl: 'https://api.groq.com/openai/v1',
        llmProvider: 'groq',
        llmModel: 'llama-3.1-8b-instant',
        llmTemperature: 0.3,
        llmMaxTokens: 500,
      },
    }));

    const llm = await import('../backend/services/llm.js');
    loadSystemPrompt = llm.loadSystemPrompt;
    buildSystemPrompt = llm.buildSystemPrompt;
    resetSystemPrompt = llm.resetSystemPrompt;
  });

  beforeEach(() => {
    resetSystemPrompt();
  });

  test('contains T1.1 formatting sections', () => {
    const prompt = loadSystemPrompt();

    expect(prompt).toContain('Be Direct and Scannable');
    expect(prompt).toContain('Cite Your Sources Inline');
    expect(prompt).toContain('Handle Limitations Honestly');
    expect(prompt).toContain('Format Your Response with Markdown');
  });

  test('contains citation format instruction with bracket pattern', () => {
    const prompt = loadSystemPrompt();

    expect(prompt).toContain('[Document Title > Section Name]');
    expect(prompt).toContain('[Document Title > Section]');
  });

  test('contains out-of-scope handling instructions', () => {
    const prompt = loadSystemPrompt();

    expect(prompt).toContain('Out of Scope');
    expect(prompt).toContain('Real-time tracking');
    expect(prompt).toContain('Live freight rates');
    expect(prompt).toContain('Booking changes');
  });

  test('contains action request handling instructions', () => {
    const prompt = loadSystemPrompt();

    expect(prompt).toContain('Action Request Handling');
    expect(prompt).toContain('knowledge assistant');
  });

  test('buildSystemPrompt replaces context placeholder completely', () => {
    const result = buildSystemPrompt('Singapore customs clearance procedures here');

    expect(result).toContain('Singapore customs clearance procedures here');
    expect(result).not.toContain('{context}');
  });
});
