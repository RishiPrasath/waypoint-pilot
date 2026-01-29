# Week 2: RAG Pipeline Development Plan

**Project**: Waypoint Phase 1 POC  
**Component**: RAG Pipeline + Ingestion Quality Assessment  
**Duration**: Days 8-14 (7 days)  
**Created**: 2025-01-28

---

## Executive Summary

Week 2 focuses on two parallel tracks:
1. **Primary**: Build the end-to-end RAG pipeline (retrieval + generation + API + UI)
2. **Critical**: Validate ingestion quality using the 50-query test bank to ensure chunking effectiveness

The ingestion pipeline is complete (29 docs → 483 chunks in ChromaDB). Now we need to:
- Connect retrieval to generation (Groq/Llama 3.1 8B)
- Implement citation tracking
- Build API + minimal UI
- **Critically**: Run systematic retrieval tests against the 50 test queries to validate chunking strategy

---

## Current State Assessment

### ✅ What's Done (Week 1)
| Component | Status | Details |
|-----------|--------|---------|
| Knowledge Base | 29/29 docs | All categories complete |
| Ingestion Pipeline | 100% | 483 chunks indexed |
| ChromaDB | Operational | 384-dim embeddings (all-MiniLM-L6-v2) |
| Metadata | Complete | 12 fields per chunk including source URLs |
| Unit Tests | 87 passing | TDD approach validated |
| Verification | 33/33 pass | Tier 1-3 retrieval tests (30 queries) |

### 🎯 What's Needed (Week 2)
| Component | Priority | Estimated Hours |
|-----------|----------|-----------------|
| Retrieval Quality Testing | P0 | 4-6h |
| Retrieval Service | P0 | 3-4h |
| Generation Service | P0 | 4-5h |
| API Layer | P0 | 3-4h |
| Basic UI | P1 | 3-4h |
| Chunking Optimization | P1 | 2-4h (if needed) |

---

## Critical Decision: Ingestion Quality Validation

### Why This Matters First

Before building the full RAG pipeline, we must validate that:
1. **Retrieval works** for the 50 evaluation queries (not just the 30 verification queries)
2. **Chunking strategy** produces coherent, contextually useful chunks
3. **Metadata** enables accurate citation generation

The existing verify_ingestion.py tests 30 queries. The evaluation framework requires **50 queries** covering:
- Booking & Documentation (10)
- Customs & Regulatory (10)  
- Carrier Information (10)
- SLA & Service (10)
- Edge Cases & Out-of-Scope (10)

### Testing Gap Analysis

| Current Tests (30) | Needed Tests (50) | Gap |
|-------------------|-------------------|-----|
| Category retrieval (8) | Full P1/P2 use cases | +20 queries |
| Document retrieval (12) | Out-of-scope detection | Edge case handling |
| Keyword matching (10) | Multi-source synthesis | Complex reasoning |

---

## Week 2 Daily Breakdown

### Day 8: Setup & Retrieval Quality Deep-Dive

**Goal**: Consolidate project files, fix ingestion, validate retrieval quality

#### Morning: Project Setup & Ingestion Fix (2-3h)

**Task 1: Copy KB and Ingestion Pipeline to RAG Pipeline folder**

```
03_rag_pipeline/
├── kb/                    # Copy from 01_knowledge_base/kb/
│   ├── 01_regulatory/
│   ├── 02_carriers/
│   ├── 03_reference/
│   └── 04_internal_synthetic/
├── ingestion/             # Copy from 02_ingestion_pipeline/
│   ├── scripts/
│   ├── tests/
│   ├── requirements.txt
│   └── ...
└── ...
```

**Task 2: Fix `ingest.py` to include `source_urls` in ChromaDB metadata**

Current issue: `source_urls` exists in KB frontmatter and passes through chunker, but `ingest.py` does not store it in ChromaDB metadata.

Fix required in `ingestion/scripts/ingest.py`:
```python
metadatas = [
    {
        ...
        "file_path": chunk["file_path"],
        "source_urls": ",".join(chunk["source_urls"]),  # ADD THIS LINE
    }
    for chunk in chunks
]
```

**Task 3: Re-run ingestion with `--clear` flag**
```bash
cd 03_rag_pipeline/ingestion
python -m scripts.ingest --clear
```

**Task 4: Verify `source_urls` now in ChromaDB**
```bash
python -m scripts.view_chroma --limit 3
# Should show source_urls in metadata
```

