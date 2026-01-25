# Ingestion Pipeline Implementation Checklist

**Project**: Waypoint Phase 1 POC  
**Component**: Document Ingestion Pipeline  
**Estimated Time**: 10-12 hours

---

## Progress Tracker

| Group | Tasks | Status |
|-------|-------|--------|
| 1. Environment Setup | 6/6 | ✅ Complete |
| 2. Configuration Module | 0/1 | ⬜ Not Started |
| 3. Document Processor | 0/2 | ⬜ Not Started |
| 4. Chunking Engine | 0/2 | ⬜ Not Started |
| 5. Main Ingestion Script | 0/2 | ⬜ Not Started |
| 6. Verification Script | 0/2 | ⬜ Not Started |
| 7. Documentation | 0/1 | ⬜ Not Started |
| 8. CI/CD (Optional) | 0/1 | ⬜ Not Started |
| **TOTAL** | **6/17** | **35%** |

**Status Legend**: ⬜ Not Started | 🟡 In Progress | ✅ Complete | ❌ Blocked

---

## Task Group 1: Environment Setup
**Duration**: 1.5-2 hours | **Prompt Folder**: `prompts/01_environment_setup/`

### Task 1.1: Create Folder Structure
- [x] `scripts/` directory created
- [x] `scripts/__init__.py` exists
- [x] `tests/` directory created
- [x] `logs/` directory created

**Target Structure**:
```
02_ingestion_pipeline/
├── scripts/
│   └── __init__.py
├── tests/
├── logs/
├── chroma_db/              (auto-created)
```

**Status**: ✅ | **Report**: `prompts/01_1.1_folder_structure/REPORT.md`

---

### Task 1.2: Create requirements.txt
- [x] File created at `requirements.txt`
- [x] chromadb==0.5.23 *(updated from 0.4.22 for numpy 2.0 compatibility)*
- [x] google-genai>=1.0.0 *(Gemini API for embeddings)*
- [x] python-frontmatter==1.1.0
- [x] langchain-text-splitters==0.0.1
- [x] pyyaml==6.0.1
- [x] tqdm==4.66.1
- [x] python-dotenv==1.0.0
- [x] requests>=2.31.0

**Status**: ✅ | **Report**: `prompts/01_1.2_requirements/REPORT.md`

---

### Task 1.3: Create Environment Files
- [x] `.env.example` created
- [x] `.env` created (copy of example)
- [x] GOOGLE_API_KEY defined *(required for Gemini API)*
- [x] EMBEDDING_MODEL defined (`gemini-embedding-001`)
- [x] EMBEDDING_DIMENSIONS defined (`768`)
- [x] CHROMA_PERSIST_PATH defined
- [x] COLLECTION_NAME defined
- [x] KNOWLEDGE_BASE_PATH defined
- [x] LOG_LEVEL defined

**Status**: ✅ | **Report**: `prompts/01_1.3_env_files/REPORT.md`

---

### Task 1.4: Create Docker Configuration
- [x] `Dockerfile` created
- [x] Single-stage build *(no model caching needed with Gemini API)*
- [x] `docker-compose.yml` created
- [x] GOOGLE_API_KEY passthrough configured
- [x] Volume mounts configured (knowledge_base, chroma_db, logs)
- [x] Environment variables configured
- [x] Verify profile configured
- [x] `.dockerignore` created

**Status**: ✅ | **Report**: `prompts/01_1.4_docker_config/REPORT.md`

---

### Task 1.5: Verify Docker Setup
- [x] `docker-compose build` succeeds
- [x] Image size < 800MB *(target: ~500MB with Gemini API)*
- [x] Container can import chromadb
- [x] Container can import google-genai
- [x] Gemini API returns 768-dimension embeddings

**Validation Commands**:
```bash
docker-compose build
docker images | grep waypoint
docker-compose run --rm --entrypoint python ingestion -c "import chromadb; print('OK')"
docker-compose run --rm --entrypoint python ingestion -c "from google import genai; print('OK')"
```

**Status**: ✅ | **Report**: `prompts/01_1.5_docker_verify/REPORT.md`

---

### Task 1.6: (Optional) Local Virtual Environment
- [x] venv created (Python 3.11.0)
- [x] All packages installed
- [x] `import chromadb` works
- [x] `from google import genai` works
- [x] Environment variables load from `.env`
- [x] Gemini API returns 768-d embeddings (with config)

**Validation Commands**:
```bash
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -c "import chromadb; print('OK')"
python -c "from google import genai; print('OK')"
```

**Note**: Use `py -3.11` on Windows since chromadb doesn't support Python 3.14 yet.

**Status**: ✅ | **Report**: `prompts/01_1.6_local_venv/REPORT.md`

---

## Task Group 2: Configuration Module
**Duration**: 30 minutes | **Prompt Folder**: `prompts/02_configuration_module/`

