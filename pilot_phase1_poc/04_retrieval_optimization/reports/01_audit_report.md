# Audit Report: Root Cause Analysis of Retrieval Failures

**Date**: 2026-02-05
**Analyst**: Claude Code
**Queries Analyzed**: 9
**Excluded (Out-of-scope)**: #36, #38, #44

---

## Executive Summary

Analysis of 9 failing queries reveals the following root cause distribution:

| Root Cause | Count | Queries |
|------------|-------|---------|
| **(a) Content Missing** | 5 | #2, #5, #19, #31, #32 |
| **(b) Content Buried** | 3 | #6, #7, #37 |
| **(c) Terminology Mismatch** | 1 | #15 |

**Key Finding**: Most failures (5/9) are due to missing content rather than chunking issues. The knowledge base lacks specific information for common customer questions about booking lead times, samples, delivery SLAs, and service inclusions. Fixing these requires adding new content sections to existing documents.

---

## Analysis by Query

### Query #2: "How far in advance should I book an LCL shipment?"

- **Category**: Booking
- **Expected source**: booking_procedure.md, service_terms_conditions.md
- **Raw doc search**: PARTIAL FOUND
  - Search terms: "LCL", "advance", "book"
  - Found in `sla_policy.md:105`: "LCL booking | 4 hours from customer confirmation" (processing time, not lead time)
  - Found in `booking_procedure.md:367`: "LCL cargo receipt | 2 days before ETD" (cutoff, not recommendation)
  - Found booking process overview showing Day -7 to Day 0 timeline, but no explicit recommendation
- **Chunk search**:
  - Top chunk: service_terms_conditions.md "Booking and Cancellation" section (score: 0.057)
  - Why wrong: Chunk discusses confirmation/cancellation, not advance booking recommendations
- **Root cause**: **(a) Content missing** - No explicit recommendation for LCL booking lead time
- **Proposed fix**: Add to `booking_procedure.md` Section 4:
  ```
  ## Recommended Booking Lead Times
  | Cargo Type | Recommended Advance Booking |
  |------------|----------------------------|
  | FCL Standard | 5-7 days before cargo ready |
  | LCL Standard | 7-10 days before cargo ready |
  | Reefer | 10-14 days before cargo ready |
  | Dangerous Goods | 14+ days before cargo ready |
  ```

---

### Query #5: "Do I need a commercial invoice for samples with no value?"

- **Category**: Booking
- **Expected source**: booking_procedure.md, export procedures
- **Raw doc search**: NOT FOUND
  - Search terms: "commercial invoice", "samples", "no value", "zero value"
  - Found 24 mentions of "commercial invoice" as required document
  - No mention of samples, NFV (no face value), or zero-value goods anywhere
- **Chunk search**:
  - Top chunk: pil_service_summary.md documentation requirements (score: -0.253)
  - Why wrong: Generic document list, no sample/value guidance
- **Root cause**: **(a) Content missing** - No information about samples or zero-value shipments
- **Proposed fix**: Add to `booking_procedure.md` Section 5 (Documentation):
  ```
  ### Special Cases: Samples and No-Value Goods

  **Samples with no commercial value still require a commercial invoice.**
  - Declare value as "No Commercial Value" or "NFV"
  - Include nominal value for customs purposes (e.g., SGD 1)
  - State "Sample - Not for Resale" on invoice
  - Some countries require minimum declared value
  ```

---

### Query #6: "What's a Bill of Lading and who issues it?"

- **Category**: Booking
- **Expected source**: booking_procedure.md
- **Raw doc search**: FOUND (but not as definition)
  - Search terms: "Bill of Lading", "B/L", "issues"
  - Found extensive B/L content in `booking_procedure.md` Section 8 (lines 280-311)
  - Covers B/L preparation, fields, types, but no clear DEFINITION
  - No explicit statement "The carrier issues the Bill of Lading"
- **Chunk search**:
  - Top chunk: philippines_import_requirements.md (score: -0.070)
  - Why wrong: B/L mentioned as required document, not defined
- **Root cause**: **(b) Content buried** - B/L process exists but lacks introductory definition paragraph
- **Proposed fix**: Add definition paragraph to `booking_procedure.md` Section 8:
  ```
  ## 8. Bill of Lading Preparation

  ### What is a Bill of Lading?
  A Bill of Lading (B/L) is a legal document issued by the carrier or their agent
  that serves three purposes: (1) receipt for shipped goods, (2) evidence of the
  contract of carriage, and (3) document of title. The ocean carrier (shipping line)
  issues the B/L after cargo is loaded on the vessel.
  ```

---

### Query #7: "Can we ship without a packing list?"

