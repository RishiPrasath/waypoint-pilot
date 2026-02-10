# Deployment Notes — Waypoint Co-Pilot

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Node.js | 18+ | With npm (for backend API and frontend) |
| Python | 3.11+ | With pip and venv support |
| Git | Any | For cloning the repository |
| Groq API Key | — | Free tier at https://console.groq.com |
| Disk Space | ~500MB | ChromaDB + ONNX model + node_modules + Python venv |
| Browser | Chrome recommended | For the React frontend |

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/RishiPrasath/waypoint-pilot.git
cd waypoint-pilot/pilot_phase1_poc/05_evaluation
```

### 2. Python Environment Setup

```bash
# Create virtual environment
py -3.11 -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Key Python packages:**
- `chromadb==0.5.23` — Vector database with built-in embeddings
- `langchain-text-splitters==0.0.1` — Document chunking
- `python-frontmatter==1.1.0` — YAML frontmatter parsing
- `pymupdf4llm>=0.0.17` — PDF extraction (reference tool)

### 3. Node.js Backend Setup

```bash
npm install
```

**Key Node.js packages:**
- `express` — REST API framework
- `openai` — Groq API client (OpenAI-compatible)
- `cors` — Cross-origin request support
- `dotenv` — Environment variable loading

### 4. React Frontend Setup

```bash
cd client
npm install
cd ..
```

**Key frontend packages:**
- `react` + `react-dom` — UI framework
- `react-markdown` + `remark-gfm` — Markdown rendering
- `tailwindcss` — Utility-first CSS

### 5. Environment Configuration

Create a `.env` file in the project root (`pilot_phase1_poc/05_evaluation/`):

```bash
# === REQUIRED ===
LLM_API_KEY=gsk_your_groq_api_key_here

# === OPTIONAL (defaults shown) ===

# Server
PORT=3000
NODE_ENV=development

# ChromaDB
CHROMA_PATH=./chroma_db
COLLECTION_NAME=waypoint_kb

# Retrieval
RETRIEVAL_TOP_K=10
RELEVANCE_THRESHOLD=0.15
MAX_CONTEXT_TOKENS=2000

# LLM
LLM_PROVIDER=groq
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=500

# Python-side
CHUNK_SIZE=600
CHUNK_OVERLAP=90
KNOWLEDGE_BASE_PATH=./kb
CHROMA_PERSIST_PATH=./chroma_db
LOG_LEVEL=INFO
```

> **Note**: The only required variable is `LLM_API_KEY`. All others have sensible defaults. Get a free Groq API key at https://console.groq.com.

### 6. Run Ingestion

Build the vector store from the knowledge base documents:

```bash
# Activate Python venv first, then:
python scripts/ingest.py --clear
```

Expected output:
```
Processing documents...
  [1/30] 01_regulatory_asean_customs_transit: 22 chunks [stored]
  [2/30] 01_regulatory_asean_tariff_classification: 18 chunks [stored]
  ...
  [30/30] 04_internal_synthetic_faq: 15 chunks [stored]

Summary
  Documents processed: 30
  Chunks processed:    709
  Stored:              709
```

Verify ingestion:
```bash
python scripts/verify_ingestion.py
```

## Starting the System

You need **two terminal windows**:

### Terminal 1 — Backend API

```bash
cd pilot_phase1_poc/05_evaluation
npm start
```

Output: `Server started { port: 3000, env: 'development' }`

Verify: `curl http://localhost:3000/api/health` should return `{"status":"ok",...}`

### Terminal 2 — Frontend

```bash
cd pilot_phase1_poc/05_evaluation/client
npm run dev
```

Output: `Local: http://localhost:5173/`

Open `http://localhost:5173` in your browser to use the application.

## Running Tests

```bash
# Backend tests (Jest) — 162 tests
npm test

# Frontend tests (Vitest) — component tests
cd client && npm test

# Python tests (pytest) — 55 tests
python -m pytest tests/ -v

# Retrieval quality test — 50-query hit rate
python scripts/retrieval_quality_test.py
```

## Directory Structure

```
05_evaluation/
├── .env                    # Environment config (create from .env.example)
├── package.json            # Node.js dependencies and scripts
├── requirements.txt        # Python dependencies
├── backend/                # Express API server
│   ├── index.js            # Server entry point
│   ├── config.js           # Configuration loader
│   ├── services/           # Pipeline, retrieval, LLM, citations
│   ├── routes/             # API endpoints
│   ├── middleware/          # Error handling
│   ├── prompts/            # System prompt template
│   └── utils/              # Logger
├── client/                 # React frontend (Vite)
│   ├── src/
│   │   ├── App.jsx         # Main application shell
│   │   ├── api/            # API client
│   │   └── components/     # UI components (7 files)
│   └── package.json
├── scripts/                # Python scripts
│   ├── ingest.py           # Ingestion entry point
│   ├── process_docs.py     # Document parser
│   ├── chunker.py          # Text splitter
│   ├── query_chroma.py     # ChromaDB query bridge
│   ├── config.py           # Python configuration
│   └── verify_ingestion.py # Ingestion verification
├── kb/                     # Knowledge base (30 markdown docs)
│   ├── 01_regulatory/      # 14 docs
│   ├── 02_carriers/        # 6 docs
│   ├── 03_reference/       # 3 docs
│   └── 04_internal_synthetic/ # 6 docs (+ 1 FAQ)
├── chroma_db/              # ChromaDB vector store (generated)
└── tests/                  # Test files (Python + Jest)
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `LLM_API_KEY environment variable is required` | Missing `.env` file or key | Create `.env` with `LLM_API_KEY=gsk_...` |
| `Python query failed` on first query | ChromaDB not populated | Run `python scripts/ingest.py --clear` |
| `ECONNREFUSED` on frontend | Backend not running | Start backend first: `npm start` |
| Port 3000 already in use | Stale Node.js process | Find PID: `netstat -ano | findstr :3000`, then kill: `taskkill /PID <pid> /F` |
| Port 5173 already in use | Stale Vite process | Find PID: `netstat -ano | findstr :5173`, then kill: `taskkill /PID <pid> /F` |
| `Failed to spawn Python process` | Missing venv or wrong Python | Verify `venv/Scripts/python.exe` exists; re-create venv if needed |
| Groq 429 (rate limit) | Too many requests too fast | Wait 60 seconds; Groq free tier allows ~30 requests/minute |
| `No relevant chunks found` for valid queries | ChromaDB empty or corrupted | Re-run ingestion: `python scripts/ingest.py --clear` |
| Frontend shows CORS error | Backend not running or wrong port | Ensure backend runs on port 3000 (default CORS expects this) |
| `ModuleNotFoundError` in Python | Venv not activated | Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` |
| Jest tests fail with import errors | Missing `--experimental-vm-modules` | Use `npm test` (already configured in package.json) |

## Updating the Knowledge Base

When knowledge base documents are added or modified:

```bash
# 1. Add/edit documents in kb/ (follow frontmatter schema)
# 2. Re-run ingestion to rebuild the vector store
python scripts/ingest.py --clear

# 3. Verify the new document count and chunk totals
python scripts/verify_ingestion.py

# 4. Test retrieval with relevant queries
python scripts/retrieval_quality_test.py
```

See [kb_schema.md](../architecture/kb_schema.md) for the full frontmatter schema and document structure.

## Related Documentation

- [User Guide](user_guide.md) — How CS agents use the system
- [Known Limitations](known_limitations.md) — System constraints and gaps
- [System Overview](../architecture/system_overview.md) — Architecture and tech stack
- [API Contract](../architecture/api_contract.md) — REST API specification
