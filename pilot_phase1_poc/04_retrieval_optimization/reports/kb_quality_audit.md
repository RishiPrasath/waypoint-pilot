# Knowledge Base Quality Audit Report

**Date**: 2026-02-06
**Scope**: All documents in `04_retrieval_optimization/kb/`
**Auditor**: Claude (automated)

---

## Executive Summary

The rebuilt KB contains **30 main documents** and **50 PDF extract files** across 4 categories. Overall content quality is strong — 21 of 30 main documents rated HIGH — but retrieval readiness is held back by missing `retrieval_keywords` metadata in 22 documents (73%). Three documents have critically thin content (<4KB) and need expansion before Task 7 validation.

| Dimension | Score | Status |
|-----------|:-----:|--------|
| Content Quality | 8.5/10 | Good |
| Structure & Organization | 8.6/10 | Good |
| Frontmatter Completeness | 7.2/10 | Needs Work |
| Retrieval Readiness | 6.9/10 | Needs Work |
| **Overall** | **7.8/10** | **Good — Ready with fixes** |

---

## Inventory

| Category | Main Docs | PDF Extracts | Total Files |
|----------|:---------:|:------------:|:-----------:|
| 01_regulatory | 14 | 30 | 44 |
| 02_carriers | 6 | 12 | 18 |
| 03_reference | 3 | 5 | 8 |
| 04_internal_synthetic | 7 | 0 | 7 |
| **Total** | **30** | **50** (Task 6: 22, Task 6.1: 28) | **80** |

---

## Quality Distribution

| Rating | Count | % | Documents |
|--------|:-----:|:-:|-----------|
| **HIGH** | 21 | 70% | atiga_overview, sg_certificates_of_origin, sg_hs_classification, indonesia_import, thailand_import, vietnam_import, philippines_import, asean_rules_of_origin, all 6 carriers, all 3 references, booking_procedure, customer_faq, cod_handling, fta_comparison, service_terms, sla_policy |
| **MEDIUM** | 6 | 20% | sg_free_trade_zones, asean_tariff_finder_guide, malaysia_import, escalation_procedure, maersk_service_summary (borderline HIGH), incoterms_comparison (borderline HIGH) |
| **LOW** | 3 | 10% | sg_export_procedures, sg_import_procedures, sg_gst_guide |

---

## Detailed Assessment: 01_regulatory (14 documents)

| # | Document | Lines | Quality | Issues | Recommendation |
|---|----------|:-----:|:-------:|--------|----------------|
| 1 | atiga_overview.md | 342 | **HIGH** | None | Production ready |
| 2 | sg_certificates_of_origin.md | 388 | **HIGH** | Missing retrieval_keywords | Add keywords |
| 3 | sg_hs_classification.md | 254 | **HIGH** | None | Production ready |
| 4 | asean_rules_of_origin.md | 191 | **HIGH** | Missing retrieval_keywords | Add keywords |
| 5 | indonesia_import_requirements.md | 181 | **HIGH** | Missing retrieval_keywords | Add keywords |
| 6 | thailand_import_requirements.md | 235 | **HIGH** | Missing retrieval_keywords | Add keywords |
| 7 | vietnam_import_requirements.md | 244 | **HIGH** | Missing retrieval_keywords | Add keywords |
| 8 | philippines_import_requirements.md | 236 | **HIGH** | Missing retrieval_keywords | Add keywords |
| 9 | malaysia_import_requirements.md | 240 | **MEDIUM** | Missing keywords; limited uCustoms detail | Add keywords; expand uCustoms workflow |
| 10 | sg_free_trade_zones.md | 151 | **MEDIUM** | Sparse penalties section | Add violation examples; expand transhipment workflow |
| 11 | asean_tariff_finder_guide.md | 144 | **MEDIUM** | Missing keywords; no FTA comparison examples | Add keywords; add worked examples |
| 12 | sg_export_procedures.md | 106 | **LOW** | ~3KB thin content; missing source_pdfs | Expand controlled goods, record retention; add source PDFs |
| 13 | sg_import_procedures.md | 126 | **LOW** | ~3.7KB thin content; missing source_pdfs | Expand MES/IGDS/TIS schemes; detail FTZ procedures |
| 14 | sg_gst_guide.md | 97 | **LOW** | ~2.4KB thinnest doc; missing source_pdfs; no relief schemes | Expand IGDS/MES mechanics; add refund procedures |

