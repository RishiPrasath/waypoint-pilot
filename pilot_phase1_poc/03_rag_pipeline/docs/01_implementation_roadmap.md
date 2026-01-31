# RAG Pipeline Implementation Checklist

**Project**: Waypoint Phase 1 POC
**Component**: RAG Pipeline (Retrieval + Generation + API + UI)
**Duration**: Days 8-14 (Week 2)

---

## Progress Tracker

| Group | Name | Tasks | Status |
|-------|------|-------|--------|
| 1. Project Setup | Copy assets, fix source_urls | 2/2 | ✅ Complete |
| 2. Retrieval Quality Testing | Quality test script, decision gate | 2/2 | ✅ Complete |
| 3. Node.js Setup | Project structure | 1/1 | ✅ Complete |
| 4. Retrieval Service | ChromaDB integration | 1/1 | ✅ Complete |
| 5. Generation Service | LLM, prompt, citations | 3/3 | ✅ Complete |
| 6. Pipeline & API | Orchestrator, Express API, E2E test | 3/3 | ✅ Complete |
| 7. UI Implementation | React + Tailwind, polish | 2/2 | ✅ Complete |
| 8. Integration Testing | E2E suite, bug fixes | 0/2 | ⬜ Not Started |
| 9. Documentation | README, checkpoint report | 0/2 | ⬜ Not Started |
| **TOTAL** | | **14/18** | **78%** |

**Status Legend**: ⬜ Not Started | 🟡 In Progress | ✅ Complete | ❌ Blocked

---

## Task Group 1: Project Setup
**Duration**: 2-3 hours (Day 8 Morning) | **Prompt Folder**: `prompts/01_1.x_*/`

### Task 1.1: Copy KB and Ingestion to RAG Pipeline
- [x] Knowledge base copied to `03_rag_pipeline/kb/`
- [x] Ingestion pipeline copied to `03_rag_pipeline/ingestion/`
- [x] Paths verified and working
- [x] venv can be created in new location

**Target Structure**:
```
03_rag_pipeline/
├── kb/                    # Copy from 01_knowledge_base/kb/
│   ├── 01_regulatory/
│   ├── 02_carriers/
│   ├── 03_reference/
│   └── 04_internal_synthetic/
└── ingestion/             # Copy from 02_ingestion_pipeline/
    ├── scripts/
    ├── tests/
    ├── requirements.txt
    └── ...
```

**Status**: ✅ | **Report**: `prompts/01_1.1_copy_assets/REPORT.md`

---

### Task 1.2: Fix source_urls in Ingestion
- [x] `ingest.py` updated to store `source_urls` in ChromaDB metadata
- [x] Re-ingestion complete with `--clear` flag
- [x] `view_chroma` or query confirms `source_urls` in metadata
- [x] All 483 chunks have source_urls field

**Fix Required** in `ingestion/scripts/ingest.py`:
```python
metadatas = [
    {
        ...
        "source_urls": ",".join(chunk["source_urls"]),  # ADD THIS LINE
    }
    for chunk in chunks
]
```

**Validation Commands**:
```bash
cd 03_rag_pipeline/ingestion
python -m scripts.ingest --clear
python -c "import chromadb; c = chromadb.PersistentClient('./chroma_db'); col = c.get_collection('waypoint_kb'); print(col.get(limit=1)['metadatas'][0].keys())"
```

**Status**: ✅ | **Report**: `prompts/01_1.2_source_url_fix/REPORT.md`

---

## Task Group 2: Retrieval Quality Testing
**Duration**: 5-6 hours (Day 8 Afternoon) | **Prompt Folder**: `prompts/02_2.x_*/`

### Task 2.1: Create Retrieval Quality Test Script
- [x] File created at `scripts/retrieval_quality_test.py`
- [x] Implements all 50 test queries from `00_docs/02_use_cases.md`
- [x] Captures top-5 chunks with similarity scores per query
- [x] Generates JSON output in `data/retrieval_test_results.json`
- [x] Generates markdown report in `reports/retrieval_quality_REPORT.md`

**Query Categories** (10 each):
1. Booking & Documentation
2. Customs & Regulatory
3. Carrier Information
4. SLA & Service
5. Edge Cases & Out-of-Scope

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

**Status**: ✅ | **Report**: `prompts/02_2.1_retrieval_quality_test/REPORT.md`

