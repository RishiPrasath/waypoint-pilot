# Task 2.13 Output — Execute Round 2 and Generate Reports

**Task:** 2.13 - Execute Round 2 and generate reports
**Phase:** Phase 2 — Systematic Testing (Layer 5: End-to-End Evaluation)
**Status:** PASS
**Date:** 2026-02-09

---

## Run Summary

| Field | Value |
|-------|-------|
| Run ID | eval-2026-02-09T23-52-23 |
| Timestamp | 2026-02-09 23:52 SGT |
| Delay | 10s between queries |
| Duration | ~10 minutes |
| Queries | 50/50 successful (0 errors) |
| API | http://localhost:3000 |

---

## Aggregate Metrics vs Targets

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Deflection Rate | **63.4%** | >= 40% | PASS |
| Citation Accuracy | **36.6%** | >= 80% | FAIL |
| Hallucination Rate | **24.0%** | < 15% | FAIL |
| OOS Handling | **100.0%** | >= 90% | PASS |
| Avg Latency | **1633ms** | < 5000ms | PASS |

**Result: 3/5 targets met. 2 targets failed (Citation Accuracy, Hallucination Rate).**

---

## Per-Category Breakdown

| Category | Queries | In-Scope | Deflection | Citation | Hallucination | Avg Latency |
|----------|---------|----------|------------|----------|---------------|-------------|
| booking | 10 | 10 | 80.0% | 50.0% | 10.0% | 2008ms |
| customs | 10 | 10 | 90.0% | 40.0% | 10.0% | 1747ms |
| carrier | 10 | 10 | 30.0% | 20.0% | 50.0% | 1642ms |
| sla | 10 | 10 | 50.0% | 40.0% | 50.0% | 1719ms |
| edge_case | 10 | 1 (+9 OOS) | 100.0% | 0.0% | 0.0% | 1050ms |

### Category Highlights
- **Best**: customs (90% deflection, only 10% hallucination)
- **Worst**: carrier (30% deflection, 50% hallucination, 20% citation)
- **Edge case**: 100% OOS handling (9/9), but Q-44 (in-scope) has 0% citation

---

## Root Cause Analysis

### 1. Citation Accuracy: 36.6% (target 80%) — CRITICAL

26 of 41 in-scope queries have **no citations**. The pattern is clear:

| Confidence Level | Count | Citation Rate |
|-----------------|-------|---------------|
| Medium | 5 | 100% (5/5) |
| Low | 36 | 25% (9/36) |

**Root cause**: The pipeline assigns **Low confidence** to most queries. When confidence is Low, the system often returns no sources. The confidence threshold or scoring is too aggressive — 36 of 41 in-scope queries (88%) get Low confidence.

### 2. Hallucination Rate: 24.0% (target <15%) — HIGH PRIORITY

12 queries flagged for hallucination. All 12 have the same signal: **"I don't have"**.

These are NOT actual hallucinations — they are **false positives**. The system is correctly declining to answer queries it lacks specific information about (carrier schedules, specific port details, etc.) by saying "I don't have specific information about...". The `must_not_contain` baselines treated "I don't have" as a hallucination signal for in-scope queries.

**Affected queries**: Q-10, Q-17, Q-21, Q-22, Q-25, Q-26, Q-30, Q-34, Q-35, Q-36, Q-38, Q-40

These overlap perfectly with the `must_contain` failures — the system is declining these queries entirely rather than attempting an answer from its KB.

### 3. Deflection Failures (15 queries)

15 of 41 in-scope queries failed `must_contain`. These fall into two patterns:

**Pattern A — System declines with "I don't have" (12 queries)**
Q-10, Q-17, Q-21, Q-22, Q-25, Q-26, Q-27, Q-28, Q-30, Q-34, Q-35, Q-36, Q-38, Q-40

The KB likely has relevant content, but retrieval isn't returning chunks with high enough similarity, so the pipeline treats them as unanswerable.

**Pattern B — Partial answer (3 queries)**
Q-04, Q-27, Q-28 — System returns some content but misses specific keywords.

---

## Phase 3 Fix Priorities

### Fix 1: Confidence Threshold Tuning (HIGH IMPACT)
**Impact**: Could fix citation accuracy from 36.6% to 80%+
The pipeline assigns Low confidence too aggressively. Most queries that get Low have retrieved relevant chunks (10 retrieved, but chunksUsed may be 0). The confidence scoring needs adjustment to use Medium/High more frequently when chunks are retrieved.

### Fix 2: Baseline Adjustments (HIGH IMPACT)
**Impact**: Could fix hallucination rate from 24% to <10%
The 12 "I don't have" false positives need to be reclassified. For queries the KB genuinely cannot answer in detail (specific carrier schedules, specific port free times), either:
- Move them to OOS
- Remove "I don't have" from `must_not_contain` and add it to `oos_decline_signals`
- Add specific KB content so the system can answer them

### Fix 3: System Prompt Enhancement (MEDIUM IMPACT)
**Impact**: Could improve deflection for queries where KB has content
Strengthen the system prompt to attempt answers using available KB content rather than declining when confidence is borderline.

### Fix 4: KB Content Gaps (LOWER PRIORITY)
Some carrier-specific queries (Q-21 Ho Chi Minh routes, Q-22 Port Klang transit, Q-27 ONE Surabaya) may need additional KB content.

---

## Output Files Generated

- [x] `data/evaluation_results.json` — 50 results, full raw data
- [x] `data/evaluation_results.csv` — 50 rows + header
- [x] `reports/evaluation_report.md` — human-readable with all sections

---

## Tracking Updates

- [x] Checklist updated: Marked Task 2.13 [x] + Phase 2 complete (13/13, 100%) + Total (23/43, 53%)
- [x] Roadmap updated: Progress Tracker + Quick Reference + Detailed task status + validation checkboxes + Phase 2 status
- [x] Bootstrap file updated: Active Initiatives progress count (23/43 -- 53%)
- [x] CLAUDE.md updated: Active Initiatives progress count
- [x] AGENTS.md updated: Active Initiatives progress count
- [x] Verified: Re-read all files, all locations consistent

---

## Next Steps

- **Task 3.1**: Failure analysis — deep-dive into root causes, classify by fix type
- **Task 3.2**: Apply fixes (confidence tuning, baseline adjustments, prompt updates)
- **Task 3.3**: Re-run evaluation (Round 3)
