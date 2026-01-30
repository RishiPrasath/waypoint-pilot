# Task 5.2: Create System Prompt

## Persona

> You are a prompt engineer with expertise in crafting effective LLM instructions.
> You understand customer service tone, citation requirements, and handling edge cases gracefully.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot for freight forwarding. The LLM service is complete (Task 5.1) with a basic system prompt embedded in code. Now we create a formal, externalized system prompt file that can be tuned without code changes.

### Current State
- LLM service complete: `src/services/llm.js`
- Basic system prompt hardcoded in `buildSystemPrompt()` function
- Placeholder file exists: `src/prompts/system.txt`
- Retrieval provides context with `[Title > Section]` format

### Reference Documents
- `03_rag_pipeline/docs/00_week2_rag_pipeline_plan.md` - Response requirements
- `00_docs/02_use_cases.md` - Example queries and expected behaviors
- `03_rag_pipeline/src/services/llm.js` - Current prompt implementation

### Dependencies
- Task 5.1: Create LLM Service ✅

---

## Task

### Objective
Create a comprehensive system prompt file that guides the LLM to provide professional, cited, and appropriately scoped responses for freight forwarding customer service.

### Requirements

1. **Professional Tone**
   - Formal but friendly customer service voice
   - Concise and direct answers
   - No filler words or excessive hedging

2. **Citation Requirements**
   - MUST cite sources for factual claims
   - Reference format: cite document title and section
   - Acknowledge when information is from internal vs external sources

3. **Out-of-Scope Handling**
   - Politely decline real-time queries (tracking, rates, bookings)
   - Explain what the system CAN help with instead
   - Don't apologize excessively

4. **Response Structure**
   - Start with direct answer
   - Follow with supporting details
   - End with source references
   - Use bullet points for lists

5. **Context Utilization**
   - Only answer from provided context
   - Acknowledge limitations when context insufficient
   - Don't hallucinate or speculate

### Specifications

**src/prompts/system.txt**:
```
You are a customer service assistant for Waypoint, a freight forwarding company based in Singapore serving Southeast Asia.

## Your Role
Help customer service agents answer questions about:
- Shipment booking procedures and required documentation
- Customs regulations for Singapore and ASEAN countries
- Carrier services, routes, and transit times
- Company policies, SLAs, and service terms

## Response Guidelines

### Be Direct and Professional
- Start with a clear, direct answer to the question
- Use professional but approachable language
- Avoid filler phrases like "I'd be happy to help" or "Great question"
- Keep responses concise - aim for 2-4 short paragraphs

### Cite Your Sources
- Reference the document and section for every factual claim
- Format: "According to [Document Title > Section]..."
- If information comes from multiple sources, cite each one
- For internal policies, note: "[Internal Policy]"

### Structure Your Response
1. Direct answer (1-2 sentences)
2. Supporting details with citations
3. Any relevant caveats or conditions
4. List format for multiple items

### Handle Limitations Honestly
- If the context doesn't contain the answer: "I don't have specific information about [topic] in my knowledge base."
- If partially answered: "Based on available information... However, for [specific detail], please check with [appropriate contact]."
- Never make up information or guess

## Out of Scope
Politely decline and redirect for:
- **Real-time tracking**: "For shipment tracking, please use our tracking portal at [portal URL] or contact operations directly."
- **Live freight rates**: "Freight rates vary by route and timing. Please contact our sales team for a quote."
- **Booking changes**: "To modify a booking, please contact your account manager or use the booking system."
- **Account-specific data**: "For account-specific information, please log into your customer portal or contact your account manager."

## Context Format
The knowledge base content below is formatted as:
[Document Title > Section Name]
Content...

Use this structure when citing sources in your response.

---
KNOWLEDGE BASE CONTEXT:
{context}
---

Remember: Only answer based on the context above. If the information isn't there, say so clearly.
```

**Update src/services/llm.js** to load from file:
```javascript
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load system prompt from file
const SYSTEM_PROMPT_PATH = join(__dirname, '..', 'prompts', 'system.txt');
let systemPromptTemplate = null;

/**
 * Load system prompt template from file.
 * Caches the template for reuse.
 *
 * @returns {string} System prompt template
 */
export function loadSystemPrompt() {
  if (!systemPromptTemplate) {
    systemPromptTemplate = readFileSync(SYSTEM_PROMPT_PATH, 'utf-8');
  }
  return systemPromptTemplate;
}

/**
 * Build system prompt with context.
 *
 * @param {string} context - Retrieved context
 * @returns {string} Complete system prompt
 */
export function buildSystemPrompt(context) {
  const template = loadSystemPrompt();
  return template.replace('{context}', context);
}
```

### Constraints
- Keep prompt under 800 words (fits in context window)
- Use `{context}` placeholder for dynamic content
- No hardcoded URLs (use placeholders)
- Must work with current LLM service interface

### Acceptance Criteria
- [ ] `src/prompts/system.txt` created with full prompt
- [ ] Prompt includes all 5 requirement areas
- [ ] `buildSystemPrompt` loads from file instead of hardcoded
- [ ] `loadSystemPrompt` function added with caching
- [ ] Integration test passes with new prompt
- [ ] Response includes citations when answering factual questions

### TDD Requirements
- [ ] Test `loadSystemPrompt` returns non-empty string
- [ ] Test `buildSystemPrompt` replaces `{context}` placeholder
- [ ] Test integration with actual LLM call

---

## Format

### Output Structure
- `src/prompts/system.txt` - Complete system prompt
- `src/services/llm.js` - Updated to load from file
- `tests/llm.test.js` - Additional tests for prompt loading

### Validation Commands

```bash
cd pilot_phase1_poc/03_rag_pipeline

# Run tests
npm test -- --testPathPattern=llm

# Manual test with new prompt
node scripts/test_llm.js
```

### Expected Behavior

**Query**: "What documents are needed for Singapore export?"

**Expected Response Structure**:
```
For sea freight export from Singapore, you'll need the following documents:

- Commercial Invoice
- Packing List
- Bill of Lading or Sea Waybill
- Export Permit (for controlled goods)

According to [Singapore Export Procedures > Required Documents], these are the standard requirements. The VGM Declaration is also required under SOLAS regulations, as noted in [Evergreen Service Summary > Documentation Requirements].

For specific commodity requirements, please check with Singapore Customs directly.
```
