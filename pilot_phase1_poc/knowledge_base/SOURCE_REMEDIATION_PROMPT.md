# Knowledge Base Source Attribution Remediation

**Purpose**: Update all knowledge base documents to use enhanced frontmatter schema with specific, citable source URLs  
**Impact**: Enables RAG system to provide accurate citations for compliance and user trust  
**Documents Requiring Update**: 9 of 29 documents

---

## Enhanced Frontmatter Schema

### New Schema Structure

All documents should follow this enhanced frontmatter format:

```yaml
---
title: [Document Title]
source_organization: [Organization/Authority Name]
source_urls:
  - url: [Primary source URL - specific page, not root domain]
    description: [What this page contains]
    retrieved_date: [YYYY-MM-DD when content was accessed]
  - url: [Additional source URL if applicable]
    description: [What this page contains]
    retrieved_date: [YYYY-MM-DD]
source_type: [public_regulatory | public_carrier | synthetic_internal]
last_updated: [YYYY-MM-DD]
jurisdiction: [SG | MY | TH | VN | ID | PH | ASEAN | Global]
category: [customs | carrier | reference | policy | procedure]
use_cases: [UC-X.X, UC-X.X]
---
```

### Key Differences from Old Schema

| Field | Old Schema | New Schema |
|-------|------------|------------|
| `source` | Single field (URL or org name) | Split into `source_organization` + `source_urls` |
| URL specificity | Often root domain only | **Must be specific page URL** |
| Multiple sources | Not supported | Array of URLs with descriptions |
| Retrieval tracking | Not tracked | `retrieved_date` per URL |

---

## Remediation Checklist

### Category A: Carrier Documents (Root Domain → Specific Pages)

These documents have root domain URLs only. Each needs specific page URLs for the content referenced.


#### A1. PIL Service Summary
**File**: `02_carriers/ocean/pil_service_summary.md`  
**Current Source**: `https://www.pilship.com`  
**Status**: ⏳ Needs specific URLs

| Content Section | URL to Find | Search Strategy |
|-----------------|-------------|-----------------|
| Company overview, fleet info | About Us / Company Profile page | Navigate: pilship.com → About Us |
| Service routes from Singapore | Services / Trade Routes page | Navigate: pilship.com → Services → Trade Routes |
| Container specifications | Equipment / Container Types page | Navigate: pilship.com → Services → Equipment |
| Digital tools (PocketPIL) | eServices / Digital Solutions page | Navigate: pilship.com → eServices |
| Contact/office info | Contact Us / Singapore office page | Navigate: pilship.com → Contact |

**Target Frontmatter**:
```yaml
source_organization: Pacific International Lines (Pte) Ltd
source_urls:
  - url: https://www.pilship.com/en-pil-pacific-international-lines-about-us/about-us/
    description: Company overview and history
    retrieved_date: 2025-01-XX
  - url: https://www.pilship.com/en-pil-pacific-international-lines-services/services/
    description: Service routes and coverage
    retrieved_date: 2025-01-XX
```

---

#### A2. Maersk Service Summary
**File**: `02_carriers/ocean/maersk_service_summary.md`  
**Current Source**: `https://www.maersk.com`  
**Status**: ⏳ Needs specific URLs

| Content Section | URL to Find | Search Strategy |
|-----------------|-------------|-----------------|
| Singapore local presence | Local Singapore page | Navigate: maersk.com → Local Information → Singapore |
| Service routes | Schedules / Point-to-Point | Navigate: maersk.com → Schedules |
| Digital solutions (Maersk.com portal) | Digital Solutions page | Navigate: maersk.com → Solutions → Digital |
| Special cargo services | Products page | Navigate: maersk.com → Products |
| Contact Singapore office | Contact / Singapore | Navigate: maersk.com → Contact → Singapore |