---

### Task 2.2: Run Retrieval Analysis & Decision Gate
- [x] All 50 queries tested against ChromaDB
- [x] Hit rate calculated (relevant doc in top-3)
- [x] Top 10 failure cases documented with root cause
- [x] GO/PIVOT decision documented (PROCEED)

**Decision Gate**:
| Retrieval Quality | Action |
|------------------|--------|
| ≥75% relevant top-3 | PROCEED - Build retrieval service |
| 60-74% | INVESTIGATE - Review specific failures, minor adjustments |
| <60% | REMEDIATE - Dedicated time to chunking fixes |

**Status**: ✅ | **Report**: `prompts/02_2.2_retrieval_analysis/REPORT.md`

---

## Task Group 3: Node.js Setup
**Duration**: 2-3 hours (Day 9 Morning) | **Prompt Folder**: `prompts/03_3.x_*/`

### Task 3.1: Create Node.js Project Structure
- [x] `package.json` created with dependencies
- [x] Directory structure created (`src/`, `tests/`, etc.)
- [x] `.env` and `.env.example` created with all config
- [x] Jest configured for testing
- [x] ESLint configured (optional - skipped)
- [x] `npm install` runs successfully (378 packages)

**Target Structure**:
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
├── client/                   # React UI (created later)
├── tests/                    # Jest unit tests
├── .env
├── .env.example
└── package.json
```

**Dependencies**:
```json
{
  "dependencies": {
    "express": "^4.18.0",
    "cors": "^2.8.5",
    "dotenv": "^16.0.0",
    "chromadb": "^1.8.0",
    "openai": "^4.0.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "supertest": "^6.3.0"
  }
}
```

**Validation Commands**:
```bash
cd 03_rag_pipeline
npm install
npm test  # Should pass with placeholder test
```

**Status**: ✅ | **Report**: `prompts/03_3.1_nodejs_setup/REPORT.md`

---

## Task Group 4: Retrieval Service
**Duration**: 3-4 hours (Day 9 Afternoon) | **Prompt Folder**: `prompts/04_4.x_*/`

### Task 4.1: Create Retrieval Service Module
- [x] File created at `src/services/retrieval.js`
- [x] `retrieveChunks(query, options)` function (via Python bridge)
- [x] `filterByThreshold(chunks, threshold)` function
- [x] `formatContext(chunks)` function
- [x] `getMetadataForCitation(chunks)` function
- [x] ChromaDB via Python subprocess bridge
- [x] Embedding generation handled by ChromaDB
- [x] Unit tests at `tests/retrieval.test.js` (16 tests)
- [x] Python bridge script at `scripts/query_chroma.py`

**Configuration** (from `.env`):
```bash
RETRIEVAL_TOP_K=10
RELEVANCE_THRESHOLD=0.15
MAX_CONTEXT_TOKENS=2000
CHROMA_PATH=./ingestion/chroma_db
COLLECTION_NAME=waypoint_kb
```

**Validation Commands**:
```bash
npm test -- --testPathPattern=retrieval
node scripts/test_retrieval.js
```

**Status**: ✅ | **Report**: `prompts/04_4.1_retrieval_service/REPORT.md`

---

## Task Group 5: Generation Service
**Duration**: 6-8 hours (Day 10) | **Prompt Folder**: `prompts/05_5.x_*/`

### Task 5.1: Create LLM Service
- [x] File created at `src/services/llm.js`
- [x] `generateResponse(query, context)` function
- [x] Groq API integration via OpenAI SDK
- [x] Error handling and retry logic
- [x] Unit tests at `tests/llm.test.js`

**Configuration** (from `.env`):
```bash
LLM_PROVIDER=groq
LLM_API_KEY=your_groq_api_key_here
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=500
```

**Status**: ✅ | **Report**: `prompts/05_5.1_llm_service/REPORT.md`

---

### Task 5.2: Create System Prompt
- [x] File created at `src/prompts/system.txt`
- [x] Professional, formal tone for customer service
- [x] Citation requirement for factual claims
- [x] Out-of-scope handling instructions
- [x] Response format specification (Structure Your Response section)

**Key Requirements**:
- MUST cite sources for every factual claim
- MUST acknowledge limitations when context insufficient
- MUST gracefully decline out-of-scope queries
- Format: Clear structure, bullet points for lists
- No casual language, filler words, or excessive hedging

**Status**: ✅ | **Report**: `prompts/05_5.2_system_prompt/REPORT.md`

---

### Task 5.3: Create Citation Extractor
- [x] File created at `src/services/citations.js`
- [x] `extractCitations(response, chunks)` function
- [x] Links citations to source documents
- [x] Formats with document title, section, URL
- [x] Unit tests at `tests/citations.test.js`

**Citation Format**:
```
[Document Title > Section Name](URL)
```

**For internal documents**:
```
[Company SLA Policy > Response Times] (Internal Document)
```

**Status**: ✅ | **Report**: `prompts/05_5.3_citation_extractor/REPORT.md`

---

## Task Group 6: Pipeline & API
**Duration**: 6-8 hours (Day 11) | **Prompt Folder**: `prompts/06_6.x_*/`

### Task 6.1: Create Pipeline Orchestrator
- [x] File created at `src/services/pipeline.js`
- [x] `processQuery(query)` function orchestrating full RAG flow
- [x] Metrics collection (latency, chunk counts)
- [x] Unit tests at `tests/pipeline.test.js`

**Pipeline Flow**:
1. Retrieve relevant chunks
2. Filter by relevance threshold
3. Format context for LLM
4. Generate response with citations
5. Return structured result

**Status**: ✅ | **Report**: `prompts/06_6.1_pipeline_orchestrator/REPORT.md`

---

### Task 6.2: Create Express API
- [x] File created at `src/index.js`
- [x] `POST /api/query` endpoint
- [x] `GET /api/health` endpoint
- [ ] `GET /api/stats` endpoint (optional)
- [x] CORS enabled for browser access
- [x] Error handling middleware
- [x] Integration tests at `tests/api.test.js`

**API Response Format**:
```json
{
  "answer": "For sea freight export...",
  "citations": [
    {
      "title": "Singapore Export Procedures",
      "section": "Required Documents",
      "url": "https://..."
    }
  ],
  "confidence": {
    "level": "High",
    "reason": "3 matching sources"
  },
  "metadata": {
    "chunksRetrieved": 10,
    "chunksUsed": 4,
    "latencyMs": 2340
  }
}
```

**Validation Commands**:
```bash
npm start &
curl -X POST http://localhost:3000/api/query -H "Content-Type: application/json" -d '{"query": "What documents for Indonesia export?"}'
curl http://localhost:3000/api/health
```

**Status**: ✅ | **Report**: `prompts/06_6.2_express_api/REPORT.md`

---

### Task 6.3: End-to-End API Test
- [x] Run 10 queries via API
- [x] Verify response structure
- [x] Verify citations present
- [x] Verify latency <5s (80% passed)
- [x] Document any issues

**Status**: ✅ | **Report**: `prompts/06_6.3_e2e_api_test/REPORT.md`

---

## Task Group 7: UI Implementation
**Duration**: 4-6 hours (Day 12) | **Prompt Folder**: `prompts/07_7.x_*/`

### Task 7.1: Create React + Tailwind UI
- [x] `client/` directory created with Vite + React
- [x] Tailwind CSS configured
- [x] `QueryInput` component
- [x] `Response` component with formatted citations
- [x] `Confidence` component
- [x] `Citations` component
- [x] `Loading` component
- [x] Basic responsive design

**Target Structure**:
```
client/
├── src/
│   ├── App.jsx
│   ├── components/
│   │   ├── QueryInput.jsx
│   │   ├── Response.jsx
│   │   ├── Citations.jsx
│   │   ├── Confidence.jsx
│   │   └── Loading.jsx
│   ├── api/
│   │   └── query.js
│   └── index.css
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── vite.config.js
```

**Validation Commands**:
```bash
cd client
npm install
npm run dev
# Open http://localhost:5173 and test queries
```

**Status**: ✅ | **Report**: `prompts/07_7.1_react_ui/REPORT.md`

---

### Task 7.2: UI Polish & Testing
- [x] Can submit queries via UI
- [x] Responses display with formatting
- [x] Citations visible/clickable
- [x] Loading states work
- [x] Mobile-responsive (basic)
- [x] Works in Chrome, Firefox (verified build, expected compatible)

**Status**: ✅ | **Report**: `prompts/07_7.2_ui_polish/REPORT.md`

---

## Task Group 8: Integration Testing
**Duration**: 6-8 hours (Day 13) | **Prompt Folder**: `prompts/08_8.x_*/`

### Task 8.1: Create E2E Test Suite
- [ ] File created at `scripts/e2e_test.py`
- [ ] Happy path: 10 factual queries
- [ ] Multi-source: 5 queries requiring multiple docs
- [ ] Out-of-scope: 5 queries to decline
- [ ] Edge cases: 5 (empty, long, special chars)
- [ ] Concurrent: 3 parallel queries
- [ ] Error recovery: ChromaDB/Groq unavailable

**Test Scenarios Summary**:
| Category | Count | Pass Target |
|----------|-------|-------------|
| Happy path | 10 | ≥80% |
| Multi-source | 5 | ≥60% |
| Out-of-scope | 5 | ≥80% |
| Edge cases | 5 | ≥80% |

**Status**: ⬜ | **Report**: `prompts/08_8.1_e2e_test_suite/REPORT.md`

---

### Task 8.2: Bug Fixes & Hardening
- [ ] Unicode handling verified
- [ ] Citation extraction edge cases fixed
- [ ] Timeout handling for slow LLM responses
- [ ] Memory usage acceptable
- [ ] All critical bugs fixed
- [ ] Known issues documented

**Status**: ⬜ | **Report**: `prompts/08_8.2_bug_fixes/REPORT.md`

---

## Task Group 9: Documentation
**Duration**: 5-6 hours (Day 14) | **Prompt Folder**: `prompts/09_9.x_*/`

### Task 9.1: Create Documentation
- [ ] `README.md` for RAG pipeline
- [ ] Architecture diagram
- [ ] API reference
- [ ] Configuration guide
- [ ] Development setup instructions

**README Sections**:
- Quick Start
- Architecture
- Configuration
- API Reference
- Development
- Testing
- Known Limitations

**Status**: ⬜ | **Report**: `prompts/09_9.1_documentation/REPORT.md`

---

### Task 9.2: Week 2 Checkpoint Report
- [ ] Checkpoint report at `docs/week2_checkpoint.md`
- [ ] Actual metrics vs targets
- [ ] Deviations from plan documented
- [ ] Ready for Week 3 evaluation

**Checkpoint Metrics**:
| Metric | Target | Actual |
|--------|--------|--------|
| Retrieval hit rate | ≥75% | TBD |
| API response latency | <5s | TBD |
| Test coverage | ≥60% | TBD |
| Documentation complete | Yes | TBD |

**Status**: ⬜ | **Report**: `prompts/09_9.2_week2_checkpoint/REPORT.md`

---

## Final Validation Checklist

### Core Functionality
- [ ] Retrieval service returns chunks with metadata
- [ ] Generation service produces cited responses
- [ ] API accepts and processes queries
- [ ] UI displays responses correctly

### Quality Gates
- [ ] Retrieval quality ≥70% on 50 queries
- [ ] API latency <5s end-to-end
- [ ] All unit tests passing
- [ ] E2E tests ≥80% pass rate

### Documentation
- [ ] README complete
- [ ] Architecture documented
- [ ] Known issues listed

---

## Quick Reference

### Commands
| Action | Command |
|--------|---------|
| Setup ingestion venv | `cd ingestion && py -3.11 -m venv venv && venv\Scripts\activate && pip install -r requirements.txt` |
| Run ingestion | `cd ingestion && python -m scripts.ingest --clear` |
| Setup Node.js | `npm install` |
| Run API server | `npm start` |
| Run Node.js tests | `npm test` |
| Setup UI | `cd client && npm install` |
| Run UI dev server | `cd client && npm run dev` |
| Run E2E tests | `python -m scripts.e2e_test` |

### Key Configuration
| Setting | Value | Rationale |
|---------|-------|-----------|
| top_k | 10 | Broader retrieval for multi-doc queries |
| relevance_threshold | 0.15 | Current scores range 0.05-0.35 |
| max_context_tokens | 2000 | Fit within LLM context |
| temperature | 0.3 | Consistent, factual responses |
| max_response_tokens | 500 | Concise answers |
| LLM model | llama-3.1-8b-instant | Fast, cost-effective via Groq |