### Regulatory Summary
- 8 HIGH, 3 MEDIUM, 3 LOW
- Country-specific import guides (5) all well-structured with consistent format
- Singapore core docs (export/import/GST) are noticeably thin vs. enriched docs
- ATIGA and CO documents heavily enriched during Tasks 6/6.1 — strongest in category

---

## Detailed Assessment: 02_carriers (6 documents)

| # | Document | Lines | Quality | Issues | Recommendation |
|---|----------|:-----:|:-------:|--------|----------------|
| 1 | maersk_service_summary.md | 281 | **HIGH** | No retrieval_keywords; 6 source PDFs but not all integrated | Add keywords; link PDF guides in content |
| 2 | pil_service_summary.md | 191 | **HIGH** | No retrieval_keywords; missing SG office details | Add keywords; expand contact info |
| 3 | one_service_summary.md | 195 | **HIGH** | No retrieval_keywords; unclear operating hours | Add keywords; clarify standard vs emergency hours |
| 4 | evergreen_service_summary.md | 215 | **HIGH** | No retrieval_keywords; PSA JV unexplained | Add keywords; explain alliance implications |
| 5 | cathay_cargo_service_guide.md | 252 | **HIGH** | No retrieval_keywords; no air vs sea comparison | Add keywords; add minimum shipment sizes |
| 6 | sia_cargo_service_guide.md | 225 | **HIGH** | No retrieval_keywords; THRUCOOL/THRUFRESH specs minimal | Add keywords; expand temperature specs |

### Carrier Summary
- All 6 rated HIGH — consistent quality across ocean and air
- **All 6 missing retrieval_keywords** — critical gap for carrier-specific queries
- Maersk most enriched (D&D calc, telex release, DO process added from PDFs)
- PIL lightest coverage (191 lines, no deep PDF enrichment)

---

## Detailed Assessment: 03_reference (3 documents)

| # | Document | Lines | Quality | Issues | Recommendation |
|---|----------|:-----:|:-------:|--------|----------------|
| 1 | hs_code_structure_guide.md | 523 | **HIGH** | No keywords; very dense (22KB) may chunk poorly | Add keywords; consider splitting Quick Guide vs Reference |
| 2 | incoterms_2020_reference.md | 416 | **HIGH** | No keywords; dense but well-structured | Add keywords; add 1-sentence summaries per term |
| 3 | incoterms_comparison_chart.md | 293 | **HIGH** | No keywords; ASCII flowcharts hard for RAG | Add keywords; add text-based decision logic |

### Reference Summary
- All 3 rated HIGH — most comprehensive category
- HS Code Guide (523 lines) is the largest document — may need splitting for optimal chunking
- **All 3 missing retrieval_keywords**

---

## Detailed Assessment: 04_internal_synthetic (7 documents)

| # | Document | Lines | Quality | Issues | Recommendation |
|---|----------|:-----:|:-------:|--------|----------------|
| 1 | booking_procedure.md | 526 | **HIGH** | Has keywords | Cross-link to SLA and escalation |
| 2 | customer_faq.md | 236 | **HIGH** | Has keywords; only 8 FAQs | Expand to 15+ FAQs |
| 3 | service_terms_conditions.md | 437 | **HIGH** | Has keywords; "[Company Name]" placeholder (5+ times) | Replace placeholders |
| 4 | sla_policy.md | 344 | **HIGH** | Has keywords; redacted contact numbers | Replace redacted numbers |
| 5 | fta_comparison_matrix.md | 334 | **HIGH** | No keywords; 27 FTAs is very dense | Add keywords; consolidate ROO into single table |
| 6 | cod_handling_procedure.md | 367 | **HIGH** | No keywords; lacks customer-facing FAQ | Add keywords; add customer FAQ section |
| 7 | escalation_procedure.md | 332 | **MEDIUM** | No keywords; redacted contact numbers | Add keywords; fix placeholders |

### Internal Summary
- 6 HIGH, 1 MEDIUM — strongest category overall
- 4 of 7 already have retrieval_keywords (best ratio of any category)
- Placeholder text in service_terms, sla_policy, escalation_procedure needs fixing
- booking_procedure.md (526 lines) is the most retrieval-friendly document in the entire KB

---

