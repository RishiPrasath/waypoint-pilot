# ADR-004: Hybrid Python/Node.js Architecture

**Status**: Accepted
**Date**: 2025-01-20

## Context

The Waypoint co-pilot requires two distinct capabilities:

1. **Document processing**: Parse markdown with YAML frontmatter, chunk text, generate embeddings, store in vector database, and query vectors at retrieval time.
2. **Web API and UI**: Serve an Express REST API, host a React frontend, orchestrate the query pipeline (retrieval, LLM generation, citation extraction).

Python has mature libraries for NLP/ML tasks (ChromaDB, ONNX runtime, PyMuPDF). Node.js has a stronger ecosystem for web APIs (Express) and frontend tooling (React, Vite, Tailwind).

## Decision

Use a **hybrid architecture**:

- **Python** for all document processing, embedding, and ChromaDB operations:
  - `scripts/ingest.py` -- ingestion pipeline
  - `scripts/process_docs.py` -- document parsing and chunking
  - `scripts/query_chroma.py` -- vector retrieval bridge
  - `scripts/pdf_extractor.py` -- PDF-to-markdown conversion
  - `scripts/retrieval_quality_test.py` -- retrieval evaluation
  - `scripts/evaluation_harness.py` -- full pipeline evaluation

- **Node.js** for the web-facing layer:
  - `backend/index.js` -- Express API server
  - `backend/services/pipeline.js` -- query orchestration
  - `backend/services/retrieval.js` -- calls Python bridge, formats context
  - `backend/services/llm.js` -- Groq LLM client with retry logic
  - `backend/services/citations.js` -- citation extraction and enrichment
  - `client/` -- React frontend with Vite

**Bridge mechanism**: The Node.js retrieval service spawns `query_chroma.py` as a child process per query. Input is JSON via stdin, output is JSON via stdout.

```
Browser -> Express API -> pipeline.js -> retrieval.js --(subprocess)--> query_chroma.py -> ChromaDB
                                      -> llm.js --(HTTP)--> Groq API
                                      -> citations.js (pure JS)
```

## Alternatives Considered

| Alternative | Reason for Rejection |
|------------|---------------------|
| **All-Python (Flask/FastAPI)** | Weaker frontend tooling. Would require Jinja templates or separate React build pipeline. FastAPI adds async complexity for a simple POC. |
| **All-Node.js** | ChromaDB has no official Node.js client with PersistentClient support. The `chromadb` npm package is limited. ONNX embedding would require custom setup. |
| **Microservices (Python service + Node service)** | Over-engineered for a single-developer POC. Adds Docker orchestration, inter-service networking, and deployment complexity. |
| **Python + HTMX** | Simpler stack but limited UI interactivity for the 4-section response card with confidence badges, category chips, and markdown rendering. |

## Consequences

**Positive**:
- Best-in-class libraries for each task: ChromaDB Python client, ONNX runtime, Express, React
- Python tests (pytest) cover document processing; Jest tests cover API and business logic
- Clean separation of concerns: data processing vs. web serving
- Each runtime can be developed and tested independently
- Frontend hot-reload (Vite) works independently of Python backend

**Negative**:
- Subprocess overhead per query: approximately 200ms for Python process spawn + ChromaDB query
- Two runtimes to install and manage (Python 3.11 venv + Node.js 18+)
- JSON serialization boundary between Python and Node.js adds potential for data format mismatches
- Debugging cross-runtime issues (Node spawning Python) is harder than single-runtime debugging
- CI/CD pipeline must handle both Python and Node.js test suites
