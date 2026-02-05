# Revised Document List

**Date**: 2026-02-05
**Author**: Claude Code
**Total Documents**: 30 (29 existing + 1 new)

## Executive Summary

The current KB contains 29 well-structured documents. Task 1 identified 9 fixes needed across 5 documents (primarily content additions). Task 2 confirmed good P1/P2 use case coverage. This revision adds 1 new FAQ document and enriches 5 existing documents to address all 9 failing queries. Expected impact: 82% → 90%+ retrieval hit rate.

---

## Current KB Inventory

### 01_regulatory/ (14 documents)

#### Singapore Customs (6 documents)

| # | File | Use Cases | Action | Notes |
|---|------|-----------|--------|-------|
| 1 | sg_export_procedures.md | UC-1.1 | CARRY FORWARD | Good coverage for export docs |
| 2 | sg_import_procedures.md | UC-2.1 | CARRY FORWARD | Good coverage for import process |
| 3 | sg_gst_guide.md | UC-2.1 | CARRY FORWARD | Covers GST queries well |
| 4 | sg_certificates_of_origin.md | UC-2.3 | CARRY FORWARD | CO requirements covered |
| 5 | sg_free_trade_zones.md | UC-2.1 | CARRY FORWARD | FTZ procedures covered |
| 6 | sg_hs_classification.md | UC-2.2 | **ENRICH** | Add customs ruling application process (#19) |

#### ASEAN Trade (3 documents)

| # | File | Use Cases | Action | Notes |
|---|------|-----------|--------|-------|
| 7 | atiga_overview.md | UC-2.3 | **ENRICH** | Add "duty rate" terminology (#15) |
| 8 | asean_rules_of_origin.md | UC-2.3 | CARRY FORWARD | RoO well documented |
| 9 | asean_tariff_finder_guide.md | UC-2.2, UC-2.3 | CARRY FORWARD | Tariff lookup covered |

#### Country Specific (5 documents)

| # | File | Use Cases | Action | Notes |
|---|------|-----------|--------|-------|
| 10 | indonesia_import_requirements.md | UC-2.4 | CARRY FORWARD | Halal, BPOM covered |
| 11 | malaysia_import_requirements.md | UC-2.4 | CARRY FORWARD | De minimis covered |
| 12 | thailand_import_requirements.md | UC-2.4 | CARRY FORWARD | BOI procedures |
| 13 | vietnam_import_requirements.md | UC-2.4 | CARRY FORWARD | E-commerce rules |
| 14 | philippines_import_requirements.md | UC-2.4 | CARRY FORWARD | Permits covered |

### 02_carriers/ (6 documents)

#### Ocean (4 documents)

| # | File | Use Cases | Action | Notes |
|---|------|-----------|--------|-------|
| 15 | pil_service_summary.md | UC-3.1, UC-3.2 | CARRY FORWARD | Good coverage |
| 16 | maersk_service_summary.md | UC-3.1, UC-3.2 | CARRY FORWARD | VGM, SI covered |
| 17 | one_service_summary.md | UC-3.1, UC-3.2 | CARRY FORWARD | Service network |
| 18 | evergreen_service_summary.md | UC-3.1, UC-3.2 | CARRY FORWARD | Routes covered |

#### Air (2 documents)

| # | File | Use Cases | Action | Notes |
|---|------|-----------|--------|-------|
| 19 | sia_cargo_service_guide.md | UC-3.1 | CARRY FORWARD | Air services |
| 20 | cathay_cargo_service_guide.md | UC-3.1 | CARRY FORWARD | Air services |

### 03_reference/ (3 documents)

#### Incoterms (2 documents)

| # | File | Use Cases | Action | Notes |
|---|------|-----------|--------|-------|
| 21 | incoterms_2020_reference.md | UC-1.3 | CARRY FORWARD | All 11 terms covered |
| 22 | incoterms_comparison_chart.md | UC-1.3 | CARRY FORWARD | Responsibility matrix |

#### HS Codes (1 document)

| # | File | Use Cases | Action | Notes |
|---|------|-----------|--------|-------|
| 23 | hs_code_structure_guide.md | UC-2.2 | CARRY FORWARD | Structure explained |

### 04_internal_synthetic/ (6 documents)

#### Policies (2 documents)

| # | File | Use Cases | Action | Notes |
|---|------|-----------|--------|-------|
| 24 | service_terms_conditions.md | UC-1.1, UC-4.1, UC-4.2 | **ENRICH** | Add door-to-door inclusions (#32), import permit services (#37) |
| 25 | sla_policy.md | UC-4.1, UC-4.2 | **ENRICH** | Add delivery SLA section (#31) |

#### Procedures (3 documents)

| # | File | Use Cases | Action | Notes |
|---|------|-----------|--------|-------|
| 26 | booking_procedure.md | UC-1.1, UC-1.2 | **ENRICH** | Add 4 sections (#2, #5, #6, #7) |
| 27 | cod_procedure.md | UC-4.3 | CARRY FORWARD | COD process covered |
| 28 | escalation_procedure.md | UC-3.3 | CARRY FORWARD | Escalation paths covered |

#### Service Guides (1 document)

| # | File | Use Cases | Action | Notes |
|---|------|-----------|--------|-------|
| 29 | fta_comparison_matrix.md | UC-2.3 | CARRY FORWARD | FTA comparison |

---

## Task 1 Fixes Applied

### Fix 1: Query #2 - LCL Booking Lead Time
- **Target**: booking_procedure.md
- **Action**: ENRICH
- **Content to Add**:
  ```markdown
  ## Recommended Booking Lead Times

  **How far in advance should I book?**

  | Cargo Type | Recommended Advance Booking | Minimum Notice |
  |------------|----------------------------|----------------|
  | FCL Standard | 5-7 days before cargo ready | 3 days |
  | LCL Standard | 7-10 days before cargo ready | 5 days |
  | Reefer (FCL) | 10-14 days before cargo ready | 7 days |
  | Out-of-Gauge | 14+ days before cargo ready | 10 days |
  | Dangerous Goods | 14+ days before cargo ready | 10 days |

  **Why book early?**
  - Ensures space availability on preferred vessel
  - Allows time for documentation preparation
  - Avoids peak season surcharges
  - LCL consolidation schedules are fixed; late bookings may miss cutoff
  ```
- **Section Placement**: After Section 4 (Booking Process Overview), before Step 1

---

### Fix 2: Query #5 - Commercial Invoice for Samples
- **Target**: booking_procedure.md
- **Action**: ENRICH
- **Content to Add**:
  ```markdown
  ### Special Cases: Samples and No-Value Goods

  **Do I need a commercial invoice for samples with no commercial value?**

  **Yes, a commercial invoice is always required**, even for samples or gifts with no commercial value.

  | Scenario | Invoice Requirement | Declared Value |
  |----------|---------------------|----------------|
  | Trade samples | Required | "No Commercial Value" or NFV |
  | Promotional items | Required | Nominal value (e.g., SGD 1) |
  | Gifts | Required | Fair market value or nominal |
  | Warranty replacements | Required | Replacement value |

  **Important Notes**:
  - Mark invoice clearly: "Sample - Not for Resale" or "No Commercial Value"
  - Some countries require minimum declared value for customs purposes
  - Zero-value declarations may trigger customs inspection
  - Insurance claims require accurate value declaration
  ```
- **Section Placement**: Within documentation requirements section (around Step 6)

---

### Fix 3: Query #6 - Bill of Lading Definition
- **Target**: booking_procedure.md
- **Action**: ENRICH
- **Content to Add**:
  ```markdown
  ### What is a Bill of Lading?

  **A Bill of Lading (B/L) is a legal document issued by the carrier** (shipping line) or their agent that serves three essential purposes:

  | Function | Description |
  |----------|-------------|
  | **Receipt** | Confirms carrier received the goods in stated condition |
  | **Contract of Carriage** | Evidence of the transportation agreement |
  | **Document of Title** | Grants ownership/control of the goods |

  **Who issues the Bill of Lading?**
  - The **ocean carrier (shipping line)** issues the B/L after cargo is loaded
  - As freight forwarder, we prepare the B/L draft and submit to the carrier
  - Carrier releases final B/L once vessel departs

  **Types of Bill of Lading**:
  - **Original B/L**: Negotiable, required for Letter of Credit shipments
  - **Telex Release**: Carrier releases cargo without original documents
  - **Sea Waybill**: Non-negotiable, faster release at destination
  - **Express B/L**: Electronic, no paper original required
  ```
- **Section Placement**: At the beginning of Section 8 (Bill of Lading Preparation)

---

### Fix 4: Query #7 - Packing List Requirement
- **Target**: booking_procedure.md
- **Action**: ENRICH
- **Content to Add**:
  ```markdown
  ### Mandatory Documents

  **Can we ship without a packing list?**

  **No. A packing list is mandatory for all shipments and cannot be waived.**

  | Document | Status | Why Required |
  |----------|--------|--------------|
  | Commercial Invoice | **Mandatory** | Customs valuation, duty calculation |
  | Packing List | **Mandatory** | Cargo verification, customs clearance |
  | Bill of Lading / Airway Bill | **Mandatory** | Contract of carriage, title |

  **Packing List Requirements**:
  - Itemized list of all goods in shipment
  - Quantities, weights (gross and net), dimensions
  - Package marks and numbers
  - Must match commercial invoice
  - Required by customs for clearance inspection
  - Required by carrier for cargo verification

  **Shipments submitted without a packing list will be rejected.**
  ```
- **Section Placement**: Within documentation section, after commercial invoice discussion

---

### Fix 5: Query #15 - ATIGA Duty Rate Terminology
- **Target**: atiga_overview.md
- **Action**: ENRICH
- **Content to Add**:
  ```markdown
  ### ATIGA Preferential Duty Rate

  **What is the ATIGA preferential duty rate?**

  The ATIGA preferential duty rate is **0% (zero percent)** for approximately 98.86% of all products traded between ASEAN member states.

  | Tariff Status | Coverage | Products |
  |--------------|----------|----------|
  | **0% duty rate** | 98.86% | Most manufactured goods, electronics, textiles |
  | **Reduced rates** | ~1% | Some agricultural products |
  | **Sensitive list** | <0.2% | Rice, sugar, specific items |

  **Key Terms** (all mean the same thing):
  - ATIGA preferential duty rate = 0%
  - ATIGA tariff rate = 0%
  - Duty-free under ATIGA
  - Tariff-free under ATIGA
  - Zero tariff

  **To qualify for the 0% duty rate**:
  1. Product must originate from an ASEAN member state
  2. Must meet Rules of Origin (40% RVC or CTC criteria)
  3. Must have valid Form D Certificate of Origin
  4. Form D must be presented to importing country customs
  ```
- **Section Placement**: After "Key Provisions > Tariff Liberalization" section

---

### Fix 6: Query #19 - Customs Ruling Application Process
- **Target**: sg_hs_classification.md
- **Action**: ENRICH
- **Content to Add**:
  ```markdown
  ## How to Apply for a Classification Ruling

  **What is a Classification Ruling?**
  A formal decision by Singapore Customs on the correct HS code for your product. Rulings provide certainty and are binding.

  **When to Request a Ruling**:
  - Product classification is unclear
  - Product is new or innovative
  - You want advance certainty before import/export
  - Previous classifications were challenged

  ### Step-by-Step Application Process

  **Step 1: Prepare Documentation**
  | Required | Optional (Helpful) |
  |----------|-------------------|
  | Completed application form | Product photos |
  | Product samples or detailed specs | Manufacturing process description |
  | Technical brochures | Competitor classification references |
  | Material composition | Intended use statement |

  **Step 2: Submit via Customs@SG Portal**
  1. Log in to [customs.gov.sg](https://www.customs.gov.sg)
  2. Navigate to "Harmonised System Classification" section
  3. Select "Apply for Classification Ruling"
  4. Upload documents and complete form
  5. Pay application fee: **S$75** (non-refundable)

  **Step 3: Processing**
  - Standard processing time: **30 working days** from complete submission
  - Complex cases may take longer
  - Customs may request additional information

  **Step 4: Receive Ruling**
  - Ruling issued in writing
  - Specifies the HS code and reasoning
  - Validity: As stated in ruling letter (typically 3 years)
  - Ruling is binding unless product changes
  ```
- **Section Placement**: New section after "Classification Process"

---

### Fix 7: Query #31 - Delivery SLA for Singapore
- **Target**: sla_policy.md
- **Action**: ENRICH
- **Content to Add**:
  ```markdown
  ## 5. Delivery SLAs

  ### 5.1 Standard Delivery Commitments

  **What is our standard delivery SLA for Singapore?**

  | Destination | Service Type | Delivery SLA | Notes |
  |-------------|--------------|--------------|-------|
  | **Singapore (local)** | Door-to-door | 1-2 working days from arrival | After customs clearance |
  | **Singapore (local)** | Port pickup | Same day (if cleared by 2 PM) | Customer collects |
  | **Malaysia (Peninsular)** | Door-to-door | 3-5 working days | Cross-border clearance |
  | **Malaysia (East)** | Door-to-door | 5-7 working days | Additional transshipment |
  | **ASEAN (other)** | Door-to-door | 5-10 working days | Varies by destination |

  ### 5.2 SLA Calculation

  **Delivery SLA starts**: After cargo arrives at destination port/airport AND customs clearance is completed

  **Excluded from SLA calculation**:
  - Customs inspection delays
  - Permit application delays
  - Customer-caused delays (incomplete documents, unavailable for delivery)
  - Force majeure events
  - Public holidays

  ### 5.3 Expedited Delivery Options

  | Service | SLA | Premium |
  |---------|-----|---------|
  | Express delivery (Singapore) | Same-day (if cleared by 12 PM) | +30% |
  | Priority clearance | 4-hour customs processing | +S$150 |
  | Weekend delivery | Saturday delivery available | +50% |
  ```
- **Section Placement**: New Section 5 after Section 4

---

### Fix 8: Query #32 - Customs Clearance in Door-to-Door
- **Target**: service_terms_conditions.md
- **Action**: ENRICH
- **Content to Add**:
  ```markdown
  ### 2.3 Door-to-Door Service Definition

  **Is customs clearance included in door-to-door service?**

  **Yes, customs clearance is included as standard** in our door-to-door service.

  | Service Component | Door-to-Door | Port-to-Port |
  |-------------------|--------------|--------------|
  | Collection from shipper | ✅ Included | ❌ Not included |
  | Export customs clearance | ✅ Included | ❌ Not included |
  | Ocean/air freight | ✅ Included | ✅ Included |
  | **Import customs clearance** | ✅ **Included** | ❌ Not included |
  | Destination delivery | ✅ Included | ❌ Not included |

  **What's NOT included** (payable separately):
  - Duties and taxes (always consignee's account unless DDP)
  - Cargo insurance (available as add-on)
  - Special permits/licenses (we handle application, fees extra)
  - Storage beyond free time
  - Inspection fees if cargo examined

  **Note**: Under DDP (Delivered Duty Paid) terms, duties and taxes are also included in our service.
  ```
- **Section Placement**: After Section 2.2 (Service Limitations)

---

### Fix 9: Query #37 - Import Permit Handling
- **Target**: service_terms_conditions.md
- **Action**: ENRICH
- **Content to Add**:
  ```markdown
  ### 2.4 Import Permit Services

  **Do you handle import permit applications?**

  **Yes, we handle import permit applications** on your behalf as part of our customs brokerage services.

  | Permit Type | We Handle | Requirements |
  |-------------|-----------|--------------|
  | Standard import permits | ✅ Yes | Complete shipping documents |
  | Controlled goods permits | ✅ Yes | Customer's license required |
  | Food/health permits (SFA) | ✅ Yes | Product registration needed |
  | Transhipment permits | ✅ Yes | Routing details required |

  **What We Do**:
  - Apply via TradeNet on your behalf
  - Track permit status
  - Coordinate with relevant authorities (Singapore Customs, SFA, HSA, etc.)
  - Handle permit amendments if needed

  **Processing Times**:
  | Permit Type | Standard Processing |
  |-------------|---------------------|
  | Standard import permit | Same day (if submitted by 2 PM) |
  | Controlled goods | 1-3 working days |
  | Food/health products | 3-5 working days |

  **Fees**: Permit application fee + government fees (varies by permit type)

  **Note**: For controlled goods, customer must hold the relevant license. We cannot apply for licenses on your behalf.
  ```
- **Section Placement**: After Section 2.3 (Door-to-Door Service)

---

## New Documents

### Document: Frequently Asked Questions (FAQ)
- **File**: `04_internal_synthetic/service_guides/customer_faq.md`
- **Type**: Synthetic Internal
- **Purpose**: Centralized, retrieval-optimized answers to common customer questions
- **Use Cases**: UC-1.1, UC-1.2, UC-4.1, UC-4.2
- **Priority**: P1

**Justification**:
1. Multiple failing queries are "common questions" that should have direct, standalone answers
2. FAQ format is highly retrieval-friendly (each Q&A is self-contained)
3. Consolidates scattered information into one searchable location
4. Addresses the pattern found in Task 1: many failures are simple questions buried in procedural documents

**Proposed Structure**:
```markdown
---
title: Frequently Asked Questions
source: Internal
source_type: synthetic_internal
last_updated: YYYY-MM-DD
jurisdiction: SG
category: reference
use_cases: [UC-1.1, UC-1.2, UC-4.1, UC-4.2]
retrieval_keywords: [FAQ, questions, help, how do I, what is, can I]
---

# Frequently Asked Questions

## Booking Questions
- How far in advance should I book? [Answer]
- What documents do I need? [Answer]
- Can I amend my booking? [Answer]

## Documentation Questions
- Do I need a commercial invoice for samples? [Answer]
- What is a Bill of Lading? [Answer]
- Can I ship without a packing list? [Answer]

## Customs Questions
- What's the ATIGA duty rate? [Answer]
- How do I apply for a customs ruling? [Answer]

## Service Questions
- What's included in door-to-door? [Answer]
- Do you handle permit applications? [Answer]
- What's our delivery SLA? [Answer]
```

---

## Use Case Coverage Matrix

| Use Case | Priority | Primary Document | Backup Document | Status |
|----------|----------|------------------|-----------------|--------|
| UC-1.1 Export Docs | P1 | booking_procedure.md | sg_export_procedures.md | ✅ Covered |
| UC-1.2 Lead Times | P1 | booking_procedure.md | carrier_summaries | ✅ **Enhanced** |
| UC-1.3 Incoterms | P1 | incoterms_2020_reference.md | incoterms_comparison_chart.md | ✅ Covered |
| UC-1.4 Cargo Types | P2 | booking_procedure.md | carrier_summaries | ✅ Covered |
| UC-2.1 SG GST | P1 | sg_gst_guide.md | sg_import_procedures.md | ✅ Covered |
| UC-2.2 HS Codes | P1 | sg_hs_classification.md | hs_code_structure_guide.md | ✅ **Enhanced** |
| UC-2.3 CO Requirements | P1 | sg_certificates_of_origin.md | atiga_overview.md | ✅ **Enhanced** |
| UC-2.4 Import Reqs | P2 | country_specific/*.md | - | ✅ Covered |
| UC-3.1 Carrier Services | P1 | *_service_summary.md | - | ✅ Covered |
| UC-3.2 Carrier Docs | P2 | carrier_summaries | booking_procedure.md | ✅ Covered |
| UC-3.3 Carrier Contact | P2 | escalation_procedure.md | carrier_summaries | ✅ Covered |
| UC-4.1 SLA Terms | P2 | sla_policy.md | service_terms_conditions.md | ✅ **Enhanced** |
| UC-4.2 Service Scope | P3 | service_terms_conditions.md | customer_faq.md | ✅ **Enhanced** |
| UC-4.3 COD | P3 | cod_procedure.md | - | ✅ Covered |

**All P1 use cases**: ✅ Covered with enhancements
**All P2 use cases**: ✅ Covered
**All P3 use cases**: ✅ Covered

---

## Document Action Summary

| Action | Count | Documents |
|--------|-------|-----------|
| **CARRY FORWARD** | 24 | sg_export_procedures, sg_import_procedures, sg_gst_guide, sg_certificates_of_origin, sg_free_trade_zones, asean_rules_of_origin, asean_tariff_finder_guide, indonesia_import, malaysia_import, thailand_import, vietnam_import, philippines_import, pil_service, maersk_service, one_service, evergreen_service, sia_cargo, cathay_cargo, incoterms_2020, incoterms_chart, hs_code_structure, cod_procedure, escalation_procedure, fta_comparison |
| **ENRICH** | 5 | booking_procedure.md (4 sections), service_terms_conditions.md (2 sections), sla_policy.md (1 section), atiga_overview.md (1 section), sg_hs_classification.md (1 section) |
| **RESTRUCTURE** | 0 | - |
| **RE-SCRAPE** | 0 | - |
| **CREATE** | 1 | customer_faq.md |

**Total**: 30 documents

---

## Retrieval-First Guidelines

### 1. Frontload Key Terms

Place the most important search terms in the first paragraph of each section.

**Before** (buried):
> The process for determining the correct HS classification involves several steps. First, traders should consult the tariff schedule...

**After** (frontloaded):
> **How do I find the right HS code?** To classify your product correctly, follow these steps...

### 2. Self-Contained Sections

Each section should answer its question completely without requiring other sections.

**Checklist**:
- [ ] Can this section stand alone as a chunk?
- [ ] Does it directly answer a likely customer question?
- [ ] Are key terms and synonyms included?

### 3. Explicit Q&A Format

Where appropriate, use question-answer format for common queries.

**Format**:
```markdown
### [Question in customer's language]

**[Direct answer in bold]**

[Supporting details, tables, examples]
```

### 4. Synonym Inclusion

Include alternative terms customers might use.

| Canonical Term | Include Synonyms |
|---------------|------------------|
| Bill of Lading | B/L, BL, shipping document |
| Commercial Invoice | CI, invoice, sales invoice |
| Duty rate | Tariff rate, customs duty, import duty |
| FOB | Free on Board, FOB Singapore |
| LCL | Less than Container, loose cargo, consolidation |

### 5. Table Format for Lookup Data

Use tables for data that users need to look up quickly.

```markdown
| Cargo Type | Booking Lead Time |
|------------|-------------------|
| FCL | 5-7 days |
| LCL | 7-10 days |
```

---

## Updated Frontmatter Template

```yaml
---
title: [Document Title]
source_org: [Organization name, e.g., "Singapore Customs" or "Internal"]
source_urls:
  - url: [Primary URL]
    description: [Brief description of what this URL provides]
    retrieved_date: YYYY-MM-DD
    verification_status: [verified | partial | unverified]
source_type: [public_regulatory | public_carrier | synthetic_internal]
last_updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
verification_method: [browser | api | internal_review]
jurisdiction: [SG | MY | ID | TH | VN | PH | ASEAN | Global]
category: [customs | carrier | policy | procedure | reference]
use_cases: [UC-1.1, UC-2.3]
priority: [P1 | P2 | P3]
document_id: [Internal reference, e.g., SOP-001]
version: [Document version]
retrieval_keywords: [keyword1, keyword2, keyword3]
---
```

**New Fields Added**:
- `priority`: Indicates P1/P2/P3 for retrieval weighting
- `retrieval_keywords`: Additional terms for semantic search

---

## Implementation Notes

### Phase 3 Execution Order

1. **Create new FAQ document** first (provides immediate retrieval improvement)
2. **ENRICH booking_procedure.md** (addresses 4 of 9 failures)
3. **ENRICH service_terms_conditions.md** (addresses 2 failures)
4. **ENRICH sla_policy.md** (addresses 1 failure)
5. **ENRICH atiga_overview.md** (addresses 1 failure)
6. **ENRICH sg_hs_classification.md** (addresses 1 failure)
7. **CARRY FORWARD** remaining 24 documents (copy as-is)

### Content Addition Guidelines

When adding new sections to existing documents:
- Place new content after logical predecessors (use section placement notes)
- Maintain existing document structure and formatting
- Add to table of contents if document has one
- Increment document version number
- Update `last_updated` date

### Quality Checklist Before Ingestion

For each ENRICH document:
- [ ] New content added at specified location
- [ ] Frontmatter updated (version, date)
- [ ] No broken internal references
- [ ] Tables properly formatted
- [ ] Q&A format used where specified

---

*Report generated as part of Week 3 Task 3: Revised Document List*
