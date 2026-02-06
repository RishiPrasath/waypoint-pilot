# Task 6.1: Deep PDF Discovery — Output Report

**Status**: Complete
**Date**: 2026-02-06
**Duration**: ~2.5 hours

---

## Summary

Task 6.1 performed keyword-driven deep crawls of the 3 highest-yield Tier 1 sites from Task 6, following sub-pages, expanding tab sections, and scanning sitemaps to uncover PDFs buried below surface-level pages.

| Metric | Value |
|--------|-------|
| Sites deep-crawled | 3 (Tier 1 only) |
| New PDFs downloaded | 28 |
| KB docs enriched | 4 |
| Content sections added | 12+ |

---

## Tier 1: asean.org Deep Crawl

### Key Documents Tab (Trade in Goods page)
- **Method**: Clicked Elementor tab widget (uid=4_45) to reveal hidden section
- **Result**: 41 PDFs exposed (37 new beyond Task 6 surface scan)
- **Downloaded**: 6 PDFs

| PDF | Pages | Quality | Action |
|-----|-------|---------|--------|
| atiga_fact_sheet_wto.pdf | 5 | MEDIUM | Merged tariff line table into atiga_overview.md |
| atiga_annex6_partial_cumulation.pdf | 1 | MEDIUM | Merged partial cumulation rules into atiga_overview.md |
| atiga_annex8_awsc_ocp.pdf | 33 | MEDIUM | Merged AWSC definitions into sg_certificates_of_origin.md |
| atiga_first_protocol_amendment.pdf | 3 | LOW | Image-only, skipped |
| aec_2025_trade_facilitation_sap.pdf | 9 | HIGH | Referenced in frontmatter |
| atiga_annex3_psr_hs2022.pdf | 41 | MEDIUM | Referenced in frontmatter (too large) |

### Trade Facilitation Sub-page
- **URL**: asean.org/our-communities/economic-community/trade-facilitation/
- **Result**: 74 PDFs found
- **Downloaded**: 4 PDFs

| PDF | Pages | Quality | Action |
|-----|-------|---------|--------|
| asean_trade_facilitation_framework.pdf | 5 | HIGH | Merged ATFF section into atiga_overview.md |
| asean_import_licensing_guidelines.pdf | 9 | MEDIUM | Referenced in frontmatter |
| asean_ntm_guidelines.pdf | 7 | MEDIUM | Referenced in frontmatter |
| asean_seamless_trade_facilitation_astfi.pdf | 168 | HIGH | Reference only (454K chars, too large) |

### Rules of Origin Sub-page
- **URL**: asean.org/our-communities/economic-community/rules-of-origin/
- **Result**: 21 PDFs (17 new)
- **Downloaded**: 5 PDFs

| PDF | Pages | Quality | Action |
|-----|-------|---------|--------|
| awsc_guidebook_english.pdf | 72 | HIGH | Merged CE requirements, OD format, FAQ into sg_certificates_of_origin.md |
| atiga_psr_implementing_guidelines.pdf | 1 | MEDIUM | Referenced in atiga_overview.md frontmatter |
| minor_discrepancies_proof_of_origin.pdf | 1 | MEDIUM | Merged 8 minor discrepancy types into sg_certificates_of_origin.md |
| awsc_origin_declaration_format.pdf | 2 | MEDIUM | Merged OD field format into sg_certificates_of_origin.md |
| eform_d_full_implementation.pdf | 1 | MEDIUM | Referenced in sg_certificates_of_origin.md frontmatter |

### Dead Pages
- AFTA Publications → 404
- Tariff Schedules (Annex 2) → 404

**asean.org total**: 15 PDFs downloaded, content merged into 2 KB docs

---

## Tier 1: customs.gov.sg Deep Crawl

### HS Classification Page
- **URL**: customs.gov.sg/businesses/harmonised-system-classification-of-goods/understanding-hs-classification/
- **Result**: 4 PDFs
- **Downloaded**: 4 PDFs

| PDF | Pages | Quality | Action |
|-----|-------|---------|--------|
| sg_customs_gir.pdf | 3 | HIGH | Merged detailed GIR rules with examples into hs_code_structure_guide.md |
| sg_customs_ahtn_2022_changes.pdf | 65 | HIGH | Referenced in frontmatter |
| sg_customs_how_to_determine_hs_code.pdf | 1 | LOW | Image-only, skipped |
| sg_customs_how_to_read_hs.pdf | 1 | LOW | Image-only, skipped |

