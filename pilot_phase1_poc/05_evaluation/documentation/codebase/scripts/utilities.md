# Utility Scripts

Layer 3 documentation for `query_chroma.py`, `verify_ingestion.py`, `view_chroma.py`, and `retrieval_quality_test.py`.

---

## query_chroma.py

JSON stdin/stdout bridge that enables the Node.js backend to query ChromaDB via a child process. Reads query parameters as JSON from stdin, returns results as JSON to stdout.

### Functions

#### `query_chroma(query: str, top_k: int = 10, collection_name: str = 'waypoint_kb') -> list[dict]`

Queries ChromaDB and returns results.

**Parameters:**
- `query` (`str`): Search query text
- `top_k` (`int`): Number of results to return (default 10)
- `collection_name` (`str`): ChromaDB collection name (default `"waypoint_kb"`)

**Returns:** List of chunk dictionaries, each containing:

| Key | Type | Description |
|-----|------|-------------|
| `content` | `str` | The chunk text |
| `metadata` | `dict` | All ChromaDB metadata fields |
| `distance` | `float` | ChromaDB distance (lower = more similar) |
| `score` | `float` | Similarity score: `1 - distance` (higher = more similar) |

**ChromaDB path:** Resolved as `Path(__file__).parent.parent / 'chroma_db'` (hardcoded, not from config).

---

#### `main()`

Entry point. Reads JSON from stdin, calls `query_chroma()`, writes JSON to stdout.

**Input JSON schema:**
```json
{
  "query": "string (required)",
  "top_k": 10,
  "collection_name": "waypoint_kb"
}
```

**Success output:**
```json
{
  "success": true,
  "chunks": [
    {
      "content": "...",
      "metadata": { "doc_id": "...", "title": "...", ... },
      "distance": 0.45,
      "score": 0.55
    }
  ],
  "count": 5
}
```

**Error output:**
```json
{
  "success": false,
  "error": "Error message"
}
```

### Usage Examples

```bash
# Basic query
echo '{"query": "Singapore export procedures", "top_k": 5}' | python scripts/query_chroma.py

# Custom collection
echo '{"query": "customs", "top_k": 3, "collection_name": "test_kb"}' | python scripts/query_chroma.py

# From Node.js (conceptual)
# const { spawn } = require('child_process');
# const proc = spawn('python', ['scripts/query_chroma.py']);
# proc.stdin.write(JSON.stringify({ query: "...", top_k: 10 }));
# proc.stdin.end();
```

**Windows note:** Single-quoted JSON in `echo` does not work reliably on Windows cmd. Use inline Python for smoke tests instead:

```bash
python -c "import subprocess, json; p = subprocess.run(['python', 'scripts/query_chroma.py'], input=json.dumps({'query':'test','top_k':3}), capture_output=True, text=True); print(p.stdout)"
```

---

## verify_ingestion.py

Post-ingestion validation script. Runs 6 progressive checks against the ChromaDB collection to verify ingestion quality.

### Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `MIN_CHUNKS` | `680` | Minimum expected chunk count |
| `MAX_CHUNKS` | `740` | Maximum expected chunk count |
| `EXPECTED_CATEGORIES` | `["01_regulatory", "02_carriers", "03_reference", "04_internal_synthetic"]` | Required categories |
| `REQUIRED_METADATA_FIELDS` | 10 fields | See list below |

**Required metadata fields:** `doc_id`, `title`, `source_org`, `source_type`, `jurisdiction`, `category`, `section_header`, `subsection_header`, `chunk_index`, `file_path`

### CLI Interface

```
usage: verify_ingestion.py [-h] [-v] [--tier {1,2,3}] [--check {1,2,3,4,5,6}]

optional arguments:
  -v, --verbose         Show detailed results
  --tier {1,2,3}        Run only specified tier
  --check {1,2,3,4,5,6} Run only specified check
```

### Check Functions

#### `check_total_count(collection, verbose: bool = False) -> tuple[bool, str]`

**Check 1:** Verifies total chunk count is within `MIN_CHUNKS` to `MAX_CHUNKS` range (680-740).

**Returns:** `(passed, message)` -- e.g., `(True, "709 chunks (expected 680-740)")`.

