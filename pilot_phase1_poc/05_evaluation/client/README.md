# Client — React Frontend (4-Section Response Card)

React + Vite frontend for the Waypoint co-pilot. Displays query results in a structured 4-section response card: answer, sources, related documents, and confidence indicator.

## File Structure

| File | Purpose |
|------|---------|
| `src/App.jsx` | Root component, layout, state management |
| `src/main.jsx` | Vite entry point |
| `src/api/query.js` | API client for backend /api/query endpoint |
| `src/types.js` | Shared type definitions |
| `src/components/QueryInput.jsx` | Search input with submit handling |
| `src/components/ResponseCard.jsx` | Main response container (4-section card) |
| `src/components/SourcesSection.jsx` | Cited sources with document attribution |
| `src/components/RelatedDocsSection.jsx` | Related knowledge base documents |
| `src/components/ConfidenceFooter.jsx` | Confidence level indicator |
| `src/components/Loading.jsx` | Loading state animation |

Component tests are located in `src/components/__tests__/`.

## Quick Start

```bash
cd pilot_phase1_poc/05_evaluation/client
npm install
npm run dev      # Dev server on port 5173
npm run build    # Production build to dist/
npm test         # Run Vitest component tests
```

## Detailed Docs

See [detailed documentation](../documentation/codebase/frontend/overview.md) for component hierarchy, state flow, and styling.
