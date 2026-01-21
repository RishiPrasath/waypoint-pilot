# 05 - Execution Roadmap

**Document Type**: Project Plan  
**Pilot**: Waypoint Phase 1 POC  
**Duration**: 30 Days  
**Version**: 1.0

---

## Timeline Overview

```
Week 1 (Days 1-7)     │ Foundation & Core Knowledge Base
Week 2 (Days 8-14)    │ RAG Pipeline Development  
Week 3 (Days 15-21)   │ Integration & Testing
Week 4 (Days 22-30)   │ Evaluation & Documentation
```

---

## Week 1: Foundation & Core Knowledge Base

**Goal**: Dev environment ready + 15 core documents collected/created

### Day 1-2: Environment Setup

| Task | Deliverable | Time |
|------|-------------|------|
| Set up project structure | `waypoint-poc/` directory created | 2h |
| Install Node.js dependencies | `package.json` with all deps | 1h |
| Set up Python environment | `venv` with requirements installed | 1h |
| Initialize ChromaDB | Local database running | 1h |
| Get Groq API key | `.env` configured | 30m |
| Test basic connectivity | "Hello world" LLM response | 1h |

**Day 2 Checkpoint**: ✓ Can send a query to Groq and get response

### Day 3-4: Core Document Collection

| Task | Documents | Source |
|------|-----------|--------|
| Singapore Customs docs (6) | Export, Import, GST, CO, HS, FTZ guides | customs.gov.sg |
| Create Incoterms reference | Comprehensive Incoterms 2020 guide | Synthetic |
| ASEAN Tariff Finder guide | How to use the tool | tariff-finder.asean.org |

**Process per document**:
1. Visit source URL
2. Copy relevant content
3. Format as markdown with metadata header
4. Save to `knowledge_base/01_regulatory/`

**Day 4 Checkpoint**: ✓ 8 regulatory documents collected and formatted

### Day 5-6: Carrier Documents + Synthetic Policies

| Task | Documents | Source |
|------|-----------|--------|
| PIL service summary | Coverage, services | pilship.com |
| Maersk service summary | Coverage, services | maersk.com |
| ONE service summary | Coverage, services | one-line.com |
| Evergreen service summary | Coverage, services | evergreen-line.com |
| Service Terms (synthetic) | Company T&Cs | Create from template |
| Booking Procedure (synthetic) | Step-by-step process | Create from template |
| SLA Policy (synthetic) | Service commitments | Create from template |

**Day 6 Checkpoint**: ✓ 15 total documents ready for ingestion

### Day 7: Document Ingestion Pipeline

| Task | Deliverable | Time |
|------|-------------|------|
| Create chunking script | `scripts/process_docs.py` | 2h |
| Implement metadata extraction | Parse frontmatter, headers | 2h |
| Build ingestion script | `scripts/ingest.py` | 2h |
| Run initial ingestion | 15 docs in ChromaDB | 1h |
| Verify embeddings | Query test successful | 1h |

**Day 7 Checkpoint**: ✓ All 15 documents chunked and embedded in ChromaDB

---

## Week 2: RAG Pipeline Development

**Goal**: Working end-to-end RAG pipeline with basic UI

### Day 8-9: Retrieval Service

| Task | Deliverable | Time |
|------|-------------|------|
| Create embedding service | `src/services/embedding.js` | 2h |
| Connect to ChromaDB | `src/services/retrieval.js` | 2h |
| Implement similarity search | Top-k retrieval working | 2h |
| Add relevance filtering | Threshold-based filtering | 1h |
| Test retrieval quality | 10 manual query tests | 1h |

```javascript
// Key retrieval function
async function retrieve(query) {
    const embedding = await getEmbedding(query);
    const results = await collection.query({
        queryEmbeddings: [embedding],
        nResults: 5
    });
    return filterByRelevance(results, 0.7);
}
```

**Day 9 Checkpoint**: ✓ Retrieval returns relevant chunks for test queries

### Day 10-11: LLM Generation Service

| Task | Deliverable | Time |
|------|-------------|------|
| Create LLM service | `src/services/llm.js` | 2h |
| Design system prompt | `src/utils/prompts.js` | 2h |
| Implement context assembly | Format chunks for prompt | 2h |
| Add source extraction | Parse citations from response | 2h |
| Test generation quality | 10 manual tests | 1h |

