# Task 1.5: Verify Docker Setup

## Persona

> You are a DevOps engineer validating Docker container builds and runtime behavior.
> You verify that containers meet size, performance, and functionality requirements.

---

## Context

### Project Background
Docker configuration has been created for the Waypoint ingestion pipeline. This task validates that the Docker image builds correctly, meets size requirements, and can run the pipeline.

### Current State
- `Dockerfile` created with model pre-caching
- `docker-compose.yml` configured with services and volumes
- `.dockerignore` excludes unnecessary files
- No build attempted yet

### Reference Documents
- Task 1.4 Report: `prompts/01_1.4_docker_config/REPORT.md`

### Dependencies
- Task 1.4 (Docker Configuration) - ✅ Complete

---

## Task

### Objective
Build the Docker image and verify it meets all requirements: successful build, appropriate size, and ability to import required Python packages and generate embeddings.

### Requirements
1. Run `docker-compose build` successfully
2. Verify image size is ~800MB-1.2GB
3. Verify container can import chromadb
4. Verify container can import sentence-transformers
5. Verify local model returns 384-dimension embeddings

### Specifications

**Build Command**:
```bash
cd pilot_phase1_poc/02_ingestion_pipeline
docker-compose build
```

**Size Requirement**: ~800MB-1.2GB (model pre-cached in image)

**Import Tests**:
```bash
docker-compose run --rm --entrypoint python ingestion -c "import chromadb; print('chromadb OK')"
docker-compose run --rm --entrypoint python ingestion -c "from sentence_transformers import SentenceTransformer; print('sentence-transformers OK')"
```

**Local Embeddings Test**:
```bash
docker-compose run --rm --entrypoint python ingestion -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(['test'])
print(f'OK - {embeddings.shape[1]} dimensions')
"
```

### Constraints
- Build must complete without errors
- No API key required (local embeddings)

### Acceptance Criteria
- [ ] `docker-compose build` succeeds
- [ ] Image size ~800MB-1.2GB
- [ ] Container can import chromadb
- [ ] Container can import sentence-transformers
- [ ] Local model returns 384-dimension embeddings

---

## Format

### Validation Commands
```bash
docker-compose build
docker images | grep waypoint
docker-compose run --rm --entrypoint python ingestion -c "import chromadb; print('OK')"
docker-compose run --rm --entrypoint python ingestion -c "from sentence_transformers import SentenceTransformer; print('OK')"
```

### Expected Output
- Build: "Successfully built" or "Successfully tagged"
- Image size: Shown in MB/GB
- Import tests: "OK" printed without errors
