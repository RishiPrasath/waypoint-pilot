# Frontend Component Documentation

**Location**: `pilot_phase1_poc/05_evaluation/client/src/`

---

## App.jsx

**Path**: `src/App.jsx`
**Role**: Root application component. Orchestrates the query flow between input, loading, response display, and error handling.

### State

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `response` | `QueryResponse \| null` | `null` | Full API response object. Set on successful query. Cleared on new submission. |
| `loading` | `boolean` | `false` | True while a query is in flight. Controls Loading visibility and disables QueryInput. |
| `error` | `string \| null` | `null` | Error message string. Shown in a rose-colored banner. Cleared on new submission. |

### handleSubmit(queryText: string)

Async handler passed to `QueryInput.onSubmit`. Execution flow:

1. Creates a new `AbortController` instance.
2. Sets `loading=true`, clears `error` and `response` to `null`.
3. Calls `submitQuery(queryText, controller.signal)`.
4. On success: sets `response` to the returned result.
5. On error: if the error is **not** an `AbortError`, sets `error` to `err.message` or a fallback string.
6. In `finally`: sets `loading=false`.

Note: The `AbortController` is created per-call but the signal is not currently used for cancellation on unmount or re-submission. It is passed to `fetch()` for potential future cleanup.

### Layout Structure

```
div.min-h-screen.bg-slate-50
├── header.bg-white.border-b
│   └── Logo icon (sky-to-blue gradient, chat bubble SVG) + "Waypoint Co-Pilot" title + subtitle
├── main.max-w-3xl.mx-auto
│   ├── <QueryInput onSubmit={handleSubmit} loading={loading} />
│   ├── Error banner (conditional: rose-50 bg, error icon + message)
│   └── Content area (conditional):
│       ├── <Loading />          — when loading=true
│       ├── <ResponseCard data={response} /> — when response exists
│       └── Placeholder text     — when no error, no loading, no response
└── footer
    └── "Waypoint Phase 1 POC - Powered by RAG Pipeline"
```

### Rendering Logic

The main content area uses a ternary chain:

- `loading` is truthy: render `<Loading />`
- `response` is truthy: render `<ResponseCard data={response} />`
- Neither, and no error: render the placeholder text ("Ask a question about...")
- Error exists: the error banner renders above the ternary (it is independent)

### Imports

- `useState` from React
- `QueryInput`, `ResponseCard`, `Loading` components
- `submitQuery` from `api/query.js`

---

## QueryInput.jsx

**Path**: `src/components/QueryInput.jsx`
**Role**: Search input field with submit button and clear functionality.

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `onSubmit` | `(query: string) => void` | Yes | Callback invoked with trimmed query text on form submission |
| `loading` | `boolean` | Yes | When true: disables the input and submit button, shows spinner |

### Internal State

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `query` | `string` | `''` | Controlled input value |

### Refs

| Ref | Target | Purpose |
|-----|--------|---------|
| `inputRef` | `<input>` element | Auto-focus on mount; re-focus after clear |

### Behavior

- **Auto-focus**: `useEffect` on mount calls `inputRef.current?.focus()`.
- **Submit**: Form `onSubmit` trims the query. If trimmed string is non-empty and `loading` is false, calls `onSubmit(trimmed)`.
- **Enter key**: Submit is triggered by pressing Enter because the input is inside a `<form>` element.
- **Clear button**: Visible when `query` is non-empty AND `loading` is false. Clicking it clears the input and re-focuses.
- **Disabled state**: When `loading=true`, the input is disabled (slate-50 background, muted text). The submit button is disabled when `loading` is true OR the trimmed query is empty.

### Submit Button States

| Condition | Visual |
|-----------|--------|
| Idle, query empty | Disabled: `bg-slate-300`, not clickable |
| Idle, query non-empty | Active: `bg-sky-500`, hover `bg-sky-600` |
| Loading | Disabled: shows SVG spinner animation (replaces "Search" text) |

### Clear Button

- SVG "X" icon positioned with `absolute right-3 top-1/2 -translate-y-1/2`.
- Colors: `text-slate-400`, hover `text-slate-600`.
- Hidden when query is empty or loading is active.
- `aria-label="Clear input"` for accessibility.

### Accessibility

- Input: `aria-label="Search query"`
- Submit button: `aria-label` toggles between `"Searching..."` and `"Search"` based on loading state
- Clear button: `aria-label="Clear input"`

---

## ResponseCard.jsx

**Path**: `src/components/ResponseCard.jsx`
**Role**: 4-section response card assembling the answer, sources, related documents, and confidence footer.

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `data` | `QueryResponse` | Yes | Full API response object (see types.js) |

### QueryResponse Shape

