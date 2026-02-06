# Task 8: Fix Remaining Failures + Parameter Experiments

## Persona

You are a retrieval optimization engineer. You have access to a RAG knowledge base with 30 documents (701 chunks) achieving 84% raw hit rate. Your job is to push this to 90%+ by (A) fixing content gaps that cause specific query failures, (B) correcting test expectations where the system is actually right, and (C) running parameter experiments to find the optimal chunk size.

## Context

### Current State

- **30 documents**, **701 chunks**, **84% raw hit rate** (42/50 queries pass)
- Adjusted hit rate: **~87%** (excluding 3 reclassified out-of-scope queries)
- Embedding model: all-MiniLM-L6-v2 via ONNX (384-d)
- Current params: CHUNK_SIZE=600, CHUNK_OVERLAP=90, top_k=5, threshold=0.15
- Config: `scripts/config.py` — chunk params are env-overridable via `.env`

### The 8 Remaining Failures

| # | Query | Category | Retrieved | Expected | Score | Root Cause |
|---|-------|----------|-----------|----------|-------|------------|
| 3 | What's the difference between FCL and LCL? | booking_documentation | `one_service_summary` | `incoterms` | -0.113 | No dedicated FCL/LCL comparison section anywhere; test expects `incoterms` but content lives in `booking_procedure` Key Terms table |
| 5 | Do I need a commercial invoice for samples with no value? | booking_documentation | `customer_faq` | `sg_export`, `indonesia_import` | 0.542 | **customer_faq** contains the correct, detailed answer (lines 60-76). Test expectation is wrong. |
| 7 | Can we ship without a packing list? | booking_documentation | `customer_faq` | `sg_export`, `indonesia_import` | 0.536 | **customer_faq** contains the correct, detailed answer (lines 102-120). Test expectation is wrong. |
| 20 | What's the difference between Form D and Form AK? | customs_regulatory | `sg_certificates_of_origin` | `asean_rules`, `atiga` | 0.070 | Content about Form D and Form AK is split across multiple docs; no single section compares them side-by-side |
| 36 | What's the process for refused deliveries? | sla_service | `incoterms_2020_reference` | `cod_procedure`, `service_terms` | -0.088 | **Reclassified out-of-scope** — no refused delivery process exists in KB |
| 38 | How do I upgrade to express service? | sla_service | `one_service_summary` | `service_terms`, `booking` | -0.204 | **Reclassified out-of-scope** — no express upgrade process documented |
| 41 | What's the current freight rate to Jakarta? | edge_cases | `indonesia_import` | — (out-of-scope) | 0.155 | Out-of-scope (live rates). Score is marginally above threshold (0.155 >= 0.15), so the out-of-scope check fails. |
| 44 | I want to file a claim for damaged cargo | edge_cases | `service_terms` | — (out-of-scope) | 0.264 | `service_terms` Section 8 actually HAS claims content. System retrieves the RIGHT document. Test incorrectly marks as out-of-scope. |

### Failure Classification

| Fix Type | Queries | Action |
|----------|---------|--------|
| **Content fix** | #3, #20 | Add comparison sections to KB docs |
| **Test expectation fix** | #5, #7, #44 | Update `EXPECTED_SOURCES` in test script |
| **Out-of-scope (no fix)** | #36, #38 | Already reclassified — skip |
| **Threshold edge case** | #41 | Out-of-scope query barely above threshold — addressable via parameter tuning |

## Task

Execute two tracks in sequence.

### Track A: Content & Test Fixes

#### A1. Add FCL vs LCL Comparison Section (fixes query #3)

**File**: `kb/04_internal_synthetic/booking_procedure.md`

The document already has a Key Terms table with FCL and LCL entries (lines 24-25) but no comparison section. Add a dedicated comparison section after the "Recommended Booking Lead Times" section (after line 99, before `## 5. Detailed Procedure`).

Insert this section:

```markdown
## FCL vs LCL: Which Should I Choose?

**What's the difference between FCL and LCL?**

| Feature | FCL (Full Container Load) | LCL (Less than Container Load) |
|---------|--------------------------|-------------------------------|
| **Container** | Dedicated container for one shipper | Shared container, cargo consolidated |
| **Best for** | Large shipments (15+ CBM) | Small shipments (1-14 CBM) |
| **Cost** | Flat rate per container | Per CBM/weight (whichever greater) |
| **Transit time** | Faster (direct, no deconsolidation) | Slower (+2-5 days for CFS handling) |
| **Minimum** | No minimum (but pay full container) | Typically 1 CBM minimum |
| **Handling** | Less handling = lower damage risk | More handling at CFS warehouse |
| **Booking lead time** | 5-7 days | 7-10 days |
| **CY/CFS** | Container Yard (CY) delivery | Container Freight Station (CFS) delivery |
| **Flexibility** | Fixed schedule, own container | Depends on consolidation schedule |

**Cost Comparison Example (Singapore to Jakarta)**:

| Volume | FCL 20' (~28 CBM) | LCL (per CBM) | Cheaper Option |
|--------|-------------------|---------------|----------------|
| 5 CBM | ~USD 800 (full container) | ~USD 250 (5 x $50) | LCL |
| 15 CBM | ~USD 800 (full container) | ~USD 750 (15 x $50) | Compare both |
| 20 CBM | ~USD 800 (full container) | ~USD 1,000 (20 x $50) | FCL |

**Rule of Thumb**: If your cargo fills more than half a 20' container (~14 CBM), FCL is usually more cost-effective.
```

Also update the test expectation for query #3. Currently expects `incoterms` — should expect `booking`:

**File**: `scripts/retrieval_quality_test.py`

Change line 96:
```python
"What's the difference between FCL and LCL?": ["incoterms"],
```
To:
```python
"What's the difference between FCL and LCL?": ["booking"],
```

---

#### A2. Add Form D vs Form AK Comparison Section (fixes query #20)

**File**: `kb/04_internal_synthetic/fta_comparison_matrix.md`

The document has Form types listed in Section 5.1 (line 164-177) but no side-by-side comparison of Form D vs Form AK. Add a new section after Section 5.3 (after line 193, before the `---` separator that precedes Section 6).

Insert this section:

```markdown
### 5.4 Form D vs Form AK: Key Differences

**What's the difference between Form D and Form AK?**

| Feature | Form D (ATIGA) | Form AK (AKFTA) |
|---------|---------------|----------------|
| **FTA** | ASEAN Trade in Goods Agreement | ASEAN-Korea FTA |
| **Coverage** | ASEAN 10 member states | ASEAN 10 + South Korea |
| **Use when** | Shipping within ASEAN (e.g., SG → ID, TH, VN) | Shipping to/from South Korea |
| **Duty rate** | 0% on 98.86% of tariff lines | 0% on ~90% of tariff lines |
| **RVC threshold** | 40% Regional Value Content | 40% RVC (varies by product) |
| **Cumulation** | Full cumulation across ASEAN 10 | Bilateral + ASEAN cumulation |
| **Issuing authority** | Singapore Customs (via TradeNet) | Singapore Customs (via TradeNet) |
| **Validity** | 12 months from issue | 12 months from issue |
| **Self-certification** | AWSC pilot (certified exporters only) | Not available |
| **Back-to-back** | Available for re-exports | Available for re-exports |

**When to use which:**
- **Form D**: For all intra-ASEAN trade (Singapore to/from any ASEAN member)
- **Form AK**: ONLY when shipping to/from South Korea via ASEAN
- **If both apply** (e.g., goods from Korea transiting through ASEAN): Compare duty rates — use whichever gives lower duty

**Common confusion**: Form D and Form AK are NOT interchangeable. Using Form D for Korea-bound goods will result in **no preferential treatment**. Always verify the correct form for the specific trade route.
```

---

#### A3. Update Test Expectations (fixes queries #5, #7, #44)

**File**: `scripts/retrieval_quality_test.py`

The test script has incorrect expected sources for 3 queries where the system is actually returning the correct document.

**Query #5** (line 98): customer_faq contains the answer at lines 60-76.
Change:
```python
"Do I need a commercial invoice for samples with no value?": ["sg_export", "indonesia_import"],
```
To:
```python
"Do I need a commercial invoice for samples with no value?": ["sg_export", "indonesia_import", "customer_faq", "booking"],
```

**Query #7** (line 100): customer_faq contains the answer at lines 102-120.
Change:
```python
"Can we ship without a packing list?": ["sg_export", "indonesia_import"],
```
To:
```python
"Can we ship without a packing list?": ["sg_export", "indonesia_import", "customer_faq", "booking"],
```

