# Retrieval Quality Report

**Generated**: 2026-01-30T11:43:38.187984
**Total Queries**: 50
**Top-K**: 5
**Threshold**: 0.15

## Summary

| Category | Queries | Hits (Top-3) | Hit Rate |
|----------|---------|--------------|----------|
| Booking Documentation | 10 | 6 | 60.0% |
| Customs Regulatory | 10 | 8 | 80.0% |
| Carrier Information | 10 | 10 | 100.0% |
| Sla Service | 10 | 5 | 50.0% |
| Edge Cases Out Of Scope | 10 | 9 | 90.0% |
| **TOTAL** | **50** | **38** | **76.0%** |

## Decision Gate

| Quality Level | Threshold | Action |
|---------------|-----------|--------|
| ≥75% | PROCEED | Build retrieval service |
| 60-74% | INVESTIGATE | Review failures, minor fixes |
| <60% | REMEDIATE | Chunking optimization needed |

**Result**: **PROCEED** (Hit rate: 76.0%)

## Top 10 Failures

| Query | Expected | Got | Score |
|-------|----------|-----|-------|
| How do I apply for a Customs ruling on HS code? | sg_hs_classification | 03_reference_hs_code_structure_guide | 0.340 |
| I want to file a claim for damaged cargo | (out-of-scope) | 04_internal_synthetic_service_terms_cond | 0.264 |
| Do you handle import permit applications? | service_terms, booking | 01_regulatory_sg_export_procedures | 0.203 |
| What's our standard delivery SLA for Singapore? | sla_policy | 02_carriers_sia_cargo_service_guide | 0.185 |
| How far in advance should I book an LCL shipment? | booking | 04_internal_synthetic_service_terms_cond | 0.057 |
| What's the ATIGA preferential duty rate? | atiga | 03_reference_hs_code_structure_guide | 0.029 |
| Can we ship without a packing list? | sg_export, indonesia_import | 03_reference_incoterms_comparison_chart | -0.024 |
| Is customs clearance included in door-to-door? | service_terms, sla_policy | 01_regulatory_sg_export_procedures | -0.038 |
| What's a Bill of Lading and who issues it? | booking | 01_regulatory_philippines_import_require | -0.070 |
| What's the process for refused deliveries? | cod_procedure, service_terms | 03_reference_incoterms_2020_reference | -0.088 |

## Per-Category Details

### Booking Documentation

| # | Query | Top Result | Score | Hit? |
|---|-------|------------|-------|------|
| 1 | What documents are needed for sea freight Sin... | 01_regulatory_indonesia_import_requ | 0.389 | PASS |
| 2 | How far in advance should I book an LCL shipm... | 04_internal_synthetic_service_terms | 0.057 | FAIL |
| 3 | What's the difference between FCL and LCL? | 02_carriers_evergreen_service_summa | -0.196 | PASS |
| 4 | When is the SI cutoff for this week's Maersk ... | 02_carriers_maersk_service_summary | 0.024 | PASS |
| 5 | Do I need a commercial invoice for samples wi... | 02_carriers_pil_service_summary | -0.253 | FAIL |
| 6 | What's a Bill of Lading and who issues it? | 01_regulatory_philippines_import_re | -0.070 | FAIL |
| 7 | Can we ship without a packing list? | 03_reference_incoterms_comparison_c | -0.024 | FAIL |
| 8 | What does FOB Singapore mean? | 03_reference_incoterms_comparison_c | 0.150 | PASS |
| 9 | How do I amend a booking after confirmation? | 04_internal_synthetic_service_terms | 0.318 | PASS |
| 10 | What's the free time at destination port? | 03_reference_incoterms_2020_referen | -0.143 | PASS |

### Customs Regulatory

