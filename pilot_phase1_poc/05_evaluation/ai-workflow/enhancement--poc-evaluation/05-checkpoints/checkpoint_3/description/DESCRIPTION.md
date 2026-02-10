# Checkpoint 3: Round 2 Metrics Finalized

**After Task:** 3.3
**Feature:** All evaluation targets met after fix-and-retest loop
**Precondition for:** Phase 4 (Documentation) and Phase 5 (Demo)

---

## Overview

Validates that the complete system (ingestion → retrieval → generation → response) meets all quality targets after systematic testing and iterative fixes. The 50-query automated evaluation harness has been run, failures analyzed and fixed, and final metrics calculated. All hard gates must be met before proceeding to documentation and demo.

---

## Requirements Reference

- Decision #4: Fully automated testing — no LLM-as-judge, no manual scoring
- Decision #5: Expected-answer baselines for all 50 queries
- Decision #6: Fix-and-retest loop (same as Week 3 Task 8 pattern)
- Decision #20: JSON + Markdown report + CSV output

---

## Tasks Included (Phase 2 + Phase 3)

| Task | Title | Status |
|------|-------|--------|
| 2.1 | Re-run existing ingestion tests | ⬜ |
| 2.2 | Add new metadata preservation tests | ⬜ |
| 2.3 | Re-run 50-query retrieval hit rate test | ⬜ |
| 2.4 | Add generation unit tests | ⬜ |
| 2.5 | Update citation service tests | ⬜ |
| 2.6 | Update existing backend tests | ⬜ |
| 2.7 | Add new endpoint tests | ⬜ |
| 2.8 | Add error/edge case tests | ⬜ |
| 2.9 | Component unit tests | ⬜ |
| 2.10 | Visual verification | ⬜ |
| 2.11 | Define expected-answer baselines | ⬜ |
| 2.12 | Build automated evaluation harness | ⬜ |
| 2.13 | Execute Round 2 and generate reports | ⬜ |
| 3.1 | Failure analysis | ⬜ |
| 3.2 | Apply fixes | ⬜ |
| 3.3 | Re-run evaluation | ⬜ |

---

## Acceptance Criteria

### Target Metrics (ALL are hard gates)

| Metric | Target | Status |
|--------|--------|--------|
| Deflection Rate | ≥ 40% | ⬜ |
| Citation Accuracy | ≥ 80% | ⬜ |
| Hallucination Rate | < 15% | ⬜ |
| OOS Handling | ≥ 90% | ⬜ |
| Avg Latency | < 5s | ⬜ |
| System Stability | No crashes | ⬜ |

### Test Suite Health
1. All Python tests pass (ingestion + retrieval + metadata)
2. All Jest tests pass (backend + citations + pipeline)
3. All Vitest tests pass (frontend components)
4. 50-query evaluation harness completes without errors

### Evaluation Artifacts
1. `data/evaluation_results.json` — raw results for programmatic use
2. `reports/evaluation_report.md` — human-readable with metrics, per-category breakdown, failure analysis
3. `data/evaluation_results.csv` — one row per query with all scoring columns

---

## Validation Checklist

- [ ] All 50 expected-answer baselines defined in `data/evaluation_baselines.json`
- [ ] Evaluation harness executes all 50 queries successfully
- [ ] 30-second delay between requests (Groq rate limit)
- [ ] 429 responses handled with exponential backoff
- [ ] Deflection rate ≥ 40%
- [ ] Citation accuracy ≥ 80%
- [ ] Hallucination rate < 15%
- [ ] OOS handling ≥ 90%
- [ ] Average latency < 5s
- [ ] No system crashes during evaluation
- [ ] evaluation_results.json generated
- [ ] evaluation_report.md generated
- [ ] evaluation_results.csv generated
- [ ] All unit tests pass (pytest + Jest + Vitest)
- [ ] Fix loop documented (what was changed and why)

---

## Demo Script

    # Step 1: Run evaluation harness
    cd pilot_phase1_poc/05_evaluation
    venv/Scripts/activate
    python scripts/evaluation_test.py

    # Step 2: Check results
    cat data/evaluation_results.json | python -m json.tool | head -50
    cat reports/evaluation_report.md

    # Step 3: Run all tests
    python -m pytest tests/ -v
    npm test
    cd client && npm test

---

## Success Criteria

Checkpoint complete when:
1. All 6 target metrics met (hard gates — no exceptions)
2. Evaluation artifacts generated (JSON, Markdown report, CSV)
3. All test suites pass
4. Fix loop documented
5. Rishi reviews metrics and approves

If targets cannot be met: escalate to Rishi for scope/approach discussion before proceeding.

---

## Next Steps

After this checkpoint, proceed to:
- Phase 4: Documentation (Task 4.1 — Codebase documentation)
- Phase 5: Demo (Task 5.1 — Select demo queries)

(Phase 4 and Phase 5 can proceed in parallel after CP3.)