**Target Frontmatter**:
```yaml
source_organization: A.P. Moller - Maersk
source_urls:
  - url: https://www.maersk.com/local-information/asia-pacific/singapore
    description: Singapore local operations and services
    retrieved_date: 2025-01-XX
  - url: https://www.maersk.com/schedules
    description: Route schedules and port coverage
    retrieved_date: 2025-01-XX
```

---

#### A3. ONE (Ocean Network Express) Service Summary
**File**: `02_carriers/ocean/one_service_summary.md`  
**Current Source**: `https://sg.one-line.com`  
**Status**: ⏳ Needs specific URLs

| Content Section | URL to Find | Search Strategy |
|-----------------|-------------|-----------------|
| Company overview | About ONE page | Navigate: one-line.com → About ONE |
| Singapore entity info | Singapore local site | Use: sg.one-line.com → About |
| Service routes | Services / Network page | Navigate: one-line.com → Services |
| Container equipment | Equipment page | Navigate: one-line.com → Services → Equipment |
| eCommerce tools | eCommerce / Digital page | Navigate: one-line.com → eCommerce |

**Target Frontmatter**:
```yaml
source_organization: Ocean Network Express Pte. Ltd.
source_urls:
  - url: https://sg.one-line.com/about
    description: Singapore entity information
    retrieved_date: 2025-01-XX
  - url: https://www.one-line.com/en/services
    description: Global service network
    retrieved_date: 2025-01-XX
```

---

#### A4. Evergreen Service Summary
**File**: `02_carriers/ocean/evergreen_service_summary.md`  
**Current Source**: `https://www.evergreen-marine.com.sg`  
**Status**: ⏳ Needs specific URLs

| Content Section | URL to Find | Search Strategy |
|-----------------|-------------|-----------------|
| Singapore entity info | About EMS page | Navigate: evergreen-marine.com.sg → About |
| Service routes | Services / Shipping Routes | Navigate: evergreen-marine.com.sg → Services |
| Container types | Container Information page | Navigate: evergreen-marine.com.sg → Services → Container |
| ShipmentLink portal | eService / ShipmentLink | Navigate: evergreen-marine.com.sg → eService |
| Ocean Alliance info | Global site network page | Navigate: evergreen-line.com → Network |

**Target Frontmatter**:
```yaml
source_organization: Evergreen Marine (Singapore) Pte. Ltd.
source_urls:
  - url: https://www.evergreen-marine.com.sg/tei1/jsp/TEI1_About.jsp
    description: Singapore entity information
    retrieved_date: 2025-01-XX
  - url: https://www.evergreen-line.com/services
    description: Global service network and routes
    retrieved_date: 2025-01-XX
```

---

#### A5. SIA Cargo Service Guide
**File**: `02_carriers/air/sia_cargo_service_guide.md`  
**Current Source**: `https://www.siacargo.com`  
**Status**: ⏳ Needs specific URLs

| Content Section | URL to Find | Search Strategy |
|-----------------|-------------|-----------------|
| Company overview | About SIA Cargo page | Navigate: siacargo.com → About Us |
| THRUCOOL/THRUFRESH products | Products / Solutions page | Navigate: siacargo.com → Products |
| Dangerous goods handling | Special Cargo / DG page | Navigate: siacargo.com → Products → Dangerous Goods |
| Network coverage | Network / Destinations page | Navigate: siacargo.com → Network |
| Booking tools | eServices page | Navigate: siacargo.com → eServices |

**Target Frontmatter**:
```yaml
source_organization: Singapore Airlines Cargo
source_urls:
  - url: https://www.siacargo.com/about-us.html
    description: Company overview and history
    retrieved_date: 2025-01-XX
  - url: https://www.siacargo.com/products.html
    description: Cargo products including THRUCOOL, THRUFRESH
    retrieved_date: 2025-01-XX
```

---

#### A6. Cathay Cargo Service Guide
**File**: `02_carriers/air/cathay_cargo_service_guide.md`  
**Current Source**: `https://www.cathaycargo.com`  
**Status**: ⏳ Needs specific URLs