```js
{
  answer: string,            // Markdown-formatted answer from LLM
  sources: Source[],         // External URLs for Sources section
  relatedDocs: RelatedDoc[], // KB documents for Related Docs section
  citations: Object[],      // Raw matched citations (not rendered directly)
  confidence: Confidence,   // { level: "High"|"Medium"|"Low", reason: string }
  metadata: ResponseMetadata // { chunksRetrieved, chunksUsed, latencyMs, model, query }
}
```

### Rendering Logic

Returns `null` if `data` is falsy. Otherwise renders a white card (`bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden`) with four sections:

| Section | Content | Separator |
|---------|---------|-----------|
| 1. Answer | `<Markdown>` rendering of `data.answer` | None (first section) |
| 2. Sources | `<SourcesSection sources={data.sources} />` | `border-t` (inside SourcesSection) |
| 3. Related Documents | `<RelatedDocsSection docs={data.relatedDocs} />` | `border-t` (inside RelatedDocsSection) |
| 4. Confidence Footer | `<ConfidenceFooter confidence={data.confidence} metadata={data.metadata} />` | `border-t` (inside ConfidenceFooter) |

### Markdown Component Mapping

The `markdownComponents` object maps markdown elements to custom Tailwind-styled React components:

| Element | Tailwind Classes | Notes |
|---------|-----------------|-------|
| `h3` | `text-sm font-bold text-slate-800 mt-5 mb-2 first:mt-0` | First heading has no top margin |
| `p` | `text-sm text-slate-700 leading-relaxed my-2` | Relaxed line height for readability |
| `ol` | `list-decimal list-outside ml-5 space-y-1.5 my-3` | Numbered list with outside markers |
| `ul` | `list-disc list-outside ml-5 space-y-1.5 my-3` | Bullet list with outside markers |
| `li` | `text-sm text-slate-700 leading-relaxed pl-1` | Slight left padding on list items |
| `strong` | `font-semibold text-slate-900` | Darker text for emphasis |
| `em` | `italic` | Standard italic |
| `blockquote` | `border-l-3 border-sky-300 bg-sky-50/50 pl-4 pr-3 py-2.5 my-3 rounded-r-lg` | Left-bordered sky-blue quote block |
| `code` | `text-xs bg-slate-100 text-slate-700 px-1.5 py-0.5 rounded font-mono` | Inline code with monospace font |

### Dependencies

- `react-markdown` (Markdown component)
- `remark-gfm` (GitHub Flavored Markdown plugin, passed as `remarkPlugins={[remarkGfm]}`)

---

## SourcesSection.jsx

**Path**: `src/components/SourcesSection.jsx`
**Role**: Renders clickable external source links with organization and domain metadata.

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `sources` | `Source[]` | Yes | Array of source objects |

### Source Object Shape

```js
{
  title: string,          // Document title
  org: string,            // Organization name (e.g., "Singapore Customs")
  url: string,            // Full external URL
  section: string | null  // Document section, if applicable
}
```

### Rendering Logic

Returns `null` if `sources` is falsy or empty.

Otherwise renders:
1. **Header**: Link SVG icon + "SOURCES" label (`text-xs font-semibold uppercase tracking-wider`).
2. **Link list**: Each source as a clickable `<a>` element opening in a new tab (`target="_blank" rel="noopener noreferrer"`).

### Per-Source Rendering

Each source link contains:

| Element | Content | Style |
|---------|---------|-------|
| Icon box | External-link SVG | `w-8 h-8 rounded-lg bg-sky-100` with `text-sky-600` icon |
| Title line | `{title}` + ` -- {section}` (if section exists) | `text-sm font-medium text-sky-700`, underlines on hover |
| Subtitle line | `{org} . {domain}` | `text-xs text-slate-400 truncate` |

### Domain Extraction

The domain is extracted inline from `source.url`:
```js
source.url.replace('https://www.', '').replace('https://', '').split('/')[0]
```
This strips protocol and `www.` prefix, taking only the hostname.

### Key

Each link uses `key={source.url}-${i}` (URL + index) to handle potential duplicate URLs.

### Container Styling

- Section wrapper: `border-t border-slate-200 px-5 py-4`
- Each link: `group flex items-start gap-3 p-2.5 rounded-lg hover:bg-sky-50 transition-colors duration-150`

---

## RelatedDocsSection.jsx

**Path**: `src/components/RelatedDocsSection.jsx`
**Role**: Displays category-tagged document chips representing KB documents used in the response.

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `docs` | `RelatedDoc[]` | Yes | Array of related document objects |

### RelatedDoc Object Shape

```js
{
  title: string,          // Document title
  category: string,       // "regulatory" | "carrier" | "internal" | "reference"
  docId: string,          // Unique document identifier (used as React key)
  url: string | null      // External URL, or null for internal-only documents
}
```

### Category Color Mapping

