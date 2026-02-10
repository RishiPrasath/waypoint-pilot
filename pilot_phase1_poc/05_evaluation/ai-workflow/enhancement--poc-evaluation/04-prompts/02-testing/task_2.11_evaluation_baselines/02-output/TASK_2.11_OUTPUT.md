# Task 2.11 Output — Expected-Answer Baselines (50 Queries)

**Task:** 2.11 — Define expected-answer baselines (50 queries)
**Phase:** Phase 2 — Systematic Testing (Layer 5: Evaluation Baselines)
**Status:** PASS
**Date:** 2026-02-09

---

## Summary

Created `data/evaluation_baselines.json` with all 50 query baselines for the automated evaluation harness (Task 2.12). Each baseline defines `must_contain`, `should_contain`, `must_not_contain`, `expected_docs`, and `oos_decline_signals` for programmatic answer quality checks.

---

## File Created

- **`data/evaluation_baselines.json`** — 50 query baselines, JSON schema v1.0

---

## Statistics

| Metric | Value |
|--------|-------|
| Total queries | 50 |
| In-scope queries | 41 |
| Out-of-scope queries | 9 |
| Categories | booking (10), customs (10), carrier (10), sla (10), edge_case (10) |
| Total `must_contain` keywords | 83 |
| Total `should_contain` keywords | 183 |
| Total `must_not_contain` keywords | 125 |
| Avg `must_contain` per in-scope query | 2.0 |

---

## Category Breakdown

| Category | Queries | In-Scope | OOS | Avg must_contain |
|----------|---------|----------|-----|-----------------|
| booking | Q-01 to Q-10 | 10 | 0 | 2.0 |
| customs | Q-11 to Q-20 | 10 | 0 | 2.0 |
| carrier | Q-21 to Q-30 | 10 | 0 | 2.0 |
| sla | Q-31 to Q-40 | 10 | 0 | 2.0 |
| edge_case | Q-41 to Q-50 | 1 (Q-44) | 9 | N/A |

---

## Key Decisions

1. **Q-44 (cargo claims)** — Marked `is_oos: false` because `service_terms` document covers claims procedures. It's partially answerable from the KB.
2. **Case-insensitive substring matching** — All `must_contain` and `must_not_contain` keywords use lowercase for case-insensitive matching in the harness.
3. **Hallucination detectors** — In-scope queries check for false declines ("I don't have"). OOS queries check for hallucinated specifics (made-up rates, tracking numbers, recommendations).
4. **GST rate validation** — Q-11 includes `must_not_contain: ["7%", "8%", "10%"]` to catch outdated or wrong rates (correct is 9%).

---

## Validation

| Criterion | Status |
|-----------|--------|
| All 50 queries have baseline definitions | PASS |
| Every in-scope query has ≥2 `must_contain` keywords | PASS (83 total, avg 2.0) |
| Every query has ≥1 `must_not_contain` signal | PASS (125 total) |
| Every OOS query has ≥1 `oos_decline_signals` | PASS (9/9 OOS) |
| `expected_docs` matches EXPECTED_SOURCES from retrieval test | PASS |
| JSON is well-formed | PASS |

---

## Tracking Updates

- **Checklist**: `03-checklist/IMPLEMENTATION_CHECKLIST.md` — Task 2.11 marked `[x]`, Phase 2 + Total updated
- **Roadmap**: `02-roadmap/IMPLEMENTATION_ROADMAP.md` — Updated all 3 locations:
  1. Progress Tracker table (top)
  2. Quick Reference table
  3. Detailed task entry
- **Verified**: Both files re-read and confirmed consistent

---

## Next Steps

- Task 2.12: Build automated evaluation harness
- Task 2.13: Round 2 execution (run harness against all 50 queries)