| Content Section | URL to Find | Search Strategy |
|-----------------|-------------|-----------------|
| Company overview | About Cathay Cargo page | Navigate: cathaycargo.com → About Us |
| Product portfolio (12+ products) | Our Solutions page | Navigate: cathaycargo.com → Our Solutions |
| CEIV certifications | Certifications / Quality page | Navigate: cathaycargo.com → About → Certifications |
| Network/destinations | Network page | Navigate: cathaycargo.com → Network |
| Booking portal | Book Now / Click & Ship | Navigate: cathaycargo.com → Book |

**Target Frontmatter**:
```yaml
source_organization: Cathay Cargo (Cathay Pacific Airways Limited)
source_urls:
  - url: https://www.cathaycargo.com/en-us/about-us/
    description: Company overview and certifications
    retrieved_date: 2025-01-XX
  - url: https://www.cathaycargo.com/en-us/our-solutions/
    description: Product portfolio and specialized services
    retrieved_date: 2025-01-XX
```

---

### Category B: Reference Documents (Organization Name → Specific URLs)

These documents cite organization names but lack clickable URLs.


#### B1. Incoterms 2020 Reference Guide
**File**: `03_reference/incoterms/incoterms_2020_reference.md`  
**Current Source**: `International Chamber of Commerce (ICC)`  
**Status**: ⏳ Needs URL

| Content Section | URL to Find | Search Strategy |
|-----------------|-------------|-----------------|
| Official Incoterms 2020 rules | ICC Incoterms page | Navigate: iccwbo.org → Knowledge → Incoterms |
| Rule definitions | ICC Knowledge Solutions | Search: "Incoterms 2020 site:iccwbo.org" |
| Official ICC guidance | ICC Store / Publications | Navigate: iccwbo.org → Store → Incoterms |

**Target Frontmatter**:
```yaml
source_organization: International Chamber of Commerce (ICC)
source_urls:
  - url: https://iccwbo.org/business-solutions/incoterms-rules/incoterms-2020/
    description: Official ICC Incoterms 2020 overview
    retrieved_date: 2025-01-XX
  - url: https://iccwbo.org/news-publications/policies-reports/incoterms-2020-introduction/
    description: ICC introduction to Incoterms 2020 rules
    retrieved_date: 2025-01-XX
```

**Note**: ICC official detailed rules are behind paywall. Use free overview pages for citation.

---

#### B2. Incoterms Comparison Chart
**File**: `03_reference/incoterms/incoterms_comparison_chart.md`  
**Current Source**: `International Chamber of Commerce (ICC)`  
**Status**: ⏳ Needs URL

| Content Section | URL to Find | Search Strategy |
|-----------------|-------------|-----------------|
| Term comparisons | ICC Incoterms resources | Same as B1 |
| Visual charts | ICC or trade.gov resources | Search: "Incoterms chart comparison" |

**Target Frontmatter**:
```yaml
source_organization: International Chamber of Commerce (ICC)
source_urls:
  - url: https://iccwbo.org/business-solutions/incoterms-rules/incoterms-2020/
    description: Official ICC Incoterms 2020 reference
    retrieved_date: 2025-01-XX
```

---

#### B3. HS Code Structure Guide
**File**: `03_reference/hs_codes/hs_code_structure_guide.md`  
**Current Source**: `World Customs Organization (WCO)`  
**Status**: ⏳ Needs URL

| Content Section | URL to Find | Search Strategy |
|-----------------|-------------|-----------------|
| HS structure explanation | WCO Nomenclature page | Navigate: wcoomd.org → Topics → Nomenclature |
| HS code system overview | WCO HS Convention page | Navigate: wcoomd.org → Topics → HS Convention |
| AHTN (ASEAN extension) | ASEAN Secretariat | Search: "AHTN 2022 site:asean.org" |

