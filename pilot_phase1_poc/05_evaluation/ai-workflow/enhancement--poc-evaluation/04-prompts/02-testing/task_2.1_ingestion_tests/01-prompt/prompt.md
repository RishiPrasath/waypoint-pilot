# Task 2.1: Re-run Existing Ingestion Tests

**Phase:** Phase 2 — Systematic Testing
**Initiative:** enhancement--poc-evaluation

---

## Persona

You are a **QA Engineer** with expertise in:
- Python test execution and troubleshooting (pytest)
- ChromaDB vector database verification
- RAG pipeline ingestion validation
- Windows Python environment management

You validate baseline test integrity before adding new tests, ensuring no regressions from prior phases.

---

## Context

### Initiative
Waypoint Phase 1 POC — Week 4 Evaluation & Documentation. Phase 1 (UX Redesign) is complete. Phase 2 begins with validating that all existing ingestion tests still pass. This is a **read-only validation task** — no code changes expected unless tests fail.

### Reference Documents
- Master rules: `./CLAUDE.md`
- Week 4 plan: `./pilot_phase1_poc/05_evaluation/week4_plan.md`
- CP2 Review: `./ai-workflow/enhancement--poc-evaluation/05-checkpoints/checkpoint_2/review/CHECKPOINT_2_REVIEW.md`
- Roadmap Task 2.1: `./ai-workflow/enhancement--poc-evaluation/02-roadmap/IMPLEMENTATION_ROADMAP.md` (search "Task 2.1")

### Working Directory
`./pilot_phase1_poc/05_evaluation/`

### Current State
- CP2 PASSED — UX Redesign complete (4/4 tasks, 119/119 Jest tests, frontend build clean)
- Fresh ingestion was run in T0.5 with `--clear` flag
- T0.6 confirmed all tests passed at workspace setup time (29 pytest + 33 verify + 50 retrieval)
- Phase 1 made **no changes** to Python scripts or ingestion pipeline — only backend JS and React components
- ChromaDB has ~709 chunks from 30 documents

### Dependencies
- **Requires**: CP2 (PASSED)
- **Blocks**: T2.2 (new metadata tests), T2.3 (retrieval hit rate re-run)

---

## Task

### Objective
Re-run all existing Python ingestion tests to confirm baseline integrity before adding new tests in T2.2+. This validates that no regressions were introduced during Phase 0 or Phase 1.

### Requirements

Run these three test suites in order:

#### 1. Python Unit Tests (pytest)
```bash
cd pilot_phase1_poc/05_evaluation
venv/Scripts/python -m pytest tests/test_pdf_extractor.py -v
```
- **Expected**: 29 tests pass (all in `test_pdf_extractor.py`)
- Tests cover: `clean_extracted_content`, `generate_frontmatter`, `assess_quality`, `extract_pdf_to_markdown`, `write_markdown_file`, `process_single`, `process_batch`

#### 2. Ingestion Verification Script
```bash
cd pilot_phase1_poc/05_evaluation
venv/Scripts/python scripts/verify_ingestion.py
```
- **Expected**: 33/33 checks pass across 6 tiers:
  1. Total chunk count (680-740 range)
  2. Category distribution (4/4 categories)
  3. Metadata integrity (10 required fields)
  4. Tier 1 retrieval — 8 category queries
  5. Tier 2 retrieval — 10+/12 document queries
  6. Tier 3 retrieval — 8+/10 keyword queries

#### 3. Retrieval Quality Test (50 queries)
```bash
cd pilot_phase1_poc/05_evaluation
venv/Scripts/python scripts/retrieval_quality_test.py
```
- **Expected**: 46/50 pass (92% hit rate)
  - 4 known failures: Q#1 (borderline), Q#36, Q#38, Q#41 (out-of-scope)
- Generates: `data/retrieval_test_results.json`

### Constraints
- **Read-only validation** — do NOT modify test scripts, ingestion scripts, or knowledge base files
- If tests fail, **document** the failures but do NOT fix them in this task. Fixes are for T3.x (Fix Loop)
- Exception: If a failure is clearly caused by an environment issue (wrong venv, missing dependency), fix the environment only

---

## Format

### Output Report
Create `TASK_2.1_OUTPUT.md` in the `02-output/` folder with:

```markdown
# Task 2.1 Output — Re-run Existing Ingestion Tests

**Task:** 2.1 — Re-run existing ingestion tests
**Phase:** Phase 2 — Systematic Testing
**Status:** [PASS/FAIL]
**Date:** [Date]

---

## Summary

[1-2 sentence overview of results]

---

## Test Results

### 1. Python Unit Tests (pytest)

| Metric | Value |
|--------|-------|
| Total Tests | [N] |
| Passed | [N] |
| Failed | [N] |
| Errors | [N] |

[If failures, list each with test name and error message]

### 2. Ingestion Verification (verify_ingestion.py)

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Chunk count | 680-740 | [N] | [PASS/FAIL] |
| Categories | 4/4 | [N/4] | [PASS/FAIL] |
| Metadata fields | 10/10 | [N/10] | [PASS/FAIL] |
| Tier 1 | 8/8 | [N/8] | [PASS/FAIL] |
| Tier 2 | 10+/12 | [N/12] | [PASS/FAIL] |
| Tier 3 | 8+/10 | [N/10] | [PASS/FAIL] |

### 3. Retrieval Quality Test (50 queries)

| Metric | Value |
|--------|-------|
| Total Queries | 50 |
| Passed | [N] |
| Failed | [N] |
| Hit Rate | [N]% |
| Known Failures | Q#1, Q#36, Q#38, Q#41 |
| New Failures | [list or "None"] |

---

## Regression Analysis

[Compare results to CP1/T0.6 baselines. Flag any new failures.]

---

## Issues

[List any issues encountered, or "None"]

---

## Validation

| Criterion | Status |
|-----------|--------|
| All Python tests pass (29+) | [PASS/FAIL] |
| verify_ingestion.py passes all 33 checks | [PASS/FAIL] |
| No regressions from T0.4 metadata changes | [PASS/FAIL] |
| Retrieval hit rate >= 92% | [PASS/FAIL] |

---

## Next Steps

- Task 2.2: Add new metadata preservation tests
- Task 2.3: Re-run 50-query retrieval hit rate test (formal)
```

### Tracking Updates
After completion:
1. Update `IMPLEMENTATION_CHECKLIST.md` — mark Task 2.1 `[x]`
2. Update `IMPLEMENTATION_ROADMAP.md` — set Task 2.1 status to `✅ Complete`
3. Update progress totals (Phase 2: 1/13, Overall: 11/43, 26%)
