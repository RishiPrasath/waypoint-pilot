# Tests — 217 Tests (55 pytest + 162 Jest)

Combined test suite covering the full RAG pipeline: backend services (Jest), Python ingestion/retrieval (pytest), and component tests (Vitest).

## Jest Tests (162 tests)

| File | Tests | Coverage |
|------|-------|----------|
| `api.test.js` | 11 | Route handlers, request validation |
| `pipeline.test.js` | 19 | End-to-end pipeline orchestration |
| `retrieval.test.js` | 15 | ChromaDB search, threshold filtering |
| `llm.test.js` | 18 | Groq API calls, prompt construction |
| `citations.test.js` | 47 | Source extraction, attribution logic |
| `generation.test.js` | 50 | Response formatting, edge cases |
| `placeholder.test.js` | 2 | Smoke tests |

Support files: `setup.js` (Jest globals and mocks).

## Python Tests (55 tests)

| File | Tests | Coverage |
|------|-------|----------|
| `test_metadata_preservation.py` | 33 | Frontmatter parsing, chunk metadata |
| `test_pdf_extractor.py` | 22 | PDF extraction, markdown conversion |

Additional ingestion tests run inline via `scripts/verify_ingestion.py`.

## Quick Start

```bash
cd pilot_phase1_poc/05_evaluation

# Jest (backend + services)
npm test

# Pytest (Python scripts)
venv\Scripts\activate
python -m pytest tests/ -v

# Vitest (React components)
cd client && npm test
```

## Detailed Docs

See [detailed documentation](../documentation/codebase/tests/overview.md) for test strategy, coverage targets, and fixture setup.
