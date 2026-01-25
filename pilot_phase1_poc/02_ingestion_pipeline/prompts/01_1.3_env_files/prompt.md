# Task 1.3: Create Environment Files

## Persona

> You are a Python DevOps engineer with expertise in configuration management and twelve-factor app principles.
> You follow best practices for separating configuration from code and prioritize environment portability.

---

## Context

### Project Background
Waypoint ingestion pipeline needs environment-specific configuration for paths, model selection, and runtime settings. Configuration should work both in Docker containers and local development.

### Current State
- `scripts/` directory exists with `__init__.py`
- `requirements.txt` created with dependencies
- No environment configuration files yet

### Reference Documents
- Pipeline Plan: `docs/00_ingestion_pipeline_plan.md`
- Component CLAUDE.md: `CLAUDE.md` (lists key config values)

### Dependencies
- Task 1.1 (Folder Structure) - ✅ Complete
- Task 1.2 (requirements.txt) - ✅ Complete

---

## Task

### Objective
Create `.env.example` (template for version control) and `.env` (actual config, gitignored) files with all required configuration variables for the ingestion pipeline.

### Requirements
1. Create `.env.example` with documented variables and default values
2. Create `.env` as a copy of `.env.example` (for immediate use)
3. Add `.env` to `.gitignore` to prevent committing secrets
4. Support both Docker and local execution paths

### Specifications

**Required Environment Variables**:
| Variable | Default Value | Description |
|----------|---------------|-------------|
| GOOGLE_API_KEY | `your-api-key-here` | Google Gemini API key (required) |
| EMBEDDING_MODEL | `gemini-embedding-001` | Gemini embedding model |
| EMBEDDING_DIMENSIONS | `768` | Embedding vector dimensions |
| CHROMA_PERSIST_PATH | `./chroma_db` | ChromaDB storage directory |
| COLLECTION_NAME | `waypoint_kb` | ChromaDB collection name |
| KNOWLEDGE_BASE_PATH | `../01_knowledge_base` | Path to source documents |
| LOG_LEVEL | `INFO` | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |

**Path Handling**:
- Paths should be relative to the `02_ingestion_pipeline/` directory
- Docker will override paths via docker-compose.yml environment section
- Local development uses these defaults directly

**File Locations**:
```
02_ingestion_pipeline/
├── .env.example    # Template (committed to git)
├── .env            # Actual config (gitignored)
└── .gitignore      # Must include .env
```

### Constraints
- `.env.example` must NOT contain real secrets (none needed for this project)
- Use comments to document each variable
- Keep values simple - no quotes needed for simple strings in dotenv

### Acceptance Criteria
- [ ] `.env.example` created with all 7 variables
- [ ] `.env` created (copy of example)
- [ ] GOOGLE_API_KEY defined
- [ ] EMBEDDING_MODEL defined (`gemini-embedding-001`)
- [ ] EMBEDDING_DIMENSIONS defined (`768`)
- [ ] CHROMA_PERSIST_PATH defined
- [ ] COLLECTION_NAME defined
- [ ] KNOWLEDGE_BASE_PATH defined
- [ ] LOG_LEVEL defined
- [ ] `.gitignore` includes `.env`

---

## Format

### Output Structure
```
02_ingestion_pipeline/
├── .env.example
├── .env
└── .gitignore
```

### File Format (.env.example)
```bash
# Waypoint Ingestion Pipeline Configuration
# Copy this file to .env and adjust values as needed

# Variable description
VARIABLE_NAME=default_value
```

### Documentation
- Each variable should have a comment explaining its purpose
- Group related variables together

### Validation
```bash
# Verify files exist
ls -la pilot_phase1_poc/02_ingestion_pipeline/.env*
cat pilot_phase1_poc/02_ingestion_pipeline/.gitignore

# Verify .env can be loaded
cd pilot_phase1_poc/02_ingestion_pipeline
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('COLLECTION_NAME'))"
```
