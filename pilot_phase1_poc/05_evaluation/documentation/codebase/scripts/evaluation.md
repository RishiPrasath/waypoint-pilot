# Evaluation Harness

Layer 3 documentation for `evaluation_harness.py`.

This script sends 50 queries to the live Waypoint Co-Pilot API, runs automated checks against predefined baselines, calculates aggregate metrics, and generates evaluation reports.

---

## Prerequisites

- Backend API running on `http://localhost:3000` (or custom URL via `--api-url`)
- ChromaDB ingested with the knowledge base
- Baselines file at `data/evaluation_baselines.json`

---

## CLI Interface

```
usage: evaluation_harness.py [-h] [--delay DELAY] [--start-from START_FROM]
                              [--dry-run] [--api-url API_URL]

optional arguments:
  --delay DELAY         Seconds between API calls (default: 30, from EVAL_DELAY_SECONDS env)
  --start-from START_FROM  Resume from a specific query ID (e.g., Q-15)
  --dry-run             Load baselines and validate, don't send queries
  --api-url API_URL     API base URL (default: http://localhost:3000, from EVAL_API_URL env)
```

---

## Configuration Constants

| Constant | Value | Source | Description |
|----------|-------|--------|-------------|
| `DEFAULT_DELAY` | `30` | `EVAL_DELAY_SECONDS` env | Seconds between queries |
| `DEFAULT_API_URL` | `http://localhost:3000` | `EVAL_API_URL` env | API base URL |
| `QUERY_ENDPOINT` | `/api/query` | hardcoded | POST endpoint for queries |
| `REQUEST_TIMEOUT` | `30` | hardcoded | HTTP request timeout (seconds) |
| `LATENCY_THRESHOLD_MS` | `5000` | hardcoded | Latency pass/fail threshold |
| `MAX_RETRIES` | `3` | hardcoded | Max retries on 429 rate limit |

### File Paths (relative to `05_evaluation/`)

| Constant | Path | Description |
|----------|------|-------------|
| `BASELINES_PATH` | `data/evaluation_baselines.json` | Input: 50 query baselines |
| `RESULTS_JSON_PATH` | `data/evaluation_results.json` | Output: full results JSON |
| `RESULTS_CSV_PATH` | `data/evaluation_results.csv` | Output: results CSV |
| `REPORT_MD_PATH` | `reports/evaluation_report.md` | Output: markdown report |

### Week 4 Targets

| Metric | Target | Direction |
|--------|--------|-----------|
| `deflection_rate` | >= 40% | Higher is better |
| `citation_accuracy` | >= 80% | Higher is better |
| `hallucination_rate` | < 15% | Lower is better |
| `oos_handling_rate` | >= 90% | Higher is better |
| `avg_latency_ms` | < 5000ms | Lower is better |

---

## Functions

### Step 1: Load Baselines

#### `load_baselines(path: str = None) -> list`

Loads and validates `evaluation_baselines.json`.

**Parameters:**
- `path` (`str | None`): Custom baselines file path. Uses `BASELINES_PATH` if None.

**Returns:** List of 50 baseline query dicts, sorted by `id`.

**Required fields per query:**
- `id` (str): Query ID, e.g., `"Q-01"`
- `category` (str): `"booking"`, `"customs"`, `"carrier"`, `"sla"`, `"edge_case"`
- `query` (str): The query text
- `is_oos` (bool): Whether the query is out-of-scope
- `expected_docs` (list[str]): Expected document ID patterns
- `must_contain` (list[str]): Required keywords in the answer
- `must_not_contain` (list[str]): Hallucination signal keywords
- `oos_decline_signals` (list[str]): Decline phrases for OOS queries (optional but expected for OOS)
- `should_contain` (list[str]): Optional nice-to-have keywords

**Exits:** `sys.exit(1)` if baselines file not found or required fields missing.

---

### Step 2: Send Queries

#### `send_query(api_url: str, query: str) -> dict`

