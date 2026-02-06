# Task 9B: Copy RAG Pipeline into 04_retrieval_optimization

## Persona

You are a DevOps engineer assembling a complete, self-contained RAG pipeline in `04_retrieval_optimization/`. The refined ingestion pipeline (scripts, ChromaDB, KB) already lives here. You need to bring over the Express backend, React frontend, and supporting files from `03_rag_pipeline/` so everything can be reviewed and tested as one deliverable.

## Context

### Current State of 04_retrieval_optimization

```
04_retrieval_optimization/
├── scripts/               ← Python ingestion pipeline (optimized, Week 3)
│   ├── ingest.py
│   ├── process_docs.py    ← Has pdfs/ exclusion fix
│   ├── config.py
│   ├── chunker.py
│   ├── verify_ingestion.py
│   ├── retrieval_quality_test.py
│   ├── pdf_extractor.py
│   └── view_chroma.py
├── chroma_db/             ← Optimized ChromaDB (709 chunks, 30 docs)
├── kb/                    ← Week 3 KB (30 docs, flat category folders)
├── tests/                 ← Python tests (test_pdf_extractor.py)
├── venv/                  ← Python virtual environment
├── .env                   ← Python ingestion config (CHUNK_SIZE=600, CHUNK_OVERLAP=90)
├── requirements.txt
├── data/
├── logs/
├── reports/
└── ai-workflow/
```

**Missing**: Express backend, React frontend, Python bridge, Jest tests, Node.js config.

### What to Copy from 03_rag_pipeline

```
03_rag_pipeline/
├── src/                   ← Express backend → COPY AS backend/
│   ├── index.js           ← Server entry point (port 3000)
│   ├── config.js          ← Loads .env, exports config object
│   ├── services/
│   │   ├── retrieval.js   ← Calls Python subprocess (query_chroma.py)
│   │   ├── llm.js         ← Groq Llama 3.1 8B
│   │   ├── pipeline.js    ← RAG orchestration
│   │   └── citations.js   ← Citation extraction
│   ├── routes/
│   │   ├── index.js       ← Route registry
│   │   └── query.js       ← POST /api/query
│   ├── middleware/
│   │   └── errorHandler.js
│   ├── prompts/
│   │   └── system.txt     ← LLM system prompt
│   └── utils/
│       └── logger.js
├── client/                ← React + Vite frontend → COPY AS-IS
├── scripts/
│   └── query_chroma.py    ← Python bridge → COPY TO scripts/
├── tests/                 ← Jest tests → MERGE INTO existing tests/
│   ├── *.test.js          ← 6 test files (105 tests)
│   ├── setup.js
│   └── e2e/               ← E2E Python tests
├── package.json           ← Node.js dependencies → COPY
├── package-lock.json      ← Lock file → COPY
├── jest.config.js         ← Jest config → COPY
└── .env                   ← Environment variables → COPY AS .env.node
```

### Critical Path Issues to Fix After Copying

1. **`src/` renamed to `backend/`**: All internal relative imports use `../` paths from `src/`. Since the folder is renamed, the `package.json` main field and any path references need updating:
   - `package.json`: `"main": "src/index.js"` → `"main": "backend/index.js"`
   - `package.json`: `"start": "node src/index.js"` → `"start": "node backend/index.js"`
   - `package.json`: `"dev": "node --watch src/index.js"` → `"dev": "node --watch backend/index.js"`

2. **`backend/config.js`**: Loads `.env` from `join(__dirname, '..', '.env')` — this resolves to the project root, which is correct. But the `.env` needs to be the Node.js one (with Groq API key, CHROMA_PATH, etc.), not the Python ingestion one. Solution: copy as `.env.node` and update `config.js` to load `.env.node`.

