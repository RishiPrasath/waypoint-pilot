# Task 3.3 Prompt — Re-run Evaluation (Round 3)

## Persona
QA engineer executing the automated evaluation harness after fixes applied in Task 3.2. You are running the full 50-query suite and comparing results against targets.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Phase**: Phase 3 — Fix-and-Retest Loop
- **Dependencies**: T3.2 (apply fixes — complete)
- **Blocks**: CP3 (Checkpoint 3 — Round 3 metrics finalized)

### Fixes Applied in T3.2 (no KB modifications)

| Fix | Change |
|-----|--------|
| Prompt | Citation instructions strengthened (MANDATORY + exact title matching + "do not claim without citing") |
| Baselines | 13 queries reclassified: 7 false positive hallucination signals removed, 6 RM queries relaxed as known KB gaps, 3 moved to OOS |
| Thresholds | Medium: 0.4→0.3, High: 0.6→0.5 |

### New Baseline Counts
- In-scope: 38 (was 41)
- OOS: 12 (was 9)

### Round 2 Results (baseline for comparison)

| Metric | Round 2 | Target | Status |
|--------|---------|--------|--------|
| Deflection Rate | 63.4% | >= 40% | PASS |
| Citation Accuracy | 36.6% | >= 80% | FAIL |
| Hallucination Rate | 24.0% | < 15% | FAIL |
| OOS Handling | 100.0% | >= 90% | PASS |
| Avg Latency | 1633ms | < 5s | PASS |

### Smoke Test Results (from T3.2)
- Q-01, Q-02, Q-03: Now produce citations (were 0 in Round 2)
- Q-11: Promoted to Medium confidence, still correct
- No regressions detected

## Task

Execute the full 50-query evaluation and generate Round 3 results.

### Step 1: Ensure Backend is Running

```bash
cd pilot_phase1_poc/05_evaluation

# Check if backend is running
curl -s http://localhost:3000/api/health

# If not running, start it
npm start
```

### Step 2: Run Full Evaluation

```bash
cd pilot_phase1_poc/05_evaluation
venv/Scripts/python scripts/evaluation_harness.py --delay 10
```

- All 50 queries, ~10 minutes
- Outputs: `data/evaluation_results.json`, `data/evaluation_results.csv`, `reports/evaluation_report.md`

### Step 3: Compare Against Targets

| Metric | Target | Hard Gate |
|--------|--------|-----------|
| Deflection Rate | >= 40% | Yes |
| Citation Accuracy | >= 80% | Yes |
| Hallucination Rate | < 15% | Yes |
| OOS Handling | >= 90% | Yes |
| Avg Latency | < 5s | Yes |
| System Stability | No crashes | Yes |

### Step 4: Decision Gate

- **All targets met**: Task 3.3 complete. Proceed to CP3.
- **Any target not met**: Document which metrics failed and by how much. Return to T3.1 for another fix cycle. (But do NOT auto-start — report results and let human decide.)

### Step 5: Round-over-Round Comparison

Create a comparison table showing Round 2 vs Round 3 for each metric, with delta and pass/fail status.

## Format

- **Run**: `python scripts/evaluation_harness.py --delay 10` (full 50-query suite)
- **Output**: `TASK_3.3_OUTPUT.md` with:
  - Aggregate metrics table (Round 3 vs Round 2 vs Target)
  - Per-query results summary (any regressions flagged)
  - Decision: all targets met? or which failed?
  - If all pass: ready for CP3

## Validation
- [ ] All 50 queries executed successfully (0 errors)
- [ ] Deflection Rate >= 40%
- [ ] Citation Accuracy >= 80%
- [ ] Hallucination Rate < 15%
- [ ] OOS Handling Rate >= 90%
- [ ] Average Latency < 5 seconds
- [ ] No system crashes during evaluation run
- [ ] All targets met simultaneously in a single run
- [ ] Round 2 vs Round 3 comparison documented

## Update on Completion

**MANDATORY — Update ALL tracking locations:**
- **Checklist**: `03-checklist/IMPLEMENTATION_CHECKLIST.md` — mark Task 3.3 `[x]` AND update Phase 3 progress (3/3, 100%) + Total (26/43, 60%)
- **Roadmap**: `02-roadmap/IMPLEMENTATION_ROADMAP.md` — update ALL FOUR locations:
  1. **Progress Tracker** table (top) — Phase 3: 3 | 3 | Complete, Total: 43 | 26 | 60%
  2. **Quick Reference** table — change Task 3.3 status `Pending` -> `Complete`
  3. **Detailed task entry** — change `Status: Pending` -> `Status: Complete` AND check validation boxes `[x]`
- **Bootstrap file**: `ai-workflow-bootstrap-prompt-v3.md` — update Active Initiatives progress count (26/43 -- 60%)
- **CLAUDE.md** (root) — update Active Initiatives progress count (26/43 — 60%)
- **AGENTS.md** (root) — update Active Initiatives progress count (26/43 -- 60%)
- **Verify**: Re-read all updated files to confirm consistency
