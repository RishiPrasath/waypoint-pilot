# Waypoint

**Guided Intelligence for Customer Service**

A RAG-based customer service co-pilot for freight forwarding companies in Singapore and Southeast Asia. Waypoint helps customer service agents instantly find accurate, source-cited answers across shipping documentation, customs regulations, carrier policies, and internal procedures — turning complex queries that typically require 30+ minutes of research into near-instant responses.

> **Status**: Phase 1 POC complete. Phase 2 POC has completed Partner Source Slice 1, including Spring Boot, FastAPI, and parity checks; `rag-db`, BFF orchestration, and frontend clients are next. Built by [CYAIRE](https://cyaire.com) (AI Solution Engineering, Singapore)

---

## Overview

Customer service agents in freight forwarding spend significant time searching for information across fragmented sources — government portals, carrier manuals, internal policy docs, and trade references. Waypoint consolidates these into a single, searchable knowledge base and uses retrieval-augmented generation to deliver accurate, cited answers in seconds.

Phase 2 is the current product direction. It expands the original knowledge-only pilot into a contract-driven logistics support platform: operational logistics data comes from `partner-source`, knowledge answers come from the RAG layer, and a later BFF will orchestrate both into a chatbot frontend for customer service agents and a delivery app frontend for delivery drivers.

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

## Current Phase 2 Architecture

Phase 2 separates operational truth from knowledge retrieval so the assistant can answer both data-backed and policy-backed questions without blurring responsibilities.

```text
Chatbot frontend                 Delivery app frontend
for customer service agents      for delivery drivers
             |                              |
             +--------------+---------------+
                            |
                            v
                  BFF orchestration layer
                            |
              +-------------+-------------+
              |                           |
              v                           v
      partner-source                    rag-db
      Operational logistics truth       Retrieval and knowledge layer
      - order status                    - document ingestion
      - order timeline                  - hybrid retrieval
      - drivers and assignments         - query planning
      - status events                   - citations and safeguards
              |                           |
              +-------------+-------------+
                            v
             Grounded client-specific response
```

### Module Boundaries

| Module | Owns | Does Not Own |
|--------|------|--------------|
| `partner-source` | Orders, drivers, assignments, status events, deterministic seed data, and API contract behavior. | Chatbot wording, RAG answers, frontend view models, retrieval logic. |
| `rag-db` | Knowledge sources, ingestion, retrieval, query planning, chunk/source validation, safeguards, and evaluation. | Partner order state, driver assignments, delivery status mutations, UI formatting. |
| `bff` | Service orchestration, client-specific response shaping, timeout handling, and combining operational data with retrieved knowledge for both frontend clients. | Source-of-truth persistence, retrieval internals, framework-specific API behavior, long-lived client state. |
| `chatbot-frontend` | Chatbot experience for customer service agents: order questions, policy/procedure answers, citations, confidence display, and escalation states. | Delivery app workflows, status mutation rules, backend business rules, retrieval ranking. |
| `delivery-app-frontend` | Delivery app experience for delivery drivers: driver profile, assigned orders, delivery details, and status-update actions. | Customer service chatbot wording, RAG answer generation, order source-of-truth persistence, transition rules. |

### What Phase 2 Proves Today

| Capability | Evidence |
|------------|----------|
| Contract-first partner API | Shared OpenAPI contract, shared error model, manual HTTP checklist, and deterministic seed scenarios. |
| Spring Boot reference implementation | Partner Source Slice 1 implemented and covered by focused, integration, and final-gate tests. |
| FastAPI parity implementation | Same Slice 1 behavior implemented against the shared contract and Spring Boot reference behavior. |
| Cross-stack parity | Latest local parity report: 24 scenarios passed, 0 failed, 0 skipped. |
| Operational question support | Current endpoints support customer questions like "Where is my order?" and driver questions like "What orders are assigned to me?" through order status, timeline, drivers, assignments, and status events. |
| Next architecture step | Pin `rag-db` and BFF contracts, then connect `partner-source` and `rag-db` behind client-shaped responses for the customer-service chatbot frontend and delivery-driver app frontend. |

## Phase 1 RAG Foundation

Phase 1 proved the knowledge-retrieval foundation: document ingestion, semantic retrieval, source-cited generation, confidence indicators, out-of-scope handling, and evaluation.

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

### Phase 1 Data Flow

1. **Query Input** — User submits question via React UI or REST API
2. **Retrieval** — Query embedded and matched against ChromaDB (top-5 chunks, relevance threshold 0.3)
3. **Context Assembly** — Relevant chunks formatted with metadata for the LLM prompt
4. **Generation** — Groq LLM (Llama 3.1 8B) generates a response grounded in retrieved context
5. **Citation Extraction** — Citations parsed and matched back to source documents
6. **Response** — Answer returned with citations, confidence level, and latency metadata

---

## Tech Stack

### Phase 2 POC

Phase 2 is tracked as modules and client components. Technology choices stay inside each module once that module is active.

| Module / Component | Role | Current State |
|--------------------|------|---------------|
| `partner-source` | Operational logistics source for orders, timelines, drivers, assignments, and status events. | Slice 1 complete with Spring Boot, FastAPI, OpenAPI contract, and parity checks. |
| `rag-db` | Knowledge and retrieval layer for ingestion, query planning, citations, safeguards, and evaluation. | Next module to plan and build. |
| `bff` | Orchestration layer that combines Partner Source data with RAG answers and shapes client responses. | Planned after `rag-db` and BFF contracts are pinned. |
| `chatbot-frontend` | Chatbot application for customer service agents. | Planned after BFF contract. |
| `delivery-app-frontend` | Delivery app for delivery drivers. | Planned after BFF contract. |
| Regression gates | Per-module checks, contract checks, parity checks, and later cross-component checks. | Partner Source gates complete; expand as new modules are built. |

### Phase 1 Definitive Application

| Component | Technology | Purpose |
|-----------|------------|---------|
| Vector Database | ChromaDB 0.5.23 | Local vector storage and semantic retrieval |
| Embeddings | all-MiniLM-L6-v2 (ONNX) | 384-dimensional embeddings (ChromaDB default) |
| LLM | Groq API — Llama 3.1 8B Instant | Response generation |
| Backend | Node.js 18+ / Express | REST API server |
| Frontend | React 19 / Tailwind CSS / Vite | Final evaluation chat interface |
| Document Processing | Python 3.11+ | Ingestion pipeline (chunking, embedding, indexing) |
| Text Splitting | LangChain RecursiveCharacterTextSplitter | Semantic chunking with header awareness |
| Evaluation | pytest, Jest, Vitest, retrieval test, evaluation harness | Final Phase 1 proof package |

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
│   └── 05_evaluation/                 Week 4 — definitive Phase 1 app + evaluation (complete)
│
├── pilot_phase2_poc/
│   └── partner-source/                Phase 2 — Synthetic logistics partner API
│       ├── docs/                      Local source-of-truth docs, contracts, and handoffs
│       ├── partner-source-springboot/ Spring Boot reference implementation
│       ├── partner-source-fastapi/    FastAPI contract-parity implementation
│       └── parity/                    Spring Boot vs FastAPI parity harness and reports
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

For Phase 1, use `pilot_phase1_poc\05_evaluation`. Earlier Phase 1 folders are build history; the evaluation folder is the definitive runnable application.

```powershell
# Clone the repository
git clone https://github.com/your-org/waypoint-pilot.git
cd waypoint-pilot

# --- Phase 1 final evaluation app ---
cd pilot_phase1_poc\05_evaluation

# Create virtual environment
py -3.11 -m venv venv

# Activate
.\venv\Scripts\Activate.ps1      # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Configure environment
Copy-Item .env.example .env
# Edit .env and set LLM_API_KEY=gsk_your_key_here

# Run ingestion (populates ChromaDB)
python scripts\ingest.py --clear

# Verify ingestion quality
python scripts\verify_ingestion.py

# --- Node.js application dependencies ---
npm install

# Install frontend
Push-Location client
npm install
Pop-Location
```

### Running

Use the startup script for the final Phase 1 app:

```powershell
cd pilot_phase1_poc\05_evaluation
.\start.ps1
```

Manual startup is also fine:

```powershell
# Terminal 1: Start backend API
cd pilot_phase1_poc\05_evaluation
npm start
# http://localhost:3000

# Terminal 2: Start frontend UI
cd pilot_phase1_poc\05_evaluation\client
npm run dev
# http://localhost:5173
```

### Phase 2 Partner Source

```powershell
# Spring Boot reference implementation
cd pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test

# FastAPI parity implementation
cd ..\partner-source-fastapi
uv run pytest

# Parity harness tests
cd ..\parity
python -m pytest
```

To run the live parity report, start Spring Boot on `http://localhost:8080`, start FastAPI on `http://localhost:8000`, then run:

```powershell
cd pilot_phase2_poc\partner-source\parity
python -m parity_runner
```

### Quick Test

```powershell
# Health check
Invoke-RestMethod http://localhost:3000/api/health

# Query
$body = @{ query = "What is the GST rate in Singapore?" } | ConvertTo-Json
Invoke-RestMethod http://localhost:3000/api/query -Method Post -ContentType "application/json" -Body $body
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_API_KEY` | required | Groq API key used by the OpenAI-compatible client |
| `LLM_MODEL` | `llama-3.1-8b-instant` | LLM model identifier |
| `LLM_BASE_URL` | `https://api.groq.com/openai/v1` | OpenAI-compatible LLM endpoint |
| `PORT` | `3000` | Express server port |
| `CHROMA_PATH` | `./chroma_db` | ChromaDB storage directory used by the backend |
| `COLLECTION_NAME` | `waypoint_kb` | ChromaDB collection name |
| `LOG_LEVEL` | `INFO` | Python script logging verbosity |

### Retrieval Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `RETRIEVAL_TOP_K` | `10` | Number of chunks to retrieve per query |
| `RELEVANCE_THRESHOLD` | `0.15` | Minimum similarity score to include a chunk |
| `MAX_CONTEXT_TOKENS` | `2000` | Maximum context size for LLM prompt construction |

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

```powershell
cd pilot_phase1_poc\05_evaluation

# Backend tests
npm test

# Frontend tests
Push-Location client
npm test
Pop-Location

# Python tests and retrieval quality
python -m pytest tests -v
python scripts\retrieval_quality_test.py

# Full evaluation harness; requires the backend to be running
python scripts\evaluation_harness.py
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

### Phase 1 POC — 30 Days (Complete)

| Week | Focus | Status |
|------|-------|--------|
| Week 1 | Foundation: knowledge base + ingestion pipeline | ✅ Complete |
| Week 2 | RAG pipeline: API + UI + E2E testing | ✅ Complete |
| Week 3 | Retrieval optimization: KB rebuild + tuning | ✅ Complete |
| Week 4 | Final evaluation + documentation | ✅ Complete |

### Phase 2 POC — Component Status

| Component | Purpose | Status |
|-----------|---------|--------|
| Partner Source contract | Shared OpenAPI and error contract for order status, timelines, drivers, assignments, and status events. | Slice 1 complete |
| Partner Source Spring Boot API | Reference implementation for the Partner Source Slice 1 contract. | Complete and tested |
| Partner Source FastAPI API | Independent implementation proving the same behavior across another stack. | Complete and tested |
| Partner Source parity harness | Local comparison runner for Spring Boot and FastAPI responses across shared scenarios. | Complete; latest report: 24 passed, 0 failed, 0 skipped |
| `rag-db` | Retrieval module for policy/procedure knowledge, citations, safeguards, and query planning. | Planned next component |
| `bff` | Orchestration layer that combines Partner Source operational truth with RAG answers and shapes client responses. | Planned after component contracts are pinned |
| Chatbot frontend for customer service agents | Customer service experience for order questions, policy answers, and grounded assistant responses. | Planned after BFF contract |
| Delivery app frontend for delivery drivers | Driver experience for profile, assigned orders, delivery details, and status updates. | Planned after BFF contract |

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

Internal use only — CYAIRE / Waypoint POC
