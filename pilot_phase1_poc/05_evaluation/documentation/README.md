# Waypoint Co-Pilot — Documentation Index

This directory contains all documentation for the Waypoint RAG Co-Pilot Phase 1 POC. Documentation is organized into four categories: architecture docs (system-level diagrams and contracts), codebase docs (detailed module-level references), architecture decision records (ADRs), and user-facing guides.

## Documentation Layer Model

| Layer | Type | Location | Purpose |
|-------|------|----------|---------|
| **Layer 1** | Inline docs | Source files | JSDoc comments, Python docstrings — embedded in code |
| **Layer 2** | Pointer READMEs | `backend/`, `client/`, `scripts/`, `tests/`, `kb/` | Quick-start overview for each code directory |
| **Layer 3** | Detailed docs | `documentation/codebase/` | Module-level reference with function signatures and data flows |
| **Layer 4** | ADRs | `documentation/adrs/` | Architecture decisions with context, alternatives, and rationale |

---

## Architecture (6 files)

System-level documentation with Mermaid diagrams, data flow descriptions, and API contracts.

| File | Description |
|------|-------------|
| [system_overview.md](architecture/system_overview.md) | Tech stack table, Mermaid component diagram, deployment topology, key constraints |
| [data_flow.md](architecture/data_flow.md) | End-to-end query flow sequence diagram, timing breakdown (~1.2s avg), error flows |
| [ingestion_pipeline_flow.md](architecture/ingestion_pipeline_flow.md) | Ingestion stages (discover → parse → chunk → embed) with config parameters |
| [rag_pipeline_flow.md](architecture/rag_pipeline_flow.md) | RAG pipeline stages (retrieval → context → LLM → citations → confidence) with config values |
| [kb_schema.md](architecture/kb_schema.md) | YAML frontmatter schema, category folder structure, ChromaDB metadata, how-to-add guide |
| [api_contract.md](architecture/api_contract.md) | POST /api/query and GET /api/health — full request/response JSON schemas, error responses |

## Codebase — Backend (6 files)

Express API server documentation covering services, routes, middleware, and configuration.

| File | Description |
|------|-------------|
| [overview.md](codebase/backend/overview.md) | Express API architecture, middleware stack, request lifecycle |
| [services.md](codebase/backend/services.md) | All 6 service modules with function signatures (pipeline, retrieval, LLM, citations, embedding, index) |
| [routes.md](codebase/backend/routes.md) | API endpoints (/api/query, /api/health), validation rules, response schemas |
| [middleware.md](codebase/backend/middleware.md) | Error handler and not-found handler middleware |
| [config.md](codebase/backend/config.md) | 14 configuration properties with environment variable mappings |
| [prompts.md](codebase/backend/prompts.md) | System prompt template structure, design rationale, Phase 3 changes |

## Codebase — Frontend (3 files)

React + Tailwind CSS frontend documentation covering components and API client.

| File | Description |
|------|-------------|
| [overview.md](codebase/frontend/overview.md) | React component tree, state management, Tailwind styling approach |
| [components.md](codebase/frontend/components.md) | All 7 components with props tables (ResponseCard, QueryInput, SourcesSection, RelatedDocsSection, ConfidenceFooter, Loading, App) |
| [api_client.md](codebase/frontend/api_client.md) | API client module (submitQuery, checkHealth), response type definitions |

## Codebase — Scripts (5 files)

Python scripts for ingestion, retrieval, evaluation, and utilities.

| File | Description |
|------|-------------|
| [overview.md](codebase/scripts/overview.md) | Python script categories, dependencies, data flow between scripts |
| [ingestion.md](codebase/scripts/ingestion.md) | Full ingestion pipeline: config.py, process_docs.py, chunker.py, ingest.py |
| [pdf_extraction.md](codebase/scripts/pdf_extraction.md) | PDF extractor (pdf_extractor.py) with 9 functions for regulatory document processing |
| [evaluation.md](codebase/scripts/evaluation.md) | Evaluation harness with 6 metric checks (deflection, citation, hallucination, OOS, latency, stability) |
| [utilities.md](codebase/scripts/utilities.md) | query_chroma.py, verify_ingestion.py, view_chroma.py, retrieval_quality_test.py |

## Codebase — Tests (4 files)

Test suite documentation covering Jest (backend), Vitest (frontend), and pytest (Python).

| File | Description |
|------|-------------|
| [overview.md](codebase/tests/overview.md) | Test pyramid, 217 total tests across 3 frameworks |
| [backend_tests.md](codebase/tests/backend_tests.md) | 7 Jest test files with mock patterns and coverage details |
| [python_tests.md](codebase/tests/python_tests.md) | All Python test files (pytest) covering ingestion, chunking, and retrieval |
| [e2e_tests.md](codebase/tests/e2e_tests.md) | E2E testing approach via Chrome DevTools MCP (no Selenium/Cypress) |

## Architecture Decision Records (6 files)

Records of key technical decisions with context, alternatives considered, and rationale.

| File | Decision |
|------|----------|
| [ADR-001-vector-database.md](adrs/ADR-001-vector-database.md) | ChromaDB selected over Pinecone, Weaviate, pgvector, and FAISS |
| [ADR-002-llm-provider.md](adrs/ADR-002-llm-provider.md) | Groq + Llama 3.1 8B selected over OpenAI, Ollama, and Claude |
| [ADR-003-chunk-config.md](adrs/ADR-003-chunk-config.md) | Chunk size 600, overlap 90, top_k 5 — with full experiment matrix (5 configs tested) |
| [ADR-004-python-node-split.md](adrs/ADR-004-python-node-split.md) | Hybrid Python/Node.js architecture with subprocess bridge |
| [ADR-005-embedding-model.md](adrs/ADR-005-embedding-model.md) | all-MiniLM-L6-v2 via ONNX (ChromaDB default, no API key required) |
| [ADR-006-response-ux.md](adrs/ADR-006-response-ux.md) | 4-section response card design (answer, sources, related docs, confidence) |

## User-Facing Guides (3 files)

Practical guides for different audiences.

| File | Audience | Description |
|------|----------|-------------|
| [user_guide.md](guides/user_guide.md) | CS Agents | How to ask effective questions, understanding the 4-section response card, when to escalate, 10 sample queries |
| [deployment_notes.md](guides/deployment_notes.md) | Developers/IT | Prerequisites, 6-step installation, full .env reference, troubleshooting (11 common issues) |
| [known_limitations.md](guides/known_limitations.md) | All stakeholders | Scope limits, technical constraints, KB gaps, evaluation results, Phase 2 recommendations |

---

## Pointer READMEs (5 files)

Quick-start overviews located in each code directory, pointing to detailed documentation above.

| File | Description |
|------|-------------|
| [backend/README.md](../backend/README.md) | Express API overview with 14-file table and quick-start commands |
| [client/README.md](../client/README.md) | React frontend overview with component list and dev commands |
| [scripts/README.md](../scripts/README.md) | Python scripts overview with 10-file table and usage examples |
| [tests/README.md](../tests/README.md) | Test suite overview — 55 pytest + 162 Jest tests |
| [kb/README.md](../kb/README.md) | Knowledge base structure — 30 docs, 4 categories, frozen notice |

---

## Summary

| Category | Files |
|----------|-------|
| Architecture | 6 |
| Codebase — Backend | 6 |
| Codebase — Frontend | 3 |
| Codebase — Scripts | 5 |
| Codebase — Tests | 4 |
| ADRs | 6 |
| Guides | 3 |
| Pointer READMEs | 5 |
| **Total** | **38** |