## PDF Extract Files Assessment (50 files)

PDF extracts in `pdfs/` subdirectories serve as **reference material** — content was selectively merged into main KB docs. These files are NOT ingested directly.

### 01_regulatory/pdfs/ (30 files)

| Source | Extract Quality | Merged Into | Notes |
|--------|:-:|---|---|
| atiga_full_text.md | HIGH | atiga_overview.md | Tariff rates, RVC principles |
| atiga_annex5_rvc_guidelines.md | HIGH | atiga_overview.md | RVC calculation |
| atiga_annex7_form_d.md | MEDIUM | — | Image-heavy form |
| atiga_annex8_awsc_ocp.md | MEDIUM | sg_certificates_of_origin.md | AWSC definitions |
| atiga_fact_sheet_wto.md | MEDIUM | atiga_overview.md | Tariff line table |
| atiga_annex6_partial_cumulation.md | MEDIUM | atiga_overview.md | Partial cumulation rules |
| atiga_first_protocol_amendment.md | LOW | — | Image-only, skipped |
| atiga_annex3_psr_hs2022.md | MEDIUM | — | Too large (41 pages), referenced only |
| aec_2025_trade_facilitation_sap.md | HIGH | — | Referenced in frontmatter |
| asean_trade_facilitation_framework.md | HIGH | atiga_overview.md | ATFF section |
| asean_import_licensing_guidelines.md | MEDIUM | — | Referenced in frontmatter |
| asean_ntm_guidelines.md | MEDIUM | — | Referenced in frontmatter |
| asean_seamless_trade_facilitation_astfi.md | HIGH | — | Too large (168 pages), referenced only |
| awsc_guidebook_english.md | HIGH | sg_certificates_of_origin.md | CE requirements, OD format, FAQs |
| atiga_psr_implementing_guidelines.md | MEDIUM | — | Referenced in frontmatter |
| minor_discrepancies_proof_of_origin.md | MEDIUM | sg_certificates_of_origin.md | 8 discrepancy types |
| awsc_origin_declaration_format.md | MEDIUM | sg_certificates_of_origin.md | OD field format |
| eform_d_full_implementation.md | MEDIUM | — | Referenced in frontmatter |
| average_cept_atiga_tariff_rates.md | HIGH | atiga_overview.md | Tariff rates table |
| asean_tariff_finder_leaflet.md | MEDIUM | — | Marketing content |
| general_interpretative_rules.md | HIGH | sg_hs_classification.md | GIR rules |
| ahtn_2022_changes.md | HIGH | — | Referenced in frontmatter |
| how_to_determine_hs_code.md | LOW | — | Image-only |
| how_to_read_the_hs.md | LOW | — | Image-only |
| handbook_roo_preferential_co.md | HIGH | sg_certificates_of_origin.md | ROO handbook |
| handbook_non_preferential_roo.md | HIGH | sg_certificates_of_origin.md | Non-preferential ROO |
| ftz_circular_01_2020.md | MEDIUM | — | FTZ circular, referenced |
| customs_guide_records_image_system.md | LOW | — | Image system guide |
| sg_customs_handbook_co_tradenet.md | HIGH | sg_certificates_of_origin.md | Certificate types, CO rules |
| sg_customs_important_permit_fields.md | MEDIUM | — | Permit field reference |
| sg_customs_asean_aeo_mra.md | HIGH | — | Referenced in frontmatter |
| sg_customs_mra_factsheet_asean.md | HIGH | — | Referenced in frontmatter |

### 02_carriers/pdfs/ (12 files)

| Source | Extract Quality | Merged Into | Notes |
|--------|:-:|---|---|
| maersk_sg_booking_amendment.md | MEDIUM | — | Image-heavy |
| maersk_sg_demurrage_detention.md | MEDIUM | maersk_service_summary.md | D&D rates |
| maersk_sg_notifications_guide.md | MEDIUM | — | Platform guide |
| maersk_sg_shipping_instructions.md | MEDIUM | — | Image-heavy |
| maersk_sg_spot_booking.md | MEDIUM | — | Image-heavy |
| maersk_sg_telex_release.md | MEDIUM | maersk_service_summary.md | LOI template |
| maersk_sg_demurrage_detention_calc.md | MEDIUM | maersk_service_summary.md | Calculator guide |
| maersk_sg_import_delivery_order.md | HIGH | maersk_service_summary.md | DO process |
| maersk_sg_spot_booking_guide.md | LOW | — | Image-heavy, minimal text |
| maersk_sg_shipping_instructions_guide.md | LOW | — | Image-heavy, minimal text |
| maersk_sg_telex_release_template.md | MEDIUM | maersk_service_summary.md | LOI template |
| sia_cargo_thrucool_brochure.md | MEDIUM | — | Product brochure |
| sia_cargo_thrufresh_brochure.md | MEDIUM | — | Product brochure |

