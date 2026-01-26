# Task 2.1: Create Configuration Module

## Persona

> You are a Python developer with expertise in configuration management and twelve-factor app principles.
> You follow best practices for separating configuration from code and use Path objects for file system operations.

---

## Context

### Project Background
The Waypoint ingestion pipeline requires centralized configuration for paths, embedding settings, and chunking parameters. The configuration module loads environment variables from `.env` and provides typed constants for use throughout the pipeline.

### Current State
- Environment setup complete (Tasks 1.1-1.4)
- `.env` file configured with ChromaDB default embeddings
- `scripts/` directory exists with `__init__.py`
- No configuration module yet

### Reference Documents
- Pipeline Plan: `docs/00_ingestion_pipeline_plan.md`
- Implementation Roadmap: `docs/01_implementation_roadmap.md`
- Environment Files: `.env`, `.env.example`

### Dependencies
- Task 1.3 (Environment Files) - ✅ Complete
- Task 1.4 (Local venv) - ✅ Complete

---

## Task

### Objective
Create a centralized configuration module (`scripts/config.py`) that loads settings from `.env` and provides typed constants for the ingestion pipeline.

### Requirements
1. Load environment variables from `.env` using python-dotenv
2. Provide Path objects for file system paths
3. Define chunking parameters as constants
4. Auto-create directories if they don't exist
5. Work correctly when imported from any script location

### Specifications

**Configuration Constants**:
| Constant | Type | Source | Default |
|----------|------|--------|---------|
| CHROMA_PERSIST_PATH | Path | `.env` | `./chroma_db` |
| KNOWLEDGE_BASE_PATH | Path | `.env` | `../01_knowledge_base` |
| LOG_DIR | Path | Hardcoded | `./logs` |
| EMBEDDING_MODEL | str | `.env` | `default` |
| EMBEDDING_DIMENSIONS | int | `.env` | `384` |
| CHUNK_SIZE | int | Hardcoded | `600` |
| CHUNK_OVERLAP | int | Hardcoded | `90` |
| SEPARATORS | list | Hardcoded | `["\n## ", "\n### ", "\n\n", "\n"]` |
| COLLECTION_NAME | str | `.env` | `waypoint_kb` |
| LOG_LEVEL | str | `.env` | `INFO` |

**Path Resolution**:
- Paths must be resolved relative to the `02_ingestion_pipeline/` directory
- Use `Path(__file__).parent.parent` to get the pipeline root
- Convert to absolute paths for reliability

**Directory Auto-Creation**:
- Create `CHROMA_PERSIST_PATH` if it doesn't exist
- Create `LOG_DIR` if it doesn't exist
- Do NOT create `KNOWLEDGE_BASE_PATH` (should already exist)

### Constraints
- Must use `pathlib.Path` for all file paths
- Must load `.env` from the correct location regardless of CWD
- Must not fail if optional env vars are missing (use defaults)

### Acceptance Criteria
- [ ] File created at `scripts/config.py`
- [ ] Loads from `.env` with dotenv
- [ ] CHROMA_PERSIST_PATH (Path object)
- [ ] KNOWLEDGE_BASE_PATH (Path object)
- [ ] LOG_DIR (Path object)
- [ ] EMBEDDING_MODEL = "default"
- [ ] EMBEDDING_DIMENSIONS = 384
- [ ] CHUNK_SIZE = 600
- [ ] CHUNK_OVERLAP = 90
- [ ] SEPARATORS list defined
- [ ] COLLECTION_NAME defined
- [ ] Directories auto-created if missing
- [ ] Works when run from any directory

---

## Format

### Output Structure
```
02_ingestion_pipeline/
├── scripts/
│   ├── __init__.py
│   └── config.py     # NEW
└── (other files)
```

### Code Style
- Use type hints
- Include module docstring
- Group related constants with comments
- Use UPPER_CASE for constants

### Validation Commands
```bash
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase1_poc\02_ingestion_pipeline
python -c "from scripts.config import *; print(f'KNOWLEDGE_BASE_PATH: {KNOWLEDGE_BASE_PATH}')"
python -c "from scripts.config import *; print(f'CHROMA_PERSIST_PATH: {CHROMA_PERSIST_PATH}')"
python -c "from scripts.config import *; print(f'EMBEDDING_MODEL: {EMBEDDING_MODEL}')"
python -c "from scripts.config import *; print(f'CHUNK_SIZE: {CHUNK_SIZE}')"
```

### Expected Output
```
KNOWLEDGE_BASE_PATH: C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase1_poc\01_knowledge_base
CHROMA_PERSIST_PATH: C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase1_poc\02_ingestion_pipeline\chroma_db
EMBEDDING_MODEL: default
CHUNK_SIZE: 600
```
