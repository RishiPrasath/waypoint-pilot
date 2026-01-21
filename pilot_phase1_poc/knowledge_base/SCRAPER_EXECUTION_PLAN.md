# Waypoint Knowledge Base Scraper: Execution Plan

**Approach**: Hybrid (web_fetch + Claude in Chrome) with Section-by-Section Human Review  
**Repository**: `C:\Users\prasa\Documents\Github\waypoint-pilot`  
**Target**: 25-30 documents per blueprint specification

---

## Execution Philosophy

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   SECTION   │────▶│   SCRAPE    │────▶│   HUMAN     │────▶│   NEXT      │
│   START     │     │   + FORMAT  │     │   REVIEW    │     │   SECTION   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │                    │
                          ▼                    ▼
                    Tool Selection:      Approve / Request
                    • web_fetch (static)   Changes / Redo
                    • Browser (dynamic)
```

**Key Principles**:
1. Process one blueprint section at a time
2. Human reviews and approves before moving on
3. **Try web_fetch first** - Quick and lightweight for static content
4. **If web_fetch fails (404, blocked, etc.) → Try Claude in Chrome** as fallback
5. All files saved with required frontmatter format
6. Progress tracked via checklist

**Tool Priority Order**:
```
1. web_fetch                  → Try first (fast, simple static pages)
2. Claude in Chrome (browser) → Fallback if fetch fails (404, JS-heavy, dynamic)
3. Claude in Chrome + Google  → Last resort: Google search to find official source
4. Manual/Synthetic           → For internal docs or when all above fail
```

**404 Recovery Strategy**:
```
When web_fetch returns 404:
  │
  ├─→ Try Claude in Chrome on same URL
  │     │
  │     ├─→ If page loads → Extract content
  │     │
  │     └─→ If still 404 → Navigate to site homepage
  │           │
  │           ├─→ Use site menu/search to find correct page
  │           ├─→ Extract content from discovered URL
  │           └─→ Document the NEW working URL for future reference
  │
  └─→ Update PROGRESS_CHECKLIST.md with findings
```

**Why this works**: Sites restructure URLs but content still exists. Browser can navigate menus, click through sections, and discover where content moved to.

**Google Search Fallback Strategy**:
```
When site navigation fails to find content:
  │
  ├─→ Open Google in browser (google.com)
  │
  ├─→ Search: "[topic] site:[official-domain]" or "[topic] official [country/org]"
  │     │
  │     Examples:
  │     • "import procedures site:customs.gov.sg"
  │     • "ATIGA rules of origin official ASEAN"
  │     • "Indonesia import requirements official"
  │
  ├─→ Read AI Overview for CLUES ONLY (topics, terminology, key concepts)
  │     │
  │     ⚠️ DO NOT use AI Overview as the source!
  │     It's a summary - we need authoritative primary sources.
  │
  ├─→ Scan search results for AUTHORITATIVE sources:
  │     │
  │     Priority order:
  │     1. Official government customs sites (.gov, .go)
  │     2. Official trade ministry sites
  │     3. Recognized trade bodies (WCO, ICC, ASEAN Secretariat)
  │     4. Reputable trade information providers (trade.gov, ITA)
  │     │
  │     For country-specific matters, ALWAYS prefer that country's official source:
  │     • Indonesia → customs.go.id, insw.go.id, kemendag.go.id
  │     • Malaysia → customs.gov.my, miti.gov.my
  │     • Thailand → customs.go.th
  │     • Vietnam → customs.gov.vn
  │     • Philippines → customs.gov.ph, boc.gov.ph
  │
  ├─→ Click on authoritative result and navigate to relevant page
  │
  ├─→ Extract content from the PRIMARY SOURCE
  │
  └─→ Document the actual source URL used
