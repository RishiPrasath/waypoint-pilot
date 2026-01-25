# 03 - Knowledge Base Blueprint

**Document Type**: Knowledge Base Specification  
**Pilot**: Waypoint Phase 1 POC  
**Version**: 1.0

---

## Overview

This document specifies exactly what documents to collect, where to find them, and what synthetic documents to create. Target: **25-30 documents** providing adequate coverage for P1 use cases.

---

## Knowledge Base Structure

```
knowledge_base/
├── 01_regulatory/
│   ├── singapore_customs/
│   ├── asean_trade/
│   └── country_specific/
├── 02_carriers/
│   ├── ocean/
│   └── air/
├── 03_reference/
│   ├── incoterms/
│   └── hs_codes/
└── 04_internal_synthetic/
    ├── policies/
    ├── procedures/
    └── service_guides/
```

---

## Part A: Public Regulatory Documents

### A1. Singapore Customs (Primary Source)

| Document | URL | Use Cases | Priority |
|----------|-----|-----------|----------|
| **Export Procedures Guide** | [customs.gov.sg/businesses/exporting-goods/overview](https://www.customs.gov.sg/businesses/exporting-goods/overview) | UC-1.1 | P1 |
| **Import Procedures Guide** | [customs.gov.sg/businesses/importing-goods/overview](https://www.customs.gov.sg/businesses/importing-goods/overview) | UC-2.1 | P1 |
| **GST Guide for Imports** | [customs.gov.sg/businesses/valuation-duties-taxes-fees/goods-and-services-tax-gst](https://www.customs.gov.sg/businesses/valuation-duties-taxes-fees/goods-and-services-tax-gst) | UC-2.1 | P1 |
| **Certificates of Origin Guide** | [customs.gov.sg/businesses/certificates-of-origin](https://www.customs.gov.sg/businesses/certificates-of-origin) | UC-2.3 | P1 |
| **Free Trade Zone Procedures** | [customs.gov.sg/businesses/exporting-goods/export-procedures/exporting-trade-samples](https://www.customs.gov.sg/businesses/customs-schemes-licences-framework/free-trade-zones) | UC-2.1 | P1 |
| **HS Classification Guide** | [customs.gov.sg/businesses/harmonised-system-classification-of-goods](https://www.customs.gov.sg/businesses/harmonised-system-hs-classification-of-goods/understanding-hs-classification) | UC-2.2 | P1 |

**Collection Method**: 
1. Visit each URL
2. Copy main content (exclude navigation/footers)
3. Save as markdown with source attribution
4. Note last updated date

---

### A2. ASEAN Trade Resources

| Document | URL | Use Cases | Priority |
|----------|-----|-----------|----------|
| **ASEAN Tariff Finder** | [tariff-finder.asean.org](https://tariff-finder.asean.org/) | UC-2.2, UC-2.3 | P1 |
| **ATIGA Overview** | [asean.org/asean-economic-community/asean-free-trade-area-afta-council](https://asean.org/) | UC-2.3 | P2 |
| **Rules of Origin Guide** | Extract from tariff finder | UC-2.3 | P2 |

**Collection Method**:
1. ASEAN Tariff Finder: Document the lookup process, capture sample outputs
2. Create summary document of ATIGA key provisions
3. Extract RoO thresholds for common product categories

---

### A3. Country-Specific Import Requirements

| Country | Source | Focus Areas | Priority |
|---------|--------|-------------|----------|
| **Indonesia** | [insw.go.id](https://www.insw.go.id/) | LARTAS, SNI, Halal | P2 |
| **Malaysia** | [customs.gov.my](https://www.customs.gov.my/) | De minimis, permits | P2 |
| **Thailand** | Thai Customs (English) | BOI, import procedures | P3 |
| **Vietnam** | Vietnam Customs | E-commerce rules | P3 |
| **Philippines** | BOC Portal | De minimis, permits | P3 |

**Collection Method**:
1. Focus on Singapore-relevant import requirements (goods FROM Singapore)
2. Create summary sheets per country (1-2 pages each)
3. Include de minimis thresholds, key permits, restricted items

---

## Part B: Public Carrier Documents

### B1. Ocean Carriers

#### PIL (Pacific International Lines)

| Document | Source | Content Focus |
|----------|--------|---------------|
| Service Network Map | [pilship.com](https://www.pilship.com/) | Port coverage, routes |
| Container Specifications | PIL website | Container types, dimensions |
| Documentation Guide | PIL website or request | SI requirements, VGM |

**Note**: PIL is Singapore-headquartered; likely best documentation access.

#### Maersk

| Document | Source | Content Focus |
|----------|--------|---------------|
| Intra-Asia Services | [maersk.com](https://www.maersk.com/) | Schedules, transit times |
| Shipping Instructions Guide | Maersk.com customer resources | Documentation procedures |
| VGM Requirements | Maersk.com | SOLAS compliance |
| Local Charges Reference | Maersk.com | Surcharges, fees |

**Note**: Maersk has excellent public documentation.

#### ONE (Ocean Network Express)

| Document | Source | Content Focus |
|----------|--------|---------------|
| Service Portfolio | [one-line.com](https://www.one-line.com/) | Network coverage |
| E-commerce Tools Guide | ONE website | Booking, tracking |
| Container Specifications | ONE website | Equipment |

#### Evergreen

| Document | Source | Content Focus |
|----------|--------|---------------|
| Service Routes | [evergreen-line.com](https://www.evergreen-line.com/) | Asia network |
| Shipping Guide | Evergreen website | Procedures |

### B2. Air Carriers

| Carrier | Document | Source |
|---------|----------|--------|
| **Singapore Airlines Cargo** | Product Guide | [siacargo.com](https://www.siacargo.com/) |
| **Cathay Cargo** | Service Guide | [cathaycargo.com](https://www.cathaycargo.com/) |

---

### B3. Carrier Document Template

For each carrier, create a standardized summary:

```markdown
# [Carrier Name] Service Summary

## Overview
- Headquarters: 
- Singapore presence:
- Primary services:

## Service Coverage (Singapore Origin)
| Destination | Service Type | Frequency | Transit Time |
|-------------|--------------|-----------|--------------|
| [Port] | [Direct/TS] | [Weekly] | [X days] |

## Documentation Requirements
- Shipping Instructions cutoff: 
- VGM submission:
- Bill of Lading options:

## Container Specifications
| Type | Dimensions | Max Payload |
|------|------------|-------------|
| 20ft | | |
| 40ft | | |

## Contact Information
- Customer Service:
- Booking:
- Documentation:

## Sources
- [Link to carrier website]
- Last updated: [Date]
```

---

## Part C: Reference Documents

### C1. Incoterms 2020

| Document | Content | Source |
|----------|---------|--------|
| Incoterms 2020 Quick Reference | All 11 terms summarized | ICC summary (public) or create synthetic |
| Incoterms Comparison Chart | Responsibility matrix | Create from public info |

**Synthetic Creation**:
Create a comprehensive Incoterms reference covering:
- Each term's definition
- Risk transfer point
- Cost responsibility matrix
- Common usage scenarios

### C2. HS Code Reference

| Document | Content | Source |
|----------|---------|--------|
| HS Code Structure Explainer | How codes work | Singapore Customs + create |
| Common HS Codes for Electronics | Sample classifications | Tariff finder examples |
| HS Lookup Process Guide | Step-by-step | Create from Customs guidance |

---

## Part D: Synthetic Internal Documents

These simulate a 3PL's internal documentation. Create realistic but generic versions.

### D1. Company Policies

#### D1.1 Service Terms & Conditions (P1)

```markdown
# [Company] Freight Forwarding Service Terms

## 1. Service Scope

### 1.1 Sea Freight Services
- Full Container Load (FCL)
- Less than Container Load (LCL)
- Door-to-door and Port-to-port options

### 1.2 Air Freight Services
- General cargo
- Express services
- Temperature-controlled (subject to carrier availability)

### 1.3 Customs Brokerage
- Import/export declaration
- Permit applications (additional fees apply)
- Duty/tax calculation and payment

## 2. Standard Inclusions & Exclusions

### Included in Standard Service:
- Cargo pickup/delivery (door services)
- Export/import customs clearance
- Ocean/air freight
- Standard documentation

### Not Included (Available as Add-ons):
- Cargo insurance
- Warehousing beyond free time
- Special permits/licenses
- Duties, taxes, and government fees

## 3. Documentation Requirements

### Customer Must Provide:
- Commercial Invoice (3 copies)
- Packing List
- Additional documents based on cargo/destination

### We Provide:
- Bill of Lading / Airway Bill
- Arrival Notice
- Delivery Order

## 4. Liability

Standard liability as per:
- Ocean: Hague-Visby Rules
- Air: Montreal Convention
- Road: CMR Convention

Recommended: Customers should arrange cargo insurance.

## 5. Payment Terms

- Payment due within 30 days of invoice
- Duties/taxes: Advance payment required
- COD available for approved customers

---
*Document: SVC-TERMS-001*
*Version: 2.3*
*Effective: January 2024*
```

#### D1.2 SLA Policy Document (P2)

```markdown
# [Company] Service Level Commitments

## Transit Time Standards

### Sea Freight (from Singapore)
| Destination | FCL Target | LCL Target |
|-------------|------------|------------|
| Port Klang | 2-3 days | 5-7 days |
| Jakarta | 4-5 days | 7-10 days |
| Ho Chi Minh | 3-4 days | 6-8 days |
| Manila | 5-6 days | 8-12 days |
| Bangkok | 4-5 days | 7-10 days |

*Note: Transit times are port-to-port, excluding customs clearance*

### Documentation Processing
| Service | Target |
|---------|--------|
| Quotation response | Within 4 business hours |
| Booking confirmation | Within 24 hours |
| BL draft | Within 48 hours of sailing |
| Arrival notice | 2 days before ETA |

## SLA Exclusions

The following are excluded from SLA calculations:
- Customs delays or inspections
- Weather/force majeure events
- Carrier schedule changes
- Customer documentation delays
- Port congestion

## Service Credits

For SLA breaches within our control:
- Minor breach (1-2 days): 5% credit on freight
- Major breach (3+ days): 10% credit on freight
- Subject to formal claim submission

---
*Document: SLA-POL-001*
*Version: 1.2*
*Effective: January 2024*
```

### D2. Operational Procedures

#### D2.1 Booking Procedure (P1)

```markdown
# Sea Freight Booking Procedure

## 1. Booking Request

### Information Required:
- Shipper/consignee details
- Cargo description and HS code
- Weight and dimensions
- Pickup/delivery addresses
- Cargo ready date
- Preferred sailing/carrier (if any)
- Incoterms

### Booking Channels:
- Email: bookings@[company].com
- Online portal: [portal URL]
- Phone: [number] (urgent only)

## 2. Booking Confirmation

Upon receiving request:
1. Check space availability with carriers
2. Confirm rates and charges
3. Issue booking confirmation with:
   - Booking reference number
   - Confirmed sailing schedule
   - Documentation requirements
   - Cutoff dates

## 3. Documentation Cutoffs

### FCL:
- SI cutoff: 3 days before vessel departure
- VGM cutoff: 2 days before vessel departure
- Cargo cutoff: 1 day before vessel departure

### LCL:
- SI cutoff: 5 days before consolidation
- Cargo delivery to CFS: 3 days before consolidation

## 4. Booking Amendments

Amendments accepted subject to:
- Space availability
- Timing (before cutoff)
- Amendment fees may apply

To amend: Contact booking team with original booking reference.

---
*Document: PROC-BKG-001*
*Version: 2.1*
```

#### D2.2 COD Handling Procedure (P3)

```markdown
# Cash on Delivery (COD) Procedure

## 1. COD Service Overview

COD allows consignee to pay for goods upon delivery.

### Eligibility:
- Available for approved shippers only
- Maximum COD amount: SGD 5,000 per shipment
- Available for Singapore deliveries only

## 2. COD Process

### Collection:
1. Driver collects cash/cheque upon delivery
2. Delivery confirmed only after payment received
3. Driver issues receipt to consignee

### Reconciliation:
1. Daily collection reconciliation at depot
2. Discrepancies investigated within 24 hours
3. Collections banked next business day

### Remittance:
1. COD funds remitted to shipper account
2. Standard cycle: 5 business days from delivery
3. Express cycle (T+2): Available for fee

## 3. Failed COD Deliveries

If consignee refuses/unable to pay:
1. Shipment returned to depot
2. Shipper notified within 24 hours
3. Options: Re-deliver, return to shipper, hold at depot
4. Storage fees apply after 3 days

## 4. Fees

| Service | Fee |
|---------|-----|
| COD handling | 2% of collection (min SGD 5) |
| Express remittance | SGD 15 per transaction |
| Return to shipper | At cost |

---
*Document: PROC-COD-001*
*Version: 1.0*
```

#### D2.3 Escalation Procedure (P2)

```markdown
# Customer Service Escalation Procedure

## 1. Escalation Levels

### Level 1: Customer Service Agent
- First point of contact
- Handle: Standard queries, status updates, documentation requests
- Resolution target: Same day

### Level 2: Team Lead / Supervisor
- Escalate when: Complex queries, customer complaints, SLA breaches
- Resolution target: 24 hours

### Level 3: Operations Manager
- Escalate when: Service recovery required, significant claims, VIP customers
- Resolution target: 48 hours

### Level 4: Management
- Escalate when: Legal issues, major service failures, contract disputes
- Resolution target: Case-dependent

## 2. When to Escalate

Immediately escalate if:
- Customer explicitly requests supervisor
- Shipment delayed >3 days with no resolution
- Cargo damage/loss reported
- Compliance/regulatory issue identified
- Customer threatens legal action

## 3. Escalation Process

1. Document all details in ticket system
2. Notify next level via email + call for urgent
3. Handover all context and history
4. Follow up until resolved
5. Log resolution for knowledge base

---
*Document: PROC-ESC-001*
*Version: 1.1*
```

---

## Document Collection Checklist

### Week 1 Target: Core Documents (15)

| # | Document | Type | Source | Status |
|---|----------|------|--------|--------|
| 1 | SG Customs Export Guide | Public | customs.gov.sg | ☐ |
| 2 | SG Customs Import Guide | Public | customs.gov.sg | ☐ |
| 3 | SG Customs GST Guide | Public | customs.gov.sg | ☐ |
| 4 | SG Customs CO Guide | Public | customs.gov.sg | ☐ |
| 5 | SG Customs HS Guide | Public | customs.gov.sg | ☐ |
| 6 | FTZ Procedures | Public | customs.gov.sg | ☐ |
| 7 | Incoterms Reference | Synthetic | Create | ☐ |
| 8 | PIL Service Summary | Public | pilship.com | ☐ |
| 9 | Maersk Service Summary | Public | maersk.com | ☐ |
| 10 | Service Terms & Conditions | Synthetic | Create | ☐ |
| 11 | Booking Procedure | Synthetic | Create | ☐ |
| 12 | SLA Policy | Synthetic | Create | ☐ |
| 13 | ASEAN Tariff Finder Guide | Public | tariff-finder | ☐ |
| 14 | ONE Service Summary | Public | one-line.com | ☐ |
| 15 | Evergreen Service Summary | Public | evergreen-line | ☐ |

### Week 2 Target: Secondary Documents (10)

| # | Document | Type | Source | Status |
|---|----------|------|--------|--------|
| 16 | Indonesia Import Requirements | Public | INSW | ☐ |
| 17 | Malaysia Import Summary | Public | customs.gov.my | ☐ |
| 18 | ATIGA Rules of Origin | Public | ASEAN | ☐ |
| 19 | Carrier VGM Procedures | Public | Carrier sites | ☐ |
| 20 | Container Specifications | Public | Carrier sites | ☐ |
| 21 | Escalation Procedure | Synthetic | Create | ☐ |
| 22 | COD Procedure | Synthetic | Create | ☐ |
| 23 | Regional De Minimis Reference | Public | Multiple | ☐ |
| 24 | Air Cargo Service Guide | Public | SIA Cargo | ☐ |
| 25 | FTA Comparison Matrix | Synthetic | Create | ☐ |

---

## Document Processing Guidelines

### Format Standardization

All documents should be processed into this format:

```markdown
---
title: [Document Title]
source: [URL or "Internal"]
source_type: [public_regulatory | public_carrier | synthetic_internal]
last_updated: [YYYY-MM-DD]
jurisdiction: [SG | MY | ID | TH | VN | PH | ASEAN | Global]
category: [customs | carrier | policy | procedure | reference]
use_cases: [UC-1.1, UC-2.3, etc.]
---

# [Document Title]

[Content here]

---
*Source: [Full attribution]*
*Retrieved/Created: [Date]*
```

### Chunking Guidelines

For RAG ingestion:
- **Regulatory docs**: Chunk by section headers (512-1024 tokens)
- **Carrier docs**: Chunk by topic (256-512 tokens)
- **Procedures**: Chunk by step/section (256-512 tokens)
- **Reference tables**: Keep tables intact as single chunks
- **Overlap**: 15% overlap between chunks for context

### Metadata Requirements

Each chunk must retain:
- Document title
- Section header
- Source URL/reference
- Last updated date
- Category tags

---

*Next Document*: [04 - Technical Architecture](./04_technical_architecture.md)
