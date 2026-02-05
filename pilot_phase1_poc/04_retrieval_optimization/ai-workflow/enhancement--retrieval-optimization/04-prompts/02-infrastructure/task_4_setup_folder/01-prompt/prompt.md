# Task 4: Set Up 04_retrieval_optimization Folder

## Persona

**Role**: Senior Python Developer / DevOps Engineer

**Expertise**:
- Python project scaffolding and virtual environment management
- Configuration management with `.env` and `dotenv`
- ChromaDB ingestion pipelines
- File system operations and cross-platform scripting (Windows)

---

## Context

### Background

Phase 1 (Audit) is complete. We identified 9 failing queries, reclassified 3 as out-of-scope, and produced a revised document list of 30 documents. Phase 2 begins with setting up the working environment: a **forked** ingestion pipeline in `04_retrieval_optimization/` that is independent from the original `02_ingestion_pipeline/` (which must remain untouched).

### Current State

- **Status**: `04_retrieval_optimization/` exists with audit reports, roadmap, and plan files but has **no scripts, no kb/, no venv, no requirements.txt**
- **Source pipeline**: `02_ingestion_pipeline/` contains the working ingestion pipeline (scripts, config, tests, requirements.txt)
- **Retrieval test**: `03_rag_pipeline/scripts/retrieval_quality_test.py` needs to be copied for validation

### References

| Document | Path | Purpose |
|----------|------|---------|
| Implementation Roadmap | `04_retrieval_optimization/ai-workflow/enhancement--retrieval-optimization/02-roadmap/IMPLEMENTATION_ROADMAP.md` | Task 4 checklist |
| Detailed Plan | `04_retrieval_optimization/ai-workflow/enhancement--retrieval-optimization/01-plan/DETAILED_PLAN.md` | Folder structure specs, chunking params |
| Revised Document List | `04_retrieval_optimization/REVISED_DOCUMENT_LIST.md` | KB categories and documents |
| Source config.py | `02_ingestion_pipeline/scripts/config.py` | Config to fork and parameterize |
| Source requirements.txt | `02_ingestion_pipeline/requirements.txt` | Dependencies to fork |
| Source ingest.py | `02_ingestion_pipeline/scripts/ingest.py` | Ingestion entry point to fork |
| Source process_docs.py | `02_ingestion_pipeline/scripts/process_docs.py` | Document processing to fork |
| Source chunker.py | `02_ingestion_pipeline/scripts/chunker.py` | Chunking logic to fork |
| Source verify_ingestion.py | `02_ingestion_pipeline/scripts/verify_ingestion.py` | Verification script to fork |
| Retrieval quality test | `03_rag_pipeline/scripts/retrieval_quality_test.py` | Retrieval testing to copy |

### Dependencies

- **Completed**: Task 1 (Audit), Task 2 (Scope Reclassification), Task 3 (Revised Document List)
- **Blocks**: Task 5 (PDF Extraction), Task 6 (KB Rebuild)

---

## Task

### Objective

Create the complete folder structure and forked ingestion pipeline in `04_retrieval_optimization/` with parameterized chunking via `.env`, so that Tasks 5-10 have a working environment.

### Requirements

1. **Create directory structure** under `04_retrieval_optimization/`:
   ```
   04_retrieval_optimization/
   ├── scripts/              # Forked pipeline scripts
   │   ├── __init__.py
   │   ├── config.py         # Updated with parameterized chunking
   │   ├── process_docs.py   # Forked from 02_
   │   ├── chunker.py        # Forked from 02_
   │   ├── ingest.py         # Forked with --clear flag
   │   ├── verify_ingestion.py
   │   ├── view_chroma.py
   │   └── retrieval_quality_test.py  # Copied from 03_rag_pipeline
   ├── tests/                # Test directory
   │   └── __init__.py
   ├── kb/                   # Empty KB folders (content added in Task 6)
   │   ├── 01_regulatory/
   │   │   └── pdfs/
   │   ├── 02_carriers/
   │   │   └── pdfs/
   │   ├── 03_reference/
   │   │   └── pdfs/
   │   └── 04_internal_synthetic/
   │       └── pdfs/
   ├── chroma_db/            # Created at runtime
   ├── logs/                 # Log output
   ├── requirements.txt      # Forked + pymupdf4llm added
   ├── .env                  # Parameterized config
   └── .gitignore            # Ignore venv, chroma_db, __pycache__
   ```

2. **Fork scripts from `02_ingestion_pipeline/scripts/`**:
   - Copy all 6 Python scripts (`config.py`, `process_docs.py`, `chunker.py`, `ingest.py`, `verify_ingestion.py`, `view_chroma.py`, `__init__.py`)
   - Copy `retrieval_quality_test.py` from `03_rag_pipeline/scripts/`