- **Category**: Booking
- **Expected source**: booking_procedure.md, country import requirements
- **Raw doc search**: FOUND (but in table format)
  - Search terms: "packing list", "required", "mandatory"
  - Found in `booking_procedure.md:202`: "| Packing List | Mandatory |"
  - Found in 15+ other documents listing packing list as required
  - No explicit statement answering "Can we ship without..."
- **Chunk search**:
  - Top chunk: incoterms_comparison_chart.md (score: -0.024)
  - Why wrong: Incoterms content, not documentation requirements
- **Root cause**: **(b) Content buried** - Requirement exists in table cell but no self-contained statement
- **Proposed fix**: Add to `booking_procedure.md` Section 5:
  ```
  ### Mandatory Documents

  **A packing list is mandatory for all shipments and cannot be waived.**
  The packing list must detail all items, quantities, weights, and dimensions.
  Customs authorities require it for clearance, and carriers need it for cargo
  verification. Shipments submitted without a packing list will be rejected.
  ```

---

### Query #15: "What's the ATIGA preferential duty rate?"

- **Category**: Customs
- **Expected source**: atiga_overview.md, fta_comparison_matrix.md
- **Raw doc search**: FOUND (but phrased differently)
  - Search terms: "ATIGA", "preferential", "duty rate"
  - Found in `atiga_overview.md:63-64`: "98.86% of tariff lines have been eliminated as of 2025"
  - Found in `fta_comparison_matrix.md:43`: "98.86% tariff-free"
  - Found tariff rate comparison tables
  - Never explicitly says "the ATIGA duty rate is 0%"
- **Chunk search**:
  - Top chunk: hs_code_structure_guide.md (score: 0.029)
  - Why wrong: HS codes topic, not tariff rates
- **Root cause**: **(c) Terminology mismatch** - Content uses "tariff-free" not "duty rate"
- **Proposed fix**: Add to `atiga_overview.md` Key Provisions section:
  ```
  ### ATIGA Preferential Duty Rate

  The ATIGA preferential duty rate is **0%** for 98.86% of all products traded
  between ASEAN member states. This means most goods qualifying under ATIGA
  Rules of Origin enjoy duty-free, tariff-free import into any ASEAN country.
  Only sensitive agricultural products (rice, sugar) retain some tariffs.
  ```

---

### Query #19: "How do I apply for a Customs ruling on HS code?"

- **Category**: Customs
- **Expected source**: sg_hs_classification.md
- **Raw doc search**: PARTIAL FOUND
  - Search terms: "customs ruling", "classification ruling", "apply", "HS code"
  - Found in `sg_hs_classification.md:99-114`: "Requesting a Classification Ruling" section
  - Has fee (S$75) and when to request, but NO APPLICATION PROCESS
  - Found in `sg_export_procedures.md:47`: mention of ruling fee
- **Chunk search**:
  - Top chunk: hs_code_structure_guide.md (score: 0.340)
  - Why wrong: HS code structure, not ruling application process
- **Root cause**: **(a) Content missing** - Section exists but lacks step-by-step application process
- **Proposed fix**: Expand `sg_hs_classification.md` "Requesting a Classification Ruling" section:
  ```
  ## How to Apply for a Classification Ruling

  1. **Prepare Documentation**:
     - Completed application form
     - Product samples or photos
     - Technical specifications
     - Manufacturing process description

  2. **Submit via Customs@SG Portal**:
     - Log in to customs.gov.sg
     - Navigate to "Classification Ruling Application"
     - Upload documents and pay S$75 fee

  3. **Processing Time**: 30 working days from complete submission

  4. **Ruling Validity**: As stated in ruling letter (typically 3 years)
  ```

---

### Query #31: "What's our standard delivery SLA for Singapore?"

- **Category**: SLA
- **Expected source**: sla_policy.md
- **Raw doc search**: NOT FOUND
  - Search terms: "delivery SLA", "Singapore", "standard delivery"
  - `sla_policy.md` is comprehensive but focuses on RESPONSE times and PROCESSING times
  - No delivery time commitments (e.g., "X days to deliver within Singapore")
  - Only found transit time mentions in carrier documents
- **Chunk search**:
  - Top chunk: sia_cargo_service_guide.md (score: 0.185)
  - Why wrong: Carrier-specific, not company SLA
- **Root cause**: **(a) Content missing** - No delivery SLA for Singapore destinations
- **Proposed fix**: Add to `sla_policy.md` new Section 5.5:
  ```
  ### 5.5 Delivery SLAs

  | Destination | Service Type | Standard Delivery |
  |-------------|--------------|-------------------|
  | Singapore (local) | Door-to-door | 1-2 working days from arrival |
  | Singapore (local) | Port pickup | Same day if cleared by 2 PM |
  | Malaysia (Peninsular) | Door-to-door | 3-5 working days |
  | ASEAN (other) | Door-to-door | 5-10 working days |

  *Note: Excludes customs clearance delays beyond our control*
  ```