Sends a single query to `POST /api/query`.

**Parameters:**
- `api_url` (`str`): Base URL (e.g., `http://localhost:3000`)
- `query` (`str`): Query text

**Returns:** Dictionary with:

| Key | Type | Description |
|-----|------|-------------|
| `response` | `dict \| None` | Parsed JSON response body |
| `latency_ms` | `int` | Client-side latency in milliseconds |
| `status_code` | `int` | HTTP status code (0 for connection errors) |
| `error` | `str \| None` | Error message if request failed |

**Error handling:**
- `ConnectionError`: Returns error `"Connection refused - backend not running on {api_url}"`
- `Timeout`: Returns error `"Timeout after {REQUEST_TIMEOUT}s"`
- `429`: Returns status 429 for retry handling by caller
- Non-200: Returns truncated response body (first 200 chars)

---

#### `run_all_queries(baselines: list, api_url: str, delay: int, start_from: str = "Q-01") -> list`

Sends all queries sequentially with delay between each.

**Parameters:**
- `baselines` (`list`): List of baseline query dicts
- `api_url` (`str`): API base URL
- `delay` (`int`): Seconds between queries
- `start_from` (`str`): Query ID to resume from (default `"Q-01"`)

**Returns:** List of result dicts, each containing:

| Key | Type | Description |
|-----|------|-------------|
| `id` | `str` | Query ID |
| `category` | `str` | Query category |
| `query` | `str` | Query text |
| `is_oos` | `bool` | Out-of-scope flag |
| `response` | `dict \| None` | API response body |
| `checks` | `dict` | Results of all 6 checks |
| `overall_pass` | `bool` | True if all applicable checks pass |
| `client_latency_ms` | `int` | Client-side latency |
| `error` | `str \| None` | Error message if failed |

**Retry logic:** On 429 status, retries up to `MAX_RETRIES` times with exponential backoff (`delay * 2^retry`).

**Early termination:** If a `ConnectionError` occurs (backend not running), saves partial results and returns immediately.

---

### Step 3: Automated Checks

Each check function evaluates one aspect of the API response against the baseline.

#### `check_must_contain(answer: str, keywords: list) -> dict`

Checks if the answer contains all required keywords (case-insensitive).

**Parameters:**
- `answer` (`str`): The LLM-generated answer text
- `keywords` (`list[str]`): Required keywords from baseline

**Returns:**
```python
{
    "pass": bool,       # True if all keywords found
    "total": int,       # Total keywords to check
    "matched": int,     # Number found
    "missing": list,    # Keywords not found
}
```

---

#### `check_must_not_contain(answer: str, keywords: list) -> dict`

Checks if the answer does NOT contain hallucination signal keywords (case-insensitive).

**Parameters:**
- `answer` (`str`): The LLM-generated answer text
- `keywords` (`list[str]`): Hallucination signal keywords from baseline

**Returns:**
```python
{
    "pass": bool,       # True if no keywords found
    "found": list,      # Keywords that were found (hallucinations)
}
```

---

#### `check_expected_docs(related_docs: list, expected: list) -> dict`

Checks if at least one expected document appears in `relatedDocs` from the API response.

**Parameters:**
- `related_docs` (`list[dict]`): The `relatedDocs` array from API response (each with `docId` key)
- `expected` (`list[str]`): Expected doc_id substrings from baseline

**Returns:**
```python
{
    "pass": bool,       # True if at least one match
    "expected": list,   # Expected patterns
    "found": list,      # Matched patterns
}
```

**Matching:** Case-insensitive substring match of expected patterns against `docId` values.

---

#### `check_citation_present(sources: list, citations: list, chunks_retrieved: int = -1) -> dict`

Checks if at least one source or citation is present in the response.

**Parameters:**
- `sources` (`list`): The `sources` array from API response
- `citations` (`list`): The `citations` array from API response
- `chunks_retrieved` (`int`): Number of chunks retrieved (from `metadata.chunksRetrieved`)

