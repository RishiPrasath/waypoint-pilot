# PDF Discovery Log

**Date**: 2026-02-06
**Tool**: Chrome DevTools MCP
**Status**: Complete

## Summary
| Category | URLs Visited | PDFs Found | PDFs Downloaded | PDFs Merged |
|----------|-------------|------------|-----------------|-------------|
| 6a Singapore Customs | 7/7 | 7 | 7 | 3 |
| 6b ASEAN Trade | 6/6 | 60+ | 6 | 1 |
| 6c Country-specific | 14/14 | 0 | 0 | 0 |
| 6d Ocean Carriers | 13/13 | 19 | 7 | 0 |
| 6e Air Carriers | 9/9 | 3 | 2 | 0 |
| 6f Reference | 6/6 | 2 | 2 | 1 |
| **TOTAL** | **55/55** | **91+** | **24** | **5** |

---

## 6a: Singapore Customs

### URL 1: https://www.customs.gov.sg/businesses/exporting-goods/overview/
- **Visited**: 2026-02-06 18:00
- **Page loaded**: Yes
- **PDF links found**: 1
  - customs_guide_records_image_system.pdf (11 pages, HIGH) → Downloaded, not merged (record-keeping focus, lower retrieval value)

### URL 2: https://www.customs.gov.sg/businesses/importing-goods/overview/
- **Visited**: 2026-02-06 18:01
- **Page loaded**: Yes
- **PDF links found**: 1 (same as URL 1, duplicate)

### URL 3: https://www.customs.gov.sg/businesses/valuation-duties-taxes-fees/goods-and-services-tax-gst/
- **Visited**: 2026-02-06 18:02
- **Page loaded**: Yes
- **PDF links found**: 0

### URL 4: https://www.customs.gov.sg/businesses/rules-of-origin/origin-documentation/
- **Visited**: 2026-02-06 18:03
- **Page loaded**: Yes
- **PDF links found**: 2
  - handbook_non_preferential_roo.pdf (6 pages, HIGH) → Merged into sg_certificates_of_origin.md
  - handbook_roo_preferential_co.pdf (33 pages, HIGH) → Merged into sg_certificates_of_origin.md

### URL 5: https://www.customs.gov.sg/businesses/importing-goods/import-procedures/depositing-goods-in-ftz/
- **Visited**: 2026-02-06 18:04
- **Page loaded**: Yes
- **PDF links found**: 1
  - ftz_circular_01_2020.pdf (2 pages, MEDIUM) → Referenced in sg_free_trade_zones.md frontmatter

### URL 6: https://www.customs.gov.sg/businesses/customs-schemes-licences-and-framework/ftz-operator-licence/
- **Visited**: 2026-02-06 18:05
- **Page loaded**: Yes
- **PDF links found**: 0

### URL 7: https://www.customs.gov.sg/businesses/harmonised-system-classification-of-goods/understanding-hs-classification
- **Visited**: 2026-02-06 18:06
- **Page loaded**: Yes
- **PDF links found**: 4
  - general_interpretative_rules.pdf (3 pages, HIGH) → Merged into sg_hs_classification.md
  - ahtn_2022_changes.pdf (65 pages, HIGH) → Downloaded, referenced in frontmatter
  - how_to_determine_hs_code.pdf (1 page, LOW - image only) → Downloaded, not merged
  - how_to_read_the_hs.pdf (1 page, LOW - image only) → Downloaded, not merged

## 6b: ASEAN Trade

### URL 1: https://asean.org/our-communities/economic-community/trade-in-goods/
- **Visited**: 2026-02-06 18:15
- **Page loaded**: Yes
- **PDF links found**: ~60 (treaty documents, annexes, protocols)
- **Relevant PDFs downloaded**:
  - atiga_full_text.pdf (129 pages, HIGH) → Referenced in atiga_overview.md frontmatter
  - atiga_annex5_rvc_guidelines.pdf (2 pages, MEDIUM) → Merged RVC principles into atiga_overview.md
  - atiga_annex7_form_d.pdf (3 pages, MEDIUM) → Downloaded, referenced in frontmatter
  - average_cept_atiga_tariff_rates.pdf (4 pages, MEDIUM) → Merged tariff rate table into atiga_overview.md
  - asean_tariff_finder_leaflet.pdf (2 pages, MEDIUM) → Downloaded
  - asean_self_certification_guidebook.pdf (72 pages, not extracted - too large, reference only)

