# Task 5.2 — Build Selenium Demo Script

## Persona
QA automation engineer building a repeatable demo capture script for the Waypoint POC presentation. The script must produce high-quality screenshots suitable for embedding in a React presentation deck.

## Context

### System Under Test
- **Frontend**: React + Vite at `http://localhost:5173`
- **Backend**: Express API at `http://localhost:3000`
- Both must be running before the script executes

### UI Structure (from `client/src/`)

**QueryInput** (`components/QueryInput.jsx`):
- `<input type="text" aria-label="Search query" placeholder="Ask about shipping, customs, carriers...">` — text input
- `<button type="submit" aria-label="Search">Search</button>` — submit button
- `<button aria-label="Clear input">` — clear button (X icon, visible when input has text)

**Loading** (`components/Loading.jsx`):
- Bouncing dots + "Searching knowledge base..." text
- Appears while API call is in flight

**ResponseCard** (`components/ResponseCard.jsx`):
- Outer container: `div.bg-white.rounded-xl.border.border-slate-200.shadow-sm`
- Section 1 — Answer: `div.px-5.py-5` containing rendered markdown
- Section 2 — Sources: `SourcesSection` with clickable URLs (hidden if no external sources)
- Section 3 — Related Docs: `RelatedDocsSection` with category chips
- Section 4 — Confidence Footer: `ConfidenceFooter` with colored badge + metadata

**Page Layout**:
- Header: "Waypoint Co-Pilot" with gradient icon
- Max width: `max-w-3xl mx-auto`
- Footer: "Waypoint Phase 1 POC"

### Demo Queries (from Task 5.1 — `demo/demo_queries.md`)

| Demo # | ID | Query Text | Type |
|--------|-----|-----------|------|
| 1 | Q-01 | What documents are needed for sea freight Singapore to Indonesia? | Happy path |
| 2 | Q-11 | What's the GST rate for imports into Singapore? | Happy path |
| 3 | Q-13 | Is Certificate of Origin required for Thailand? | Happy path |
| 4 | Q-24 | How do I submit VGM to Maersk? | Happy path |
| 5 | Q-14 | What permits are needed to import cosmetics to Indonesia? | Happy path |
| 6 | Q-03 | What's the difference between FCL and LCL? | Happy path |
| 7 | Q-31 | What's our standard delivery SLA for Singapore? | Happy path |
| 8 | Q-42 | Where is my shipment right now? | OOS decline |
| 9 | Q-46 | What's the weather forecast for shipping? | OOS decline |
| 10 | Q-04 | When is the SI cutoff for this week's Maersk sailing? | Boundary |

### Dependencies
- Selenium (separate from core pipeline — Decision #8)
- Chrome + ChromeDriver (must match Chrome version)
- Backend + frontend running before script execution

## Task

Create an automated Selenium script that runs all 10 demo queries through the React UI, capturing screenshots at key states.

### Files to Create

#### 1. `demo/selenium/requirements.txt`
```
selenium>=4.15.0
```

#### 2. `demo/selenium/demo_script.py`

**Script Requirements**:

1. **Setup**:
   - Use Chrome in non-headless mode (screenshots need to be visually accurate)
   - Set window size to 1400x900 (desktop, wider than max-w-3xl to show full card with margins)
   - Navigate to `http://localhost:5173`
   - Wait for page load (check for "Waypoint Co-Pilot" header text)

2. **For each of the 10 demo queries**:
   a. **Clear previous state**: If there's existing text in the input, click the Clear button (aria-label="Clear input") or select-all + delete. Wait for any previous response card to disappear.
   b. **Type query**: Find input by `aria-label="Search query"`, clear it, type the query text
   c. **Screenshot — "typed" state**: Capture screenshot showing the query in the input box before submission. Save as `demo_{NN}_typed.png` (e.g., `demo_01_typed.png`)
   d. **Submit**: Click the Search button (aria-label="Search" or type="submit")
   e. **Wait for response**: Wait for the Loading component to disappear AND one of:
      - The ResponseCard to appear (`.bg-white.rounded-xl.border` within main) for in-scope queries
      - OR the decline message to appear for OOS queries
      - Use `WebDriverWait` with explicit waits (up to 15 seconds)
   f. **Screenshot — "response" state**: Capture screenshot showing the full response. Save as `demo_{NN}_response.png`
   g. **Pause**: Wait 2 seconds between queries (breathing room for next cycle)

3. **Screenshot Output Directory**:
   - Save to `demo/presentation/public/demo/screenshots/`
   - Create directory if it doesn't exist
   - Naming: `demo_01_typed.png`, `demo_01_response.png`, `demo_02_typed.png`, etc.

4. **Full-Page Screenshots for Rich Responses**:
   - For queries with long responses (Demo 1, 5 especially), use `driver.execute_script("return document.body.scrollHeight")` to check if the page scrolls
   - If content extends below the viewport, take an additional `demo_{NN}_response_full.png` using full-page screenshot capability or scroll-and-stitch approach

5. **Error Handling**:
   - If a query times out (no response after 15 seconds), log the error, capture a screenshot of the error state (`demo_{NN}_error.png`), and continue with the next query
   - If the input element can't be found, wait and retry once before failing
   - Print progress to console: `[1/10] Demo 1: Typing query...`, `[1/10] Demo 1: Response captured (2.1s)`

6. **Summary Report**:
   - At the end, print a summary: how many queries succeeded, failed, average response time
   - Save summary to `demo/selenium/demo_results.txt`

### Selenium Selectors Reference

| Element | Selector Strategy | Value |
|---------|-------------------|-------|
| Query input | CSS / aria-label | `input[aria-label="Search query"]` |
| Submit button | CSS / type | `button[type="submit"]` |
| Clear button | CSS / aria-label | `button[aria-label="Clear input"]` |
| Loading indicator | Text presence | `"Searching knowledge base..."` |
| Response card | CSS | `.bg-white.rounded-xl.border.border-slate-200.shadow-sm.overflow-hidden` |
| Error display | CSS | `.bg-rose-50.border.border-rose-200` |
| Header text | Text | `"Waypoint Co-Pilot"` |

### Wait Strategy
```python
# Wait for response: Loading gone AND (response card visible OR decline text visible)
WebDriverWait(driver, 15).until(
    EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Searching knowledge base')]"))
)
# Then check for response card
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.rounded-xl.border.shadow-sm.overflow-hidden"))
)
```

## Format

### Validation
- [ ] `demo/selenium/requirements.txt` created with selenium dependency
- [ ] `demo/selenium/demo_script.py` created and runs without import errors
- [ ] Script captures 2 screenshots per query (typed + response) = 20+ screenshots
- [ ] Screenshots saved to `demo/presentation/public/demo/screenshots/`
- [ ] Screenshots are 1400px wide (desktop resolution)
- [ ] Script handles response delays gracefully (15s timeout per query)
- [ ] Script handles errors without crashing (continues to next query)
- [ ] Console output shows progress for each query
- [ ] Summary report saved to `demo/selenium/demo_results.txt`
- [ ] Tested with at least 2 queries to verify end-to-end flow

### Execution Commands
```bash
cd pilot_phase1_poc/05_evaluation

# Install (one-time, into existing venv)
venv/Scripts/pip install -r demo/selenium/requirements.txt

# Pre-requisite: start backend + frontend in separate terminals
# Terminal 1: npm start
# Terminal 2: cd client && npm run dev

# Run demo script
venv/Scripts/python demo/selenium/demo_script.py
```
