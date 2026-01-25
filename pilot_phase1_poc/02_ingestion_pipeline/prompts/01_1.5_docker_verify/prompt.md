# Task 1.5: Verify Docker Setup

## Persona

> You are a DevOps engineer validating Docker container builds and runtime behavior.
> You verify that containers meet size, performance, and functionality requirements.

---

## Context

### Project Background
Docker configuration has been created for the Waypoint ingestion pipeline. This task validates that the Docker image builds correctly, meets size requirements, and can run the pipeline.

### Current State
- `Dockerfile` created with multi-stage build
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
Build the Docker image and verify it meets all requirements: successful build, size under 1.5GB, and ability to import required Python packages.

### Requirements
1. Run `docker-compose build` successfully
2. Verify image size is under 800MB
3. Verify container can import chromadb
4. Verify container can import google-genai
5. Verify Gemini API returns 768-dimension embeddings

### Specifications

**Build Command**:
```bash
cd pilot_phase1_poc/02_ingestion_pipeline
docker-compose build
```

**Size Requirement**: < 800MB

**Import Tests**:
```bash
docker-compose run --rm --entrypoint python ingestion -c "import chromadb; print('chromadb OK')"
docker-compose run --rm --entrypoint python ingestion -c "from google import genai; print('google-genai OK')"
```

**Gemini API Test**:
```bash
docker-compose run --rm --entrypoint python ingestion -c "
from google import genai
client = genai.Client()
r = client.models.embed_content(model='gemini-embedding-001', contents='test')
print(f'Gemini OK - {len(r.embeddings[0].values)} dimensions')
"
```

### Constraints
- Build must complete without errors
- Gemini API must be reachable with valid GOOGLE_API_KEY

### Acceptance Criteria
- [ ] `docker-compose build` succeeds
- [ ] Image size < 800MB
- [ ] Container can import chromadb
- [ ] Container can import google-genai
- [ ] Gemini API returns 768-dimension embeddings

---

## Format

### Validation Commands
```bash
docker-compose build
docker images | grep waypoint
docker-compose run --rm --entrypoint python ingestion -c "import chromadb; print('OK')"
docker-compose run --rm --entrypoint python ingestion -c "from google import genai; print('OK')"
```

### Expected Output
- Build: "Successfully built" or "Successfully tagged"
- Image size: Shown in MB/GB
- Import tests: "OK" printed without errors