**Acceptance Criteria**:
- [ ] KB copied to `03_rag_pipeline/kb/`
- [ ] Ingestion pipeline copied to `03_rag_pipeline/ingestion/`
- [ ] `ingest.py` updated to store `source_urls`
- [ ] Re-ingestion complete (483 chunks with URLs)
- [ ] `view_chroma` confirms `source_urls` in metadata

#### Afternoon: Retrieval Quality Testing (3-4h)

**Tasks**:
1. Create `scripts/retrieval_quality_test.py`
2. Implement all 50 test queries from 02_use_cases.md
3. For each query, capture:
   - Top-5 retrieved chunks
   - Similarity scores
   - Source documents
   - Category matches
4. Generate retrieval quality report

**Output Files**:
```
03_rag_pipeline/
├── scripts/
│   └── retrieval_quality_test.py
├── reports/
│   └── retrieval_quality_REPORT.md
└── data/
    └── retrieval_test_results.json
```

#### Afternoon: Analysis & Decision Point (2-3h)

**Analysis Dimensions**:
1. **Per-category hit rate**: % of queries where relevant category appears in top-3
2. **Document precision**: % of queries where correct document appears in top-3
3. **Chunk coherence**: Manual review of 10 worst-performing queries
4. **Edge case handling**: How does retrieval behave for out-of-scope queries?

**Decision Gate**:
| Retrieval Quality | Action |
|------------------|--------|
| ≥75% relevant top-3 | PROCEED - Build retrieval service |
| 60-74% | INVESTIGATE - Review specific failures, minor adjustments |
| <60% | REMEDIATE - Day 9 dedicated to chunking fixes |

**Acceptance Criteria**:
- [ ] All 50 queries tested against ChromaDB
- [ ] Retrieval quality report generated
- [ ] Top 10 failure cases documented with root cause
- [ ] GO/PIVOT decision documented

---

### Day 9: Retrieval Service Implementation

**Goal**: Production-ready retrieval service with configurable parameters

#### Tasks (6-8h)

**1. Retrieval Service Module** (`src/services/retrieval.py`)
```python
# Core functions needed:
- async def get_relevant_chunks(query: str, top_k: int = 5) -> List[Chunk]
- async def filter_by_relevance(chunks: List[Chunk], threshold: float = 0.7) -> List[Chunk]
- async def format_context(chunks: List[Chunk]) -> str
- async def get_metadata_for_citation(chunks: List[Chunk]) -> List[Citation]
```

**2. Configuration** — All parameters via environment variables (no hardcoding):

`.env`:
```bash
# Retrieval
RETRIEVAL_TOP_K=10
RELEVANCE_THRESHOLD=0.15
MAX_CONTEXT_TOKENS=2000

# LLM Provider (OpenAI-compatible endpoint)
LLM_PROVIDER=groq
LLM_API_KEY=your_groq_api_key_here
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=500
```

`src/config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Retrieval
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", 10))
RELEVANCE_THRESHOLD = float(os.getenv("RELEVANCE_THRESHOLD", 0.15))
MAX_CONTEXT_TOKENS = int(os.getenv("MAX_CONTEXT_TOKENS", 2000))

# LLM Provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.3))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 500))
```

**3. Retrieval Quality Logging**
```python
# For each retrieval:
- Log query text
- Log retrieved chunk IDs
- Log similarity scores
- Log latency (target: <200ms)
```

**Output Files**:
```
03_rag_pipeline/
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── services/
│       ├── __init__.py
│       └── retrieval.py
└── tests/
    └── test_retrieval.py
```

**Acceptance Criteria**:
- [ ] Retrieval service returns top-k chunks with metadata
- [ ] Similarity scores accessible
- [ ] Configurable threshold filtering
- [ ] Average latency <200ms for single query
- [ ] 10+ unit tests passing

---

### Day 10: Generation Service Implementation

**Goal**: LLM generation with grounding and citation extraction

#### Tasks (6-8h)

**1. Groq Integration** (`src/services/llm.py`)
```python
# Core functions:
- async def generate_response(query: str, context: str) -> Response
- async def extract_citations(response: str) -> List[Citation]
- def build_system_prompt() -> str
- def build_user_prompt(query: str, context: str) -> str
```

**2. System Prompt Design** (`src/prompts/system_prompt.txt`)

