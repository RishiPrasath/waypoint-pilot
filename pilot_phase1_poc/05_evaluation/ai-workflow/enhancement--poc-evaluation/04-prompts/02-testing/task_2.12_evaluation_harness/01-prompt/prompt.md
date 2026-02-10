# Task 2.12 Prompt — Build Automated Evaluation Harness

## Persona
Senior QA automation engineer building a Python evaluation harness that sends 50 queries to a live RAG API, runs automated answer-quality checks, and produces aggregate metrics + detailed reports.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Phase**: Phase 2 — Systematic Testing (Layer 5: End-to-End Evaluation)
- **Dependencies**: T2.11 (evaluation baselines — complete)
- **Blocks**: T2.13 (Round 2 execution)
- **Current state**: `data/evaluation_baselines.json` exists with 50 query baselines. Backend runs on `http://localhost:3000`. No evaluation harness script exists yet.

### API Endpoint

**`POST http://localhost:3000/api/query`**

Request body:
```json
{ "query": "What is the GST rate for imports into Singapore?" }
```

Response shape (from `backend/services/pipeline.js`):
```json
{
  "answer": "string — markdown-formatted answer text",
  "sources": [
    { "title": "string", "org": "string", "url": "string", "section": "string|null" }
  ],
  "relatedDocs": [
    { "title": "string", "category": "regulatory|carrier|internal|reference", "docId": "string", "url": "string|null" }
  ],
  "citations": [
    { "raw": "string", "title": "string", "matched": true }
  ],
  "confidence": {
    "level": "High|Medium|Low",
    "reason": "string"
  },
  "metadata": {
    "query": "string",
    "chunksRetrieved": 10,
    "chunksUsed": 3,
    "latencyMs": 1500,
    "model": "llama-3.1-8b-instant"
  }
}
```

Error response (no chunks found):
```json
{
  "answer": "I don't have specific information about that topic...",
  "sources": [],
  "relatedDocs": [],
  "citations": [],
  "confidence": { "level": "Low", "reason": "No relevant documents found" },
  "metadata": { "chunksRetrieved": 0, "chunksUsed": 0, "latencyMs": 250, "model": null }
}
```

### Baselines File Schema (`data/evaluation_baselines.json`)
```json
{
  "version": "1.0",
  "queries": [
    {
      "id": "Q-01",
      "category": "booking",
      "query": "What documents are needed for sea freight Singapore to Indonesia?",
      "is_oos": false,
      "expected_docs": ["sg_export", "indonesia_import"],
      "must_contain": ["commercial invoice", "packing list", "bill of lading"],
      "should_contain": ["certificate of origin", "Form D"],
      "must_not_contain": ["I don't have", "no information available"],
      "oos_decline_signals": []
    }
  ]
}
```

### Rate Limiting
- **Groq free tier**: 30 requests/minute, 14,400 requests/day
- Default delay: 30 seconds between queries (configurable via `EVAL_DELAY_SECONDS` env var)
- Handle HTTP 429 with exponential backoff (30s → 60s → 120s, max 3 retries)

### Week 4 Targets
| Metric | Target |
|--------|--------|
| Deflection Rate | ≥ 40% |
| Citation Accuracy | ≥ 80% |
| Hallucination Rate | < 15% |
| OOS Handling | ≥ 90% |
| Avg Latency | < 5s |

## Task

Create `scripts/evaluation_harness.py` — a standalone Python script that:
1. Loads baselines from `data/evaluation_baselines.json`
2. Sends each query to `POST /api/query`
3. Runs 6 automated checks per response
4. Calculates aggregate metrics
5. Outputs 3 report files

### Script Structure

```python
"""
Evaluation Harness for Waypoint Co-Pilot
Sends 50 queries to the live API, checks answers against baselines,
and generates evaluation reports.

Usage:
  python scripts/evaluation_harness.py
  python scripts/evaluation_harness.py --delay 10
  python scripts/evaluation_harness.py --start-from Q-15
  python scripts/evaluation_harness.py --dry-run

Environment:
  EVAL_DELAY_SECONDS  — delay between queries (default: 30)
  EVAL_API_URL        — API base URL (default: http://localhost:3000)
"""
```

### CLI Arguments

| Arg | Default | Purpose |
|-----|---------|---------|
| `--delay` | 30 (or `EVAL_DELAY_SECONDS` env) | Seconds between API calls |
| `--start-from` | Q-01 | Resume from a specific query ID (for partial runs) |
| `--dry-run` | false | Load baselines and validate, don't send queries |
| `--output-dir` | `.` (cwd = `05_evaluation/`) | Base directory for output files |

### Step 1: Load Baselines

```python
def load_baselines(path: str) -> list[dict]:
    """Load and validate evaluation_baselines.json."""
    # Parse JSON
    # Validate: 50 queries, all required fields present
    # Return sorted by id (Q-01 through Q-50)
```

### Step 2: Send Queries

