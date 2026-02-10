# Task 1.3: Implement New React Frontend (TDD per section)

**Phase:** Phase 1 — UX Redesign
**Initiative:** enhancement--poc-evaluation

---

## Persona

You are a **React Frontend Engineer** with expertise in:
- React 19 with functional components and hooks
- Tailwind CSS utility-first styling
- `react-markdown` with custom component mapping
- Vitest / React Testing Library for component testing
- Accessible, responsive UI design

---

## Context

### Initiative
Waypoint Phase 1 POC — Week 4 Evaluation & Documentation. The frontend is being redesigned from a simple text-based response into a structured 4-section response card. The visual reference is the UX mockup.

### Reference Documents
- **UX Mockup (visual reference)**: `./pilot_phase1_poc/05_evaluation/ux_mockup/waypoint_response_mockup.jsx`
- Master rules: `./CLAUDE.md`
- Task 1.1 output (system prompt): `./ai-workflow/.../task_1.1_system_prompt/02-output/TASK_1.1_OUTPUT.md`
- Task 1.2 output (backend pipeline): `./ai-workflow/.../task_1.2_backend_pipeline/02-output/TASK_1.2_OUTPUT.md`

### Working Directory
`./pilot_phase1_poc/05_evaluation/`

### Dependencies
- Task 1.1 (System Prompt) — ✅ COMPLETE
- Task 1.2 (Backend Pipeline) — ✅ COMPLETE

### Current Frontend State

The existing frontend at `client/` has:
- **React 19.2.0** + **Vite 7.2.4** + **Tailwind CSS 3.4.19**
- **`react-markdown` 10.1.0** already installed (but `remark-gfm` is NOT installed)
- 5 existing components: `QueryInput.jsx`, `Response.jsx`, `Citations.jsx`, `Confidence.jsx`, `Loading.jsx`
- API client at `api/query.js` — uses `fetch('/api/query')` via Vite proxy
- No test framework configured for frontend yet (no Vitest)

### Backend Response Shape (from Task 1.2)

```javascript
{
  answer: "LLM markdown text",
  sources: [{ title, org, url, section }],
  relatedDocs: [{ title, category, docId, url }],
  citations: [{ title, section, matched, sourceUrls, docId, score, fullTitle }],
  confidence: { level: "High|Medium|Low", reason: "string" },
  metadata: { query, chunksRetrieved, chunksUsed, latencyMs, model },
}
```

### Mockup Design Specs (from `ux_mockup/waypoint_response_mockup.jsx`)

**Component Structure:**
- `ResponseCard` — card wrapper (`bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden`)
- `SourcesSection` — clickable source URLs with org + domain subtitle
- `RelatedDocsSection` — category-tagged document chips
- `ConfidenceFooter` — colored badge + metadata stats

**Category Colors/Icons:**
| Category | BG | Text | Border | Icon |
|----------|----|------|--------|------|
| regulatory | `bg-blue-50` | `text-blue-700` | `border-blue-200` | 🏛️ |
| carrier | `bg-amber-50` | `text-amber-700` | `border-amber-200` | 🚢 |
| internal | `bg-slate-50` | `text-slate-600` | `border-slate-200` | 📋 |
| reference | `bg-emerald-50` | `text-emerald-700` | `border-emerald-200` | 📚 |

**Confidence Badge Colors:**
| Level | BG | Text | Border | Dot |
|-------|----|------|--------|-----|
| High | `bg-emerald-50` | `text-emerald-700` | `border-emerald-300` | `bg-emerald-500` |
| Medium | `bg-amber-50` | `text-amber-700` | `border-amber-300` | `bg-amber-500` |
| Low | `bg-rose-50` | `text-rose-700` | `border-rose-300` | `bg-rose-500` |

**Markdown Approach:** Hybrid — `react-markdown` + `remark-gfm` for parsing, custom Tailwind component mapping matching mockup styles.

---

## Task

### Objective

