# Task 7.2: UI Polish & Testing

## Persona
You are a QA engineer and frontend developer performing end-to-end testing and polish on the Waypoint co-pilot UI. You validate functionality across browsers, ensure accessibility, and fix any issues discovered during testing.

## Context

### Project State
- **Task 7.1 Complete**: React + Tailwind UI created in `client/`
- **Backend Running**: Express API at `http://localhost:3000`
- **Frontend Dev Server**: Vite at `http://localhost:5173`

### Components Created (Task 7.1)
```
client/src/
├── App.jsx              # Main app with state management
├── api/query.js         # Fetch API client
└── components/
    ├── QueryInput.jsx   # Search input with submit/clear
    ├── Response.jsx     # Markdown answer display
    ├── Citations.jsx    # Source links list
    ├── Confidence.jsx   # Color-coded badge
    └── Loading.jsx      # Delayed spinner (200ms)
```

### API Response Format
```json
{
  "answer": "For sea freight export...",
  "citations": [
    {
      "title": "Singapore Export Procedures",
      "section": "Required Documents",
      "matched": true,
      "sourceUrls": ["https://..."]
    }
  ],
  "confidence": {
    "level": "High",
    "reason": "3 relevant sources"
  },
  "metadata": {
    "chunksRetrieved": 10,
    "chunksUsed": 4,
    "latency": { "totalMs": 2340 }
  }
}
```

### References
- Roadmap: `docs/01_implementation_roadmap.md` (Task 7.2)
- Task 7.1 Report: `prompts/07_7.1_react_ui/REPORT.md`
- Backend API: `src/index.js`

### Dependencies
- ✅ Task 7.1: React + Tailwind UI (Complete)
- ✅ Task 6.3: E2E API Test (Complete)

## Task

### Objective
Validate the UI works end-to-end with the live backend, test across browsers, ensure mobile responsiveness, and fix any issues discovered.

### Requirements

#### 1. End-to-End Functional Testing

**Test Queries (10 total)**
Run these queries through the UI and verify correct behavior:

| # | Query | Expected Behavior |
|---|-------|-------------------|
| 1 | "What documents are needed for export from Singapore?" | Answer with citations, High/Medium confidence |
| 2 | "What is the GST rate for imports?" | Factual answer about 9% GST |
| 3 | "Maersk transit times to Europe" | Carrier-specific response |
| 4 | "Explain CIF Incoterms" | Reference/educational content |
| 5 | "What is our SLA for email response?" | Internal policy answer |
| 6 | "HS code for electronics" | Classification guidance |
| 7 | "PIL container tracking" | May have limited info |
| 8 | "" (empty submit) | Should not submit, button disabled |
| 9 | "What is the stock price of Apple?" | Out-of-scope graceful decline |
| 10 | Very long query (200+ chars) | Should handle without UI breaking |

**Validation Checklist**
- [ ] Query submits on button click
- [ ] Query submits on Enter key
- [ ] Loading spinner appears (after 200ms)
- [ ] Response displays with markdown formatting
- [ ] Citations show as clickable links
- [ ] External links open in new tab
- [ ] Internal docs show "(Internal)" badge
- [ ] Confidence badge shows correct color
- [ ] Metadata stats display (chunks, latency)
- [ ] Clear button resets input
- [ ] Input focuses on page load

#### 2. Error State Testing

| Scenario | How to Test | Expected Behavior |
|----------|-------------|-------------------|
| Backend down | Stop `npm start`, submit query | Error message: "Unable to process query" |
| Network timeout | Slow network simulation | Loading persists, eventual error |
| Invalid response | (Manual mock) | Graceful error handling |

**Error UI Requirements**
- Rose/red colored error box
- Clear error message text
- User can try again (input still works)

#### 3. Browser Compatibility

Test in the following browsers:
- [ ] Chrome (latest) - Primary
- [ ] Firefox (latest)
- [ ] Edge (latest)
- [ ] Safari (if available)

**Check for each browser:**
- Layout renders correctly
- Tailwind styles apply
- Animations work (spinner)
- Links open in new tab
- Form submission works

#### 4. Responsive Design Testing

**Breakpoints to Test**
| Device | Width | Key Checks |
|--------|-------|------------|
| Mobile | 375px | Input full width, readable text, no horizontal scroll |
| Tablet | 768px | Comfortable layout, good spacing |
| Desktop | 1024px+ | Centered content, max-width container |

**Responsive Checklist**
- [ ] No horizontal scrollbar on mobile
- [ ] Text is readable without zooming
- [ ] Buttons are tappable size (44px minimum)
- [ ] Input field is usable on mobile keyboard
- [ ] Citations don't overflow container

#### 5. Accessibility Checks

- [ ] Tab navigation works (input → button → links)
- [ ] Focus states visible (focus ring on input/button)
- [ ] Color contrast sufficient (check confidence badges)
- [ ] Screen reader would understand structure (headings, labels)
- [ ] No keyboard traps

#### 6. Polish & Fixes

**Common Issues to Check/Fix**
- Console errors (React warnings, failed requests)
- Flash of unstyled content (FOUC)
- Layout shift when response loads
- Long words/URLs breaking layout
- Missing loading states

**Optional Enhancements (if time permits)**
- Add `aria-label` to icon buttons
- Add keyboard shortcut hint (e.g., "Press Enter to search")
- Smooth scroll to response on mobile
- Persist last query in session storage

### Constraints
- No major refactoring - only bug fixes and polish
- Keep changes minimal and focused
- Document any issues that can't be fixed immediately

### Acceptance Criteria
- [ ] All 10 test queries work correctly
- [ ] Error states display properly
- [ ] Works in Chrome and Firefox
- [ ] Mobile layout (375px) is usable
- [ ] No console errors in normal usage
- [ ] Tab navigation works
- [ ] Report documents all test results

## Format

### Testing Process
1. Start backend: `cd 03_rag_pipeline && npm start`
2. Start frontend: `cd 03_rag_pipeline/client && npm run dev`
3. Open http://localhost:5173
4. Run through test cases
5. Document results in REPORT.md

### Bug Fix Format
For any issues found:
```markdown
### Issue: [Brief description]
**Severity**: High/Medium/Low
**File**: `src/components/Foo.jsx`
**Fix**: [Description of change]
```

### Validation Commands
```bash
# Terminal 1
cd pilot_phase1_poc/03_rag_pipeline
npm start

# Terminal 2
cd pilot_phase1_poc/03_rag_pipeline/client
npm run dev

# Browser testing
# Open http://localhost:5173
# Open DevTools → Toggle device toolbar for mobile
# Open DevTools → Console for errors
```

### Output
1. Test results for all 10 queries
2. Browser compatibility results
3. Responsive design results
4. List of issues found and fixes applied
5. Any known issues that remain

### Test Result Template
```markdown
## Query Test Results

| # | Query | Result | Notes |
|---|-------|--------|-------|
| 1 | Export documents | ✅ Pass | 3 citations, High confidence |
| 2 | GST rate | ✅ Pass | Correct 9% answer |
...
```
