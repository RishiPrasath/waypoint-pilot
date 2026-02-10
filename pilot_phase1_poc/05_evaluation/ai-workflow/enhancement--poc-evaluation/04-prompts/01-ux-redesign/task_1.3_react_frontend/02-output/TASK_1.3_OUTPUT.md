# Task 1.3 Output — Implement New React Frontend

**Task:** 1.3 — Implement new React frontend (4-section response card)
**Phase:** Phase 1 — UX Redesign
**Status:** COMPLETE
**Date:** 2026-02-09

---

## Summary

Refactored the React frontend from a simple text-based response into a structured 4-section response card matching the UX mockup. Created 4 new components (`SourcesSection`, `RelatedDocsSection`, `ConfidenceFooter`, `ResponseCard`), updated 2 existing components (`Loading`, `App`), deleted 3 old components and 1 unused CSS file. Added `remark-gfm` for GFM markdown support. Fixed a backend bug where `source_urls: "N/A"` was rendered as a link. Build succeeds, visual verification passed via Chrome DevTools MCP.

---

## New Components

### `SourcesSection.jsx`
- **Props:** `{ sources }` — array of `{ title, org, url, section }`
- **Behavior:** Renders clickable external URLs with title + section, org + domain subtitle
- **Null guard:** Returns `null` if sources is empty or undefined
- **Styling:** Link icon header, sky-blue icon boxes, hover:bg-sky-50 transitions

### `RelatedDocsSection.jsx`
- **Props:** `{ docs }` — array of `{ title, category, docId, url }`
- **Behavior:** Renders category-tagged document chips with color coding
- **Category colors:** regulatory=blue, carrier=amber, internal=slate, reference=emerald
- **Link handling:** Chips with `url` render as `<a>` with external link icon; chips without `url` render as `<span>`
- **Null guard:** Returns `null` if docs is empty or undefined

### `ConfidenceFooter.jsx`
- **Props:** `{ confidence, metadata }` — confidence `{ level, reason }`, metadata `{ chunksRetrieved, chunksUsed, latencyMs }`
- **Behavior:** Left side = colored dot + badge + reason; Right side = monospace stats
- **Confidence styles:** High=emerald, Medium=amber, Low=rose
- **Null guard:** Returns `null` if confidence is undefined

### `ResponseCard.jsx`
- **Props:** `{ data }` — full API response object
- **Behavior:** Assembles 4 sections in a card wrapper
- **Markdown:** Uses `react-markdown` + `remark-gfm` with custom Tailwind component mapping
- **Component mapping:** h3, p, ol, ul, li, strong, em, blockquote, code — all with mockup-matching Tailwind classes
- **Null guard:** Returns `null` if data is undefined

---

## Updated Components

### `Loading.jsx`
- **Before:** Spinner SVG with 200ms delay logic, `useState`/`useEffect` hooks
- **After:** 3 bouncing sky-blue dots with staggered animation delays (0ms, 150ms, 300ms), no delay logic, matches card styling (rounded-xl border shadow-sm)

### `App.jsx`
- **Before:** Imported `Response`, had card wrapper around response area, flat sky-500 header icon
- **After:** Imports `ResponseCard` instead, no outer card wrapper (ResponseCard provides its own), gradient header icon (`bg-gradient-to-br from-sky-500 to-blue-600`), inline error display with rose styling, `space-y-5` layout

---

## Deleted Components

| File | Replaced By |
|------|-------------|
| `Citations.jsx` | `SourcesSection.jsx` |
| `Confidence.jsx` | `ConfidenceFooter.jsx` |
| `Response.jsx` | `ResponseCard.jsx` |
| `App.css` | Unused (all Tailwind) |

---

## Dependencies Added

| Package | Version | Purpose |
|---------|---------|---------|
| `remark-gfm` | ^4.0.1 | GitHub Flavored Markdown (tables, strikethrough, autolinks) |

---

## Backend Bug Fix

