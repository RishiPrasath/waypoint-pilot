# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Waypoint is a RAG-based customer service co-pilot for freight forwarding companies, specifically targeting 3PL companies in Singapore and Southeast Asia. Phase 1 POC has detailed planning documents and a curated knowledge base of 29 documents.

**Target**: Customer service agents who need quick, accurate answers about shipment booking, customs regulations, and carrier information.

## Current Project Structure

```
waypoint-pilot/
├── pilot_phase1_poc/
│   ├── 00_docs/                    # Planning documents (numbered 00-06)
│   ├── 01_knowledge_base/          # Knowledge base root
│   │   ├── kb/                     # Content documents only (29 docs)
│   │   │   ├── 01_regulatory/      # Singapore Customs, ASEAN trade (14 docs)
│   │   │   ├── 02_carriers/        # Ocean & Air carriers (6 docs)
│   │   │   ├── 03_reference/       # Incoterms, HS codes (3 docs)
│   │   │   └── 04_internal_synthetic/  # Policies, procedures (6 docs)
│   │   ├── PROGRESS_CHECKLIST.md   # Meta file (outside kb/)
│   │   └── SCRAPER_EXECUTION_PLAN.md  # Meta file (outside kb/)
│   ├── 02_ingestion_pipeline/      # Document ingestion component (Week 1 - Complete)
│   │   ├── docs/                   # Pipeline plan and roadmap
│   │   ├── prompts/                # PCTF task prompts
│   │   └── CLAUDE.md               # Component-specific instructions
│   ├── 03_rag_pipeline/            # RAG Pipeline component (Week 2)
│   │   ├── docs/                   # Pipeline planning documents
│   │   │   ├── 00_week2_rag_pipeline_plan.md
│   │   │   └── 01_implementation_roadmap.md  <-- CHECK THIS FIRST
│   │   ├── prompts/                # PCTF task prompts
│   │   ├── src/                    # Node.js backend (created during tasks)
│   │   ├── client/                 # React UI (created during tasks)
│   │   ├── scripts/                # Python scripts
│   │   ├── tests/                  # Test files
│   │   └── logs/                   # Log files
│   ├── 04_retrieval_optimization/  # Retrieval Optimization (Week 3 - Complete)
│   │   ├── ai-workflow/            # Week 3 workflow
│   │   ├── kb/                     # Optimized KB (30 docs)
│   │   ├── scripts/                # Ingestion + retrieval testing
│   │   └── chroma_db/              # Vector store (92% hit rate)
│   └── 05_evaluation/              # Evaluation & Documentation (Week 4 - In Progress)
│       ├── ai-workflow/            # Week 4 workflow (enhancement--poc-evaluation)
│       ├── backend/                # Express API
│       ├── client/                 # React frontend (4-section card)
│       ├── scripts/                # Evaluation scripts
│       ├── data/                   # Baselines, test results
│       └── demo/                   # Presentation + Selenium
└── CLAUDE.md                       # This file
```

## Tech Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Vector DB | ChromaDB | 0.5.23 | Vector storage and retrieval |
| Embeddings | all-MiniLM-L6-v2 | via ONNX | 384-d embeddings (ChromaDB default) |
| Document Processing | Python | 3.11+ | Ingestion pipeline |
| Backend | Node.js + Express | 18+ | API server |
| Frontend | React + Tailwind | 18+ | Minimal UI |
| LLM | Groq API (Llama 3.1 8B) | - | Response generation |

## Ingestion Pipeline Commands

```bash
cd pilot_phase1_poc/02_ingestion_pipeline

# Setup (one-time)
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run ingestion
python scripts/ingest.py           # Full ingestion
python scripts/ingest.py --dry-run # Test without storing
python scripts/ingest.py --verbose # Show chunk details
python scripts/verify_ingestion.py # Run verification
```

## Key Architecture Decisions

