---
title: Sea Freight Booking Procedure
source: Internal
source_type: synthetic_internal
last_updated: 2025-01-21
last_validated: 2025-01-24
validation_method: internal_consistency_check
validation_notes: Complete 10-step workflow; cut-off times align with Singapore port standards
jurisdiction: SG
category: procedure
use_cases: [UC-1.1, UC-1.2, UC-4.2]
document_id: SOP-001
version: 3.0
---

# Sea Freight Booking Procedure

## Document Control

| Attribute | Value |
|-----------|-------|
| **Document ID** | SOP-001 |
| **Version** | 3.0 |
| **Effective Date** | January 1, 2025 |
| **Review Date** | July 1, 2025 |
| **Owner** | Sea Freight Manager |
| **Classification** | Internal Operations |

---

## 1. Purpose

This procedure establishes the standard process for handling sea freight bookings from customer inquiry to cargo departure.

---

## 2. Scope

Applies to all sea freight bookings:
- Full Container Load (FCL)
- Less than Container Load (LCL)
- Breakbulk cargo
- Out-of-gauge (OOG) cargo

---

## 3. Responsibilities

| Role | Responsibilities |
|------|------------------|
| **Customer Service (CS)** | Receive inquiries, provide quotes, confirm bookings |
| **Operations** | Carrier booking, documentation, cargo coordination |
| **Documentation** | B/L preparation, customs declarations |
| **Finance** | Credit checks, invoicing, collections |

---

## 4. Booking Process Overview

```
[1. Inquiry] → [2. Quote] → [3. Confirmation] → [4. Documentation] → [5. Cargo Receipt] → [6. Departure]
     │             │              │                   │                    │                │
   Day -7        Day -5         Day -3              Day -2               Day -1           Day 0
```

---

## 5. Detailed Procedure

### Step 1: Receive Customer Inquiry

**Timeline**: Upon receipt

**Customer Service Actions**:

1. Receive inquiry via email, phone, or portal
2. Log inquiry in booking system
3. Collect required information:

| Required Information | Details |
|---------------------|---------|
| Origin | City, port, or door address |
| Destination | City, port, or door address |
| Cargo description | Commodity, HS code |
| Weight & volume | Gross weight (kg), CBM |
| Container type | 20'/40'/40'HC/RF/OT |
| Incoterm | FOB, CIF, etc. |
| Ready date | Cargo ready date |
| Special requirements | DG, reefer temp, etc. |

4. Verify customer account status (new/existing/credit)

**Output**: Inquiry logged with reference number

---

### Step 2: Prepare and Send Quotation

**Timeline**: Within 4 hours (standard), 24 hours (special cargo)

**Customer Service Actions**:

1. Check carrier rates and space availability
2. Calculate all-in cost:

| Cost Component | Source |
|----------------|--------|
| Ocean freight | Carrier tariff/contract |
| Origin charges | Terminal/trucker rates |
| Documentation | Internal pricing |
| Destination charges | Agent quotes |
| Surcharges | BAF, CAF, PSS, EBS |

3. Apply margin per pricing guidelines
4. Prepare quotation using standard template
5. Send to customer with validity period (7 days)

**Quotation Must Include**:
- All charges (itemized or all-in)
- Transit time
- Carrier and routing
- Validity period
- Terms and conditions

**Output**: Quotation sent to customer

---

### Step 3: Process Booking Confirmation

**Timeline**: Within 2 hours of customer acceptance

**Customer Service Actions**:

1. Receive customer booking confirmation
2. For new customers:
   - Complete KYC verification
   - Request prepayment or credit application
3. For existing customers:
   - Verify credit limit availability
4. Create booking in system with all details
5. Send booking confirmation to customer

**Booking Confirmation Must Include**:

| Field | Description |
|-------|-------------|
| Booking reference | Internal reference number |
| Vessel/voyage | Carrier, vessel name, voyage |
| ETD/ETA | Estimated departure and arrival |
| CY cut-off | Container yard deadline |
| SI cut-off | Shipping instruction deadline |
| Rates confirmed | As per quotation |

**Output**: Booking confirmation issued

---

### Step 4: Book with Carrier

**Timeline**: Same day as customer confirmation

**Operations Actions**:

1. Submit booking request to carrier via:
   - Carrier portal (preferred)
   - EDI transmission
   - Email (backup)

2. Booking request details:

| Field | Source |
|-------|--------|
| Shipper/consignee | Customer SI |
| Cargo description | Booking confirmation |
| Container type/quantity | Customer requirement |
| Requested vessel | Based on customer ETD |
| POL/POD | Booking confirmation |

3. Receive carrier booking confirmation
4. Verify details match customer booking
5. Update system with carrier booking number
6. Arrange empty container pickup (for FCL)

**Output**: Carrier booking confirmed

---

### Step 5: Collect Documentation

**Timeline**: By SI cut-off (typically 3 days before ETD)

**Documentation Team Actions**:

1. Send documentation reminder to customer
2. Collect from customer:

| Document | Requirement |
|----------|-------------|
| Shipping Instructions | Mandatory |
| Commercial Invoice | Mandatory |
| Packing List | Mandatory |
| Export Permit | If applicable |
| Certificate of Origin | If required |
| DG Declaration | For dangerous goods |

3. Verify documents for completeness and accuracy
4. Flag any discrepancies to customer immediately

