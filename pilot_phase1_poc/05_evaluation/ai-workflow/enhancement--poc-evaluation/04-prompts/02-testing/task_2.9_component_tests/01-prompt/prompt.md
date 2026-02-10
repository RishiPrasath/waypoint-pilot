# Task 2.9 Prompt — Component Unit Tests

## Persona
Senior frontend engineer setting up Vitest + React Testing Library and writing component unit tests for the 4-section response card.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Phase**: Phase 2 — Systematic Testing (Layer 4: React Frontend)
- **Dependencies**: CP2 (UX Redesign complete)
- **Blocks**: T2.10 (visual verification)
- **Current state**: No test infrastructure exists in `client/` — no Vitest, no `@testing-library/react`, no test script, no test files

### What Happened
The roadmap says "validation of tests created in T1.3" but T1.3 created the components without test files. The TDD was implicit (manual visual verification during development). This task must **create** the test setup and write component tests.

### Component Inventory (6 components in `client/src/components/`)

| Component | Props | Key Behavior |
|-----------|-------|-------------|
| **QueryInput** | `onSubmit(query)`, `loading` | Form submit, clear button, disabled states, auto-focus |
| **Loading** | none | Static animated dots |
| **ResponseCard** | `data: QueryResponse` | Renders 4 sections, returns null if no data, markdown rendering |
| **SourcesSection** | `sources: Source[]` | Returns null if empty, URL domain extraction, external links |
| **RelatedDocsSection** | `docs: RelatedDoc[]` | Returns null if empty, category color mapping, link vs span |
| **ConfidenceFooter** | `confidence`, `metadata` | Returns null if undefined, color-coded badge, stats formatting |

### Type Definitions (from `client/src/types.js`)
```javascript
Source: { title, org, url, section: string|null }
RelatedDoc: { title, category: "regulatory"|"carrier"|"internal"|"reference", docId, url: string|null }
Confidence: { level: "High"|"Medium"|"Low", reason: string }
ResponseMetadata: { query, chunksRetrieved, chunksUsed, latencyMs, model }
```

### Dependencies
- React 19.2, Vite 7.2
- `react-markdown` + `remark-gfm` (in ResponseCard)
- Tailwind CSS for styling

## Task

### Step 1: Install Test Dependencies
```bash
cd client
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

### Step 2: Configure Vitest
Add to `vite.config.js`:
```javascript
test: {
  globals: true,
  environment: 'jsdom',
  setupFiles: './src/test/setup.js',
}
```

Add test script to `package.json`:
```json
"test": "vitest run",
"test:watch": "vitest"
```

Create `client/src/test/setup.js`:
```javascript
import '@testing-library/jest-dom';
```

### Step 3: Write Component Tests

Create test files alongside components in `client/src/components/__tests__/`:

#### 3a. SourcesSection.test.jsx (7-8 tests)
- Returns null when sources is empty array
- Returns null when sources is undefined
- Renders correct number of source links
- Extracts domain from URL correctly
- Shows section when provided, omits when null
- Renders section header ("Sources")
- **All source links open in new tab** — every `<a>` has `target="_blank"` and `rel="noopener noreferrer"`
- **All source links have valid href** — every `<a>` has a non-empty `href` starting with `https://`

#### 3b. RelatedDocsSection.test.jsx (7-8 tests)
- Returns null when docs is empty array
- Returns null when docs is undefined
- Renders correct number of doc chips
- Applies correct category colors/emojis (regulatory=blue/🏛️, carrier=amber/🚢, internal=slate/📋, reference=emerald/📚)
- Renders link `<a>` when url exists, `<span>` when url is null
- Renders section header ("Related Documents")
- **All doc links open in new tab** — every `<a>` has `target="_blank"` and `rel="noopener noreferrer"`
- **All doc links have valid href** — every `<a>` has a non-empty `href` starting with `https://`
- **External link icon** — links (not spans) include an external-link SVG indicator

#### 3c. ConfidenceFooter.test.jsx (4-5 tests)
- Returns null when confidence is undefined
- Renders confidence level badge with correct text
- Applies correct color class per level (High=emerald, Medium=amber, Low=rose)
- Renders metadata stats when provided
- Omits metadata section when metadata is undefined

#### 3d. QueryInput.test.jsx (3-4 tests)
- Calls onSubmit with trimmed query on form submit
- Disables submit when query is empty
- Disables submit and input when loading is true
- Clear button resets query text

#### 3e. ResponseCard.test.jsx (3-4 tests)
- Returns null when data is undefined
- Renders answer section with markdown content
- Renders all 4 child sections when data is populated
- **Source and RelatedDoc links are accessible** — within the full card, all links from Sources and Related Documents have correct `href`, `target="_blank"`, and `rel="noopener noreferrer"` attributes

**IMPORTANT — Link Accessibility Requirements:**
Every external link in SourcesSection and RelatedDocsSection must be verified for:
1. `href` attribute with a valid URL (not empty, not "#")
2. `target="_blank"` so it opens in a new tab (users should not navigate away from the app)
3. `rel="noopener noreferrer"` for security (prevents reverse tabnapping)
4. Use `getAllByRole('link')` to find links, then iterate and assert all three attributes on each

Use distinct domains in mock data (e.g., `customs.gov.sg`, `maersk.com`, `iccwbo.org`) to ensure each link has a unique, verifiable `href`.

**Target: ~25-30 tests total across 5 files.**

### Step 4: Run and Iterate
```bash
cd client && npm test
```

Fix any failures until all pass.

## Format
- **Create**: Vitest config, setup file, 5 test files
- **Modify**: `client/package.json` (test script), `client/vite.config.js` (test config)
- **Output**: `TASK_2.9_OUTPUT.md` with test inventory and results
- **Validation**: `cd client && npm test` — all green
