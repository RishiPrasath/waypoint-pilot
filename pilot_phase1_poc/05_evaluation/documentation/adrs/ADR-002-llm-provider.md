# ADR-002: LLM Provider Selection -- Groq + Llama 3.1 8B

**Status**: Accepted
**Date**: 2025-01-22

## Context

The Waypoint co-pilot needs an LLM for response generation -- taking retrieved knowledge base context and producing customer service answers with citations. Requirements:

- Low latency (target: < 5 seconds end-to-end including retrieval)
- Minimal cost (total POC budget: under $10 for all LLM API calls)
- Sufficient quality for structured, citation-backed responses
- OpenAI-compatible API format for standard client library usage

The POC runs 50 evaluation queries plus development/testing iterations, estimated at 200-500 total API calls.

## Decision

Use **Groq API** with the **llama-3.1-8b-instant** model.

Configuration:
- Base URL: `https://api.groq.com/openai/v1`
- Model: `llama-3.1-8b-instant`
- Temperature: 0.3
- Max tokens: 500
- Client: `openai` npm package (Groq is OpenAI-compatible)

Retry logic handles 429 rate limit errors with exponential backoff (1s base, 10s cap, 25% jitter).

## Alternatives Considered

| Alternative | Reason for Rejection |
|------------|---------------------|
| **OpenAI GPT-4** | Cost prohibitive for POC. GPT-4 pricing would consume the entire $10 budget in ~50 queries with context. |
| **OpenAI GPT-3.5-turbo** | Lower cost but still accumulates charges. Groq free tier eliminates cost entirely for POC volume. |
| **Local Ollama (Llama 3.1)** | Slow inference without GPU (~10-30s per query on CPU). Requires model download (4-8GB). Development machine lacks dedicated GPU. |
| **Anthropic Claude** | Higher per-token cost. No free tier sufficient for POC volume. Would add separate SDK dependency. |

## Consequences

**Positive**:
- Inference latency around 100ms on Groq hardware (fastest available inference)
- Free tier sufficient for all POC evaluation queries (well under $10 budget)
- OpenAI-compatible API means standard `openai` npm package works without modification
- Llama 3.1 8B produces adequate quality for structured, citation-backed responses
- No vendor lock-in -- can swap to any OpenAI-compatible provider by changing base URL and API key

**Negative**:
- Nondeterministic outputs even at temperature 0.3 -- same query may produce slightly different responses
- Rate limits on free tier (429 errors) require backoff handling in production-like evaluation runs
- 8B parameter model has limited complex reasoning ability compared to larger models
- Groq is a relatively newer provider -- less established SLA and support than OpenAI
- Model may occasionally fail to follow citation format instructions (`[Title > Section]`), requiring post-processing