3. **`backend/services/retrieval.js`**: Has two hardcoded relative paths:
   ```js
   const QUERY_SCRIPT = join(__dirname, '..', '..', 'scripts', 'query_chroma.py');
   const PYTHON_PATH = join(__dirname, '..', '..', 'ingestion', 'venv', 'Scripts', 'python.exe');
   ```
   After rename to `backend/`:
   - `QUERY_SCRIPT`: `join(__dirname, '..', '..', 'scripts', 'query_chroma.py')` — still resolves correctly (backend/services/ → backend/ → root/ → scripts/)
   - `PYTHON_PATH`: `join(__dirname, '..', '..', 'ingestion', 'venv', ...)` — **WRONG**. There's no `ingestion/` folder in 04. The venv is at `./venv/`. Update to: `join(__dirname, '..', '..', 'venv', 'Scripts', 'python.exe')`

4. **`scripts/query_chroma.py`**: The Python bridge has:
   ```python
   sys.path.insert(0, str(Path(__file__).parent.parent / 'ingestion'))
   chroma_path = Path(__file__).parent.parent / 'ingestion' / 'chroma_db'
   ```
   In 04, there's no `ingestion/` folder. ChromaDB is at `./chroma_db/`. Update both paths:
   - `sys.path.insert(0, str(Path(__file__).parent.parent))` (or remove — not needed if chromadb is in venv)
   - `chroma_path = Path(__file__).parent.parent / 'chroma_db'`

5. **`.env` conflict**: 04 already has `.env` for Python ingestion (CHUNK_SIZE, CHUNK_OVERLAP). The Node.js `.env` has different vars (PORT, LLM_API_KEY, CHROMA_PATH). Solution: merge into single `.env` or use `.env.node`. Recommended: **merge into single `.env`** since there are no conflicts (different variable names).

6. **`jest.config.js`**: `testMatch: ['**/tests/**/*.test.js']` — works as-is since Jest tests go into `tests/`.

7. **`CHROMA_PATH` in .env**: Currently `./ingestion/chroma_db` — update to `./chroma_db`.

### Existing .env in 04_retrieval_optimization (Python ingestion)

```env
CHUNK_SIZE=600
CHUNK_OVERLAP=90
COLLECTION_NAME=waypoint_kb
```

### .env from 03_rag_pipeline (Node.js backend)

```env
PORT=3000
NODE_ENV=development
CHROMA_PATH=./ingestion/chroma_db    ← MUST CHANGE to ./chroma_db
COLLECTION_NAME=waypoint_kb
RETRIEVAL_TOP_K=10
RELEVANCE_THRESHOLD=0.15
MAX_CONTEXT_TOKENS=2000
LLM_PROVIDER=groq
LLM_API_KEY=<key>
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=500
```

## Task

### Step 1: Copy Files

```bash
# From project root: pilot_phase1_poc/

# 1. Express backend (renamed src → backend)
cp -r 03_rag_pipeline/src 04_retrieval_optimization/backend

# 2. React frontend
cp -r 03_rag_pipeline/client 04_retrieval_optimization/client

# 3. Python bridge
cp 03_rag_pipeline/scripts/query_chroma.py 04_retrieval_optimization/scripts/query_chroma.py

# 4. Jest tests (merge into existing tests/)
cp 03_rag_pipeline/tests/*.test.js 04_retrieval_optimization/tests/
cp 03_rag_pipeline/tests/setup.js 04_retrieval_optimization/tests/
cp -r 03_rag_pipeline/tests/e2e 04_retrieval_optimization/tests/e2e_node

# 5. Node.js config
cp 03_rag_pipeline/package.json 04_retrieval_optimization/
cp 03_rag_pipeline/package-lock.json 04_retrieval_optimization/
cp 03_rag_pipeline/jest.config.js 04_retrieval_optimization/
```

### Step 2: Merge .env Files

Merge the Node.js env vars into the existing `.env`. Keep the Python vars, add the Node.js vars, fix CHROMA_PATH:

```env
# Python Ingestion
CHUNK_SIZE=600
CHUNK_OVERLAP=90
COLLECTION_NAME=waypoint_kb

# Server
PORT=3000
NODE_ENV=development

# ChromaDB
CHROMA_PATH=./chroma_db

# Retrieval
RETRIEVAL_TOP_K=10
RELEVANCE_THRESHOLD=0.15
MAX_CONTEXT_TOKENS=2000

# LLM (Groq)
LLM_PROVIDER=groq
LLM_API_KEY=<copy from 03_rag_pipeline/.env>
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=500
```

