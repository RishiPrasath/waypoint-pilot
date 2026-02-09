# Waypoint

**Guided Intelligence for Customer Service**

A RAG-based customer service co-pilot for freight forwarding companies in Singapore and Southeast Asia. Waypoint helps customer service agents instantly find accurate, source-cited answers across shipping documentation, customs regulations, carrier policies, and internal procedures — turning complex queries that typically require 30+ minutes of research into near-instant responses.

> **Status**: Phase 1 POC (active development) · Built by [CYAIRE](https://cyaire.com) (AI Solution Engineering, Singapore)

---

## Overview

Customer service agents in freight forwarding spend significant time searching for information across fragmented sources — government portals, carrier manuals, internal policy docs, and trade references. Waypoint consolidates these into a single, searchable knowledge base and uses retrieval-augmented generation to deliver accurate, cited answers in seconds.

### What It Does

- Answers booking, documentation, and procedural questions from a curated knowledge base of 29 documents
- Provides source citations with every response (document title, section, and source URLs)
- Detects out-of-scope queries (live tracking, rate quotes, bookings) and gracefully declines
- Shows confidence indicators (High / Medium / Low) based on retrieval quality
- Handles concurrent requests with average latency of 2–4 seconds

### What It Doesn't Do (Phase 1)

- No live TMS/WMS/ERP integration
- No real-time shipment tracking or rate quotations
- No booking execution or claims processing
- No multi-country regulatory comparisons (Singapore-centric)

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Semantic Retrieval** | ChromaDB vector search with all-MiniLM-L6-v2 embeddings (384-d) across ~480 indexed chunks |
| **Source Citations** | Every response includes document name, section header, and source URLs |
| **Confidence Scoring** | High / Medium / Low indicators based on chunk relevance and count |
| **Out-of-Scope Detection** | Identifies action requests (bookings, tracking) and redirects appropriately |
| **Multi-Source Synthesis** | Combines regulatory, carrier, reference, and internal policy documents in a single response |
| **Retrieval Optimization** | Retrieval-first content strategy with industry abbreviation mapping for logistics terminology |

---

## Architecture

```
┌─────────────┐     ┌─────────────────────────────────────────────────┐
│   React UI  │────▶│              Express API (Port 3000)            │
│ (Port 5173) │     │                                                 │
└─────────────┘     │  Query Handler → Retrieval → LLM → Citations   │
                    └─────────────────────────────────────────────────┘
                                        │
                      ┌─────────────────┼─────────────────┐
                      ▼                 ▼                 ▼
                ┌──────────┐     ┌──────────────┐   ┌──────────┐
                │ ChromaDB │     │  Groq API    │   │ Citation │
                │ (Local)  │     │ (Llama 3.1)  │   │ Extractor│
                └──────────┘     └──────────────┘   └──────────┘
```

### Data Flow

1. **Query Input** — User submits question via React UI or REST API
2. **Retrieval** — Query embedded and matched against ChromaDB (top-5 chunks, relevance threshold 0.3)
3. **Context Assembly** — Relevant chunks formatted with metadata for the LLM prompt
4. **Generation** — Groq LLM (Llama 3.1 8B) generates a response grounded in retrieved context
5. **Citation Extraction** — Citations parsed and matched back to source documents
6. **Response** — Answer returned with citations, confidence level, and latency metadata

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Vector Database | ChromaDB 0.5.23 | Local vector storage and semantic retrieval |
| Embeddings | all-MiniLM-L6-v2 (ONNX) | 384-dimensional embeddings (ChromaDB default) |
| LLM | Groq API — Llama 3.1 8B Instant | Response generation |
| Backend | Node.js 18+ / Express | REST API server |
| Frontend | React 18+ / Tailwind CSS / Vite | Chat interface |
| Document Processing | Python 3.11+ | Ingestion pipeline (chunking, embedding, indexing) |
| Text Splitting | LangChain RecursiveCharacterTextSplitter | Semantic chunking with header awareness |
| Testing | pytest (Python) / Jest (Node.js) | Unit + integration + E2E tests |

---

## Knowledge Base

29 curated documents organized into four categories:

```
kb/
├── 01_regulatory/          14 documents
│   ├── singapore_customs/      Singapore export/import, GST, FTZ, permits
│   ├── asean_trade/            ATIGA, RCEP, ASEAN tariff resources
│   └── country_specific/       Indonesia, Malaysia, Vietnam regulations
├── 02_carriers/             6 documents
│   ├── ocean/                  PIL, Maersk, ONE, Evergreen service guides
│   └── air/                    SIA Cargo, Cathay Cargo
├── 03_reference/            3 documents
│   ├── incoterms/              Incoterms 2020 comprehensive guide
│   └── hs_codes/               HS code classification reference
└── 04_internal_synthetic/   6 documents
    ├── policies/               Company service terms, SLA policies
    ├── procedures/             Booking procedures, escalation workflows
    └── service_guides/         Service scope, FAQ documents
```

All documents use YAML frontmatter with standardized metadata: `title`, `source_org`, `source_urls`, `source_type`, `last_updated`, `jurisdiction`, `category`, and `use_cases`.

---

## Project Structure

```
waypoint-pilot/
├── pilot_phase1_poc/
│   ├── 00_docs/                        Planning & specification documents
│   │   ├── 00_pilot_overview.md            Executive summary & document index
│   │   ├── 01_scope_definition.md          In/out scope, constraints
│   │   ├── 02_use_cases.md                 50 test queries across 4 categories
│   │   ├── 03_knowledge_base_blueprint.md  Source list & document templates
│   │   ├── 04_technical_architecture.md    Stack, API spec, system design
│   │   ├── 05_execution_roadmap.md         30-day week-by-week milestones
│   │   └── 06_evaluation_framework.md      Metrics, scoring rubric, go/no-go
│   │
│   ├── 01_knowledge_base/              Knowledge base root
│   │   └── kb/                             29 markdown documents (see above)
│   │
│   ├── 02_ingestion_pipeline/          Week 1 — Document ingestion (Python)
│   │   ├── scripts/                        process_docs, chunker, ingest, verify
│   │   ├── tests/                          87 pytest unit tests
│   │   ├── chroma_db/                      Vector database (auto-created)
│   │   └── requirements.txt
│   │
│   ├── 03_rag_pipeline/               Week 2 — RAG API + UI (Node.js)
│   │   ├── src/                            Express backend (routes, services, prompts)
│   │   ├── client/                         React + Tailwind frontend (Vite)
│   │   ├── scripts/                        Python E2E test suite
│   │   └── tests/                          105 Jest unit tests
│   │
│   ├── 04_retrieval_optimization/      Week 3 — KB rebuild + retrieval tuning
│   │   ├── backend/                        Forked Express backend
│   │   ├── client/                         Forked React frontend
│   │   ├── scripts/                        Enhanced ingestion + PDF extractor
│   │   ├── kb/                             Rebuilt knowledge base
│   │   └── Retrieval_Optimization_Plan.md
│   │
│   └── 05_evaluation/                 Week 4 — Final evaluation (planned)
│
├── CLAUDE.md                           Claude Code project instructions
├── AGENTS.md                           AI coding agent guide
└── .github/workflows/                  CI/CD (GitHub Actions)
```

---

## Getting Started

### Prerequisites

- **Node.js** 18+
- **Python** 3.11+ (ChromaDB does not support 3.14)
- **Groq API key** — [Get one free](https://console.groq.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/waypoint-pilot.git
cd waypoint-pilot

# --- Ingestion Pipeline (Python) ---
cd pilot_phase1_poc/02_ingestion_pipeline

# Create virtual environment
py -3.11 -m venv venv          # Windows
python3.11 -m venv venv        # macOS/Linux

# Activate
venv\Scripts\activate           # Windows
source venv/bin/activate        # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run ingestion (populates ChromaDB)
python -m scripts.ingest --clear

# Verify ingestion quality
python -m scripts.verify_ingestion

# --- RAG Pipeline (Node.js) ---
cd ../03_rag_pipeline

# Install backend
npm install

# Install frontend
cd client && npm install && cd ..

# Configure environment
cp .env.example .env
# Edit .env → add GROQ_API_KEY
```

### Running

```bash
# Terminal 1: Start backend API
cd pilot_phase1_poc/03_rag_pipeline
npm start
# → http://localhost:3000

# Terminal 2: Start frontend UI
cd pilot_phase1_poc/03_rag_pipeline/client
npm run dev
# → http://localhost:5173
```

### Quick Test

```bash
# Health check
curl http://localhost:3000/api/health

# Query
curl -X POST http://localhost:3000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the GST rate in Singapore?"}'
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | — | **Required.** Groq API key |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | LLM model identifier |
| `PORT` | `3000` | Express server port |
| `CHROMA_PATH` | `./chroma_data` | ChromaDB storage directory |
| `COLLECTION_NAME` | `waypoint_kb` | ChromaDB collection name |
| `LOG_LEVEL` | `info` | Logging: debug / info / warn / error |

### Retrieval Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `RETRIEVAL_TOP_K` | `5` | Number of chunks to retrieve per query |
| `RELEVANCE_THRESHOLD` | `0.3` | Minimum similarity score to include a chunk |
| `MAX_CONTEXT_CHARS` | `4000` | Maximum context window for LLM prompt |

### Chunking Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| Chunk size | 600 characters (~150 tokens) | Target size per chunk |
| Chunk overlap | 90 characters (15%) | Overlap between consecutive chunks |
| Separators | `\n## `, `\n### `, `\n\n`, `\n` | Split priority (header-aware) |

---

## Evaluation & Metrics

### Target KPIs

| Metric | Target | Stretch | Minimum Viable |
|--------|--------|---------|----------------|
| Query Deflection Rate | 40% | 50% | 30% |
| Citation Accuracy | 80% | 95% | 70% |
| Hallucination Rate | <15% | <5% | <20% |
| Response Latency | <5s avg | <3s avg | <10s |
| Retrieval Hit Rate | 80% | 90% | 76% |

### Test Suite

50 test queries across four categories:

| Category | Queries | Examples |
|----------|---------|---------|
| UC-1.x Booking & Documentation | ~15 | Export docs, lead times, Incoterms |
| UC-2.x Customs & Regulatory | ~15 | GST, HS codes, ATIGA, permits |
| UC-3.x Carrier Information | ~10 | Transit times, service coverage, restrictions |
| UC-4.x SLA & Service Scope | ~10 | Delivery SLAs, service inclusions |

### Running Tests

```bash
# Python unit tests (ingestion pipeline)
cd pilot_phase1_poc/02_ingestion_pipeline
python -m pytest tests/ -v                    # 87 tests

# Node.js unit tests (RAG pipeline)
cd pilot_phase1_poc/03_rag_pipeline
npm test                                       # 105 tests

# Ingestion verification (30 semantic queries)
cd pilot_phase1_poc/02_ingestion_pipeline
python -m scripts.verify_ingestion --verbose

# E2E test suite (30 end-to-end tests)
cd pilot_phase1_poc/03_rag_pipeline
python scripts/e2e_test_suite.py
```

### Scoring Rubric

| Score | Label | Deflected? |
|-------|-------|-----------|
| 5 | Excellent — complete, accurate, cited | ✅ |
| 4 | Good — accurate, minor gaps | ✅ |
| 3 | Partial — relevant but incomplete | ❌ |
| 2 | Poor — significant errors | ❌ |
| 1 | Failed — incorrect or irrelevant | ❌ |
| 0 | Appropriate Decline — correctly out-of-scope | Separate metric |

---

## Roadmap

### Phase 1 POC — 30 Days (Current)

| Week | Focus | Status |
|------|-------|--------|
| Week 1 | Foundation: knowledge base + ingestion pipeline | ✅ Complete |
| Week 2 | RAG pipeline: API + UI + E2E testing | ✅ Complete |
| Week 3 | Retrieval optimization: KB rebuild + tuning | ✅ Complete |
| Week 4 | Final evaluation + documentation | ⬜ Planned |

---

## Limitations & Scope

### Explicitly Excluded (Phase 1)

| Exclusion | Reason |
|-----------|--------|
| Live TMS/WMS integration | Requires system access; Phase 2+ |
| Real-time tracking | Needs carrier API integration |
| Booking execution | Transaction processing out of scope |
| Rate quotations | Requires live rate data |
| Claims processing | Complex multi-step workflow; Phase 3 |
| Hazmat / DG shipments | High complexity, high risk |
| Multi-country regulatory comparison | Singapore-first to limit scope |

### Known Limitations

- **LLM variability**: Response times vary with Groq API load (1–15s range)
- **Knowledge scope**: Limited to 29 curated documents (~480 chunks)
- **Abbreviation matching**: Embedding model cannot natively match logistics abbreviations (e.g., "BL" → "Bill of Lading") without explicit keyword mapping in documents
- **No conversation memory**: Each query is independent; no multi-turn context

---

## License

Internal use only — CYAIRE / Waypoint Phase 1 POC
