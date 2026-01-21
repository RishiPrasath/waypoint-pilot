# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Waypoint is a RAG-based customer service co-pilot for freight forwarding companies, specifically targeting 3PL companies in Singapore and Southeast Asia. The project is in Phase 1 POC stage with detailed planning documents but no implemented code yet.

**Target**: Customer service agents who need quick, accurate answers about shipment booking, customs regulations, and carrier information.

## Tech Stack (Planned)

- **Backend**: Node.js with Express.js
- **Vector Database**: ChromaDB (local development)
- **LLM**: Groq API with Llama 3.1 8B (or Ollama for local development)
- **Embeddings**: sentence-transformers (`all-MiniLM-L6-v2`) via Python
- **Document Processing**: Python scripts using LangChain

## Project Structure (When Implemented)

```
waypoint-poc/
├── src/
│   ├── index.js           # Express server
│   ├── routes/query.js    # Query endpoint
│   ├── services/
│   │   ├── embedding.js   # Embedding service
│   │   ├── retrieval.js   # ChromaDB retrieval
│   │   └── llm.js         # LLM generation
│   └── utils/prompts.js   # System prompts
├── scripts/
│   ├── ingest.py          # Document ingestion
│   └── process_docs.py    # Document processing
├── knowledge_base/        # 25-30 curated documents
│   ├── 01_regulatory/     # Singapore Customs, ASEAN trade
│   ├── 02_carriers/       # PIL, Maersk, ONE, Evergreen
│   ├── 03_reference/      # Incoterms, HS codes
│   └── 04_internal_synthetic/  # Simulated company policies
├── tests/
└── public/                # Simple web UI
```

## Commands (When Implemented)

```bash
# Start development server
npm run dev

# Ingest documents into ChromaDB
python scripts/ingest.py

# Run tests
npm test

# Check ChromaDB status
python -c "import chromadb; c=chromadb.PersistentClient('./chroma_db'); print(c.list_collections())"
```

## Key Architecture Decisions

1. **Hybrid Python/Node**: Document processing uses Python (better libraries), API uses Node.js
2. **Local-first**: ChromaDB and sentence-transformers run locally; LLM via Groq API
3. **Knowledge base only**: Phase 1 has no live system integration (TMS/WMS, tracking, rates)
4. **Singapore-centric**: Regulatory scope limited to Singapore with SEA secondary coverage

## RAG Pipeline Flow

1. Query Processing: Clean/normalize, generate embedding
2. Retrieval: Search ChromaDB (top-k=5), filter by relevance threshold (0.7)
3. Context Assembly: Format chunks with source attribution
4. Generation: LLM with constrained system prompt
5. Response: Include answer, sources, and confidence indicator

## Critical Constraints

- Responses must cite sources from knowledge base
- Must gracefully decline out-of-scope queries (live rates, tracking, bookings)
- Target 40% query deflection rate for POC success
- LLM API costs must stay under $10 total for POC

## Document Metadata Format

All knowledge base documents use this frontmatter:
```yaml
---
title: [Document Title]
source: [URL or "Internal"]
source_type: [public_regulatory | public_carrier | synthetic_internal]
last_updated: [YYYY-MM-DD]
jurisdiction: [SG | MY | ID | TH | VN | PH | ASEAN | Global]
category: [customs | carrier | policy | procedure | reference]
use_cases: [UC-1.1, UC-2.3, etc.]
---
```

## Planning Documents

The `pilot_phase1_poc/` directory contains the complete POC specification:
- `00_pilot_overview.md` - Executive summary and document index
- `01_scope_definition.md` - What's in/out of scope
- `02_use_cases.md` - 50 test queries and expected behaviors
- `03_knowledge_base_blueprint.md` - Document collection plan
- `04_technical_architecture.md` - Stack and API specification
- `05_execution_roadmap.md` - 30-day implementation plan
- `06_evaluation_framework.md` - Metrics and go/no-go criteria