**Target Frontmatter**:
```yaml
source_organization: World Customs Organization (WCO)
source_urls:
  - url: https://www.wcoomd.org/en/topics/nomenclature/overview.aspx
    description: WCO Harmonized System overview
    retrieved_date: 2025-01-XX
  - url: https://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs-nomenclature-2022-edition.aspx
    description: HS Nomenclature 2022 edition
    retrieved_date: 2025-01-XX
```

---

### Category C: Documents Already Compliant ✅

These documents already have specific page URLs and only need minor schema updates.

| # | File | Current Source | Action |
|---|------|----------------|--------|
| C1 | `sg_import_procedures.md` | `https://www.customs.gov.sg/businesses/importing-goods/overview` | ✅ Add `source_organization` field |
| C2 | `sg_export_procedures.md` | Specific customs.gov.sg URL | ✅ Add `source_organization` field |
| C3 | `sg_gst_guide.md` | Specific customs.gov.sg URL | ✅ Add `source_organization` field |
| C4 | `sg_certificates_of_origin.md` | Specific customs.gov.sg URL | ✅ Add `source_organization` field |
| C5 | `sg_free_trade_zones.md` | Specific customs.gov.sg URL | ✅ Add `source_organization` field |
| C6 | `sg_hs_classification.md` | Specific customs.gov.sg URL | ✅ Add `source_organization` field |
| C7 | `indonesia_import_requirements.md` | Specific trade.gov URL + `official_sources` | ✅ Rename `official_sources` → `source_urls` |
| C8 | `malaysia_import_requirements.md` | Specific trade.gov URL | ✅ Add `source_organization` field |
| C9 | `thailand_import_requirements.md` | Specific trade.gov URL | ✅ Add `source_organization` field |
| C10 | `vietnam_import_requirements.md` | Specific trade.gov URL | ✅ Add `source_organization` field |
| C11 | `philippines_import_requirements.md` | Specific trade.gov URL | ✅ Add `source_organization` field |
| C12 | `asean_tariff_finder_guide.md` | Specific asean.org URL | ✅ Add `source_organization` field |
| C13 | `atiga_overview.md` | Specific asean.org URL | ✅ Add `source_organization` field |
| C14 | `asean_rules_of_origin.md` | Specific asean.org URL | ✅ Add `source_organization` field |

---

### Category D: Internal/Synthetic Documents ✅

These documents are internally created and do not require external source URLs.

| # | File | Current Source | Action |
|---|------|----------------|--------|
| D1 | `service_terms_conditions.md` | `Internal` | ✅ No change needed |
| D2 | `sla_policy.md` | `Internal` | ✅ No change needed |
| D3 | `booking_procedure.md` | `Internal` | ✅ No change needed |
| D4 | `escalation_procedure.md` | `Internal` | ✅ No change needed |
| D5 | `cod_procedure.md` | `Internal` | ✅ No change needed |
| D6 | `fta_comparison_matrix.md` | `Internal` | ✅ No change needed |

**Schema for Internal Documents**:
```yaml
source_organization: [Company Name] - Internal
source_urls: []  # Empty array for internal docs
source_type: synthetic_internal
```

---

## Execution Instructions

### Phase 1: Category A - Carrier Documents (Priority: HIGH)

**Why High Priority**: Carrier information is frequently queried (UC-3.x use cases) and agents need to verify service claims.

**Execution Steps**:

```
For each carrier document (A1-A6):

1. OPEN BROWSER to carrier website root domain

2. NAVIGATE to find specific pages for:
   - Company/About page
   - Services/Routes page  
   - Singapore-specific page (if exists)
   - Digital tools/eServices page

3. RECORD the exact URLs found

4. UPDATE the document frontmatter:
   - Add source_organization field
   - Convert source to source_urls array
   - Add retrieved_date for each URL
   - Keep all other frontmatter fields

5. VERIFY content still matches sources
   - If content has changed, update document body
   - Note any discrepancies in commit message

6. MARK complete in checklist below
```