```python
def send_query(api_url: str, query: str, timeout: int = 30) -> dict:
    """
    Send a single query to POST /api/query.
    Returns: { "response": <parsed JSON>, "latency_ms": <int>, "status_code": <int>, "error": <str|None> }
    """
    # Use requests library
    # Capture client-side latency (separate from server-reported latency)
    # Handle: ConnectionError, Timeout, HTTP 429, HTTP 500, JSON decode error
```

```python
def run_all_queries(baselines: list, api_url: str, delay: int, start_from: str) -> list[dict]:
    """
    Send all 50 queries sequentially with delay between each.
    Returns list of { "baseline": <baseline>, "result": <send_query result> }
    """
    # Skip queries before start_from
    # Print progress: [01/50] Q-01: "What documents are needed..." (1.2s) ✓
    # On 429: exponential backoff (30s, 60s, 120s), max 3 retries
    # On error: log and continue (don't abort the run)
    # Sleep delay seconds between requests
```

### Step 3: Run Automated Checks (6 checks per response)

```python
def check_must_contain(answer: str, keywords: list[str]) -> dict:
    """
    Check if answer contains all required keywords.
    Returns: { "pass": bool, "total": int, "matched": int, "missing": list[str] }
    Case-insensitive substring match.
    """

def check_must_not_contain(answer: str, keywords: list[str]) -> dict:
    """
    Check if answer does NOT contain hallucination signals.
    Returns: { "pass": bool, "found": list[str] }
    Case-insensitive substring match.
    """

def check_expected_docs(related_docs: list[dict], expected: list[str]) -> dict:
    """
    Check if at least one expected doc_id keyword appears in relatedDocs.
    Match: expected keyword is substring of relatedDoc's docId (case-insensitive).
    Returns: { "pass": bool, "expected": list, "found": list[str] }
    """

def check_citation_present(sources: list[dict], citations: list[dict]) -> dict:
    """
    Check if at least one source or citation is present in the response.
    Returns: { "pass": bool, "source_count": int, "citation_count": int }
    """

def check_oos_handling(answer: str, is_oos: bool, decline_signals: list[str]) -> dict:
    """
    For OOS queries: check if at least one decline signal appears.
    For in-scope queries: always pass (N/A).
    Returns: { "pass": bool, "applicable": bool, "signals_found": list[str] }
    """

def check_latency(latency_ms: int, threshold_ms: int = 5000) -> dict:
    """
    Check if response time is under threshold.
    Returns: { "pass": bool, "latency_ms": int, "threshold_ms": int }
    """
```

### Step 4: Calculate Aggregate Metrics

```python
def calculate_metrics(results: list[dict]) -> dict:
    """
    Calculate aggregate metrics from all 50 query results.

    Returns: {
      "deflection_rate": float,     # % of in-scope with must_contain pass
      "citation_accuracy": float,   # % of in-scope with citation present
      "hallucination_rate": float,  # % of ALL queries with must_not_contain fail
      "oos_handling_rate": float,   # % of OOS queries with decline signal
      "avg_latency_ms": float,     # average across all queries
      "latency_under_5s": float,   # % under 5 seconds
      "total_queries": int,
      "successful_queries": int,   # got a valid response (not error)
      "failed_queries": int,       # server errors, timeouts
      "by_category": {
        "booking": { "total": 10, "deflection": float, ... },
        "customs": { ... },
        "carrier": { ... },
        "sla": { ... },
        "edge_case": { ... }
      }
    }
    """
```

**Metric Definitions:**
- **Deflection Rate** = `(in-scope queries where ALL must_contain keywords found) / (total in-scope queries)` — this approximates whether the answer addresses the question
- **Citation Accuracy** = `(in-scope queries with ≥1 source or citation) / (total in-scope queries)`
- **Hallucination Rate** = `(queries where ANY must_not_contain keyword found) / (total successful queries)`
- **OOS Handling Rate** = `(OOS queries with ≥1 decline signal) / (total OOS queries)`

### Step 5: Generate 3 Output Files

#### 5a. `data/evaluation_results.json` — Raw results
```json
{
  "run_id": "eval-2026-02-09T14-30-00",
  "timestamp": "2026-02-09T14:30:00Z",
  "config": { "delay_seconds": 30, "api_url": "http://localhost:3000", "baselines_version": "1.0" },
  "metrics": { /* aggregate metrics from Step 4 */ },
  "results": [
    {
      "id": "Q-01",
      "category": "booking",
      "query": "What documents are needed...",
      "is_oos": false,
      "response": {
        "answer": "For sea freight export from Singapore...",
        "sources": [ ... ],
        "relatedDocs": [ ... ],
        "confidence": { "level": "Medium", "reason": "..." },
        "metadata": { "chunksRetrieved": 10, "chunksUsed": 3, "latencyMs": 1500 }
      },
      "checks": {
        "must_contain": { "pass": true, "total": 3, "matched": 3, "missing": [] },
        "must_not_contain": { "pass": true, "found": [] },
        "expected_docs": { "pass": true, "expected": ["sg_export", "indonesia_import"], "found": ["sg_export"] },
        "citation_present": { "pass": true, "source_count": 2, "citation_count": 1 },
        "oos_handling": { "pass": true, "applicable": false },
        "latency": { "pass": true, "latency_ms": 1500, "threshold_ms": 5000 }
      },
      "overall_pass": true,
      "client_latency_ms": 1650,
      "error": null
    }
  ]
}
```