Key requirements for customer service co-pilot:
- **Professional & formal tone** (agents use responses directly with customers)
- MUST cite sources for every factual claim
- MUST acknowledge limitations when context insufficient
- MUST gracefully decline out-of-scope queries
- Format: Clear structure, bullet points for lists
- No casual language, filler words, or excessive hedging

**Out-of-Scope Response Style** (Explain why + redirect):
```
"This query requires access to our live pricing system, which 
is outside my current capabilities. For rate quotes, please 
contact the booking team at bookings@company.com."
```

**Response Length**: Comprehensive — detailed explanations with categorized sections

**Example Response Format**:
```
For FCL sea freight export from Singapore to Indonesia, 
you will need to prepare several categories of documentation:

**Core Documents:**
- Commercial Invoice (minimum 3 copies)
- Packing List
- Bill of Lading

**Origin Documentation:**
- Certificate of Origin (Form D) - Required for ATIGA 
  preferential tariff rates. Must show 40% regional value content.

**Special Requirements:**
- For LARTAS-restricted goods, additional import permits 
  from Indonesian authorities are mandatory.

Sources:
- [Singapore Export Procedures > Required Documents](https://...)
- [Indonesia Import Requirements > Documentation](https://...)

Confidence: High
(Based on 3 matching sources with consistent information)
```

**3. Response Schema**
```python
@dataclass
class Response:
    answer: str
    citations: List[Citation]
    confidence: float  # 0-1, based on context relevance
    is_complete: bool  # False if info might be incomplete
    out_of_scope: bool  # True if query is outside knowledge base
```

**4. Guardrails**
```python
# Critical guardrails:
- Max response length: 500 tokens
- Hallucination prevention: "Only use information from the provided context"
- Citation requirement: "Always cite the source document for factual claims"
- Uncertainty acknowledgment: "If unsure, say 'I'm not certain about this'"
```

**Output Files**:
```
03_rag_pipeline/
├── src/
│   ├── services/
│   │   └── llm.py
│   └── prompts/
│       ├── system_prompt.txt
│       └── user_prompt_template.txt
└── tests/
    └── test_llm.py
```

**Acceptance Criteria**:
- [ ] Groq API connection working
- [ ] Responses generated with citations
- [ ] Out-of-scope queries handled gracefully
- [ ] Temperature = 0.3 for consistency
- [ ] Max tokens = 500 enforced
- [ ] 5+ unit tests passing

---

### Day 11: Pipeline Integration & API

**Goal**: End-to-end query pipeline with REST API

#### Morning: Pipeline Orchestration (3-4h)

**1. Query Pipeline** (`src/pipeline.py`)
```python
async def process_query(query: str) -> QueryResult:
    """
    Full RAG pipeline:
    1. Retrieve relevant chunks
    2. Filter by relevance threshold
    3. Format context for LLM
    4. Generate response with citations
    5. Validate response quality
    6. Return structured result
    """
```

**2. Pipeline Metrics**
```python
@dataclass
class QueryMetrics:
    query_received: datetime
    retrieval_latency_ms: float
    chunks_retrieved: int
    chunks_after_filter: int
    generation_latency_ms: float
    total_latency_ms: float
    citations_count: int
```

#### Afternoon: API Layer (3-4h)

**1. FastAPI Application** (`src/api.py`)

```python
# Endpoints:
POST /api/query
  Request: { "query": str }
  Response: { 
    "answer": str, 
    "citations": List[Citation],
    "confidence": float,
    "latency_ms": float
  }

GET /api/health
  Response: { "status": "ok", "chunks_indexed": int }

GET /api/stats
  Response: { "queries_processed": int, "avg_latency_ms": float }
```

**Output Files**:
```
03_rag_pipeline/
├── src/
│   ├── pipeline.py
│   └── api.py
├── tests/
│   ├── test_pipeline.py
│   └── test_api.py
└── requirements.txt (updated)
```

**Acceptance Criteria**:
- [ ] POST /api/query returns complete responses
- [ ] GET /api/health returns collection stats
- [ ] Latency <5s for typical queries
- [ ] Error handling for invalid queries
- [ ] CORS enabled for browser access
- [ ] 8+ integration tests passing

---

### Day 12: Basic UI Implementation

**Goal**: Minimal React/Tailwind interface for testing and demos

#### Tasks (2-3h)

