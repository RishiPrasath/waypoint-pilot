/**
 * Manual integration test for LLM service
 */

import { generateResponse, buildSystemPrompt } from '../src/services/llm.js';

async function main() {
  const query = 'What documents are needed for Singapore export?';
  const context = `[Singapore Export Procedures > Required Documents]
For sea freight export from Singapore, you need:
- Commercial Invoice
- Packing List
- Bill of Lading
- Export Permit (if applicable)

[Evergreen Service Summary > Documentation]
Standard documentation includes commercial invoice and packing list.`;

  console.log('Query:', query);
  console.log('Context length:', context.length, 'chars');
  console.log('---');

  try {
    const startTime = Date.now();
    const response = await generateResponse(query, context);
    const elapsed = Date.now() - startTime;

    console.log('Answer:');
    console.log(response.answer);
    console.log('');
    console.log('Metadata:');
    console.log('- Model:', response.model);
    console.log('- Finish reason:', response.finishReason);
    console.log('- Prompt tokens:', response.usage.promptTokens);
    console.log('- Completion tokens:', response.usage.completionTokens);
    console.log('- Total latency:', elapsed, 'ms');
    console.log('');
    console.log('✅ Integration test passed');
  } catch (error) {
    console.error('❌ Integration test failed:', error.message);
    process.exit(1);
  }
}

main();