| # | Query | Top Result | Score | Hit? |
|---|-------|------------|-------|------|
| 11 | What's the GST rate for imports into Singapor... | 01_regulatory_sg_gst_guide | 0.619 | PASS |
| 12 | How do I find the HS code for electronics? | 03_reference_hs_code_structure_guid | 0.272 | PASS |
| 13 | Is Certificate of Origin required for Thailan... | 01_regulatory_thailand_import_requi | 0.180 | PASS |
| 14 | What permits are needed to import cosmetics t... | 01_regulatory_indonesia_import_requ | 0.322 | PASS |
| 15 | What's the ATIGA preferential duty rate? | 03_reference_hs_code_structure_guid | 0.029 | FAIL |
| 16 | How does the Free Trade Zone work for re-expo... | 01_regulatory_sg_free_trade_zones | 0.165 | PASS |
| 17 | What's the de minimis threshold for Malaysia? | 01_regulatory_malaysia_import_requi | 0.087 | PASS |
| 18 | Do I need halal certification for food to Ind... | 01_regulatory_indonesia_import_requ | 0.310 | PASS |
| 19 | How do I apply for a Customs ruling on HS cod... | 03_reference_hs_code_structure_guid | 0.340 | FAIL |
| 20 | What's the difference between Form D and Form... | 01_regulatory_asean_rules_of_origin | -0.080 | PASS |

### Carrier Information

| # | Query | Top Result | Score | Hit? |
|---|-------|------------|-------|------|
| 21 | Which carriers sail direct to Ho Chi Minh? | 02_carriers_maersk_service_summary | -0.086 | PASS |
| 22 | What's the transit time to Port Klang? | 04_internal_synthetic_sla_policy | -0.168 | PASS |
| 23 | Does PIL offer reefer containers? | 02_carriers_pil_service_summary | 0.180 | PASS |
| 24 | How do I submit VGM to Maersk? | 02_carriers_maersk_service_summary | 0.286 | PASS |
| 25 | Can I get an electronic Bill of Lading? | 02_carriers_pil_service_summary | -0.027 | PASS |
| 26 | What's the weight limit for a 40ft container? | 02_carriers_one_service_summary | -0.013 | PASS |
| 27 | Does ONE service Surabaya? | 04_internal_synthetic_sla_policy | -0.268 | PASS |
| 28 | How do I track my shipment with Evergreen? | 02_carriers_evergreen_service_summa | 0.052 | PASS |
| 29 | What's the difference between Maersk and ONE ... | 02_carriers_maersk_service_summary | 0.201 | PASS |
| 30 | Who do I contact for a booking amendment? | 04_internal_synthetic_booking_proce | -0.094 | PASS |

### Sla Service

| # | Query | Top Result | Score | Hit? |
|---|-------|------------|-------|------|
| 31 | What's our standard delivery SLA for Singapor... | 02_carriers_sia_cargo_service_guide | 0.185 | FAIL |
| 32 | Is customs clearance included in door-to-door... | 01_regulatory_sg_export_procedures | -0.038 | FAIL |
| 33 | Do you provide cargo insurance? | 04_internal_synthetic_service_terms | 0.362 | PASS |
| 34 | What happens if shipment is delayed? | 04_internal_synthetic_sla_policy | -0.057 | PASS |
| 35 | Are duties and taxes included in the quote? | 04_internal_synthetic_service_terms | -0.114 | PASS |
| 36 | What's the process for refused deliveries? | 03_reference_incoterms_2020_referen | -0.088 | FAIL |
| 37 | Do you handle import permit applications? | 01_regulatory_sg_export_procedures | 0.203 | FAIL |
| 38 | How do I upgrade to express service? | 02_carriers_cathay_cargo_service_gu | -0.322 | FAIL |
| 39 | What's covered under standard liability? | 04_internal_synthetic_service_terms | 0.275 | PASS |
| 40 | Can I get proof of delivery? | 04_internal_synthetic_service_terms | -0.227 | PASS |

### Edge Cases Out Of Scope

