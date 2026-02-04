# Task 8.2: Bug Fixes & Hardening

## Persona
You are a senior software engineer performing bug fixes and system hardening based on E2E test results. You focus on production-readiness, edge case handling, and system reliability.

## Context

### Project Journey Summary

The Waypoint RAG Co-pilot has been built over 15 tasks:

| Phase | Tasks | Key Deliverables |
|-------|-------|------------------|
| Setup | 1.1-1.2 | Assets copied, source URLs fixed |
| Quality | 2.1-2.2 | Retrieval quality validated (~350 chunks) |
| Backend | 3.1-6.3 | Node.js, ChromaDB, Groq LLM, Express API |
| Frontend | 7.1-7.2 | React + Tailwind UI |
| Testing | 8.1 | E2E test suite (30 tests, 90% pass) |

### E2E Test Results (Task 8.1)

**Overall**: 27/30 passed (90%)

| Category | Pass Rate | Issues |
|----------|-----------|--------|
| Happy Path | 80% (8/10) | 2 latency failures |
| Multi-Source | 100% (5/5) | None |
| Out-of-Scope | 80% (4/5) | 1 logic failure |
| Edge Cases | 100% (5/5) | None |
| Concurrent | 100% (3/3) | None |
| Error Recovery | 100% (2/2) | None |

### Failed Tests (from `docs/02_e2e_failure_analysis.md`)

1. **HP-02 (GST Rate)**: Latency 15,389ms > 10,000ms threshold
2. **HP-07 (Indonesia Permits)**: Latency 10,694ms > 10,000ms threshold (borderline)
3. **OOS-02 (Booking Request)**: Did not decline action request "Book a shipment for me to Jakarta"

### Known Issues from Journey

| Source | Issue | Priority |
|--------|-------|----------|
| Task 8.1 | Low citation count (0-1 per response) | P2 |
| Task 8.1 | All confidence levels show "Low" | P3 |
| Task 8.1 | Action requests not declined | P1 |
| Task 8.1 | P95 latency 15s (high) | P2 |
| Roadmap | Unicode handling unverified | P2 |
| Roadmap | Memory usage unverified | P3 |

### Key Files

| File | Purpose |
|------|---------|
| `src/prompts/system.txt` | System prompt (needs action detection) |
| `src/services/citations.js` | Citation extraction |
| `src/services/pipeline.js` | Confidence calculation |
| `src/services/llm.js` | LLM service |
| `tests/e2e/test_config.py` | Test thresholds |

### References

- Failure Analysis: `docs/02_e2e_failure_analysis.md`
- E2E Report: `reports/e2e_test_report.md`
- System Prompt Report: `prompts/05_5.2_system_prompt/REPORT.md`
- Citation Extractor Report: `prompts/05_5.3_citation_extractor/REPORT.md`

### Dependencies

- ✅ Task 8.1: E2E Test Suite (Complete)

## Task

### Objective
Fix identified bugs and harden the system for production readiness based on E2E test findings and roadmap requirements.

### Bug Fixes Required

#### Fix 1: Action Request Detection (P1 - Critical)

**Problem**: "Book a shipment for me to Jakarta" was not declined.

**Solution**: Update `src/prompts/system.txt` to detect and decline action requests.

Add to system prompt:
```
## ACTION REQUEST HANDLING

If the user asks you to PERFORM an action rather than provide information, politely decline:

**Action verbs to detect**: book, order, schedule, reserve, cancel, modify, track, update, create, delete, send, submit

**Response pattern for action requests**:
"I cannot [action] on your behalf. I'm a knowledge assistant that provides information only.
For [action type], please:
- Contact our operations team at [appropriate contact]
- Use the booking portal / tracking system
- Speak with your account manager

However, I can help you with information about [related topic]. Would you like to know more?"

**Examples**:
- "Book a shipment" → Decline, offer shipping info
- "Track my container" → Decline, explain tracking system access
- "Cancel my order" → Decline, provide cancellation policy info
```

**Acceptance Criteria**:
- [ ] System prompt updated with action detection
- [ ] "Book a shipment" query returns decline response
- [ ] Other action verbs (track, cancel, order) also declined
- [ ] Decline response is helpful (offers alternative)

#### Fix 2: Citation Extraction Improvement (P2)

**Problem**: Most responses show 0-1 citations despite multiple sources being relevant.

**Investigation**:
1. Check if LLM is actually citing sources in response
2. Check if citation regex pattern matches LLM output format
3. Check fuzzy matching threshold (currently 0.7)

**Potential Fixes**:
- Adjust system prompt to encourage more explicit citations
- Relax fuzzy matching threshold to 0.6
- Add alternative citation patterns (e.g., "Source:", "Reference:")

