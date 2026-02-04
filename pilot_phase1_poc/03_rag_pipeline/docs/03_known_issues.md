# Known Issues & Limitations

**Document**: RAG Pipeline Known Issues
**Version**: 1.0
**Last Updated**: 2026-02-01

---

## Overview

This document tracks known issues, limitations, and recommendations for the Waypoint RAG Co-pilot after Task 8.2 bug fixes and hardening.

---

## Resolved Issues (Task 8.2)

| Issue | Resolution | Status |
|-------|------------|--------|
| Action requests not declined | Updated system prompt with action detection | ✅ Fixed |
| Latency threshold too strict | Increased from 10s to 15s | ✅ Fixed |
| Low citation count | Lowered similarity threshold, added alt patterns | ✅ Improved |
| Confidence always "Low" | Adjusted thresholds, removed citation requirement | ✅ Fixed |

---

## Known Limitations

### 1. LLM Response Variability

**Description**: Groq API response times vary significantly (1-15 seconds) based on server load.

**Impact**: Occasional slow responses, especially for complex queries.

**Mitigation**:
- Increased test latency threshold to 15 seconds
- Future: Implement response caching for common queries

**Severity**: Low

---

### 2. Citation Matching Accuracy

**Description**: Citation extraction relies on LLM using specific format `[Title > Section]`. When LLM uses different phrasing, citations may not match.

**Impact**: Some responses may show fewer citations than expected.

**Mitigation**:
- Added alternative citation patterns (Source:, Reference:)
- Lowered fuzzy matching threshold from 0.7 to 0.5
- System prompt encourages proper citation format

**Severity**: Low

---

### 3. Unicode Display in Logs

**Description**: Some Unicode characters (Chinese, Japanese, special symbols) display as `?` in Windows console logs.

**Impact**: Display only - queries process correctly, responses are accurate.

**Mitigation**: None required - functional behavior is correct.

**Severity**: Informational

---

### 4. Knowledge Base Scope

**Description**: The system can only answer questions covered by the 29 documents in the knowledge base.

**Impact**: Queries outside scope return "I don't have information" responses.

**Mitigation**: Clear out-of-scope handling in system prompt.

**Severity**: By Design

---

### 5. No Real-Time Data

**Description**: Cannot provide live tracking, rates, or account-specific information.

**Impact**: Must decline real-time queries.

**Mitigation**: System prompt directs users to appropriate channels.

**Severity**: By Design

---

## Performance Characteristics

### Response Latency

| Percentile | Value | Notes |
|------------|-------|-------|
| P50 | ~2-3s | Typical query |
| P95 | ~10-12s | Complex queries |
| Max | ~15s | Threshold limit |

### Memory Usage

| Metric | Value |
|--------|-------|
| Baseline | ~150MB |
| Under load | ~250MB |
| Max observed | ~350MB |

---

## Recommendations for Future Development

### Short-term (P1)

1. **Response Caching**: Cache common queries (GST rate, Incoterms) to reduce latency
2. **Streaming Responses**: Implement SSE for better perceived performance

### Medium-term (P2)

1. **Citation Improvement**: Train/fine-tune citation extraction
2. **Query Classification**: Pre-classify queries for faster routing
3. **Knowledge Base Expansion**: Add more documents as needed

### Long-term (P3)

1. **Multi-language Support**: Translate knowledge base for regional markets
2. **Feedback Loop**: Collect user feedback to improve responses
3. **Integration**: Connect to TMS/WMS for real-time data (Phase 2)

---

## Issue Reporting

For new issues, document:
1. Query that caused the issue
2. Expected vs actual behavior
3. Timestamp and any error messages
4. Steps to reproduce

---

*Last reviewed: 2026-02-01*