| # | Query | Top Result | Score | Hit? |
|---|-------|------------|-------|------|
| 41 | What's the current freight rate to Jakarta? | 04_internal_synthetic_fta_compariso | -0.002 | PASS |
| 42 | Where is my shipment right now? | 03_reference_incoterms_2020_referen | -0.289 | PASS |
| 43 | Can you book a shipment for me? | 04_internal_synthetic_booking_proce | -0.122 | PASS |
| 44 | I want to file a claim for damaged cargo | 04_internal_synthetic_service_terms | 0.264 | FAIL |
| 45 | Can you ship hazmat by air? | 03_reference_incoterms_comparison_c | -0.112 | PASS |
| 46 | What's the weather forecast for shipping? | 03_reference_incoterms_2020_referen | -0.202 | PASS |
| 47 | Can you recommend a supplier in China? | 03_reference_incoterms_2020_referen | -0.097 | PASS |
| 48 | What's your company's financial status? | 04_internal_synthetic_sla_policy | -0.152 | PASS |
| 49 | How do I become a freight forwarder? | 04_internal_synthetic_service_terms | 0.130 | PASS |
| 50 | What are your competitor's rates? | 04_internal_synthetic_service_terms | -0.145 | PASS |

## Appendix: Full Results

```json
[
  {
    "query_num": 1,
    "category": "booking_documentation",
    "query": "What documents are needed for sea freight Singapore to Indonesia?",
    "top_result_doc_id": "01_regulatory_indonesia_import_requirements",
    "top_result_title": "Indonesia Import Requirements",
    "top_score": 0.3892,
    "hit": true,
    "expected_sources": [
      "sg_export",
      "indonesia_import"
    ],
    "matched_source": "indonesia_import",
    "top_5_chunks": [
      {
        "doc_id": "01_regulatory_indonesia_import_requirements",
        "title": "Indonesia Import Requirements",
        "section": "Key Regulatory Bodies",
        "similarity": 0.3892
      },
      {
        "doc_id": "02_carriers_pil_service_summary",
        "title": "PIL (Pacific International Lines) Service Summary",
        "section": "Singapore Office (Headquarters)",
        "similarity": 0.3069
      },
      {
        "doc_id": "03_reference_incoterms_2020_reference",
        "title": "Incoterms 2020 Complete Reference Guide",
        "section": "Key Changes in Incoterms 2020",
        "similarity": 0.2862
      },
      {
        "doc_id": "02_carriers_maersk_service_summary",
        "title": "Maersk Service Summary",
        "section": "Routes from Singapore",
        "similarity": 0.2783
      },
      {
        "doc_id": "01_regulatory_malaysia_import_requirements",
        "title": "Malaysia Import Requirements",
        "section": "Key Regulatory Bodies",
        "similarity": 0.2773
      }
    ]
  },
  {
    "query_num": 2,
    "category": "booking_documentation",
    "query": "How far in advance should I book an LCL shipment?",
    "top_result_doc_id": "04_internal_synthetic_service_terms_conditions",
    "top_result_title": "Service Terms and Conditions",
    "top_score": 0.0572,
    "hit": false,
    "expected_sources": [
      "booking"
    ],
    "matched_source": null,
    "top_5_chunks": [
      {
        "doc_id": "04_internal_synthetic_service_terms_conditions",
        "title": "Service Terms and Conditions",
        "section": "4. Booking and Cancellation",
        "similarity": 0.0572
      },
      {
        "doc_id": "04_internal_synthetic_sla_policy",
        "title": "Service Level Agreement (SLA) Policy",
        "section": "4. Response Time Standards",
        "similarity": 0.0321
      },
      {
        "doc_id": "04_internal_synthetic_sla_policy",
        "title": "Service Level Agreement (SLA) Policy",
        "section": "6. Issue Resolution SLAs",
        "similarity": -0.0064
      },
      {
        "doc_id": "04_internal_synthetic_cod_procedure",
        "title": "Collect on Delivery (COD) Handling Procedure",
        "section": "7. Collection Process",
        "similarity": -0.0925
      },
      {
        "doc_id": "04_internal_synthetic_sla_policy",
        "title": "Service Level Agreement (SLA) Policy",
        "section": "5. Operational SLAs",
        "similarity": -0.0979
      }
    ]
  },
  {
    "query_num": 3,
    "category": "
... (truncated)
```