**1. UI Setup**
```
public/
├── src/
│   ├── App.jsx          # Main component
│   ├── components/
│   │   ├── QueryInput.jsx
│   │   ├── Response.jsx
│   │   └── Citations.jsx
│   └── index.css        # Tailwind imports
├── index.html
├── package.json
├── tailwind.config.js
└── vite.config.js
```

**2. UI Features — Minimal MVP**
- Query input box with Enter key support
- Response display with formatted citations
- Confidence indicator (High/Medium/Low + explanation)
- Loading state
- Clean Tailwind styling

**3. Deferred to Phase 2** (if needed):
- Collapsible source panel showing retrieved chunks
- Copy-to-clipboard for responses
- Query history dropdown

**4. Tech Stack**
- React (Vite)
- Tailwind CSS

**3. Response Rendering**
```html
<!-- Example response display -->
<div class="response">
  <p class="answer">For an FCL export from Singapore...</p>
  <div class="citations">
    <span class="citation" data-source="sg_export_procedures">
      [1] Singapore Customs Export Procedures Guide
    </span>
  </div>
  <div class="metadata">
    <span class="latency">Response time: 2.3s</span>
    <span class="confidence">Confidence: High</span>
  </div>
</div>
```

**Output Files**:
```
03_rag_pipeline/
├── public/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── src/
    └── api.py (static file serving added)
```

**Acceptance Criteria**:
- [ ] Can submit queries via UI
- [ ] Responses display with formatting
- [ ] Citations clickable/visible
- [ ] Loading states work
- [ ] Mobile-responsive (basic)
- [ ] Works in Chrome, Firefox

---

### Day 13: Integration Testing & Bug Fixes

**Goal**: System stability and edge case handling

#### Morning: End-to-End Testing (3-4h)

**Test Scenarios**:
1. Happy path: Simple factual queries (10 queries)
2. Multi-source: Queries requiring multiple docs (5 queries)
3. Out-of-scope: Queries that should be declined (5 queries)
4. Edge cases: Empty query, very long query, special chars (5 queries)
5. Concurrent: Multiple simultaneous queries (3 parallel)
6. Error recovery: ChromaDB unavailable, Groq API error

**Testing Script**: `scripts/e2e_test.py`

#### Afternoon: Bug Fixes & Hardening (3-4h)

Common issues to check:
- [ ] Unicode handling in queries/responses
- [ ] Citation extraction edge cases
- [ ] Timeout handling for slow LLM responses
- [ ] Memory usage under load
- [ ] Log rotation

**Output Files**:
```
03_rag_pipeline/
├── scripts/
│   └── e2e_test.py
├── docs/
│   └── known_issues.md
└── logs/
    └── (test run logs)
```

**Acceptance Criteria**:
- [ ] All 25 test scenarios documented
- [ ] ≥80% pass rate on happy path
- [ ] All critical bugs fixed
- [ ] Known issues documented

---

### Day 14: Documentation & Week 2 Checkpoint

**Goal**: Complete documentation, prepare for Week 3 evaluation

#### Morning: Documentation (3-4h)

**1. README.md for RAG Pipeline**
```markdown
# Waypoint RAG Pipeline

## Quick Start
## Architecture
## Configuration
## API Reference
## Development
## Testing
## Known Limitations
```

**2. Architecture Diagram**
```
                    ┌─────────────┐
     User Query ───►│  FastAPI    │
                    │   /query    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Pipeline   │
                    │ Orchestrator│
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
   ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
   │  Retrieval  │  │    LLM      │  │  Citation   │
   │   Service   │  │  Service    │  │  Extractor  │
   └──────┬──────┘  └──────┬──────┘  └─────────────┘
          │                │
   ┌──────▼──────┐  ┌──────▼──────┐
   │  ChromaDB   │  │   Groq API  │
   │  (483 chunks)│  │ (Llama 3.1)│
   └─────────────┘  └─────────────┘
```

**3. Implementation Roadmap Update**
- Update `docs/01_implementation_roadmap.md` with actual progress
- Document any deviations from original plan

#### Afternoon: Week 2 Checkpoint (2-3h)

**Checkpoint Report**: `docs/week2_checkpoint.md`

| Metric | Target | Actual |
|--------|--------|--------|
| Retrieval hit rate | ≥75% | TBD |
| API response latency | <5s | TBD |
| Test coverage | ≥60% | TBD |
| Documentation complete | Yes | TBD |

