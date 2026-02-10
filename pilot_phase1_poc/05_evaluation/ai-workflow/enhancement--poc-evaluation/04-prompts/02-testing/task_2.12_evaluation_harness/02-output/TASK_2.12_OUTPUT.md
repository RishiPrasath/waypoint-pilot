# Task 2.12 Output - Build Automated Evaluation Harness

**Task:** 2.12 - Build automated evaluation harness
**Phase:** Phase 2 - Systematic Testing (Layer 5: End-to-End Evaluation)
**Status:** PASS
**Date:** 2026-02-09

---

## Summary

Created `scripts/evaluation_harness.py` - a standalone Python evaluation script that sends 50 queries to the live RAG API, runs 6 automated answer-quality checks per response, calculates 5 aggregate metrics, and outputs 3 report formats (JSON, CSV, Markdown).

---

## File Created

- **`scripts/evaluation_harness.py`** - 450+ lines, fully functional

## No Dependencies Added

`requests` was already in `requirements.txt`.

---

## Features

### CLI Arguments
| Arg | Default | Purpose |
|-----|---------|---------|
| `--delay` | 30 (or `EVAL_DELAY_SECONDS` env) | Seconds between API calls |
| `--start-from` | Q-01 | Resume from a specific query ID |
| `--dry-run` | false | Validate baselines without sending queries |
| `--api-url` | http://localhost:3000 | API base URL |

### 6 Automated Checks
1. **must_contain** - case-insensitive substring match for required keywords
2. **must_not_contain** - hallucination signal detection
3. **expected_docs** - at least one expected doc in relatedDocs
4. **citation_present** - at least one source or citation in response
5. **oos_handling** - decline signals present for OOS queries
6. **latency** - response under 5 seconds

### 3 Output Files
1. `data/evaluation_results.json` - full raw results with checks
2. `data/evaluation_results.csv` - one row per query, spreadsheet-friendly
3. `reports/evaluation_report.md` - human-readable with metrics, failures, per-category breakdown

### Error Handling
- Connection refused: friendly message + exit
- HTTP 429: exponential backoff (30s, 60s, 120s), max 3 retries
- HTTP 500: log error, continue with remaining queries
- Timeout (30s): log timeout, continue
- Ctrl+C: save partial results

---

## Validation

### Dry Run
```
$ python scripts/evaluation_harness.py --dry-run

Loaded 50 baselines (version: 1.0)
  41 in-scope, 9 out-of-scope
  must_contain keywords:     83
  should_contain keywords:   183
  must_not_contain keywords: 125
  All in-scope queries have >= 2 must_contain PASS
  All OOS queries have >= 1 decline signal PASS
  Estimated run time: 25m 0s (at 30s delay)
```

### Live Query Test (Q-01 - In-scope)
```
Q-01: "What documents are needed for sea freight Singapore to Indonesia?"
  must_contain:     PASS (3/3: commercial invoice, packing list, bill of lading)
  must_not_contain: PASS (no hallucination signals)
  expected_docs:    PASS (found: sg_export)
  citation_present: FAIL (0 sources - Low confidence, no chunks used)
  oos_handling:     PASS (N/A - in-scope)
  latency:          FAIL (19934ms - cold start)
```

### Live Query Test (Q-41 - OOS)
```
Q-41: "What's the current freight rate to Jakarta?"
  must_contain:     PASS (0 required for OOS)
  must_not_contain: PASS (no hallucinated rates)
  expected_docs:    PASS (none expected)
  citation_present: FAIL (correct - OOS has no citations)
  oos_handling:     PASS (found: "don't have", "contact", "sales", "specific information")
  latency:          FAIL (5426ms - marginal)
```

---

## Observations

1. **Cold start latency** - First query took ~20s (cold start for Python ChromaDB subprocess + Groq API). Subsequent queries will be faster.
2. **Citation check on OOS** - OOS queries correctly have no citations, but `citation_present` marks them as FAIL. This is expected behavior - the metric only counts in-scope queries for citation accuracy.
3. **Estimated run time** - ~25 minutes at 30s delay, ~8 minutes at 10s delay.

---

## Tracking Updates

- [x] Checklist updated: Marked Task 2.12 [x] + Progress Summary totals
- [x] Roadmap updated: Progress Tracker totals + Quick Reference status + Detailed task status + validation checkboxes
- [x] Bootstrap file updated: Active Initiatives progress count (22/43 - 51%)
- [x] CLAUDE.md updated: Active Initiatives progress count
- [x] AGENTS.md updated: Active Initiatives progress count
- [x] Verified: Re-read all files, all locations consistent

---

## Next Steps

- Task 2.13: Execute Round 2 (run full 50-query evaluation)
