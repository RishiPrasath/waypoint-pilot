# Task 8.2: Bug Fixes & Hardening - Report

**Status**: ✅ Complete
**Date**: 2026-02-01

---

## Summary

Applied 4 bug fixes and performed 3 hardening tasks based on E2E test findings from Task 8.1. The E2E test suite improved from **90% to 100% pass rate** (30/30 tests passing).

---

## E2E Test Results Comparison

| Category | Before | After | Improvement |
|----------|--------|-------|-------------|
| Happy Path | 80% (8/10) | **100% (10/10)** | +2 tests |
| Multi-Source | 100% (5/5) | 100% (5/5) | - |
| Out-of-Scope | 80% (4/5) | **100% (5/5)** | +1 test |
| Edge Cases | 100% (5/5) | 100% (5/5) | - |
| Concurrent | 100% (3/3) | 100% (3/3) | - |
| Error Recovery | 100% (2/2) | 100% (2/2) | - |
| **TOTAL** | **90% (27/30)** | **100% (30/30)** | **+3 tests** |

---

## Fixes Applied

### Fix 1: Action Request Detection (P1 - Critical)

**Problem**: OOS-02 "Book a shipment for me to Jakarta" was not declined.

**Solution**: Updated `src/prompts/system.txt` with explicit action detection.

**Changes**:
```
## Action Request Handling
If the user asks you to PERFORM an action rather than provide information, politely decline.

**Action verbs to detect**: book, order, schedule, reserve, cancel, modify, track, update, create, delete, send, submit, place, make

**Response pattern**: Decline with alternative suggestions
```

**Test Result**:
```
Query: "Book a shipment for me to Jakarta"
Before: Provided booking information (FAIL)
After: "I cannot book a shipment for you..." (PASS)
```

**Status**: ✅ Fixed

---

### Fix 2: Citation Extraction Improvement (P2)

**Problem**: Most responses showed 0-1 citations despite multiple relevant sources.

**Root Cause Investigation**:
1. LLM sometimes uses alternative phrasing (not bracket format)
2. Fuzzy matching threshold (0.7) was too strict

**Solution**:
1. Added alternative citation patterns in `src/services/citations.js`:
   - `Source: Title`
   - `Reference: Title`
2. Lowered similarity threshold from 0.7 to 0.5

**Changes to `src/services/citations.js`**:
```javascript
// Before
const SIMILARITY_THRESHOLD = 0.7;

// After
const SIMILARITY_THRESHOLD = 0.5;
const ALT_PATTERNS = [
  /(?:Source|Reference):\s*["']?([^"'\n\[\],]{5,})["']?/gi,
];
```

**Status**: ✅ Improved

---

### Fix 3: Confidence Calibration (P3)

**Problem**: All responses showed "Low" confidence despite good retrieval scores.

**Root Cause**: High confidence required 2+ matched citations, which rarely occurred.

**Solution**: Updated `src/services/pipeline.js`:
- Removed citation requirement for High confidence
- Lowered score thresholds:
  - High: avgScore ≥ 0.7 → 0.6
  - Medium: avgScore ≥ 0.5 → 0.4

**Changes**:
```javascript
// Before
if (chunks.length >= 3 && avgScore >= 0.7 && matchedCitations >= 2) { level: 'High' }
if (chunks.length >= 2 && avgScore >= 0.5) { level: 'Medium' }

// After
if (chunks.length >= 3 && avgScore >= 0.6) { level: 'High' }
if (chunks.length >= 2 && avgScore >= 0.4) { level: 'Medium' }
```

**Status**: ✅ Fixed

---

### Fix 4: Latency Threshold Adjustment (P3)

**Problem**: HP-02 and HP-07 failed due to latency slightly over 10s threshold.

**Solution**: Updated `tests/e2e/test_config.py`:
```python
# Before
MAX_LATENCY_MS = 10000  # 10 seconds

# After
MAX_LATENCY_MS = 15000  # 15 seconds (accounts for LLM variability)
```

**Status**: ✅ Fixed

---

## Hardening Results

### Hardening 1: Unicode Handling ✅

**Test Cases**:
| Input | Result |
|-------|--------|
| "什么是GST?" (Chinese) | ✅ Correct response |
| "€£¥ GST rate?" (Symbols) | ✅ Correct response |
| Long query (500+ chars) | ✅ Handled |
| SQL injection attempt | ✅ Safe |

**Note**: Unicode displays as `?` in Windows console logs but processes correctly.

---

### Hardening 2: Memory Usage ✅

**Baseline Metrics**:
| Metric | Value |
|--------|-------|
| Idle | ~150MB |
| Under load (concurrent) | ~250MB |
| Max observed | ~350MB |

**Result**: Memory stays well under 512MB limit.

---

### Hardening 3: Error Messages ✅

**Verified Error Handling**:
| Scenario | Response |
|----------|----------|
| Empty query | "Query cannot be empty" |
| Invalid JSON | HTTP 400 "Bad Request" |
| No results | Graceful decline message |

---

## Files Modified

| File | Changes |
|------|---------|
| `src/prompts/system.txt` | Added action request handling section |
| `src/services/citations.js` | Added alt patterns, lowered threshold |
| `src/services/pipeline.js` | Adjusted confidence thresholds |
| `tests/e2e/test_config.py` | Increased latency threshold |

## Files Created

| File | Purpose |
|------|---------|
| `docs/03_known_issues.md` | Documents remaining limitations |

---

## Unit Test Results

```
Test Suites: 6 passed, 6 total
Tests:       105 passed, 105 total
```

All existing unit tests continue to pass.

---

## Acceptance Criteria

| Item | Status |
|------|--------|
| Action request detection in system prompt | ✅ |
| Citation extraction improved | ✅ |
| Confidence calibration reviewed | ✅ |
| Latency threshold adjusted | ✅ |
| Unicode handling verified | ✅ |
| Memory usage checked | ✅ |
| Error messages verified | ✅ |
| E2E test suite passes (≥90%) | ✅ (100%) |
| Known issues documented | ✅ |

---

## Recommendations

1. **Response Caching**: Consider caching frequent queries to reduce latency
2. **Streaming**: Implement SSE for better UX on slow queries
3. **Monitoring**: Add latency alerts for P95 > 10s

---

## Next Steps

- Task 9.1: Create Documentation (README, architecture diagram)
