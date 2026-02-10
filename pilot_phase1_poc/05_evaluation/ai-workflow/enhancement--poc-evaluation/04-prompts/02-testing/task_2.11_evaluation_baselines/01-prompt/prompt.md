# Task 2.11 Prompt — Define Expected-Answer Baselines (50 Queries)

## Persona
Senior QA engineer defining automated evaluation baselines for a RAG-based freight forwarding co-pilot. Deep knowledge of Singapore customs, ASEAN trade, and freight operations.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Phase**: Phase 2 — Systematic Testing (Layer 5: Evaluation Baselines)
- **Dependencies**: CP2 (UX Redesign complete)
- **Blocks**: T2.12 (automated evaluation harness)
- **Current state**: 50 test queries exist in `scripts/retrieval_quality_test.py` with `EXPECTED_SOURCES` for retrieval. No answer-level baselines exist yet.

### What This Enables
Task 2.12 will build an automated evaluation harness that reads `data/evaluation_baselines.json` and:
- Sends each query to `POST /api/query`
- Checks the response against `must_contain`, `should_contain`, `must_not_contain`
- Verifies `expected_docs` appear in retrieved results
- Identifies OOS queries and checks for graceful decline
- Calculates aggregate metrics (deflection rate, citation accuracy, hallucination rate)

### Source Files to Reference

1. **`scripts/retrieval_quality_test.py`** — Contains `TEST_QUERIES` (50 queries in 5 categories) and `EXPECTED_SOURCES` (doc_id keywords per query)
2. **`00_docs/02_use_cases.md`** — Use case catalog with expected response patterns for each category
3. **`00_docs/06_evaluation_framework.md`** — Scoring rubric (5-point scale), metric definitions, targets

### The 50 Queries by Category

**Booking & Documentation (Q-01 to Q-10)**:
1. What documents are needed for sea freight Singapore to Indonesia?
2. How far in advance should I book an LCL shipment?
3. What's the difference between FCL and LCL?
4. When is the SI cutoff for this week's Maersk sailing?
5. Do I need a commercial invoice for samples with no value?
6. What's a Bill of Lading and who issues it?
7. Can we ship without a packing list?
8. What does FOB Singapore mean?
9. How do I amend a booking after confirmation?
10. What's the free time at destination port?

**Customs & Regulatory (Q-11 to Q-20)**:
11. What's the GST rate for imports into Singapore?
12. How do I find the HS code for electronics?
13. Is Certificate of Origin required for Thailand?
14. What permits are needed to import cosmetics to Indonesia?
15. What's the ATIGA preferential duty rate?
16. How does the Free Trade Zone work for re-exports?
17. What's the de minimis threshold for Malaysia?
18. Do I need halal certification for food to Indonesia?
19. How do I apply for a Customs ruling on HS code?
20. What's the difference between Form D and Form AK?

**Carrier Information (Q-21 to Q-30)**:
21. Which carriers sail direct to Ho Chi Minh?
22. What's the transit time to Port Klang?
23. Does PIL offer reefer containers?
24. How do I submit VGM to Maersk?
25. Can I get an electronic Bill of Lading?
26. What's the weight limit for a 40ft container?
27. Does ONE service Surabaya?
28. How do I track my shipment with Evergreen?
29. What's the difference between Maersk and ONE service?
30. Who do I contact for a booking amendment?

**SLA & Service (Q-31 to Q-40)**:
31. What's our standard delivery SLA for Singapore?
32. Is customs clearance included in door-to-door?
33. Do you provide cargo insurance?
34. What happens if shipment is delayed?
35. Are duties and taxes included in the quote?
36. What's the process for refused deliveries?
37. Do you handle import permit applications?
38. How do I upgrade to express service?
39. What's covered under standard liability?
40. Can I get proof of delivery?

**Edge Cases & Out-of-Scope (Q-41 to Q-50)**:
41. What's the current freight rate to Jakarta?
42. Where is my shipment right now?
43. Can you book a shipment for me?
44. I want to file a claim for damaged cargo
45. Can you ship hazmat by air?
46. What's the weather forecast for shipping?
47. Can you recommend a supplier in China?
48. What's your company's financial status?
49. How do I become a freight forwarder?
50. What are your competitor's rates?

### EXPECTED_SOURCES from retrieval_quality_test.py