### 03_reference/pdfs/ (5 files)

| Source | Extract Quality | Merged Into | Notes |
|--------|:-:|---|---|
| wco_hs_compendium_30years.md | HIGH | hs_code_structure_guide.md | Border treatment content |
| wco_understanding_hs_2028.md | HIGH | hs_code_structure_guide.md | HS overview |
| sg_customs_gir.md | HIGH | hs_code_structure_guide.md | Detailed GIR rules |
| sg_customs_how_to_determine_hs_code.md | LOW | — | Image-only |
| sg_customs_how_to_read_hs.md | LOW | — | Image-only |
| sg_customs_ahtn_2022_changes.md | HIGH | — | Referenced in frontmatter |

### PDF Extract Summary
- **HIGH quality**: 17 (34%) — substantial extractable text, merged into KB docs
- **MEDIUM quality**: 22 (44%) — partial text, selectively merged or referenced
- **LOW quality**: 6 (12%) — image-only or near-empty, skipped
- **5 image-only PDFs** (0-1 chars extracted): atiga_first_protocol_amendment, how_to_determine_hs_code, how_to_read_the_hs, maersk_sg_spot_booking_guide, maersk_sg_shipping_instructions_guide

---

## Critical Issues

### Issue 1: Missing Retrieval Keywords (22/30 documents) — SEVERITY: HIGH

**Impact**: Without `retrieval_keywords`, semantic search relies solely on content matching. Documents without keywords may not surface for synonym-rich queries (e.g., "duty rate" vs "tariff", "BL" vs "bill of lading").

| Category | With Keywords | Without | Gap |
|----------|:---:|:---:|:---:|
| 01_regulatory | 2/14 | 12 | 86% missing |
| 02_carriers | 0/6 | 6 | 100% missing |
| 03_reference | 0/3 | 3 | 100% missing |
| 04_internal | 4/7 | 3 | 43% missing |
| **Total** | **8/30** | **22** | **73% missing** |

**Documents with keywords**: atiga_overview, sg_hs_classification, booking_procedure, customer_faq, service_terms_conditions, sla_policy (+ 2 partial)

### Issue 2: Thin Content Documents (3 documents) — SEVERITY: HIGH

| Document | Lines | Chars | Problem |
|----------|:-----:|:-----:|---------|
| sg_gst_guide.md | 97 | 2,432 | No relief schemes, no refund procedures |
| sg_export_procedures.md | 106 | 3,015 | No controlled goods detail, no record retention examples |
| sg_import_procedures.md | 126 | 3,667 | No import scheme details (MES/IGDS/TIS) |

These are the **only 3 documents under 4KB** and are all core Singapore regulatory docs. They may produce too few chunks for effective retrieval.

### Issue 3: Placeholder Text (3 documents) — SEVERITY: MEDIUM

| Document | Placeholder | Occurrences |
|----------|-------------|:-----------:|
| service_terms_conditions.md | "[Company Name]" | 5+ |
| sla_policy.md | "+65 XXXX XXXX" | 2+ |
| escalation_procedure.md | "+65 XXXX XXXX" | 2+ |

These are synthetic internal documents created for the POC. Placeholders are intentional but may confuse retrieval if a query matches the placeholder pattern.

### Issue 4: Missing Source PDFs in Frontmatter (3 documents) — SEVERITY: LOW

| Document | Has source_pdfs? |
|----------|:---:|
| sg_export_procedures.md | No |
| sg_import_procedures.md | No |
| sg_gst_guide.md | No |

These 3 docs were CARRY FORWARD from Week 1 and received no PDF enrichment. No relevant PDFs were discovered during Tasks 6/6.1.

---

## Frontmatter Completeness Matrix

