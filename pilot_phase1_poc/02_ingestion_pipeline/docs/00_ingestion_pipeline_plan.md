# Waypoint Document Ingestion Pipeline Plan

**Project**: Waypoint Phase 1 POC  
**Phase**: W2 - RAG Pipeline Development  
**Focus**: Document Ingestion Pipeline  
**Date**: January 2025

---

## Executive Summary

This plan details the implementation of the document ingestion pipeline for Waypoint, transforming 29 curated knowledge base documents into a searchable vector store. The pipeline will parse YAML frontmatter, chunk documents uniformly, generate embeddings using ChromaDB's built-in default embeddings (all-MiniLM-L6-v2 via ONNX), and store them in ChromaDB with rich metadata for accurate citation retrieval.

**Key Deliverables**:
- Fully functional Python ingestion pipeline
- Local venv execution (no Docker required)
- ~350-400 chunks indexed in ChromaDB
- Metadata-rich storage enabling 80% citation accuracy target
- Verification scripts confirming data integrity

---

## Current State Assessment

### Knowledge Base Inventory

| Category | Path | Documents | Avg Size | Purpose |
|----------|------|-----------|----------|---------|
| Regulatory | `01_regulatory/` | 14 | 5,460 chars | Singapore Customs, ASEAN trade, country-specific requirements |
| Carriers | `02_carriers/` | 6 | 7,439 chars | Ocean (PIL, Maersk, ONE, Evergreen) and Air (SIA, Cathay) |
| Reference | `03_reference/` | 3 | 12,054 chars | Incoterms, HS codes |
| Internal Synthetic | `04_internal_synthetic/` | 6 | 9,251 chars | Policies, procedures, service guides |
| **Total** | | **29** | **212,754 chars** | |

---

## Key Technical Decisions

### Embedding Model: ChromaDB Default (ONNX)

| Attribute | Value |
|-----------|-------|
| Dimensions | 384 |
| Provider | ChromaDB built-in (ONNX runtime) |
| Model | all-MiniLM-L6-v2 |
| Requirement | None (offline capable, no API key) |

### Chunking Strategy: Uniform 600 chars

```python
CHUNKING_CONFIG = {
    "chunk_size": 600,      # chars (~150 tokens)
    "chunk_overlap": 90,    # 15% overlap
    "separators": ["\n## ", "\n### ", "\n\n", "\n"]
}
```

**Data-Driven Rationale**:
- Total documents: 29
- Total characters: 212,754 (~368 chunks at 600 chars)
- Average section size: 657 chars (600 chars keeps most sections intact)
- Total sections: 324 (one chunk ≈ one concept)

### Chunk Metadata Schema (12 fields)

```python
{
    # Core Metadata
    "doc_id": "sg_export_procedures",
    "doc_title": "Singapore Export Procedures",
    "source_org": "Singapore Customs",
    "source_urls": "[\"https://...\"]",  # JSON array
    "category": "01_regulatory",
    "chunk_index": 3,
    "total_chunks": 8,
    
    # Extended Metadata
    "section_header": "Required Steps",      # Nearest H2
    "subsection_header": "Step 1: Register", # Nearest H3/H4
    "use_cases": "UC-1.1,UC-2.1",
    "jurisdiction": "SG",
    "last_updated": "2025-01-22",
    "source_type": "public_regulatory"
}
```

---

## Confirmed Decisions

| Decision | Choice |
|----------|--------|
| Folder structure | `pilot_phase1_poc/02_ingestion_pipeline/` |
| Python environment | Local venv (Python 3.11+) |
| Python version | 3.11+ |
| Embedding model | ChromaDB default (all-MiniLM-L6-v2 via ONNX) |
| Chunk size | 600 chars uniform |
| Chunk overlap | 90 chars (15%) |
| Metadata fields | All extended fields (12 total) |
| Source URL storage | JSON array (all URLs preserved) |
| Section headers | Both H2 (`section_header`) + H3/H4 (`subsection_header`) |
| Document ID | Filename without extension |
| Chunk ID format | Zero-padded with label (`sg_export_procedures_chunk_003`) |
| Logging level | Standard + `--verbose` flag |
| Error handling | Skip failed documents and continue |
| Re-ingestion | Clear and rebuild from scratch |
| CLI arguments | `--verbose`, `--dry-run`, `--category <n>` |
| Verification tests | 30 queries across 3 tiers |
| Implementation | Incremental (build one script, verify, then next) |

