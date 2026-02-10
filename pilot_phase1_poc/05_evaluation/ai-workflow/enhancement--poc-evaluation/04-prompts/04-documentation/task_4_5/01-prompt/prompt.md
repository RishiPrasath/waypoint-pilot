# Task 4.5 Prompt — Project-Level README

## Persona
Technical writer creating a project-level README for a RAG-based customer service co-pilot POC.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Task**: 4.5 — Project-level README
- **Phase**: 4 (Documentation)
- **Dependencies**: T4.4 (Documentation index) — complete
- **Blocks**: None
- **Workspace**: `pilot_phase1_poc/05_evaluation/`

### Project Summary
Waypoint is a RAG-based customer service co-pilot for freight forwarding (3PL) companies in Singapore and Southeast Asia. Phase 1 POC has a curated knowledge base of 30 documents, a Python ingestion pipeline, a Node.js/Express API server, and a React frontend with a 4-section response card (answer, sources, related docs, confidence).

### Tech Stack
| Component | Technology | Version |
|-----------|------------|---------|
| Vector DB | ChromaDB | 0.5.23 |
| Embeddings | all-MiniLM-L6-v2 | via ONNX (384-d) |
| Document Processing | Python | 3.11+ |
| Backend | Node.js + Express | 18+ |
| Frontend | React + Tailwind CSS | React 19, Tailwind 3 |
| LLM | Groq API (Llama 3.1 8B) | llama-3.1-8b-instant |
| Testing | Jest + Vitest + pytest | Jest 29, Vitest 4, pytest 8 |

### Actual Folder Structure
```
05_evaluation/
├── backend/                    # Express API server
│   ├── config.js               # 14 configuration properties
│   ├── index.js                # Express app entry point
│   ├── middleware/              # Error + not-found handlers
│   ├── prompts/                # System prompt template
│   │   └── system.txt
│   ├── routes/                 # API routes
│   │   ├── query.js            # POST /api/query
│   │   └── health.js           # GET /api/health
│   ├── services/               # Core business logic
│   │   ├── pipeline.js         # Orchestrator (processQuery)
│   │   ├── retrieval.js        # ChromaDB bridge (Python subprocess)
│   │   ├── llm.js              # Groq LLM client
│   │   ├── citations.js        # Citation extraction + matching
│   │   ├── embedding.js        # Embedding service
│   │   └── index.js            # Service exports
│   ├── utils/                  # Utility functions
│   └── README.md               # Pointer README
├── client/                     # React frontend
│   ├── src/
│   │   ├── App.jsx             # Main app component
│   │   ├── components/         # 7 React components
│   │   ├── api/                # API client (submitQuery, checkHealth)
│   │   ├── types.js            # Response type definitions
│   │   └── test/               # Vitest component tests
│   └── README.md               # Pointer README
├── scripts/                    # Python scripts
│   ├── config.py               # Pipeline configuration
│   ├── process_docs.py         # Document discovery + parsing
│   ├── chunker.py              # Text chunking (600/90)
│   ├── ingest.py               # Ingestion orchestrator
│   ├── query_chroma.py         # ChromaDB query bridge (JSON stdin/stdout)
│   ├── evaluation_harness.py   # 6-metric automated evaluation
│   ├── retrieval_quality_test.py # 50-query hit rate test
│   ├── verify_ingestion.py     # Post-ingestion verification
│   ├── view_chroma.py          # ChromaDB inspector
│   ├── pdf_extractor.py        # PDF extraction utility
│   └── README.md               # Pointer README
├── kb/                         # Knowledge base (30 docs)
│   ├── 01_regulatory/          # Singapore Customs, ASEAN (14 docs)
│   ├── 02_carriers/            # Ocean & Air carriers (6 docs)
│   ├── 03_reference/           # Incoterms, HS codes (3 docs)
│   ├── 04_internal_synthetic/  # Policies, procedures (7 docs)
│   └── README.md               # Pointer README
├── tests/                      # Test suite
│   ├── *.test.js               # Jest backend tests (7 files)
│   ├── test_*.py               # pytest Python tests
│   ├── e2e_node/               # E2E test approach
│   └── README.md               # Pointer README
├── documentation/              # Full documentation (33 files)
│   ├── architecture/           # 6 architecture docs
│   ├── codebase/               # 18 codebase reference docs
│   ├── adrs/                   # 6 architecture decision records
│   ├── guides/                 # 3 user-facing guides
│   └── README.md               # Master documentation index (T4.4)
├── data/                       # Evaluation data
│   ├── evaluation_baselines.json
│   ├── evaluation_results.json
│   └── evaluation_results.csv
├── reports/                    # Evaluation reports
├── chroma_db/                  # ChromaDB persistent storage
├── demo/                       # Demo artifacts (Phase 5)
│   ├── presentation/           # React presentation app
│   └── selenium/               # Demo capture scripts
├── .env.example                # Environment template
├── package.json                # Node.js dependencies
├── requirements.txt            # Python dependencies
└── jest.config.js              # Jest configuration
```

