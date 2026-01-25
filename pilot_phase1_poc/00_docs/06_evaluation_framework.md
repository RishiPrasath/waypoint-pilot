# 06 - Evaluation Framework

**Document Type**: Evaluation Specification  
**Pilot**: Waypoint Phase 1 POC  
**Version**: 1.0

---

## Evaluation Objectives

1. **Measure** whether the co-pilot achieves target deflection rate
2. **Identify** failure modes and improvement opportunities
3. **Validate** the approach before investing in Phase 2
4. **Document** learnings for future iterations

---

## Primary Metric: Query Deflection Rate

### Definition

> **Deflection Rate** = Percentage of queries where the co-pilot provides an accurate, useful answer that would allow a CS agent to respond without additional research.

### Target

| Metric | Target | Stretch | Minimum Viable |
|--------|--------|---------|----------------|
| Deflection Rate | 40% | 50% | 30% |

### Measurement Method

For each test query:
1. Submit query to co-pilot
2. Evaluate response quality (see scoring rubric)
3. Responses scoring 4-5 count as "deflected"

```
Deflection Rate = (Queries scoring 4 or 5) / (Total test queries) × 100%
```

---

## Response Scoring Rubric

### 5-Point Scale

| Score | Label | Description | Counts as Deflection? |
|-------|-------|-------------|----------------------|
| **5** | Excellent | Complete, accurate answer with correct sources. Agent could use directly. | ✅ Yes |
| **4** | Good | Accurate answer, minor gaps or formatting issues. Usable with minimal edits. | ✅ Yes |
| **3** | Partial | Contains relevant information but incomplete or requires verification. | ❌ No |
| **2** | Poor | Some relevant content but significant errors or missing key information. | ❌ No |
| **1** | Failed | Incorrect, irrelevant, or harmful response. | ❌ No |
| **0** | Appropriate Decline | Correctly identified as out-of-scope and declined gracefully. | Separate metric |

### Scoring Examples

**Score 5 - Excellent**
```
Query: "What documents are needed for sea freight export to Indonesia?"

Response: "For sea freight export from Singapore to Indonesia, you need:
1. Commercial Invoice (minimum 3 copies)
2. Packing List
3. Bill of Lading
4. Certificate of Origin (Form D for ATIGA preferential rates)
5. For certain goods: Import permit from Indonesian authorities

[Source: Singapore Customs Export Procedures Guide, Section 3.2]
[Source: Indonesia INSW Import Requirements]"

Rationale: Complete, accurate, properly sourced.
```

**Score 4 - Good**
```
Query: "What's the transit time to Port Klang?"

Response: "Transit time from Singapore to Port Klang by sea is typically 2-3 days for direct sailings. FCL shipments may have faster transit than LCL due to consolidation time.

[Source: Maersk Service Guide]"

Rationale: Accurate but could include more carrier options.
```

**Score 3 - Partial**
```
Query: "Do I need halal certification for food exports to Indonesia?"

Response: "Food products exported to Indonesia may require halal certification. I recommend checking the specific requirements with Indonesian authorities.

[Source: General knowledge]"

Rationale: Correct direction but lacks specifics (mandatory by Oct 2026, BPOM process).
```

**Score 2 - Poor**
```
Query: "What's the GST rate for imports?"

Response: "GST in Singapore is 8%.

[Source: Singapore Customs]"

Rationale: Outdated information (GST is 9% since Jan 2024).
```

**Score 1 - Failed**
```
Query: "What's FOB?"

Response: "FOB means the buyer pays for shipping from the warehouse."

Rationale: Incorrect definition, missing key details about risk transfer.
```

**Score 0 - Appropriate Decline**
```
Query: "What's the cheapest shipping rate to Jakarta?"

Response: "I don't have access to current shipping rates. For a rate quote, please contact our booking team at bookings@company.com.

[Note: Rate queries require live pricing systems which are outside my current capabilities.]"

Rationale: Correctly identified as out of scope, provided helpful redirect.
```

---

## Supporting Metrics

### Citation Accuracy

> **Definition**: Percentage of sourced responses where the cited source actually contains the claimed information.

| Target | Measurement |
|--------|-------------|
| 80% | Manual verification of cited sources |

**Evaluation Process**:
1. For each response with citations
2. Check if cited document exists
3. Check if cited section contains the information
4. Score: Correct / Partially Correct / Incorrect

### Hallucination Rate