3. **Update `config.py`** with these changes:
   - Change `KNOWLEDGE_BASE_PATH` to point to local `./kb` (not `../01_knowledge_base/kb`)
   - Change `CHROMA_PERSIST_PATH` default to `./chroma_db`
   - **Parameterize** `CHUNK_SIZE` and `CHUNK_OVERLAP` via `.env` (currently hardcoded as `600` and `90`)
   - Keep all other config the same (EMBEDDING_MODEL, COLLECTION_NAME, etc.)
   - Relax the KB directory check: warn instead of raising `FileNotFoundError` if KB dir is empty (we'll add content in Task 6)

4. **Create `.env` file** with defaults:
   ```
   CHUNK_SIZE=600
   CHUNK_OVERLAP=90
   COLLECTION_NAME=waypoint_kb
   CHROMA_PERSIST_PATH=./chroma_db
   KNOWLEDGE_BASE_PATH=./kb
   LOG_LEVEL=INFO
   ```

5. **Create `requirements.txt`** forked from `02_ingestion_pipeline/requirements.txt`:
   ```
   chromadb==0.5.23
   langchain-text-splitters==0.0.1
   python-dotenv==1.0.0
   python-frontmatter==1.1.0
   pyyaml==6.0.1
   requests>=2.31.0
   tqdm==4.66.1
   pymupdf4llm>=0.0.17
   pytest>=8.0.0
   pytest-cov>=4.1.0
   ```

6. **Create `.gitignore`**:
   ```
   venv/
   __pycache__/
   *.pyc
   chroma_db/
   .env
   logs/*.log
   ```

7. **Set up Python virtual environment**:
   ```bash
   cd pilot_phase1_poc/04_retrieval_optimization
   py -3.11 -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

8. **Verify pipeline runs on empty KB**:
   - `python scripts/ingest.py --dry-run` should start but gracefully handle empty KB (no crash)
   - `python scripts/verify_ingestion.py` should report 0 documents/chunks

### Specifications

```python
# config.py key changes:
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "600"))       # Was hardcoded 600
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "90"))  # Was hardcoded 90
KNOWLEDGE_BASE_PATH = PIPELINE_ROOT / os.getenv("KNOWLEDGE_BASE_PATH", "./kb")
CHROMA_PERSIST_PATH = PIPELINE_ROOT / os.getenv("CHROMA_PERSIST_PATH", "./chroma_db")
```

### Constraints

- **DO NOT modify** anything in `02_ingestion_pipeline/` — it is the Week 1 stable baseline (protected path)
- **DO NOT modify** anything in `01_knowledge_base/kb/` — it is the original KB baseline (protected path)
- Use `py -3.11` for venv creation on Windows
- All paths must work on Windows (use `Path` objects, not hardcoded forward slashes)
- Keep the `.env` file in `.gitignore` but commit a `.env.example` with the same defaults

### Acceptance Criteria

- [ ] Directory structure matches the spec above
- [ ] All 7 scripts are present in `scripts/`
- [ ] `config.py` reads `CHUNK_SIZE` and `CHUNK_OVERLAP` from `.env`
- [ ] `config.py` paths point to local `./kb` and `./chroma_db`
- [ ] `kb/` has 4 category folders each with a `pdfs/` subfolder
- [ ] `requirements.txt` includes `pymupdf4llm`
- [ ] `.gitignore` is present and correct
- [ ] `.env` and `.env.example` exist with correct defaults
- [ ] Python venv created and `pip install -r requirements.txt` succeeds
- [ ] `python scripts/ingest.py --dry-run` runs without crashing on empty KB
- [ ] `python scripts/verify_ingestion.py` runs and reports 0 docs/chunks
- [ ] No files in `02_ingestion_pipeline/` or `01_knowledge_base/kb/` were modified

---

## Format

### Output Structure

```
04_retrieval_optimization/
├── scripts/
│   ├── __init__.py
│   ├── config.py          (updated)
│   ├── process_docs.py    (forked)
│   ├── chunker.py         (forked)
│   ├── ingest.py          (forked)
│   ├── verify_ingestion.py (forked)
│   ├── view_chroma.py     (forked)
│   └── retrieval_quality_test.py (copied from 03_)
├── tests/
│   └── __init__.py
├── kb/
│   ├── 01_regulatory/pdfs/
│   ├── 02_carriers/pdfs/
│   ├── 03_reference/pdfs/
│   └── 04_internal_synthetic/pdfs/
├── logs/
├── requirements.txt
├── .env
├── .env.example
└── .gitignore
```

### Code Style

- Python 3.11+ type hints
- Docstrings for modified functions
- Use `pathlib.Path` for all path operations
- Follow existing code conventions from `02_ingestion_pipeline`

### Documentation

- Add a brief comment header to `config.py` noting it was forked from `02_ingestion_pipeline`
- Log which `.env` values are loaded at startup (DEBUG level)

### Validation Commands

```bash
cd pilot_phase1_poc/04_retrieval_optimization

# Activate venv
venv\Scripts\activate

# Verify all scripts exist
python -c "import scripts.config; print('Config OK:', scripts.config.CHUNK_SIZE)"

# Test parameterization
python -c "import scripts.config as c; assert c.CHUNK_SIZE == 600; assert c.CHUNK_OVERLAP == 90; print('Defaults OK')"

# Run on empty KB (should not crash)
python scripts/ingest.py --dry-run

# Verify empty state
python scripts/verify_ingestion.py

# Run tests
python -m pytest tests/ -v
```

---

## Notes

- The `retrieval_quality_test.py` script may need path adjustments when copied from `03_rag_pipeline/scripts/` — update its ChromaDB path to point to the local `chroma_db/` in `04_retrieval_optimization/`
- Task 5 (PDF Extraction) will add `pdf_extractor.py` to the `scripts/` folder — leave room for it
- Task 6 will populate `kb/` — the empty folders with `pdfs/` subfolders are placeholders
- The `ingest.py` fork should support a `--clear` flag to wipe ChromaDB before re-ingestion (check if it already does)