**Document Verification Checklist**:
- [ ] Shipper/consignee details complete
- [ ] Cargo description matches booking
- [ ] Weight/volume consistent across docs
- [ ] HS code provided and correct format
- [ ] Marks and numbers specified
- [ ] Permit validity (if applicable)

**Output**: Complete documentation set collected

---

### Step 6: Customs Declaration

**Timeline**: 1 day before cargo receipt

**Documentation Team Actions**:

1. Prepare export declaration via TradeNet
2. Key in declaration details:
   - Declarant information
   - Consignment details
   - Cargo particulars
   - Permit type (OUT, various)

3. Submit declaration
4. Receive permit approval
5. Print/save permit for cargo gate-in

**Permit Status Handling**:

| Status | Action |
|--------|--------|
| Approved | Proceed with shipment |
| Pending | Follow up with customs |
| Rejected | Identify issue, re-submit |
| Query | Respond to customs questions |

**Output**: Export permit obtained

---

### Step 7: Cargo Receipt and Container Loading

**Timeline**: By CY cut-off

**Operations Actions**:

**For FCL:**
1. Coordinate container delivery to shipper
2. Shipper loads cargo and seals container
3. Receive container at terminal before cut-off

**For LCL:**
1. Receive cargo at CFS warehouse
2. Verify cargo against packing list
3. Measure and weigh cargo
4. Consolidate with other LCL cargo
5. Load container and seal

**Cargo Receipt Documentation**:
- Equipment interchange receipt
- Container seal number
- Verified gross mass (VGM) declaration
- Damage remarks (if any)

**Output**: Cargo received at terminal/CFS

---

### Step 8: Bill of Lading Preparation

**Timeline**: Before vessel departure

**Documentation Team Actions**:

1. Prepare draft B/L based on shipping instructions
2. Verify all details:

| B/L Field | Verification |
|-----------|--------------|
| Shipper | Matches invoice/permit |
| Consignee | As per SI |
| Notify party | As per SI |
| Port of loading | Booking POL |
| Port of discharge | Booking POD |
| Cargo description | Matches invoice |
| Container/seal | Actual numbers |
| Freight terms | Prepaid/Collect |

3. Send draft B/L to customer for approval
4. Receive customer confirmation
5. Submit final B/L to carrier
6. Receive carrier-approved B/L
7. Issue B/L to customer (as per freight payment)

**B/L Types**:
- Original B/L (3/3): Negotiable
- Telex release: Release at destination
- Seaway bill: Non-negotiable, named consignee

**Output**: Bill of Lading issued

---

### Step 9: Pre-Departure Confirmation

**Timeline**: 1 day before ETD

**Operations Actions**:

1. Verify cargo loaded on planned vessel
2. Obtain load confirmation from terminal
3. Update tracking system
4. Send pre-alert to destination agent
5. Send departure notice to customer

**Pre-Alert Contents**:
- B/L number
- Container/seal numbers
- Vessel/voyage
- ETD/ETA
- B/L copy (if applicable)

**Output**: Shipment confirmed departed

---

### Step 10: Post-Departure

**Timeline**: Within 1 day of departure

**Actions**:

| Team | Action |
|------|--------|
| Operations | Close booking, file documents |
| Finance | Generate invoice |
| Customer Service | Provide tracking link to customer |

**Invoice Contents**:
- All charges as quoted
- Supporting documents attached
- Payment terms stated

**Output**: Invoice issued, file closed

---

## 6. Cut-off Times (Standard Singapore)

| Activity | Standard Cut-off |
|----------|-----------------|
| Shipping Instructions | 3 days before ETD |
| Documentation complete | 2 days before ETD |
| VGM submission | 2 days before ETD |
| FCL CY gate-in | 1 day before ETD |
| LCL cargo receipt | 2 days before ETD |
| Export permit | Before cargo gate-in |

**Note**: Actual cut-offs vary by carrier and terminal. Always verify with carrier booking.

---

## 7. Special Cargo Procedures

### 7.1 Dangerous Goods

Additional requirements:
- DG booking approval (5+ days lead time)
- DG declaration (IMDG format)
- Proper packaging certification
- Container placards
- Segregation verification

### 7.2 Reefer Cargo

Additional requirements:
- Pre-trip inspection (PTI)
- Temperature setting confirmation
- Genset booking (if required)
- Ventilation settings
- Temperature monitoring plan

### 7.3 Out-of-Gauge (OOG)

Additional requirements:
- Detailed dimensions and weight
- Lashing/securing plan
- Flat rack or open top container
- Special handling quotes
- Port/terminal approval

---

## 8. Exception Handling

| Exception | Escalation |
|-----------|------------|
| Space not available | Contact carrier supervisor |
| Rate dispute | Involve pricing team |
| Documentation delay | Notify customer, request extension |
| Permit rejection | Engage customs broker |
| Cargo damage | Initiate claims procedure |
| Missed cut-off | Roll to next vessel, notify customer |

---

## 9. System Entries

All bookings must be entered in the TMS with:
- Complete cargo details
- Accurate rates and charges
- Document links/attachments
- Status updates at each milestone
- Notes for special instructions

---

## 10. Performance Metrics

| KPI | Target |
|-----|--------|
| Quote response time | < 4 hours |
| Booking confirmation | < 2 hours |
| Documentation accuracy | > 99% |
| On-time shipment | > 95% |
| Customer complaints | < 1% of bookings |

---

*Procedure Owner: Sea Freight Manager*
*Next Review: July 1, 2025*
