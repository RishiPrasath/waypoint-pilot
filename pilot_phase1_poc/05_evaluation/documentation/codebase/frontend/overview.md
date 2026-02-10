# Frontend Architecture Overview

**Location**: `pilot_phase1_poc/05_evaluation/client/`

## Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.2.0 | UI component library |
| Vite | 7.2.4 | Build tool and dev server |
| Tailwind CSS | 3.4.19 | Utility-first CSS framework |
| react-markdown | 10.1.0 | Markdown rendering in Answer section |
| remark-gfm | 4.0.1 | GitHub Flavored Markdown support (tables, strikethrough) |
| Vitest | 4.0.18 | Unit test framework |
| Testing Library | 16.3.2 | React component testing utilities |

## Entry Point

`src/main.jsx` renders the `<App />` component inside `React.StrictMode` into the `#root` DOM element. Global styles are imported from `src/index.css` (Tailwind directives).

## Component Tree

```
App
 ├── QueryInput          (search bar + submit button)
 ├── Loading             (bounce animation placeholder)
 ├── ResponseCard        (4-section answer card)
 │   ├── Answer          (inline react-markdown block)
 │   ├── SourcesSection  (external URL links)
 │   ├── RelatedDocsSection (category-colored document chips)
 │   └── ConfidenceFooter   (confidence badge + pipeline stats)
 └── Error display       (inline conditional — not a separate component)
```

All components are functional components. There are no class components in the codebase.

## State Management

State lives entirely in `App.jsx` using React `useState` hooks. There is no Redux, Context API, or external state management library.

| State Variable | Type | Default | Purpose |
|---------------|------|---------|---------|
| `response` | `QueryResponse \| null` | `null` | Full API response object passed to `ResponseCard` |
| `loading` | `boolean` | `false` | Controls loading indicator and input disabled state |
| `error` | `string \| null` | `null` | Error message shown in the error banner |

### Data Flow

1. User types a query in `QueryInput` and submits.
2. `App.handleSubmit` sets `loading=true`, clears `error` and `response`.
3. `submitQuery()` calls `POST /api/query` with an `AbortController` signal.
4. On success: `response` is set, `loading` is cleared.
5. On failure: `error` is set (unless the error is an `AbortError`).
6. `ResponseCard` receives `response` and delegates to its four sub-sections.

No data flows upward from child components except `QueryInput.onSubmit(query)`.

## Styling Approach

- **Framework**: Tailwind CSS utility classes applied directly to JSX elements.
- **No CSS modules**: Zero `.module.css` files. All styling is inline Tailwind.
- **No custom CSS**: Only Tailwind directives in `index.css` (`@tailwind base/components/utilities`).
- **Color scheme**:
  - **Primary**: `sky-500` / `sky-600` (buttons, links, focus rings, loading dots)
  - **Neutrals**: `slate-50` through `slate-900` (backgrounds, text, borders)
  - **Confidence colors**: `emerald` (High), `amber` (Medium), `rose` (Low)
  - **Category colors**: `blue` (regulatory), `amber` (carrier), `slate` (internal), `emerald` (reference)
- **Layout**: Single-column centered layout with `max-w-3xl mx-auto` on header, main, and footer.
- **Card style**: `rounded-xl border border-slate-200 shadow-sm` used on ResponseCard and Loading.

## API Communication

- **Client module**: `src/api/query.js` exports `submitQuery()` and `checkHealth()`.
- **HTTP method**: `fetch` API (no Axios or other HTTP library).
- **Request format**: `POST /api/query` with `Content-Type: application/json` body `{ query: string }`.
- **Abort handling**: Every query creates an `AbortController`. The signal is passed to `fetch()`. `AbortError` exceptions are silently caught (not displayed to the user).
- **No authentication**: No auth tokens, cookies, or API keys required.

## Dev Server Proxy

Configured in `vite.config.js`:

```js
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:3000',
      changeOrigin: true,
    },
  },
}
```

All requests matching `/api/*` are proxied to the Express backend at `localhost:3000`. This avoids CORS issues during development.

## 4-Section Response Card Design (Decision #9)

The response card is divided into four visually distinct sections, separated by `border-t` dividers:

| Section | Component | Content |
|---------|-----------|---------|
| 1. Answer | Inline in `ResponseCard` | Markdown-rendered LLM answer with custom Tailwind typography |
| 2. Sources | `SourcesSection` | Clickable external URLs with org + domain subtitle |
| 3. Related Documents | `RelatedDocsSection` | Category-colored chips with emoji icons |
| 4. Confidence Footer | `ConfidenceFooter` | Colored confidence badge + monospace pipeline stats |

This design separates the answer from its evidence, providing transparency about source attribution and retrieval confidence.

## Test Configuration

Tests use Vitest with jsdom environment, configured in `vite.config.js`:

```js
test: {
  globals: true,
  environment: 'jsdom',
  setupFiles: './src/test/setup.js',
}
```

Test files are co-located with components at `src/components/__tests__/*.test.jsx`. Testing Library (`@testing-library/react` and `@testing-library/user-event`) is used for DOM queries and user interaction simulation.

## Build Commands

```bash
cd pilot_phase1_poc/05_evaluation/client

npm run dev          # Start Vite dev server on port 5173
npm run build        # Production build to dist/
npm run preview      # Preview production build
npm run test         # Run Vitest (single pass)
npm run test:watch   # Run Vitest in watch mode
npm run lint         # ESLint
```

## File Structure

```
client/
├── index.html
├── package.json
├── vite.config.js
├── postcss.config.js
├── tailwind.config.js
├── eslint.config.js
├── src/
│   ├── main.jsx                 # React entry point
│   ├── App.jsx                  # Root component with state management
│   ├── index.css                # Tailwind CSS directives
│   ├── types.js                 # JSDoc type definitions
│   ├── api/
│   │   └── query.js             # API client (submitQuery, checkHealth)
│   ├── components/
│   │   ├── QueryInput.jsx       # Search input with clear + submit
│   │   ├── ResponseCard.jsx     # 4-section answer card
│   │   ├── SourcesSection.jsx   # External source links
│   │   ├── RelatedDocsSection.jsx # Category document chips
│   │   ├── ConfidenceFooter.jsx # Confidence badge + stats
│   │   ├── Loading.jsx          # Bouncing dots animation
│   │   └── __tests__/           # Component test files
│   └── test/
│       └── setup.js             # Vitest setup
└── public/                      # Static assets
```