### Task 2.1: Create config.py
- [ ] File created at `scripts/config.py`
- [ ] Loads from `.env` with dotenv
- [ ] CHROMA_PERSIST_PATH (Path object)
- [ ] KNOWLEDGE_BASE_PATH (Path object)
- [ ] LOG_DIR (Path object)
- [ ] EMBEDDING_MODEL = "gemini-embedding-001"
- [ ] EMBEDDING_DIMENSIONS = 768
- [ ] CHUNK_SIZE = 600
- [ ] CHUNK_OVERLAP = 90
- [ ] SEPARATORS list defined
- [ ] COLLECTION_NAME defined
- [ ] Directories auto-created if missing
- [ ] Works in Docker environment
- [ ] Works in local environment

**Validation Commands**:
```bash
# Docker
docker-compose run --rm ingestion python -c "from scripts.config import *; print(KNOWLEDGE_BASE_PATH)"

# Local
python -c "from scripts.config import *; print(KNOWLEDGE_BASE_PATH)"
```

**Status**: ⬜ | **Report**: `prompts/02_configuration_module/02_2.1_config_module_REPORT.md`

---

## Task Group 3: Document Processor
**Duration**: 1.5-2 hours | **Prompt Folder**: `prompts/03_document_processor/`

### Task 3.1: Create process_docs.py
- [ ] File created at `scripts/process_docs.py`
- [ ] `discover_documents(path)` function
- [ ] `parse_frontmatter(content)` function
- [ ] `extract_content(content)` function
- [ ] `get_category(file_path)` function
- [ ] `parse_document(file_path)` function
- [ ] Returns structured doc object with all fields:
  - [ ] doc_id
  - [ ] file_path
  - [ ] title
  - [ ] source_org
  - [ ] source_urls
  - [ ] category
  - [ ] jurisdiction
  - [ ] use_cases
  - [ ] last_updated
  - [ ] source_type
  - [ ] content
- [ ] Handles missing optional fields gracefully

**Status**: ⬜ | **Report**: `prompts/03_document_processor/03_3.1_process_docs_REPORT.md`

---

### Task 3.2: Test Document Processor
- [ ] Discovers all 29 documents
- [ ] Parses 01_regulatory document correctly
- [ ] Parses 02_carriers document correctly
- [ ] Parses 03_reference document correctly
- [ ] Parses 04_internal_synthetic document correctly

**Validation Commands**:
```bash
docker-compose run --rm ingestion python -c "
from scripts.process_docs import discover_documents, parse_document
from scripts.config import KNOWLEDGE_BASE_PATH
docs = discover_documents(KNOWLEDGE_BASE_PATH)
print(f'Found {len(docs)} documents')
"
```

**Status**: ⬜ | **Report**: `prompts/03_document_processor/03_3.2_test_processor_REPORT.md`

---

## Task Group 4: Chunking Engine
**Duration**: 1.5-2 hours | **Prompt Folder**: `prompts/04_chunking_engine/`

### Task 4.1: Create chunker.py
- [ ] File created at `scripts/chunker.py`
- [ ] `extract_section_header(content, position)` function
- [ ] `extract_subsection_header(content, position)` function
- [ ] `chunk_document(doc)` function
- [ ] `generate_chunk_id(doc_id, index)` function
- [ ] Chunk size: 600 chars
- [ ] Chunk overlap: 90 chars (15%)
- [ ] Separators: `["\n## ", "\n### ", "\n\n", "\n"]`
- [ ] Zero-padded chunk IDs (e.g., `_chunk_003`)
- [ ] All 12 metadata fields carried through

**Status**: ⬜ | **Report**: `prompts/04_chunking_engine/04_4.1_chunker_REPORT.md`

---

### Task 4.2: Test Chunker
- [ ] Produces ~350-400 total chunks
- [ ] Section headers extracted correctly
- [ ] Subsection headers extracted correctly
- [ ] Chunk IDs are zero-padded
- [ ] All metadata present in chunks

**Validation Commands**:
```bash
docker-compose run --rm ingestion python -c "
from scripts.process_docs import discover_documents, parse_document
from scripts.chunker import chunk_document
from scripts.config import KNOWLEDGE_BASE_PATH
docs = discover_documents(KNOWLEDGE_BASE_PATH)
total = sum(len(chunk_document(parse_document(d))) for d in docs)
print(f'Total chunks: {total}')
"
```

**Status**: ⬜ | **Report**: `prompts/04_chunking_engine/04_4.2_test_chunker_REPORT.md`

---

## Task Group 5: Main Ingestion Script
**Duration**: 2-3 hours | **Prompt Folder**: `prompts/05_main_ingestion_script/`

### Task 5.1: Create ingest.py
- [ ] File created at `scripts/ingest.py`
- [ ] CLI argument: `--verbose`
- [ ] CLI argument: `--dry-run`
- [ ] CLI argument: `--category <n>`
- [ ] Initializes embedding model
- [ ] Initializes ChromaDB client
- [ ] Discovers documents
- [ ] Parses documents
- [ ] Chunks documents
- [ ] Generates embeddings (batch)
- [ ] Clears existing collection
- [ ] Stores chunks with metadata
- [ ] Logs progress per document
- [ ] Prints summary
- [ ] Skips failed documents and continues
- [ ] Shows summary of failures