1. **Hybrid Python/Node**: Document processing uses Python (better libraries), API uses Node.js
2. **Local-first**: ChromaDB and embeddings run locally; LLM via Groq API
3. **Knowledge base only**: Phase 1 has no live system integration (TMS/WMS, tracking, rates)
4. **Singapore-centric**: Regulatory scope limited to Singapore with SEA secondary coverage
5. **Minimal dependencies**: ChromaDB default embeddings via ONNX (no PyTorch/CUDA)

## RAG Pipeline Flow

1. **Query Processing**: Clean/normalize, generate embedding
2. **Retrieval**: Search ChromaDB (top-k=5), filter by relevance threshold (0.7)
3. **Context Assembly**: Format chunks with source attribution
4. **Generation**: LLM with constrained system prompt
5. **Response**: Include answer, sources, and confidence indicator

## Document Metadata Format

All knowledge base documents use YAML frontmatter:
```yaml
---
title: [Document Title]
source_org: [Organization name, e.g., "Singapore Customs"]
source_urls:
  - [Primary URL]
  - [Additional URLs if applicable]
source_type: [public_regulatory | public_carrier | synthetic_internal]
last_updated: [YYYY-MM-DD]
jurisdiction: [SG | MY | ID | TH | VN | PH | ASEAN | Global]
category: [customs | carrier | policy | procedure | reference]
use_cases: [UC-1.1, UC-2.3, etc.]
---
```

## Ingestion Pipeline Configuration

```python
EMBEDDING_MODEL = "default"  # ChromaDB built-in (all-MiniLM-L6-v2 via ONNX)
EMBEDDING_DIMENSIONS = 384
CHUNK_SIZE = 600        # chars (~150 tokens)
CHUNK_OVERLAP = 90      # 15% overlap
COLLECTION_NAME = "waypoint_kb"
# No API key required - runs fully offline
```

Target: ~350-400 chunks from 29 documents with 12 metadata fields each.

## Critical Constraints

- Responses must cite sources from knowledge base
- Must gracefully decline out-of-scope queries (live rates, tracking, bookings)
- Target 40% query deflection rate for POC success
- LLM API costs must stay under $10 total for POC

## Success Criteria

- 29 documents parsed, ~350-400 chunks generated
- Tier 1 tests (category retrieval): 8/8 pass
- Tier 2 tests (document retrieval): 10+/12 pass
- 80% citation accuracy

## Planning Documents

Located in `pilot_phase1_poc/00_docs/`:
- `00_pilot_overview.md` - Executive summary and document index
- `01_scope_definition.md` - What's in/out of scope
- `02_use_cases.md` - 50 test queries and expected behaviors
- `03_knowledge_base_blueprint.md` - Document collection plan
- `04_technical_architecture.md` - Stack and API specification
- `05_execution_roadmap.md` - 30-day implementation plan
- `06_evaluation_framework.md` - Metrics and go/no-go criteria

## Ingestion Pipeline Coordination Rules (Week 1 - Complete)

### Rule 1: Check Roadmap Before Any Task
- Read `pilot_phase1_poc/02_ingestion_pipeline/docs/01_implementation_roadmap.md` first
- Verify task status: ⬜ Not Started | 🟡 In Progress | ✅ Complete | ❌ Blocked
- Confirm all dependency tasks are complete before starting

### Rule 2: Create Task Folder On-Demand
When user requests a task from the roadmap:
1. Create folder: `pilot_phase1_poc/02_ingestion_pipeline/prompts/[GROUP]_[TASK]_[description]/`
2. Create `prompt.md` inside using PCTF format
3. Then execute the task
4. Create `REPORT.md` after completion

### Rule 3: Follow PCTF Format
All prompts must include:
- **P**ersona: Role and expertise
- **C**ontext: Background, current state, references, dependencies
- **T**ask: Objective, requirements, specs, constraints, acceptance criteria
- **F**ormat: Output structure, code style, docs, validation commands

### Rule 4: Update Roadmap After Completion
After each task:
1. Mark checkboxes `[x]` in `01_implementation_roadmap.md`
2. Update status: ⬜ → ✅
3. Update Progress Tracker totals

### Rule 5: Local venv Execution
Use local venv for execution:
```bash
cd pilot_phase1_poc/02_ingestion_pipeline
python scripts/ingest.py
```

