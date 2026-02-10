# Knowledge Base — 30 Documents, 709 Chunks

Curated knowledge base for the Waypoint freight forwarding co-pilot. Covers Singapore customs regulations, carrier services, trade references, and internal procedures.

> **Frozen for evaluation. Do not modify content.**

## Structure

| Directory | Docs | Scope |
|-----------|------|-------|
| `01_regulatory/` | 14 | Singapore Customs, ASEAN trade, country import requirements |
| `02_carriers/` | 6 | Ocean (Maersk, Evergreen, ONE, PIL) and Air (SIA Cargo, Cathay) |
| `03_reference/` | 3 | Incoterms 2020, HS code classification |
| `04_internal_synthetic/` | 6 | Booking, escalation, COD procedures, FAQ, SLA, T&C |

Each directory also contains a `pdfs/` subfolder with extracted PDF reference material.
These PDF extracts are **not ingested** — their content has been merged into the main documents.

## Document Format

All documents use YAML frontmatter with standardized metadata:
- `title`, `source_org`, `source_type`, `jurisdiction`, `category`
- `source_urls`, `last_updated`, `use_cases`

## Ingestion Stats

- **30 documents** ingested (pdfs/ excluded)
- **709 chunks** at 600 chars / 90 overlap
- **92% retrieval hit rate** (98% adjusted)
- Embedding: all-MiniLM-L6-v2 (384-d via ONNX)

## Detailed Docs

See [architecture docs](../documentation/architecture/kb_schema.md) for schema details, metadata fields, and document sourcing methodology.
