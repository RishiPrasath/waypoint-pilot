# Task 5.2 Output — Build Selenium Demo Script

**Status**: Complete
**Date**: 2026-02-11

## Deliverables

### Files Created
1. `demo/selenium/requirements.txt` — selenium>=4.15.0
2. `demo/selenium/demo_script.py` — Full automation script (10 queries, screenshots, error handling)
3. `demo/presentation/public/demo/screenshots/` — Output directory (created)

### Script Features
- **10 demo queries** hardcoded from Task 5.1 selection
- **2 screenshots per query**: `demo_{NN}_typed.png` + `demo_{NN}_response.png`
- **Full-page screenshots** auto-detected when content scrolls beyond viewport
- **Error recovery**: timeout/failure captures error screenshot, continues to next query
- **CLI flags**: `--quick` (2 queries only), `--headless` (no visible browser)
- **Summary report**: saved to `demo/selenium/demo_results.txt`
- **Window size**: 1400x900 for desktop-quality captures

### Smoke Test Results (--quick, 2 queries)
```
Queries run: 2
Succeeded: 2
Failed: 0
Avg response time: 5.6s

Demo  1 (Q-01) [happy   ] — OK   (9.2s)  + full-page screenshot
Demo  2 (Q-11) [happy   ] — OK   (2.1s)
```

### Screenshot Quality Verified
- **demo_01_response.png** (115KB): Rich response with numbered document list, bold terms
- **demo_01_response_full.png** (225KB): Full-page capture of long Q-01 response
- **demo_02_response.png** (86KB): All 4 sections visible — Answer, Sources (2 URLs), Related Docs (5 chips), Confidence Footer (Medium badge)
- Resolution: 1400px wide, clear and readable

## Validation

- [x] Selenium script runs without errors
- [x] Screenshots captured for each query (typed + response)
- [x] Screenshots saved to correct output directory (`demo/presentation/public/demo/screenshots/`)
- [x] Screenshots are clear and readable (1400px wide)
- [x] Script handles response rendering delays gracefully (WebDriverWait, 15s timeout)
- [x] Console output shows progress for each query
- [x] Summary report saved to `demo/selenium/demo_results.txt`
- [x] Tested with 2 queries — both passed (smoke test OK)