**Returns:**
```python
{
    "pass": bool,           # True if sources or citations present
    "applicable": bool,     # False when chunks_retrieved == 0
    "source_count": int,    # Number of sources
    "citation_count": int,  # Number of citations
    "reason": str,          # Only when not applicable
}
```

**Special case:** When `chunks_retrieved == 0`, the check is marked as `applicable: False` with `pass: True`. This handles queries where the system correctly declines and cannot cite nonexistent sources. These queries are excluded from the adjusted citation accuracy metric.

---

#### `check_oos_handling(answer: str, is_oos: bool, decline_signals: list) -> dict`

For out-of-scope queries, checks if at least one decline signal appears in the answer.

**Parameters:**
- `answer` (`str`): The LLM-generated answer text
- `is_oos` (`bool`): Whether the query is out-of-scope
- `decline_signals` (`list[str]`): Expected decline phrases from baseline

**Returns:**
```python
{
    "pass": bool,              # True if decline signal found (or not OOS)
    "applicable": bool,        # True only for OOS queries
    "signals_found": list,     # Matched decline signals
}
```

**Non-OOS queries:** Returns `pass: True, applicable: False` -- the check does not apply.

---

#### `check_latency(latency_ms: int) -> dict`

Checks if response time is under the 5000ms threshold.

**Parameters:**
- `latency_ms` (`int`): Server-side latency in milliseconds

**Returns:**
```python
{
    "pass": bool,            # True if latency < 5000ms
    "latency_ms": int,       # Actual latency
    "threshold_ms": int,     # 5000
}
```

---

#### `run_checks(baseline: dict, result: dict) -> dict`

Runs all 6 checks on a single query result.

**Parameters:**
- `baseline` (`dict`): Baseline query dict
- `result` (`dict`): Return value from `send_query()`

**Returns:** Dictionary with keys: `must_contain`, `must_not_contain`, `expected_docs`, `citation_present`, `oos_handling`, `latency`. Each value is the return dict from the respective check function.

**Error handling:** If `result["error"]` is set (query failed), returns all checks as failed.

---

### Step 4: Aggregate Metrics

#### `calculate_metrics(results: list) -> dict`

Calculates aggregate metrics from all query results.

**Parameters:**
- `results` (`list`): List of result dicts from `run_all_queries()`

**Returns:** Dictionary with:

| Key | Type | Description |
|-----|------|-------------|
| `deflection_rate` | `float` | % of in-scope queries with all must_contain passing |
| `citation_accuracy` | `float` | % of applicable in-scope queries with citations (adjusted) |
| `citation_accuracy_raw` | `float` | % of all in-scope queries with citations (unadjusted) |
| `citation_applicable_queries` | `int` | In-scope queries where citation check applies |
| `citation_na_queries` | `int` | In-scope queries with 0 chunks (citation N/A) |
| `hallucination_rate` | `float` | % of successful queries with must_not_contain failure |
| `oos_handling_rate` | `float` | % of OOS queries with decline signals |
| `avg_latency_ms` | `float` | Average server-side latency |
| `latency_under_5s` | `float` | % of queries under 5000ms |
| `total_queries` | `int` | Total queries run |
| `successful_queries` | `int` | Queries without errors |
| `failed_queries` | `int` | Queries with errors |
| `in_scope_queries` | `int` | Non-OOS successful queries |
| `oos_queries` | `int` | OOS successful queries |
| `by_category` | `dict` | Per-category breakdown (see below) |

**Per-category breakdown** (`by_category[cat]`):

| Key | Type |
|-----|------|
| `total` | `int` |
| `in_scope` | `int` |
| `oos` | `int` |
| `citation_applicable` | `int` |
| `deflection_rate` | `float` |
| `citation_accuracy` | `float` |
| `hallucination_rate` | `float` |
| `avg_latency_ms` | `float` |

Categories: `booking`, `customs`, `carrier`, `sla`, `edge_case`.

