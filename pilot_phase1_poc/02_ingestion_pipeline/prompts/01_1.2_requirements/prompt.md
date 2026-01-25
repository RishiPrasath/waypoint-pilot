# Task 1.2: Create requirements.txt

## Persona

> You are a Python DevOps engineer with expertise in dependency management and reproducible environments.
> You follow best practices for pinning versions and prioritize stability over bleeding-edge features.

---

## Context

### Project Background
Waypoint ingestion pipeline transforms 29 knowledge base documents into ChromaDB vectors. The pipeline requires specific Python packages for document parsing, text chunking, embedding generation, and vector storage.

### Current State
- `scripts/` directory exists with `__init__.py`
- `tests/` and `logs/` directories exist
- No `requirements.txt` yet

### Reference Documents
- Pipeline Plan: `docs/00_ingestion_pipeline_plan.md`
- Implementation Roadmap: `docs/01_implementation_roadmap.md`

### Dependencies
- Task 1.1 (Create Folder Structure) - ✅ Complete

---

## Task

### Objective
Create a `requirements.txt` file with pinned versions of all Python dependencies needed for the ingestion pipeline.

### Requirements
1. Pin all package versions for reproducibility
2. Include all packages needed for:
   - Vector database (ChromaDB)
   - Embedding generation (sentence-transformers)
   - Document parsing (python-frontmatter, pyyaml)
   - Text chunking (langchain-text-splitters)
   - Progress display (tqdm)
   - Configuration (python-dotenv)

### Specifications

**Required Packages**:
| Package | Version | Purpose |
|---------|---------|---------|
| chromadb | 0.4.22 | Vector database |
| sentence-transformers | 2.2.2 | Embedding model (BGE-small) |
| python-frontmatter | 1.1.0 | YAML frontmatter parsing |
| langchain-text-splitters | 0.0.1 | Document chunking |
| pyyaml | 6.0.1 | YAML parsing |
| tqdm | 4.66.1 | Progress bars |
| python-dotenv | 1.0.0 | Environment variable loading |

**File Location**: `02_ingestion_pipeline/requirements.txt`

### Constraints
- Use exact version pinning (`==`) not ranges
- Do not include dev/test dependencies (those go in a separate file if needed)
- Order packages alphabetically for readability

### Acceptance Criteria
- [ ] File created at `requirements.txt`
- [ ] chromadb==0.4.22
- [ ] sentence-transformers==2.2.2
- [ ] python-frontmatter==1.1.0
- [ ] langchain-text-splitters==0.0.1
- [ ] pyyaml==6.0.1
- [ ] tqdm==4.66.1
- [ ] python-dotenv==1.0.0

---

## Format

### Output Structure
```
02_ingestion_pipeline/
└── requirements.txt
```

### File Format
```txt
# Waypoint Ingestion Pipeline Dependencies
# Pin versions for reproducibility

package-name==X.Y.Z
```

### Documentation
- Include a header comment explaining the file's purpose
- Group related packages with blank lines if helpful

### Validation
```bash
# Verify file exists and contents
cat pilot_phase1_poc/02_ingestion_pipeline/requirements.txt

# Verify syntax is valid (dry-run install check)
cd pilot_phase1_poc/02_ingestion_pipeline
pip install --dry-run -r requirements.txt
```