> **Definition**: Percentage of responses containing fabricated information not present in the knowledge base.

| Target | Measurement |
|--------|-------------|
| < 15% | Manual review for invented facts |

**Hallucination Types**:
- Invented document names
- Fabricated statistics
- Non-existent procedures
- Incorrect regulatory requirements
- Made-up carrier policies

### Out-of-Scope Handling

> **Definition**: Percentage of out-of-scope queries correctly identified and gracefully declined.

| Target | Measurement |
|--------|-------------|
| 90% | Test with 10 known out-of-scope queries |

**Out-of-Scope Test Queries**:
1. "What's the current freight rate to Jakarta?" (needs live rates)
2. "Where is my shipment right now?" (needs tracking API)
3. "Book a shipment for me" (transaction)
4. "File a claim for damaged cargo" (complex workflow)
5. "Ship hazmat by air" (out of POC scope)
6. "What's the weather forecast?" (irrelevant)
7. "Recommend a supplier in China" (not logistics CS)
8. "What are competitor rates?" (inappropriate)
9. "How do I become a freight forwarder?" (career advice)
10. "What's your company's revenue?" (confidential)

### Response Latency

> **Definition**: Time from query submission to response display.

| Target | Measurement |
|--------|-------------|
| < 5 seconds | Timestamp logging in API |

```javascript
// Latency logging
const startTime = Date.now();
const response = await queryPipeline(query);
const latency = Date.now() - startTime;
console.log(`Query latency: ${latency}ms`);
```

---

## Test Query Bank

### Structure

50 test queries organized by category:

| Category | Count | Focus |
|----------|-------|-------|
| Booking & Documentation | 10 | UC-1.x |
| Customs & Regulatory | 10 | UC-2.x |
| Carrier Information | 10 | UC-3.x |
| Service & SLA | 10 | UC-4.x |
| Out-of-Scope / Edge Cases | 10 | Decline handling |

### Complete Test Query List

See [02 - Use Case Catalog](./02_use_cases.md) for full list of 50 queries.

---

## Evaluation Process

### Round 1 (Day 19-20)

**Purpose**: Identify issues for iteration

| Step | Action | Output |
|------|--------|--------|
| 1 | Run all 50 queries | Raw responses |
| 2 | Score each response | Scores (0-5) |
| 3 | Calculate initial metrics | Baseline numbers |
| 4 | Identify failure patterns | Issue list |
| 5 | Prioritize fixes | Action items |

### Iteration (Day 21)

**Purpose**: Address identified issues

| Issue Type | Fix Approach |
|------------|--------------|
| Retrieval miss | Add document, adjust chunking |
| Wrong context retrieved | Improve embeddings, adjust threshold |
| Generation hallucination | Strengthen system prompt |
| Missing citation | Check metadata pipeline |
| Too verbose | Adjust prompt, max_tokens |
| Too brief | Encourage detail in prompt |

### Round 2 (Day 22-23)

**Purpose**: Final evaluation

| Step | Action | Output |
|------|--------|--------|
| 1 | Re-run all 50 queries | Updated responses |
| 2 | Re-score all responses | Final scores |
| 3 | Calculate final metrics | Final numbers |
| 4 | Compare to Round 1 | Improvement analysis |
| 5 | Document remaining gaps | Known limitations |

---

## Evaluation Spreadsheet Template

```
| Query ID | Query Text | Response (truncated) | Score | Citation OK? | Latency | Notes |
|----------|------------|---------------------|-------|--------------|---------|-------|
| Q01 | What docs for Indonesia export? | For sea freight... | 5 | Yes | 2.3s | |
| Q02 | How far in advance to book LCL? | Recommend 5-7 days... | 4 | Yes | 1.8s | Minor detail missing |
| Q03 | What's FOB mean? | Free On Board means... | 5 | Yes | 1.5s | |
| ... | ... | ... | ... | ... | ... | ... |
```

### Calculated Metrics

```
Total Queries: 50
Score 5: [count]
Score 4: [count]
Score 3: [count]
Score 2: [count]
Score 1: [count]
Score 0 (appropriate decline): [count]

Deflection Rate: (Score 4+5) / 50 × 100 = [X]%
Citation Accuracy: [correct] / [total with citations] × 100 = [X]%
OOS Handling: [correct declines] / 10 × 100 = [X]%
Avg Latency: [X] seconds
```

---

## Go / No-Go Criteria

### Phase 2 Go Decision