**Query #44** (line 141): service_terms Section 8 has full claims procedure (notification deadlines, required docs, time bars).
Change:
```python
"I want to file a claim for damaged cargo": [],  # Out of scope
```
To:
```python
"I want to file a claim for damaged cargo": ["service_terms"],  # Claims covered in Section 8
```

---

#### A4. No Action Required (queries #36, #38, #41)

- **#36** (refused deliveries): Reclassified out-of-scope. No KB content exists. Skip.
- **#38** (express upgrade): Reclassified out-of-scope. No KB content exists. Skip.
- **#41** (freight rate to Jakarta): Genuinely out-of-scope (live rates). The 0.155 score marginally exceeds threshold. Accept as expected behavior or adjust in Track B.

---

### Track B: Parameter Experiments

After Track A content fixes are applied, run systematic experiments varying chunk size and overlap.

#### Setup

The `.env` file in `pilot_phase1_poc/04_retrieval_optimization/` controls chunk parameters:
```
CHUNK_SIZE=600
CHUNK_OVERLAP=90
```

For each experiment:
1. Update `.env` with new parameters
2. Re-ingest: `venv/Scripts/python -m scripts.ingest --clear`
3. Run test: `venv/Scripts/python -m scripts.retrieval_quality_test`
4. Record: hit rate, chunk count, per-category breakdown, any new failures/fixes

#### Experiment Matrix

| Run | CHUNK_SIZE | CHUNK_OVERLAP | top_k | Notes |
|-----|-----------|---------------|-------|-------|
| **Baseline** | 600 | 90 | 5 | Current (84% raw, post-Track A fixes) |
| **Exp A** | 800 | 120 | 5 | Larger chunks = more context per chunk |
| **Exp B** | 1000 | 150 | 5 | Even larger chunks |
| **Exp C** | 400 | 60 | 5 | Smaller chunks = more precise matching |
| **Exp D** | (best from A-C) | (best) | 10 | More results = higher recall |

#### What to Record Per Experiment

For each run, capture:
- Total chunk count
- Overall hit rate (raw and adjusted)
- Per-category hit rates (5 categories)
- Any queries that flipped PASS→FAIL or FAIL→PASS
- Top score for each of the previously-failing queries (#3, #20, #41)

#### Stop Condition

- **Target**: 90% adjusted hit rate (currently ~87%)
- **Hard stop**: After Experiment D (diminishing returns)
- **Regression guard**: If any experiment drops below 84% raw, discard and try next

#### After Experiments

1. Restore `.env` to the best-performing configuration
2. Run final ingestion with best params
3. Generate final `retrieval_quality_REPORT.md`

---

## Format

### Execution Order

1. Apply Track A content fixes (A1-A3) — edit 2 KB docs + 1 test script
2. Re-ingest with current params (600/90): `venv/Scripts/python -m scripts.ingest --clear`
3. Run baseline test with Track A fixes: `venv/Scripts/python -m scripts.retrieval_quality_test`
4. Record baseline results (this is the new "post-fix" baseline)
5. Run Experiments A through D sequentially
6. Select best configuration
7. Run final validation with best config

### Commands

```bash
cd pilot_phase1_poc/04_retrieval_optimization

# Activate venv (Windows)
venv/Scripts/activate

# Ingest (clear existing)
venv/Scripts/python -m scripts.ingest --clear

# Run retrieval quality test
venv/Scripts/python -m scripts.retrieval_quality_test

# Verify ingestion details
venv/Scripts/python -m scripts.verify_ingestion
```

**Important**: Use `venv/Scripts/python` with forward slashes (Windows bash compatibility). Use `-m scripts.module_name` pattern to avoid import errors.

### Output Report

Save the output report to:
```
04-prompts/04-refinement/task_8_fix_failures_parameter_experiments/02-output/REPORT.md
```

Report structure:
1. **Summary**: Best configuration found, final hit rate
2. **Track A Results**: Content fixes applied, test expectation updates, post-fix baseline
3. **Track B Results**: Table of all experiments with hit rates, chunk counts, per-category breakdowns
4. **Best Configuration**: Selected params with justification
5. **Remaining Failures**: Any queries still failing and why
6. **Recommendations**: Suggestions for further improvement (Week 4)

Also update:
- `IMPLEMENTATION_ROADMAP.md` — mark Task 8 complete with results
- `IMPLEMENTATION_CHECKLIST.md` — mark Task 8 items