```javascript
// Key generation function
async function generate(query, context) {
    const prompt = buildPrompt(query, context);
    const response = await groq.chat.completions.create({
        messages: [
            { role: "system", content: SYSTEM_PROMPT },
            { role: "user", content: prompt }
        ],
        model: "llama-3.1-8b-instant",
        temperature: 0.3
    });
    return parseResponse(response);
}
```

**Day 11 Checkpoint**: ✓ LLM generates sourced responses from retrieved context

### Day 12-13: API Integration

| Task | Deliverable | Time |
|------|-------------|------|
| Create Express server | `src/index.js` | 1h |
| Implement query endpoint | `POST /api/query` | 2h |
| Add health check | `GET /api/health` | 30m |
| Connect pipeline components | End-to-end flow | 2h |
| Error handling | Graceful failure modes | 2h |
| Test via Postman/curl | API working | 1h |

**Day 13 Checkpoint**: ✓ API accepts query, returns response with sources

### Day 14: Basic UI

| Task | Deliverable | Time |
|------|-------------|------|
| Create HTML page | `public/index.html` | 2h |
| Add CSS styling | Clean, minimal design | 1h |
| Implement JS fetch | Query submission | 1h |
| Display responses | Formatted with sources | 2h |
| Test user flow | Submit query, see response | 1h |

**Day 14 Checkpoint**: ✓ Can use co-pilot via browser interface

---

## Week 3: Integration & Testing

**Goal**: Expand knowledge base + systematic testing

### Day 15-16: Secondary Document Collection

| Task | Documents | Source |
|------|-----------|--------|
| Indonesia INSW requirements | LARTAS, permits | insw.go.id |
| Malaysia customs summary | De minimis, procedures | customs.gov.my |
| ATIGA Rules of Origin | RoO requirements | ASEAN sources |
| Container specifications | Dimensions, weights | Carrier sites |
| VGM procedures | Per carrier | Carrier sites |

**Day 16 Checkpoint**: ✓ 20 total documents in knowledge base

### Day 17-18: Synthetic Document Expansion

| Task | Documents | Purpose |
|------|-----------|---------|
| Escalation Procedure | Guide for when to escalate | UC-4.x support |
| COD Procedure | Cash-on-delivery process | Secondary scope |
| FTA Comparison Matrix | Form D vs E vs AK | UC-2.3 support |
| Carrier Contact Matrix | Who to contact for what | UC-3.3 support |
| Exception Handling Guide | Common issues and solutions | General support |

**Day 18 Checkpoint**: ✓ 25 documents ingested, covering all P1 use cases

### Day 19-20: Systematic Testing - Round 1

| Task | Deliverable | Time |
|------|-------------|------|
| Run 50 test queries | Documented results | 4h |
| Score each response | Accuracy rating (1-5) | 2h |
| Identify failure patterns | List of problematic queries | 2h |
| Categorize failures | Retrieval vs. generation issues | 1h |
| Document edge cases | Out-of-scope handling | 1h |

**Test Query Execution Process**:
```
For each query in test bank:
1. Submit query via UI
2. Record response
3. Score: 1=Wrong, 2=Partially correct, 3=Correct but incomplete, 4=Good, 5=Excellent
4. Note: Was source citation accurate?
5. Note: Did it correctly decline out-of-scope?
```

**Day 20 Checkpoint**: ✓ First round testing complete with issues documented

### Day 21: Iteration & Fixes

| Task | Deliverable | Time |
|------|-------------|------|
| Fix retrieval issues | Adjust chunking/threshold | 3h |
| Improve system prompt | Based on failure analysis | 2h |
| Add missing documents | For uncovered queries | 2h |
| Re-test fixed queries | Verification | 1h |

**Common Fixes**:
- Retrieval miss → Add document or adjust chunking
- Generation hallucination → Strengthen system prompt
- Wrong source cited → Check metadata preservation
- Too verbose → Adjust max_tokens, prompt instructions

**Day 21 Checkpoint**: ✓ Major issues addressed, pipeline improved

---

## Week 4: Evaluation & Documentation

**Goal**: Final evaluation, documentation, demo-ready

### Day 22-23: Systematic Testing - Round 2

| Task | Deliverable | Time |
|------|-------------|------|
| Re-run all 50 queries | Updated results | 3h |
| Calculate metrics | Deflection rate, accuracy | 2h |
| Compare to Round 1 | Improvement analysis | 1h |
| Final failure analysis | Remaining gaps | 2h |

**Metrics Calculation**:
```
Deflection Rate = (Queries scored 4-5) / Total Queries × 100%

Target: 40% (20/50 queries answered well)

Citation Accuracy = (Responses with correct sources) / (Responses with sources) × 100%

Target: 80%
```

