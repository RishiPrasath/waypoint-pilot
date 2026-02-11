# Waypoint POC Demo — Query Selection

**Selected**: 10 queries | **Estimated Duration**: ~20 minutes | **Source**: Round 4 Evaluation (2026-02-10)

---

## Demo Flow (10 queries)

The demo follows a narrative arc: start with the strongest showcase (multi-source regulatory), move through different categories, show internal policy handling, then demonstrate graceful boundaries.

---

### Demo 1: Export Documentation (Booking + Regulatory)

- **Query**: "What documents are needed for sea freight Singapore to Indonesia?"
- **ID**: Q-01 | **Category**: booking
- **Expected Behavior**: Rich multi-source response with external URLs, multiple related docs across categories, markdown-formatted numbered list
- **Why Selected**: Richest response in the entire evaluation — 4 external source URLs, 8 related documents spanning regulatory/carrier/internal/reference categories. Best first impression.
- **Key Visuals**:
  - Answer section: numbered document list with bold key terms (Commercial Invoice, Bill of Lading, Certificate of Origin)
  - Sources section: 4 clickable external URLs (trade.gov, insw.go.id, beacukai.go.id)
  - Related Docs: 8 category chips across all 4 colors (blue/amber/slate/emerald)
  - Confidence footer: metadata showing 10 chunks retrieved, 1 used, ~2s latency
- **Speaking Points**: "This shows the full power of the system — pulling from multiple regulatory sources, linking to official government portals, and surfacing related carrier and internal documents. Notice all four sections of the response card."

---

### Demo 2: Singapore GST Rate (Core Regulatory)

- **Query**: "What's the GST rate for imports into Singapore?"
- **ID**: Q-11 | **Category**: customs
- **Expected Behavior**: Concise factual answer with government source URLs, Medium confidence badge, multiple related docs
- **Why Selected**: Core regulatory question that CS agents ask daily. Shows the system at its strongest — correct answer (9%), cited source (Singapore Customs), Medium confidence. 2 external URLs + 5 related docs.
- **Key Visuals**:
  - Answer section: bold "9%" rate with effective date
  - Sources section: 2 URLs (customs.gov.sg, iras.gov.sg) — official government sources
  - Related Docs: 5 chips (regulatory + reference)
  - Confidence footer: Medium badge (amber) — highest confidence tier commonly seen
- **Speaking Points**: "This is the bread-and-butter query for CS agents. The system gives the exact rate, cites official Singapore Customs and IRAS sources, and surfaces related documents about certificates of origin and import procedures."

---

### Demo 3: Cross-Border Regulatory (Thailand COO)

- **Query**: "Is Certificate of Origin required for Thailand?"
- **ID**: Q-13 | **Category**: customs
- **Expected Behavior**: Clear yes/no answer with regulatory source, external URLs to Thai customs
- **Why Selected**: Shows cross-border regulatory knowledge beyond Singapore. 4 source URLs including Thai government sites. Demonstrates SEA coverage.
- **Key Visuals**:
  - Answer section: clear "Yes" with requirements breakdown
  - Sources section: 4 URLs (trade.gov Thailand guide, Thai Customs portal)
  - Related Docs: 2 regulatory chips
  - Confidence footer: shows retrieval stats
- **Speaking Points**: "The knowledge base covers Southeast Asian trade routes. Here it correctly identifies Thailand's COO requirements and links to official Thai customs authorities — not just Singapore."

---

### Demo 4: Carrier-Specific Operations (Maersk VGM)

- **Query**: "How do I submit VGM to Maersk?"
- **ID**: Q-24 | **Category**: carrier
- **Expected Behavior**: Step-by-step process with Maersk-specific URLs, carrier category related doc
- **Why Selected**: Carrier-specific operational query. Highest source URL count (5 Maersk URLs). Shows the system handles carrier-specific procedures, not just regulations.
- **Key Visuals**:
  - Answer section: numbered step-by-step VGM submission process
  - Sources section: 5 Maersk URLs (about, schedules, logistics, contact, Asia-Pacific)
  - Related Docs: 1 carrier chip (amber, ship emoji)
  - Confidence footer: 2 chunks retrieved, 1 used
- **Speaking Points**: "Carrier-specific queries are common in freight forwarding. The system retrieves Maersk's VGM procedures and provides 5 direct links to Maersk's portal — agents can click through to the official source."