### URL 2: https://asean.org/our-communities/economic-community/rules-of-origin/
- **Visited**: 2026-02-06 18:16
- **Page loaded**: Yes
- **PDF links found**: 21 (mostly overlaps with URL 1)
- **Notes**: Self-certification guidebook and ROO focal points list. No new unique PDFs beyond URL 1.

### URL 3: https://tariff-finder.asean.org
- **Visited**: 2026-02-06 18:17
- **Page loaded**: Redirected to login page (asean.mendel-online.com)
- **PDF links found**: 0 (requires authentication)

### URL 4: https://atr.asean.org
- **Visited**: 2026-02-06 18:18
- **Page loaded**: Yes (ASEAN Trade Repository)
- **PDF links found**: 0 (web application)

### URL 5: https://asw.asean.org
- **Visited**: 2026-02-06 18:19
- **Page loaded**: Yes (ASEAN Single Window)
- **PDF links found**: 0 (web application)

### URL 6: https://acts.asean.org
- **Visited**: 2026-02-06 18:20
- **Page loaded**: Yes (ASEAN Customs Transit System)
- **PDF links found**: 0 (information portal)

## 6c: Country-specific

### trade.gov Country Guides (5 URLs)
- **Indonesia**: 3 PDFs — all ITA Quality Assurance (irrelevant), 0 relevant
- **Malaysia**: 3 PDFs — all ITA Quality Assurance (irrelevant), 0 relevant
- **Thailand**: 3 PDFs — all ITA Quality Assurance (irrelevant), 0 relevant
- **Vietnam**: 3 PDFs — all ITA Quality Assurance (irrelevant), 0 relevant
- **Philippines**: 3 PDFs — all ITA Quality Assurance (irrelevant), 0 relevant

### National Customs Portals (9 URLs)
- **insw.go.id** (Indonesia): No PDFs (web portal)
- **beacukai.go.id** (Indonesia): No PDFs (web portal)
- **customs.gov.my** (Malaysia): No PDFs (redirects to Malay version)
- **miti.gov.my** (Malaysia): No PDFs
- **customs.go.th** (Thailand): TIMEOUT — page did not load
- **customs.gov.vn** (Vietnam): No PDFs
- **vietnamtradeportal.gov.vn** (Vietnam): No PDFs (web portal)
- **customs.gov.ph** (Philippines): 403 Forbidden — access blocked
- **dti.gov.ph** (Philippines): ERR_CERT_DATE_INVALID — SSL certificate expired

**Summary**: No relevant PDFs found across all 14 country-specific URLs. Government portals are web-based applications, and trade.gov pages only contain standard ITA boilerplate PDFs.

## 6d: Ocean Carriers

