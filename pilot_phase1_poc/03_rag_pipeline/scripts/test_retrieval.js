/**
 * Manual integration test for retrieval service
 */

import { retrieveChunks, formatContext, getMetadataForCitation } from '../src/services/retrieval.js';

async function main() {
  const query = 'What documents are required for Singapore export?';
  console.log('Query:', query);
  console.log('---');

  try {
    const chunks = await retrieveChunks(query);
    console.log('Retrieved:', chunks.length, 'chunks\n');

    if (chunks.length > 0) {
      console.log('Top 3 results:');
      chunks.slice(0, 3).forEach((c, i) => {
        console.log(`${i + 1}. ${c.metadata.title} > ${c.metadata.section || 'N/A'}`);
        console.log(`   Score: ${c.score.toFixed(3)}, Doc ID: ${c.metadata.doc_id}`);
      });
      console.log('');

      console.log('Context preview (first 500 chars):');
      const context = formatContext(chunks);
      console.log(context.substring(0, 500) + '...\n');

      console.log('Citations:');
      const citations = getMetadataForCitation(chunks.slice(0, 3));
      citations.forEach(c => console.log(`- ${c.title}: ${c.sourceUrls[0] || 'Internal'}`));
    }

    console.log('\n✅ Integration test passed');
  } catch (error) {
    console.error('❌ Integration test failed:', error.message);
    process.exit(1);
  }
}

main();