### Phase 2: Category B - Reference Documents (Priority: MEDIUM)

**Why Medium Priority**: Reference documents (Incoterms, HS codes) are foundational but less frequently updated.

**Execution Steps**:

```
For each reference document (B1-B3):

1. SEARCH for official source pages:
   - ICC website for Incoterms
   - WCO website for HS codes
   - ASEAN website for AHTN

2. NAVIGATE to authoritative pages (avoid paid/gated content)

3. RECORD the exact URLs found

4. UPDATE the document frontmatter with new schema

5. MARK complete in checklist below
```

### Phase 3: Category C - Schema Alignment (Priority: LOW)

**Why Low Priority**: These documents already have good URLs; just need schema consistency.

**Execution Steps**:

```
For each compliant document (C1-C14):

1. ADD source_organization field based on existing source URL

2. CONVERT source field to source_urls array format

3. ADD retrieved_date field (use last_updated date or current date)

4. VERIFY no content changes needed

5. MARK complete in checklist below
```

---

## Execution Tracking Checklist

### Category A: Carrier Documents

| Doc | File | URLs Found | Updated | Verified |
|-----|------|------------|---------|----------|
| A1 | `pil_service_summary.md` | ⬜ | ⬜ | ⬜ |
| A2 | `maersk_service_summary.md` | ⬜ | ⬜ | ⬜ |
| A3 | `one_service_summary.md` | ⬜ | ⬜ | ⬜ |
| A4 | `evergreen_service_summary.md` | ⬜ | ⬜ | ⬜ |
| A5 | `sia_cargo_service_guide.md` | ⬜ | ⬜ | ⬜ |
| A6 | `cathay_cargo_service_guide.md` | ⬜ | ⬜ | ⬜ |

### Category B: Reference Documents

| Doc | File | URLs Found | Updated | Verified |
|-----|------|------------|---------|----------|
| B1 | `incoterms_2020_reference.md` | ⬜ | ⬜ | ⬜ |
| B2 | `incoterms_comparison_chart.md` | ⬜ | ⬜ | ⬜ |
| B3 | `hs_code_structure_guide.md` | ⬜ | ⬜ | ⬜ |

### Category C: Schema Alignment

| Doc | File | Updated | Verified |
|-----|------|---------|----------|
| C1 | `sg_import_procedures.md` | ⬜ | ⬜ |
| C2 | `sg_export_procedures.md` | ⬜ | ⬜ |
| C3 | `sg_gst_guide.md` | ⬜ | ⬜ |
| C4 | `sg_certificates_of_origin.md` | ⬜ | ⬜ |
| C5 | `sg_free_trade_zones.md` | ⬜ | ⬜ |
| C6 | `sg_hs_classification.md` | ⬜ | ⬜ |
| C7 | `indonesia_import_requirements.md` | ⬜ | ⬜ |
| C8 | `malaysia_import_requirements.md` | ⬜ | ⬜ |
| C9 | `thailand_import_requirements.md` | ⬜ | ⬜ |
| C10 | `vietnam_import_requirements.md` | ⬜ | ⬜ |
| C11 | `philippines_import_requirements.md` | ⬜ | ⬜ |
| C12 | `asean_tariff_finder_guide.md` | ⬜ | ⬜ |
| C13 | `atiga_overview.md` | ⬜ | ⬜ |
| C14 | `asean_rules_of_origin.md` | ⬜ | ⬜ |

### Category D: Internal Documents (No Action Required)

| Doc | File | Status |
|-----|------|--------|
| D1 | `service_terms_conditions.md` | ✅ No change needed |
| D2 | `sla_policy.md` | ✅ No change needed |
| D3 | `booking_procedure.md` | ✅ No change needed |
| D4 | `escalation_procedure.md` | ✅ No change needed |
| D5 | `cod_procedure.md` | ✅ No change needed |
| D6 | `fta_comparison_matrix.md` | ✅ No change needed |

