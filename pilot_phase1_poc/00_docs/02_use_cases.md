# 02 - Use Case Catalog

**Document Type**: Use Case Specification  
**Pilot**: Waypoint Phase 1 POC  
**Version**: 1.0

---

## Overview

This catalog defines the customer service scenarios the co-pilot must handle. Use cases are organized by category and prioritized for the 30-day POC timeline.

**Design Principle**: Each use case is answerable from the knowledge base alone — no live system integration required.

---

## Priority Definitions

| Priority | Meaning | POC Target |
|----------|---------|------------|
| **P1** | Must have for POC success | Implement in Week 1-2 |
| **P2** | Should have; strengthens demo | Implement in Week 3 |
| **P3** | Nice to have; defer if needed | Only if time permits |

---

## Category 1: Shipment Booking & Documentation

### UC-1.1: Export Documentation Requirements (P1)

**Scenario**: Agent needs to advise customer on required documents for a specific shipment.

**Example Queries**:
- "What documents do I need for an FCL export from Singapore to Jakarta?"
- "Is a Certificate of Origin required for shipments to Vietnam?"
- "What's the difference between a Bill of Lading and a Sea Waybill?"

**Expected Response Pattern**:
> For an FCL export from Singapore to Indonesia, you typically need:
> - Commercial Invoice
> - Packing List  
> - Bill of Lading
> - Certificate of Origin (Form D for ATIGA preferential rates)
> - [Additional docs based on cargo type]
>
> *Source: Singapore Customs Export Procedures Guide, Section 3.2*

**Knowledge Sources Required**:
- Singapore Customs export procedures
- Indonesia INSW import requirements
- ATIGA Certificate of Origin guidelines

---

### UC-1.2: Lead Time & Booking Cutoffs (P1)

**Scenario**: Agent needs to provide realistic timelines for shipment planning.

**Example Queries**:
- "How far in advance should we book an LCL shipment to Manila?"
- "What's the typical transit time Singapore to Bangkok by sea?"
- "When is the documentation cutoff for this week's sailing?"

**Expected Response Pattern**:
> For LCL shipments Singapore to Manila:
> - Recommended booking lead time: 5-7 working days before cargo ready date
> - Typical transit time: 7-10 days (depending on carrier/routing)
> - Documentation cutoff: Usually 2-3 days before vessel departure
>
> *Source: [Carrier] Service Guide, LCL Procedures*

**Knowledge Sources Required**:
- Carrier sailing schedules (general patterns)
- LCL consolidation procedures
- Port cutoff guidelines

---

### UC-1.3: Incoterms Explanation (P1)

**Scenario**: Agent needs to clarify responsibility boundaries for customers.

**Example Queries**:
- "What does FOB mean and when does our responsibility end?"
- "Customer is asking about CIF vs CFR - what's the difference?"
- "Under DDP, who handles customs clearance?"

**Expected Response Pattern**:
> Under FOB (Free On Board):
> - Seller's responsibility ends when goods pass the ship's rail at origin port
> - Buyer assumes risk and cost from that point
> - Seller handles export clearance; buyer handles import clearance
>
> *Source: ICC Incoterms 2020 Guide*

**Knowledge Sources Required**:
- Incoterms 2020 reference guide
- Synthetic internal policy on standard terms offered

---

### UC-1.4: Cargo Type Requirements (P2)

**Scenario**: Agent needs to advise on special handling or restrictions.

**Example Queries**:
- "Can we ship lithium batteries by sea? What's required?"
- "What's the process for shipping temperature-controlled goods?"
- "Are there restrictions on shipping electronics to Indonesia?"

**Expected Response Pattern**:
> Lithium batteries by sea freight:
> - Must comply with IMDG Code requirements
> - UN3481 (packed with equipment) or UN3480 (standalone)
> - Requires proper packaging, labeling, and documentation
> - Some carriers have additional restrictions
> - Note: This is general guidance; specific shipments should be reviewed by our DG specialist.
>
> *Source: IMDG Code Chapter 3.3, Carrier DG Acceptance Policies*

**Knowledge Sources Required**:
- IMDG Code summary (public excerpts)
- Carrier dangerous goods policies
- Synthetic internal DG handling procedure

---

## Category 2: Customs & Regulatory

### UC-2.1: Singapore GST & Duty Queries (P1)

**Scenario**: Agent needs to explain tax treatment for imports/exports.

**Example Queries**:
- "Is GST applicable on goods stored in FTZ?"
- "What's the current GST rate for imports into Singapore?"
- "How does the Major Exporter Scheme work?"

**Expected Response Pattern**:
> Singapore GST on imports:
> - Current rate: 9% (as of 2024)
> - GST is payable on all goods imported into Singapore unless specifically exempted
> - Goods in Free Trade Zones (FTZ) are GST-suspended until they enter customs territory
> - Major Exporter Scheme (MES) allows approved companies to import goods with GST suspended
>
> *Source: Singapore Customs GST Guide for Imports*

**Knowledge Sources Required**:
- Singapore Customs GST guides
- FTZ procedures documentation
- Approved schemes overview (MES, 3PL scheme)