**Acceptance Criteria**:
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Average citations per response ≥ 1.5

#### Fix 3: Confidence Calibration (P3)

**Problem**: All responses show "Low" confidence despite good retrieval scores.

**Investigation**: Review `calculateConfidence()` in `src/services/pipeline.js`

**Current Logic**:
```javascript
// High: 3+ chunks, avg score ≥0.7, 2+ citations matched
// Medium: 2+ chunks, avg score ≥0.5
// Low: Otherwise
```

**Potential Issues**:
- Citation match count always 0-1 (blocks High)
- Score thresholds may be too strict

**Acceptance Criteria**:
- [ ] Confidence calculation reviewed
- [ ] Thresholds adjusted if needed
- [ ] Happy path queries show Medium/High confidence

#### Fix 4: Latency Threshold Adjustment (P3)

**Problem**: 2 tests failed due to latency slightly over 10s threshold.

**Solution**: Adjust test threshold to account for LLM variability.

Update `tests/e2e/test_config.py`:
```python
MAX_LATENCY_MS = 15000  # Increased from 10000
```

**Acceptance Criteria**:
- [ ] Test config updated
- [ ] HP-02 and HP-07 pass on re-run

### Hardening Tasks

#### Hardening 1: Unicode Handling Verification

**Test Cases**:
- Chinese: "什么是GST?"
- Japanese: "輸出書類は何ですか?"
- Korean: "수출 서류가 뭐예요?"
- Special chars: "€£¥ GST rate?"
- Emoji: "📦 shipping documents?"

**Verification**:
- [ ] All queries process without error
- [ ] Responses are coherent
- [ ] No encoding errors in logs

#### Hardening 2: Memory Usage Check

**Test**:
```bash
# Run 50 sequential queries and monitor memory
node --max-old-space-size=512 src/index.js
# In another terminal, run load test
```

**Acceptance Criteria**:
- [ ] Memory stays under 512MB during normal operation
- [ ] No memory leaks over 50 queries
- [ ] Document baseline memory usage

#### Hardening 3: Error Message Improvements

Review error messages for user-friendliness:

| Scenario | Current | Improved |
|----------|---------|----------|
| Empty query | "Query cannot be empty" | ✅ Good |
| ChromaDB down | Raw error | "Knowledge base unavailable. Please try again." |
| Groq timeout | Raw error | "Response generation timed out. Please try a simpler query." |

**Acceptance Criteria**:
- [ ] All error messages are user-friendly
- [ ] No stack traces exposed to users
- [ ] Errors logged server-side for debugging

### Constraints

- Do not break existing passing tests
- Minimize changes to stable code
- Document any threshold changes
- Run full E2E suite after fixes

### Acceptance Criteria Summary

| Item | Priority | Status |
|------|----------|--------|
| Action request detection in system prompt | P1 | [ ] |
| Citation extraction improved | P2 | [ ] |
| Confidence calibration reviewed | P3 | [ ] |
| Latency threshold adjusted | P3 | [ ] |
| Unicode handling verified | P2 | [ ] |
| Memory usage checked | P3 | [ ] |
| Error messages improved | P3 | [ ] |
| E2E test suite passes (≥90%) | P1 | [ ] |
| Known issues documented | P2 | [ ] |

## Format

### Code Style
- Follow existing patterns in codebase
- Add comments explaining threshold changes
- Update tests for new behavior

### Validation Commands
```bash
# Run backend
cd pilot_phase1_poc/03_rag_pipeline && npm start

# Test action detection manually
curl -X POST http://localhost:3000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Book a shipment for me to Jakarta"}'

# Run E2E test suite
python scripts/e2e_test_suite.py

# Run unit tests
npm test
```

### Output
1. Updated `src/prompts/system.txt` with action detection
2. Any fixes to `src/services/citations.js` or `src/services/pipeline.js`
3. Updated `tests/e2e/test_config.py` with adjusted thresholds
4. `docs/03_known_issues.md` documenting remaining issues
5. `REPORT.md` with all findings and changes

### Report Structure
```markdown
# Task 8.2: Bug Fixes & Hardening - Report

## Summary
[Overview of changes made]

## Fixes Applied

### Fix 1: Action Request Detection
- Changes made
- Test results

### Fix 2: Citation Extraction
- Root cause
- Fix applied
- Before/after metrics

[etc.]

## Hardening Results

### Unicode Handling
[Test results]

### Memory Usage
[Baseline metrics]

## E2E Test Results (Post-Fix)

| Category | Before | After |
|----------|--------|-------|
| Happy Path | 80% | XX% |
| Out-of-Scope | 80% | XX% |
| TOTAL | 90% | XX% |

## Known Issues
[Any remaining issues]

## Recommendations
[Future improvements]
```