### ROO Overview Page
- 1 new PDF: sg_customs_important_permit_fields.pdf (20pg, MEDIUM) — TradeNet permit field reference

### Sitemap Scan
- **Total PDFs in sitemap**: 2,315
- **Keyword-filtered**: 193 relevant
- **Downloaded**: 3 PDFs

| PDF | Pages | Quality | Action |
|-----|-------|---------|--------|
| sg_customs_handbook_co_tradenet.pdf | 46 | HIGH | Merged Certificate Types table + CO application rules into sg_certificates_of_origin.md |
| sg_customs_asean_aeo_mra.pdf | 3 | HIGH | Referenced in frontmatter |
| sg_customs_mra_factsheet_asean.pdf | 3 | HIGH | Referenced in frontmatter |

**customs.gov.sg total**: 8 PDFs downloaded, content merged into 2 KB docs

---

## Tier 1: maersk.com Deep Crawl

### Singapore Local Information Page
- **URL**: maersk.com/local-information/asia-pacific/singapore
- **Result**: 19 PDFs (mostly image-heavy platform guides)
- **Downloaded**: 5 PDFs

| PDF | Pages | Quality | Action |
|-----|-------|---------|--------|
| maersk_sg_demurrage_detention_calc.pdf | 2 | MEDIUM | Merged D&D calculator guide into maersk_service_summary.md |
| maersk_sg_import_delivery_order.pdf | 15 | HIGH | Merged DO release process into maersk_service_summary.md |
| maersk_sg_spot_booking_guide.pdf | 4 | MEDIUM | Image-heavy, referenced only |
| maersk_sg_shipping_instructions_guide.pdf | 5 | MEDIUM | Image-heavy, referenced only |
| maersk_sg_telex_release_template.pdf | 1 | MEDIUM | Merged telex release LOI template into maersk_service_summary.md |

**maersk.com total**: 5 PDFs downloaded, content merged into 1 KB doc

---

## KB Documents Modified

| Document | Sections Added |
|----------|---------------|
| **atiga_overview.md** | Tariff Line Elimination table, Partial Cumulation rules, ATFF section (scope, instruments, principles, import licensing), 4 new source_pdfs |
| **sg_certificates_of_origin.md** | CE requirements (7 conditions), CE obligations, OD vs e-Form D comparison, OD format fields, Minor discrepancies (8 types), AWSC FAQs (6), TradeNet Certificate Types (20 types), CO application rules, CO collection points, 6 new source_pdfs |
| **hs_code_structure_guide.md** | Detailed GIR rules with practical examples (all 6 rules), 2 new source_pdfs |
| **maersk_service_summary.md** | D&D calculator guide, Telex release process + LOI template, Self-service delivery order process |

---

## Cumulative PDF Inventory (Task 6 + Task 6.1)

| Category | Task 6 | Task 6.1 | Total |
|----------|--------|----------|-------|
| 01_regulatory | 14 | 20 | 34 |
| 02_carriers | 9 | 5 | 14 |
| 03_reference | 2 | 4 | 6 |
| **Total** | **25** | **28** | **53** |

---

## Key Findings

1. **Tab widgets vs accordions**: ASEAN site uses Elementor tab widgets, not traditional accordions. Standard JavaScript DOM walking missed them — needed accessibility tree (snapshot UIDs) to click tabs.

2. **Sitemap goldmine**: customs.gov.sg's sitemap.xml revealed 2,315 PDFs — far more than any page-by-page crawl could find. Keyword filtering narrowed to 193 relevant, then manual selection of highest-value.

3. **Image-heavy carrier guides**: Most Maersk platform guides are screenshot-heavy with minimal extractable text. The D&D calc, telex release, and IDO guides had useful text; others were essentially visual tutorials.

4. **Dead ASEAN sub-pages**: AFTA Publications and Tariff Schedules sub-pages both returned 404 — site has been restructured. Content likely merged into other pages.

5. **AWSC Guidebook was the biggest win**: 72 pages of detailed AWSC content including CE requirements, FAQ section, and OD format details — directly addresses multiple failing queries about self-certification and origin declarations.