---

#### `check_category_distribution(collection, verbose: bool = False) -> tuple[bool, str]`

**Check 2:** Verifies all 4 expected categories are present in metadata.

**Returns:** `(passed, message)` -- e.g., `(True, "4/4 categories")`.

---

#### `check_metadata_integrity(collection, verbose: bool = False) -> tuple[bool, str]`

**Check 3:** Samples 20 chunks and verifies all 10 required metadata fields are present.

**Returns:** `(passed, message)` -- e.g., `(True, "10/10 fields")` or `(False, "8/10 fields (missing: source_org, jurisdiction)")`.

---

#### `check_tier1_retrieval(collection, verbose: bool = False) -> tuple[bool, str, int, int]`

**Check 4:** Tier 1 category retrieval tests. 8 queries, each checks if the top-1 result has the expected category.

**Test queries:** 2 per category (regulatory, carriers, reference, internal_synthetic).

**Pass criteria:** 8/8 queries must match.

**Returns:** `(passed, message, pass_count, total)` -- e.g., `(True, "8/8", 8, 8)`.

---

#### `check_tier2_retrieval(collection, verbose: bool = False) -> tuple[bool, str, int, int]`

**Check 5:** Tier 2 document retrieval tests. 12 queries, each checks if any of the top-3 results contains an expected doc_id substring.

**Pass criteria:** 10+/12 queries must match.

**Returns:** `(passed, message, pass_count, total)` -- e.g., `(True, "11/12", 11, 12)`.

---

#### `check_tier3_scenarios(collection, verbose: bool = False) -> tuple[bool, str, int, int]`

**Check 6:** Tier 3 keyword matching tests. 10 queries, each checks if at least 2 of 3 expected keywords appear in the combined text of the top-3 results.

**Pass criteria:** 8+/10 queries must match.

**Returns:** `(passed, message, pass_count, total)` -- e.g., `(True, "9/10", 9, 10)`.

---

#### `run_all_checks(collection, args: argparse.Namespace) -> dict`

Orchestrates all checks with filtering based on `--tier` and `--check` arguments.

**Returns:** Dictionary with:

| Key | Type | Description |
|-----|------|-------------|
| `checks` | `list[dict]` | Individual check results |
| `total_passed` | `int` | Total test cases passed |
| `total_tests` | `int` | Total test cases run |
| `passed` | `bool` | True if pass rate >= 93% (28/30) |

---

#### `print_results(results: dict, verbose: bool = False) -> None`

Prints formatted verification results to stdout.

---

#### `main() -> None`

CLI entry point. Initializes ChromaDB, runs checks, prints results, exits with code 0 (pass) or 1 (fail).

### Usage Examples

```bash
# Run all 6 checks
python -m scripts.verify_ingestion

# Verbose output (shows individual query results)
python -m scripts.verify_ingestion --verbose

# Run only Tier 1 retrieval tests
python -m scripts.verify_ingestion --tier 1

# Run only Check 3 (metadata integrity)
python -m scripts.verify_ingestion --check 3
```

### Expected Output

```
==================================================
Waypoint Ingestion Verification
==================================================

[PASS] Check 1: Total count: 709 chunks (expected 680-740)
[PASS] Check 2: Category distribution: 4/4 categories
[PASS] Check 3: Metadata integrity: 10/10 fields
[PASS] Check 4: Tier 1 retrieval: 8/8
[PASS] Check 5: Tier 2 retrieval: 11/12
[PASS] Check 6: Tier 3 scenarios: 9/10

Summary: 29/30 tests passed (97%)
Result: VERIFICATION PASSED
```

---

## view_chroma.py

Debug utility to inspect ChromaDB collection contents. Supports summary view, filtered browsing, semantic search, and JSON export.

### CLI Interface

```
usage: view_chroma.py [-h] [--all] [--limit LIMIT] [--category CATEGORY]
                       [--doc-id DOC_ID] [--search SEARCH] [--export EXPORT]
                       [--no-content]

optional arguments:
  --all                 Show all records
  --limit LIMIT         Limit number of records (default: 10)
  --category CATEGORY   Filter by category (e.g., 01_regulatory)
  --doc-id DOC_ID       Filter by document ID
  --search SEARCH       Semantic search query
  --export EXPORT       Export all records to JSON file
  --no-content          Hide content in output
```