### Environment Variables
From `.env.example` (Python-side):
- `CHUNK_SIZE=600`
- `CHUNK_OVERLAP=90`
- `COLLECTION_NAME=waypoint_kb`
- `CHROMA_PERSIST_PATH=./chroma_db`
- `KNOWLEDGE_BASE_PATH=./kb`
- `LOG_LEVEL=INFO`

Node.js backend also requires (in `.env`):
- `GROQ_API_KEY` — Groq API key for LLM
- `PORT=3000` — API server port

### Key Commands
```bash
# Python setup
py -3.11 -m venv venv
venv/Scripts/activate          # Windows
pip install -r requirements.txt

# Node.js setup
npm install
cd client && npm install && cd ..

# Ingestion
python scripts/ingest.py --clear    # Fresh ingestion
python scripts/verify_ingestion.py  # Verify chunks

# Backend
npm start                           # Start API (port 3000)
npm run dev                         # Dev mode with --watch

# Frontend
cd client && npm run dev            # Vite dev server (port 5173)

# Tests
npm test                            # Jest backend tests
cd client && npm run test           # Vitest frontend tests
python -m pytest tests/ -v          # pytest Python tests
python scripts/retrieval_quality_test.py  # 50-query hit rate

# Evaluation
python scripts/evaluation_harness.py     # Full 6-metric evaluation
```

### Evaluation Results (Round 4 — Final)
| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Deflection Rate | ≥ 40% | 87.2% | PASS |
| Citation Accuracy | ≥ 80% | 96.0% (adjusted) | PASS |
| Hallucination Rate | < 15% | 2.0% | PASS |
| OOS Handling | ≥ 90% | 100% | PASS |
| Avg Latency | < 5s | 1,182ms | PASS |
| System Stability | No crashes | Stable | PASS |

## Task

Create **1 project-level README** at `05_evaluation/README.md`.

**Content (in order):**
1. **Title + badge-style summary line** — project name, one-sentence description
2. **Quick Start** — 5-6 steps to get from clone to running (prerequisites, Python setup, Node setup, ingestion, start backend, start frontend)
3. **Architecture Overview** — High-level description of the hybrid Python/Node architecture, RAG pipeline flow (query → retrieval → context → LLM → response), and the 4-section response card
4. **Tech Stack** — Table from context above
5. **Folder Structure** — Tree diagram matching the actual layout above
6. **Commands Reference** — All commands from context above, grouped by category
7. **Evaluation Results** — Summary table of Round 4 metrics (all 6 targets met)
8. **Documentation** — Link to `documentation/README.md` (the master index from T4.4), brief mention of 38 files across 4 layers
9. **Knowledge Base** — Brief description: 30 curated documents across 4 categories, YAML frontmatter schema, ChromaDB with 709 chunks
10. **License / Status** — POC status note (Phase 1 complete, Phase 2 planned)

**Style:**
- Use relative links for all internal references
- Keep each section concise (README should be scannable, not exhaustive)
- No Mermaid diagrams — keep it plain Markdown for GitHub rendering
- Target length: 150-250 lines

## Validation
- [ ] Quick start section covers setup from scratch
- [ ] Architecture overview is accurate
- [ ] Folder structure matches actual layout
- [ ] All commands are correct and tested
- [ ] Links to documentation index

## Output

Create output report: `04-prompts/04-documentation/task_4_5/02-output/TASK_4.5_OUTPUT.md`

## Update on Completion

**MANDATORY — Update ALL 7 tracking locations:**
1. **Checklist**: `03-checklist/IMPLEMENTATION_CHECKLIST.md` — mark T4.5 `[x]`, update Phase 4 progress (5/9), Total (33/45, 73%)
2. **Roadmap Progress Tracker**: Phase 4 → `5`, Total → `33 | 73%`
3. **Roadmap Quick Reference**: T4.5 → `✅ Complete`
4. **Roadmap Detailed Entry**: T4.5 Status → `✅ Complete`, validation checkboxes `[x]`
5. **Bootstrap file**: `ai-workflow-bootstrap-prompt-v3.md` → `33/45 -- 73%`
6. **CLAUDE.md** (root): → `33/45 — 73%`
7. **AGENTS.md** (root): → `33/45 -- 73%`
