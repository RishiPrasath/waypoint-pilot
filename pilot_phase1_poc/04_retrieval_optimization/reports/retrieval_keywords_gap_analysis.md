# Retrieval Keywords Gap Analysis

**Date**: 2026-02-06
**Related Tasks**: Task 7.2 (KB Metadata Enhancement)
**Source**: KB Quality Audit findings (Issue #1)

---

## Problem Statement

22 of 30 KB documents (73%) are missing `retrieval_keywords` in their frontmatter. More critically, these documents lack synonym and abbreviation coverage **in their body content**, meaning the embedding model cannot match common query phrasings to the right documents.

## Root Cause: How the Pipeline Works

### Ingestion Flow

```
Markdown file → process_docs.py → chunker.py → ingest.py → ChromaDB
                     │                  │             │
              strips frontmatter   splits body    embeds chunk_text only
              extracts metadata    into chunks    stores metadata separately
```

1. **`process_docs.py`** calls `extract_content()` which returns only the body text below the `---` frontmatter block. The `retrieval_keywords` field is never read or extracted.
2. **`chunker.py`** splits the body text into ~600-character chunks using `RecursiveCharacterTextSplitter`.
3. **`ingest.py`** sends each `chunk_text` to ChromaDB for embedding via `all-MiniLM-L6-v2` (384-dimensional vectors). Metadata (`doc_id`, `title`, `category`, etc.) is stored alongside but **not embedded**.

### What Gets Embedded vs. What Doesn't

| Content | Embedded? | Searchable by vector similarity? |
|---------|:---------:|:--------------------------------:|
| Document body text (markdown after frontmatter) | ✅ Yes | ✅ Yes |
| `title` field | ❌ No (metadata only) | ❌ No |
| `retrieval_keywords` field | ❌ No (not even extracted) | ❌ No |
| Section headers (##, ###) | ✅ Yes (part of body) | ✅ Yes |

### The Embedding Model's Limitation

`all-MiniLM-L6-v2` is a general-purpose sentence transformer. It produces semantic embeddings but has no domain-specific knowledge of logistics abbreviations:

| Query Term | Document Term | Semantic Similarity | Problem |
|-----------|---------------|:-------------------:|---------|
| "BL" | "Bill of Lading" | LOW (~0.3) | Model doesn't know BL = Bill of Lading |
| "D&D" | "Demurrage and Detention" | LOW (~0.2) | Abbreviation not in model vocabulary |
| "DO" | "Delivery Order" | LOW (~0.25) | "DO" is ambiguous (verb vs. noun) |
| "SI" | "Shipping Instructions" | LOW (~0.2) | "SI" could mean many things |
| "duty rate" | "tariff" | MEDIUM (~0.5) | Related but not identical |
| "CO" | "Certificate of Origin" | LOW (~0.3) | Abbreviation gap |
| "VGM" | "Verified Gross Mass" | LOW (~0.15) | Technical abbreviation |
| "FOB" | "Free on Board" | LOW (~0.2) | Incoterm abbreviation |

When a customer service agent queries "What's the BL process for Maersk?" and the Maersk doc only says "Bill of Lading" in the body, the cosine similarity is lower than it should be, potentially pushing the correct document below the top-5 results.

## Impact on Retrieval Quality

### Documents at Risk

| Category | Docs Missing Keywords | Test Queries Affected |
|----------|:--------------------:|----------------------|
| 01_regulatory | 12/14 | #11 (GST), #12 (HS code), #13 (CO), #15 (ATIGA), #16 (FTZ), #19 (HS ruling), #20 (Form D/AK) |
| 02_carriers | 6/6 | #21-#30 (all carrier queries) |
| 03_reference | 3/3 | #3 (FCL/LCL), #8 (FOB), #20 (Form D/AK) |
| 04_internal | 3/7 | #10 (free time), #35 (duties), #37 (import permit) |

### Worst-Case Scenarios

1. **All 6 carrier docs** have no abbreviation coverage. Queries using "BL", "SI", "D&D", "DO", "VGM" may fail to retrieve the correct carrier document.
2. **All 3 reference docs** lack abbreviation mappings. "FOB", "CIF", "DDP" queries may not find the Incoterms reference.
3. **12 regulatory docs** missing keywords. "CO", "HS code", "FTA", "ROO" queries rely entirely on body text matching.

## Solution: Two-Layer Fix

### Layer 1: Body Content Enhancement (PRIMARY — fixes retrieval)

Add a "Key Terms and Abbreviations" section to each document body, immediately after the `# Title` heading. This section gets chunked and embedded like any other content.

**Template:**
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **BL / B/L** | Bill of Lading | Transport document issued by carrier |
| **SI** | Shipping Instructions | Submitted before vessel cutoff |
```

**Why this works:** The chunk containing this table will have high cosine similarity to BOTH the abbreviation ("BL") and the full term ("Bill of Lading"), acting as a bridge between how agents query and how documents are written.

**Why a table:** Tables chunk well with `RecursiveCharacterTextSplitter` — the entire table typically stays in one chunk (under 600 chars for 8-12 rows), keeping all term mappings together.

### Layer 2: Frontmatter Metadata (SECONDARY — for audit/future use)

Add `retrieval_keywords` to frontmatter for:
- **Tracking**: Acts as a checklist of "what queries should find this doc"
- **Future hybrid search**: If/when we add keyword-based retrieval alongside vector search
- **Debugging**: Can inspect which docs should have matched a failed query

This does NOT directly improve retrieval today because the field is not embedded or used in `collection.query()`.

## Scope of Work

### Per-Document Changes

| # | Change | Location | Impact |
|---|--------|----------|--------|
| 1 | Add `retrieval_keywords` list (8-15 terms) | Frontmatter | Audit/tracking |
| 2 | Add "Key Terms and Abbreviations" table (8-15 rows) | Body (after title) | **Fixes retrieval** |

### Documents Requiring Changes: 22

**01_regulatory (12 docs):**
sg_certificates_of_origin, asean_rules_of_origin, indonesia_import_requirements, thailand_import_requirements, vietnam_import_requirements, philippines_import_requirements, malaysia_import_requirements, sg_free_trade_zones, asean_tariff_finder_guide, sg_export_procedures, sg_import_procedures, sg_gst_guide

**02_carriers (6 docs):**
maersk_service_summary, pil_service_summary, one_service_summary, evergreen_service_summary, cathay_cargo_service_guide, sia_cargo_service_guide

**03_reference (3 docs):**
hs_code_structure_guide, incoterms_2020_reference, incoterms_comparison_chart

**04_internal_synthetic (1 doc):**
fta_comparison_matrix

### Documents to Verify (have keywords but may lack body terms): 8

atiga_overview, sg_hs_classification, booking_procedure, customer_faq, service_terms_conditions, sla_policy, cod_handling_procedure, escalation_procedure

## Keyword Reference by Category

### Carrier Documents — Common Terms
BL/B/L (Bill of Lading), SI (Shipping Instructions), D&D (Demurrage and Detention), DO (Delivery Order), VGM (Verified Gross Mass), FCL (Full Container Load), LCL (Less than Container Load), ETA (Estimated Time of Arrival), ETD (Estimated Time of Departure), TEU (Twenty-foot Equivalent Unit), EBL (Electronic Bill of Lading), LOI (Letter of Indemnity), LOA (Letter of Authorization), OOG (Out of Gauge), DG (Dangerous Goods)

### Regulatory Documents — Common Terms
HS code (Harmonized System), CO (Certificate of Origin), Form D (ATIGA Certificate of Origin), FTA (Free Trade Agreement), ROO (Rules of Origin), RVC (Regional Value Content), CTC (Change in Tariff Classification), MFN (Most Favoured Nation), GST (Goods and Services Tax), ATIGA (ASEAN Trade in Goods Agreement), RCEP (Regional Comprehensive Economic Partnership), NTP (Networked Trade Platform), TradeNet, FTZ (Free Trade Zone), IGDS (Import GST Deferment Scheme), MES (Major Exporter Scheme)

### Reference Documents — Common Terms
FOB (Free on Board), CIF (Cost Insurance Freight), DDP (Delivered Duty Paid), EXW (Ex Works), DAP (Delivered at Place), FCA (Free Carrier), CFR (Cost and Freight), CPT (Carriage Paid To), UN number, packing group, hazard class, IMDG (International Maritime Dangerous Goods)

### Internal Documents — Common Terms
SLA (Service Level Agreement), KPI (Key Performance Indicator), COD (Cash on Delivery), POD (Proof of Delivery), TAT (Turnaround Time), cutoff, free time, laytime

## Estimated Effort

| Task | Count | Time per doc | Total |
|------|:-----:|:------------:|:-----:|
| Generate keyword lists (22 docs) | 22 | ~3 min | ~1 hour |
| Add Key Terms section to body (22 docs) | 22 | ~3 min | ~1 hour |
| Verify 8 existing docs have terms in body | 8 | ~2 min | ~15 min |
| Total | 30 | — | **~2.25 hours** |

## Success Criteria

After Task 7.2, re-run ingestion and retrieval test:
- All 30 docs should have `retrieval_keywords` in frontmatter
- All 30 docs should have "Key Terms" section in body
- No regression in adjusted hit rate (must stay ≥82%)
- Expected improvement: 82% → 88-92% adjusted
