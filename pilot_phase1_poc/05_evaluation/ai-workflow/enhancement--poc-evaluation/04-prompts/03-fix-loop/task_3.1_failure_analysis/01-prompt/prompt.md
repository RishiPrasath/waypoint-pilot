# Task 3.1 Prompt — Failure Analysis

## Persona
Senior QA engineer performing root cause analysis on a RAG system evaluation. Your goal is to classify every failure, identify systemic patterns, and produce an actionable fix plan prioritized by impact.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Phase**: Phase 3 — Fix-and-Retest Loop
- **Dependencies**: T2.13 (Round 2 evaluation — complete)
- **Blocks**: T3.2 (apply fixes)
- **Current state**: Round 2 completed with 50/50 queries executed. 3/5 targets met, 2 failed. Results in `data/evaluation_results.json`, human-readable report in `reports/evaluation_report.md`.

### Round 2 Results

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Deflection Rate | 63.4% | >= 40% | PASS |
| Citation Accuracy | 36.6% | >= 80% | FAIL |
| Hallucination Rate | 24.0% | < 15% | FAIL |
| OOS Handling | 100.0% | >= 90% | PASS |
| Avg Latency | 1633ms | < 5000ms | PASS |

### Per-Category Breakdown

| Category | Queries | Deflection | Citation | Hallucination | Avg Latency |
|----------|---------|------------|----------|---------------|-------------|
| booking | 10 | 80.0% | 50.0% | 10.0% | 2008ms |
| customs | 10 | 90.0% | 40.0% | 10.0% | 1747ms |
| carrier | 10 | 30.0% | 20.0% | 50.0% | 1642ms |
| sla | 10 | 50.0% | 40.0% | 50.0% | 1719ms |
| edge_case | 10 | 100.0% | 0.0% | 0.0% | 1050ms |

### Key Data Points from Results Analysis

**Confidence Distribution (50 queries):**
- High: 0 queries (0%)
- Medium: 5 queries (10%) — ALL pass, ALL have citations
- Low: 45 queries (90%) — 37 fail (82% fail rate)

**Chunk Retrieval for Low Confidence Queries:**
- 23 of 45 Low queries have chunksRetrieved = 0 (51%)
- 35 of 45 Low queries have chunksUsed = 0 (78%)
- Even when chunks ARE retrieved, scores are too low to use

**Failure Count by Check:**
- citation_present: 35 failures (26 in-scope + 9 OOS)
- must_contain: 15 failures
- expected_docs: 15 failures
- must_not_contain: 12 failures (ALL from "I don't have" signal)
- latency: 2 failures (Q-23: 5772ms, Q-39: 6718ms)

### Architecture Reference

**Confidence scoring** (`backend/services/pipeline.js:145-175`):
```
High:   chunks.length >= 3 && avgScore >= 0.6
Medium: chunks.length >= 2 && avgScore >= 0.4
Low:    everything else
```

**Retrieval config** (`backend/config.js`):
- `retrievalTopK`: 10
- `relevanceThreshold`: 0.15

**Source building** (`backend/services/citations.js`):
- Sources are built from chunks that matched citations in the LLM response
- If LLM doesn't produce `[Title > Section]` citations, sources array is empty
- `buildSources()` and `buildRelatedDocs()` depend on `processCitations()` finding matches

**System prompt** (`backend/prompts/system.txt`):
- Instructs LLM to cite with `[Document Title > Section]` format
- Instructs "If the context doesn't contain the answer: I don't have specific information about [topic]"
- This "I don't have" instruction is the source of all 12 hallucination false positives

### Root Cause Hypotheses (from Round 2 analysis)

**Three distinct failure modes identified:**

1. **Retrieval failure** (23 queries, chunksRetrieved=0): Vector search returns nothing. Carrier queries hardest hit (8/10 get 0 chunks). These cascade into "I don't have" responses, failing must_contain + must_not_contain + expected_docs + citation_present simultaneously.

2. **Low relevance / chunksUsed=0** (12 queries): Chunks retrieved but scores too low → avgScore < 0.4 → Low confidence. LLM gets context but generates response without strong grounding → no citations → sources empty.

3. **Latency spikes** (2 queries): Q-23 and Q-39 produce good responses but exceed 5s threshold. Minor issue.

### Files to Reference

| File | Purpose |
|------|---------|
| `data/evaluation_results.json` | Full raw results (50 queries with checks) |
| `reports/evaluation_report.md` | Human-readable report with failure tables |
| `data/evaluation_results.csv` | Spreadsheet-friendly results |
| `backend/services/pipeline.js` | Confidence scoring logic |
| `backend/services/citations.js` | Citation extraction and source building |
| `backend/services/retrieval.js` | Chunk retrieval and scoring |
| `backend/config.js` | Retrieval threshold config |
| `backend/prompts/system.txt` | System prompt |
| `data/evaluation_baselines.json` | 50 query baselines with expected answers |
| `kb/` | Knowledge base documents |

## Task

