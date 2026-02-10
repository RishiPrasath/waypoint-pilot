# Task 1.1 Output — Update System Prompt for Structured Formatting

**Task:** 1.1 — Update system prompt for structured formatting
**Phase:** Phase 1 — UX Redesign
**Status:** ✅ COMPLETE
**Date:** 2026-02-09

---

## Summary

Updated `backend/prompts/system.txt` to enforce markdown-formatted responses for the new 4-section response card. Three sections were modified; all safety/scope sections preserved unchanged. All 105 Jest tests continue to pass.

---

## Before/After

### Section 1: "Be Direct and Professional" → "Be Direct and Scannable"

**Before (lines 10-13):**
```
### Be Direct and Professional
- Start with a direct answer (1-2 sentences)
- Keep it concise and professional
- If multiple topics, organize with numbered headers
```

**After (lines 12-17):**
```
### Be Direct and Scannable
- Start with a clear, direct answer to the question (1-2 sentences)
- Use professional but approachable language
- Avoid filler phrases like "I'd be happy to help" or "Great question"
- Structure for quick scanning — use headers, lists, and bold for key terms
- Prefer structured lists over long paragraphs
```

**Why:** Added explicit scannable structure guidance. The old prompt only said "concise and professional" — the new one tells the LLM how to structure for quick scanning (headers, lists, bold).

---

### Section 2: "Cite Your Sources" → "Cite Your Sources Inline"

**Before:**
```
### Cite Your Sources
- Reference the document and section for every factual claim
- Format: "According to [Document Title > Section]..."
- If information comes from multiple sources, cite each one
- For internal policies, note: "[Internal Policy]"
```

**After (lines 19-24):**
```
### Cite Your Sources Inline
- Reference the document and section for every factual claim using `[Document Title > Section]`
- Place citations naturally in the text, e.g., "The lead time is 3 working days [Booking Procedure > Lead Times]."
- If information comes from multiple sources, cite each one at the relevant point
- For internal policies, use `[Internal Policy]` as the source tag
- Do NOT include URLs or links — source links are displayed separately by the system
```

**Why:** The new UX has a dedicated Sources section with clickable URLs extracted by the backend. The LLM should place `[Document Title > Section]` inline (so the backend can match citations to chunks), but should NOT output URLs. Removed the "According to..." phrasing requirement — citations should flow naturally.

---

### Section 3: "Structure Your Response" → "Format Your Response with Markdown"

**Before:**
```
### Structure Your Response
- For simple questions: 2-3 sentence paragraph
- For complex questions: Use numbered sections with ### headers
- For procedures: Use numbered steps
- For comparisons: Use a structured list
```

**After (lines 26-35):**
```
### Format Your Response with Markdown
Use markdown formatting so the response renders well:

- **Headers** (`###`): Use to organize multi-part answers (e.g., `### Required Documents`, `### Process Steps`). Skip headers for simple single-topic answers.
- **Numbered lists**: Use for sequential steps, procedures, or ordered requirements
- **Bullet points**: Use for non-sequential items, features, or options
- **Bold**: Use for key terms, thresholds, deadlines, and document names
- **Blockquotes** (`>`): Use for important warnings, caveats, or notes

Keep each list item to one concise line. Do not use tables.
```

**Why:** The old section was vague ("Use numbered sections with ### headers"). The new section is explicit about which markdown elements to use and when, matched to what `react-markdown` with `remark-gfm` supports. Tables excluded because they render poorly on narrow screens.

---

## Sections Preserved (Unchanged)

| Section | Lines | Status |
|---------|-------|--------|
| Role definition | 1-8 | ✅ Preserved |
| Handle Limitations Honestly | 37-40 | ✅ Preserved |
| Out of Scope | 42-47 | ✅ Preserved |
| Action Request Handling | 49-68 | ✅ Preserved |
| Context Format + `{context}` placeholder | 70-82 | ✅ Preserved |

---

## Design Decisions

1. **No URL output** — Sources section is backend-driven from `source_urls` in ChromaDB metadata. The LLM outputs `[Document Title > Section]` inline, and the backend matches these to chunk metadata to extract clickable URLs. This separation ensures URLs are always accurate (from metadata, not hallucinated by LLM).

2. **No tables** — Narrow mobile screens and the response card width make tables hard to read. Lists are more scannable and render consistently.

3. **Natural citation placement** — Removed the "According to..." template. Natural inline placement like `"The lead time is 3 working days [Booking Procedure > Lead Times]."` reads better and still gives the backend parseable citation references.

4. **Blockquotes for warnings** — Added blockquote guidance for important caveats (e.g., `> Note: Permits must be obtained before shipment`). This gives visual emphasis in the rendered markdown.

5. **"Scannable" framing** — Renamed the section from "Professional" to "Scannable" to emphasize that CS agents need to quickly extract key information during live calls.

---

## Validation

| Criterion | Status |
|-----------|--------|
| `backend/prompts/system.txt` updated | ✅ |
| Role definition preserved | ✅ |
| Out-of-scope handling preserved | ✅ |
| Action request handling preserved | ✅ |
| `{context}` placeholder preserved | ✅ |
| Inline citation format `[Document Title > Section]` preserved | ✅ |
| No URL output instructions | ✅ Added explicit "Do NOT include URLs" |
| Markdown formatting instructions added | ✅ Headers, lists, bold, blockquotes |
| Jest tests pass (105/105) | ✅ |

---

## Issues

None. The prompt update was a text-only change to `system.txt` with no code impact. All 105 Jest tests pass unchanged.

---

## Next Steps

- **Task 1.2**: Update backend pipeline (sources, relatedDocs, confidence) — depends on this task
