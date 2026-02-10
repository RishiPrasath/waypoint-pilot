# Backend — Express API for RAG Pipeline

Node.js/Express API server that orchestrates the full RAG pipeline: query processing, ChromaDB retrieval, LLM generation (Groq/Llama 3.1 8B), and citation extraction.

## File Structure

| File | Purpose |
|------|---------|
| `config.js` | Environment variables, ports, API keys, thresholds |
| `index.js` | Express app entry point, middleware registration |
| `middleware/errorHandler.js` | Centralized error handling middleware |
| `prompts/system.txt` | System prompt for LLM response generation |
| `routes/index.js` | Route aggregator |
| `routes/query.js` | POST /api/query — main RAG endpoint |
| `routes/health.js` | GET /api/health — status check |
| `services/pipeline.js` | End-to-end pipeline orchestration |
| `services/retrieval.js` | ChromaDB vector search (top-k=5, threshold=0.7) |
| `services/llm.js` | Groq API integration for response generation |
| `services/citations.js` | Source attribution and citation extraction |
| `services/embedding.js` | Query embedding via all-MiniLM-L6-v2 |
| `services/index.js` | Service barrel export |
| `utils/logger.js` | Structured logging utility |

## Quick Start

```bash
cd pilot_phase1_poc/05_evaluation
npm install
npm start        # Starts on port 3000
npm test         # Run Jest test suite (162 tests)
```

## Environment Variables

Requires `GROQ_API_KEY` in `.env`. See `config.js` for all options.

## Detailed Docs

See [detailed documentation](../documentation/codebase/backend/overview.md) for architecture, API contract, and service interactions.
