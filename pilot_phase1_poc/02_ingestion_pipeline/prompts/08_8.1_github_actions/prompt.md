# Task 8.1: Create GitHub Actions Workflow

## Persona

> You are a DevOps engineer with expertise in GitHub Actions, CI/CD pipelines, and Python automation.
> You follow infrastructure-as-code best practices and prioritize reproducibility, caching, and clear job outputs.

---

## Context

### Project Background

Waypoint is a RAG-based customer service co-pilot. The ingestion pipeline processes 29 knowledge base documents into ChromaDB for semantic retrieval. The pipeline is complete and verified locally.

### Current State

**Completed components:**
- `scripts/config.py` - Configuration module
- `scripts/process_docs.py` - Document discovery and parsing
- `scripts/chunker.py` - Text chunking with metadata
- `scripts/ingest.py` - Main ingestion orchestrator
- `scripts/verify_ingestion.py` - Quality verification (33 tests)
- `tests/` - 140+ pytest tests
- `requirements.txt` - Python dependencies
- `README.md` - Documentation

**Pipeline outputs:**
- 483 chunks in ChromaDB
- 4 categories, 10 metadata fields per chunk
- 33/33 verification tests passing

### Reference Documents

| Document | Path |
|----------|------|
| Implementation Roadmap | `docs/01_implementation_roadmap.md` |
| README | `README.md` |
| Requirements | `requirements.txt` |

### Dependencies

- All previous tasks (1-7) complete
- GitHub repository exists at `waypoint-pilot/`
- Knowledge base at `pilot_phase1_poc/01_knowledge_base/kb/`

---

## Task

### Objective

Create a GitHub Actions workflow that automatically runs the ingestion pipeline and verification when knowledge base documents or pipeline code changes.

### Requirements

1. **Workflow file** at `.github/workflows/ingestion.yml`
2. **Trigger on push/PR** to paths:
   - `pilot_phase1_poc/01_knowledge_base/kb/**`
   - `pilot_phase1_poc/02_ingestion_pipeline/**`
3. **Python 3.11** environment setup
4. **Dependency caching** for faster runs
5. **Run ingestion** with `--clear` flag
6. **Run verification** and fail if not 93%+
7. **Upload ChromaDB** as artifact for downstream use
8. **Job summary** with verification results

### Specifications

**Workflow structure:**
```yaml
name: Ingestion Pipeline
on:
  push:
    paths:
      - 'pilot_phase1_poc/01_knowledge_base/kb/**'
      - 'pilot_phase1_poc/02_ingestion_pipeline/**'
  pull_request:
    paths:
      - 'pilot_phase1_poc/01_knowledge_base/kb/**'
      - 'pilot_phase1_poc/02_ingestion_pipeline/**'
  workflow_dispatch:  # Manual trigger

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      # ... implementation
```

**Required steps:**
1. Checkout repository
2. Setup Python 3.11
3. Cache pip dependencies
4. Install dependencies
5. Run pytest (unit tests)
6. Run ingestion (`python -m scripts.ingest --clear`)
7. Run verification (`python -m scripts.verify_ingestion`)
8. Upload chroma_db/ as artifact
9. Add job summary with results

### Constraints

- Use `ubuntu-latest` runner
- Python version must be 3.11 (not 3.14)
- Working directory: `pilot_phase1_poc/02_ingestion_pipeline`
- No secrets required (no external APIs)
- Artifact retention: 7 days
- Fail fast on test/verification failure

### Acceptance Criteria

- [ ] Workflow file created at correct path
- [ ] Triggers on KB and pipeline changes
- [ ] Manual trigger (`workflow_dispatch`) enabled
- [ ] Python 3.11 with pip caching
- [ ] Unit tests run before ingestion
- [ ] Ingestion runs with `--clear`
- [ ] Verification runs and checks pass rate
- [ ] ChromaDB artifact uploaded
- [ ] Job summary shows verification results
- [ ] Workflow passes on current main branch

---

## Format

### Output Structure

```
.github/
└── workflows/
    └── ingestion.yml    # GitHub Actions workflow
```

### Workflow Style

- Use `actions/checkout@v4`
- Use `actions/setup-python@v5`
- Use `actions/cache@v4` for pip
- Use `actions/upload-artifact@v4`
- Clear step names with emojis for visibility
- Proper working-directory for all run steps

### Job Summary Format

```markdown
## Ingestion Pipeline Results

### Verification
- Check 1: Total count - PASS (483 chunks)
- Check 2: Categories - PASS (4/4)
- ...

### Summary
- Tests passed: 33/33
- Result: VERIFICATION PASSED
```

### Validation

```bash
# Validate workflow syntax locally (optional)
# Requires act: https://github.com/nektos/act
act -n

# Or push to branch and check Actions tab
git add .github/workflows/ingestion.yml
git commit -m "Add ingestion pipeline workflow"
git push
```

---

## Implementation Notes

### Pip Caching

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Working Directory

```yaml
- name: Run ingestion
  working-directory: pilot_phase1_poc/02_ingestion_pipeline
  run: python -m scripts.ingest --clear
```

### Job Summary

```yaml
- name: Add job summary
  run: |
    echo "## Ingestion Results" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY
    cat verification_output.txt >> $GITHUB_STEP_SUMMARY
```

### Artifact Upload

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: chroma-db
    path: pilot_phase1_poc/02_ingestion_pipeline/chroma_db/
    retention-days: 7
```