### PIL (3 URLs)
- **pilship.com/about-pil/**: No PDFs
- **pilship.com/shipping-solutions/overview/**: No PDFs
- **pilship.com/tariffs-charges/**: 23 PDFs found — all India-specific port tariffs, not relevant to Singapore KB. Skipped.

### Maersk (4 URLs)
- **maersk.com/about**: No PDFs
- **maersk.com/local-information/asia-pacific/singapore**: 19 Singapore-specific PDFs found!
  - maersk_sg_import_delivery_order.pdf (15 pages, HIGH) → Downloaded, referenced in frontmatter
  - maersk_sg_spot_booking.pdf (4 pages, MEDIUM) → Downloaded
  - maersk_sg_shipping_instructions.pdf (5 pages, MEDIUM) → Downloaded
  - maersk_sg_demurrage_detention.pdf (2 pages, MEDIUM) → Downloaded
  - maersk_sg_booking_amendment.pdf (3 pages, MEDIUM) → Downloaded
  - maersk_sg_notifications_guide.pdf (5 pages, HIGH) → Downloaded
  - maersk_sg_telex_release.pdf (1 page, MEDIUM) → Downloaded
  - **Note**: Most PDFs are image-heavy operational guides with limited extractable text
- **maersk.com/schedules/**: No PDFs (web app)
- **maersk.com/logistics-solutions**: No PDFs

### ONE (3 URLs)
- **sg.one-line.com/about-us**: No PDFs
- **sg.one-line.com/service-maps**: No PDFs
- **sg.one-line.com/dry-containers**: No PDFs

### Evergreen (3 URLs)
- **evergreen-marine.com.sg/.../CorporateProfile.jsp**: No PDFs
- **ss.shipmentlink.com/.../LongTermMenu.jsp**: 398 sailing schedule PDFs — not relevant, skipped
- **evergreen-marine.com.sg/.../Containers.jsp**: No PDFs

## 6e: Air Carriers

### SIA Cargo (5 URLs)
- **siacargo.com/our-company/**: No PDFs
- **siacargo.com/products/**: No PDFs
- **siacargo.com/products/thrucool/**: 1 PDF found
  - sia_cargo_thrucool_brochure.pdf (2 pages, LOW - image only) → Downloaded
- **siacargo.com/products/thrufresh/**: 2 PDFs found
  - sia_cargo_thrufresh_brochure.pdf (4 pages, HIGH) → Downloaded, referenced in frontmatter
  - Cargo tracking device PDF → Skipped (not relevant)
- **siacargo.com/network/**: No PDFs

### Cathay Cargo (4 URLs)
- **cathaycargo.com/en-us/about-us.html**: No PDFs
- **cathaycargo.com/en-us/solutions/cathay-pharma.html**: ERROR - net::ERR_HTTP2_PROTOCOL_ERROR
- **cathaycargo.com/en-us/solutions/cathay-fresh.html**: ERROR - net::ERR_HTTP2_PROTOCOL_ERROR
- **cathaycargo.com/en-us/solutions/cathay-live-animal.html**: ERROR - net::ERR_HTTP2_PROTOCOL_ERROR

## 6f: Reference

### URL 1: https://iccwbo.org/business-solutions/incoterms-rules/
- **Visited**: 2026-02-06 18:25
- **Page loaded**: Yes
- **PDF links found**: 0

### URL 2: https://iccwbo.org/business-solutions/incoterms-rules/incoterms-2020/
- **Visited**: 2026-02-06 18:26
- **Page loaded**: Yes (redirected from /ressources-for-business-2/)
- **PDF links found**: 0

### URL 3: https://iccwbo.org/business-solutions/incoterms-rules/incoterms-rules-history/
- **Visited**: 2026-02-06 18:27
- **Page loaded**: Yes
- **PDF links found**: 0

### URL 4: https://www.wcoomd.org/en/topics/nomenclature/overview.aspx
- **Visited**: 2026-02-06 18:28
- **Page loaded**: Yes
- **PDF links found**: 3
  - access_request_form.pdf → Skipped (irrelevant)
  - wco_hs_compendium_30years.pdf (54 pages, HIGH) → Downloaded, referenced in hs_code_structure_guide.md frontmatter
  - wco_understanding_hs_2028.pdf (2 pages, HIGH) → Downloaded, merged border treatment content into hs_code_structure_guide.md

### URL 5: https://www.wcoomd.org/en/topics/nomenclature/overview/what-is-the-harmonized-system.aspx
- **Visited**: 2026-02-06 18:29
- **Page loaded**: Yes
- **PDF links found**: 1 (access form only, duplicate)

### URL 6: https://www.wcoomd.org/en/topics/nomenclature/overview/hs-multi-purposes-tool.aspx
- **Visited**: 2026-02-06 18:30
- **Page loaded**: Yes
- **PDF links found**: 1 (access form only, duplicate)

**Summary**: 2 relevant PDFs found and downloaded from WCO. No PDFs available from ICC (Incoterms content is behind paywall/proprietary).
