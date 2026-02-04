# Task 8.1: Create E2E Test Suite

## Persona
You are a QA automation engineer creating a comprehensive end-to-end test suite for the Waypoint RAG pipeline. You focus on testing real-world scenarios, edge cases, and system resilience.

## Context

### Project State
- **Backend**: Express API at `http://localhost:3000`
- **Frontend**: React UI at `http://localhost:5173`
- **API Endpoint**: `POST /api/query` accepts `{ "query": "..." }`
- **Health Check**: `GET /api/health`

### API Response Format
```json
{
  "answer": "Response text...",
  "citations": [
    {
      "title": "Document Title",
      "section": "Section Name",
      "matched": true,
      "sourceUrls": ["https://..."]
    }
  ],
  "confidence": {
    "level": "High|Medium|Low",
    "reason": "Explanation"
  },
  "metadata": {
    "chunksRetrieved": 10,
    "chunksUsed": 4,
    "latency": { "totalMs": 2340 }
  }
}
```

### Knowledge Base Categories
- **Regulatory**: Singapore Customs, ASEAN trade, GST, HS codes
- **Carriers**: Maersk, PIL, ocean/air services
- **Reference**: Incoterms, documentation guides
- **Internal**: SLA policies, procedures

### References
- Roadmap: `docs/01_implementation_roadmap.md` (Task 8.1)
- Use Cases: `00_docs/02_use_cases.md`
- Task 6.3 Report: `prompts/06_6.3_e2e_api_test/REPORT.md`

### Dependencies
- ✅ Task 7.2: UI Polish & Testing (Complete)
- ✅ Task 6.3: E2E API Test (Complete)

## Task

### Objective
Create a comprehensive Python-based E2E test suite that validates the RAG pipeline across multiple scenarios, measures quality metrics, and generates a detailed report.

### Requirements

#### 1. Test File Structure
```
03_rag_pipeline/
├── scripts/
│   └── e2e_test_suite.py    # Main test script
├── tests/
│   └── e2e/
│       ├── __init__.py
│       ├── test_config.py   # Test configuration
│       ├── test_data.py     # Test queries and expected behaviors
│       └── test_runner.py   # Test execution utilities
└── reports/
    └── e2e_test_report.md   # Generated report
```

#### 2. Test Categories

**Category A: Happy Path (10 queries)**
Factual queries that should return good answers with citations.

| # | Query | Expected |
|---|-------|----------|
| 1 | What documents are needed for FCL export from Singapore to Jakarta? | Answer with export docs, citations |
| 2 | What is the current GST rate for imports into Singapore? | 9% GST, regulatory citation |
| 3 | What's the difference between CIF and CFR Incoterms? | Incoterms explanation |
| 4 | How do I find the right HS code for my product? | HS code guidance |
| 5 | Does my shipment to Thailand qualify for ATIGA rates? | ATIGA/Form D info |
| 6 | What's Maersk's service coverage in Southeast Asia? | Carrier info |
| 7 | What permits are needed for food imports to Indonesia? | BPOM, regulatory info |
| 8 | What is the difference between Form D and Form E? | Certificate of Origin |
| 9 | What are the reefer container options available? | Carrier/equipment info |
| 10 | How does the Major Exporter Scheme work? | MES explanation |

**Category B: Multi-Source (5 queries)**
Queries requiring information from multiple documents.

| # | Query | Expected Sources |
|---|-------|------------------|
| 1 | Compare FCL vs LCL for shipping to Malaysia | Carrier + procedures |
| 2 | What documents and permits for electronics export to Indonesia? | Customs + INSW |
| 3 | Explain customs clearance process with GST implications | Customs + GST guide |
| 4 | What carriers offer temperature-controlled shipping to Vietnam? | Multiple carriers |
| 5 | Full process for ATIGA preferential tariff application | CO guide + customs |

**Category C: Out-of-Scope (5 queries)**
Queries the system should gracefully decline.

