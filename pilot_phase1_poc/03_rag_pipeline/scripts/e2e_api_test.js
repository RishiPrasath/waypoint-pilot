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
    query: 'What are the transit times for Maersk shipping?',
    expectCitations: true,
  },
  {
    id: 5,
    category: 'carrier',
    query: 'Does PIL offer reefer container services?',
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
    query: 'What are Incoterms and how do they work?',
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
