# Task 2.10 Prompt — Visual Verification via Chrome DevTools MCP

**Phase:** Phase 2 — Systematic Testing (Layer 4: Visual/Integration)
**Task:** 2.10 — Visual verification via Chrome DevTools MCP
**Dependencies:** Task 2.9 (component unit tests) — COMPLETE

---

## Persona

You are a QA engineer performing interactive visual verification of a RAG-based co-pilot UI. You will use Chrome DevTools MCP tools to interact with the live application in the browser, verify rendering correctness, and capture screenshots for documentation.

## Context

### Application Architecture
- **Backend**: Express.js on `http://localhost:3000` (start with `npm start` from `05_evaluation/`)
- **Frontend**: React + Vite on `http://localhost:5173` (start with `npm run dev` from `05_evaluation/client/`)
- **Proxy**: Vite proxies `/api` requests to `localhost:3000`
- **API endpoint**: `POST /api/query` with `{ "query": "..." }` body

### UI Structure (4-section Response Card)
After submitting a query, the `ResponseCard` renders 4 sections:

1. **Answer Section** — Markdown-rendered response text with citations like `[Title > Section]`
2. **Sources Section** — Clickable external URLs with org name + domain subtitle (e.g., "Singapore Customs · customs.gov.sg")
3. **Related Documents Section** — Color-coded category chips: `regulatory` (blue), `carrier` (green), `reference` (amber), `internal` (slate)
4. **Confidence Footer** — Colored badge (green=High, amber=Medium, rose=Low), reason text, metadata stats (chunks retrieved/used, latency)

### Components (in `client/src/components/`)
| Component | Role |
|-----------|------|
| `QueryInput.jsx` | Search bar with submit button, clear button, loading states |
| `ResponseCard.jsx` | Orchestrator — renders answer markdown + 3 child sections |
| `SourcesSection.jsx` | Clickable source links with title, org, domain |
| `RelatedDocsSection.jsx` | Category-colored document chips |
| `ConfidenceFooter.jsx` | Confidence badge + reason + metadata stats |
| `Loading.jsx` | Pulsing loading animation |

### Key Queries for Testing
| Query | Type | Expected Behavior |
|-------|------|-------------------|
| "What is the GST rate for imports into Singapore?" | In-scope (regulatory) | Answer with citations, High confidence, Sources from customs.gov.sg |
| "What documents do I need for exporting from Singapore?" | In-scope (regulatory) | Multiple sources, Related Documents chips |
| "What is the freight rate to Jakarta?" | Out-of-scope | Graceful decline, Low confidence badge |

## Task

Perform interactive visual verification of the Waypoint Co-Pilot UI using Chrome DevTools MCP. This is a manual visual check, not automated Selenium testing.

### Pre-requisites
1. Start the Express backend: `cd pilot_phase1_poc/05_evaluation && npm start`
2. Start the React dev server: `cd pilot_phase1_poc/05_evaluation/client && npm run dev`
3. Both servers must be running simultaneously

### Verification Steps

#### Step 1: Initial Page Load
- Navigate Chrome to `http://localhost:5173`
- Verify: Waypoint Co-Pilot header visible with logo
- Verify: Search input field present and enabled
- Verify: Placeholder text visible ("Ask a question about freight forwarding...")
- Verify: Footer text "Waypoint Phase 1 POC" visible
- **Screenshot**: initial empty state

#### Step 2: In-Scope Query — Regulatory
- Type query: "What is the GST rate for imports into Singapore?"
- Click Submit (or press Enter)
- Wait for response to load
- Verify Answer Section:
  - Markdown renders correctly (headers, bold, lists if present)
  - Citation references appear as `[Title > Section]` in text
- Verify Sources Section:
  - "Sources" header visible
  - At least 1 clickable link with `href` and `target="_blank"`
  - Org name and domain subtitle displayed
- Verify Related Documents Section:
  - "Related Documents" header visible
  - Category chips rendered (regulatory = blue tones)
- Verify Confidence Footer:
  - Confidence badge visible (expect High = green)
  - Reason text displayed
  - Metadata stats: "X retrieved", "Y used", latency in seconds
- **Screenshot**: full response card

#### Step 3: In-Scope Query — Export Documents
- Clear input, type: "What documents do I need for exporting from Singapore?"
- Submit and wait
- Verify: Multiple sources appear
- Verify: Related Documents chips present
- Verify: Confidence badge (expect High or Medium)

#### Step 4: Out-of-Scope Query
- Clear input, type: "What is the freight rate to Jakarta?"
- Submit and wait
- Verify: Response indicates inability to provide live rates
- Verify: Confidence badge shows Low (rose/red tones)
- **Screenshot**: out-of-scope response

#### Step 5: Layout & Console
- Verify viewport width is ≥1280px (desktop)
- Check max-width constraint (content centered in `max-w-3xl` = 768px container)
- Check browser console for errors — no React warnings or JS errors
- **Screenshot**: if any console errors found

### Output Report
Create `TASK_2.10_OUTPUT.md` at the output location with:
- Summary of what was verified
- Screenshot references (file paths)
- Pass/fail for each validation criterion
- Any issues found (with details)
- Console error check results

## Format

### Screenshots
Save to `pilot_phase1_poc/05_evaluation/ai-workflow/enhancement--poc-evaluation/04-prompts/02-testing/task_2_10/02-output/screenshots/`

Naming:
- `01_initial_state.png`
- `02_gst_query_response.png`
- `03_export_docs_response.png` (optional)
- `04_oos_query_response.png`
- `05_console_check.png` (if errors)

### Validation Checklist (for output report)
```
- [ ] App loads at localhost:5173 without errors
- [ ] Header shows "Waypoint Co-Pilot" with logo
- [ ] QueryInput renders with placeholder text
- [ ] In-scope query returns 4-section response card
- [ ] Answer section renders markdown content
- [ ] Sources section shows clickable URLs with org/domain
- [ ] Related Documents shows category chips
- [ ] Confidence Footer shows colored badge + reason + stats
- [ ] Out-of-scope query shows Low confidence / graceful decline
- [ ] No console errors (React warnings, JS errors)
- [ ] Layout centered at 1280px+ desktop width
```