| # | Query | Expected Behavior |
|---|-------|-------------------|
| 1 | What is the stock price of Maersk today? | Decline - live data |
| 2 | Book a shipment for me to Jakarta | Decline - action request |
| 3 | What's the weather in Singapore? | Decline - unrelated |
| 4 | Track my shipment BL12345 | Decline - live tracking |
| 5 | What are your competitor's rates? | Decline - no info |

**Category D: Edge Cases (5 queries)**

| # | Query | Test Purpose |
|---|-------|--------------|
| 1 | "" (empty) | Should reject/handle |
| 2 | "a" (single char) | Minimal input |
| 3 | Very long query (500+ chars) | Length handling |
| 4 | Query with special chars: "什么是GST? €£¥" | Unicode handling |
| 5 | "SELECT * FROM users; DROP TABLE" | Injection attempt |

**Category E: Concurrent Requests (3 queries)**
Submit 3 queries simultaneously to test concurrency.

**Category F: Error Recovery (2 scenarios)**
| Scenario | How to Test |
|----------|-------------|
| API timeout | Set very short timeout |
| Malformed request | Send invalid JSON |

#### 3. Test Metrics to Capture

For each query:
- Response time (ms)
- Response received (boolean)
- Has answer (boolean)
- Answer length (chars)
- Citation count
- Matched citations count
- Confidence level
- Error message (if any)

Aggregate metrics:
- Pass rate per category
- Average response time
- P95 response time
- Total citations generated
- Confidence distribution

#### 4. Pass/Fail Criteria

| Category | Pass Criteria |
|----------|---------------|
| Happy Path | Response with answer, latency < 10s |
| Multi-Source | Response with answer |
| Out-of-Scope | Graceful decline (no hallucination) |
| Edge Cases | No crash, appropriate error handling |
| Concurrent | All 3 complete successfully |
| Error Recovery | Graceful error message |

#### 5. Report Format

Generate `reports/e2e_test_report.md`:
```markdown
# E2E Test Suite Report

**Date**: YYYY-MM-DD HH:MM
**Duration**: X seconds
**API Endpoint**: http://localhost:3000/api/query

## Summary

| Category | Total | Passed | Failed | Pass Rate |
|----------|-------|--------|--------|-----------|
| Happy Path | 10 | X | Y | XX% |
| Multi-Source | 5 | X | Y | XX% |
| Out-of-Scope | 5 | X | Y | XX% |
| Edge Cases | 5 | X | Y | XX% |
| Concurrent | 3 | X | Y | XX% |
| Error Recovery | 2 | X | Y | XX% |
| **TOTAL** | 30 | X | Y | **XX%** |

## Performance

| Metric | Value |
|--------|-------|
| Min Latency | XXX ms |
| Max Latency | XXX ms |
| Avg Latency | XXX ms |
| P95 Latency | XXX ms |

## Detailed Results

### Category A: Happy Path
| # | Query | Status | Latency | Citations | Confidence |
|---|-------|--------|---------|-----------|------------|
...

### Failed Tests
[Details of any failures]

## Recommendations
[Based on test results]
```

### Constraints
- Python script (no additional test framework required, just requests)
- Must run against live API (not mocked)
- Should complete in < 5 minutes
- Generate markdown report automatically
- Handle network errors gracefully

### Acceptance Criteria
- [ ] Script runs without errors
- [ ] All 30 test cases execute
- [ ] Happy path pass rate ≥ 80%
- [ ] Out-of-scope queries don't hallucinate
- [ ] Edge cases don't crash the system
- [ ] Concurrent requests all complete
- [ ] Report generated with all metrics
- [ ] Latency metrics captured

## Format

### Code Style
- Python 3.11+ compatible
- Type hints for functions
- Docstrings for main functions
- Clear section comments

### Validation Commands
```bash
# Ensure backend is running
curl http://localhost:3000/api/health

# Run test suite
cd pilot_phase1_poc/03_rag_pipeline
python scripts/e2e_test_suite.py

# View report
cat reports/e2e_test_report.md
```

### Output
1. `scripts/e2e_test_suite.py` - Main test script
2. `reports/e2e_test_report.md` - Generated report
3. Console output showing progress and summary
