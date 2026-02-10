# Task 0: Workspace Setup

**Phase:** Phase 0 — Setup
**Initiative:** enhancement--poc-evaluation
**Covers:** Tasks 0.1–0.6

---

## Persona

You are a **DevOps and Build Engineer** with expertise in:
- Project scaffolding and codebase forking
- Python and Node.js environment management
- ChromaDB vector database administration
- Ingestion pipeline configuration
- Test suite validation across Python (pytest) and Node.js (Jest)

You ensure clean, reproducible builds with verified test suites.

---

## Context

### Initiative
Waypoint Phase 1 POC — Week 4 Evaluation & Documentation. Setting up the `05_evaluation/` workspace by forking the Week 3 codebase, fixing ingestion metadata, running fresh ingestion, and validating all existing tests pass.

### Reference Documents
- Master rules: `./CLAUDE.md`
- Week 4 plan: `./pilot_phase1_poc/05_evaluation/week4_plan.md` (Decisions #2, #27, #31)
- Week 3 final state: `./pilot_phase1_poc/04_retrieval_optimization/` (709 chunks, 30 docs, 92% hit rate)

### Working Directory
`./pilot_phase1_poc/05_evaluation/`

### Dependencies
- Week 3 complete (all 12 tasks, 92% retrieval hit rate)
- `04_retrieval_optimization/` contains: backend/, client/, kb/, scripts/, tests/, data/, configs

### Current State
- `05_evaluation/` directory exists with `ai-workflow/` folder and `week4_plan.md`
- No codebase, no venv, no node_modules, no chroma_db yet

---

## Task

### Objective
Create a fully functional `05_evaluation/` workspace with fresh ChromaDB ingestion and all existing tests passing. This proves the pipeline is reproducible and the knowledge base is self-contained.

### Sub-task 0.1: Create folder structure

Create the full folder structure per Decision #27:

```
pilot_phase1_poc/05_evaluation/
├── backend/                      # (will be copied)
├── client/                       # (will be copied)
├── kb/                           # (will be copied)
├── scripts/                      # (will be copied)
├── tests/                        # (will be copied)
├── chroma_db/                    # (built fresh via ingestion)
├── data/                         # Test results
├── logs/                         # System logs
├── reports/                      # Evaluation reports
├── documentation/                # Full documentation suite
│   ├── adrs/                     # Architecture Decision Records
│   ├── architecture/             # System overview, data flow, pipelines
│   ├── codebase/                 # Backend, frontend, scripts, tests docs
│   └── guides/                   # User guide, deployment, limitations
├── demo/                         # Presentation + Selenium
│   ├── presentation/             # Standalone Vite app
│   └── selenium/                 # Demo scripts + captures
```

### Sub-task 0.2: Copy codebase from 04_retrieval_optimization/

**Copy these:**
- `backend/` — full Express server
- `client/` — React frontend
- `kb/` — all 4 KB subdirectories including `pdfs/`
- `scripts/` — Python ingestion, chunking, retrieval test, PDF extractor
- `tests/` — all JS and Python test files
- `data/` — `retrieval_test_results.json`
- `logs/`
- Root configs: `.env`, `.env.example`, `.gitignore`, `package.json`, `package-lock.json`, `jest.config.js`, `requirements.txt`, `start.ps1`, `start.sh`

**Exclude (do NOT copy):**
- `ai-workflow/` — W3 workflow artifacts
- `ai-workflow-bootstrap-prompt-v3.md` — W3 bootstrap
- `Retrieval_Optimization_Plan.md` — W3 planning
- `REVISED_DOCUMENT_LIST.md` — W3 tracker
- `reports/` — all W3 reports
- `chroma_db/` — will be rebuilt fresh
- `venv/` — will be recreated
- `node_modules/` — will be reinstalled
- `.pytest_cache/`, `__pycache__/` — transient

### Sub-task 0.3: Setup environment

```bash
cd pilot_phase1_poc/05_evaluation
npm install
py -3.11 -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```

### Sub-task 0.4: Fix ingestion pipeline metadata

The current `ingest.py` does NOT store `source_urls`, `retrieval_keywords`, or `use_cases` in ChromaDB metadata. These fields are parsed by `process_docs.py` but dropped during `ingest_document()`.

**Update `scripts/ingest.py` `ingest_document()` metadata dict to include:**
- `source_urls` — joined as comma-separated string (ChromaDB metadata only supports string/int/float)
- `retrieval_keywords` — joined as comma-separated string
- `use_cases` — joined as comma-separated string

This aligns with the existing `citations.js` pattern which already splits `source_urls` by comma.

**Implementation detail:**
```python
# In ingest_document(), when building metadata dict for each chunk:
metadata["source_urls"] = ",".join(doc.get("source_urls", []))
metadata["retrieval_keywords"] = ",".join(doc.get("retrieval_keywords", []))
metadata["use_cases"] = ",".join(doc.get("use_cases", []))
```

### Sub-task 0.5: Run fresh ingestion

```bash
cd pilot_phase1_poc/05_evaluation
venv/Scripts/activate
python scripts/ingest.py --clear
```

**Validate:**
- Document count: 30
- Chunk count: ~709
- Spot-check: `source_urls` present in ChromaDB chunks
- Spot-check: `retrieval_keywords` present in ChromaDB chunks

### Sub-task 0.6: Run ALL existing tests

```bash
# Python tests
python -m pytest tests/ -v

# Jest tests
npm test

# Retrieval quality
python scripts/retrieval_quality_test.py

# Smoke test: start backend, submit test query
npm start
# Verify response includes citations
```

**Expected results:**
- pytest: all ingestion tests pass
- Jest: all backend tests pass
- Retrieval: 92% hit rate (46/50 or better)
- Smoke test: response with citations returned

---

## Format

### Output Location
`./pilot_phase1_poc/05_evaluation/ai-workflow/enhancement--poc-evaluation/04-prompts/00-setup/task_0_workspace_setup/02-output/TASK_0_OUTPUT.md`

### Output Report Sections
1. **Summary** — What was accomplished
2. **Folder Structure** — Tree view of created structure
3. **Copy Manifest** — Files/folders copied and excluded
4. **Metadata Fix** — Code changes to ingest.py
5. **Ingestion Results** — Document count, chunk count, metadata spot-check
6. **Test Results** — pytest, Jest, retrieval hit rate, smoke test
7. **Issues** — Any problems encountered
8. **Next Steps** — Ready for Phase 1 (UX Redesign)

### Update on Completion
- [ ] Checklist: Mark Tasks 0.1–0.6 complete
- [ ] Roadmap: Update status for all Phase 0 tasks

---

## Validation Criteria

This task is complete when:
- [ ] `05_evaluation/` folder structure matches Decision #27
- [ ] Codebase copied (backend, client, kb, scripts, tests, configs)
- [ ] W3-specific artifacts excluded
- [ ] npm install succeeds
- [ ] Python venv created, requirements installed
- [ ] `ingest.py` updated with source_urls, retrieval_keywords, use_cases metadata
- [ ] Fresh ingestion: 30 docs, ~709 chunks
- [ ] source_urls verified in ChromaDB chunks
- [ ] pytest passes (all tests)
- [ ] npm test passes (all tests)
- [ ] retrieval_quality_test.py: 92% hit rate
- [ ] Backend starts, test query returns response with citations
- [ ] Output report created
- [ ] Tracking docs updated

**→ CHECKPOINT 1: All existing tests pass on fresh ingestion with new metadata fields.**