### Functions

#### `get_collection() -> chromadb.Collection`

Initializes and returns the ChromaDB collection using `CHROMA_PERSIST_PATH` and `COLLECTION_NAME` from config.

---

#### `show_summary(collection)`

Shows collection statistics: total chunks, unique documents, unique sources, category distribution, and all document IDs.

---

#### `show_records(collection, limit: int = 10, category: Optional[str] = None, doc_id: Optional[str] = None, show_content: bool = True)`

Shows records with optional filtering by category or doc_id.

**Parameters:**
- `collection`: ChromaDB collection
- `limit` (`int`): Max records to show (default 10). `None` for all.
- `category` (`Optional[str]`): Filter by category value
- `doc_id` (`Optional[str]`): Filter by doc_id value
- `show_content` (`bool`): Show content preview (first 200 chars)

**ChromaDB where clause:** Uses `{"category": category}` or `{"doc_id": doc_id}` for filtering.

---

#### `search_records(collection, query: str, n_results: int = 5)`

Performs semantic similarity search and displays results with similarity scores.

**Parameters:**
- `collection`: ChromaDB collection
- `query` (`str`): Search query text
- `n_results` (`int`): Number of results (default 5)

**Output includes:** Similarity score (`1 - distance`), doc_id, category, title, section header, content preview (300 chars).

---

#### `export_to_json(collection, filepath: str)`

Exports all records (IDs, content, metadata) to a JSON file.

**Parameters:**
- `collection`: ChromaDB collection
- `filepath` (`str`): Output JSON file path

---

#### `main()`

CLI entry point. Dispatches to the appropriate function based on arguments.

**Dispatch logic:**
1. `--export` -> `export_to_json()`
2. `--search` -> `search_records()`
3. `--all`, `--category`, `--doc-id` -> `show_records()`
4. No args -> `show_summary()`

**Windows note:** On Windows, stdout is reconfigured to UTF-8 with `errors='replace'` to handle Unicode content:
```python
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
```

### Usage Examples

```bash
# Show collection summary
python -m scripts.view_chroma

# Show first 10 records
python -m scripts.view_chroma --limit 10

# Show all records (no limit)
python -m scripts.view_chroma --all

# Filter by category
python -m scripts.view_chroma --category 01_regulatory

# Filter by document ID
python -m scripts.view_chroma --doc-id 01_regulatory_sg_import_procedures

# Semantic search
python -m scripts.view_chroma --search "customs import Singapore"

# Export to JSON
python -m scripts.view_chroma --export chroma_export.json

# Browse without content preview
python -m scripts.view_chroma --category 02_carriers --no-content
```

---

## retrieval_quality_test.py

50-query hit rate test against ChromaDB. Checks if expected documents appear in top-k results. Generates per-category and overall hit rate reports with a decision gate.

### Configuration Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `TOP_K` | `5` | Number of results retrieved per query |
| `THRESHOLD` | `0.15` | Similarity threshold for OOS queries |
| `CHROMA_PATH` | `CHROMA_PERSIST_PATH` | From config |

### Test Query Structure

50 queries organized into 5 categories (10 each):
- `booking_documentation` (10 queries)
- `customs_regulatory` (10 queries)
- `carrier_information` (10 queries)
- `sla_service` (10 queries)
- `edge_cases_out_of_scope` (10 queries)

`EXPECTED_SOURCES` maps each query to a list of expected doc_id substrings. Out-of-scope queries have empty expected lists.

### Functions

#### `initialize_chromadb() -> chromadb.Collection`

Initializes ChromaDB persistent client and returns the collection.

---

#### `run_query(collection, query: str, top_k: int = TOP_K) -> list[dict]`

Runs a single query against ChromaDB.

**Parameters:**
- `collection`: ChromaDB collection
- `query` (`str`): Search query text
- `top_k` (`int`): Number of results (default 5)

**Returns:** List of chunk dicts:

| Key | Type | Description |
|-----|------|-------------|
| `chunk_id` | `str` | ChromaDB chunk ID |
| `metadata` | `dict` | Full metadata |
| `text` | `str` | Chunk text (truncated to 200 chars) |
| `similarity` | `float` | `1 - distance`, rounded to 4 decimals |

---

#### `is_hit(chunks: list[dict], expected_keywords: list[str]) -> bool`

Determines if a query is a "hit" -- at least one of the top-3 chunks matches an expected doc_id pattern.

**Parameters:**
- `chunks` (`list[dict]`): Query results
- `expected_keywords` (`list[str]`): Expected doc_id substrings

**Returns:** `True` if any top-3 chunk's doc_id contains an expected keyword (case-insensitive).

**Out-of-scope logic:** If `expected_keywords` is empty (OOS query), considers it a hit if the top result's similarity is below `THRESHOLD` (0.15), meaning the system correctly found no relevant content.

---

#### `get_matching_source(chunk: dict, expected_keywords: list[str]) -> Optional[str]`

Identifies which expected keyword matched a given chunk.

**Parameters:**
- `chunk` (`dict`): A single chunk result
- `expected_keywords` (`list[str]`): Expected doc_id substrings

**Returns:** Matching keyword string, or `None`.

---

#### `run_all_tests(collection) -> dict`

Runs all 50 test queries and collects results.

**Parameters:**
- `collection`: ChromaDB collection

**Returns:** Dictionary with:

| Key | Type | Description |
|-----|------|-------------|
| `timestamp` | `str` | ISO timestamp |
| `config` | `dict` | `top_k`, `threshold`, `chroma_path`, `collection_name` |
| `summary` | `dict` | `total_queries`, `total_hits`, `overall_hit_rate` |
| `category_stats` | `dict` | Per-category: `queries`, `hits`, `hit_rate`, `results` |
| `all_results` | `list` | Per-query results with full details |

**Per-query result fields:**

| Key | Type |
|-----|------|
| `query_num` | `int` |
| `category` | `str` |
| `query` | `str` |
| `top_result_doc_id` | `str` |
| `top_result_title` | `str` |
| `top_score` | `float` |
| `hit` | `bool` |
| `expected_sources` | `list[str]` |
| `matched_source` | `str \| None` |
| `top_5_chunks` | `list[dict]` |

---

#### `determine_decision(overall_hit_rate: float) -> str`

Returns a decision gate recommendation based on hit rate.

| Hit Rate | Decision | Action |
|----------|----------|--------|
| >= 75% | `"PROCEED"` | Build retrieval service |
| 60-74% | `"INVESTIGATE"` | Review failures, minor fixes |
| < 60% | `"REMEDIATE"` | Chunking optimization needed |

---

#### `generate_json_report(results: dict, output_path: Path)`

Saves raw results to JSON at `data/retrieval_test_results.json`.

---

#### `generate_markdown_report(results: dict, output_path: Path)`

Generates human-readable markdown report at `reports/retrieval_quality_REPORT.md`.

**Report sections:**
1. Summary table (per-category hit rates)
2. Decision gate (PROCEED / INVESTIGATE / REMEDIATE)
3. Top 10 failures
4. Per-category details with all query results
5. Full results appendix (truncated JSON)

---

#### `main()`

Entry point. Initializes ChromaDB, runs all tests, generates JSON and markdown reports, prints summary.

### Usage Examples

```bash
# Run all 50 queries
python scripts/retrieval_quality_test.py
```

### Expected Output

```
============================================================
Waypoint Retrieval Quality Test
============================================================

Connected to ChromaDB: C:\...\05_evaluation\chroma_db
Collection: waypoint_kb
Total chunks: 709

Running retrieval quality tests...
Total queries: 50
Top-K: 5, Threshold: 0.15
============================================================

Testing booking_documentation (10 queries)...
  [1/10] "What documents are needed for sea freight..." -> 01_regulatory_sg_export (0.72) PASS
  ...
  Category hit rate: 90.0%

...

============================================================
SUMMARY
============================================================
Total queries: 50
Overall hit rate: 92.0%
Decision: PROCEED

Reports generated:
  - data/retrieval_test_results.json
  - reports/retrieval_quality_REPORT.md
```