Perform a comprehensive failure analysis of all 37 failing queries from Round 2. Produce `reports/failure_analysis.md` with:

### Step 1: Read Results Data
- Read `data/evaluation_results.json` to extract per-query details
- For each of the 37 failing queries, note: confidence level, chunksRetrieved, chunksUsed, which checks failed, and the actual answer text (first 200 chars)

### Step 2: Classify Root Causes
For each failing query, assign ONE primary root cause:

| Root Cause | Code | Description |
|------------|------|-------------|
| Retrieval miss | RM | chunksRetrieved = 0, query didn't match any KB content |
| Low relevance | LR | Chunks retrieved but avgScore too low, chunksUsed = 0 |
| Citation gap | CG | Answer is correct/useful but LLM didn't cite sources |
| Baseline mismatch | BM | Baseline expectations are wrong (e.g., "I don't have" is correct for certain queries) |
| KB content gap | KC | KB genuinely lacks content to answer the query |
| OOS citation | OC | OOS query correctly declined but penalized for no citation (evaluation design issue) |
| Latency spike | LS | Good response but exceeded 5s threshold |

### Step 3: Analyze the "I don't have" Problem
The 12 must_not_contain failures ALL have "I don't have" as the signal. For each:
- Is the system **correctly** declining because it lacks the information? → Reclassify as BM
- Is the system **incorrectly** declining when KB has the content? → Classify as RM or LR
- Check `chunksRetrieved`: if 0, it's a retrieval problem. If >0, it's a relevance/confidence problem.

### Step 4: Analyze Carrier Category (worst performer)
Carrier has 9/10 failures. For each carrier query:
- Check which carrier docs exist in KB (`kb/02_carriers/`)
- Check if the query topic is actually covered in those docs
- Determine if this is a retrieval problem or a genuine KB gap

### Step 5: Analyze Citation Accuracy Problem
26 in-scope queries lack citations. For each:
- If chunksUsed = 0: the LLM had no context → can't cite → fix is retrieval/confidence
- If chunksUsed > 0 but no citations: the LLM didn't format citations properly → fix is prompt
- Determine which fix (confidence tuning vs prompt tuning) would help more

### Step 6: Prioritize Fixes by Impact
Group fixes into categories and estimate how many queries each would resolve:

| Fix Category | Description | Est. Impact (queries fixed) |
|-------------|-------------|-----------------------------|
| Confidence threshold | Lower thresholds so more queries get Medium/High | N queries |
| Baseline reclassification | Fix false positive hallucination signals | N queries |
| KB content | Add content for genuinely missing topics | N queries |
| System prompt | Strengthen citation instructions | N queries |
| Retrieval tuning | Adjust relevance threshold or top-k | N queries |

### Step 7: Produce Fix Plan for Task 3.2
Create a specific, ordered list of fixes for Task 3.2 to implement:

1. **Fix X** — what to change, which file, expected impact
2. **Fix Y** — ...

Order by: highest impact first, then easiest to implement.

## Format

**Create**: `reports/failure_analysis.md` with:
1. Executive summary (3 sentences)
2. Root cause classification table (all 37 failing queries)
3. Root cause distribution chart
4. Detailed analysis per failure mode
5. Fix priority matrix (ordered by impact)
6. Specific fix plan for Task 3.2

**Output report**: `TASK_3.1_OUTPUT.md` with:
- Summary of findings
- Root cause distribution
- Top 5 fix priorities
- Link to full report

## Validation
- [ ] All 37 failing queries analyzed with root cause code
- [ ] Root cause distribution summarized
- [ ] "I don't have" false positives specifically analyzed
- [ ] Carrier category deep-dive completed
- [ ] Citation accuracy root cause identified
- [ ] Fixes prioritized by impact (number of queries fixed)
- [ ] Specific fix plan for Task 3.2 produced
- [ ] `reports/failure_analysis.md` created

## Update on Completion

**MANDATORY — Update ALL tracking locations:**
- **Checklist**: `03-checklist/IMPLEMENTATION_CHECKLIST.md` — mark Task 3.1 `[x]` AND update Phase 3 progress (1/3, 33%) + Total (24/43, 56%)
- **Roadmap**: `02-roadmap/IMPLEMENTATION_ROADMAP.md` — update ALL FOUR locations:
  1. **Progress Tracker** table (top) — Phase 3: 3 | 1 | In Progress, Total: 43 | 24 | 56%
  2. **Quick Reference** table — change Task 3.1 status `Pending` -> `Complete`
  3. **Detailed task entry** — change `Status: Pending` -> `Status: Complete` AND check validation boxes `[x]`
  4. Phase 3 status: `Pending` -> `In Progress`
- **Bootstrap file**: `ai-workflow-bootstrap-prompt-v3.md` — update Active Initiatives progress count (24/43 -- 56%)
- **CLAUDE.md** (root) — update Active Initiatives progress count (24/43 — 56%)
- **AGENTS.md** (root) — update Active Initiatives progress count (24/43 -- 56%)
- **Verify**: Re-read all updated files to confirm consistency