### Step 3: Fix Paths

**3a. `package.json`** — update `src/` → `backend/`:
```json
"main": "backend/index.js",
"scripts": {
  "start": "node backend/index.js",
  "dev": "node --watch backend/index.js",
  "test": "node --experimental-vm-modules node_modules/jest/bin/jest.js"
}
```

**3b. `backend/services/retrieval.js`** — fix Python venv path:
```js
// OLD: const PYTHON_PATH = join(__dirname, '..', '..', 'ingestion', 'venv', 'Scripts', 'python.exe');
// NEW:
const PYTHON_PATH = join(__dirname, '..', '..', 'venv', 'Scripts', 'python.exe');
```

**3c. `scripts/query_chroma.py`** — fix ChromaDB path:
```python
# OLD: sys.path.insert(0, str(Path(__file__).parent.parent / 'ingestion'))
# OLD: chroma_path = Path(__file__).parent.parent / 'ingestion' / 'chroma_db'
# NEW:
chroma_path = Path(__file__).parent.parent / 'chroma_db'
```
Remove the `sys.path.insert` line (not needed — chromadb is in venv).

**3d. `backend/config.js`** — no change needed (loads `.env` from `join(__dirname, '..', '.env')` which resolves to project root).

### Step 4: Install Node.js Dependencies

```bash
cd 04_retrieval_optimization
npm install
```

### Step 5: Verify

```bash
# Jest tests
npm test
# Expect: 6 suites, 105 tests PASS

# Check paths resolve correctly
node -e "import('./backend/config.js').then(m => console.log(m.config))"
```

## Format

### Target Directory Structure After Completion

```
04_retrieval_optimization/
├── backend/               ← Express backend (was src/ in 03)
│   ├── index.js
│   ├── config.js
│   ├── services/
│   ├── routes/
│   ├── middleware/
│   ├── prompts/
│   └── utils/
├── client/                ← React + Vite frontend
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── scripts/               ← Python ingestion + query bridge
│   ├── ingest.py
│   ├── process_docs.py
│   ├── query_chroma.py    ← NEW (Python bridge)
│   ├── config.py
│   ├── chunker.py
│   ├── verify_ingestion.py
│   ├── retrieval_quality_test.py
│   ├── pdf_extractor.py
│   └── view_chroma.py
├── tests/                 ← Python + Jest tests combined
│   ├── __init__.py
│   ├── test_pdf_extractor.py   ← Python
│   ├── api.test.js             ← Jest (NEW)
│   ├── citations.test.js       ← Jest (NEW)
│   ├── llm.test.js             ← Jest (NEW)
│   ├── pipeline.test.js        ← Jest (NEW)
│   ├── retrieval.test.js       ← Jest (NEW)
│   ├── placeholder.test.js     ← Jest (NEW)
│   ├── setup.js                ← Jest (NEW)
│   └── e2e_node/               ← E2E tests (NEW)
├── chroma_db/             ← Optimized ChromaDB (709 chunks)
├── kb/                    ← Week 3 KB (30 docs)
├── venv/                  ← Python virtual environment
├── node_modules/          ← Node.js dependencies (NEW)
├── .env                   ← Merged Python + Node.js env vars
├── package.json           ← NEW
├── package-lock.json      ← NEW
├── jest.config.js         ← NEW
├── requirements.txt
└── ai-workflow/
```

### Output Report

Save to:
```
04-prompts/04-refinement/task_9b_copy_rag_pipeline/02-output/REPORT.md
```

Report structure:
1. **Summary**: What was copied, what was renamed, what paths were fixed
2. **Files Copied**: Full list with source → destination
3. **Path Fixes**: Each fix with before/after
4. **Test Results**: Jest test output, npm install success
5. **Issues**: Any problems and resolutions