Refactor the existing React frontend into the 4-section response card design matching the UX mockup. Use TDD where practical — write tests for component rendering and data-driven behavior, then implement. Use Chrome DevTools MCP for visual verification.

### Implementation Order

#### Step 0 — Install dependencies

```bash
cd client
npm install remark-gfm
```

No Vitest setup required — frontend tests will be covered in Phase 2 (Task 2.9). Focus this task on implementation with visual verification via Chrome DevTools MCP.

#### Step 1 — Create `SourcesSection.jsx`

**New file:** `client/src/components/SourcesSection.jsx`

Replaces the old `Citations.jsx` for displaying clickable external URLs.

**Props:** `{ sources }` — array of `{ title, org, url, section }`

**Behavior:**
- Returns `null` if `sources` is empty or undefined
- Section header: link icon + "Sources" uppercase label
- Each source: clickable link with title + section, org + domain subtitle below
- Link styling: `hover:bg-sky-50`, sky-blue link icon
- Domain extraction: `url.replace("https://www.", "").split("/")[0]`

**Tailwind classes from mockup:**
- Container: `border-t border-slate-200 px-5 py-4`
- Header: `text-xs font-semibold text-slate-500 uppercase tracking-wider`
- Link row: `group flex items-start gap-3 p-2.5 rounded-lg hover:bg-sky-50 transition-colors duration-150`
- Link icon box: `flex-shrink-0 w-8 h-8 rounded-lg bg-sky-100 flex items-center justify-center`
- Title: `text-sm font-medium text-sky-700 group-hover:text-sky-800 group-hover:underline`
- Subtitle: `text-xs text-slate-400 truncate mt-0.5`

#### Step 2 — Create `RelatedDocsSection.jsx`

**New file:** `client/src/components/RelatedDocsSection.jsx`

This is entirely new — no existing component to refactor.

**Props:** `{ docs }` — array of `{ title, category, docId, url }`

**Behavior:**
- Returns `null` if `docs` is empty or undefined
- Section header: document icon + "Related Documents" uppercase label
- Category chip per document using `categoryColors` mapping
- Chips with `url`: render as `<a>` with external link icon
- Chips without `url` (null): render as `<span>` (no link)

**Category color mapping** (define as const in the component):
```javascript
const categoryColors = {
  regulatory: { bg: "bg-blue-50", text: "text-blue-700", border: "border-blue-200", icon: "🏛️" },
  carrier: { bg: "bg-amber-50", text: "text-amber-700", border: "border-amber-200", icon: "🚢" },
  internal: { bg: "bg-slate-50", text: "text-slate-600", border: "border-slate-200", icon: "📋" },
  reference: { bg: "bg-emerald-50", text: "text-emerald-700", border: "border-emerald-200", icon: "📚" },
};
```

**Tailwind classes from mockup:**
- Container: `border-t border-slate-200 px-5 py-4`
- Chips wrapper: `flex flex-wrap gap-2`
- Each chip: `inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border ${cat.bg} ${cat.text} ${cat.border}`
- Link chips: add `hover:shadow-sm transition-all duration-150`
- External link icon on link chips: `w-3 h-3 opacity-50`

#### Step 3 — Create `ConfidenceFooter.jsx`

**Refactor:** Replace `Confidence.jsx` with `ConfidenceFooter.jsx` (new file, different layout).

**Props:** `{ confidence, metadata }`
- `confidence`: `{ level, reason }`
- `metadata`: `{ chunksRetrieved, chunksUsed, latencyMs }`

**Behavior:**
- Left side: colored dot + badge + reason text
- Right side: metadata stats in monospace (`{chunksRetrieved} retrieved · {chunksUsed} used · {(latencyMs/1000).toFixed(1)}s`)
- Footer background: `bg-slate-50/50 rounded-b-xl`