### Rule 6: Validate Before Marking Complete
Run validation commands from roadmap before marking any task complete.

### Rule 7: Reference Component CLAUDE.md
For detailed tech stack, config, and task specifics, see:
`pilot_phase1_poc/02_ingestion_pipeline/CLAUDE.md`

### Rule 8: Test-Driven Development (TDD)
Follow TDD methodology for all code tasks:

1. **Write Tests First**: Before implementing any function/module, write failing tests that define expected behavior
2. **Red-Green-Refactor Cycle**:
   - **Red**: Write a failing test
   - **Green**: Write minimal code to make the test pass
   - **Refactor**: Clean up code while keeping tests green
3. **Test File Convention**:
   - Tests go in `tests/` directory
   - Test files mirror source: `scripts/chunker.py` → `tests/test_chunker.py`
4. **Run Tests Before Completion**: All tests must pass before marking a task complete
5. **Test Coverage**: Each public function should have at least one test case

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_process_docs.py -v
```

## RAG Pipeline Coordination Rules (Week 2)

### Rule 1: Check Roadmap Before Any Task
- Read `pilot_phase1_poc/03_rag_pipeline/docs/01_implementation_roadmap.md` first
- Verify task status: ⬜ Not Started | 🟡 In Progress | ✅ Complete | ❌ Blocked
- Confirm all dependency tasks are complete before starting

### Rule 2: Create Task Folder On-Demand
When user requests a task from the roadmap:
1. Create folder: `pilot_phase1_poc/03_rag_pipeline/prompts/[GROUP]_[TASK]_[description]/`
2. Create `prompt.md` inside using PCTF format
3. Then execute the task
4. Create `REPORT.md` after completion

### Rule 3: Use MCP Tools for Documentation
Before implementing library integrations:
1. Use `docfork:docfork_search_docs` to search library docs
2. Use `docfork:docfork_read_url` to read full documentation
3. Alternative: Use context7 MCP for library docs

### Rule 4: Follow TDD
- Python: `tests/test_<module>.py` with pytest
- Node.js: `tests/<module>.test.js` with Jest
- Red → Green → Refactor cycle

### Rule 5: Update Roadmap After Completion
After each task:
1. Mark checkboxes `[x]` in `01_implementation_roadmap.md`
2. Update status: ⬜ → ✅
3. Update Progress Tracker totals

### RAG Pipeline Commands
```bash
cd pilot_phase1_poc/03_rag_pipeline

# Ingestion (Python)
cd ingestion && python -m scripts.ingest --clear

# Node.js backend
npm install
npm start
npm test

# React UI
cd client && npm install && npm run dev
```

## Retrieval Optimization Coordination Rules (Week 3)

### Rule 1: Check Roadmap Before Any Task
- Read `pilot_phase1_poc/04_retrieval_optimization/ai-workflow/enhancement--retrieval-optimization/02-roadmap/IMPLEMENTATION_ROADMAP.md` first
- Verify task status: ⬜ Pending | 🔄 In Progress | ✅ Complete | ❌ Blocked
- Confirm all dependency tasks are complete before starting

### Rule 2: Follow AI Workflow Process
When user requests a task:
1. Check roadmap for task details
2. Generate prompt file at `04-prompts/[phase]/01-prompt/` → STOP
3. Wait for human to review and say "Execute"
4. Execute the task
5. Create output report at `04-prompts/[phase]/02-output/`
6. Update checklist and roadmap

### Rule 3: Protected Paths (Week 3)
Do NOT modify these (fork instead):
- `pilot_phase1_poc/02_ingestion_pipeline/` - Week 1 stable baseline
- `pilot_phase1_poc/01_knowledge_base/kb/` - Original KB baseline

### Rule 4: Week 3 Workspace
All Week 3 work happens in:
```bash
cd pilot_phase1_poc/04_retrieval_optimization

# Setup
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Ingestion
python scripts/ingest.py

# PDF Extraction
python scripts/pdf_extractor.py path/to/file.pdf