```

**Why this works**: Google AI Overview gives quick orientation, but authoritative content must come from official sources. For regulatory matters, always trace back to the country's own customs/trade authority.

**CRITICAL**: AI Overview is NOT a source. It's a clue. Always click through to and cite the actual authoritative page.

---

## Directory Structure (Created)

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

**Status**: ✅ Directory structure created

---

## Section 1: Singapore Customs (P1) 🏛️

**Tool**: `web_fetch` (government sites are server-rendered HTML)  
**Documents**: 6  
**Est. Time**: 1.5-2 hours  
**Use Cases**: UC-1.1, UC-2.1, UC-2.2, UC-2.3

| # | Document | URL | Filename | Status |
|---|----------|-----|----------|--------|
| 1.1 | Export Procedures | `customs.gov.sg/businesses/exporting-goods/overview` | `sg_export_procedures.md` | ☐ |
| 1.2 | Import Procedures | `customs.gov.sg/businesses/importing-goods/overview` | `sg_import_procedures.md` | ☐ |
| 1.3 | GST Guide | `customs.gov.sg/businesses/valuation-duties-taxes-fees/goods-and-services-tax-gst` | `sg_gst_guide.md` | ☐ |
| 1.4 | Certificates of Origin | `customs.gov.sg/businesses/certificates-of-origin` | `sg_certificates_of_origin.md` | ☐ |
| 1.5 | Free Trade Zones | `customs.gov.sg/businesses/customs-schemes-licences-framework/free-trade-zones` | `sg_free_trade_zones.md` | ☐ |
| 1.6 | HS Classification | `customs.gov.sg/businesses/harmonised-system-hs-classification-of-goods/understanding-hs-classification` | `sg_hs_classification.md` | ☐ |

**Output Directory**: `knowledge_base/01_regulatory/singapore_customs/`

### Frontmatter Template (Section 1)
```yaml
---
title: [Document Title]
source: https://www.customs.gov.sg/[path]
source_type: public_regulatory
last_updated: 2025-01-20
jurisdiction: SG
category: customs
use_cases: [UC-1.1]  # Adjust per document
---
```

### ✋ CHECKPOINT 1
```
□ All 6 Singapore Customs documents created
□ Frontmatter correct and complete
□ Content clean (no navigation/footer/sidebar)
□ Tables and lists preserved
□ Human approved → Proceed to Section 2
```

---

## Section 2: ASEAN Trade Resources (P1-P2) 🌏

**Tool**: `web_fetch` (may need browser for tariff finder interactive elements)  
**Documents**: 3  
**Est. Time**: 1 hour  
**Use Cases**: UC-2.2, UC-2.3

| # | Document | URL | Filename | Tool | Status |
|---|----------|-----|----------|------|--------|
| 2.1 | ASEAN Tariff Finder Guide | `tariff-finder.asean.org` | `asean_tariff_finder_guide.md` | web_fetch / browser | ☐ |
| 2.2 | ATIGA Overview | `asean.org` | `atiga_overview.md` | web_fetch | ☐ |
| 2.3 | Rules of Origin Summary | Extract from tariff finder | `asean_rules_of_origin.md` | browser | ☐ |

**Output Directory**: `knowledge_base/01_regulatory/asean_trade/`

### Special Instructions
- **Tariff Finder**: Document HOW to use the tool, capture sample lookup process
- **ATIGA**: Extract key provisions, preferential rate info
- **RoO**: Focus on 40% Regional Value Content threshold, cumulation rules

### Frontmatter Template (Section 2)
```yaml
---
title: [Document Title]
source: https://[url]
source_type: public_regulatory
last_updated: 2025-01-20
jurisdiction: ASEAN
category: customs
use_cases: [UC-2.2, UC-2.3]
---
```

### ✋ CHECKPOINT 2
```
□ All 3 ASEAN documents created
□ Tariff finder guide includes step-by-step usage
□ RoO thresholds clearly documented
□ Human approved → Proceed to Section 3
```

---

## Section 3: Country-Specific Requirements (P2-P3) 🗺️

**Tool**: `web_fetch` (may need browser for Indonesia INSW)  
**Documents**: 5  
**Est. Time**: 1.5-2 hours  
**Use Cases**: UC-2.4

| # | Document | URL | Filename | Priority | Status |
|---|----------|-----|----------|----------|--------|
| 3.1 | Indonesia Import Reqs | `insw.go.id` | `indonesia_import_requirements.md` | P2 | ☐ |
| 3.2 | Malaysia Import Reqs | `customs.gov.my` | `malaysia_import_requirements.md` | P2 | ☐ |
| 3.3 | Thailand Import Reqs | Thai Customs (English) | `thailand_import_requirements.md` | P3 | ☐ |
| 3.4 | Vietnam Import Reqs | Vietnam Customs | `vietnam_import_requirements.md` | P3 | ☐ |
| 3.5 | Philippines Import Reqs | BOC Portal | `philippines_import_requirements.md` | P3 | ☐ |

**Output Directory**: `knowledge_base/01_regulatory/country_specific/`

### Content Focus (per Blueprint)
Each document should include:
- De minimis threshold
- Key permits required
- Restricted items (LARTAS for Indonesia)
- Certification requirements (SNI, Halal)
- Singapore-relevant info (goods FROM Singapore)

### Frontmatter Template (Section 3)
```yaml
---
title: [Country] Import Requirements
source: https://[url]
source_type: public_regulatory
last_updated: 2025-01-20
jurisdiction: [ID/MY/TH/VN/PH]
category: customs
use_cases: [UC-2.4]
---
```

### ✋ CHECKPOINT 3
```
□ All 5 country documents created (P2 first, then P3)
□ De minimis thresholds clearly stated
□ Key permits listed for each country
□ Human approved → Proceed to Section 4
```

---

## Section 4: Ocean Carriers (P1) 🚢

**Tool**: `Claude in Chrome` (carrier sites are JavaScript-heavy)  
**Documents**: 4  
**Est. Time**: 2-2.5 hours  
**Use Cases**: UC-3.1, UC-3.2, UC-3.3

| # | Document | URL | Filename | Status |
|---|----------|-----|----------|--------|
| 4.1 | PIL Service Summary | `pilship.com` | `pil_service_summary.md` | ☐ |
| 4.2 | Maersk Service Summary | `maersk.com` | `maersk_service_summary.md` | ☐ |
| 4.3 | ONE Service Summary | `one-line.com` | `one_service_summary.md` | ☐ |
| 4.4 | Evergreen Service Summary | `evergreen-line.com` | `evergreen_service_summary.md` | ☐ |

**Output Directory**: `knowledge_base/02_carriers/ocean/`

### Carrier Document Template (per Blueprint)
```markdown
---
title: [Carrier] Service Summary
source: https://www.[carrier].com
source_type: public_carrier
last_updated: 2025-01-20
jurisdiction: Global
category: carrier
use_cases: [UC-3.1, UC-3.2]
---