| Category | Background | Text | Border | Emoji Icon |
|----------|-----------|------|--------|------------|
| `regulatory` | `bg-blue-50` | `text-blue-700` | `border-blue-200` | building (U+1F3DB) |
| `carrier` | `bg-amber-50` | `text-amber-700` | `border-amber-200` | ship (U+1F6A2) |
| `internal` | `bg-slate-50` | `text-slate-600` | `border-slate-200` | clipboard (U+1F4CB) |
| `reference` | `bg-emerald-50` | `text-emerald-700` | `border-emerald-200` | books (U+1F4DA) |
| *(default)* | `bg-slate-50` | `text-slate-600` | `border-slate-200` | page (U+1F4C4) |

### Rendering Logic

Returns `null` if `docs` is falsy or empty.

Otherwise renders:
1. **Header**: Document SVG icon + "RELATED DOCUMENTS" label.
2. **Chip container**: `flex flex-wrap gap-2` layout containing one chip per document.

### Per-Document Rendering

Each chip is conditionally rendered as either an `<a>` or a `<span>`:

| Condition | Element | Extra Classes |
|-----------|---------|---------------|
| `doc.url` exists | `<a>` with `target="_blank"` | `hover:shadow-sm transition-all duration-150` + external-link SVG icon appended |
| `doc.url` is falsy | `<span>` | No hover effect, no link icon |

### Chip Structure

All chips share the base classes:
```
inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border
```
Plus the category-specific `bg`, `text`, and `border` classes.

Contents: emoji icon + document title (+ external-link icon for URL chips).

### Key

Each chip uses `key={doc.docId}`.

---

## ConfidenceFooter.jsx

**Path**: `src/components/ConfidenceFooter.jsx`
**Role**: Displays a colored confidence level badge and pipeline retrieval statistics.

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `confidence` | `Confidence` | Yes | Confidence level and explanation |
| `metadata` | `ResponseMetadata` | No | Pipeline stats (optional, footer renders without it) |

### Confidence Object Shape

```js
{
  level: "High" | "Medium" | "Low",   // Confidence tier
  reason: string                       // Explanation (e.g., "Multiple relevant sources found")
}
```

### ResponseMetadata Object Shape

```js
{
  chunksRetrieved: number,  // Total chunks returned from ChromaDB
  chunksUsed: number,       // Chunks matched by citation extraction
  latencyMs: number,        // Total pipeline latency in milliseconds
  model: string,            // LLM model identifier
  query: string             // Original query text
}
```

### Confidence Style Mapping

| Level | Background | Text | Border | Dot Color |
|-------|-----------|------|--------|-----------|
| `High` | `bg-emerald-50` | `text-emerald-700` | `border-emerald-300` | `bg-emerald-500` |
| `Medium` | `bg-amber-50` | `text-amber-700` | `border-amber-300` | `bg-amber-500` |
| `Low` | `bg-rose-50` | `text-rose-700` | `border-rose-300` | `bg-rose-500` |

Falls back to `Medium` style if the confidence level does not match any key.

### Rendering Logic

Returns `null` if `confidence` is falsy.

Layout is a flexbox row with `justify-between`:

**Left side**:
- Colored badge: `rounded-full` pill containing a colored dot (`w-1.5 h-1.5 rounded-full`) + level text (e.g., "High confidence").
- Reason text: `text-xs text-slate-400` shown to the right of the badge, only if `confidence.reason` is truthy.

**Right side** (only if `metadata` is truthy):
- Monospace stats: `text-xs text-slate-400 font-mono`
- Format: `{chunksRetrieved} retrieved . {chunksUsed} used . {latencySeconds}s`
- Latency is converted from milliseconds: `(metadata.latencyMs / 1000).toFixed(1)`

### Container Styling

```
border-t border-slate-100 px-5 py-3 flex items-center justify-between bg-slate-50/50 rounded-b-xl
```

Note: uses `border-slate-100` (lighter than other section dividers which use `border-slate-200`) and `bg-slate-50/50` (semi-transparent background).

---

## Loading.jsx

**Path**: `src/components/Loading.jsx`
**Role**: Animated loading indicator displayed while a query is in flight.

### Props

None. This is a stateless, propless component.

### Rendering

A card matching the `ResponseCard` styling (`bg-white rounded-xl border border-slate-200 shadow-sm`) with centered content:

1. **Three bouncing dots**: Each is `w-2 h-2 bg-sky-400 rounded-full` with the `animate-bounce` Tailwind animation.
2. **Status text**: "Searching knowledge base..." in `text-sm text-slate-400`.

### Bounce Stagger

The three dots use inline `animationDelay` styles to create a wave effect:

| Dot | Delay |
|-----|-------|
| 1st | `0ms` |
| 2nd | `150ms` |
| 3rd | `300ms` |

### Layout

```
div.bg-white.rounded-xl.p-8
└── div.flex.items-center.justify-center.gap-3
    ├── div.flex.gap-1 (three dots)
    └── span (status text)
```

No internal state, no effects, no refs. Renders immediately with no delay.