# Retrieval Testing
python scripts/retrieval_quality_test.py
```

### Rule 5: Week 3 Targets
| Metric | Baseline | Adjusted | Min Target | Stretch |
|--------|----------|----------|------------|---------|
| Hit Rate | 76% | 82% | 80% | 90% |

Reclassified as out-of-scope: Queries #36, #38, #44

---

## Evaluation & Documentation Coordination Rules (Week 4)

### Rule 1: Check Roadmap Before Any Task
- Read `pilot_phase1_poc/05_evaluation/ai-workflow/enhancement--poc-evaluation/02-roadmap/IMPLEMENTATION_ROADMAP.md` first
- Verify task status: ⬜ Pending | 🔄 In Progress | ✅ Complete | ❌ Blocked
- Confirm all dependency tasks are complete before starting

### Rule 2: Follow AI Workflow Process
When user requests a task:
1. Check roadmap for task details
2. Generate prompt file at `04-prompts/[phase]/task_N/01-prompt/` → STOP
3. Wait for human to review and say "Execute"
4. Execute the task
5. Create output report at `04-prompts/[phase]/task_N/02-output/`
6. Update checklist and roadmap

### Rule 3: Protected Paths (Week 4)
Do NOT modify these — all frozen from previous weeks:
- `pilot_phase1_poc/01_knowledge_base/` — Original KB baseline
- `pilot_phase1_poc/02_ingestion_pipeline/` — Week 1 stable
- `pilot_phase1_poc/03_rag_pipeline/` — Week 2 stable
- `pilot_phase1_poc/04_retrieval_optimization/` — Week 3 stable

### Rule 4: Week 4 Workspace
All Week 4 work happens in:
```bash
cd pilot_phase1_poc/05_evaluation

# Python setup
py -3.11 -m venv venv
venv/Scripts/activate
pip install -r requirements.txt

# Node.js setup
npm install

# Backend
npm start

# React frontend
cd client && npm run dev

# Ingestion
python scripts/ingest.py --clear

# Evaluation harness
python scripts/evaluation_test.py

# Tests
npm test                       # Jest backend tests
python -m pytest tests/ -v     # Python tests
```

### Rule 5: Week 4 Targets
| Metric | Target |
|--------|--------|
| Deflection Rate | ≥ 40% |
| Citation Accuracy | ≥ 80% |
| Hallucination Rate | < 15% |
| OOS Handling | ≥ 90% |
| Avg Latency | < 5s |
| System Stability | No crashes |

### Rule 6: Task Order
UX redesign → Testing (5 layers) → Fix loop → Documentation → Demo → Finalize

### Rule 7: New Dependencies
- Selenium — demo capture (`demo/selenium/requirements.txt`)
- framer-motion, react-mermaidjs, html2canvas — React presentation (`demo/presentation/package.json`)

### Rule 8: Presentation
Standalone Vite app in `demo/presentation/`:
- `npm run dev` — preview
- `npm run build` — static deploy

---

## Active Initiatives

| Initiative | Status | Path |
|------------|--------|------|
| Ingestion Pipeline (Week 1) | ✅ Complete | ./pilot_phase1_poc/02_ingestion_pipeline/ |
| RAG Pipeline (Week 2) | ✅ Complete | ./pilot_phase1_poc/03_rag_pipeline/ |
| Retrieval Optimization (Week 3) | ✅ Complete | ./pilot_phase1_poc/04_retrieval_optimization/ai-workflow/enhancement--retrieval-optimization/ |
| **Evaluation & Documentation (Week 4)** | 🔄 In Progress (28/45 — 62%) | ./pilot_phase1_poc/05_evaluation/ai-workflow/enhancement--poc-evaluation/ |

To work on Week 4:
1. Read plan: `./pilot_phase1_poc/05_evaluation/ai-workflow/enhancement--poc-evaluation/01-plan/DETAILED_PLAN.md`
2. Check roadmap: `./pilot_phase1_poc/05_evaluation/ai-workflow/enhancement--poc-evaluation/02-roadmap/IMPLEMENTATION_ROADMAP.md`
3. Say "Generate prompt for Task N" to start a task