# [Carrier Name] Service Summary

## Overview
- Headquarters: [City, Country]
- Singapore presence: [Description]
- Primary services: [FCL, LCL, etc.]

## Service Coverage (Singapore Origin)
| Destination | Service Type | Frequency | Transit Time |
|-------------|--------------|-----------|--------------|
| Port Klang | Direct | Weekly | X days |
| Jakarta | Direct/TS | Weekly | X days |
| Ho Chi Minh | Direct | Weekly | X days |

## Documentation Requirements
- Shipping Instructions cutoff: [X days before departure]
- VGM submission: [Method and deadline]
- Bill of Lading options: [Paper, e-BL, Sea Waybill]

## Container Specifications
| Type | Internal Dimensions | Max Payload |
|------|---------------------|-------------|
| 20' Dry | LxWxH | XX,XXX kg |
| 40' Dry | LxWxH | XX,XXX kg |
| 40' HC | LxWxH | XX,XXX kg |

## Contact Information
- Customer Service: [Phone/Email]
- Booking: [Phone/Email]
- Documentation: [Phone/Email]

---
*Source: [Carrier Website]*
*Retrieved: 2025-01-20*
```

### Browser Navigation Strategy
1. Navigate to carrier homepage
2. Find "Services" or "Shipping" section
3. Look for:
   - Route finder / Schedule search
   - Container specifications
   - Documentation / Shipping instructions guide
   - Local information (Singapore)
4. Extract relevant content following template

### ✋ CHECKPOINT 4
```
□ All 4 ocean carrier documents created
□ Each follows carrier template structure
□ Transit times to key SEA ports captured
□ Container specs included
□ Human approved → Proceed to Section 5
```

---

## Section 5: Air Carriers (P2) ✈️

**Tool**: `Claude in Chrome` (corporate sites, JS-heavy)  
**Documents**: 2  
**Est. Time**: 1 hour  
**Use Cases**: UC-3.1

| # | Document | URL | Filename | Status |
|---|----------|-----|----------|--------|
| 5.1 | SIA Cargo Service Guide | `siacargo.com` | `sia_cargo_service_guide.md` | ☐ |
| 5.2 | Cathay Cargo Service Guide | `cathaycargo.com` | `cathay_cargo_service_guide.md` | ☐ |

**Output Directory**: `knowledge_base/02_carriers/air/`

### Content Focus
- Product offerings (general cargo, express, temp-controlled)
- Network coverage from Singapore
- Documentation requirements
- Special cargo handling

### ✋ CHECKPOINT 5
```
□ Both air carrier documents created
□ Product offerings clearly listed
□ Human approved → Proceed to Section 6
```

---

## Section 6: Reference Documents (P1) 📚

**Tool**: `create_file` (synthetic/compiled from public info)  
**Documents**: 3  
**Est. Time**: 1.5 hours  
**Use Cases**: UC-1.3, UC-2.2

| # | Document | Source | Filename | Status |
|---|----------|--------|----------|--------|
| 6.1 | Incoterms 2020 Reference | Compile from ICC public info | `incoterms_2020_reference.md` | ☐ |
| 6.2 | Incoterms Comparison Chart | Create matrix | `incoterms_comparison_chart.md` | ☐ |
| 6.3 | HS Code Structure Guide | Compile from SG Customs | `hs_code_structure_guide.md` | ☐ |

**Output Directories**: 
- `knowledge_base/03_reference/incoterms/`
- `knowledge_base/03_reference/hs_codes/`

### Incoterms Reference Must Include
- All 11 Incoterms 2020 terms
- Definition of each
- Risk transfer point
- Cost responsibility (seller vs buyer)
- Common usage scenarios

### HS Code Guide Must Include
- 6-digit international structure
- AHTN (ASEAN) 8-digit extension
- National 10-digit codes
- How to lookup codes
- When to request a ruling

### ✋ CHECKPOINT 6
```
□ All 3 reference documents created
□ All 11 Incoterms covered with full details
□ HS code structure clearly explained
□ Human approved → Proceed to Section 7
```

---

## Section 7: Synthetic Internal Documents (P1-P3) 📋

**Tool**: `create_file` (templates provided in blueprint)  
**Documents**: 6  
**Est. Time**: 1 hour (mostly copy from blueprint templates)  
**Use Cases**: UC-1.2, UC-4.1, UC-4.2, UC-4.3

| # | Document | Priority | Filename | Status |
|---|----------|----------|----------|--------|
| 7.1 | Service Terms & Conditions | P1 | `service_terms_conditions.md` | ☐ |
| 7.2 | Sea Freight Booking Procedure | P1 | `booking_procedure.md` | ☐ |
| 7.3 | SLA Policy | P2 | `sla_policy.md` | ☐ |
| 7.4 | Escalation Procedure | P2 | `escalation_procedure.md` | ☐ |
| 7.5 | COD Handling Procedure | P3 | `cod_procedure.md` | ☐ |
| 7.6 | FTA Comparison Matrix | P3 | `fta_comparison_matrix.md` | ☐ |

**Output Directories**:
- `knowledge_base/04_internal_synthetic/policies/` (7.1, 7.3)
- `knowledge_base/04_internal_synthetic/procedures/` (7.2, 7.4, 7.5)
- `knowledge_base/04_internal_synthetic/service_guides/` (7.6)

### Frontmatter Template (Section 7)
```yaml
---
title: [Document Title]
source: Internal
source_type: synthetic_internal
last_updated: 2025-01-20
jurisdiction: SG
category: [policy/procedure]
use_cases: [UC-x.x]
---
```

### ✋ CHECKPOINT 7 (FINAL)
```
□ All 6 synthetic documents created
□ Content matches blueprint templates
□ Frontmatter correct
□ Human approved → COMPLETE
```

---

## Execution Summary

| Section | Documents | Tool | Priority | Est. Time |
|---------|-----------|------|----------|-----------|
| 1. Singapore Customs | 6 | web_fetch | P1 | 1.5-2 hrs |
| 2. ASEAN Trade | 3 | web_fetch / browser | P1-P2 | 1 hr |
| 3. Country-Specific | 5 | web_fetch / browser | P2-P3 | 1.5-2 hrs |
| 4. Ocean Carriers | 4 | browser | P1 | 2-2.5 hrs |
| 5. Air Carriers | 2 | browser | P2 | 1 hr |
| 6. Reference Docs | 3 | create_file | P1 | 1.5 hrs |
| 7. Synthetic Docs | 6 | create_file | P1-P3 | 1 hr |
| **TOTAL** | **29** | | | **10-12 hrs** |

---

## Recommended Execution Order

### Session 1: P1 Regulatory (3-4 hours)
1. ✅ Setup directories
2. ☐ Section 1: Singapore Customs (6 docs)
3. ☐ Section 2: ASEAN Trade (3 docs)

### Session 2: P1 Carriers + Reference (3-4 hours)
4. ☐ Section 4: Ocean Carriers (4 docs)
5. ☐ Section 6: Reference Docs (3 docs)
6. ☐ Section 7: Synthetic P1 (2 docs)

### Session 3: P2-P3 Remaining (3-4 hours)
7. ☐ Section 3: Country-Specific (5 docs)
8. ☐ Section 5: Air Carriers (2 docs)
9. ☐ Section 7: Synthetic P2-P3 (4 docs)

---

## Quick Reference: Start Commands

**To begin Section 1:**
```
"Let's start Section 1: Singapore Customs. 
Fetch and process document 1.1 (Export Procedures) 
from customs.gov.sg/businesses/exporting-goods/overview"
```

**To continue after review:**
```
"Section 1 approved. Let's proceed to Section 2: ASEAN Trade Resources."
```

**To retry a failed extraction:**
```
"Document 4.2 (Maersk) didn't capture transit times. 
Use browser to navigate to their schedule/route finder and extract that data."
```

---

## Final Validation Checklist

Before marking knowledge base complete:

```
□ Total document count: 25-30 ✓
□ All P1 documents present (14)
□ All frontmatter follows required format
□ No navigation/footer/sidebar garbage in content
□ Tables preserved and readable
□ Carrier docs follow standard template
□ Synthetic docs match blueprint content
□ Directory structure matches blueprint exactly
```

---

*Plan Version: 1.0*  
*Created: 2025-01-20*  
*Blueprint Reference: 03_knowledge_base_blueprint.md*