| Metric | Threshold | Status |
|--------|-----------|--------|
| Deflection Rate | ≥ 35% | ☐ |
| Citation Accuracy | ≥ 70% | ☐ |
| OOS Handling | ≥ 80% | ☐ |
| Hallucination Rate | ≤ 20% | ☐ |
| System Stability | No crashes in testing | ☐ |

**Decision Rule**: 
- **Go**: Meet 4/5 thresholds including deflection rate
- **Conditional Go**: Meet 3/5, clear path to fixing gaps
- **No-Go**: Fail deflection rate OR 3+ thresholds missed

### Phase 2 Scope Decisions

Based on POC results:

| POC Result | Phase 2 Recommendation |
|------------|----------------------|
| 45%+ deflection | Expand to full pilot with real 3PL |
| 35-44% deflection | Improve knowledge base, then pilot |
| 25-34% deflection | Deeper iteration needed before pilot |
| < 25% deflection | Re-evaluate architecture approach |

---

## Failure Analysis Framework

### Categorizing Failures

For each query scoring ≤ 3:

```markdown
## Failure Analysis: [Query ID]

### Query
[The query text]

### Expected Response
[What a good response would include]

### Actual Response
[What the system returned]

### Score
[1-3]

### Root Cause Category
☐ Retrieval - relevant doc not retrieved
☐ Retrieval - wrong doc retrieved
☐ Missing Knowledge - no doc exists for this
☐ Generation - hallucinated despite good context
☐ Generation - misunderstood context
☐ Generation - too brief/incomplete
☐ Prompt - system prompt issue
☐ Edge Case - unusual query format

### Fix Approach
[What would fix this]

### Priority
[High/Medium/Low]
```

### Common Fix Patterns

| Root Cause | Fix |
|------------|-----|
| Doc not retrieved | Lower similarity threshold, check embeddings |
| Wrong doc retrieved | Better chunking, add metadata filters |
| No doc exists | Create/collect missing document |
| Hallucination | Strengthen "only use context" instruction |
| Misunderstood context | Better context formatting in prompt |
| Too brief | Add "be comprehensive" to prompt |
| Unusual query | Add query preprocessing |

---

## Quality Assurance Checklist

### Before Round 1

- [ ] All 50 test queries documented
- [ ] Scoring rubric understood
- [ ] Spreadsheet template ready
- [ ] System running stably
- [ ] All documents ingested

### After Round 1

- [ ] All queries scored
- [ ] Metrics calculated
- [ ] Failures categorized
- [ ] Fix priorities assigned
- [ ] Day 21 plan clear

### Before Round 2

- [ ] Identified fixes implemented
- [ ] Documents added if needed
- [ ] Prompt updated if needed
- [ ] System re-tested

### After Round 2

- [ ] Final metrics calculated
- [ ] Comparison to Round 1 documented
- [ ] Go/No-Go decision made
- [ ] Remaining limitations documented
- [ ] Phase 2 recommendations drafted

---

## Reporting Template

### POC Evaluation Report

```markdown
# Waypoint POC Evaluation Report

## Executive Summary
[2-3 sentences on overall outcome]

## Key Metrics

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Deflection Rate | 40% | [X]% | ✅/❌ |
| Citation Accuracy | 80% | [X]% | ✅/❌ |
| OOS Handling | 90% | [X]% | ✅/❌ |
| Hallucination Rate | <15% | [X]% | ✅/❌ |

## What Worked Well
- [Bullet points]

## Areas for Improvement
- [Bullet points]

## Known Limitations
- [What the system cannot do well]

## Recommendation
[Go / Conditional Go / No-Go for Phase 2]

## Phase 2 Prerequisites
[If Conditional Go, what needs to happen first]

## Appendix
- Full test results
- Failure analysis details
```

---

## Continuous Improvement

### Post-POC Knowledge Capture

Document learnings for future:

1. **Effective prompt patterns** — What worked in system prompt
2. **Chunking strategies** — What worked for different doc types
3. **Threshold tuning** — Optimal similarity thresholds
4. **Query patterns** — Common user query formats
5. **Failure modes** — What to watch for in production

### Feedback Loop Design

For Phase 2, plan to capture:
- Agent feedback (thumbs up/down)
- Query logs for analysis
- Escalation reasons
- Document gaps identified in production

---

*End of Evaluation Framework*

---

**Document Set Complete**

Return to [00 - Pilot Overview](./00_pilot_overview.md) for document index.
