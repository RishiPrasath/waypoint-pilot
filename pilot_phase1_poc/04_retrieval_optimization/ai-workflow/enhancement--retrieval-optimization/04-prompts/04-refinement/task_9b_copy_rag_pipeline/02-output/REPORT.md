# Task 9B: Copy RAG Pipeline to 04_retrieval_optimization

**Status**: COMPLETE
**Date**: 2026-02-07

---

## 1. Summary

Task 9B copied the full RAG pipeline (Express backend, React frontend, Python bridge, Jest tests, and Node.js configuration) from `03_rag_pipeline/` into `04_retrieval_optimization/`, making it a self-contained deliverable that includes ingestion, backend API, and frontend UI in a single directory.

The Express `src/` directory was renamed to `backend/` for clarity. All internal path references were updated to reflect the new directory structure. The existing Python `.env` was merged with the Node.js `.env` into a single unified file with no conflicts.

---

## 2. Files Copied

| # | Source (`03_rag_pipeline/`) | Destination (`04_retrieval_optimization/`) | Notes |
|---|---|---|---|
| 1 | `src/` (entire directory) | `backend/` | Renamed `src` to `backend` for clarity |
| 2 | `client/` (entire directory) | `client/` | React + Vite + Tailwind frontend, copied as-is |
| 3 | `scripts/query_chroma.py` | `scripts/query_chroma.py` | Python bridge for ChromaDB queries from Node.js |
| 4 | `tests/*.test.js` (6 files) | `tests/` | Merged into existing tests directory |
| 5 | `tests/setup.js` | `tests/setup.js` | Jest test setup file |
| 6 | `tests/e2e/` | `tests/e2e_node/` | E2E tests, renamed to avoid conflict |
| 7 | `package.json` | `package.json` | Node.js project config |
| 8 | `package-lock.json` | `package-lock.json` | Dependency lock file |
| 9 | `jest.config.js` | `jest.config.js` | Jest test configuration |
| 10 | `.env` (Node.js vars) | `.env` (merged) | Merged into existing Python `.env` |

### Backend Directory Contents

```
backend/
  index.js              # Express server entry point (port 3000)
  config.js             # Environment configuration loader
  services/
    retrieval.js        # ChromaDB query via Python subprocess
    llm.js              # Groq Llama 3.1 8B integration
    pipeline.js         # RAG orchestration
    citations.js        # Citation extraction
    embedding.js        # Embedding service
    index.js            # Service barrel export
  routes/
    index.js            # Route registry
    query.js            # POST /api/query
    health.js           # GET /api/health
  middleware/
    errorHandler.js     # Express error handling
  prompts/
    system.txt          # LLM system prompt
  utils/
    logger.js           # Logging utility
```

### Jest Test Files Merged

```
tests/
  api.test.js           # 19 tests - API endpoint tests
  citations.test.js     # 12 tests - Citation extraction tests
  llm.test.js           # 20 tests - LLM service tests
  pipeline.test.js      # 15 tests - RAG pipeline orchestration tests
  retrieval.test.js     # 28 tests - Retrieval service tests
  placeholder.test.js   # 11 tests - Configuration and placeholder tests
  setup.js              # Jest setup file
  e2e_node/             # E2E integration tests
```

---

## 3. Path Fixes Applied

### 3a. `package.json` -- `src/` to `backend/`

| Field | Before | After |
|-------|--------|-------|
| `main` | `"src/index.js"` | `"backend/index.js"` |
| `scripts.start` | `"node src/index.js"` | `"node backend/index.js"` |
| `scripts.dev` | `"node --watch src/index.js"` | `"node --watch backend/index.js"` |

### 3b. `backend/services/retrieval.js` -- Python venv path

```
BEFORE: const PYTHON_PATH = join(__dirname, '..', '..', 'ingestion', 'venv', 'Scripts', 'python.exe');
AFTER:  const PYTHON_PATH = join(__dirname, '..', '..', 'venv', 'Scripts', 'python.exe');
```

Rationale: In `03_rag_pipeline/`, the Python venv was inside an `ingestion/` subfolder. In `04_retrieval_optimization/`, the venv is at the project root (`./venv/`).

### 3c. `scripts/query_chroma.py` -- ChromaDB path

```
BEFORE: sys.path.insert(0, str(Path(__file__).parent.parent / 'ingestion'))
        chroma_path = Path(__file__).parent.parent / 'ingestion' / 'chroma_db'

AFTER:  (sys.path.insert line removed -- not needed, chromadb is in venv)
        chroma_path = Path(__file__).parent.parent / 'chroma_db'
```

Rationale: In `03_rag_pipeline/`, ChromaDB data was at `ingestion/chroma_db/`. In `04_retrieval_optimization/`, it is at `./chroma_db/`.

### 3d. `backend/config.js` -- Fallback chroma path

```
BEFORE: chromaPath: process.env.CHROMA_PATH || './ingestion/chroma_db',
AFTER:  chromaPath: process.env.CHROMA_PATH || './chroma_db',
```

### 3e. Jest Test Files -- Import paths (14 occurrences across 6 files)

All `../src/` imports updated to `../backend/`:

| File | Occurrences Changed |
|------|-------------------|
| `api.test.js` | 3 (`../src/services/pipeline.js`, `../src/index.js`, `../src/services/pipeline.js`) |
| `citations.test.js` | 1 (`../src/services/citations.js`) |
| `llm.test.js` | 1 (`../src/services/llm.js`) |
| `pipeline.test.js` | 6 (`../src/services/retrieval.js`, `../src/services/llm.js`, `../src/services/citations.js`, `../src/services/pipeline.js`, `../src/services/retrieval.js`, `../src/services/llm.js`, `../src/services/citations.js`) |
| `retrieval.test.js` | 1 (`../src/services/retrieval.js`) |
| `placeholder.test.js` | 1 (`../src/config.js`) |