---

## URL Discovery Strategy

### Tool: Claude in Chrome (REQUIRED)

**All URL discovery MUST be performed using Claude in Chrome browser extension.**

Do NOT use:
- ❌ `web_fetch` tool (unreliable for carrier sites, many 404s and blocks)
- ❌ `WebSearch` tool (returns search results, not actual page verification)

Use ONLY:
- ✅ **Claude in Chrome** for all URL discovery and verification

### Why Claude in Chrome?

1. **Handles JavaScript-heavy sites** - Carrier websites often use React/Vue/Angular
2. **Sees actual rendered content** - Not just HTML source
3. **Can navigate dynamically** - Click menus, expand sections, follow redirects
4. **No bot blocking** - Uses real browser with user cookies/session
5. **Visual verification** - Can confirm content matches document claims

### URL Discovery Flowchart

```
For each carrier/reference document:
  │
  ├─→ Step 1: Open Claude in Chrome
  │     │
  │     └─→ Navigate to the organization's root domain
  │           • pilship.com, maersk.com, one-line.com, etc.
  │
  ├─→ Step 2: Find specific pages via navigation
  │     │
  │     ├─→ Use site menu to find: About, Services, Products, Contact
  │     ├─→ Look for Singapore-specific pages or regional content
  │     ├─→ Check footer for sitemap or additional links
  │     │
  │     └─→ For each page found:
  │           • Copy the FULL URL from browser address bar
  │           • Note what content the page contains
  │
  ├─→ Step 3: If page not in navigation, use site search
  │     │
  │     └─→ Search within the site for: "about", "services", "singapore"
  │
  └─→ Step 4: If still not found, use Google Search
        │
        ├─→ Search: "[topic] site:[official-domain]"
        │     Examples:
        │     • "about us site:pilship.com"
        │     • "services singapore site:maersk.com"
        │     • "incoterms 2020 site:iccwbo.org"
        │
        ├─→ ⚠️ Use AI Overview for CLUES ONLY, not as source
        │
        ├─→ Click through to authoritative result
        │
        └─→ Copy the actual page URL from browser
```

### User Workflow

When Claude Code requests URL discovery:

1. **User opens Chrome** with Claude extension active
2. **User navigates** to the carrier/organization website
3. **User finds** the relevant pages (About, Services, etc.)
4. **User copies URLs** and provides them to Claude Code
5. **Claude Code updates** the document frontmatter with verified URLs

**Communication format**:
```
Claude Code: "Please use Claude in Chrome to find the About and Services
             page URLs for pilship.com"

User: "Found these URLs:
       - About: https://www.pilship.com/about-pil/
       - Services: https://www.pilship.com/shipping-solutions/overview/"

Claude Code: [Updates document with provided URLs]
```

### Google Search Best Practices

**Search patterns**:
```
"[topic] site:[domain]"           → Search within specific domain
"[company] [page type] official"  → Find official pages
"[topic] [org] -pdf"              → Exclude PDF results
```

**For carrier websites**:
```
"PIL singapore services site:pilship.com"
"Maersk local information singapore site:maersk.com"
"ONE ocean network express about site:one-line.com"
"Evergreen marine singapore site:evergreen-marine.com"
"SIA cargo products site:siacargo.com"
"Cathay cargo solutions site:cathaycargo.com"
```

**For reference organizations**:
```
"Incoterms 2020 rules site:iccwbo.org"
"Harmonized System nomenclature site:wcoomd.org"
"AHTN 2022 site:asean.org"
```

### Source Authority Hierarchy

When multiple sources are found, prioritize:

| Priority | Source Type | Examples |
|----------|-------------|----------|
| 1 | Official organization page | carrier's own website |
| 2 | Official regulatory body | customs.gov.sg, wcoomd.org |
| 3 | Government trade portals | trade.gov, enterprisesg.gov.sg |
| 4 | Industry associations | iccwbo.org, asean.org |
| 5 | News/press releases | Only if no official page exists |

