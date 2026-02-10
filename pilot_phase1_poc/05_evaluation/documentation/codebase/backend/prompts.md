# System Prompt Documentation

## Purpose

The system prompt defines the LLM's persona, response guidelines, and behavioral constraints for the Waypoint customer service co-pilot. It is stored as a text file and injected into every LLM request with retrieved context replacing the `{context}` placeholder at runtime.

## File

| File | Purpose |
|------|---------|
| `backend/prompts/system.txt` | System prompt template with `{context}` placeholder |

---

## Runtime Integration

### Loading and Caching

The prompt template is loaded by `llm.js:loadSystemPrompt()`:

```js
function loadSystemPrompt() {
  if (!systemPromptTemplate) {
    systemPromptTemplate = readFileSync(SYSTEM_PROMPT_PATH, 'utf-8');
  }
  return systemPromptTemplate;
}
```

- Read synchronously from disk on first call using `fs.readFileSync`
- Cached in a module-level variable (`systemPromptTemplate`) for all subsequent requests
- Cache can be cleared via `resetSystemPrompt()` (used in tests)

### Context Injection

`buildSystemPrompt(context)` performs a string replacement of the `{context}` placeholder:

```js
function buildSystemPrompt(context) {
  const template = loadSystemPrompt();
  return template.replace('{context}', context);
}
```

The `context` parameter is the formatted chunk string from `retrieval.js:formatContext()`, which uses the format:

```
[Document Title > Section Name]
chunk content here

[Another Document Title]
more content here
```

### Message Assembly

The final messages array sent to Groq:

```js
[
  { role: 'system', content: buildSystemPrompt(context) },
  { role: 'user', content: query }
]
```

---

## Prompt Structure

The system prompt is organized into the following sections:

### 1. Role Definition

Establishes the LLM as a customer service assistant for Waypoint, a freight forwarding company based in Singapore serving Southeast Asia. Defines the scope of knowledge:

- Shipment booking procedures and required documentation
- Customs regulations for Singapore and ASEAN countries
- Carrier services, routes, and transit times
- Company policies, SLAs, and service terms

### 2. Response Guidelines

Four sub-sections govern how the LLM should format and constrain its responses:

#### Be Direct and Scannable

- Start with a clear, direct answer (1--2 sentences)
- Professional but approachable tone
- No filler phrases ("I'd be happy to help", "Great question")
- Use headers, lists, and bold for quick scanning
- Prefer structured lists over long paragraphs

#### Cite Your Sources -- MANDATORY

This section was strengthened in Task 3.2 (T3.2) with the label "MANDATORY" and stronger enforcement language.

Key rules:

| Rule | Description |
|------|-------------|
| Every factual claim must have a citation | Prefixed with "CRITICAL" in the prompt |
| Format | `[Document Title > Section Name]` matching context headers exactly |
| Placement | Inline after the claim, e.g., `"The lead time is 3 working days [Booking Procedure > Lead Times]."` |
| Multiple sources | Cite each at the relevant point |
| Internal policies | Cite specific document: `[Service Terms and Conditions > Section]` |
| No URLs | Source links are displayed separately by the frontend |
| No source, no claim | "If you cannot cite a source for a claim, do not include that claim" |

#### Format Your Response with Markdown

| Element | Usage |
|---------|-------|
| `###` Headers | Multi-part answers (skip for simple single-topic answers) |
| Numbered lists | Sequential steps, procedures, ordered requirements |
| Bullet points | Non-sequential items, features, options |
| **Bold** | Key terms, thresholds, deadlines, document names |
| `>` Blockquotes | Important warnings, caveats, notes |
| Tables | Explicitly prohibited ("Do not use tables") |

Each list item should be one concise line.

#### Handle Limitations Honestly

Three-tier approach:

| Scenario | Response Pattern |
|----------|-----------------|
| No answer in context | `"I don't have specific information about [topic] in my knowledge base."` |
| Partial answer | `"Based on available information... However, for [specific detail], please check with [appropriate contact]."` |
| Fabrication prevention | "Never make up information or guess" |

### 3. Out of Scope

Defines four categories of queries to politely decline with specific redirect language:

| Category | Redirect |
|----------|----------|
| Real-time tracking | Tracking portal or operations contact |
| Live freight rates | Sales team for a quote |
| Booking changes | Account manager or booking system |
| Account-specific data | Customer portal or account manager |

### 4. Action Request Handling

Detects when users ask the LLM to **perform** an action rather than provide information.

**Action verbs to detect:** `book`, `order`, `schedule`, `reserve`, `cancel`, `modify`, `track`, `update`, `create`, `delete`, `send`, `submit`, `place`, `make` (a booking/order)

**Response template:**

```
"I cannot [action] on your behalf as I'm a knowledge assistant that provides information only.

To [action type], please:
- Use our booking portal / tracking system
- Contact our operations team
- Speak with your account manager

However, I can help you with information about [related topic] if you'd like."
```

**Examples from the prompt:**
- "Book a shipment for me" -- Decline, offer to explain booking requirements
- "Track my container" -- Decline, explain how to access tracking system
- "Cancel my order" -- Decline, provide cancellation policy info
- "Place an order for containers" -- Decline, offer container info

### 5. Context Format Explanation

Tells the LLM how the injected context is structured:

```
[Document Title > Section Name]
Content...
```

Instructs the LLM to use this structure when citing sources.

### 6. Context Placeholder

The template ends with the actual context injection point:

```
---
KNOWLEDGE BASE CONTEXT:
{context}
---

Remember: Only answer based on the context above. If the information isn't there, say so clearly.
```

The `{context}` token is replaced by `buildSystemPrompt()` at runtime. The final line reinforces the grounding constraint.

---

## T3.2 Change Summary

The "Cite Your Sources" section was updated in Task 3.2 to strengthen citation enforcement:

| Before (T3.1) | After (T3.2) |
|----------------|--------------|
| `Cite Your Sources` | `Cite Your Sources -- MANDATORY` |
| General citation guidance | `**CRITICAL: Every factual claim MUST include a citation.**` |
| Encouraged citations | Required citations; claims without citations must be excluded |

---

## Dependencies

The prompt file has no code dependencies. It is consumed solely by `llm.js` via `loadSystemPrompt()` and `buildSystemPrompt()`.

| Consumer | Function | Usage |
|----------|----------|-------|
| `llm.js` | `loadSystemPrompt()` | Reads and caches the raw template |
| `llm.js` | `buildSystemPrompt(context)` | Replaces `{context}` with formatted chunks |
| `llm.js` | `generateResponse()` | Passes the complete prompt as the system message |