```python
EXPECTED_SOURCES = {
    # Booking queries
    "Q-01": ["sg_export", "indonesia_import"],
    "Q-02": ["booking"],
    "Q-03": ["booking", "incoterms"],
    "Q-04": ["maersk"],
    "Q-05": ["sg_export", "indonesia_import", "customer_faq", "booking"],
    "Q-06": ["booking"],
    "Q-07": ["sg_export", "indonesia_import", "customer_faq", "booking"],
    "Q-08": ["incoterms"],
    "Q-09": ["booking"],
    "Q-10": ["carrier", "service"],
    # Customs queries
    "Q-11": ["sg_gst"],
    "Q-12": ["hs_classification", "hs_code"],
    "Q-13": ["sg_certificates", "atiga"],
    "Q-14": ["indonesia_import"],
    "Q-15": ["atiga"],
    "Q-16": ["sg_free_trade"],
    "Q-17": ["malaysia_import"],
    "Q-18": ["indonesia_import"],
    "Q-19": ["sg_hs_classification"],
    "Q-20": ["asean_rules", "atiga", "fta_comparison"],
    # Carrier queries
    "Q-21": ["pil", "maersk", "one", "evergreen"],
    "Q-22": ["pil", "maersk", "one", "evergreen"],
    "Q-23": ["pil"],
    "Q-24": ["maersk"],
    "Q-25": ["carrier", "maersk", "evergreen"],
    "Q-26": ["carrier"],
    "Q-27": ["one"],
    "Q-28": ["evergreen"],
    "Q-29": ["maersk", "one"],
    "Q-30": ["booking", "escalation"],
    # SLA queries
    "Q-31": ["sla_policy"],
    "Q-32": ["service_terms", "sla_policy"],
    "Q-33": ["service_terms"],
    "Q-34": ["sla_policy", "escalation"],
    "Q-35": ["service_terms"],
    "Q-36": ["cod_procedure", "service_terms"],
    "Q-37": ["service_terms", "booking"],
    "Q-38": ["service_terms", "booking"],
    "Q-39": ["service_terms", "sla_policy"],
    "Q-40": ["cod_procedure", "service_terms"],
    # Edge cases — out of scope
    "Q-41": [],  # freight rates — live data
    "Q-42": [],  # tracking — needs API
    "Q-43": [],  # booking — transaction
    "Q-44": ["service_terms"],  # claims — partially in scope
    "Q-45": [],  # hazmat — complex
    "Q-46": [],  # weather — irrelevant
    "Q-47": [],  # supplier — not logistics
    "Q-48": [],  # financials — inappropriate
    "Q-49": [],  # career — irrelevant
    "Q-50": [],  # competitor — inappropriate
}
```

## Task

Create `data/evaluation_baselines.json` with all 50 query baselines.

### JSON Schema

