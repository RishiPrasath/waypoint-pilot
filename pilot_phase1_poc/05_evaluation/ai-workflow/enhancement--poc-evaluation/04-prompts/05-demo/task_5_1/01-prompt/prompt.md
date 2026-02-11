# Task 5.1 — Select Demo Queries (8-10)

## Persona
Senior Solutions Engineer preparing a stakeholder demo of the Waypoint RAG co-pilot POC. You have access to all Round 4 evaluation results and must select queries that best showcase the system's capabilities AND graceful limitations.

## Context
- **Round 4 results**: 50 queries evaluated, all 6 targets met
- **Metrics achieved**: Deflection 87.2%, Citation 96%, Hallucination 2%, OOS 100%, Latency 1,182ms avg
- **System**: RAG pipeline with 30 KB docs, ChromaDB, Groq LLM (Llama 3.1 8B), 4-section response card
- **Response card sections**: Answer (markdown), Sources (clickable URLs), Related Documents (category chips), Confidence Footer (badge + metadata)
- **Evaluation data**: `data/evaluation_results.json` — full responses for all 50 queries

## Task

Select **10 demo queries** from the 50 evaluated queries based on Round 4 results. The selection must:

### Selection Criteria
1. **5-6 Happy Path** — Queries that passed all checks AND produce visually rich responses (multiple sources, related docs, citations, good markdown formatting)
2. **2 OOS/Graceful Decline** — Out-of-scope queries that demonstrate the system correctly declining with appropriate messaging
3. **2 Edge/Interesting Cases** — Queries that show system behavior at boundaries (e.g., low confidence but still correct, borderline topics)

### Recommended Candidates (from Round 4 analysis)

**Happy Path (richest responses — best visual showcase):**
| ID | Category | Query | Sources | RelDocs | Citations | Why |
|----|----------|-------|---------|---------|-----------|-----|
| Q-01 | booking | What documents are needed for sea freight Singapore to Indonesia? | 4 | 8 | 1 | Richest response — 4 external URLs, 8 related docs across 4 categories |
| Q-11 | customs | What's the GST rate for imports into Singapore? | 2 | 5 | 1 | Core regulatory query, 5 related docs, Medium confidence |
| Q-14 | customs | What permits are needed to import cosmetics to Indonesia? | 4 | 4 | 1 | Multi-source regulatory, 4 external URLs |
| Q-24 | carrier | How do I submit VGM to Maersk? | 5 | 1 | 1 | Carrier-specific, 5 external URLs from Maersk |
| Q-31 | sla | What's our standard delivery SLA for Singapore? | 0 | 5 | 1 | Internal policy, 5 related docs, Medium confidence |
| Q-03 | booking | What's the difference between FCL and LCL? | 0 | 1 | 1 | Clean structured answer with headers and bullet points |

**OOS/Graceful Decline:**
| ID | Category | Query | Why |
|----|----------|-------|-----|
| Q-42 | edge_case | What is the current freight rate from Singapore to Jakarta? | Classic OOS — live rates explicitly excluded |
| Q-46 | edge_case | Can you track my shipment with BL number MAEU1234567? | Classic OOS — live tracking explicitly excluded |

**Edge/Interesting:**
| ID | Category | Query | Why |
|----|----------|-------|-----|
| Q-04 | booking | When is the SI cutoff for this week's Maersk sailing? | Failed — shows system correctly declines real-time schedule queries |
| Q-13 | customs | Is Certificate of Origin required for Thailand? | Passed with 4 sources — good cross-border regulatory example |

### Output

Create `demo/demo_queries.md` with:

1. **Ordered demo sequence** (10 queries) — number them Demo 1 through Demo 10
2. **For each query**:
   - Query text
   - Category
   - Expected behavior (what the demo should show)
   - Why selected (what capability it demonstrates)
   - Key visual elements to highlight during demo
3. **Demo flow narrative** — suggested speaking points for presenting the 10 queries in sequence
4. **Timing estimate** — ~2 minutes per query, ~20 minutes total demo

## Format

### File: `pilot_phase1_poc/05_evaluation/demo/demo_queries.md`

```markdown
# Waypoint POC Demo — Query Selection

## Demo Flow (10 queries, ~20 minutes)

### Demo 1: [Query]
- **Category**: ...
- **Expected Behavior**: ...
- **Why Selected**: ...
- **Key Visuals**: ...
- **Speaking Points**: ...

[... repeat for all 10 ...]

## Selection Rationale
- Category coverage: booking, customs, carrier, sla, edge_case
- Capability coverage: markdown rendering, sources, related docs, confidence levels, OOS handling
- All selected queries verified in Round 4 evaluation
```

### Validation
- [ ] 10 queries selected
- [ ] 5-6 happy path with rich responses
- [ ] 2 OOS/graceful decline examples
- [ ] 2 edge/interesting cases
- [ ] All 5 categories represented
- [ ] Each query has rationale documented
- [ ] Demo flow narrative included
- [ ] Timing estimate included
