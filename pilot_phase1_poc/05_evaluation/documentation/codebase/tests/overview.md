# Test Suite Overview

## Test Pyramid

**Total: 217 tests** across two runtimes.

| Runtime | Framework | Test Count | Files |
|---------|-----------|------------|-------|
| Python (pytest) | pytest | 55 | 4 files |
| Node.js (Jest) | Jest 29 + ESM | 162 | 7 files |

## Python Test Files (pytest)

| File | Tests | Scope |
|------|-------|-------|
| `test_process_docs.py` | 22 | Frontmatter parsing, document discovery, metadata extraction, content extraction, category/doc_id generation |
| `test_pdf_extractor.py` | 22 | PDF-to-markdown extraction, content cleaning, quality assessment, batch processing, error handling |
| `test_verify_ingestion.py` | 5 | Post-ingestion verification (total count, category distribution, metadata integrity, tier 1-3 retrieval) |
| `test_retrieval_quality.py` | 6 | Retrieval hit rate across 50 queries (92% baseline), category-level breakdown |

### Python Test Location

Tests for Week 1 ingestion pipeline (`test_process_docs.py`, `test_verify_ingestion.py`) originate from `02_ingestion_pipeline/tests/` and are referenced from there. Week 3 tests (`test_pdf_extractor.py`) are in `04_retrieval_optimization/tests/`. Week 4 copies or extends these into `05_evaluation/tests/`.

### Python Test Runner

```bash
cd pilot_phase1_poc/05_evaluation
python -m pytest tests/ -v
```

## Jest Test Files

| File | Tests | Scope |
|------|-------|-------|
| `api.test.js` | 11 | Express endpoint validation (health, query, error handling, CORS) |
| `pipeline.test.js` | 19 | Query orchestration, confidence scoring, error propagation |
| `retrieval.test.js` | 15 | Chunk retrieval, threshold filtering, context formatting, citation metadata |
| `llm.test.js` | 18 | LLM client functions (system prompt, completion parsing, retry logic, backoff) |
| `citations.test.js` | 47 | Citation extraction regex, fuzzy matching, enrichment, formatting, sources/relatedDocs building |
| `generation.test.js` | 50 | generateResponse with mock OpenAI (10), formatContext (6), system prompt content validation (5), plus additional integration-level tests across 3 `describe` groups |
| `placeholder.test.js` | 2 | Jest configuration verification, environment loading |

### Jest Mocking Pattern

All Jest test files use `jest.unstable_mockModule()` for ESM module mocking. This is required because the backend uses ES modules (`type: "module"` in `package.json`). The pattern is:

```javascript
import { jest } from '@jest/globals';

// Mock BEFORE importing the module under test
jest.unstable_mockModule('../backend/services/pipeline.js', () => ({
  processQuery: jest.fn(),
}));

// Dynamic import AFTER mocks are set up
const { processQuery } = await import('../backend/services/pipeline.js');
```

### Jest Test Runner

```bash
cd pilot_phase1_poc/05_evaluation
npm test
```

## Additional Test Infrastructure

### Metadata Preservation Tests

`test_metadata_preservation.py` (in `05_evaluation/tests/`) validates that `source_urls`, `retrieval_keywords`, `use_cases`, and `category` fields are correctly stored in ChromaDB chunk metadata after ingestion. Runs against the live ChromaDB instance (not mocked). Contains 5 test classes:

- **TestFieldPresence** (6 tests) -- verifies all 3 new metadata fields exist as strings on every chunk
- **TestFieldFormat** (4 tests) -- validates category enum values, URL format, UC-N.N pattern
- **TestKnownValues** (9 tests) -- spot checks specific documents for expected metadata
- **TestEdgeCases** (5 tests) -- N/A URLs, multi-URL docs, same-doc consistency
- **TestCategoryCoverage** (2 tests) -- all 4 KB categories present with sufficient chunks

### E2E Node Tests

`tests/e2e_node/` contains Python-based E2E test utilities (`test_runner.py`, `test_config.py`, `test_data.py`) for running integration tests against the live Node.js API.

## E2E Testing Approach

No dedicated E2E test framework (Vitest, Cypress, Playwright) is configured. Frontend verification uses:

1. `npm run build` -- clean compilation check (zero warnings/errors)
2. Chrome DevTools MCP -- visual verification during Task T2.10
3. `evaluation_harness.py` -- functional E2E that sends real queries to the live API, validating the full pipeline end-to-end

See [e2e_tests.md](./e2e_tests.md) for details.