**Day 23 Checkpoint**: ✓ Final metrics calculated

### Day 24-25: Documentation

| Task | Deliverable | Time |
|------|-------------|------|
| Update technical docs | Final architecture state | 2h |
| Document known limitations | What doesn't work well | 1h |
| Create user guide | How to use the co-pilot | 2h |
| Write deployment notes | How to run locally | 1h |
| Prepare demo script | Walkthrough for presentation | 2h |

**User Guide Outline**:
1. Starting the system
2. Asking effective questions
3. Understanding responses
4. When to escalate (system says "I don't know")
5. Providing feedback

**Day 25 Checkpoint**: ✓ All documentation complete

### Day 26-27: Demo Preparation

| Task | Deliverable | Time |
|------|-------------|------|
| Select demo queries | 5-7 impressive examples | 1h |
| Prepare failure examples | Show graceful degradation | 1h |
| Create presentation | POC summary slides | 3h |
| Practice demo flow | Smooth demonstration | 2h |
| Prepare Q&A responses | Anticipate questions | 1h |

**Demo Script Structure**:
1. Problem statement (2 min)
2. Solution overview (2 min)
3. Live demo - happy path (5 min)
4. Live demo - edge cases (3 min)
5. Results & metrics (2 min)
6. Next steps (1 min)

**Day 27 Checkpoint**: ✓ Demo ready for internal review

### Day 28-29: Buffer & Polish

| Task | Deliverable | Time |
|------|-------------|------|
| Address any remaining issues | Bug fixes | Variable |
| UI polish | Minor improvements | 2h |
| Final testing | Smoke test | 2h |
| Backup everything | Code, data, docs | 1h |

**Day 29 Checkpoint**: ✓ System stable, demo-ready

### Day 30: POC Complete

| Task | Deliverable |
|------|-------------|
| Internal demo | Present to CYAIRE team |
| Gather feedback | Document reactions, questions |
| Document learnings | What worked, what didn't |
| Plan Phase 2 | Based on POC results |

**Day 30 Checkpoint**: ✓ POC complete, decision point for Phase 2

---

## Daily Standup Template

```markdown
## Day [X] Standup

### Yesterday
- [What was completed]

### Today
- [What will be worked on]

### Blockers
- [Any issues preventing progress]

### Notes
- [Learnings, decisions, changes]
```

---

## Risk Mitigation

| Risk | Mitigation | Trigger |
|------|------------|---------|
| Document collection takes longer | Start with fewer, highest-value docs | Day 4 behind |
| Retrieval quality poor | Try different embedding model | Day 9 tests fail |
| LLM responses hallucinate | Strengthen prompt, lower temperature | Day 11 tests fail |
| 40% deflection not achievable | Document as learning, adjust target | Day 23 metrics |
| Time overrun | Cut secondary scope (COD, SLA) | Week 2 behind |

---

## Decision Points

### Day 7 Decision: Proceed with Pipeline?
- **Proceed if**: 12+ documents successfully ingested
- **Pivot if**: Ingestion pipeline broken, documents inadequate

### Day 14 Decision: Expand Scope?
- **Expand if**: Pipeline working well, time available
- **Focus if**: Pipeline needs work, stick to P1 only

### Day 23 Decision: Phase 2 Viability?
- **Viable if**: 35%+ deflection rate achieved
- **Needs work if**: Below 35%, identify gaps
- **Pivot if**: Below 25%, fundamental issues

---

## Success Criteria Checklist

### Technical
- [ ] ChromaDB running with 25+ documents
- [ ] Retrieval returns relevant results (>70% accuracy)
- [ ] LLM generates sourced responses
- [ ] API endpoint functional
- [ ] Basic UI working

### Quality
- [ ] 50 test queries executed
- [ ] 40% deflection rate achieved
- [ ] 80% citation accuracy
- [ ] Graceful "I don't know" for out-of-scope

### Documentation
- [ ] Architecture documented
- [ ] User guide complete
- [ ] Known limitations listed
- [ ] Demo script prepared

---

## Quick Reference: Key Commands

```bash
# Start development
cd waypoint-poc
source venv/bin/activate  # Python
npm run dev               # Node server

# Ingest documents
python scripts/ingest.py

# Run tests
npm test

# Check ChromaDB status
python -c "import chromadb; c=chromadb.PersistentClient('./chroma_db'); print(c.list_collections())"
```

---

*Next Document*: [06 - Evaluation Framework](./06_evaluation_framework.md)