**Status**: ⬜ | **Report**: `prompts/05_main_ingestion_script/05_5.1_ingest_script_REPORT.md`

---

### Task 5.2: Run Full Ingestion
- [ ] Runs end-to-end without errors
- [ ] Processes all 29 documents
- [ ] Stores ~350-400 chunks
- [ ] `--dry-run` works (no storage)
- [ ] `--verbose` shows chunk details
- [ ] `--category` filters correctly
- [ ] ChromaDB persisted in `chroma_db/`
- [ ] Data persists after container stops

**Validation Commands**:
```bash
# Full run
docker-compose run --rm ingestion

# Dry run
docker-compose run --rm ingestion --dry-run

# Verbose
docker-compose run --rm ingestion --verbose

# Single category
docker-compose run --rm ingestion --category 01_regulatory
```

**Status**: ⬜ | **Report**: `prompts/05_main_ingestion_script/05_5.2_run_ingestion_REPORT.md`

---

## Task Group 6: Verification Script
**Duration**: 1-1.5 hours | **Prompt Folder**: `prompts/06_verification_script/`

### Task 6.1: Create verify_ingestion.py
- [ ] File created at `scripts/verify_ingestion.py`
- [ ] Check 1: Total chunk count (~350-400)
- [ ] Check 2: Category distribution (all 4 present)
- [ ] Check 3: Metadata integrity
- [ ] Check 4: Tier 1 retrieval tests (8 queries)
- [ ] Check 5: Tier 2 retrieval tests (12 queries)
- [ ] Check 6: Tier 3 scenario tests (10 queries)
- [ ] Clear pass/fail reporting
- [ ] Summary with total pass rate

**Status**: ⬜ | **Report**: `prompts/06_verification_script/06_6.1_verify_script_REPORT.md`

---

### Task 6.2: Run Verification
- [ ] Tier 1: 8/8 pass (category retrieval)
- [ ] Tier 2: 10+/12 pass (document retrieval)
- [ ] Tier 3: Relevant content retrieved (10 scenarios)
- [ ] Overall: 28+/30 tests pass

**Validation Commands**:
```bash
docker-compose --profile verify run --rm verify
```

**Status**: ⬜ | **Report**: `prompts/06_verification_script/06_6.2_run_verification_REPORT.md`

---

## Task Group 7: Documentation
**Duration**: 45 minutes | **Prompt Folder**: `prompts/07_documentation/`

### Task 7.1: Create README.md
- [ ] File created at `README.md`
- [ ] Overview section
- [ ] Prerequisites section (Docker OR Python 3.11+)
- [ ] Quick Start (Docker) section
- [ ] Local Development Setup section
- [ ] Usage section with CLI examples
- [ ] Configuration section (env vars)
- [ ] Docker Commands Reference
- [ ] Verification section
- [ ] Troubleshooting section
- [ ] Architecture diagram

**Status**: ⬜ | **Report**: `prompts/07_documentation/07_7.1_readme_REPORT.md`

---

## Task Group 8: CI/CD Preparation (Optional)
**Duration**: 30 minutes | **Prompt Folder**: `prompts/08_cicd_preparation/`

### Task 8.1: Create GitHub Actions Workflow
- [ ] File created at `.github/workflows/ingestion.yml`
- [ ] Triggers on KB changes
- [ ] Triggers on pipeline changes
- [ ] Builds Docker image
- [ ] Runs ingestion
- [ ] Runs verification
- [ ] Uploads ChromaDB artifact

**Status**: ⬜ | **Report**: `prompts/08_cicd_preparation/08_8.1_github_actions_REPORT.md`

---

## Final Validation Checklist

### Core Functionality
- [ ] All 29 documents ingested
- [ ] ~350-400 chunks in ChromaDB
- [ ] All 12 metadata fields populated
- [ ] Source URLs preserved

### Docker
- [ ] Image builds without errors
- [ ] Container runs ingestion successfully
- [ ] ChromaDB persists after container stops
- [ ] Verification runs in container
- [ ] Volume mounts work correctly

### Quality Gates
- [ ] Tier 1 tests: 8/8 pass
- [ ] Tier 2 tests: 10+/12 pass
- [ ] Tier 3 tests: Relevant content
- [ ] Documentation complete

### Single Command Test
- [ ] `docker-compose up --build` runs full pipeline

---

## Quick Reference

### Commands
| Action | Command |
|--------|---------|
| Build | `docker-compose build` |
| Run ingestion | `docker-compose run --rm ingestion` |
| Run verbose | `docker-compose run --rm ingestion --verbose` |
| Dry run | `docker-compose run --rm ingestion --dry-run` |
| Verify | `docker-compose --profile verify run --rm verify` |
| Stop | `docker-compose down` |

### Key Decisions
| Setting | Value |
|---------|-------|
| Embedding model | `gemini-embedding-001` (768-d) |
| Chunk size | 600 chars |
| Chunk overlap | 90 chars (15%) |
| Metadata fields | 12 |
| Base image | `python:3.11-slim` |
