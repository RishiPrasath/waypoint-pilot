# Task 1.1: Copy KB and Ingestion to RAG Pipeline

## Persona

> You are a DevOps engineer with expertise in project structure organization and file management.
> You follow clean architecture principles and ensure all paths and dependencies are correctly configured after file operations.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. Week 1 completed the ingestion pipeline (29 docs → 483 chunks in ChromaDB). Week 2 builds the full RAG pipeline which needs its own copy of the knowledge base and ingestion tools for self-contained operation.

### Current State
- Knowledge base exists at: `pilot_phase1_poc/01_knowledge_base/kb/` (29 documents)
- Ingestion pipeline exists at: `pilot_phase1_poc/02_ingestion_pipeline/` (complete with scripts, tests, chroma_db)
- RAG pipeline folder exists at: `pilot_phase1_poc/03_rag_pipeline/` (coordination files only)

### Reference Documents
- `03_rag_pipeline/docs/00_week2_rag_pipeline_plan.md` - Week 2 plan with target structure
- `02_ingestion_pipeline/docs/01_implementation_roadmap.md` - Completed ingestion tasks

### Dependencies
- None (this is the first task)

---

## Task

### Objective
Copy the knowledge base and ingestion pipeline into the RAG pipeline folder so Week 2 development is self-contained.

### Requirements

1. **Copy Knowledge Base**
   - Source: `pilot_phase1_poc/01_knowledge_base/kb/`
   - Destination: `pilot_phase1_poc/03_rag_pipeline/kb/`
   - Include all 4 subdirectories with all 29 markdown files
   - Do NOT copy meta files (PROGRESS_CHECKLIST.md, SCRAPER_EXECUTION_PLAN.md)

2. **Copy Ingestion Pipeline**
   - Source: `pilot_phase1_poc/02_ingestion_pipeline/`
   - Destination: `pilot_phase1_poc/03_rag_pipeline/ingestion/`
   - Include: `scripts/`, `tests/`, `requirements.txt`, `.env.example`, `README.md`
   - Do NOT copy: `chroma_db/`, `logs/`, `.env`, `venv/`, `__pycache__/`, `prompts/`, `docs/`

3. **Update Paths in Ingestion Config**
   - Update `ingestion/scripts/config.py` to use new relative path to KB
   - Change `KNOWLEDGE_BASE_PATH` from `../01_knowledge_base/kb` to `../kb`

4. **Create .env from .env.example**
   - Copy `.env.example` to `.env` in the ingestion folder

### Specifications

**Target Structure**:
```
03_rag_pipeline/
├── kb/                         # Copied from 01_knowledge_base/kb/
│   ├── 01_regulatory/          # 14 docs
│   ├── 02_carriers/            # 6 docs
│   ├── 03_reference/           # 3 docs
│   └── 04_internal_synthetic/  # 6 docs
│
├── ingestion/                  # Copied from 02_ingestion_pipeline/
│   ├── scripts/
│   │   ├── __init__.py
│   │   ├── config.py           # Updated KB path
│   │   ├── process_docs.py
│   │   ├── chunker.py
│   │   ├── ingest.py
│   │   ├── verify_ingestion.py
│   │   └── view_chroma.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_process_docs.py
│   │   ├── test_chunker.py
│   │   ├── test_ingest.py
│   │   └── test_verify_ingestion.py
│   ├── .env                    # Created from .env.example
│   ├── .env.example
│   ├── requirements.txt
│   └── README.md
│
├── docs/
├── prompts/
├── scripts/
├── tests/
└── logs/
```

### Constraints
- Do NOT modify source files in `01_knowledge_base/` or `02_ingestion_pipeline/`
- Do NOT copy any generated files (chroma_db, logs, venv, __pycache__)
- Do NOT copy prompt/report files from ingestion (they stay with that component)

### Acceptance Criteria
- [ ] `03_rag_pipeline/kb/` contains all 29 markdown documents across 4 subdirectories
- [ ] `03_rag_pipeline/ingestion/scripts/` contains all 6 Python modules
- [ ] `03_rag_pipeline/ingestion/tests/` contains all test files
- [ ] `03_rag_pipeline/ingestion/scripts/config.py` has updated `KNOWLEDGE_BASE_PATH`
- [ ] `03_rag_pipeline/ingestion/.env` exists (copied from .env.example)
- [ ] venv can be created and packages installed
- [ ] Ingestion runs successfully with `python -m scripts.ingest --dry-run`

### TDD Requirements
- N/A (file copy task, no new code)

---

## Format

### Output Structure
Files copied as specified in target structure above.

### Validation Commands

```bash
cd pilot_phase1_poc/03_rag_pipeline

# Verify KB copied (should show 29 files)
find kb -name "*.md" | wc -l
# Or on Windows:
dir /s /b kb\*.md | find /c ".md"

# Verify ingestion scripts copied
ls ingestion/scripts/

# Verify config path updated
grep "KNOWLEDGE_BASE_PATH" ingestion/scripts/config.py

# Setup venv and test
cd ingestion
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Test dry run (should discover 29 docs)
python -m scripts.ingest --dry-run

# Verify document discovery
python -c "from scripts.process_docs import discover_documents; from scripts.config import KNOWLEDGE_BASE_PATH; docs = discover_documents(KNOWLEDGE_BASE_PATH); print(f'Found {len(docs)} documents')"
```

### Expected Dry Run Output
```
[DRY RUN] Would process 29 documents
[DRY RUN] Would create ~483 chunks
[DRY RUN] No changes made to ChromaDB
```