```json
{
  "version": "1.0",
  "description": "Evaluation baselines for Waypoint Co-Pilot 50-query test suite",
  "generated": "2026-02-09",
  "queries": [
    {
      "id": "Q-01",
      "category": "booking",
      "query": "What documents are needed for sea freight Singapore to Indonesia?",
      "is_oos": false,
      "expected_docs": ["sg_export", "indonesia_import"],
      "must_contain": ["commercial invoice", "packing list", "bill of lading"],
      "should_contain": ["certificate of origin", "Form D", "export permit"],
      "must_not_contain": ["I don't know", "I cannot help", "no information available"],
      "oos_decline_signals": []
    }
  ]
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Q-01 through Q-50 |
| `category` | string | Yes | One of: `booking`, `customs`, `carrier`, `sla`, `edge_case` |
| `query` | string | Yes | Exact query text from TEST_QUERIES |
| `is_oos` | boolean | Yes | `true` for out-of-scope queries (Q-41 to Q-50, except Q-44) |
| `expected_docs` | string[] | Yes | Doc ID keywords from EXPECTED_SOURCES |
| `must_contain` | string[] | Yes | Keywords that MUST appear in answer (min 2 per query). Case-insensitive substring match. Use specific domain terms, not generic words. |
| `should_contain` | string[] | Yes | Keywords that SHOULD appear (soft signal, min 1 per query) |
| `must_not_contain` | string[] | Yes | Hallucination signals (min 1 per query). Include factually wrong information that the LLM might hallucinate. |
| `oos_decline_signals` | string[] | Yes for OOS | Phrases expected in a graceful decline (e.g., "don't have", "not available", "contact", "out of scope") |

### Guidelines for Writing Baselines

#### `must_contain` — Hard requirements (answer fails without these)
- Use **specific domain terms**, not generic words
- For factual queries: include the key fact (e.g., "9%" for GST rate)
- For process queries: include at least 2 key steps or document names
- For comparison queries: include terms for both items being compared
- Match what the KB actually contains — not what you wish it contained
- **Min 2 per in-scope query**, 0 for OOS queries

#### `should_contain` — Soft signals (nice to have)
- Additional details that indicate a thorough answer
- Related terms, examples, caveats, or qualifications
- Source-specific terms (carrier names, regulation numbers)
- **Min 1 per in-scope query**

#### `must_not_contain` — Hallucination detectors
- **Generic declines on in-scope queries**: "I don't have information", "I cannot help", "no data available" — the co-pilot should answer these, not decline
- **Factually wrong information**: wrong GST rate, wrong transit times, wrong carrier names
- **Invented specifics**: made-up regulation numbers, fake URLs, non-existent forms
- **Confidently wrong details**: e.g., "GST rate is 7%" (old rate), "PIL sails to Antarctica"
- For OOS queries: `must_not_contain` should catch hallucinated answers (e.g., made-up rates, fake tracking numbers)
- **Min 1 per query**

#### `oos_decline_signals` — For OOS queries only
- Phrases that indicate graceful decline: "don't have specific information", "not available in our knowledge base", "contact your sales representative", "unable to provide"
- OOS queries should NOT answer the question — they should redirect
- Q-44 (cargo claims) is partially in-scope: `is_oos: false` since `service_terms` covers claims basics

### Step-by-Step

1. **Read** `scripts/retrieval_quality_test.py` for exact query text and EXPECTED_SOURCES
2. **Read** `00_docs/02_use_cases.md` for expected response patterns per category
3. **Author Q-01 to Q-10** (booking) — use UC-1.1 through UC-1.4 patterns
4. **Author Q-11 to Q-20** (customs) — use UC-2.1 through UC-2.4 patterns
5. **Author Q-21 to Q-30** (carrier) — use UC-3.1 through UC-3.3 patterns
6. **Author Q-31 to Q-40** (SLA) — use UC-4.1 through UC-4.3 patterns
7. **Author Q-41 to Q-50** (edge cases) — define OOS signals, must_not_contain for hallucination
8. **Validate** JSON is well-formed (`python -c "import json; json.load(open('data/evaluation_baselines.json'))"`)
9. **Spot-check** 5 random baselines for correctness

### Key Decisions

- **Q-44 ("file a claim for damaged cargo")** — `is_oos: false` because `service_terms` covers claims procedures in Section 8. It's partially answerable from the KB.
- **Case-insensitive matching** — The evaluation harness will use case-insensitive substring matching, so write `must_contain` in lowercase.
- **Substring not exact** — "bill of lading" will match "A Bill of Lading is..." and "bill of lading (B/L)..."
- **Keep must_contain achievable** — Only include terms the KB actually contains. Don't set baselines the system can't possibly meet.

## Format
- **Create**: `pilot_phase1_poc/05_evaluation/data/evaluation_baselines.json`
- **Output**: `TASK_2.11_OUTPUT.md` with summary statistics
- **Validation**:
  - `python -c "import json; d=json.load(open('data/evaluation_baselines.json')); print(f'{len(d[\"queries\"])} queries loaded')"` → 50
  - Every query has `len(must_contain) >= 2` (in-scope) or `len(oos_decline_signals) >= 1` (OOS)
  - Every query has `len(must_not_contain) >= 1`
  - `expected_docs` matches EXPECTED_SOURCES from retrieval_quality_test.py

## Update on Completion

**MANDATORY — Update ALL tracking locations:**
- **Checklist**: `03-checklist/IMPLEMENTATION_CHECKLIST.md` — mark Task 2.11 `[x]` AND update Phase 2 + Total progress counts
- **Roadmap**: `02-roadmap/IMPLEMENTATION_ROADMAP.md` — update ALL THREE locations:
  1. **Progress Tracker** table (top) — increment Phase 2 completed count and overall percentage
  2. **Quick Reference** table — change Task 2.11 status `⬜ Pending` → `✅ Complete`
  3. **Detailed task entry** — change `**Status**: ⬜ Pending` → `**Status**: ✅ Complete`
- **Verify**: Re-read both files after updating to confirm all locations are consistent
