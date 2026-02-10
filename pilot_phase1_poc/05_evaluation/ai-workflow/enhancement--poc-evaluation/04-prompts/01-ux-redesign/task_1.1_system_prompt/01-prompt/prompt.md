# Task 1.1: Update System Prompt for Structured Formatting

**Phase:** Phase 1 — UX Redesign
**Initiative:** enhancement--poc-evaluation

---

## Persona

You are a **Prompt Engineer** with expertise in:
- LLM system prompt design for RAG applications
- Structured output formatting (markdown rendering)
- Citation and source attribution patterns
- Groq API / Llama 3.1 8B behavior and constraints

You write clear, well-structured system prompts that produce consistent, well-formatted outputs.

---

## Context

### Initiative
Waypoint Phase 1 POC — Week 4 Evaluation & Documentation. The UX is being redesigned from a simple text block into a structured 4-section response card. The system prompt must be updated to enforce structured markdown formatting so the LLM produces responses that render well in the new frontend.

### Reference Documents
- Master rules: `./CLAUDE.md`
- Week 4 plan: `./pilot_phase1_poc/05_evaluation/week4_plan.md` (Decisions #11, #12)
- Task 0 output: `./ai-workflow/enhancement--poc-evaluation/04-prompts/00-setup/task_0_workspace_setup/02-output/TASK_0_OUTPUT.md`

### Working Directory
`./pilot_phase1_poc/05_evaluation/`

### Dependencies
- Task 0 (Workspace Setup) — ✅ COMPLETE (CP1 passed)

### Current State
The current system prompt at `backend/prompts/system.txt` produces plain text responses with inline citations like `"According to [Document Title > Section]..."`. The new UX will:
- Render the **Answer** section via `react-markdown` with `remark-gfm` (supports headers, numbered lists, bullets, bold, blockquotes, tables)
- Display **Sources** separately (clickable external URLs) — extracted by the backend from chunk metadata, NOT from the LLM response
- Display **Related Documents** separately (category chips) — extracted by the backend from chunk metadata
- Display **Confidence Footer** separately — calculated by the backend

Therefore the system prompt should focus ONLY on formatting the **Answer** section well. It should NOT ask the LLM to output source URLs or confidence info — those are handled by the backend.

### Current System Prompt
```
backend/prompts/system.txt (76 lines)
```

Key sections to preserve:
- Role definition (freight forwarding co-pilot for Singapore/SEA)
- Out-of-scope handling (tracking, live rates, bookings, account data)
- Action request detection and decline pattern
- Context format explanation (`{context}` placeholder)
- "Only answer based on the context above" rule

Key sections to change:
- "Cite Your Sources" — simplify since Sources section is now separate
- "Structure Your Response" — enforce markdown formatting for the Answer section
- "Be Direct and Professional" — keep but strengthen structure requirements

---

## Task

### Objective
Update `backend/prompts/system.txt` to produce well-structured, markdown-formatted responses that render correctly in the new 4-section response card. The LLM should focus on producing a high-quality **Answer** with proper markdown formatting and inline document references.

### Changes Required

#### 1. Update "Cite Your Sources" section
The new UX has a dedicated Sources section with clickable URLs. The LLM should still reference document names inline (so the backend can match citations), but should NOT include URLs or try to format source blocks.

**Current:**
```
### Cite Your Sources
- Reference the document and section for every factual claim
- Format: "According to [Document Title > Section]..."
- If information comes from multiple sources, cite each one
- For internal policies, note: "[Internal Policy]"
```

**New — simplified inline citation format:**
- Keep referencing `[Document Title > Section]` inline — backend uses this to match chunks
- Remove the "According to..." phrasing requirement — just use `[Title > Section]` naturally
- Keep the multi-source citation rule
- Keep the internal policy note

#### 2. Update "Structure Your Response" section
Enforce markdown formatting that renders well in react-markdown:

- Use `###` headers to organize multi-part answers (e.g., "### Required Documents", "### Process Steps")
- Use **numbered lists** for sequential steps or required document lists
- Use **bullet points** for non-sequential items
- Use **bold** for key terms, thresholds, deadlines, document names
- Use **blockquotes** (`>`) for important warnings or caveats
- Keep each bullet/item to one concise line
- For simple questions, skip headers — just give a direct paragraph + list
- Do NOT use tables (they render poorly on narrow screens)

#### 3. Update "Be Direct and Professional" section
- Keep the concise, professional tone
- Add: structure the response to be scannable — headers, lists, bold key terms
- Reduce the paragraph target: aim for structured lists over paragraphs where possible

#### 4. Keep these sections unchanged
- Role definition (lines 1-8)
- "Handle Limitations Honestly" section
- "Out of Scope" section
- "Action Request Handling" section
- Context format and `{context}` placeholder
- Final "Only answer based on the context above" rule

### What NOT to change
- Do NOT add instructions for Sources, Related Documents, or Confidence sections — those are handled entirely by the backend
- Do NOT ask the LLM to output URLs
- Do NOT change the `{context}` placeholder format
- Do NOT change the out-of-scope or action handling behavior

---

## Format

### Output Location
`./ai-workflow/enhancement--poc-evaluation/04-prompts/01-ux-redesign/task_1.1_system_prompt/02-output/TASK_1.1_OUTPUT.md`

### Output Report Sections
1. **Summary** — What was changed
2. **Before/After** — Key sections showing old vs new
3. **Design Decisions** — Why each change was made
4. **Validation** — How to verify the prompt works (test query examples)
5. **Issues** — Any problems encountered
6. **Next Steps** — Task 1.2 (backend pipeline)

### Update on Completion
- [ ] Checklist: Mark Task 1.1 complete
- [ ] Roadmap: Update Task 1.1 status

---

## Validation Criteria

This task is complete when:
- [ ] `backend/prompts/system.txt` updated with new formatting instructions
- [ ] Role definition preserved (freight forwarding co-pilot)
- [ ] Out-of-scope handling preserved
- [ ] Action request handling preserved
- [ ] `{context}` placeholder preserved
- [ ] Inline citation format `[Document Title > Section]` preserved (for backend matching)
- [ ] No URL output instructions (Sources section is separate)
- [ ] Markdown formatting instructions added (headers, lists, bold, blockquotes)
- [ ] Output report created
- [ ] Tracking docs updated
