# Knowledge Base Schema

## Overview

The knowledge base consists of 30 curated markdown documents covering freight forwarding topics for Singapore and Southeast Asia. Documents use YAML frontmatter for metadata and are organized into category folders.

## YAML Frontmatter Schema

Every KB document begins with a YAML frontmatter block:

```yaml
---
title: "Singapore Import Procedures"          # string (required) — Document title
source_org: "Singapore Customs"                # string (required) — Organization name
source_urls:                                    # list[string] (required) — Primary source URLs
  - "https://www.customs.gov.sg/businesses/importing-goods/overview"
source_type: "public_regulatory"                # enum (required) — See values below
last_updated: "2025-01-15"                      # date (required) — YYYY-MM-DD format
jurisdiction: "SG"                              # enum (required) — See values below
category: "customs"                             # enum (required) — See values below
use_cases:                                      # list[string] (optional) — Use case IDs
  - "UC-1.1"
  - "UC-1.2"
retrieval_keywords:                             # list[string] (optional) — See note below
  - "import"
  - "GST"
  - "permit"
---
```

### Field Details

| Field | Type | Required | Values |
|-------|------|----------|--------|
| `title` | string | Yes | Document title for display and citation matching |
| `source_org` | string | Yes | e.g., `"Singapore Customs"`, `"Maersk"`, `"Waypoint (Internal)"` |
| `source_urls` | list[string] | Yes | Primary URLs; may also accept `[{url, label}]` objects |
| `source_type` | enum | Yes | `public_regulatory` \| `public_carrier` \| `synthetic_internal` |
| `last_updated` | date | Yes | ISO format `YYYY-MM-DD` |
| `jurisdiction` | enum | Yes | `SG` \| `MY` \| `ID` \| `TH` \| `VN` \| `PH` \| `ASEAN` \| `Global` |
| `category` | enum | Yes | `customs` \| `carrier` \| `policy` \| `procedure` \| `reference` |
| `use_cases` | list[string] | No | IDs from the use case document (e.g., `UC-1.1`, `UC-2.3`) |
| `retrieval_keywords` | list[string] | No | **Not embedded** — see important note below |

> **Important**: `retrieval_keywords` in frontmatter are stored as ChromaDB metadata but are **not embedded**. The ingestion pipeline strips frontmatter before embedding — only body text gets embedded. To improve retrieval for specific terms, add them to the document body (e.g., in a "Key Terms" section).

## Category Folder Structure

```
kb/
├── 01_regulatory/          # 14 documents — Singapore Customs, ASEAN trade regulations
│   ├── sg_import_procedures.md
│   ├── sg_export_procedures.md
│   ├── sg_customs_permits.md
│   ├── sg_gst_imports.md
│   ├── sg_prohibited_controlled_goods.md
│   ├── sg_free_trade_zones.md
│   ├── sg_customs_valuation.md
│   ├── sg_rules_of_origin.md
│   ├── sg_trade_compliance.md
│   ├── asean_trade_regulations.md
│   ├── asean_customs_transit.md
│   ├── asean_tariff_classification.md
│   ├── dangerous_goods_regulations.md
│   ├── cold_chain_logistics.md
│   └── pdfs/               # Reference PDFs (NOT ingested)
│
├── 02_carriers/            # 6 documents — Ocean and air carrier information
│   ├── maersk_services.md
│   ├── msc_services.md
│   ├── one_services.md
│   ├── pil_services.md
│   ├── evergreen_services.md
│   ├── air_cargo_carriers.md
│   └── pdfs/               # Reference PDFs (NOT ingested)
│
├── 03_reference/           # 3 documents — Trade reference material
│   ├── incoterms_2020.md
│   ├── hs_code_guide.md
│   ├── fta_comparison.md
│   └── pdfs/               # Reference PDFs (NOT ingested)
│
└── 04_internal_synthetic/  # 6 documents — Company policies and procedures
    ├── booking_procedure.md
    ├── documentation_checklist.md
    ├── service_terms.md
    ├── sla_policy.md
    ├── escalation_matrix.md
    └── faq.md
```

### Category Details

| Category | Folder | Count | Content |
|----------|--------|-------|---------|
| Regulatory | `01_regulatory/` | 14 | Singapore Customs procedures, GST, permits, ASEAN trade, DG regs |
| Carriers | `02_carriers/` | 6 | Ocean carrier services (Maersk, MSC, ONE, PIL, Evergreen) + air cargo |
| Reference | `03_reference/` | 3 | Incoterms 2020, HS code classification, FTA comparison |
| Internal | `04_internal_synthetic/` | 6 | Company booking procedures, SLAs, escalation, FAQ |

### PDF Subdirectories

Each category folder may contain a `pdfs/` subdirectory with reference PDFs. These are **excluded** from ingestion by `discover_documents()` — their content has been selectively merged into the main markdown documents during KB curation.

## ChromaDB Chunk Metadata

Each chunk stored in ChromaDB carries 13 metadata fields:

| Field | Type | Description |
|-------|------|-------------|
| `doc_id` | string | Unique document ID (`{category}_{filename}`) |
| `title` | string | Document title from frontmatter |
| `source_org` | string | Source organization |
| `source_type` | string | Document type enum |
| `jurisdiction` | string | Jurisdiction code |
| `category` | string | Category folder name (e.g., `01_regulatory`) |
| `section_header` | string | Nearest `##` header above the chunk |
| `subsection_header` | string | Nearest `###` header above the chunk |
| `chunk_index` | int | Zero-based position within the document |
| `file_path` | string | Absolute path to source file |
| `source_urls` | string | Comma-joined list of URLs |
| `retrieval_keywords` | string | Comma-joined list of keywords |
| `use_cases` | string | Comma-joined list of use case IDs |

Note: `source_urls`, `retrieval_keywords`, and `use_cases` are stored as comma-joined strings because ChromaDB metadata only supports scalar types.

## How to Add a New Document

1. **Create the markdown file** with YAML frontmatter following the schema above
2. **Place it in the correct category folder** under `kb/`
3. **Ensure key terms appear in the body text** — frontmatter keywords are not embedded
4. **Run ingestion** to rebuild the vector store:
   ```bash
   python scripts/ingest.py --clear
   ```
5. **Verify** the new document was ingested:
   ```bash
   python scripts/verify_ingestion.py
   ```
6. **Test retrieval** with relevant queries to confirm the document is discoverable

## KB Statistics

| Metric | Value |
|--------|-------|
| Total documents | 30 |
| Total chunks | 709 |
| Average chunks per document | ~23.6 |
| Retrieval hit rate (50-query test) | 92% |
| Embedding dimensions | 384 |
| Chunk size | 600 characters |
| Chunk overlap | 90 characters (15%) |

## Related Documentation

- [Ingestion Pipeline Flow](ingestion_pipeline_flow.md) — How documents are processed and chunked
- [System Overview](system_overview.md) — Tech stack and component diagram
- See [ingestion.md](../codebase/scripts/ingestion.md) for function-level details
