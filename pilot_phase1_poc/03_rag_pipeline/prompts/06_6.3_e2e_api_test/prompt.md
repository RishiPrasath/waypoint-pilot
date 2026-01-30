# Task 6.3: End-to-End API Test

## Persona

> You are a QA engineer with expertise in API testing and end-to-end validation.
> You verify that integrated systems work correctly from user request to final response.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. The Express API (Task 6.2) is complete. Now we need to verify the full pipeline works end-to-end: HTTP request → retrieval → LLM generation → citation extraction → response.

### Current State
- Pipeline orchestrator: `src/services/pipeline.js` - `processQuery()`
- Express API: `src/index.js` - POST /api/query, GET /api/health
- ChromaDB: 483 chunks from 29 documents
- LLM: Groq API (llama-3.1-8b-instant)
- Unit tests: 105 passing

### Reference Documents
- `03_rag_pipeline/docs/00_week2_rag_pipeline_plan.md` - API specifications
- `00_docs/02_use_cases.md` - Test queries and expected behaviors
- `prompts/06_6.2_express_api/REPORT.md` - API implementation details

### Dependencies
- Task 6.2: Create Express API ✅
- Valid GROQ_API_KEY in `.env`

---

## Task

### Objective
Run end-to-end tests against the live API to verify the complete RAG pipeline works correctly, with proper response structure, citations, and acceptable latency.

### Requirements

1. **Create E2E test script**
   - File: `scripts/e2e_api_test.js`
   - Run 10 diverse queries against POST /api/query
   - Measure response time for each
   - Validate response structure
   - Check for citations presence
   - Generate summary report

2. **Test query categories** (10 queries total)
   - 3x Regulatory/Customs queries
   - 2x Carrier information queries
   - 2x Documentation/booking queries
   - 2x Internal policy queries
   - 1x Edge case (out-of-scope)

3. **Validation criteria per response**
   - Has `answer` field (non-empty string)
   - Has `citations` array
   - Has `confidence` object with `level` and `reason`
   - Has `metadata` object with latency info
   - Response time < 5000ms

4. **Generate test report**
   - Pass/fail for each query
   - Latency breakdown
   - Citation counts
   - Any errors encountered
   - Overall pass rate

### Specifications

**scripts/e2e_api_test.js**:
```javascript
/**
 * End-to-End API Test Script
 * Tests the complete RAG pipeline via HTTP requests.
 */

const BASE_URL = 'http://localhost:3000';

// Test queries covering different categories
const TEST_QUERIES = [
  // Regulatory/Customs (3)
  {
    id: 1,
    category: 'regulatory',
    query: 'What documents are required for exporting goods from Singapore?',
    expectCitations: true,
  },
  {
    id: 2,
    category: 'regulatory',
    query: 'What are the HS code classification rules for electronics?',
    expectCitations: true,
  },
  {
    id: 3,
    category: 'regulatory',
    query: 'What is the GST rate for imported goods in Singapore?',
    expectCitations: true,
  },
  // Carrier information (2)
  {
    id: 4,
    category: 'carrier',
    query: 'What are the transit times for Maersk shipping to Europe?',
    expectCitations: true,
  },
  {
    id: 5,
    category: 'carrier',
    query: 'What container types does Hapag-Lloyd offer?',
    expectCitations: true,
  },
  // Documentation/booking (2)
  {
    id: 6,
    category: 'documentation',
    query: 'What is the process for booking a sea freight shipment?',
    expectCitations: true,
  },
  {
    id: 7,
    category: 'documentation',
    query: 'What are the required fields for a commercial invoice?',
    expectCitations: true,
  },
  // Internal policy (2)
  {
    id: 8,
    category: 'internal',
    query: 'What is the SLA for customer query response times?',
    expectCitations: true,
  },
  {
    id: 9,
    category: 'internal',
    query: 'What is the escalation procedure for urgent shipments?',
    expectCitations: true,
  },
  // Edge case (1)
  {
    id: 10,
    category: 'edge',
    query: 'What is the current stock price of Maersk?',
    expectCitations: false, // Out of scope
  },
];

/**
 * Validate response structure
 */
function validateResponse(response) {
  const errors = [];

  if (!response.answer || typeof response.answer !== 'string') {
    errors.push('Missing or invalid answer field');
  }

  if (!Array.isArray(response.citations)) {
    errors.push('Missing citations array');
  }

  if (!response.confidence || !response.confidence.level) {
    errors.push('Missing confidence object');
  }

  if (!response.metadata) {
    errors.push('Missing metadata object');
  }

  return errors;
}

/**
 * Run a single test query
 */
async function runTest(testCase) {
  const startTime = Date.now();

  try {
    const response = await fetch(`${BASE_URL}/api/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: testCase.query }),
    });

    const latencyMs = Date.now() - startTime;
    const data = await response.json();

    if (!response.ok) {
      return {
        ...testCase,
        passed: false,
        latencyMs,
        error: `HTTP ${response.status}: ${data.message || 'Unknown error'}`,
      };
    }

    const validationErrors = validateResponse(data);
    const hasCitations = data.citations && data.citations.length > 0;
    const latencyOk = latencyMs < 5000;

    const passed = validationErrors.length === 0 && latencyOk;

    return {
      ...testCase,
      passed,
      latencyMs,
      citationCount: data.citations?.length || 0,
      confidence: data.confidence?.level,
      validationErrors,
      hasCitations,
      latencyOk,
      answerPreview: data.answer?.substring(0, 100) + '...',
    };

  } catch (error) {
    return {
      ...testCase,
      passed: false,
      latencyMs: Date.now() - startTime,
      error: error.message,
    };
  }
}