---

### UC-2.2: HS Code Guidance (P1)

**Scenario**: Agent needs to help customer understand classification.

**Example Queries**:
- "How do I find the right HS code for my product?"
- "What's the HS code structure?"
- "Where can I check duty rates for a specific HS code?"

**Expected Response Pattern**:
> HS Code structure:
> - First 6 digits: Internationally standardized (Harmonized System)
> - Digits 7-8: ASEAN Harmonized Tariff Nomenclature (AHTN)
> - Digits 9-10: National subdivision (varies by country)
>
> To find the right HS code:
> 1. Use Singapore Customs' Tradenet HS/CA Product Code Search
> 2. Consult the ASEAN Tariff Finder for regional codes
> 3. For complex products, request a ruling from Customs
>
> *Source: Singapore Customs HS Classification Guide*

**Knowledge Sources Required**:
- HS code structure explanation
- Singapore Customs classification resources
- ASEAN Tariff Finder reference

---

### UC-2.3: Certificate of Origin Requirements (P1)

**Scenario**: Agent needs to advise on preferential tariff documentation.

**Example Queries**:
- "Does my shipment to Thailand qualify for ATIGA rates?"
- "What's the difference between Form D and Form E?"
- "How do we apply for a Certificate of Origin?"

**Expected Response Pattern**:
> ATIGA preferential tariffs (Form D):
> - Applies to trade between ASEAN member states
> - Product must meet Rules of Origin (typically 40% Regional Value Content)
> - Form D must be issued by authorized body (Singapore Customs or approved organizations)
> - Must be presented to importing country customs for preferential rate
>
> Form D vs Form E:
> - Form D: ASEAN Trade in Goods Agreement (ATIGA) — intra-ASEAN
> - Form E: ASEAN-China FTA (ACFTA) — ASEAN to/from China
>
> *Source: Singapore Customs Certificates of Origin Guide*

**Knowledge Sources Required**:
- Singapore Customs CO guide
- ATIGA Rules of Origin summary
- FTA comparison matrix

---

### UC-2.4: Import Requirements by Country (P2)

**Scenario**: Agent needs to advise on destination country requirements.

**Example Queries**:
- "What permits are needed to import food products into Indonesia?"
- "Does Malaysia require pre-shipment inspection?"
- "What's the de minimis threshold for Philippines?"

**Expected Response Pattern**:
> Importing food products into Indonesia:
> - BPOM (Food & Drug Authority) registration required for processed foods
> - ML (Angka Surat) import permit from Ministry of Trade
> - Halal certification mandatory for applicable products (by Oct 2026 for all F&B)
> - SNI certification may apply depending on product category
>
> *Source: Indonesia INSW Portal, Ministry of Trade Regulation 18/2021*

**Knowledge Sources Required**:
- Indonesia INSW LARTAS requirements
- Malaysia customs guides
- Philippines BOC procedures
- Regional de minimis thresholds

---

## Category 3: Carrier Information

### UC-3.1: Carrier Service Capabilities (P1)

**Scenario**: Agent needs to compare or recommend carriers.

**Example Queries**:
- "Which carriers have direct service to Ho Chi Minh City?"
- "Does PIL offer LCL consolidation to Surabaya?"
- "What's Maersk's transit time Singapore to Port Klang?"

**Expected Response Pattern**:
> Direct ocean services Singapore to Ho Chi Minh City:
> - PIL: Weekly service, ~3-4 days transit
> - Maersk: Multiple weekly sailings, ~3 days transit
> - ONE: Weekly service via their intra-Asia network
> - Evergreen: Available but may involve transshipment
>
> Note: Schedules subject to change; confirm specific sailings with booking team.
>
> *Source: Carrier Service Guides (PIL, Maersk, ONE)*

**Knowledge Sources Required**:
- Carrier service guides/brochures
- Port pair coverage matrices
- Transit time references

---

### UC-3.2: Carrier Documentation Requirements (P2)

**Scenario**: Agent needs to clarify carrier-specific procedures.

**Example Queries**:
- "What's the VGM submission deadline for Maersk?"
- "How do I submit shipping instructions to ONE?"
- "Does PIL accept electronic Bill of Lading?"

**Expected Response Pattern**:
> Maersk VGM (Verified Gross Mass) requirements:
> - VGM must be submitted before cargo gate-in at terminal
> - Accepted via Maersk.com, EDI, or third-party platforms
> - Cutoff typically 24-48 hours before vessel departure (varies by port)
> - Non-compliance may result in cargo being rolled
>
> *Source: Maersk Shipping Instructions Guide*

**Knowledge Sources Required**:
- Carrier SI/documentation guides
- VGM procedures by carrier
- E-BL acceptance policies

---

### UC-3.3: Carrier Contact & Escalation (P2)

**Scenario**: Agent needs to direct customer to appropriate carrier contact.

**Example Queries**:
- "How do I contact PIL for a booking amendment?"
- "What's the process to file a claim with Maersk?"
- "Who handles Evergreen's Singapore operations?"