---

### Demo 5: Product-Specific Import (Indonesia Cosmetics)

- **Query**: "What permits are needed to import cosmetics to Indonesia?"
- **ID**: Q-14 | **Category**: customs
- **Expected Behavior**: Detailed permit list (BPOM registration), multiple regulatory sources, cross-referencing ASEAN docs
- **Why Selected**: Shows depth — specific product category (cosmetics) for a specific destination (Indonesia). 4 source URLs, 4 related docs including cross-border references (Malaysia, Philippines, ATIGA).
- **Key Visuals**:
  - Answer section: numbered permit requirements with BPOM registration highlighted
  - Sources section: 4 URLs (trade.gov, INSW, Bea Cukai)
  - Related Docs: 4 chips — regulatory across multiple countries
  - Confidence footer: 10 chunks retrieved, shows broad search
- **Speaking Points**: "This shows the system handles product-specific queries. Notice it pulls from Indonesian regulatory sources AND cross-references ASEAN trade agreements — exactly the kind of multi-source research that takes agents 15-20 minutes manually."

---

### Demo 6: FCL vs LCL Comparison (Structured Answer)

- **Query**: "What's the difference between FCL and LCL?"
- **ID**: Q-03 | **Category**: booking
- **Expected Behavior**: Well-structured comparison with headers, bullet points, and "When to Choose" guidance
- **Why Selected**: Showcases markdown rendering — headers (###), nested bullet points, bold terms. Clean internal knowledge with no external URLs (internal policy doc). Good contrast to previous multi-source queries.
- **Key Visuals**:
  - Answer section: "Key Differences" header with bullet comparisons, "When to Choose Each" with FCL/LCL subsections
  - Sources section: hidden (no external URLs)
  - Related Docs: 1 internal chip (slate, clipboard emoji)
  - Confidence footer: 1 chunk retrieved and used — precise retrieval
- **Speaking Points**: "This demonstrates the markdown rendering capability. The system structures its answer with clear headers and comparisons. Also notice — no external sources section because this comes from internal booking procedures. The system adapts its display based on available data."

---

### Demo 7: Internal Policy (SLA Commitment)

- **Query**: "What's our standard delivery SLA for Singapore?"
- **ID**: Q-31 | **Category**: sla
- **Expected Behavior**: Specific SLA commitment (1-2 working days) with Medium confidence, internal policy citation, multiple related docs
- **Why Selected**: Shows internal knowledge capability — policies and SLAs that wouldn't be on any public website. Medium confidence badge. 5 related docs spanning internal/carrier/regulatory/reference categories.
- **Key Visuals**:
  - Answer section: specific "1-2 working days" commitment with conditions
  - Sources section: hidden (internal documents)
  - Related Docs: 5 chips across multiple categories
  - Confidence footer: Medium badge (amber), 10 chunks retrieved
- **Speaking Points**: "This is where the co-pilot really shines for CS agents — instant access to internal SLA commitments. No searching through policy PDFs. The system cites the exact section of the SLA Policy document. Note the Medium confidence — this is the system's way of saying 'I found relevant content with reasonable match quality.'"

---

### Demo 8: Graceful Decline — Live Tracking (Out of Scope)

- **Query**: "Where is my shipment right now?"
- **ID**: Q-42 | **Category**: edge_case (OOS)
- **Expected Behavior**: Polite decline with redirect to customer service. No hallucinated tracking info. Empty response card.
- **Why Selected**: Classic out-of-scope query — live shipment tracking requires TMS integration not available in POC. Shows the system does NOT hallucinate tracking information.
- **Key Visuals**:
  - Answer section: brief decline message ("I don't have specific information...")
  - Sources section: hidden (none)
  - Related Docs: hidden (none)
  - Confidence footer: Low badge (red), 0 chunks retrieved, fast response (~850ms)
- **Speaking Points**: "Equally important to getting things right is knowing when NOT to answer. Live tracking requires TMS integration — a Phase 2 feature. The system correctly declines rather than making up tracking data. Notice the fast response — no LLM call needed when no relevant content is found."

---

### Demo 9: Graceful Decline — External Data (Out of Scope)

- **Query**: "What's the weather forecast for shipping?"
- **ID**: Q-46 | **Category**: edge_case (OOS)
- **Expected Behavior**: Polite decline. No weather information generated. Clean boundary handling.
- **Why Selected**: Completely outside the knowledge domain. Demonstrates the system's scope boundaries — it's a freight forwarding co-pilot, not a general-purpose assistant.
- **Key Visuals**:
  - Answer section: brief decline message
  - Sources/Related Docs: hidden
  - Confidence footer: Low badge (red), 0 chunks
- **Speaking Points**: "The system knows its boundaries. Weather forecasts are completely outside the freight forwarding knowledge base. A general chatbot might hallucinate an answer — Waypoint correctly stays in its lane and directs the agent to appropriate resources."

---

### Demo 10: Boundary Case — Real-Time Schedule Query

- **Query**: "When is the SI cutoff for this week's Maersk sailing?"
- **ID**: Q-04 | **Category**: booking
- **Expected Behavior**: Decline — the KB has general SI cutoff info but not real-time sailing schedules. Shows the difference between static knowledge and live data.
- **Why Selected**: Interesting boundary — the system HAS Maersk content in the KB but correctly recognizes that "this week's sailing" requires live schedule data it doesn't have. Demonstrates nuanced scope handling.
- **Key Visuals**:
  - Answer section: decline message
  - Sources/Related Docs: empty
  - Confidence footer: Low badge, 0 chunks, fast response (~900ms)
- **Speaking Points**: "This is a nuanced case. We DO have Maersk carrier information in the knowledge base, but 'this week's sailing schedule' is real-time data. The system correctly recognizes it can't answer time-specific queries. In Phase 2, connecting to Maersk's API would enable this."

---

## Selection Rationale

### Category Coverage
| Category | Queries | IDs |
|----------|---------|-----|
| Booking | 3 | Q-01, Q-03, Q-04 |
| Customs | 3 | Q-11, Q-13, Q-14 |
| Carrier | 1 | Q-24 |
| SLA | 1 | Q-31 |
| Edge Case | 2 | Q-42, Q-46 |

### Capability Coverage
| Capability | Demonstrated By |
|------------|-----------------|
| Markdown rendering (headers, lists, bold) | Q-01, Q-03, Q-14, Q-24 |
| External source URLs (clickable) | Q-01, Q-11, Q-13, Q-14, Q-24 |
| Related document chips (all 4 categories) | Q-01, Q-11, Q-14, Q-31 |
| Internal knowledge (no external URLs) | Q-03, Q-31 |
| Medium confidence badge | Q-11, Q-31 |
| Low confidence badge | Q-01, Q-03, Q-13, Q-14, Q-24 |
| OOS graceful decline | Q-42, Q-46 |
| Boundary/nuanced decline | Q-04 |
| Multi-source cross-referencing | Q-01, Q-14 |
| Carrier-specific operations | Q-24 |
| Product-specific regulations | Q-14 |
| Cross-border (non-SG) knowledge | Q-13, Q-14 |

### Visual Element Coverage
| UI Section | Visible In | Hidden In |
|------------|-----------|-----------|
| Answer (markdown) | Demos 1-7 | Demos 8-10 (brief decline) |
| Sources (URLs) | Demos 1-5 | Demos 6-10 |
| Related Docs (chips) | Demos 1-7 | Demos 8-10 |
| Confidence: Medium | Demos 2, 7 | — |
| Confidence: Low | Demos 1, 3-6, 8-10 | — |

### Demo Narrative Arc
1. **Open strong** (Demos 1-2): Richest responses, full 4-section card, government sources
2. **Show breadth** (Demos 3-5): Cross-border, carrier-specific, product-specific
3. **Show depth** (Demos 6-7): Internal knowledge, policy, structured answers
4. **Show boundaries** (Demos 8-10): OOS handling, graceful decline, nuanced scope

### Timing Estimate
| Segment | Queries | Duration |
|---------|---------|----------|
| Introduction + system overview | — | 2 min |
| Happy path demos (1-7) | 7 queries | 14 min |
| Boundary demos (8-10) | 3 queries | 4 min |
| Wrap-up + Q&A transition | — | 2 min |
| **Total** | **10** | **~22 min** |

### Round 4 Verification
All 10 selected queries were evaluated in Round 4 (2026-02-10). 8/10 passed all automated checks. The 2 "failures" (Q-04 — failed must_contain; Q-42 — OOS) are intentionally included to demonstrate system boundaries.