/**
 * Check API health before running tests
 */
async function checkHealth() {
  try {
    const response = await fetch(`${BASE_URL}/api/health`);
    const data = await response.json();
    return data.status === 'ok';
  } catch {
    return false;
  }
}

/**
 * Main test runner
 */
async function runAllTests() {
  console.log('╔════════════════════════════════════════════════╗');
  console.log('║     Waypoint RAG Pipeline - E2E API Test       ║');
  console.log('╚════════════════════════════════════════════════╝\n');

  // Health check
  console.log('Checking API health...');
  const healthy = await checkHealth();
  if (!healthy) {
    console.error('❌ API is not healthy. Start the server with: npm start');
    process.exit(1);
  }
  console.log('✅ API is healthy\n');

  // Run tests
  console.log(`Running ${TEST_QUERIES.length} test queries...\n`);
  console.log('─'.repeat(60));

  const results = [];
  for (const testCase of TEST_QUERIES) {
    const result = await runTest(testCase);
    results.push(result);

    const status = result.passed ? '✅ PASS' : '❌ FAIL';
    console.log(`\n${status} [${result.category}] Query #${result.id}`);
    console.log(`   Query: "${result.query.substring(0, 50)}..."`);
    console.log(`   Latency: ${result.latencyMs}ms ${result.latencyOk ? '✓' : '⚠ SLOW'}`);

    if (result.error) {
      console.log(`   Error: ${result.error}`);
    } else {
      console.log(`   Citations: ${result.citationCount}, Confidence: ${result.confidence}`);
      if (result.validationErrors.length > 0) {
        console.log(`   Validation: ${result.validationErrors.join(', ')}`);
      }
    }
  }

  // Summary
  console.log('\n' + '─'.repeat(60));
  console.log('\n📊 TEST SUMMARY\n');

  const passed = results.filter(r => r.passed).length;
  const failed = results.filter(r => !r.passed).length;
  const avgLatency = Math.round(results.reduce((sum, r) => sum + r.latencyMs, 0) / results.length);
  const maxLatency = Math.max(...results.map(r => r.latencyMs));
  const minLatency = Math.min(...results.map(r => r.latencyMs));
  const withCitations = results.filter(r => r.hasCitations).length;

  console.log(`Total:      ${results.length} tests`);
  console.log(`Passed:     ${passed} (${Math.round(passed/results.length*100)}%)`);
  console.log(`Failed:     ${failed}`);
  console.log(`Avg Latency: ${avgLatency}ms`);
  console.log(`Min/Max:    ${minLatency}ms / ${maxLatency}ms`);
  console.log(`With Citations: ${withCitations}/${results.length}`);

  // Pass/fail criteria
  const passRate = passed / results.length;
  const overallPass = passRate >= 0.8 && avgLatency < 5000;

  console.log('\n' + '═'.repeat(60));
  if (overallPass) {
    console.log('✅ E2E TEST SUITE PASSED');
  } else {
    console.log('❌ E2E TEST SUITE FAILED');
    if (passRate < 0.8) console.log(`   - Pass rate ${Math.round(passRate*100)}% < 80% required`);
    if (avgLatency >= 5000) console.log(`   - Avg latency ${avgLatency}ms >= 5000ms limit`);
  }
  console.log('═'.repeat(60));

  // Return results for programmatic use
  return {
    total: results.length,
    passed,
    failed,
    passRate,
    avgLatency,
    maxLatency,
    minLatency,
    withCitations,
    overallPass,
    results,
  };
}

// Run if executed directly
runAllTests().catch(console.error);
```

### Constraints
- Must test against live API (not mocked)
- Requires valid GROQ_API_KEY
- Server must be running on port 3000
- Each query should complete in <5s
- At least 80% of tests should pass

### Acceptance Criteria
- [ ] E2E test script created at `scripts/e2e_api_test.js`
- [ ] 10 diverse queries tested
- [ ] Response structure validated
- [ ] Citations presence verified
- [ ] Latency <5s for all queries
- [ ] Pass rate ≥80%
- [ ] Test report generated
- [ ] Any issues documented in REPORT.md

---

## Format

### Output Structure
- `scripts/e2e_api_test.js` - E2E test script
- `prompts/06_6.3_e2e_api_test/REPORT.md` - Test results and findings

### Validation Commands

```bash
cd pilot_phase1_poc/03_rag_pipeline

# Terminal 1: Start the server
npm start

# Terminal 2: Run E2E tests
node scripts/e2e_api_test.js

# Alternative: Single command with background server
npm start & sleep 3 && node scripts/e2e_api_test.js
```

### Expected Output

```
╔════════════════════════════════════════════════╗
║     Waypoint RAG Pipeline - E2E API Test       ║
╚════════════════════════════════════════════════╝

Checking API health...
✅ API is healthy

Running 10 test queries...
────────────────────────────────────────────────────────────

✅ PASS [regulatory] Query #1
   Query: "What documents are required for exporting..."
   Latency: 2340ms ✓
   Citations: 3, Confidence: High

... (more tests) ...

────────────────────────────────────────────────────────────

📊 TEST SUMMARY

Total:      10 tests
Passed:     9 (90%)
Failed:     1
Avg Latency: 2500ms
Min/Max:    1800ms / 3200ms
With Citations: 9/10

════════════════════════════════════════════════════════════
✅ E2E TEST SUITE PASSED
════════════════════════════════════════════════════════════
```

### Report Template

The REPORT.md should include:
1. Test execution summary
2. Individual query results
3. Latency analysis
4. Citation quality observations
5. Any issues or failures encountered
6. Recommendations for improvement
