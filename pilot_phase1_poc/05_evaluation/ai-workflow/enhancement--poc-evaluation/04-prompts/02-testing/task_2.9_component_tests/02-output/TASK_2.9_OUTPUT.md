# Task 2.9 Output — Component Unit Tests

**Task:** 2.9 — Component unit tests
**Phase:** Phase 2 — Systematic Testing
**Status:** PASS
**Date:** 2026-02-09 (updated with link accessibility tests)

---

## Summary

Set up **Vitest + React Testing Library** test infrastructure from scratch and wrote **33 component unit tests** across 5 test files. The client had no test setup — this task installed dependencies, configured Vitest with jsdom environment, and created tests for all 5 testable components.

**Update**: Added 6 link accessibility tests verifying `target="_blank"`, `rel="noopener noreferrer"`, and valid `https://` href on all external links in Sources, Related Documents, and the full ResponseCard.

**Frontend: 33/33 tests pass across 5 files. Backend: 162/162 unchanged. Combined: 195 total.**

---

## Infrastructure Created

### Dependencies Installed
```
vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

### Configuration
- **`vite.config.js`**: Added `test` block with `globals: true`, `environment: 'jsdom'`, `setupFiles: './src/test/setup.js'`
- **`package.json`**: Added `"test": "vitest run"` and `"test:watch": "vitest"` scripts
- **`src/test/setup.js`**: Imports `@testing-library/jest-dom` for DOM matchers

---

## Test Files Created

### SourcesSection.test.jsx (9 tests)
| Test | What It Validates |
|------|-------------------|
| returns null when sources is empty array | Null rendering on `[]` |
| returns null when sources is undefined | Null rendering on `undefined` |
| renders correct number of source links | 2 `<a>` elements with correct `href` and `target="_blank"` |
| displays title with section when provided | "Export Guide — Documents" rendered |
| displays title without section separator when section is null | No ` — ` separator |
| extracts domain from URL correctly | `customs.gov.sg` extracted from both URLs |
| renders section header | "Sources" header text |
| **all source links open in new tab with secure rel** | Every `<a>` has `target="_blank"` and `rel="noopener noreferrer"` |
| **all source links have valid https href** | Every `<a>` href starts with `https://` |

### RelatedDocsSection.test.jsx (9 tests)
| Test | What It Validates |
|------|-------------------|
| returns null when docs is empty array | Null rendering on `[]` |
| returns null when docs is undefined | Null rendering on `undefined` |
| renders correct number of doc chips | All 4 category docs rendered |
| renders link for docs with URL | 2 `<a>` elements for docs with URLs |
| renders span (not link) for docs without URL | No links when URL is null |
| renders section header | "Related Documents" header text |
| **all doc links open in new tab with secure rel** | Every `<a>` has `target="_blank"` and `rel="noopener noreferrer"` |
| **all doc links have valid https href** | Every `<a>` href starts with `https://` |
| **links include external-link icon SVG** | Every `<a>` (not `<span>`) contains an SVG element |

### ConfidenceFooter.test.jsx (7 tests)
| Test | What It Validates |
|------|-------------------|
| returns null when confidence is undefined | Null rendering |
| renders High confidence badge | "High confidence" text |
| renders Medium confidence badge | "Medium confidence" text |
| renders Low confidence badge | "Low confidence" text |
| displays confidence reason | Reason text rendered |
| renders metadata stats when provided | "5 retrieved", "3 used", "1.3s" |
| omits metadata section when undefined | No "retrieved" text |

### QueryInput.test.jsx (4 tests)
| Test | What It Validates |
|------|-------------------|
| calls onSubmit with trimmed query | Submits "What is GST?" from "  What is GST?  " |
| disables submit when query is empty | Submit button disabled |
| disables input and submit when loading | Both elements disabled |
| clear button resets query text | Input value cleared to "" |

### ResponseCard.test.jsx (4 tests)
| Test | What It Validates |
|------|-------------------|
| returns null when data is undefined | Null rendering |
| renders answer content | Markdown content appears |
| renders all 4 child sections | Sources, Related Documents, confidence all present |
| **all links in card are accessible** | All links have valid `href`, `target="_blank"`, `rel="noopener noreferrer"` (integration check across Sources + RelatedDocs) |

---

## Link Accessibility Coverage

Every external link in the UI is verified for:
1. **Valid href** — starts with `https://`, not empty or `#`
2. **Opens in new tab** — `target="_blank"` prevents navigating away from app
3. **Security** — `rel="noopener noreferrer"` prevents reverse tabnapping
4. **Visual indicator** — RelatedDocs links include external-link SVG icon

| Component | Links Tested | Attributes Verified |
|-----------|-------------|-------------------|
| SourcesSection | 2 source links | href, target, rel |
| RelatedDocsSection | 2 doc links (with URL) | href, target, rel, SVG icon |
| ResponseCard (integration) | 4+ links (sources + relatedDocs combined) | href, target, rel |

---

## Issues Found and Fixed

1. **SourcesSection domain extraction test** — both mock sources shared the same domain (`customs.gov.sg`), causing `getByText` to fail with "multiple elements found". Fixed by using `getAllByText` and asserting length === 2.

2. **ResponseCard mock data expanded** — original mock had only 1 source and 1 relatedDoc, insufficient to test link accessibility across both sections. Added 2nd source (different URL) and 2 more relatedDocs (one with URL, one null) to verify the integration test properly iterates all links.

---

## Test Results

| Suite | Tests | Status |
|-------|-------|--------|
| SourcesSection.test.jsx | 9 | PASS |
| RelatedDocsSection.test.jsx | 9 | PASS |
| ConfidenceFooter.test.jsx | 7 | PASS |
| QueryInput.test.jsx | 4 | PASS |
| ResponseCard.test.jsx | 4 | PASS |
| **Frontend Total** | **33** | **PASS** |
| Backend (unchanged) | 162 | PASS |
| **Combined Total** | **195** | **PASS** |

---

## Validation

| Criterion | Status |
|-----------|--------|
| All Answer section tests pass | PASS (via ResponseCard) |
| All Sources section tests pass | PASS (9/9) |
| All Related Documents section tests pass | PASS (9/9) |
| All Confidence Footer tests pass | PASS (7/7) |
| All link accessibility tests pass | PASS (6/6 new tests) |
| No console errors during test run | PASS |
| Backend tests unaffected | PASS (162/162) |

---

## Next Steps

- Task 2.10: Visual verification via Chrome DevTools MCP (COMPLETE)
- Task 2.11: Define expected-answer baselines (50 queries)
