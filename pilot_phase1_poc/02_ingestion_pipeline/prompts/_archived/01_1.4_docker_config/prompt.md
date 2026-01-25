# Task 1.4: Create Docker Configuration

## Persona

> You are a DevOps engineer with expertise in Docker containerization and Python application deployment.
> You follow best practices for image optimization, layer caching, and reproducible builds.

---

## Context

### Project Background
Waypoint ingestion pipeline needs Docker containerization for reproducible execution across development, CI/CD, and production environments. The container must pre-cache the embedding model to avoid download delays at runtime.

### Current State
- `scripts/` directory with `__init__.py`
- `requirements.txt` with all dependencies
- `.env` and `.env.example` configuration files
- `.gitignore` for excluding generated files

### Reference Documents
- Pipeline Plan: `docs/00_ingestion_pipeline_plan.md` (Docker Architecture section)
- Implementation Roadmap: `docs/01_implementation_roadmap.md`

### Dependencies
- Task 1.1 (Folder Structure) - ✅ Complete
- Task 1.2 (requirements.txt) - ✅ Complete
- Task 1.3 (Environment Files) - ✅ Complete

---

## Task

### Objective
Create Docker configuration files (`Dockerfile`, `docker-compose.yml`, `.dockerignore`) that containerize the ingestion pipeline with pre-cached embedding model and proper volume mounts.

### Requirements
1. Create `Dockerfile` with multi-stage build
2. Pre-download BGE-small embedding model during build
3. Create `docker-compose.yml` with volume mounts and profiles
4. Create `.dockerignore` to exclude unnecessary files
5. Support both ingestion and verification services

### Specifications

**Dockerfile Requirements**:
- Base image: `python:3.11-slim`
- Single-stage build with model pre-caching
- Install build-essential for sentence-transformers
- Install dependencies from `requirements.txt`
- Pre-cache `all-MiniLM-L6-v2` model during build
- Working directory: `/app`
- Entrypoint: `python scripts/ingest.py`
- Target image size: ~800MB-1.2GB

**docker-compose.yml Requirements**:
- Service: `ingestion` (main pipeline)
- Service: `verify` (verification script, profile: verify)
- Volume mounts:
  - `../01_knowledge_base` → `/app/knowledge_base` (read-only)
  - `./chroma_db` → `/app/chroma_db` (read-write)
  - `./logs` → `/app/logs` (read-write)
- Environment variables from `.env`
- Override paths for container context

**Volume Mount Diagram**:
```
Host                              Container
─────────────────────────────────────────────────
../01_knowledge_base (RO)    →    /app/knowledge_base
./chroma_db (RW)             →    /app/chroma_db
./logs (RW)                  →    /app/logs
```

**Container Environment Overrides**:
| Variable | Container Value |
|----------|-----------------|
| EMBEDDING_MODEL | `all-MiniLM-L6-v2` |
| EMBEDDING_DIMENSIONS | `384` |
| KNOWLEDGE_BASE_PATH | `/app/knowledge_base` |
| CHROMA_PERSIST_PATH | `/app/chroma_db` |
| LOG_DIR | `/app/logs` |

**.dockerignore Contents**:
- `chroma_db/`
- `logs/`
- `venv/`
- `__pycache__/`
- `.git/`
- `*.md` (except README)
- `.env` (use docker-compose env instead)

### Constraints
- Image must work on both Windows (Docker Desktop) and Linux
- Do not hardcode absolute paths in Dockerfile
- Use named volumes or bind mounts consistently
- No API key required (local embeddings)

### Acceptance Criteria
- [ ] `Dockerfile` created
- [ ] Single-stage build with model pre-caching
- [ ] `docker-compose.yml` created
- [ ] Volume mounts configured (knowledge_base, chroma_db, logs)
- [ ] Environment variables configured
- [ ] Verify profile configured
- [ ] `.dockerignore` created

---

## Format

### Output Structure
```
02_ingestion_pipeline/
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

### Dockerfile Template
```dockerfile
# Single-stage build with local sentence-transformers model
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Pre-cache embedding model during build
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
COPY scripts/ ./scripts/
# ... set environment and entrypoint
```

### docker-compose.yml Template
```yaml
version: '3.8'
services:
  ingestion:
    build: .
    volumes:
      - ...
    environment:
      - ...
  verify:
    profiles: ["verify"]
    # ...
```

### Documentation
- Add comments explaining key decisions
- Document the model caching step

### Validation
```bash
# Build image
cd pilot_phase1_poc/02_ingestion_pipeline
docker-compose build

# Check image size (should be ~800MB-1.2GB)
docker images | grep waypoint

# Test container can import dependencies
docker-compose run --rm --entrypoint python ingestion -c "import chromadb; print('chromadb OK')"
docker-compose run --rm --entrypoint python ingestion -c "from sentence_transformers import SentenceTransformer; print('sentence-transformers OK')"

# Verify local embeddings work
docker-compose run --rm --entrypoint python ingestion -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(['test'])
print(f'OK - {embeddings.shape[1]} dimensions')
"
```
