# Task 3.4 Prompt — Apply Hybrid B+A Fixes (Harness + Selective Reclassification)

## Persona
QA engineer fixing a measurement flaw in the evaluation harness and correcting baseline scope misclassifications. You understand the distinction between "in-scope but not KB-covered" and "out-of-scope."

## Context
- **Initiative**: enhancement--poc-evaluation
- **Phase**: Phase 3 — Fix-and-Retest Loop (extended)
- **Dependencies**: T3.3 (Round 3 evaluation — complete, 5/6 targets met)
- **Blocks**: T3.5 (Round 4 evaluation)

### Round 3 Results
| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Deflection Rate | 89.5% | >= 40% | PASS |
| Citation Accuracy | 60.5% | >= 80% | **FAIL** |
| Hallucination Rate | 0.0% | < 15% | PASS |
| OOS Handling | 100.0% | >= 90% | PASS |
| Avg Latency | 1314ms | < 5s | PASS |

### Root Cause Analysis
15 in-scope queries failed citation. They split into two groups:

**Group 1 — Zero-chunk queries (12 queries)**: Q-04, Q-10, Q-17, Q-25, Q-27, Q-28, Q-30, Q-34, Q-35, Q-36, Q-38, Q-40
- ChromaDB returns 0 chunks → system correctly responds "I don't have specific information"
- The harness checks `citation_present` on these responses and marks FAIL
- But there is nothing to cite — the system is correctly identifying its knowledge boundary
- This is a **measurement flaw**, not a system flaw

**Group 2 — Genuine citation failures (3 queries)**: Q-03, Q-23, Q-29
- Q-03: 1 chunk retrieved, LLM didn't cite (nondeterministic — had citation in smoke test)
- Q-23: 1 chunk retrieved, LLM cited using section header format instead of `[Document Title > Section]`
- Q-29: 2 chunks but avg relevance 21% (Low confidence), no citation

### Scope Document Corrections
Per `pilot_phase1_poc/00_docs/01_scope_definition.md`:
- **Q-28** ("How do I track my shipment with Evergreen?") — Real-time tracking is explicitly **excluded** from POC scope. Should be OOS.
- **Q-21** ("Which carriers sail direct to Ho Chi Minh?") — This is literally the **example in-scope query** in the scope document under Carrier Selection. Was incorrectly moved to OOS in T3.2. Must revert.
- **Q-22** ("What's the transit time to Port Klang?") — "Transit times" is explicitly listed as in-scope under Carrier Selection Guidance. Was incorrectly moved to OOS in T3.2. Must revert.

### Design Constraint — No KB Modifications
The knowledge base (`kb/`) is frozen for evaluation integrity. All fixes are to the evaluation harness and baselines only.

## Task

Apply two categories of fixes:

### Fix 1: Harness Measurement Logic (Option B)

Modify `scripts/evaluation_harness.py` to add an `applicable` field to `check_citation_present()`, matching the pattern already used by `check_oos_handling()`.

**File**: `scripts/evaluation_harness.py`

#### 1a. Update `check_citation_present()` (line ~285)

Current:
```python
def check_citation_present(sources: list, citations: list) -> dict:
    """Check if at least one source or citation is present."""
    source_count = len(sources) if sources else 0
    citation_count = len(citations) if citations else 0

    return {
        "pass": source_count > 0 or citation_count > 0,
        "source_count": source_count,
        "citation_count": citation_count,
    }
```

New — add `chunks_retrieved` parameter:
```python
def check_citation_present(sources: list, citations: list, chunks_retrieved: int) -> dict:
    """Check if at least one source or citation is present.

    Not applicable when chunks_retrieved == 0 — the system correctly declines
    these queries and cannot cite nonexistent sources.
    """
    # When no chunks retrieved, citation check is not applicable
    if chunks_retrieved == 0:
        return {
            "pass": True,
            "applicable": False,
            "source_count": 0,
            "citation_count": 0,
            "reason": "No chunks retrieved — citation N/A",
        }

    source_count = len(sources) if sources else 0
    citation_count = len(citations) if citations else 0

    return {
        "pass": source_count > 0 or citation_count > 0,
        "applicable": True,
        "source_count": source_count,
        "citation_count": citation_count,
    }
```

#### 1b. Update `run_checks()` (line ~321)

Pass `chunks_retrieved` from the response metadata to `check_citation_present()`:

```python
# In run_checks(), after extracting citations:
chunks_retrieved = resp.get("metadata", {}).get("chunksRetrieved", 0)

# Update the citation_present call:
"citation_present": check_citation_present(sources, citations, chunks_retrieved),
```

Also update the error fallback to include `applicable`:
```python
"citation_present": {"pass": False, "applicable": True, "source_count": 0, "citation_count": 0},
```

#### 1c. Update `calculate_metrics()` (line ~355)

Filter citation denominator to only `applicable: True` queries:

```python
# Citation accuracy: in-scope with citation applicable and present
citation_applicable = [r for r in in_scope if r["checks"]["citation_present"].get("applicable", True)]
citation_count = sum(1 for r in citation_applicable if r["checks"]["citation_present"]["pass"])
citation_accuracy = (citation_count / len(citation_applicable) * 100) if citation_applicable else 0.0
```

Add the `citation_applicable` count to the returned metrics dict:
```python
"citation_applicable_queries": len(citation_applicable),
```

