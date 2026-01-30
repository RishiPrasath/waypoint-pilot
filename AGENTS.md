# Waypoint - AI Coding Agent Guide

This document provides essential information for AI coding agents working on the Waypoint project. Read this file first before making any changes.

---

## Project Overview

**Waypoint** is a RAG-based customer service co-pilot for freight forwarding companies, specifically targeting 3PL (Third-Party Logistics) companies in Singapore and Southeast Asia.

**Target Users**: Customer service agents who need quick, accurate answers about:
- Shipment booking procedures
- Customs regulations (Singapore, ASEAN)
- Carrier information (ocean and air)
- Internal policies and SLAs

**Phase 1 Scope**: Knowledge-base only RAG system with 29 curated documents. No live system integration (TMS/WMS, tracking, rates) in this phase.

---

## Project Structure

```
waypoint-pilot/
├── pilot_phase1_poc/
│   ├── 00_docs/                    # Planning documents (00-06)
│   │   ├── 00_pilot_overview.md
│   │   ├── 01_scope_definition.md
│   │   ├── 02_use_cases.md
│   │   ├── 03_knowledge_base_blueprint.md
│   │   ├── 04_technical_architecture.md
│   │   ├── 05_execution_roadmap.md
│   │   └── 06_evaluation_framework.md
│   │
│   ├── 01_knowledge_base/          # Knowledge base root
│   │   ├── kb/                     # Content documents only (29 docs)
│   │   │   ├── 01_regulatory/      # Singapore Customs, ASEAN trade (14 docs)
│   │   │   ├── 02_carriers/        # Ocean & Air carriers (6 docs)
│   │   │   ├── 03_reference/       # Incoterms, HS codes (3 docs)
│   │   │   └── 04_internal_synthetic/  # Policies, procedures (6 docs)
│   │   ├── PROGRESS_CHECKLIST.md   # Meta file (outside kb/)
│   │   └── SCRAPER_EXECUTION_PLAN.md  # Meta file (outside kb/)
│   │
│   ├── 02_ingestion_pipeline/      # Document ingestion component (Week 1 - Complete)
│   │   ├── scripts/                # Python modules
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # Configuration module
│   │   │   ├── process_docs.py     # Document discovery and parsing
│   │   │   ├── chunker.py          # Text chunking with metadata
│   │   │   ├── ingest.py           # Main ingestion orchestrator
│   │   │   └── verify_ingestion.py # Quality verification
│   │   ├── tests/                  # pytest test files
│   │   ├── docs/                   # Pipeline planning documents
│   │   │   ├── 00_ingestion_pipeline_plan.md
│   │   │   └── 01_implementation_roadmap.md  <-- CHECK THIS FIRST
│   │   ├── prompts/                # PCTF task prompts
│   │   ├── chroma_db/              # Vector database (auto-created)
│   │   ├── logs/                   # Log files (auto-created)
│   │   ├── .env                    # Environment config (gitignored)
│   │   ├── .env.example            # Environment template
│   │   ├── requirements.txt        # Python dependencies
│   │   └── README.md               # Detailed documentation
│   │
│   └── 03_rag_pipeline/            # RAG Pipeline component (Week 2)
│       ├── docs/                   # Pipeline planning documents
│       │   ├── 00_week2_rag_pipeline_plan.md
│       │   └── 01_implementation_roadmap.md  <-- CHECK THIS FIRST
│       ├── prompts/                # PCTF task prompts
│       ├── src/                    # Node.js backend (created during tasks)
│       │   ├── index.js            # Express app entry point
│       │   ├── config.js           # Environment config loader
│       │   ├── routes/             # API route handlers
│       │   ├── services/           # Business logic (pipeline, retrieval, llm)
│       │   ├── prompts/            # System prompt templates
│       │   └── utils/              # Utilities (logger, etc.)
│       ├── client/                 # React UI (created during tasks)
│       ├── scripts/                # Python evaluation scripts
│       ├── tests/                  # Jest unit tests
│       ├── logs/                   # Log files
│       ├── .env                    # Environment config (gitignored)
│       └── .env.example            # Environment template
│
├── .github/workflows/ingestion.yml # CI/CD pipeline
├── CLAUDE.md                       # Root project guide
└── AGENTS.md                       # This file
```