**Confidence styles** (define as const):
```javascript
const confidenceStyles = {
  High: { bg: "bg-emerald-50", text: "text-emerald-700", border: "border-emerald-300", dot: "bg-emerald-500" },
  Medium: { bg: "bg-amber-50", text: "text-amber-700", border: "border-amber-300", dot: "bg-amber-500" },
  Low: { bg: "bg-rose-50", text: "text-rose-700", border: "border-rose-300", dot: "bg-rose-500" },
};
```

**Tailwind classes from mockup:**
- Container: `border-t border-slate-100 px-5 py-3 flex items-center justify-between bg-slate-50/50 rounded-b-xl`
- Badge: `inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${style.bg} ${style.text} ${style.border}`
- Dot: `w-1.5 h-1.5 rounded-full ${style.dot}`
- Reason: `text-xs text-slate-400`
- Stats: `text-xs text-slate-400 font-mono`

#### Step 4 — Create `ResponseCard.jsx`

**New file:** `client/src/components/ResponseCard.jsx`

Assembles all 4 sections into the card layout.

**Props:** `{ data }` — full API response object

**Behavior:**
- Card wrapper: `bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden`
- Section 1 (Answer): render `data.answer` via `react-markdown` + `remark-gfm` with custom component mapping
- Section 2: `<SourcesSection sources={data.sources} />`
- Section 3: `<RelatedDocsSection docs={data.relatedDocs} />`
- Section 4: `<ConfidenceFooter confidence={data.confidence} metadata={data.metadata} />`

**react-markdown custom component mapping:**
```jsx
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const markdownComponents = {
  h3: ({ children }) => (
    <h3 className="text-sm font-bold text-slate-800 mt-5 mb-2 first:mt-0">{children}</h3>
  ),
  p: ({ children }) => (
    <p className="text-sm text-slate-700 leading-relaxed my-2">{children}</p>
  ),
  ol: ({ children }) => (
    <ol className="list-decimal list-outside ml-5 space-y-1.5 my-3">{children}</ol>
  ),
  ul: ({ children }) => (
    <ul className="list-disc list-outside ml-5 space-y-1.5 my-3">{children}</ul>
  ),
  li: ({ children }) => (
    <li className="text-sm text-slate-700 leading-relaxed pl-1">{children}</li>
  ),
  strong: ({ children }) => (
    <strong className="font-semibold text-slate-900">{children}</strong>
  ),
  em: ({ children }) => (
    <em className="italic">{children}</em>
  ),
  blockquote: ({ children }) => (
    <blockquote className="border-l-3 border-sky-300 bg-sky-50/50 pl-4 pr-3 py-2.5 my-3 rounded-r-lg">{children}</blockquote>
  ),
  code: ({ children }) => (
    <code className="text-xs bg-slate-100 text-slate-700 px-1.5 py-0.5 rounded font-mono">{children}</code>
  ),
};

// In JSX:
<div className="px-5 py-5">
  <Markdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
    {data.answer}
  </Markdown>
</div>
```

#### Step 5 — Update `Loading.jsx`

Update loading animation to match mockup (bouncing dots instead of spinner).

**New behavior:**
- 3 sky-blue bouncing dots with staggered animation delays (0ms, 150ms, 300ms)
- Text: "Searching knowledge base..."
- Remove the 200ms delay logic (show immediately)

**Tailwind from mockup:**
```jsx
<div className="bg-white rounded-xl border border-slate-200 shadow-sm p-8">
  <div className="flex items-center justify-center gap-3">
    <div className="flex gap-1">
      <div className="w-2 h-2 bg-sky-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
      <div className="w-2 h-2 bg-sky-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
      <div className="w-2 h-2 bg-sky-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
    </div>
    <span className="text-sm text-slate-400">Searching knowledge base...</span>
  </div>
</div>
```

#### Step 6 — Update `App.jsx`

Replace the existing response rendering with the new `ResponseCard`.

**Changes:**
- Import `ResponseCard` instead of `Response`
- Remove imports of `Response` (keep `QueryInput`, `Loading`)
- Update the main content area to use `ResponseCard`
- The response area should NOT have its own card wrapper — `ResponseCard` provides the card styling
- Keep error handling (move error display inline or into a separate error block)
- Update header styling to match mockup (gradient icon)

