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
│   ├── 01_knowledge_base/          # 29 curated markdown documents
│   │   ├── 01_regulatory/          # Singapore Customs, ASEAN trade (14 docs)
│   │   ├── 02_carriers/            # Ocean & Air carriers (6 docs)
│   │   ├── 03_reference/           # Incoterms, HS codes (3 docs)
│   │   └── 04_internal_synthetic/  # Policies, procedures (6 docs)
│   └── 02_ingestion_pipeline/      # Document ingestion component
│       ├── docs/                   # Pipeline plan and roadmap
│       ├── prompts/                # PCTF task prompts
│       └── CLAUDE.md               # Component-specific instructions
└── CLAUDE.md                       # This file
```

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Vector DB | ChromaDB | Vector storage and retrieval |
| Embeddings | ChromaDB default (all-MiniLM-L6-v2 via ONNX, 384-d) | Embedding generation |
| Document Processing | Python 3.11+ | Ingestion pipeline |
| Backend | Node.js + Express (planned) | API server |
| LLM | Groq API (Llama 3.1 8B) | Response generation |

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

## Ingestion Pipeline Coordination Rules

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