---

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Language | Python | 3.11+ | Document processing, ingestion (ChromaDB doesn't support 3.14) |
| Vector DB | ChromaDB | 0.5.23 | Vector storage and retrieval |
| Embeddings | all-MiniLM-L6-v2 | via ONNX | 384-dimensional embeddings (ChromaDB default) |
| Text Splitting | langchain-text-splitters | 0.0.1 | Semantic chunking |
| Frontmatter | python-frontmatter | 1.1.0 | YAML frontmatter parsing |
| Backend | Node.js + Express | 18+ | API server |
| Frontend | React + Tailwind | 18+ | Minimal UI |
| LLM | Groq API (Llama 3.1 8B) | - | Response generation |
| Testing (Python) | pytest | 8.0+ | Python unit tests |
| Testing (Node.js) | Jest | 29+ | Node.js unit tests |
| CI/CD | GitHub Actions | - | Automated testing and ingestion |

**Key Architecture Decisions:**
1. **Hybrid Python/Node**: Document processing uses Python (better libraries), API uses Node.js
2. **Local-first**: ChromaDB and embeddings run locally; LLM via Groq API
3. **Knowledge base only**: Phase 1 has no live system integration
4. **Singapore-centric**: Regulatory scope limited to Singapore with SEA secondary coverage
5. **Minimal dependencies**: ChromaDB default embeddings via ONNX (no PyTorch/CUDA required)

---

## Build and Test Commands

### Ingestion Pipeline (Primary Component)

All commands run from `pilot_phase1_poc/02_ingestion_pipeline/`:

```bash
cd pilot_phase1_poc/02_ingestion_pipeline

# Setup (one-time)
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run ingestion
python -m scripts.ingest                    # Full ingestion
python -m scripts.ingest --dry-run          # Test without storing
python -m scripts.ingest --verbose          # Show chunk details
python -m scripts.ingest --clear            # Clear and re-ingest
python -m scripts.ingest --category 01_regulatory  # Single category

# Run verification
python -m scripts.verify_ingestion          # Run all checks
python -m scripts.verify_ingestion --verbose
python -m scripts.verify_ingestion --tier 1
python -m scripts.verify_ingestion --check 3

# Run tests
python -m pytest tests/ -v                  # All tests
python -m pytest tests/test_process_docs.py -v
python -m pytest tests/test_chunker.py -v
```

### CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ingestion.yml`):
- Triggers on changes to KB or pipeline code
- Runs pytest unit tests
- Runs full ingestion with `--clear`
- Runs verification (must pass)
- Uploads ChromaDB artifact (7-day retention)

---

## Code Style Guidelines

### Python Code Style

- **Docstrings**: Google-style docstrings with Args/Returns sections
- **Type hints**: Use for function signatures where practical
- **Line length**: ~100 characters (not strictly enforced)
- **Imports**: Group by stdlib, third-party, local; alphabetize within groups
- **Naming**: snake_case for functions/variables, PascalCase for classes, UPPER_SNAKE for constants

Example:
```python
def parse_document(file_path: Path) -> dict:
    """
    Parse a markdown document and return a structured document object.

    Args:
        file_path: Path to the markdown document

    Returns:
        Dictionary with all document fields
    """
    # Implementation
```

### Document Metadata Format

All knowledge base documents use YAML frontmatter:

```yaml
---
title: [Document Title]
source_org: [Organization name, e.g., "Singapore Customs"]
source_urls:
  - [Primary URL]
source_type: [public_regulatory | public_carrier | synthetic_internal]
last_updated: [YYYY-MM-DD]
jurisdiction: [SG | MY | ID | TH | VN | PH | ASEAN | Global]
category: [customs | carrier | policy | procedure | reference]
use_cases: [UC-1.1, UC-2.3, etc.]
---
```

---

## Testing Instructions

### Test-Driven Development (TDD)

This project follows TDD methodology:

1. **Write Tests First**: Before implementing any function/module, write failing tests
2. **Red-Green-Refactor Cycle**:
   - **Red**: Write a failing test
   - **Green**: Write minimal code to make the test pass
   - **Refactor**: Clean up while keeping tests green
3. **Test File Convention**: Tests go in `tests/` directory, mirroring source structure
   - `scripts/chunker.py` → `tests/test_chunker.py`

### Running Tests

```bash
# All tests with coverage
python -m pytest tests/ -v --tb=short

# Specific test file
python -m pytest tests/test_process_docs.py -v

# Specific test class
python -m pytest tests/test_chunker.py::TestChunkDocument -v

# Specific test method
python -m pytest tests/test_chunker.py::TestChunkDocument::test_produces_multiple_chunks -v
```

### Verification Tests

The verification script runs 30 semantic queries across 3 tiers:

| Tier | Description | Pass Criteria |
|------|-------------|---------------|
| Tier 1 | Category retrieval (8 queries) | 8/8 pass |
| Tier 2 | Document retrieval (12 queries) | 10+/12 pass |
| Tier 3 | Keyword matching (10 queries) | 8+/10 pass |

**Overall target**: 28+/30 tests pass (93%+)

---

## Development Conventions

### Task Coordination (PCTF)

Before starting any task from the roadmap:

1. **Read the Roadmap**: Check `docs/01_implementation_roadmap.md` first
2. **Verify Status**: Check task status (⬜ Not Started | 🟡 In Progress | ✅ Complete | ❌ Blocked)
3. **Check Dependencies**: Confirm all dependencies are complete
4. **Create Task Folder**: `prompts/[GROUP]_[TASK]_[description]/`
5. **Use PCTF Format** for prompts:
   - **P**ersona: Role and expertise
   - **C**ontext: Background, current state, references, dependencies
   - **T**ask: Objective, requirements, specs, constraints, acceptance criteria
   - **F**ormat: Output structure, code style, docs, validation commands
6. **Update Roadmap**: Mark checkboxes `[x]` and update status after completion

### Configuration

Environment variables (loaded from `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `CHROMA_PERSIST_PATH` | `./chroma_db` | ChromaDB storage directory |
| `KNOWLEDGE_BASE_PATH` | `../01_knowledge_base/kb` | Knowledge base documents |
| `COLLECTION_NAME` | `waypoint_kb` | ChromaDB collection name |
| `EMBEDDING_MODEL` | `default` | ChromaDB built-in embeddings |
| `EMBEDDING_DIMENSIONS` | `384` | Embedding vector size |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

Chunking settings (in `scripts/config.py`):
- `CHUNK_SIZE`: 600 characters (~150 tokens)
- `CHUNK_OVERLAP`: 90 characters (15%)
- `SEPARATORS`: `["\n## ", "\n### ", "\n\n", "\n"]`

---

## Security Considerations

1. **API Keys**: No API keys required for ingestion pipeline (local embeddings)
2. **Environment Files**: `.env` is gitignored; use `.env.example` as template
3. **Vector DB**: ChromaDB stored locally in `chroma_db/`, not committed to git
4. **Knowledge Base**: Contains public regulatory info and synthetic internal policies - no sensitive customer data
5. **Dependencies**: Minimal external dependencies; all pinned in requirements.txt

---

## RAG Pipeline Flow

```
Knowledge Base (29 docs)
        |
        v
+-------------------+
| Document Processor|  scripts/process_docs.py
| - Discover docs   |  - Finds all .md files in kb/
| - Parse YAML      |  - Extracts frontmatter
| - Extract content |  - Separates metadata/content
+-------------------+
        |
        v
+-------------------+
| Chunking Engine   |  scripts/chunker.py
| - Split by headers|  - Respects ## and ### boundaries
| - 600 char chunks |  - 90 char overlap
| - Add metadata    |  - 12 fields per chunk
+-------------------+
        |
        v
+-------------------+
| ChromaDB Storage  |  scripts/ingest.py
| - Default embed   |  - all-MiniLM-L6-v2 (384-d)
| - Persist to disk |  - ./chroma_db/
| - Collection: kb  |  - waypoint_kb
+-------------------+
        |
        v
+-------------------+
| Verification      |  scripts/verify_ingestion.py
| - Count checks    |  - 450-520 chunks expected
| - Category checks |  - 4 categories
| - Retrieval tests |  - 30 semantic queries
+-------------------+
```

---

## Critical Constraints

- **Responses must cite sources** from knowledge base
- **Gracefully decline out-of-scope queries** (live rates, tracking, bookings)
- **Target 40% query deflection rate** for POC success
- **LLM API costs under $10 total** for POC
- **Singapore primary, SEA secondary** regulatory scope

---

## Success Criteria

- 29 documents parsed, ~350-400 chunks generated (actual: 483)
- Tier 1 tests (category retrieval): 8/8 pass
- Tier 2 tests (document retrieval): 10+/12 pass
- 80% citation accuracy

---

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

# E2E tests
python -m scripts.e2e_test
```

---

## Useful Resources

- Root `CLAUDE.md`: Project overview and high-level architecture
- `02_ingestion_pipeline/docs/01_implementation_roadmap.md`: Ingestion task checklist (Week 1)
- `03_rag_pipeline/docs/01_implementation_roadmap.md`: RAG pipeline task checklist (Week 2)
- `02_ingestion_pipeline/README.md`: Detailed pipeline documentation
- `00_docs/04_technical_architecture.md`: Stack and API specification
- `00_docs/02_use_cases.md`: 50 test queries and expected behaviors