### 3f. `.env` -- Merged and fixed CHROMA_PATH

The Python ingestion `.env` (3 vars) was merged with the Node.js `.env` (13 vars) into a single unified file. `COLLECTION_NAME=waypoint_kb` appeared in both with the same value -- deduplicated. `CHROMA_PATH` was updated from `./ingestion/chroma_db` to `./chroma_db`.

---

## 4. Verification Results

### npm install

```
378 packages installed
0 vulnerabilities
```

### Jest Tests

```
Test Suites: 6 passed, 6 total
Tests:       105 passed, 105 total

  PASS  tests/api.test.js        (19 tests)
  PASS  tests/citations.test.js  (12 tests)
  PASS  tests/llm.test.js        (20 tests)
  PASS  tests/pipeline.test.js   (15 tests)
  PASS  tests/retrieval.test.js  (28 tests)
  PASS  tests/placeholder.test.js (11 tests)
```

All 6 test suites pass. All 105 individual tests pass.

---

## 5. Final Directory Structure

```
04_retrieval_optimization/
├── backend/                  # Express API server (copied from 03/src/, renamed)
│   ├── index.js
│   ├── config.js
│   ├── services/
│   │   ├── retrieval.js
│   │   ├── llm.js
│   │   ├── pipeline.js
│   │   ├── citations.js
│   │   ├── embedding.js
│   │   └── index.js
│   ├── routes/
│   │   ├── index.js
│   │   ├── query.js
│   │   └── health.js
│   ├── middleware/
│   │   └── errorHandler.js
│   ├── prompts/
│   │   └── system.txt
│   └── utils/
│       └── logger.js
├── client/                   # React + Vite + Tailwind UI
│   ├── src/
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── eslint.config.js
├── scripts/                  # Python scripts (ingestion + query bridge)
│   ├── query_chroma.py       # ChromaDB query bridge (Node.js -> Python)
│   ├── process_docs.py       # Document processing
│   ├── ingest.py             # Full ingestion pipeline
│   ├── config.py             # Python config
│   ├── chunker.py            # Text chunking
│   ├── verify_ingestion.py   # Ingestion verification
│   ├── retrieval_quality_test.py  # Retrieval quality evaluation
│   ├── pdf_extractor.py      # PDF content extraction
│   └── view_chroma.py        # ChromaDB viewer
├── tests/                    # Combined Python + Jest test suite
│   ├── api.test.js           # Jest: API endpoint tests (19)
│   ├── citations.test.js     # Jest: Citation tests (12)
│   ├── llm.test.js           # Jest: LLM service tests (20)
│   ├── pipeline.test.js      # Jest: Pipeline tests (15)
│   ├── retrieval.test.js     # Jest: Retrieval tests (28)
│   ├── placeholder.test.js   # Jest: Config/placeholder tests (11)
│   ├── setup.js              # Jest: Test setup
│   ├── e2e_node/             # Jest: E2E integration tests
│   ├── test_pdf_extractor.py # pytest: PDF extractor tests
│   └── __init__.py           # Python package marker
├── kb/                       # Week 3 optimized knowledge base (30 docs)
├── chroma_db/                # ChromaDB vector store (709 chunks)
├── venv/                     # Python virtual environment
├── node_modules/             # Node.js dependencies (378 packages)
├── package.json              # Node.js project config (paths fixed)
├── package-lock.json         # Dependency lock file
├── jest.config.js            # Jest test configuration
├── .env                      # Merged Python + Node.js environment variables
├── requirements.txt          # Python dependencies
├── data/
├── logs/
├── reports/
└── ai-workflow/              # AI workflow process files
```

---

## 6. Issues and Resolutions

| # | Issue | Resolution |
|---|-------|------------|
| 1 | `src/` rename to `backend/` broke `package.json` entry points | Updated `main`, `start`, and `dev` fields |
| 2 | `retrieval.js` referenced `ingestion/venv/` which does not exist in 04 | Changed to `venv/` (root-level) |
| 3 | `query_chroma.py` referenced `ingestion/chroma_db/` | Changed to `chroma_db/` (root-level) |
| 4 | `query_chroma.py` had unnecessary `sys.path.insert` for `ingestion/` dir | Removed (chromadb installed in venv) |
| 5 | `config.js` fallback chroma path pointed to `ingestion/chroma_db` | Changed to `chroma_db` |
| 6 | `.env` conflict -- both Python and Node.js had separate `.env` files | Merged into single `.env` (no variable name conflicts) |
| 7 | 14 Jest test imports used `../src/` paths | Updated all to `../backend/` |
| 8 | `CHROMA_PATH` env var pointed to `./ingestion/chroma_db` | Changed to `./chroma_db` |

No unresolved issues remain.

---

## 7. Commands Reference

```bash
cd pilot_phase1_poc/04_retrieval_optimization

# Install Node.js dependencies
npm install

# Run Jest tests (backend)
npm test

# Start Express backend (port 3000)
npm start

# Start React frontend (port 5173)
cd client && npm run dev

# Run Python ingestion
venv\Scripts\activate && python scripts/ingest.py

# Run Python retrieval quality tests
venv\Scripts\activate && python scripts/retrieval_quality_test.py
```
