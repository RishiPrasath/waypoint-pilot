# Task 5.3 — Record Demo (Screenshots + Video)

## Persona
Demo engineer executing the full Selenium capture run and producing presentation-ready static assets (screenshots + screen recording) for the React presentation app (Task 5.4).

## Context

### Current State
- **Backend**: Express API running on `http://localhost:3000` (already started)
- **Frontend**: React dev server running on `http://localhost:5173` (already started)
- **Selenium script**: `demo/selenium/demo_script.py` — tested with 2 queries (smoke test passed)
- **Existing screenshots**: 5 files from smoke test in `demo/presentation/public/demo/screenshots/` (will be overwritten by full run)

### What Task 5.3 Produces
Static assets consumed by Task 5.4 (React presentation app):
1. **20+ screenshots** (10 queries x 2 each + full-page captures) — embedded in Slide 10
2. **Screen recording** (optional, .mp4) — embedded in Slide 10 as `<video>`

### Downstream Consumer (Task 5.4 — Slide 10)
```
| 10 | Live demo (screenshots + video) | `<img>` + `<video>` |
```
The presentation app expects assets at:
- `demo/presentation/public/demo/screenshots/demo_NN_*.png`
- `demo/presentation/public/demo/recording.mp4` (optional)

## Task

### Step 1: Run the Full 10-Query Demo Capture

Execute the Selenium script (no `--quick` flag) to capture all 10 demo queries.

```bash
cd pilot_phase1_poc/05_evaluation
venv/Scripts/python demo/selenium/demo_script.py
```

**Expected output**: ~25 files in `demo/presentation/public/demo/screenshots/`:
- `demo_01_typed.png` through `demo_10_typed.png` (10 files)
- `demo_01_response.png` through `demo_10_response.png` (10 files)
- `demo_NN_response_full.png` for any queries with scrollable responses (~3-5 files)

**Expected runtime**: ~3-4 minutes (10 queries x 15s avg response + 2s pause between)

**If any queries fail**: The script continues and logs errors. Check `demo/selenium/demo_results.txt` for the summary. Re-run if >2 failures.

### Step 2: Verify Screenshot Quality

For each of the 10 queries, verify the response screenshot shows the expected content:

| Demo | ID | Expected Visual |
|------|----|-----------------|
| 1 | Q-01 | Long numbered doc list + 4 source URLs + 8 related doc chips |
| 2 | Q-11 | Concise "9%" answer + 2 govt source URLs + 5 related doc chips + Medium badge |
| 3 | Q-13 | COO requirements + 4 source URLs + 2 regulatory chips |
| 4 | Q-24 | Step-by-step VGM process + 5 Maersk URLs + 1 carrier chip |
| 5 | Q-14 | BPOM permit list + 4 source URLs + 4 regulatory chips |
| 6 | Q-03 | FCL vs LCL structured comparison + 1 internal chip |
| 7 | Q-31 | SLA commitment "1-2 working days" + 5 related doc chips + Medium badge |
| 8 | Q-42 | Brief decline message + Low (red) badge + 0 chunks |
| 9 | Q-46 | Brief decline message + Low (red) badge + 0 chunks |
| 10 | Q-04 | Brief decline message + Low (red) badge + 0 chunks |

Read/view each `demo_NN_response.png` to confirm the response card rendered correctly.

### Step 3: Screen Recording (Best-Effort)

The roadmap specifies an MP4 screen recording. Options:

**Option A — Skip video, screenshots are sufficient**: The 20+ screenshots provide complete visual coverage for Slide 10. The presentation app can display them as an image carousel. This is the pragmatic choice if OBS is not available.

**Option B — Record via OBS (manual)**: If the user wants a video, they can:
1. Open OBS, set capture region to the Chrome window
2. Start recording
3. Re-run: `venv/Scripts/python demo/selenium/demo_script.py`
4. Stop recording, save as `demo/presentation/public/demo/recording.mp4`

**Recommendation**: Proceed with Option A (screenshots only). Note in the output report that video is optional and can be added later.

### Step 4: Create Screenshot Manifest

Create a simple JSON manifest listing all captured screenshots for the presentation app to consume programmatically.

**File**: `demo/presentation/public/demo/screenshots/manifest.json`

```json
{
  "generated": "2026-02-11T...",
  "queries": [
    {
      "demo": 1,
      "id": "Q-01",
      "query": "What documents are needed for sea freight Singapore to Indonesia?",
      "type": "happy",
      "files": {
        "typed": "demo_01_typed.png",
        "response": "demo_01_response.png",
        "full": "demo_01_response_full.png"
      }
    },
    ...
  ]
}
```

This allows Slide 10 to dynamically render all screenshots without hardcoding filenames.

## Format

### Output Files
- `demo/presentation/public/demo/screenshots/demo_*.png` — 20+ screenshots
- `demo/presentation/public/demo/screenshots/manifest.json` — screenshot manifest
- `demo/selenium/demo_results.txt` — updated with full run results

### Validation
- [ ] All 10 queries executed (check `demo_results.txt`)
- [ ] 20+ screenshots captured (10 typed + 10 response + full-page extras)
- [ ] Screenshots are 1400px+ wide and visually clear
- [ ] Happy path screenshots (Demos 1-7) show full response cards with rendered markdown
- [ ] OOS screenshots (Demos 8-10) show decline messages with Low confidence badge
- [ ] `manifest.json` created listing all screenshot files
- [ ] No broken/blank screenshots
- [ ] Demo 2 (Q-11) shows all 4 response card sections (Answer, Sources, Related Docs, Confidence)

### Execution Commands
```bash
cd pilot_phase1_poc/05_evaluation

# Servers already running from Task 5.2
# If not: npm start & cd client && npm run dev

# Full run (all 10 queries)
venv/Scripts/python demo/selenium/demo_script.py

# Check results
cat demo/selenium/demo_results.txt

# List screenshots
ls demo/presentation/public/demo/screenshots/
```