---

## Deliverables

| # | File | Description |
|---|------|-------------|
| 1 | `config.py` | Centralized configuration |
| 2 | `process_docs.py` | Document parser with frontmatter extraction |
| 3 | `chunker.py` | Chunking logic with section header extraction |
| 4 | `ingest.py` | Main ingestion orchestrator |
| 5 | `verify_ingestion.py` | Post-ingestion validation with 30 test queries |
| 6 | `requirements.txt` | Python dependencies |
| 7 | `.env.example` | Environment template |
| 8 | `README.md` | Pipeline documentation |

---

## Verification Test Plan (30 queries)

### Tier 1: Category Retrieval (8 queries)
| Query | Expected Category |
|-------|-------------------|
| "Singapore export permit requirements" | 01_regulatory |
| "Indonesia LARTAS restricted goods" | 01_regulatory |
| "Maersk container shipping routes Asia" | 02_carriers |
| "Cathay Cargo air freight services" | 02_carriers |
| "FOB Incoterms seller responsibility" | 03_reference |
| "HS code structure 6 digits" | 03_reference |
| "escalation procedure priority levels" | 04_internal_synthetic |
| "SLA response time standards" | 04_internal_synthetic |

### Tier 2: Document Retrieval (12 queries)
| Query | Expected Document |
|-------|-------------------|
| "GST calculation CIF value Singapore" | sg_gst_guide.md |
| "Free Trade Zone storage regulations" | sg_free_trade_zones.md |
| "TradeNet permit application" | sg_export_procedures.md |
| "Malaysia de minimis threshold" | malaysia_import_requirements.md |
| "Vietnam import licensing MoIT" | vietnam_import_requirements.md |
| "ATIGA 40% regional value content" | atiga_overview.md |
| "PIL Pacific International Lines Singapore" | pil_service_summary.md |
| "ONE Ocean Network Express container" | one_service_summary.md |
| "DDP delivered duty paid customs" | incoterms_2020_reference.md |
| "Form D vs Form E certificate origin" | sg_certificates_of_origin.md |
| "booking cancellation policy charges" | booking_procedure.md |
| "COD collect on delivery handling" | cod_procedure.md |

### Tier 3: Use Case Scenarios (10 queries)
| Query | Use Case |
|-------|----------|
| "What documents needed for FCL export Singapore to Jakarta?" | UC-1.1 |
| "Customer asking about CIF vs FOB difference" | UC-1.3 |
| "Is Certificate of Origin required for Thailand shipment?" | UC-2.3 |
| "How to find HS code for electronics?" | UC-2.2 |
| "What's GST rate on imports and any exemptions?" | UC-2.1 |
| "Which carriers have direct service to Vietnam?" | UC-3.1 |
| "Maersk vs PIL for Southeast Asia routes" | UC-3.2 |
| "What's our standard response time for urgent queries?" | UC-4.1 |
| "When should I escalate a customer complaint?" | UC-4.3 |
| "ASEAN tariff finder how to check duty rates?" | UC-2.2 |

---

## Success Criteria

- [ ] All 29 documents successfully parsed
- [ ] ~350-400 chunks generated with proper metadata
- [ ] ChromaDB populated and persistent
- [ ] Tier 1 tests: 8/8 pass
- [ ] Tier 2 tests: 10+/12 pass
- [ ] Source URLs preserved in chunk metadata
- [ ] Python venv runs full pipeline successfully
- [ ] ChromaDB default generates 384-d embeddings

---

*See 01_implementation_roadmap.md for detailed task breakdown*