**Expected Response Pattern**:
> For PIL booking amendments in Singapore:
> - Contact PIL Singapore customer service
> - For urgent amendments close to sailing, escalate to operations team
> - Amendment fees may apply depending on timing and type of change
>
> Note: Specific contact details should be confirmed with our operations team.
>
> *Source: PIL Singapore Service Guide*

**Knowledge Sources Required**:
- Carrier contact matrices (synthetic)
- Claims procedures summaries
- Escalation guidelines (synthetic)

---

## Category 4: Service & Policy Queries (Secondary Scope)

### UC-4.1: SLA Terms Clarification (P2)

**Scenario**: Agent needs to explain service commitments.

**Example Queries**:
- "What's our standard transit time guarantee?"
- "What happens if a shipment is delayed beyond SLA?"
- "Are weekends counted in delivery SLAs?"

**Expected Response Pattern**:
> Standard transit time commitments:
> - SLA timelines are calculated in business days (Mon-Fri, excluding public holidays)
> - Delays due to customs clearance, weather, or carrier issues are typically excluded from SLA penalties
> - Specific SLA terms depend on the service tier and contract
>
> For your specific contract terms, please check with your account manager.
>
> *Source: [Company] Standard Service Terms v2.3*

**Knowledge Sources Required**:
- Synthetic SLA policy document
- Synthetic service tier definitions
- Exception handling procedures (synthetic)

---

### UC-4.2: Service Scope Clarification (P3)

**Scenario**: Agent needs to explain what's included/excluded.

**Example Queries**:
- "Does door-to-door include customs clearance?"
- "Is insurance included in our freight quote?"
- "Do you handle permit applications?"

**Expected Response Pattern**:
> Door-to-door service scope:
> - **Included**: Origin pickup, export customs clearance, ocean/air freight, import customs clearance, destination delivery
> - **Excluded by default**: Cargo insurance (available as add-on), special permits, storage beyond free time
> - Customs duties and taxes are always for buyer's account unless otherwise agreed
>
> *Source: [Company] Service Definitions Guide*

**Knowledge Sources Required**:
- Synthetic service scope document
- Pricing inclusion/exclusion matrix (synthetic)

---

### UC-4.3: COD Procedures (P3)

**Scenario**: Agent needs to explain cash-on-delivery process.

**Example Queries**:
- "How does COD reconciliation work?"
- "When do we remit COD collections?"
- "What if the customer refuses the COD shipment?"

**Expected Response Pattern**:
> COD process overview:
> - Driver collects payment upon delivery
> - Collections reconciled daily at depot
> - Remittance to shipper typically within 3-5 business days
> - Refused shipments: Returned to origin; shipper may be charged return freight
>
> *Source: [Company] COD Operations Guide*

**Knowledge Sources Required**:
- Synthetic COD procedure document
- Regional COD variations reference

---

## Test Query Bank

For POC evaluation, use these 50 test queries (10 per category):

### Booking & Documentation (10)
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

### Customs & Regulatory (10)
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

### Carrier Information (10)
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

### SLA & Service (10)
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

### Edge Cases & Out-of-Scope (10)
41. What's the current freight rate to Jakarta? (out of scope - live rates)
42. Where is my shipment right now? (out of scope - needs tracking API)
43. Can you book a shipment for me? (out of scope - transaction)
44. I want to file a claim for damaged cargo (out of scope - complex workflow)
45. Can you ship hazmat by air? (out of scope - DG/complex)
46. What's the weather forecast for shipping? (out of scope - irrelevant)
47. Can you recommend a supplier in China? (out of scope - not logistics)
48. What's your company's financial status? (out of scope - inappropriate)
49. How do I become a freight forwarder? (out of scope - career advice)
50. What are your competitor's rates? (out of scope - competitive intel)

---

## Use Case to Knowledge Source Mapping

| Use Case | Primary Sources | Secondary Sources |
|----------|-----------------|-------------------|
| UC-1.1 Export Docs | SG Customs Export Guide | Indonesia INSW, ATIGA Guide |
| UC-1.2 Lead Times | Carrier Service Guides | Synthetic booking procedures |
| UC-1.3 Incoterms | Incoterms 2020 Reference | Synthetic policy on terms used |
| UC-1.4 Cargo Types | IMDG Code excerpts | Carrier DG policies |
| UC-2.1 SG GST | SG Customs GST Guide | FTZ procedures |
| UC-2.2 HS Codes | SG Customs HS Guide | ASEAN Tariff Finder ref |
| UC-2.3 CO Requirements | SG Customs CO Guide | ATIGA RoO summary |
| UC-2.4 Import Reqs | INSW, country guides | Regional requirements matrix |
| UC-3.1 Carrier Services | Carrier brochures | Transit time matrix |
| UC-3.2 Carrier Docs | Carrier SI guides | VGM procedures |
| UC-3.3 Carrier Contacts | Synthetic contact matrix | Escalation procedures |
| UC-4.1-4.3 Service/SLA | Synthetic policy docs | COD procedures |

---

*Next Document*: [03 - Knowledge Base Blueprint](./03_knowledge_base_blueprint.md)