**Updated structure:**
```jsx
<main className="max-w-3xl mx-auto px-4 py-6 space-y-5">
  <QueryInput onSubmit={handleSubmit} loading={loading} />

  {error && (
    <div className="bg-rose-50 border border-rose-200 rounded-xl p-4">
      {/* error display */}
    </div>
  )}

  {loading ? (
    <Loading />
  ) : response ? (
    <ResponseCard data={response} />
  ) : (
    <div className="text-center py-12 text-slate-500">
      {/* empty state */}
    </div>
  )}
</main>
```

**Header update** (match mockup gradient icon):
```jsx
<div className="w-9 h-9 rounded-xl bg-gradient-to-br from-sky-500 to-blue-600 flex items-center justify-center shadow-sm">
```

#### Step 7 — Clean up old files

- Delete `client/src/components/Citations.jsx` — replaced by `SourcesSection.jsx`
- Delete `client/src/components/Confidence.jsx` — replaced by `ConfidenceFooter.jsx`
- Delete `client/src/components/Response.jsx` — replaced by `ResponseCard.jsx`
- Delete `client/src/App.css` — unused (all styling is Tailwind)

#### Step 8 — Visual verification

Use Chrome DevTools MCP to verify:
1. Start backend: `cd pilot_phase1_poc/05_evaluation && npm start`
2. Start frontend: `cd pilot_phase1_poc/05_evaluation/client && npm run dev`
3. Open browser to `http://localhost:5173`
4. Submit a test query
5. Verify all 4 sections render correctly
6. Check loading state (bouncing dots)
7. Check empty state
8. Verify at desktop resolution (1280px+)

### What NOT to Change

- Do NOT modify `api/query.js` — API client is unchanged
- Do NOT modify `QueryInput.jsx` — search input is kept as-is (already matches mockup styling closely)
- Do NOT modify backend code
- Do NOT add Vitest/testing in this task — frontend tests are Task 2.9
- Do NOT add the mockup's query switcher buttons — those are demo-only

---

## Format

### Output Location
`./ai-workflow/enhancement--poc-evaluation/04-prompts/01-ux-redesign/task_1.3_react_frontend/02-output/TASK_1.3_OUTPUT.md`

### Output Report Sections
1. **Summary** — What was changed
2. **New Components** — Component names, props, behavior
3. **Deleted Components** — What was removed
4. **Design Decisions** — Why each choice was made
5. **Visual Verification** — Screenshots/description of browser check
6. **Issues** — Any problems encountered
7. **Next Steps** — Task 1.4 (inline documentation)

### Update on Completion
- [ ] Checklist: Mark Task 1.3 complete
- [ ] Roadmap: Update Task 1.3 status

---

## Validation Criteria

This task is complete when:
- [ ] `remark-gfm` installed
- [ ] `SourcesSection.jsx` created — renders clickable URLs with org + domain subtitle
- [ ] `RelatedDocsSection.jsx` created — renders category chips with correct colors/icons
- [ ] `ConfidenceFooter.jsx` created — renders colored badge + metadata stats
- [ ] `ResponseCard.jsx` created — assembles all 4 sections with react-markdown + remark-gfm
- [ ] `Loading.jsx` updated — bouncing dots animation
- [ ] `App.jsx` updated — uses ResponseCard, gradient header icon
- [ ] Old components deleted (`Citations.jsx`, `Confidence.jsx`, `Response.jsx`, `App.css`)
- [ ] `npm run build` succeeds (no compilation errors)
- [ ] Visual verification via Chrome DevTools MCP — all 4 sections visible
- [ ] Loading state shows bouncing dots
- [ ] Empty state renders correctly
- [ ] Category chip colors match mockup
- [ ] Confidence badge colors match mockup
- [ ] Output report created