**Ready for Week 3?**
- [ ] All 50 test queries can be processed
- [ ] Citation accuracy measurable
- [ ] Latency within target
- [ ] UI functional for demos

---

## Technology Stack Summary

### Core Components
| Component | Technology | Version |
|-----------|------------|---------|
| Vector DB | ChromaDB | 0.5.23 |
| Embeddings | all-MiniLM-L6-v2 (default) | 384-dim |
| LLM | Llama 3.1 8B via Groq | OpenAI-compatible endpoint |
| Backend | Node.js + Express (Layered) | Retrieval + API |
| Ingestion | Python scripts | Document processing only |
| Frontend | React + Tailwind | Minimal UI |

### Backend Architecture: Express.js + Layered Architecture

**Selected Approach**: Layered architecture with clean separation of concerns (routes → services → data). This approach balances POC speed (~6h build) with maintainability for potential production evolution.

**Why This Approach**:
- Clear separation makes debugging easier
- Services can be tested independently
- Easy to extend or swap components later
- Minimal dependencies (no heavy frameworks)
- Good balance of structure vs. boilerplate

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT REQUEST                           │
│                    POST /api/query { query }                    │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ROUTES LAYER                               │
│                   routes/query.js                               │
│  • Validates request body                                       │
│  • Calls pipeline service                                       │
│  • Formats HTTP response                                        │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SERVICES LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│  pipeline.js                                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ async processQuery(query)                               │   │
│  │   1. retrieval.getRelevantChunks(query)                │   │
│  │   2. retrieval.filterByThreshold(chunks)               │   │
│  │   3. llm.generateResponse(query, context)              │   │
│  │   4. Return { answer, citations, confidence, metadata } │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  retrieval.js                    │  llm.js                      │
│  ┌────────────────────────────┐  │  ┌────────────────────────┐  │
│  │ getRelevantChunks(query)   │  │  │ generateResponse()     │  │
│  │ filterByThreshold(chunks)  │  │  │ buildPrompt()          │  │
│  │ formatContext(chunks)      │  │  │ extractCitations()     │  │
│  └────────────────────────────┘  │  └────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  embedding.js                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ embedQuery(text) → vector[384]                          │   │
│  │ Uses: sentence-transformers via Python subprocess       │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                  │
├────────────────────────────┬────────────────────────────────────┤
│  ChromaDB (Local)          │  Groq API (External)               │
│  • 483 indexed chunks      │  • Llama 3.1 8B                    │
│  • 384-dim embeddings      │  • OpenAI-compatible               │
│  • Metadata + source URLs  │  • temp=0.3, max_tokens=500        │
└────────────────────────────┴────────────────────────────────────┘
```

**Directory Structure**:
```
03_rag_pipeline/
├── src/
│   ├── index.js              # Express app entry point
│   ├── config.js             # Environment config loader
│   ├── routes/
│   │   └── query.js          # POST /api/query endpoint
│   ├── services/
│   │   ├── pipeline.js       # Orchestrates RAG flow
│   │   ├── retrieval.js      # ChromaDB queries
│   │   ├── llm.js            # Groq API calls
│   │   └── embedding.js      # Query embedding
│   ├── prompts/
│   │   └── system.txt        # System prompt template
│   └── utils/
│       └── logger.js         # Structured logging
├── client/                   # React UI (Vite + Tailwind)
├── tests/                    # Jest unit tests
├── .env                      # Configuration
└── package.json
```

**API Response Format**:
```json
{
  "answer": "For sea freight export from Singapore to Indonesia...",
  "citations": [
    {
      "title": "Singapore Export Procedures",
      "section": "Required Documents",
      "url": "https://www.customs.gov.sg/..."
    }
  ],
  "confidence": {
    "level": "High",
    "reason": "3 matching sources with consistent information"
  },
  "metadata": {
    "chunksRetrieved": 10,
    "chunksUsed": 4,
    "latencyMs": 2340
  }
}
```

### Configuration Defaults
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| top_k | 10 | Multi-document queries need broader retrieval; relevant docs often appear at rank 6-10 |
| relevance_threshold | 0.15 | Current similarity scores range 0.05-0.35; higher threshold filters everything |
| max_context_tokens | 2000 | Fit within LLM context |
| temperature | 0.3 | Consistent, factual responses |
| max_response_tokens | 500 | Concise answers |

### Citation Format

Responses must include source citations with URLs where available:

**Format**:
```
[Document Title > Section Name](URL)
```

**Example Response**:
```
For sea freight export from Singapore to Indonesia, you need:
1. Commercial Invoice (minimum 3 copies)
2. Packing List
3. Bill of Lading
4. Certificate of Origin (Form D for ATIGA preferential rates)

