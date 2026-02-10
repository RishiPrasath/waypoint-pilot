# End-to-End Testing Approach

## Framework Status

No dedicated E2E test framework (Vitest, Cypress, Playwright) is configured in this project. This is a deliberate POC-scoped decision -- the 30-day timeline prioritized functional coverage over browser automation infrastructure.

## Verification Methods

### 1. Build Verification

```bash
cd pilot_phase1_poc/05_evaluation/client
npm run build
```

The React frontend is verified through clean Vite production builds. A successful build with zero warnings or errors confirms:
- All component imports resolve
- TypeScript/JSX compilation succeeds
- Tailwind CSS classes are valid
- No circular dependencies

### 2. Visual Verification via Chrome DevTools MCP

During Task T2.10 (UX implementation), the Chrome DevTools MCP tool was used for interactive visual verification:
- Page snapshot inspection (accessibility tree)
- Element interaction testing (click, type, hover)
- Layout verification at different viewport sizes
- Network request monitoring for API calls

This approach provides real-browser verification without the overhead of maintaining a Playwright/Cypress test suite.

### 3. Evaluation Harness (Functional E2E)

The `evaluation_harness.py` script serves as the primary functional E2E test mechanism. It exercises the full pipeline end-to-end:

**Location**: `pilot_phase1_poc/05_evaluation/scripts/evaluation_harness.py`

**What it does**:
1. Sends 50 real queries to the live Express API (`POST /api/query`)
2. Receives full pipeline responses (retrieval + LLM generation + citation extraction)
3. Validates responses against baseline expectations
4. Measures latency per query (target: < 5s average)
5. Generates evaluation reports (JSON, CSV, Markdown)

**Usage**:
```bash
cd pilot_phase1_poc/05_evaluation

# Full run (50 queries with 30s delay between each)
python scripts/evaluation_harness.py

# Custom delay
python scripts/evaluation_harness.py --delay 10

# Resume from a specific query
python scripts/evaluation_harness.py --start-from Q-15

# Dry run (no API calls)
python scripts/evaluation_harness.py --dry-run
```

**Configuration**:
- `EVAL_DELAY_SECONDS` env var (default: 30) -- delay between queries to respect Groq rate limits
- `EVAL_API_URL` env var (default: `http://localhost:3000`) -- API base URL
- `REQUEST_TIMEOUT`: 30 seconds per request
- `MAX_RETRIES`: 3 attempts per query

**Output files**:
- `data/evaluation_results.json` -- raw results
- `data/evaluation_results.csv` -- tabular results
- `reports/evaluation_report.md` -- formatted report

**Metrics evaluated**:
| Metric | Target | Description |
|--------|--------|-------------|
| Deflection Rate | >= 40% | Percentage of queries deflected to human agents |
| Citation Accuracy | >= 80% | Percentage of citations that match KB documents |
| Hallucination Rate | < 15% | Percentage of responses with fabricated information |
| OOS Handling | >= 90% | Percentage of out-of-scope queries correctly identified |
| Avg Latency | < 5s | Average end-to-end response time |

### 4. E2E Node Test Utilities

**Location**: `pilot_phase1_poc/05_evaluation/tests/e2e_node/`

Python-based E2E test utilities for running integration tests against the live Node.js API:

- `test_runner.py` -- orchestrates test execution against the API
- `test_config.py` -- API endpoint configuration
- `test_data.py` -- test query data and expected results

## What Is NOT Covered

- **Browser interaction tests**: No automated click/type/navigate tests for the React frontend
- **Cross-browser testing**: Only Chrome verified (via DevTools MCP)
- **Responsive testing**: Manual verification only, no automated viewport tests
- **Accessibility testing**: No automated a11y checks (axe-core, Lighthouse)
- **Performance testing**: No load testing or stress testing (single-user POC)

## Rationale

For a 30-day POC with a single-user demo target, the combination of:
1. Comprehensive unit tests (217 across Jest + pytest)
2. Build verification (Vite production build)
3. Evaluation harness (50-query functional E2E)
4. Chrome DevTools MCP (interactive visual verification)

provides sufficient confidence without the setup and maintenance cost of a full E2E framework. A production system would add Playwright or Cypress for browser automation.