---

### Query #32: "Is customs clearance included in door-to-door?"

- **Category**: SLA
- **Expected source**: service_terms_conditions.md
- **Raw doc search**: NOT FOUND
  - Search terms: "customs clearance", "door-to-door", "included"
  - `service_terms_conditions.md:54` lists "Customs Brokerage" as a service
  - `incoterms_2020_reference.md` discusses customs responsibilities per Incoterm
  - No explicit statement about what's included in "door-to-door" service
- **Chunk search**:
  - Top chunk: sg_export_procedures.md (score: -0.038)
  - Why wrong: Export procedures, not service inclusions
- **Root cause**: **(a) Content missing** - No door-to-door service definition
- **Proposed fix**: Add to `service_terms_conditions.md` Section 2:
  ```
  ### 2.3 Door-to-Door Service Inclusions

  Our door-to-door service includes:
  - Collection from shipper's premises
  - Export customs clearance (origin)
  - Ocean/air freight
  - **Import customs clearance (destination)** - included as standard
  - Delivery to consignee's premises

  Duties and taxes are payable by consignee unless DDP terms agreed.
  ```

---

### Query #37: "Do you handle import permit applications?"

- **Category**: SLA
- **Expected source**: service_terms_conditions.md, sla_policy.md
- **Raw doc search**: FOUND (but buried)
  - Search terms: "import permit", "handle", "application"
  - Found in `sla_policy.md:116`: "Import permit | Same day (if submitted by 2 PM)"
  - This implies we DO handle them, but it's in a processing time table
  - `service_terms_conditions.md:54` lists "Customs Brokerage" including "permits"
- **Chunk search**:
  - Top chunk: sg_export_procedures.md (score: 0.203)
  - Why wrong: Export focus, not import permits
- **Root cause**: **(b) Content buried** - Service exists but not explicitly stated
- **Proposed fix**: Add to `service_terms_conditions.md` Section 2.1:
  ```
  | **Customs Brokerage** | Import/export declaration, **import permit applications**, certificates |

  ### Import Permit Services

  Yes, we handle import permit applications on your behalf. Our customs team
  can apply for TradeNet permits for:
  - Standard import permits
  - Controlled goods permits (with customer's license)
  - Transhipment permits

  Processing: Same day if submitted by 2 PM with complete documents.
  ```

---

## Summary Table

| Query # | Query Text | Root Cause | Fix Type | Target Document |
|---------|------------|------------|----------|-----------------|
| 2 | LCL booking advance time | (a) Missing | Add section | booking_procedure.md |
| 5 | Commercial invoice for samples | (a) Missing | Add section | booking_procedure.md |
| 6 | Bill of Lading definition | (b) Buried | Add definition | booking_procedure.md |
| 7 | Ship without packing list | (b) Buried | Add statement | booking_procedure.md |
| 15 | ATIGA duty rate | (c) Terminology | Add synonyms | atiga_overview.md |
| 19 | Customs ruling application | (a) Missing | Expand section | sg_hs_classification.md |
| 31 | Delivery SLA Singapore | (a) Missing | Add section | sla_policy.md |
| 32 | Customs in door-to-door | (a) Missing | Add section | service_terms_conditions.md |
| 37 | Handle import permits | (b) Buried | Add statement | service_terms_conditions.md |

---

## Recommendations for Task 3

### Priority 1: Documents Needing Content Additions (Multiple Fixes)

1. **booking_procedure.md** - 4 fixes needed:
   - Add recommended booking lead times (#2)
   - Add samples/zero-value guidance (#5)
   - Add B/L definition paragraph (#6)
   - Add mandatory documents statement (#7)

2. **service_terms_conditions.md** - 2 fixes needed:
   - Add door-to-door service inclusions (#32)
   - Add import permit services statement (#37)

### Priority 2: Documents Needing Single Fix

3. **sla_policy.md** - Add delivery SLA section (#31)

4. **atiga_overview.md** - Add "duty rate" terminology (#15)

5. **sg_hs_classification.md** - Expand ruling application process (#19)

### New Synthetic Document Candidates

Consider creating a **Frequently Asked Questions (FAQ)** document to address common queries like:
- Booking lead times
- Document requirements for special cases (samples, gifts)
- Service inclusions (what's in door-to-door)
- Permit handling capabilities

This would provide a centralized, retrieval-friendly location for answers to common customer questions.

---

*Report generated as part of Week 3 Task 1: Root Cause Analysis*