**Issue:** Internal documents with `source_urls: "N/A"` in metadata were rendered as clickable links pointing to `http://localhost:5173/N/A`.

**Fix:** Updated URL filtering in both `buildSources()` and `buildRelatedDocs()` in `citations.js` to reject non-HTTP values:
```javascript
.filter(u => u && u !== 'N/A' && u.startsWith('http'))
```

**Impact:** Internal documents now correctly render as `<span>` chips (no link) instead of broken `<a>` tags. All 119 tests still pass.

---

## Design Decisions

1. **Hybrid markdown rendering** — `react-markdown` + `remark-gfm` for robust parsing, custom Tailwind component mapping for visual fidelity to mockup
2. **No outer card wrapper in App** — `ResponseCard` owns its own card styling, preventing double-border issues
3. **Null guards on all sections** — Each section returns `null` independently, so the card gracefully handles missing data (e.g., no sources, no related docs)
4. **Unicode emoji for category icons** — Used Unicode escape sequences in JSX to avoid encoding issues across platforms
5. **Domain extraction** — Simple string replace + split approach matches mockup (no URL parsing library needed)

---

## Visual Verification

Verified via Chrome DevTools MCP at `http://localhost:5173`:

### Empty State
- Search input with placeholder text
- Gradient header icon (sky-to-blue)
- "Ask a question..." prompt text
- Footer visible

### Query: "What documents do I need to import goods into Singapore?"
- **Section 1 (Answer):** Markdown rendered with h3 headers, bold terms, bullet lists, clean typography
- **Section 2 (Sources):** Link icon + "SOURCES" label, clickable URL "Singapore Import Procedures" with "Singapore Customs · customs.gov.sg" subtitle
- **Section 3 (Related Docs):** 9 category chips — blue (regulatory), slate (internal), emerald (reference), amber (carrier) — all with correct colors and external link icons
- **Section 4 (Confidence):** Rose "Low confidence" badge with dot, reason text, monospace "10 retrieved · 1 used · 1.9s"

### Query: "What is the GST rate for imports into Singapore?"
- **Section 1 (Answer):** Bold heading + paragraph, concise response
- **Section 2 (Sources):** Correctly hidden (no matched citations with URLs)
- **Section 3 (Related Docs):** 5 chips — regulatory (blue) + reference (emerald)
- **Section 4 (Confidence):** Amber "Medium confidence" badge + stats

### Loading State
- Bouncing dots animation with "Searching knowledge base..." text (confirmed via brief visibility during query submission)

---

## Issues

1. **N/A URL bug** — Discovered and fixed during visual verification. Internal docs with `source_urls: "N/A"` metadata were rendering as broken links. Fixed by adding URL validation filter in both `enrichCitations()` and `buildRelatedDocs()`.

---

## Validation

| Criterion | Status |
|-----------|--------|
| `remark-gfm` installed | Done |
| `SourcesSection.jsx` created — renders clickable URLs with org + domain subtitle | Done |
| `RelatedDocsSection.jsx` created — renders category chips with correct colors/icons | Done |
| `ConfidenceFooter.jsx` created — renders colored badge + metadata stats | Done |
| `ResponseCard.jsx` created — assembles all 4 sections with react-markdown + remark-gfm | Done |
| `Loading.jsx` updated — bouncing dots animation | Done |
| `App.jsx` updated — uses ResponseCard, gradient header icon | Done |
| Old components deleted (Citations, Confidence, Response, App.css) | Done |
| `npm run build` succeeds (no compilation errors) | Done |
| `npm test` — 119/119 green | Done |
| Visual verification via Chrome DevTools MCP — all 4 sections visible | Done |
| Loading state shows bouncing dots | Done |
| Empty state renders correctly | Done |
| Category chip colors match mockup | Done |
| Confidence badge colors match mockup | Done |

---

## Next Steps

- **Task 1.4**: Add Layer 1 inline documentation (JSDoc/docstrings) — depends on this task
