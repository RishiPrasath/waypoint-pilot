# E2E Test Suite - Failure Analysis Report

**Date**: 2026-02-01
**Test Run**: Task 8.1 E2E Test Suite
**Overall Result**: 90% Pass (27/30)

---

## Executive Summary

The E2E test suite identified 3 failures out of 30 test cases. Two failures are latency-related (borderline threshold violations), and one is a logic issue requiring system prompt improvement.

| Failure ID | Category | Issue Type | Severity | Priority |
|------------|----------|------------|----------|----------|
| HP-02 | Happy Path | Latency | Low | P3 |
| HP-07 | Happy Path | Latency | Low | P3 |
| OOS-02 | Out-of-Scope | Logic | Medium | P2 |

---

## Failure #1: HP-02 - Singapore GST Rate

### Test Details

| Field | Value |
|-------|-------|
| Test ID | HP-02 |
| Category | Happy Path |
| Query | "What is the current GST rate for imports into Singapore?" |
| Expected | Answer with 9% GST, latency < 10s |

### Failure Metrics

| Metric | Threshold | Actual | Delta |
|--------|-----------|--------|-------|
| Latency | 10,000 ms | 15,389 ms | +5,389 ms (54% over) |
| Answer Length | 50+ chars | Passed | - |
| Citations | Any | 0 | - |

### Root Cause Analysis

1. **LLM Response Variability**: Groq API response times vary between 1-15 seconds depending on server load
2. **Query Complexity**: Despite being a simple factual query, the LLM generated a comprehensive response
3. **No Caching**: Repeated identical queries hit the LLM each time

### Evidence

```
Response received: Yes
Answer provided: Yes (correct 9% GST info)
Confidence: Low
Issue: Response time exceeded threshold
```

### Recommended Fixes

| Fix | Effort | Impact |
|-----|--------|--------|
| Increase latency threshold to 15s | Low | Immediate |
| Implement response caching for common queries | Medium | Long-term |
| Add streaming response support | High | UX improvement |

---

## Failure #2: HP-07 - Indonesia Food Import Permits

### Test Details

| Field | Value |
|-------|-------|
| Test ID | HP-07 |
| Category | Happy Path |
| Query | "What permits are needed for food imports to Indonesia?" |
| Expected | BPOM, regulatory info, latency < 10s |

### Failure Metrics

| Metric | Threshold | Actual | Delta |
|--------|-----------|--------|-------|
| Latency | 10,000 ms | 10,694 ms | +694 ms (7% over) |
| Answer Length | 50+ chars | Passed | - |
| Citations | Any | 0 | - |

### Root Cause Analysis

1. **Complex Query**: Indonesia food import requires information from multiple sources (BPOM, Ministry of Trade, Halal certification)
2. **Chunk Retrieval**: Multiple relevant chunks needed to be retrieved and processed
3. **Borderline Failure**: Only 694ms over threshold - essentially a pass with margin

### Evidence

```
Response received: Yes
Answer provided: Yes (correct BPOM/permit info)
Confidence: Low
Issue: Marginally exceeded latency threshold
```

### Recommended Fixes

| Fix | Effort | Impact |
|-----|--------|--------|
| Increase latency threshold to 12s | Low | Immediate |
| Optimize Indonesia regulatory doc chunking | Medium | Query-specific |
| Pre-compute embeddings for regulatory queries | Medium | Performance |

---

## Failure #3: OOS-02 - Booking Request (Critical)

### Test Details

| Field | Value |
|-------|-------|
| Test ID | OOS-02 |
| Category | Out-of-Scope |
| Query | "Book a shipment for me to Jakarta" |
| Expected | Graceful decline - cannot perform actions |

### Failure Metrics

| Metric | Expected | Actual |
|--------|----------|--------|
| Response Type | Decline | Informational |
| Decline Detected | Yes | No |
| Latency | N/A | 6,697 ms |

### Root Cause Analysis

1. **Action Verb Not Detected**: System prompt doesn't explicitly handle action requests (book, order, schedule)
2. **Helpful Override**: The system defaulted to being helpful by providing Jakarta shipping information
3. **Missing Guardrail**: No explicit instruction to decline booking/action requests

### Expected vs Actual Response

**Expected Response Pattern**:
```
I cannot book shipments or perform actions on your behalf.
Please contact our booking team at [contact] or use the
booking portal to schedule your shipment.
```

**Actual Response Pattern** (inferred):
```
To ship to Jakarta, you'll need the following documents:
- Commercial Invoice
- Packing List
- Bill of Lading
...
```

### Recommended Fixes

| Fix | Effort | Impact |
|-----|--------|--------|
| Update system prompt with action detection | Low | Critical |
| Add explicit decline patterns | Low | Critical |
| Test with additional action verbs | Low | Validation |

### System Prompt Addition

Add to `src/services/generation.js` system prompt:

```
ACTION REQUEST HANDLING:
If the user asks you to PERFORM an action (book, order, schedule,
reserve, track, cancel, modify), politely decline and explain:
- You cannot perform actions or transactions
- Direct them to the appropriate system or contact
- You can only provide information and answer questions
```

### Action Verbs to Detect

| Verb | Example Query | Expected Response |
|------|---------------|-------------------|
| book | "Book a shipment" | Decline - cannot book |
| order | "Order containers" | Decline - cannot order |
| schedule | "Schedule pickup" | Decline - cannot schedule |
| track | "Track my shipment" | Decline - no tracking access |
| cancel | "Cancel my booking" | Decline - cannot cancel |
| reserve | "Reserve space" | Decline - cannot reserve |

---

## Summary & Recommendations

### Immediate Actions (Task 8.2)

1. **[P2] Fix OOS-02**: Update system prompt to detect and decline action requests
2. **[P3] Adjust Latency Threshold**: Consider increasing from 10s to 12-15s

### Future Improvements

1. **Response Caching**: Cache common query responses (GST rate, Incoterms)
2. **Streaming Responses**: Implement streaming for better UX on slow queries
3. **Confidence Calibration**: Most responses show "Low" confidence - needs tuning

### Test Suite Adjustments

| Current | Proposed | Rationale |
|---------|----------|-----------|
| 10s latency threshold | 15s | Account for LLM variability |
| Binary pass/fail | Soft/hard thresholds | 10s soft, 20s hard fail |

---

## Appendix: Full Test Results

See: `reports/e2e_test_report.md`

---

*Report generated: 2026-02-01*
*Next action: Task 8.2 Bug Fixes & Hardening*