Do the same for per-category breakdown:
```python
cat_cite_applicable = [r for r in cat_inscope if r["checks"]["citation_present"].get("applicable", True)]
cat_cite = sum(1 for r in cat_cite_applicable if r["checks"]["citation_present"]["pass"])
# ...
"citation_accuracy": (cat_cite / len(cat_cite_applicable) * 100) if cat_cite_applicable else 0.0,
```

#### 1d. Update report generation

In `write_report_md()`, add a note in the Aggregate Metrics table showing both raw and adjusted citation:

After the main metrics table, add:
```markdown
> **Note**: Citation accuracy excludes {N} queries where chunksRetrieved = 0 (system correctly declined — citation N/A). Raw citation rate: {raw}%.
```

In the "Citation Missing" section, separate N/A queries from genuine failures:
```markdown
## Citation N/A (0 chunks retrieved — correct decline)
| Query | Confidence | Reason |
...

## Citation Missing (chunks available but no citation)
| Query | Confidence | Chunks |
...
```

### Fix 2: Baseline Scope Corrections

**File**: `data/evaluation_baselines.json`

#### 2a. Move Q-28 to OOS
Q-28 ("How do I track my shipment with Evergreen?") — real-time tracking explicitly excluded in scope doc.

```json
{
  "id": "Q-28",
  "is_oos": true,
  "must_contain": [],
  "must_not_contain": [],
  "expected_docs": [],
  "oos_decline_signals": ["don't have", "contact", "specific information", "tracking"]
}
```

#### 2b. Revert Q-21 to in-scope
Q-21 ("Which carriers sail direct to Ho Chi Minh?") — the literal example query in scope doc.

Restore to in-scope. However, since the KB genuinely lacks port-specific route data (no carrier doc lists Ho Chi Minh routes by name), keep expectations relaxed:
```json
{
  "id": "Q-21",
  "is_oos": false,
  "must_contain": [],
  "must_not_contain": [],
  "expected_docs": [],
  "notes": "In-scope per scope doc (literal example query), but KB lacks port-specific route data. System will correctly decline — 0 chunks expected."
}
```

#### 2c. Revert Q-22 to in-scope
Q-22 ("What's the transit time to Port Klang?") — transit times explicitly in scope.

Same pattern — in-scope but KB lacks specific transit time data:
```json
{
  "id": "Q-22",
  "is_oos": false,
  "must_contain": [],
  "must_not_contain": [],
  "expected_docs": [],
  "notes": "In-scope per scope doc (transit times in Carrier Selection Guidance), but KB lacks port-specific transit data. System will correctly decline — 0 chunks expected."
}
```

### Fix 3: Smoke Test

After applying fixes, run a quick verification:
```bash
cd pilot_phase1_poc/05_evaluation

# Verify harness loads without errors
venv/Scripts/python -c "from scripts.evaluation_harness import *; print('Harness imports OK')"

# Run 3 queries to verify:
# 1. A 0-chunk query (e.g., Q-10) → citation should be applicable: False
# 2. An in-scope query with chunks (e.g., Q-01) → citation should be applicable: True
# 3. An OOS query (e.g., Q-41) → OOS handling should work as before
```

## Expected Impact

After these fixes, using Round 3 data:

| Metric | Before | After | Logic |
|--------|--------|-------|-------|
| In-scope | 38 | **39** | +Q-21, +Q-22 reverted; -Q-28 to OOS |
| OOS | 12 | **11** | -Q-21, -Q-22 from OOS; +Q-28 to OOS |
| Citation denominator | 38 (all in-scope) | **~26-28** (only applicable) | 0-chunk queries excluded |
| Citation accuracy | 60.5% | **~82-89%** | 23 passes / ~26-28 applicable |

## Format

- **Output**: `TASK_3.4_OUTPUT.md` in `02-output/` with:
  - All code changes documented with before/after
  - Baseline changes documented
  - Smoke test results
  - Expected metric projections for Round 4

## Validation
- [ ] `check_citation_present()` returns `applicable: False` when `chunks_retrieved == 0`
- [ ] `calculate_metrics()` excludes N/A queries from citation denominator
- [ ] Report shows both raw and adjusted citation rates
- [ ] Q-28 moved to OOS in baselines
- [ ] Q-21 reverted to in-scope in baselines
- [ ] Q-22 reverted to in-scope in baselines
- [ ] Baseline counts verified: new in-scope count, new OOS count
- [ ] Harness smoke test passes without errors
- [ ] Changes documented in TASK_3.4_OUTPUT.md

## Update on Completion

**MANDATORY — Update ALL tracking locations:**
- **Checklist**: `03-checklist/IMPLEMENTATION_CHECKLIST.md` — mark Task 3.4 `[x]` AND update Phase 3 progress (4/5, 80%) + Total (27/45, 60%)
- **Roadmap**: `02-roadmap/IMPLEMENTATION_ROADMAP.md` — update ALL locations:
  1. **Progress Tracker** table (top) — Phase 3: 5 | 4 | 🔄, Total: 45 | 27 | 60%
  2. **Quick Reference** table — change Task 3.4 status `Pending` -> `Complete`
  3. **Detailed task entry** — change `Status: Pending` -> `Status: Complete` AND check validation boxes `[x]`
- **Bootstrap file**: `ai-workflow-bootstrap-prompt-v3.md` — update Active Initiatives progress count (27/45 -- 60%)
- **CLAUDE.md** (root) — update Active Initiatives progress count (27/45 — 60%)
- **AGENTS.md** (root) — update Active Initiatives progress count (27/45 -- 60%)
- **Verify**: Re-read all updated files to confirm consistency
