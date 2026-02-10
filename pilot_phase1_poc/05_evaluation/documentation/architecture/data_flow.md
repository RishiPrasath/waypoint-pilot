# Data Flow — End-to-End Query Processing

## Overview

This document traces a user query from the React frontend through all pipeline stages and back to the UI. Each stage transforms data in a specific way before passing it downstream.

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant React as React UI
    participant Express as Express API<br/>(port 3000)
    participant Pipeline as pipeline.js
    participant Retrieval as retrieval.js
    participant Python as query_chroma.py<br/>(subprocess)
    participant ChromaDB
    participant LLMService as llm.js
    participant Groq as Groq API
    participant CitationSvc as citations.js

    User->>React: Types query
    React->>Express: POST /api/query { query }
    Express->>Express: Validate (non-empty, string, ≤1000 chars)
    Express->>Pipeline: processQuery(query)

    Note over Pipeline: Stage 1 — Retrieval
    Pipeline->>Retrieval: retrieveChunks(query, {topK, threshold})
    Retrieval->>Python: spawn process, write JSON to stdin
    Python->>ChromaDB: collection.query(query_texts, n_results)
    ChromaDB-->>Python: documents, metadatas, distances
    Python->>Python: Convert distance → similarity (1 - distance)
    Python-->>Retrieval: JSON stdout {success, chunks[]}
    Retrieval->>Retrieval: filterByThreshold(chunks, 0.15)
    Retrieval-->>Pipeline: filtered chunks[]

    alt No chunks found
        Pipeline-->>Express: buildNoResultsResponse (skip LLM)
        Express-->>React: {answer: decline msg, confidence: Low}
        React-->>User: Display "no info" message
    end

    Note over Pipeline: Stage 2 — Context Assembly
    Pipeline->>Retrieval: formatContext(chunks)
    Retrieval->>Retrieval: Build "[Title > Section]\ncontent\n\n" per chunk
    Retrieval->>Retrieval: Truncate at maxContextTokens × 4 chars
    Retrieval-->>Pipeline: context string

    Note over Pipeline: Stage 3 — Generation
    Pipeline->>LLMService: generateResponse(query, context)
    LLMService->>LLMService: buildSystemPrompt(context) — replace {context} placeholder
    LLMService->>Groq: chat.completions.create({model, messages, temperature, max_tokens})

    alt Groq 429 / 5xx
        Groq-->>LLMService: Error
        LLMService->>LLMService: Retry with exponential backoff (1s base, 10s max, 25% jitter)
    end

    Groq-->>LLMService: completion response
    LLMService->>LLMService: parseCompletion → {answer, usage, model}
    LLMService-->>Pipeline: {answer, finishReason, usage, model}

    Note over Pipeline: Stage 4 — Citation Processing
    Pipeline->>CitationSvc: processCitations(answer, chunks)
    CitationSvc->>CitationSvc: extractCitations — regex /\[([^\]]+)\]/g
    CitationSvc->>CitationSvc: enrichCitations — 3-tier matching per citation
    Note right of CitationSvc: 1. Exact title match<br/>2. Contains match<br/>3. Dice similarity > 0.5
    CitationSvc-->>Pipeline: {citations[], stats{matched, unmatched}}

    Note over Pipeline: Stage 5 — Confidence & Response
    Pipeline->>Pipeline: calculateConfidence(chunks, citationResult)
    Note right of Pipeline: High: ≥3 chunks, avgScore ≥ 0.5<br/>Medium: ≥2 chunks, avgScore ≥ 0.3<br/>Low: otherwise
    Pipeline->>CitationSvc: buildSources(citations, chunks)
    Pipeline->>CitationSvc: buildRelatedDocs(chunks)
    Pipeline-->>Express: {answer, sources, relatedDocs, citations, confidence, metadata}
    Express-->>React: JSON response (200)

    React->>React: Render 4-section card
    Note right of React: 1. Answer (react-markdown)<br/>2. Sources (clickable links)<br/>3. Related Docs (category chips)<br/>4. Confidence Footer (badge + stats)
    React-->>User: Display response
```

## Timing Breakdown

| Stage | Typical Duration | Notes |
|-------|-----------------|-------|
| Retrieval (Python subprocess) | ~200ms | ChromaDB query + subprocess spawn overhead |
| Context Assembly | <1ms | String concatenation |
| LLM Generation (Groq) | ~800ms | Network latency + token generation |
| Citation Processing | <10ms | Regex + string matching |
| Confidence Calculation | <1ms | Arithmetic |
| **Total** | **~1.0–1.5s** | Average ~1.2s |

## Data Transformations by Stage

### Input → Stage 1 (Retrieval)
- **In**: Query string (e.g., `"What are Singapore import procedures?"`)
- **Out**: Array of chunk objects, each with `content`, `metadata` (13 fields), `distance`, `score`
- **Transform**: Query string → ChromaDB embedding → vector similarity search → distance-to-similarity conversion (`score = 1 - distance`) → threshold filter (score ≥ 0.15)

### Stage 1 → Stage 2 (Context Assembly)
- **In**: Filtered chunks array
- **Out**: Single context string
- **Transform**: Each chunk formatted as `[Title > Section]\ncontent\n\n`, concatenated up to `maxContextTokens × 4` character limit (default: 8000 chars)

### Stage 2 → Stage 3 (Generation)
- **In**: Query string + context string
- **Out**: LLM response object `{answer, finishReason, usage, model}`
- **Transform**: System prompt template with `{context}` placeholder replaced → two-message array (`[system, user]`) → Groq API call → parsed completion

### Stage 3 → Stage 4 (Citation Processing)
- **In**: Answer text + original chunks
- **Out**: `{citations[], markdown, stats}`
- **Transform**: Regex extraction of `[bracketed references]` → 3-tier matching to source chunks → enrichment with `sourceUrls`, `docId`, `score`

### Stage 4 → Stage 5 (Response Assembly)
- **In**: Answer, chunks, citation result
- **Out**: Complete API response
- **Transform**:
  - `buildSources()` — matched citations with external URLs → sources array
  - `buildRelatedDocs()` — unique parent documents from all chunks → relatedDocs array
  - `calculateConfidence()` — chunk count + average score → confidence level
  - Final assembly into `{answer, sources, relatedDocs, citations, confidence, metadata}`

## Error Flows

| Error | Source | Behavior |
|-------|--------|----------|
| ChromaDB unavailable | Python subprocess exit code ≠ 0 | Pipeline throws `Retrieval failed` error → 500 response |
| Groq 429 (rate limit) | Groq API | Retry with exponential backoff (base 1s, max 10s, 25% jitter), up to 3 attempts |
| Groq 5xx (server error) | Groq API | Same retry logic as 429 |
| Groq 400 (bad request) | Groq API | Immediate fail, no retry → Pipeline error → 500 response |
| Network errors (ECONNRESET, ETIMEDOUT) | Groq API | Retry with backoff |
| Empty query | Route validation | 400 response: `"Query cannot be empty"` |
| Query too long | Route validation | 400 response: `"Query exceeds maximum length of 1000 characters"` |
| No chunks found | Threshold filter returns 0 | `buildNoResultsResponse()` — skip LLM, return Low confidence with decline message |

## Related Documentation

- [System Overview](system_overview.md) — Component diagram and tech stack
- [RAG Pipeline Flow](rag_pipeline_flow.md) — Detailed stage configuration values
- See [services.md](../codebase/backend/services.md) for function-level details