Sources:
- [Singapore Export Procedures > Required Documents](https://www.customs.gov.sg/businesses/exporting-goods/overview)
- [Indonesia Import Requirements > Documentation](https://www.trade.gov/country-commercial-guides/indonesia-import-requirements)
```

**For internal/synthetic documents** (no URL):
```
[Company SLA Policy > Response Times] (Internal Document)
```

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Poor retrieval quality | Medium | High | Day 8 dedicated to validation |
| Groq API rate limits | Low | Medium | Implement retry with backoff |
| LLM hallucinations | Medium | High | Strong system prompt, citation requirement |
| Latency >5s | Medium | Low | Optimize context size, parallel requests |
| UI complexity scope creep | Medium | Low | Stick to minimal viable UI |

---

## File Structure (End of Week 2)

```
03_rag_pipeline/
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
│
├── kb/                          # Knowledge base (copied from 01_knowledge_base)
│   ├── 01_regulatory/
│   ├── 02_carriers/
│   ├── 03_reference/
│   └── 04_internal_synthetic/
│
├── ingestion/                   # Ingestion pipeline (copied from 02_ingestion_pipeline)
│   ├── scripts/
│   │   ├── config.py
│   │   ├── process_docs.py
│   │   ├── chunker.py
│   │   ├── ingest.py           # Updated to include source_urls
│   │   ├── verify_ingestion.py
│   │   └── view_chroma.py
│   ├── tests/
│   ├── chroma_db/              # Vector database
│   └── requirements.txt
│
├── docs/
│   ├── 00_week2_rag_pipeline_plan.md
│   ├── 01_implementation_roadmap.md
│   ├── week2_checkpoint.md
│   └── known_issues.md
│
├── src/                         # RAG pipeline source
│   ├── __init__.py
│   ├── config.py
│   ├── pipeline.py
│   ├── api.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── retrieval.py
│   │   └── llm.py
│   └── prompts/
│       ├── system_prompt.txt
│       └── user_prompt_template.txt
│
├── public/                      # UI files
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── scripts/                     # Evaluation scripts
│   ├── retrieval_quality_test.py
│   └── e2e_test.py
│
├── tests/                       # RAG pipeline tests
│   ├── __init__.py
│   ├── test_retrieval.py
│   ├── test_llm.py
│   ├── test_pipeline.py
│   └── test_api.py
│
├── reports/
│   └── retrieval_quality_REPORT.md
│
├── data/
│   └── retrieval_test_results.json
│
└── logs/
    └── .gitkeep
```

---

## Quick Reference: Key Commands

```bash
# Setup (from 03_rag_pipeline/)
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run API server
python -m src.api

# Run tests
python -m pytest tests/ -v

# Run retrieval quality test
python -m scripts.retrieval_quality_test

# Run e2e tests
python -m scripts.e2e_test
```

---

## Success Criteria: Week 2 Complete

| Criteria | Required | Notes |
|----------|----------|-------|
| Retrieval service operational | ✓ | Returns chunks with metadata |
| Generation service operational | ✓ | Groq + citation extraction |
| API accepts queries | ✓ | POST /api/query works |
| UI displays responses | ✓ | Basic but functional |
| Retrieval quality ≥70% | ✓ | Measured against 50 queries |
| Latency <5s | ✓ | End-to-end |
| Documentation complete | ✓ | README, architecture |

---

*Next Steps*: After Week 2, proceed to Week 3: Integration & Testing with full 50-query evaluation against scoring rubric.


---

## Phase 2: RAG Evaluation & Chunking Optimization

**When**: After Week 2 pipeline is functional (Days 15-18)  
**Goal**: Validate RAG accuracy against source documents, optimize chunking if needed

---

### Evaluation Approach Sequence

Execute in this order—each phase informs the next:

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 2A: Retrieval-Only Isolation (Day 15)                │
│     ↓ Identifies: Is it a retrieval or generation problem?  │
├─────────────────────────────────────────────────────────────┤
│  Phase 2B: Chunk Quality Audit (Day 15-16)                  │
│     ↓ Identifies: Systematic chunking defects               │
├─────────────────────────────────────────────────────────────┤
│  Phase 2C: A/B Chunking Experiments (Day 16) — IF NEEDED    │
│     ↓ Identifies: Optimal chunking configuration            │
├─────────────────────────────────────────────────────────────┤
│  Phase 2D: Golden Test Set Creation (Day 17)                │
│     ↓ Creates: Ground truth for final scoring               │
├─────────────────────────────────────────────────────────────┤
│  Phase 2E: LLM-as-Judge Automation (Day 18) — OPTIONAL      │
│     ↓ Enables: Scalable ongoing evaluation                  │
└─────────────────────────────────────────────────────────────┘
```

---

### Phase 2A: Retrieval-Only Isolation Testing (Day 15 Morning)

**Purpose**: Determine if failures are retrieval vs generation problems

**Method**:
1. Select 20 queries from the 50 test bank (4 per category)
2. Run retrieval only—no LLM generation
3. For each query, capture top-5 chunks
4. Manually answer: "Could a human find the correct answer in these chunks?"

**Output**: `reports/retrieval_isolation_REPORT.md`

| Query | Top Chunk Doc | Answer in Chunks? | Notes |
|-------|---------------|-------------------|-------|
| Q1: Docs for Indonesia export | sg_export_procedures | ✓ Yes | Chunk 3 has full list |
| Q11: GST rate Singapore | sg_gst_guide | ✓ Yes | 9% clearly stated |
| Q21: Carriers to HCMC | pil_service_summary | ✗ Partial | Missing ONE/Evergreen |

**Decision Gate**:
| Result | Action |
|--------|--------|
| ≥80% "Yes" | Retrieval OK → Focus on generation/prompt tuning |
| 60-79% "Yes" | Retrieval issues → Proceed to Phase 2B |
| <60% "Yes" | Major retrieval failure → Phase 2B + 2C mandatory |

**Time**: 2-3 hours

---

### Phase 2B: Chunk Quality Audit (Day 15 Afternoon)

**Purpose**: Identify systematic chunking defects

**Method**:
1. Extract 40 random chunks from ChromaDB (10 per category)
2. Read each chunk in isolation
3. Score each chunk on 4 criteria

**Chunk Scoring Rubric**:
| Criteria | Score | Description |
|----------|-------|-------------|
| Coherent | 0/1 | Complete sentences, not cut mid-thought |
| Self-contained | 0/1 | Understandable without surrounding context |
| Has context | 0/1 | Section header or topic indicator present |
| Useful | 0/1 | Would help answer a likely query |

**Output**: `reports/chunk_audit_REPORT.md`

**Common Defects to Flag**:
- [ ] Tables split across chunks
- [ ] Numbered procedures broken mid-step
- [ ] Headers orphaned from their content
- [ ] Lists with items split across chunks
- [ ] Regulatory citations cut off

**Decision Gate**:
| Avg Chunk Score | Action |
|-----------------|--------|
| ≥3.0/4.0 | Chunking acceptable |
| 2.0-2.9 | Minor adjustments needed (separators, overlap) |
| <2.0 | Major re-chunking required → Phase 2C |

**Time**: 2-3 hours

---

### Phase 2C: A/B Chunking Experiments (Day 16) — IF NEEDED

**Purpose**: Data-driven chunking configuration selection

**Trigger**: Run only if Phase 2A <80% OR Phase 2B <3.0 score

**Method**:
1. Define 3 chunking variants:

| Variant | Chunk Size | Overlap | Separators |
|---------|------------|---------|------------|
| A (current) | 600 chars | 90 (15%) | `\n## `, `\n### `, `\n\n`, `\n` |
| B (larger) | 800 chars | 120 (15%) | Same |
| C (semantic) | 512 chars | 100 (20%) | `\n## `, `\n### `, `\n- `, `\n\n` |

2. Create separate ChromaDB collections for each variant
3. Run same 20 queries against all 3
4. Compare retrieval hit rates

**Output**: `reports/chunking_ab_test_REPORT.md`

| Query | Variant A | Variant B | Variant C |
|-------|-----------|-----------|-----------|
| Q1 | ✓ | ✓ | ✓ |
| Q11 | ✓ | ✓ | ✗ |
| Q21 | ✗ | ✓ | ✓ |
| **Hit Rate** | 75% | 85% | 70% |

**Decision**: Select variant with highest hit rate, re-ingest full KB

**Time**: 4-5 hours (including re-ingestion)

---

### Phase 2D: Golden Test Set Creation (Day 17)

**Purpose**: Create ground truth for definitive accuracy scoring

**Method**:
1. Select 25 queries (5 per category, prioritize P1 use cases)
2. For each query, manually create:
   - **Ideal answer**: What a perfect response looks like
   - **Source reference**: Exact doc, section, page
   - **Key facts**: Must-have information points
   - **Disallowed content**: Things that would be hallucination

**Golden Test Entry Template**:
```yaml
query_id: Q01
query: "What documents are needed for sea freight Singapore to Indonesia?"
category: booking_documentation
priority: P1

ideal_answer: |
  For sea freight export from Singapore to Indonesia, you need:
  1. Commercial Invoice (minimum 3 copies)
  2. Packing List
  3. Bill of Lading
  4. Certificate of Origin (Form D for ATIGA preferential rates)
  5. Import permit if goods are LARTAS restricted

source_references:
  - doc: sg_export_procedures.md
    section: "Required Export Documents"
  - doc: indonesia_import_requirements.md
    section: "Documentation Requirements"

key_facts:
  - Commercial Invoice required
  - Packing List required
  - Bill of Lading required
  - Form D for ATIGA
  - LARTAS goods need permit

disallowed:
  - Made-up document names
  - Incorrect form numbers
  - Fabricated regulations
```

**Output**: `data/golden_test_set.yaml` (25 entries)

**Time**: 4-5 hours (most labor-intensive but most valuable)

---

### Phase 2E: LLM-as-Judge Automation (Day 18) — OPTIONAL

**Purpose**: Enable scalable, repeatable evaluation

**Trigger**: Only if manual evaluation is bottleneck

**Method**:
1. Create evaluation prompt for judge LLM
2. Feed: Source chunks + RAG answer + Golden answer + Rubric
3. Have judge LLM score on 4 dimensions

**Judge Prompt Structure**:
```
You are evaluating a RAG system response for accuracy.

SOURCE CONTEXT:
{retrieved_chunks}

RAG SYSTEM ANSWER:
{rag_response}

GOLDEN REFERENCE ANSWER:
{golden_answer}

Score the RAG answer on these criteria (1-5 each):
1. ACCURACY: Does it match the source documents?
2. COMPLETENESS: Does it cover all key facts?
3. HALLUCINATION: Does it contain invented information?
4. CITATION: Are sources correctly attributed?

Provide scores and brief justification for each.
```

**Output**: `scripts/llm_judge_eval.py` + `reports/llm_judge_REPORT.md`

**Validation**: Spot-check 10 judge scores manually to ensure alignment

**Time**: 3-4 hours (script development + validation)

---

### Evaluation Outputs Summary

| Phase | Output File | Purpose |
|-------|-------------|---------|
| 2A | `reports/retrieval_isolation_REPORT.md` | Diagnose retrieval vs generation |
| 2B | `reports/chunk_audit_REPORT.md` | Identify chunking defects |
| 2C | `reports/chunking_ab_test_REPORT.md` | Select optimal config |
| 2D | `data/golden_test_set.yaml` | Ground truth for scoring |
| 2E | `reports/llm_judge_REPORT.md` | Automated evaluation results |

---

### Phase 2 Success Criteria

| Metric | Target | Measured In |
|--------|--------|-------------|
| Retrieval hit rate | ≥80% | Phase 2A |
| Chunk quality score | ≥3.0/4.0 | Phase 2B |
| Golden test accuracy | ≥70% | Phase 2D |
| Hallucination rate | ≤15% | Phase 2D |

**Go/No-Go for Week 3 Full Evaluation**:
- Must achieve retrieval hit rate ≥75%
- Must have golden test set complete
- Chunking issues resolved or documented as known limitations

---

### Quick Reference: Phase 2 Commands

```bash
# Run retrieval isolation test
python -m scripts.retrieval_isolation_test

# Run chunk quality audit
python -m scripts.chunk_audit --sample 40

# Run A/B chunking experiment
python -m scripts.chunking_ab_test --variants A,B,C

# Validate against golden test set
python -m scripts.golden_test_eval

# Run LLM judge evaluation (optional)
python -m scripts.llm_judge_eval --model gpt-4o-mini
```

---

*This Phase 2 evaluation feeds directly into Week 3's systematic 50-query evaluation with the scoring rubric from 06_evaluation_framework.md*
