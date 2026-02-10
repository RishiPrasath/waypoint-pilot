# Waypoint Co-Pilot — Phase 1 POC

A RAG-based customer service co-pilot for freight forwarding companies in Singapore and Southeast Asia. Answers questions about shipment booking, customs regulations, carrier information, and internal policies using a curated knowledge base of 30 documents.

**Status**: Phase 1 POC complete | All 6 evaluation targets met | Phase 2 planned

---

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Groq API key (free tier at [console.groq.com](https://console.groq.com))

### Setup

```bash
# 1. Python environment
py -3.11 -m venv venv
venv/Scripts/activate            # Windows
# source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt

# 2. Node.js dependencies
npm install
cd client && npm install && cd ..

# 3. Environment variables
cp .env.example .env
# Edit .env and add: GROQ_API_KEY=your_key_here

# 4. Ingest knowledge base into ChromaDB
python scripts/ingest.py --clear

# 5. Start the backend API (port 3000)
npm start

# 6. Start the frontend (new terminal, port 5173)
cd client && npm run dev
```

Open [http://localhost:5173](http://localhost:5173) to use the co-pilot.

---

## Architecture Overview

Waypoint uses a hybrid Python/Node.js architecture:

- **Python** handles document ingestion and ChromaDB vector queries (better library support for NLP)
- **Node.js/Express** serves the REST API, orchestrates the RAG pipeline, and calls the Groq LLM
- **React** renders a 4-section response card (answer, sources, related docs, confidence indicator)

### RAG Pipeline Flow

```
User Query → Express API → Python subprocess (ChromaDB retrieval)
          → Format context with source attribution
          → Groq LLM (Llama 3.1 8B) generates answer with citations
          → Extract + match citations to sources
          → Calculate confidence (High/Medium/Low)
          → Return 4-section response card
```

The Python subprocess bridge (`query_chroma.py`) communicates via JSON over stdin/stdout, keeping the Node.js server stateless while leveraging ChromaDB's Python SDK.

---

## Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Vector DB | ChromaDB | 0.5.23 |
| Embeddings | all-MiniLM-L6-v2 | ONNX (384-d, runs locally) |
| Document Processing | Python | 3.11+ |
| Backend API | Node.js + Express | 18+ |
| Frontend | React + Tailwind CSS | React 19, Tailwind 3 |
| LLM | Groq API | Llama 3.1 8B Instant |
| Backend Tests | Jest | 29 |
| Frontend Tests | Vitest + Testing Library | Vitest 4 |
| Python Tests | pytest | 8+ |

---

## Folder Structure

```
05_evaluation/
├── backend/                    # Express API server
│   ├── config.js               # 14 configuration properties
│   ├── index.js                # App entry point, middleware, graceful shutdown
│   ├── middleware/              # Error + not-found handlers
│   ├── prompts/system.txt      # LLM system prompt template
│   ├── routes/                 # POST /api/query, GET /api/health
│   └── services/               # pipeline, retrieval, llm, citations, embedding
├── client/                     # React + Tailwind frontend
│   └── src/
│       ├── components/         # 7 components (ResponseCard, QueryInput, etc.)
│       ├── api/                # API client (submitQuery, checkHealth)
│       └── test/               # Vitest component tests
├── scripts/                    # Python pipeline scripts
│   ├── ingest.py               # Ingestion orchestrator (--clear, --dry-run)
│   ├── process_docs.py         # Document discovery + frontmatter parsing
│   ├── chunker.py              # Text chunking (600 chars, 90 overlap)
│   ├── query_chroma.py         # ChromaDB query bridge (JSON stdin/stdout)
│   ├── evaluation_harness.py   # 6-metric automated evaluation
│   └── retrieval_quality_test.py  # 50-query hit rate test
├── kb/                         # Knowledge base (30 documents)
│   ├── 01_regulatory/          # Singapore Customs, ASEAN trade (14 docs)
│   ├── 02_carriers/            # Ocean & air carriers (6 docs)
│   ├── 03_reference/           # Incoterms, HS codes (3 docs)
│   └── 04_internal_synthetic/  # Policies, procedures (7 docs)
├── tests/                      # Test suite (217 tests across 3 frameworks)
├── documentation/              # 33 documentation files (see below)
├── data/                       # Evaluation baselines + results
├── reports/                    # Evaluation reports
├── chroma_db/                  # ChromaDB persistent storage (709 chunks)
└── demo/                       # Presentation + demo capture (Phase 5)
```

---

## Commands Reference

### Ingestion

```bash
python scripts/ingest.py --clear     # Fresh ingestion (clears existing DB)
python scripts/ingest.py             # Incremental ingestion
python scripts/ingest.py --dry-run   # Preview without storing
python scripts/verify_ingestion.py   # Verify chunk counts and metadata
```

### Development

```bash
npm start                            # Start API server (port 3000)
npm run dev                          # Dev mode with --watch
cd client && npm run dev             # Vite dev server (port 5173)
```

### Testing

```bash
npm test                             # Jest backend tests (162 tests)
cd client && npm run test            # Vitest frontend tests
python -m pytest tests/ -v           # pytest Python tests (55 tests)
python scripts/retrieval_quality_test.py  # 50-query retrieval hit rate
```

### Evaluation

```bash
python scripts/evaluation_harness.py # Full 6-metric evaluation (requires running server)
```

---

## Evaluation Results

Round 4 (final) — all 6 targets met:

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Deflection Rate | ≥ 40% | 87.2% | PASS |
| Citation Accuracy | ≥ 80% | 96.0% (adjusted) | PASS |
| Hallucination Rate | < 15% | 2.0% | PASS |
| OOS Handling | ≥ 90% | 100% | PASS |
| Avg Latency | < 5s | 1,182 ms | PASS |
| System Stability | No crashes | Stable | PASS |

See [reports/evaluation_report.md](reports/evaluation_report.md) for the full evaluation report.

---

## Documentation

This project includes 38 documentation files organized into 4 layers:

| Layer | Type | Location |
|-------|------|----------|
| Layer 1 | Inline docs | JSDoc comments and Python docstrings in source files |
| Layer 2 | Pointer READMEs | `backend/`, `client/`, `scripts/`, `tests/`, `kb/` |
| Layer 3 | Detailed reference | `documentation/codebase/` (18 files) |
| Layer 4 | Architecture decisions | `documentation/adrs/` (6 ADRs) |

Plus 6 architecture docs and 3 user-facing guides.

Full index: [documentation/README.md](documentation/README.md)

---

## Knowledge Base

30 curated Markdown documents across 4 categories:

- **Regulatory** (14 docs) — Singapore Customs procedures, ASEAN trade regulations, permits
- **Carriers** (6 docs) — Maersk, ONE, Hapag-Lloyd, Singapore Airlines Cargo, Cathay Cargo
- **Reference** (3 docs) — Incoterms 2020, HS code classification, freight glossary
- **Internal** (7 docs) — Booking SOPs, escalation policies, SLA commitments

All documents use YAML frontmatter with 9 metadata fields (title, source_org, category, jurisdiction, etc.). The ingestion pipeline produces 709 chunks stored in ChromaDB with 13 metadata fields per chunk.

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | *(required)* | Groq API key for LLM calls |
| `PORT` | `3000` | Express API server port |
| `CHUNK_SIZE` | `600` | Characters per chunk |
| `CHUNK_OVERLAP` | `90` | Overlap between chunks |
| `COLLECTION_NAME` | `waypoint_kb` | ChromaDB collection name |
| `CHROMA_PERSIST_PATH` | `./chroma_db` | ChromaDB storage path |
| `KNOWLEDGE_BASE_PATH` | `./kb` | Knowledge base document path |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## Status

**Phase 1 POC**: Complete. All 6 evaluation targets met. The system answers freight forwarding questions with 96% citation accuracy and sub-1.2s latency using a 30-document knowledge base.

**Phase 2** (planned): Live system integration (TMS/WMS), expanded KB, production deployment. See [documentation/guides/known_limitations.md](documentation/guides/known_limitations.md) for detailed Phase 2 recommendations.
