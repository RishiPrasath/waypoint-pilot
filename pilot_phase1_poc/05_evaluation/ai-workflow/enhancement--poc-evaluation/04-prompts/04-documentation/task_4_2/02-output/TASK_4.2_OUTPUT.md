# Task 4.2 Output — Architecture Documentation (6 files)

**Status**: Complete
**Date**: 2026-02-10

## Files Created

| # | File | Description |
|---|------|-------------|
| 1 | `documentation/architecture/system_overview.md` | Purpose, tech stack table, Mermaid component diagram, deployment topology, constraints |
| 2 | `documentation/architecture/data_flow.md` | End-to-end Mermaid sequence diagram, timing breakdown, data transformations per stage, error flows |
| 3 | `documentation/architecture/ingestion_pipeline_flow.md` | Mermaid flow diagram, 4 stages (discover → parse → chunk → embed), config params, CLI usage |
| 4 | `documentation/architecture/rag_pipeline_flow.md` | Mermaid flow diagram, 5 stages with config tables, no-results path, confidence scoring |
| 5 | `documentation/architecture/kb_schema.md` | YAML frontmatter schema, category folder structure, ChromaDB metadata, how-to-add guide |
| 6 | `documentation/architecture/api_contract.md` | POST /api/query (full request/response JSON schema), GET /api/health, error responses |

## Validation Checklist

- [x] 6 architecture docs created
- [x] `system_overview.md` includes tech stack with versions + component diagram (Mermaid)
- [x] `data_flow.md` includes sequence diagram (Mermaid)
- [x] `ingestion_pipeline_flow.md` covers all stages with config parameters
- [x] `rag_pipeline_flow.md` covers all stages with config parameters
- [x] `kb_schema.md` covers all frontmatter fields and ChromaDB metadata
- [x] `api_contract.md` covers new 4-section response shape with full JSON schema

## Source Files Verified

All HIGH priority source files were read before generating documentation:
- `backend/services/pipeline.js` — RAG pipeline stages, confidence scoring thresholds
- `backend/services/retrieval.js` — ChromaDB bridge, formatContext, filterByThreshold
- `backend/services/llm.js` — Groq client, retry logic, buildSystemPrompt
- `backend/services/citations.js` — Citation pipeline, buildSources, buildRelatedDocs
- `backend/config.js` — All 14 config values verified
- `backend/routes/query.js` — Request validation (non-empty, string, ≤1000 chars)
- `backend/routes/health.js` — Health endpoint response shape
- `backend/index.js` — Express server setup, CORS, body limit
- `backend/prompts/system.txt` — System prompt template with {context} placeholder
- `scripts/config.py` — Python-side config (CHUNK_SIZE, CHUNK_OVERLAP, SEPARATORS)
- `scripts/process_docs.py` — Document discovery, frontmatter parsing, content extraction
- `scripts/chunker.py` — RecursiveCharacterTextSplitter configuration, section header extraction
- `scripts/ingest.py` — Ingestion entry point, ChromaDB initialization, metadata mapping
- `scripts/query_chroma.py` — Python bridge, distance→similarity conversion

## Notes

- All Mermaid diagrams verified against actual source code
- Config values (topK=10, threshold=0.15, temperature=0.3, etc.) confirmed from `config.js` and `config.py`
- Confidence thresholds (High: ≥3/≥0.5, Medium: ≥2/≥0.3) confirmed from `pipeline.js`
- Cross-references to Layer 3 codebase docs included where appropriate