| Field | Present | Missing | Coverage |
|-------|:-------:|:-------:|:--------:|
| title | 30 | 0 | 100% |
| source_organization | 30 | 0 | 100% |
| source_urls | 30 | 0 | 100% |
| source_type | 30 | 0 | 100% |
| last_updated | 30 | 0 | 100% |
| jurisdiction | 30 | 0 | 100% |
| category | 30 | 0 | 100% |
| use_cases | 30 | 0 | 100% |
| **retrieval_keywords** | **8** | **22** | **27%** |
| source_pdfs | 10 | 20 | 33% |
| answers_queries | 8 | 22 | 27% |
| related_documents | 6 | 24 | 20% |

Core frontmatter (8 fields) is 100% complete across all 30 documents. Extended metadata (keywords, answers_queries, related_documents) is sparse.

---

## Enrichment Impact Analysis

### Documents Enriched via PDF Content (Tasks 6 + 6.1)

| Document | Sections Added | Source PDFs | Impact |
|----------|:-:|:-:|--------|
| sg_certificates_of_origin.md | 12+ | 8 | CE requirements, OD format, Certificate Types, CO rules, FAQs |
| atiga_overview.md | 4+ | 6 | Tariff lines, partial cumulation, ATFF, import licensing |
| hs_code_structure_guide.md | 3+ | 4 | Detailed GIR with examples, WCO border treatment |
| maersk_service_summary.md | 3 | 6 | D&D calc, telex release, delivery order |
| sg_hs_classification.md | 2 | 2 | GIR rules, customs ruling process |

These 5 documents received the most significant enrichment and are expected to drive the biggest retrieval improvements in Task 7.

### Queries Expected to Improve

| Query | Root Cause | Fix Applied | Expected Result |
|-------|-----------|-------------|:---:|
| #2 LCL booking | Missing | booking_procedure enriched with LCL section | PASS |
| #5 Commercial invoice samples | Missing | booking_procedure enriched with documentation | PASS |
| #6 Bill of Lading | Buried | booking_procedure restructured with B/L FAQ | PASS |
| #7 Packing list | Buried | booking_procedure restructured with packing list section | PASS |
| #15 ATIGA duty rate | Terminology | atiga_overview enriched with tariff rates + terminology | PASS |
| #19 HS code ruling | Missing | sg_hs_classification + hs_code_structure_guide enriched | PASS |
| #31 SLA Singapore | Missing | sla_policy enriched with delivery SLA section | PASS |
| #32 Customs in door-to-door | Missing | service_terms enriched with door-to-door definition | PASS |
| #37 Import permit | Buried | sg_import_procedures + service_terms restructured | LIKELY |

---

## Recommendations

### Priority 1: Before Task 7 (Must Do)

1. **Add retrieval_keywords to all 22 missing documents** (~1-2 hours)
   - Use existing atiga_overview.md and booking_procedure.md as templates
   - Include 8-15 keywords per document covering synonyms and abbreviations

2. **Expand 3 thin documents** (~2-3 hours)
   - sg_gst_guide.md → target 150+ lines: add IGDS, MES mechanics, GST refund process
   - sg_export_procedures.md → target 180+ lines: add controlled goods, record retention, schemes
   - sg_import_procedures.md → target 180+ lines: add MES/IGDS/TIS schemes, FTZ detail

### Priority 2: Should Do

3. **Fix placeholder text** in service_terms, sla_policy, escalation_procedure
4. **Expand customer_faq.md** from 8 to 15+ FAQs
5. **Add cross-reference sections** ("See Also") to all 30 documents

### Priority 3: Nice to Have

6. Consider splitting hs_code_structure_guide.md (523 lines) for better chunking
7. Add carrier-specific booking guides
8. Add worked FTA comparison examples to asean_tariff_finder_guide

---

## Conclusion

The KB rebuild (Tasks 6 + 6.1) significantly enriched 5 key documents with content from 53 PDFs discovered across 55+ URLs. The overall content quality is strong (70% HIGH), with the main gap being **retrieval metadata** rather than content itself.

**Key risk for Task 7**: The 22 documents without `retrieval_keywords` may underperform on synonym-heavy queries. Adding keywords before running the initial validation would provide the cleanest comparison against the Week 2 baseline.

**Estimated effort for Priority 1 fixes**: 3-5 hours
**Expected retrieval improvement**: 82% adjusted → 88-92% adjusted (if keyword + content fixes applied)
