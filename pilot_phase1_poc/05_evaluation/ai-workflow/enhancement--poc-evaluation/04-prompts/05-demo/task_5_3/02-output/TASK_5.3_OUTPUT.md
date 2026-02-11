# Task 5.3 Output — Record Demo (Screenshots)

**Status**: Complete
**Date**: 2026-02-11

## Run Summary

```
Queries run: 10
Succeeded: 10
Failed: 0
Avg response time: 3.5s

Demo  1 (Q-01) [happy   ] — OK   (3.1s) + full-page
Demo  2 (Q-11) [happy   ] — OK   (2.0s)
Demo  3 (Q-13) [happy   ] — OK   (2.0s) + full-page
Demo  4 (Q-24) [happy   ] — OK   (3.1s) + full-page
Demo  5 (Q-14) [happy   ] — OK   (3.5s) + full-page
Demo  6 (Q-03) [happy   ] — OK   (2.5s) + full-page
Demo  7 (Q-31) [happy   ] — OK  (13.7s)
Demo  8 (Q-42) [oos     ] — OK   (1.5s)
Demo  9 (Q-46) [oos     ] — OK   (1.5s)
Demo 10 (Q-04) [boundary] — OK   (1.5s)
```

## Deliverables

### Screenshots (25 files)
- **10 typed screenshots**: `demo_01_typed.png` through `demo_10_typed.png`
- **10 response screenshots**: `demo_01_response.png` through `demo_10_response.png`
- **5 full-page screenshots**: Demos 1, 3, 4, 5, 6 (responses exceeding viewport height)
- **Location**: `demo/presentation/public/demo/screenshots/`

### Manifest
- `demo/presentation/public/demo/screenshots/manifest.json` — JSON listing all 10 queries with their screenshot filenames for programmatic use in Slide 10

### Video Recording
- **Skipped** (Option A — screenshots sufficient). Can be added later via OBS if needed.

## Visual Verification

| Demo | ID | Visual Check |
|------|----|--------------|
| 1 | Q-01 | Numbered doc list, bold terms, full-page capture for long response |
| 2 | Q-11 | "9%" answer, 2 govt source URLs, 5 related doc chips, Medium amber badge |
| 3 | Q-13 | COO requirements, 4 source URLs, 2 regulatory chips |
| 4 | Q-24 | Step-by-step VGM process, Maersk source URLs, carrier chip |
| 5 | Q-14 | BPOM permit list, 4 source URLs, 4 regulatory chips |
| 6 | Q-03 | FCL vs LCL structured comparison, 1 internal chip |
| 7 | Q-31 | SLA "1-2 working days", 5 related doc chips, Medium badge |
| 8 | Q-42 | Decline message, red Low badge, "0 retrieved / 0 used / 1.0s" |
| 9 | Q-46 | Decline message, red Low badge |
| 10 | Q-04 | Decline message, red Low badge |

## Validation

- [x] All 10 queries executed (10/10 OK)
- [x] 25 screenshots captured (10 typed + 10 response + 5 full-page)
- [x] Screenshots are 1400px wide and visually clear
- [x] Happy path screenshots (Demos 1-7) show full response cards with rendered markdown
- [x] OOS screenshots (Demos 8-10) show decline messages with Low confidence badge
- [x] `manifest.json` created listing all screenshot files
- [x] No broken/blank screenshots
- [x] Demo 2 (Q-11) shows all 4 response card sections (Answer, Sources, Related Docs, Confidence)