**CRITICAL**: 
- AI Overview is NOT a source - it's a clue
- Always click through to and cite the actual authoritative page
- Never cite aggregator or secondary sources when primary exists

---

## Browser Navigation Tips

### For Carrier Websites

**Common URL patterns to try**:
```
/about-us or /about or /company
/services or /solutions or /products
/network or /routes or /schedules
/singapore or /local/singapore or /en-sg
/eservices or /digital or /tools
/contact or /contact-us
```

**If page not found (404)**:
1. Go to site homepage
2. Use site navigation menu
3. Look for footer links
4. Try site search if available
5. Check if there's a Singapore-specific subdomain (e.g., sg.carrier.com)

### For Reference Organizations

**ICC (Incoterms)**:
- Main site: iccwbo.org
- Navigate: Business Solutions → Incoterms Rules
- Free resources are in Knowledge/Publications sections
- Avoid ICC Store links (paid content)

**WCO (HS Codes)**:
- Main site: wcoomd.org
- Navigate: Topics → Nomenclature
- HS Convention and HS Edition pages are public
- Online tools may require registration

---

## Quality Checklist

Before marking a document complete, verify:

- [ ] `source_organization` field added with correct official name
- [ ] `source_urls` array with at least one specific page URL
- [ ] Each URL has `description` explaining what content it provides
- [ ] Each URL has `retrieved_date` in YYYY-MM-DD format
- [ ] URLs are specific pages, NOT root domains
- [ ] URLs are publicly accessible (not behind login/paywall)
- [ ] Document content still matches information from sources
- [ ] All other frontmatter fields preserved

---

## Example: Before and After

### Before (Old Schema)
```yaml
---
title: Maersk Service Summary
source: https://www.maersk.com
source_type: public_carrier
last_updated: 2025-01-20
jurisdiction: Global
category: carrier
use_cases: [UC-3.1, UC-3.2, UC-3.3]
---
```

### After (New Schema)
```yaml
---
title: Maersk Service Summary
source_organization: A.P. Moller - Maersk
source_urls:
  - url: https://www.maersk.com/local-information/asia-pacific/singapore
    description: Singapore local operations and office information
    retrieved_date: 2025-01-22
  - url: https://www.maersk.com/transportation-services/ocean-transport
    description: Ocean freight service offerings and capabilities
    retrieved_date: 2025-01-22
  - url: https://www.maersk.com/schedules
    description: Route schedules and port coverage
    retrieved_date: 2025-01-22
source_type: public_carrier
last_updated: 2025-01-22
jurisdiction: Global
category: carrier
use_cases: [UC-3.1, UC-3.2, UC-3.3]
---
```

---

## Start Command

To begin remediation, use this prompt:

```
Start source attribution remediation for Waypoint knowledge base.

Read the full prompt at:
C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase1_poc\knowledge_base\SOURCE_REMEDIATION_PROMPT.md

Begin with Category A (carrier documents) - Phase 1.

For each carrier document (A1-A6):

1. USE CLAUDE IN CHROME to navigate to carrier website
   - pilship.com, maersk.com, one-line.com, etc.

2. FIND specific page URLs for:
   - About / Company page
   - Services / Solutions page
   - Singapore-specific page (if exists)
   - Contact page

3. COPY the exact URLs from browser address bar

4. PROVIDE URLs to Claude Code in this format:
   - About: [URL]
   - Services: [URL]
   - Singapore: [URL] (or "not found")

5. Claude Code will UPDATE the document frontmatter with new schema

6. VERIFY and CONFIRM each document before moving to next

Proceed document by document.
```

---

**Document Created**: 2025-01-22  
**Total Documents to Update**: 23 (9 need URLs, 14 need schema alignment)  
**Estimated Time**: 2-3 hours for full remediation
