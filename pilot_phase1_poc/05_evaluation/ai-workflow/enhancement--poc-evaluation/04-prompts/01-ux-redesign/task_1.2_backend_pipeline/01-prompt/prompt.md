# Task 1.2: Update Backend Pipeline (sources, relatedDocs, confidence, metadata)

**Phase:** Phase 1 — UX Redesign
**Initiative:** enhancement--poc-evaluation

---

## Persona

You are a **Node.js Backend Engineer** with expertise in:
- Express.js REST API development
- RAG pipeline architecture (retrieval → generation → citation)
- Data transformation and deduplication
- Jest unit testing with ESM mocks
- Working with ChromaDB metadata (comma-separated string fields)

---

## Context

### Initiative
Waypoint Phase 1 POC — Week 4 Evaluation & Documentation. The UX is being redesigned from a simple text response into a structured 4-section response card. The backend must return an enriched response shape so the React frontend can render each section independently.

### Reference Documents
- Master rules: `./CLAUDE.md`
- UX Mockup: `./pilot_phase1_poc/05_evaluation/ux_mockup/waypoint_response_mockup.jsx`
- Week 4 plan: `./pilot_phase1_poc/05_evaluation/week4_plan.md` (Decisions #11, #12)
- Task 1.1 output: `./ai-workflow/enhancement--poc-evaluation/04-prompts/01-ux-redesign/task_1.1_system_prompt/02-output/TASK_1.1_OUTPUT.md`

### Working Directory
`./pilot_phase1_poc/05_evaluation/`

### Dependencies
- Task 1.1 (System Prompt Update) — ✅ COMPLETE
- Checkpoint 1 (Workspace Setup) — ✅ PASSED

### Current State

The pipeline currently returns this response shape from `processQuery()` in `pipeline.js`:

```javascript
{
  answer: "LLM-generated text",
  citations: [{ title, section, matched, sourceUrls, docId, score, fullTitle }],
  sourcesMarkdown: "---\n**Sources:**\n1. [Title](url)",
  confidence: { level: "High|Medium|Low", reason: "string" },
  metadata: {
    query: "original query",
    chunksRetrieved: 5,
    chunksUsed: 3,
    model: "llama-3.1-8b-instant",
    usage: { promptTokens, completionTokens },
    latency: { retrievalMs, generationMs, citationMs, totalMs },
  },
}
```

The new UX mockup expects this shape:

```javascript
{
  answer: "LLM-generated markdown text",
  sources: [{ title, org, url, section }],           // NEW — clickable external URLs
  relatedDocs: [{ title, category, docId, url }],    // NEW — category-tagged document chips
  citations: [...],                                    // KEEP — existing citation array
  confidence: { level, reason },                       // KEEP — same shape
  metadata: { chunksRetrieved, chunksUsed, latencyMs }, // SIMPLIFIED — flat, frontend-friendly
}
```

### ChromaDB Chunk Metadata Fields Available

Each chunk stored in ChromaDB has these metadata fields (all strings):

| Field | Example | Notes |
|-------|---------|-------|
| `doc_id` | `"01_regulatory_sg_import_procedures"` | Unique document identifier |
| `title` | `"Singapore Import Procedures"` | Human-readable document title |
| `source_org` | `"Singapore Customs"` | Organization that published the document |
| `source_type` | `"public_regulatory"` | One of: `public_regulatory`, `public_carrier`, `synthetic_internal` |
| `category` | `"01_regulatory"` | KB folder category |
| `source_urls` | `"https://url1.com,https://url2.com"` | Comma-separated URLs (may be empty `""`) |
| `section_header` | `"Documentation Requirements"` | Section within the document |
| `jurisdiction` | `"SG"` | Country/region code |
| `file_path` | `"kb/01_regulatory/..."` | Relative file path |
| `retrieval_keywords` | `"import,permit,tradenet"` | Comma-separated keywords |
| `use_cases` | `"UC-1.1,UC-2.1"` | Comma-separated use case IDs |
| `chunk_index` | `"0"` | Chunk position within document (string) |

### Files to Modify

1. **`backend/services/pipeline.js`** — Update `processQuery()` and `buildNoResultsResponse()` to return the new shape
2. **`backend/services/citations.js`** — Add new functions to build `sources` and `relatedDocs` arrays from chunk metadata

### Existing Test Files (will need updates)

1. **`tests/pipeline.test.js`** — 19 tests: response shape assertions, confidence calculation, error handling
2. **`tests/citations.test.js`** — 33 tests: extraction, matching, enrichment, formatting, deduplication
3. **`tests/api.test.js`** — 11 tests: endpoint validation, mock response shape

---

## Task

### Objective

Update the backend pipeline to return the enriched response structure needed for the 4-section frontend. Add `sources` and `relatedDocs` arrays built from chunk metadata. Simplify `metadata` for frontend consumption. Keep existing `citations` and `confidence` intact.

### Changes Required

#### 1. Add `buildSources()` to `citations.js`

Build the `sources` array from enriched citations. Each source represents a clickable external URL.

```javascript
/**
 * Build sources array for the frontend Sources section.
 * Extracts external URLs from matched citations' chunk metadata.
 *
 * @param {Array} enrichedCitations - Enriched citations from enrichCitations()
 * @param {Array} chunks - Retrieved chunks with metadata
 * @returns {Array<{title: string, org: string, url: string, section: string|null}>}
 */
export function buildSources(enrichedCitations, chunks) {
  // For each matched citation that has sourceUrls:
  //   - title: citation.fullTitle or citation.title
  //   - org: look up source_org from the matched chunk's metadata
  //   - url: first source URL (or iterate all URLs)
  //   - section: citation.section or null
  // Deduplicate by URL
  // Return empty array if no external sources
}
```

**Rules:**
- Only include citations where `matched === true` AND `sourceUrls.length > 0`
- `org` comes from the chunk's `metadata.source_org` field
- If a citation has multiple `sourceUrls`, create one source entry per URL (same title/org, different url)
- Deduplicate by `url` (no duplicate URLs in output)
- Sort by citation position (order they appear in the answer)

#### 2. Add `buildRelatedDocs()` to `citations.js`

Build the `relatedDocs` array from all retrieved chunks' parent documents.

```javascript
/**
 * Build relatedDocs array for the frontend Related Documents section.
 * Extracts unique parent documents from all retrieved chunks.
 *
 * @param {Array} chunks - All retrieved chunks with metadata
 * @returns {Array<{title: string, category: string, docId: string, url: string|null}>}
 */
export function buildRelatedDocs(chunks) {
  // For each unique doc_id across all chunks:
  //   - title: chunk.metadata.title
  //   - category: map chunk.metadata.category to frontend category name
  //     "01_regulatory" → "regulatory"
  //     "02_carriers" → "carrier"
  //     "03_reference" → "reference"
  //     "04_internal_synthetic" → "internal"
  //   - docId: chunk.metadata.doc_id
  //   - url: first source_url if external, null if internal/empty
  // Deduplicate by docId
}
```

**Rules:**
- Deduplicate by `doc_id` — each parent document appears once
- `category` must be the **frontend category name** (strip the number prefix): `"01_regulatory"` → `"regulatory"`, `"02_carriers"` → `"carrier"`, `"03_reference"` → `"reference"`, `"04_internal_synthetic"` → `"internal"`
- `url` is the first `source_url` if the document has external URLs, otherwise `null`
- Order: maintain the order of first appearance in the chunks array

#### 3. Update `processQuery()` in `pipeline.js`

Update the response assembly to include the new fields:

```javascript
const response = {
  answer: llmResult.answer,
  sources: buildSources(citationResult.citations, chunks),      // NEW
  relatedDocs: buildRelatedDocs(chunks),                         // NEW
  citations: citationResult.citations.filter(c => c.matched),   // KEEP
  confidence,                                                     // KEEP (already { level, reason })
  metadata: {                                                     // SIMPLIFIED
    query: trimmedQuery,
    chunksRetrieved: chunks.length,
    chunksUsed: citationResult.stats.matched,
    latencyMs: metrics.totalMs,                                   // Single number, not nested
    model: llmResult.model,
  },
};
```

**Note:** Remove `sourcesMarkdown` from the response — the frontend Sources section replaces it. Keep backward compatibility: the `citations` array stays (used by tests and for debugging), but `sourcesMarkdown` is removed.

#### 4. Update `buildNoResultsResponse()` in `pipeline.js`

```javascript
{
  answer: "I don't have specific information...",
  sources: [],
  relatedDocs: [],
  citations: [],
  confidence: { level: 'Low', reason: 'No relevant documents found' },
  metadata: {
    query,
    chunksRetrieved: 0,
    chunksUsed: 0,
    latencyMs: metrics.totalMs,
    model: null,
  },
}
```

#### 5. Update existing tests

**`tests/pipeline.test.js`:**
- Update response shape assertions: add `sources`, `relatedDocs`; remove `sourcesMarkdown`
- Update `mockCitationResult` to include enriched citation fields needed by `buildSources()`
- Keep all existing confidence and error handling tests unchanged

**`tests/citations.test.js`:**
- Add test suite for `buildSources()`:
  - Returns source objects with correct shape `{ title, org, url, section }`
  - Deduplicates by URL
  - Excludes unmatched citations
  - Excludes citations with no sourceUrls
  - Returns empty array when no external sources
  - Handles multiple URLs per citation
- Add test suite for `buildRelatedDocs()`:
  - Returns relatedDoc objects with correct shape `{ title, category, docId, url }`
  - Maps category prefixes correctly (`01_regulatory` → `regulatory`, etc.)
  - Deduplicates by docId
  - Sets `url` to null for internal documents with no source_urls
  - Preserves first-appearance order

**`tests/api.test.js`:**
- Update `mockResult` to include `sources` and `relatedDocs`; remove `sourcesMarkdown`

### What NOT to Change

- Do NOT modify `citations.js` extraction logic (`extractCitations`, `matchCitationToChunk`, `similarity`)
- Do NOT modify `retrieval.js`
- Do NOT modify `llm.js`
- Do NOT modify `config.js`
- Do NOT modify the query route (`routes/query.js`) — it passes through `processQuery()` result directly
- Do NOT change the `confidence` calculation logic in `calculateConfidence()`

---

## Format

### Output Location
`./ai-workflow/enhancement--poc-evaluation/04-prompts/01-ux-redesign/task_1.2_backend_pipeline/02-output/TASK_1.2_OUTPUT.md`

### Output Report Sections
1. **Summary** — What was changed
2. **New Functions** — `buildSources()` and `buildRelatedDocs()` signatures and behavior
3. **Response Shape** — Before/after comparison
4. **Test Changes** — What tests were added/modified
5. **Validation** — Test results (all tests must pass)
6. **Issues** — Any problems encountered
7. **Next Steps** — Task 1.3 (React frontend)

### Update on Completion
- [ ] Checklist: Mark Task 1.2 complete
- [ ] Roadmap: Update Task 1.2 status

---

## Validation Criteria

This task is complete when:
- [ ] `buildSources()` added to `citations.js` — returns `[{ title, org, url, section }]`
- [ ] `buildRelatedDocs()` added to `citations.js` — returns `[{ title, category, docId, url }]`
- [ ] Category mapping works: `01_regulatory` → `regulatory`, `02_carriers` → `carrier`, `03_reference` → `reference`, `04_internal_synthetic` → `internal`
- [ ] `processQuery()` returns `sources`, `relatedDocs` in response
- [ ] `sourcesMarkdown` removed from response
- [ ] `metadata` includes flat `latencyMs` (not nested `latency` object)
- [ ] `buildNoResultsResponse()` returns empty `sources` and `relatedDocs`
- [ ] All new `buildSources()` tests pass (≥5 test cases)
- [ ] All new `buildRelatedDocs()` tests pass (≥5 test cases)
- [ ] All existing tests pass or are updated to match new shape
- [ ] `npm test` — all tests green
- [ ] Output report created

### Test Commands
```bash
cd pilot_phase1_poc/05_evaluation
npm test
```

**Important:** Use `npm test` (NOT `npx jest`) — requires `--experimental-vm-modules` flag for ESM.
