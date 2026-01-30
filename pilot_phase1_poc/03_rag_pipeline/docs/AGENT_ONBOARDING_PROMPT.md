# One-Shot Agent Onboarding: RAG Pipeline (Week 2)

**Purpose**: This prompt provides all context needed to work on Waypoint RAG Pipeline tasks.

---

## Project Context

**Waypoint** is a RAG-based customer service co-pilot for freight forwarding. Week 1 completed the ingestion pipeline (29 docs → 483 chunks in ChromaDB). Week 2 builds the full RAG pipeline.

**Current State**: Task 1.1 complete. KB and ingestion copied to `03_rag_pipeline/`.

---

## Critical Files to Read First

Before ANY task, read these files in order:

1. **Roadmap**: `pilot_phase1_poc/03_rag_pipeline/docs/01_implementation_roadmap.md`
   - Check task status (⬜ Not Started | 🟡 In Progress | ✅ Complete)
   - Verify dependencies are complete
   - Read acceptance criteria

2. **PCTF Template**: `pilot_phase1_poc/03_rag_pipeline/prompts/00_PCTF_TEMPLATE.md`
   - Follow this format for all task prompts
   - Includes MCP tools for documentation lookup
   - Includes TDD requirements for Python and Node.js

3. **Week 2 Plan**: `pilot_phase1_poc/03_rag_pipeline/docs/00_week2_rag_pipeline_plan.md`
   - Full technical specifications
   - Architecture decisions
   - API response formats

---

## Task Execution Workflow

### Before Starting a Task

```
1. Read roadmap → Find task → Check status is ⬜ or 🟡
2. Check dependencies → All must be ✅
3. Read the task's prompt.md if it exists
4. If prompt.md doesn't exist, create it using PCTF format
```

### During Task Execution

```
1. Follow TDD: Write tests FIRST, then implement
   - Python: tests/test_<module>.py with pytest
   - Node.js: tests/<module>.test.js with Jest

2. Use MCP tools for library docs BEFORE implementing:
   - docfork:docfork_search_docs → search library documentation
   - docfork:docfork_read_url → read full doc pages
   - context7 → alternative for library docs

3. Run validation commands from the roadmap
```

### After Task Completion

```
1. Create REPORT.md in the task folder:
   prompts/[GROUP]_[TASK]_[description]/REPORT.md

2. Update roadmap:
   - Mark checkboxes [x]
   - Update status: ⬜ → ✅
   - Update Progress Tracker totals

3. Commit changes with descriptive message
```

---

## Folder Naming Convention

Task folders follow: `[GROUP]_[GROUP.SUBTASK]_[description]/`

Examples:
- `01_1.1_copy_assets/`
- `01_1.2_source_url_fix/`
- `02_2.1_retrieval_quality_test/`
- `05_5.1_llm_service/`

---

## Current Progress

| Group | Tasks | Status |
|-------|-------|--------|
| 1. Project Setup | 1/2 | 🟡 In Progress |
| 2-9. Remaining | 0/16 | ⬜ Not Started |
| **TOTAL** | **1/18** | **6%** |

**Next Task**: 1.2 - Fix source_urls in Ingestion

---

## Key Technical Decisions

| Setting | Value |
|---------|-------|
| Embeddings | ChromaDB default (all-MiniLM-L6-v2, 384-d) |
| LLM | Groq API (Llama 3.1 8B) |
| Backend | Node.js + Express |
| Frontend | React + Tailwind |
| top_k | 10 |
| relevance_threshold | 0.15 |
| temperature | 0.3 |

---

## Directory Structure

```
03_rag_pipeline/
├── kb/                     # Knowledge base (29 docs) ✅
├── ingestion/              # Python ingestion pipeline ✅
│   ├── scripts/            # Python modules
│   ├── tests/              # pytest tests
│   ├── chroma_db/          # Vector DB (created on ingest)
│   └── .env                # Config
├── src/                    # Node.js backend (to be created)
│   ├── services/           # retrieval.js, llm.js, pipeline.js
│   ├── routes/             # Express routes
│   └── prompts/            # System prompt
├── client/                 # React UI (to be created)
├── docs/                   # Planning docs
│   ├── 00_week2_rag_pipeline_plan.md
│   ├── 01_implementation_roadmap.md
│   └── AGENT_ONBOARDING_PROMPT.md (this file)
├── prompts/                # PCTF task prompts
│   ├── 00_PCTF_TEMPLATE.md
│   └── 01_1.1_copy_assets/
│       ├── prompt.md
│       └── REPORT.md
├── scripts/                # Python evaluation scripts
├── tests/                  # Jest tests (Node.js)
└── logs/
```

---

## PCTF Format Summary

Every task prompt must include:

```markdown
# Task [ID]: [Title]

## Persona
> Role and expertise

## Context
- Project Background
- Current State
- Reference Documents
- Dependencies

## Task
- Objective
- Requirements (numbered list)
- Specifications
- Constraints
- Acceptance Criteria (checkboxes)
- TDD Requirements

## Format
- Output Structure
- Code Style
- Validation Commands
```

---

## REPORT.md Format Summary

Every completed task must have:

```markdown
# Task [ID]: [Title] - Output Report

**Completed**: [Date]
**Status**: Complete / Partial / Failed

## Summary
[What was accomplished]

## Files Created/Modified
| File | Action | Path |

## Acceptance Criteria
- [x] Completed items
- [ ] Incomplete items

## Issues Encountered
[Any problems or "None"]

## Next Steps
[Follow-up tasks]
```

---

## Commands Quick Reference

```bash
# Ingestion (Python)
cd pilot_phase1_poc/03_rag_pipeline/ingestion
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m scripts.ingest --clear
python -m scripts.verify_ingestion

# Node.js (after Task 3.1)
cd pilot_phase1_poc/03_rag_pipeline
npm install
npm test
npm start

# React UI (after Task 7.1)
cd pilot_phase1_poc/03_rag_pipeline/client
npm install
npm run dev
```

---

## Remember

1. **Always read the roadmap first** - know what's done and what's next
2. **Always create REPORT.md** - document your work
3. **Always update the roadmap** - keep progress accurate
4. **Use MCP tools for docs** - don't guess at library APIs
5. **Follow TDD** - tests first, then implementation