#### 5b. `reports/evaluation_report.md` — Human-readable report
```markdown
# Evaluation Report — Round N

**Date**: 2026-02-09
**Run ID**: eval-2026-02-09T14-30-00
**Queries**: 50 (41 in-scope, 9 OOS)

## Aggregate Metrics

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Deflection Rate | X% | ≥ 40% | PASS/FAIL |
| Citation Accuracy | X% | ≥ 80% | PASS/FAIL |
| Hallucination Rate | X% | < 15% | PASS/FAIL |
| OOS Handling | X% | ≥ 90% | PASS/FAIL |
| Avg Latency | Xs | < 5s | PASS/FAIL |

## Per-Category Breakdown

| Category | Queries | Deflection | Citation | Hallucination | Avg Latency |
|----------|---------|------------|----------|--------------|-------------|
| booking | 10 | X% | X% | X% | Xs |
| customs | 10 | X% | X% | X% | Xs |
| carrier | 10 | X% | X% | X% | Xs |
| sla | 10 | X% | X% | X% | Xs |
| edge_case | 10 | X% | X% | X% | Xs |

## Failures

### must_contain Failures
| Query | Missing Keywords |
|-------|-----------------|
| Q-XX | keyword1, keyword2 |

### Hallucination Detections
| Query | Found Signals |
|-------|--------------|
| Q-XX | signal1 |

### OOS Failures
| Query | Expected Decline | Got |
|-------|-----------------|-----|
| Q-XX | "don't have..." | (answer text excerpt) |

## Raw Query Results

| ID | Category | Confidence | Deflect | Citation | Halluc | OOS | Latency | Pass |
|----|----------|------------|---------|----------|--------|-----|---------|------|
| Q-01 | booking | Medium | ✓ | ✓ | ✓ | — | 1.5s | ✓ |
[...all 50 rows...]
```

#### 5c. `data/evaluation_results.csv` — Spreadsheet-friendly
```
id,category,query,is_oos,confidence,must_contain_pass,must_contain_matched,must_contain_total,must_not_contain_pass,expected_docs_pass,citation_present,oos_handling_pass,latency_ms,overall_pass,error
Q-01,booking,"What documents are needed...",false,Medium,true,3,3,true,true,true,true,1500,true,
```

### Step 6: Error Handling

- **Connection refused**: Print "Backend not running on {api_url}. Start with: cd 05_evaluation && npm start" and exit
- **HTTP 429**: Exponential backoff (delay × 2^retry), max 3 retries, then log failure and continue
- **HTTP 500**: Log error, record as failed query, continue
- **Timeout (30s)**: Log timeout, record as failed query, continue
- **Partial run**: If `--start-from` used, merge with existing `evaluation_results.json` if it exists
- **Ctrl+C**: Catch KeyboardInterrupt, save partial results, calculate metrics on completed queries

### Dependencies

The script should use only packages already in `requirements.txt`:
- `requests` (should already be installed; if not, add it)
- `json`, `csv`, `datetime`, `time`, `argparse`, `os`, `sys` (stdlib)

Check `requirements.txt` and add `requests` if missing.

## Format
- **Create**: `scripts/evaluation_harness.py`
- **Modify**: `requirements.txt` (add `requests` if missing)
- **Output**: `TASK_2.12_OUTPUT.md` with script overview and dry-run validation
- **Validation**:
  - `python scripts/evaluation_harness.py --dry-run` — loads baselines, validates 50 queries, exits without sending
  - `python scripts/evaluation_harness.py --delay 5 --start-from Q-01` — test with 1-2 queries (Ctrl+C after verifying)
  - Script handles connection refused gracefully

## Update on Completion

**MANDATORY — Update ALL tracking locations:**
- **Checklist**: `03-checklist/IMPLEMENTATION_CHECKLIST.md` — mark Task 2.12 `[x]` AND update Phase 2 + Total progress counts
- **Roadmap**: `02-roadmap/IMPLEMENTATION_ROADMAP.md` — update ALL THREE locations:
  1. **Progress Tracker** table (top) — increment Phase 2 completed count and overall percentage
  2. **Quick Reference** table — change Task 2.12 status `⬜ Pending` → `✅ Complete`
  3. **Detailed task entry** — change `**Status**: ⬜ Pending` → `**Status**: ✅ Complete` AND check validation boxes `[x]`
- **Bootstrap file**: `ai-workflow-bootstrap-prompt-v3.md` — update Active Initiatives progress count
- **CLAUDE.md** (root) — update Active Initiatives progress count
- **AGENTS.md** (root) — update Active Initiatives progress count
- **Verify**: Re-read all updated files to confirm consistency