---

### Step 5: Output Files

#### `write_results_json(results: list, metrics: dict, config: dict) -> str`

Writes `data/evaluation_results.json`.

**Parameters:**
- `results` (`list`): Full results list
- `metrics` (`dict`): Aggregate metrics
- `config` (`dict`): Run configuration (delay, api_url, start_from, version)

**Returns:** Run ID string in format `eval-YYYY-MM-DDTHH-MM-SS`.

**Output structure:**
```json
{
  "run_id": "eval-2026-02-10T14-30-00",
  "timestamp": "2026-02-10T14:30:00+00:00",
  "config": { ... },
  "metrics": { ... },
  "results": [ ... ]
}
```

---

#### `write_results_csv(results: list)`

Writes `data/evaluation_results.csv`.

**CSV columns:**
`id`, `category`, `query`, `is_oos`, `confidence`, `must_contain_pass`, `must_contain_matched`, `must_contain_total`, `must_not_contain_pass`, `expected_docs_pass`, `citation_present`, `citation_applicable`, `oos_handling_pass`, `latency_ms`, `overall_pass`, `error`

The `citation_applicable` column distinguishes genuine citation failures from N/A queries (0 chunks retrieved).

---

#### `write_report_md(results: list, metrics: dict, run_id: str)`

Writes `reports/evaluation_report.md`.

**Report sections:**
1. Header with date, run ID, query counts
2. Aggregate Metrics table (result vs. target with PASS/FAIL status)
3. Per-Category Breakdown table
4. must_contain Failures table (in-scope only)
5. Hallucination Detections table
6. OOS Handling Failures table
7. Citation N/A table (0-chunk queries)
8. Citation Missing table (has chunks but no citation)
9. Raw Query Results table (all 50 queries)

---

### Main Entry Point

#### `main()`

CLI entry point. Orchestrates the full evaluation run.

**Flow:**
1. Parse CLI arguments
2. Load and validate baselines (50 queries)
3. If `--dry-run`: validate baselines and print statistics, then exit
4. Send all queries with delay between each
5. Calculate aggregate metrics
6. Write JSON, CSV, and markdown report files
7. Print evaluation summary

---

## Usage Examples

```bash
# Full evaluation run (30s delay between queries)
python scripts/evaluation_harness.py

# Faster run (10s delay)
python scripts/evaluation_harness.py --delay 10

# Resume from query Q-15
python scripts/evaluation_harness.py --start-from Q-15

# Dry run -- validate baselines without sending queries
python scripts/evaluation_harness.py --dry-run

# Custom API URL
python scripts/evaluation_harness.py --api-url http://localhost:4000

# Override delay via environment variable
set EVAL_DELAY_SECONDS=5
python scripts/evaluation_harness.py
```

### Expected Output

```
============================================================
  Waypoint Co-Pilot - Evaluation Harness
============================================================
  API:    http://localhost:3000
  Delay:  30s between queries
  Start:  Q-01
  Mode:   LIVE

Loaded 50 baselines (version: 1.0)
  40 in-scope, 10 out-of-scope

  Estimated run time: ~25m 0s

Sending queries...

  [01/50] Q-01: "What documents are needed for sea freight Singap..." (1523ms) [high] PASS
  [02/50] Q-02: "How far in advance should I book an LCL shipmen..." (1201ms) [high] PASS
  ...

Writing output files...
  JSON: data/evaluation_results.json
  CSV:  data/evaluation_results.csv
  Report: reports/evaluation_report.md

============================================================
  EVALUATION SUMMARY
============================================================
  Queries:         50/50 successful
  Deflection Rate: 72.5% (target: >= 40.0%)
  Citation Acc:    87.5% (target: >= 80.0%)
  Hallucination:   4.0% (target: < 15.0%)
  OOS Handling:    90.0% (target: >= 90.0%)
  Avg Latency:     1842ms (target: < 5000ms)
============================================================
```
