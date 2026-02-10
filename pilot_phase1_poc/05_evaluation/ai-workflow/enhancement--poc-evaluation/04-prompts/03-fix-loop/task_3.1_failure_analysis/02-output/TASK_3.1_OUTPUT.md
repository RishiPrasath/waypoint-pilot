# Task 3.1 Output — Failure Analysis

**Task:** 3.1 - Failure analysis
**Phase:** Phase 3 — Fix-and-Retest Loop
**Status:** PASS
**Date:** 2026-02-10

---

## Summary

Analyzed all 37 failing queries from Round 2. Classified each into 6 root cause categories. Produced `reports/failure_analysis.md` with per-query classification, impact analysis, and a 6-fix priority plan for Task 3.2.

---

## Key Findings

### Root Cause Distribution

| Root Cause | Count | % |
|-----------|-------|---|
| CG — Citation Gap (LLM has context but doesn't cite) | 11 | 30% |
| OC — OOS Citation (correct OOS handling, evaluation design) | 9 | 24% |
| RM — Retrieval Miss (content exists but not retrieved) | 8 | 22% |
| KC — KB Content Gap (genuine missing content) | 4 | 11% |
| RM+BM — Retrieval + Baseline mismatch | 3 | 8% |
| LS — Latency Spike (good response, slow) | 2 | 5% |

### The Two Failing Metrics — Root Causes

**Citation Accuracy (36.6%, target 80%)**:
- 11 queries have context but LLM doesn't produce `[Title > Section]` citations → Fix: strengthen prompt
- 8 queries have no chunks retrieved → Fix: KB body text + retrieval
- Fixing CG alone: 63.4%. Fixing CG + RM: 82.9% (exceeds target)

**Hallucination Rate (24.0%, target <15%)**:
- ALL 12 detections are "I don't have" false positives
- System correctly declines when retrieval returns 0 chunks
- Fix: reclassify baselines for queries where content genuinely doesn't exist

### Top 5 Fix Priorities

1. **Strengthen system prompt citation instructions** — Impact: +11 queries citation, Low effort
2. **Reclassify baselines** (remove "I don't have" from must_not_contain) — Impact: -12 hallucination false positives, Low effort
3. **Add key terms to KB body text** (eBL, booking amendment, express) — Impact: +5-8 retrieval, Medium effort
4. **Lower confidence Medium threshold** (avgScore 0.4 → 0.3) — Impact: better LLM citation behavior, Low effort
5. **Add missing KB content** (container weights, transit times) — Impact: +2-4 queries, Medium effort

---

## Files Created

- `reports/failure_analysis.md` — full failure analysis with per-query classification, 6-section detailed analysis, fix priority matrix, and specific Task 3.2 plan

---

## Tracking Updates

- [x] Checklist updated: Marked Task 3.1 [x] + Phase 3 progress (1/3, 33%) + Total (24/43, 56%)
- [x] Roadmap updated: Progress Tracker + Quick Reference + Detailed task status + validation checkboxes
- [x] Bootstrap file updated: Active Initiatives progress count (24/43 -- 56%)
- [x] CLAUDE.md updated: Active Initiatives progress count
- [x] AGENTS.md updated: Active Initiatives progress count
- [x] Verified: Re-read all files, all locations consistent

---

## Next Steps

- **Task 3.2**: Apply fixes (prompt, baselines, KB content, confidence threshold) — follow the 6-fix execution plan in `reports/failure_analysis.md`
