# Task 1.1: Create Folder Structure

## Persona

> You are a Python DevOps engineer with expertise in project scaffolding and Docker-based development workflows.
> You follow Python packaging conventions and prioritize clean, maintainable project structures.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot for freight forwarding companies. The ingestion pipeline component will transform 29 curated knowledge base documents into a searchable ChromaDB vector store.

### Current State
The `02_ingestion_pipeline/` directory exists with:
- `docs/` - Planning documents
- `prompts/` - PCTF task prompts
- `CLAUDE.md` - Component instructions

Missing: Core pipeline directories (`scripts/`, `tests/`, `logs/`)

### Reference Documents
- Pipeline Plan: `docs/00_ingestion_pipeline_plan.md`
- Implementation Roadmap: `docs/01_implementation_roadmap.md`

### Dependencies
None - this is the first task.

---

## Task

### Objective
Create the foundational folder structure for the ingestion pipeline, establishing the directories needed for Python scripts, tests, and runtime logs.

### Requirements
1. Create `scripts/` directory for Python modules
2. Create `scripts/__init__.py` to make it a Python package
3. Create `tests/` directory for unit tests
4. Create `logs/` directory for runtime logs
5. Add `.gitkeep` files to empty directories so they're tracked in git

### Specifications

**Target Structure**:
```
02_ingestion_pipeline/
├── scripts/
│   └── __init__.py
├── tests/
│   └── .gitkeep
├── logs/
│   └── .gitkeep
├── chroma_db/              (auto-created at runtime, do NOT create)
├── docs/                   (exists)
├── prompts/                (exists)
└── CLAUDE.md               (exists)
```

**`__init__.py` Content**:
```python
"""Waypoint Ingestion Pipeline - Document processing and ChromaDB storage."""
```

### Constraints
- Do NOT create `chroma_db/` - it will be auto-created by ChromaDB at runtime
- Do NOT modify existing directories (`docs/`, `prompts/`)
- Use Unix-style line endings (LF) for all files

### Acceptance Criteria
- [ ] `scripts/` directory exists
- [ ] `scripts/__init__.py` exists with docstring
- [ ] `tests/` directory exists
- [ ] `tests/.gitkeep` exists
- [ ] `logs/` directory exists
- [ ] `logs/.gitkeep` exists

---

## Format

### Output Structure
```
02_ingestion_pipeline/
├── scripts/
│   └── __init__.py
├── tests/
│   └── .gitkeep
└── logs/
    └── .gitkeep
```

### Code Style
- Python files: PEP 8 compliant
- Module docstrings: Triple-quoted strings

### Documentation
- `__init__.py` should have a one-line module docstring

### Validation
```bash
# Verify directories exist
ls -la pilot_phase1_poc/02_ingestion_pipeline/scripts/
ls -la pilot_phase1_poc/02_ingestion_pipeline/tests/
ls -la pilot_phase1_poc/02_ingestion_pipeline/logs/

# Verify __init__.py content
cat pilot_phase1_poc/02_ingestion_pipeline/scripts/__init__.py

# Verify Python package is importable (from pipeline directory)
cd pilot_phase1_poc/02_ingestion_pipeline
python -c "import scripts; print('Package OK')"
```
