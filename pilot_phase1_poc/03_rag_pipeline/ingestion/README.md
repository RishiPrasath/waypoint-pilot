# Waypoint Ingestion Pipeline

Document ingestion pipeline for the Waypoint RAG-based customer service co-pilot. Processes markdown documents from the knowledge base, chunks them, generates embeddings, and stores them in ChromaDB for semantic retrieval.

## Overview

The pipeline processes 29 curated knowledge base documents covering:
- **Regulatory**: Singapore Customs, ASEAN trade regulations (14 docs)
- **Carriers**: Ocean and air carrier service guides (6 docs)
- **Reference**: Incoterms, HS codes (3 docs)
- **Internal**: Policies, procedures, service guides (6 docs)

### Key Features
- Chunking with semantic boundaries (600 chars, 15% overlap)
- ChromaDB default embeddings (all-MiniLM-L6-v2, 384 dimensions)
- 10 metadata fields per chunk for filtering and attribution
- Verification script with 33 retrieval tests

## Prerequisites

- Python 3.11+ (ChromaDB doesn't support Python 3.14 yet)
- 500MB disk space for dependencies and vector database

## Quick Start

```bash
cd pilot_phase1_poc/02_ingestion_pipeline

# Create virtual environment
py -3.11 -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Unix/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run ingestion
python -m scripts.ingest

# Verify ingestion quality
python -m scripts.verify_ingestion
```

## Usage

### Ingestion Commands

```bash
# Full ingestion (clears existing data)
python -m scripts.ingest --clear

# Dry run (process without storing)
python -m scripts.ingest --dry-run

# Verbose output (show chunk details)
python -m scripts.ingest --verbose

# Single category only
python -m scripts.ingest --category 01_regulatory
python -m scripts.ingest --category 02_carriers
python -m scripts.ingest --category 03_reference
python -m scripts.ingest --category 04_internal_synthetic
```

### Verification Commands

```bash
# Run all 6 checks
python -m scripts.verify_ingestion

# Verbose output (show individual query results)
python -m scripts.verify_ingestion --verbose

# Run specific tier only
python -m scripts.verify_ingestion --tier 1
python -m scripts.verify_ingestion --tier 2
python -m scripts.verify_ingestion --tier 3

# Run specific check only
python -m scripts.verify_ingestion --check 1  # Total count
python -m scripts.verify_ingestion --check 2  # Category distribution
python -m scripts.verify_ingestion --check 3  # Metadata integrity
python -m scripts.verify_ingestion --check 4  # Tier 1 retrieval
python -m scripts.verify_ingestion --check 5  # Tier 2 retrieval
python -m scripts.verify_ingestion --check 6  # Tier 3 scenarios
```

### Running Tests

```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_verify_ingestion.py -v
python -m pytest tests/test_ingest.py -v
python -m pytest tests/test_chunker.py -v
python -m pytest tests/test_process_docs.py -v
```

## Configuration

Environment variables are loaded from `.env` (copy from `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `CHROMA_PERSIST_PATH` | `./chroma_db` | ChromaDB storage directory |
| `KNOWLEDGE_BASE_PATH` | `../01_knowledge_base/kb` | Knowledge base documents |
| `COLLECTION_NAME` | `waypoint_kb` | ChromaDB collection name |
| `EMBEDDING_MODEL` | `default` | ChromaDB built-in embeddings |
| `EMBEDDING_DIMENSIONS` | `384` | Embedding vector size |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

### Chunking Settings (in config.py)

| Setting | Value | Description |
|---------|-------|-------------|
| `CHUNK_SIZE` | 600 | Characters per chunk (~150 tokens) |
| `CHUNK_OVERLAP` | 90 | Overlap between chunks (15%) |
| `SEPARATORS` | `["\n## ", "\n### ", "\n\n", "\n"]` | Split priorities |

## Verification Checks

The verification script runs 6 progressive quality checks:

| Check | Description | Pass Criteria |
|-------|-------------|---------------|
| 1 | Total chunk count | 450-520 chunks |
| 2 | Category distribution | All 4 categories present |
| 3 | Metadata integrity | 10/10 fields in samples |
| 4 | Tier 1: Category retrieval | 8/8 queries |
| 5 | Tier 2: Document retrieval | 10+/12 queries |
| 6 | Tier 3: Keyword matching | 8+/10 queries |

**Target**: 28+/30 tests pass (93%+)

### Sample Verification Output

```
==================================================
Waypoint Ingestion Verification
==================================================

[PASS] Check 1: Total count: 483 chunks (expected 450-520)
[PASS] Check 2: Category distribution: 4/4 categories
[PASS] Check 3: Metadata integrity: 10/10 fields
[PASS] Check 4: Tier 1 retrieval: 8/8
[PASS] Check 5: Tier 2 retrieval: 12/12
[PASS] Check 6: Tier 3 scenarios: 10/10

Summary: 33/33 tests passed (100%)
Result: VERIFICATION PASSED
```

## Architecture

```
Knowledge Base (29 docs)
        |
        v
+-------------------+
| Document Processor|  scripts/process_docs.py
| - Discover docs   |  - Finds all .md files
| - Parse YAML      |  - Extracts frontmatter
| - Extract content |  - Separates metadata/content
+-------------------+
        |
        v
+-------------------+
| Chunking Engine   |  scripts/chunker.py
| - Split by headers|  - Respects ## and ### boundaries
| - 600 char chunks |  - 90 char overlap
| - Add metadata    |  - 10 fields per chunk
+-------------------+
        |
        v
+-------------------+
| ChromaDB Storage  |  scripts/ingest.py
| - Default embed   |  - all-MiniLM-L6-v2 (384-d)
| - Persist to disk |  - ./chroma_db/
| - Collection: kb  |  - waypoint_kb
+-------------------+
        |
        v
+-------------------+
| Verification      |  scripts/verify_ingestion.py
| - Count checks    |  - 450-520 chunks
| - Category checks |  - 4 categories
| - Retrieval tests |  - 30 semantic queries
+-------------------+
```

## Project Structure

```
02_ingestion_pipeline/
├── scripts/
│   ├── __init__.py
│   ├── config.py           # Configuration module
│   ├── process_docs.py     # Document discovery and parsing
│   ├── chunker.py          # Text chunking with metadata
│   ├── ingest.py           # Main ingestion orchestrator
│   └── verify_ingestion.py # Quality verification
├── tests/
│   ├── __init__.py
│   ├── test_process_docs.py
│   ├── test_chunker.py
│   ├── test_ingest.py
│   └── test_verify_ingestion.py
├── chroma_db/              # Vector database (auto-created)
├── logs/                   # Log files (auto-created)
├── docs/                   # Planning documents
├── prompts/                # PCTF task prompts
├── .env                    # Environment config
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Metadata Fields

Each chunk includes 10 metadata fields:

| Field | Source | Example |
|-------|--------|---------|
| `doc_id` | Derived from filename | `sg_import_procedures` |
| `title` | Frontmatter | `Singapore Import Procedures` |
| `source_org` | Frontmatter | `Singapore Customs` |
| `source_type` | Frontmatter | `public_regulatory` |
| `jurisdiction` | Frontmatter | `SG` |
| `category` | Directory path | `01_regulatory` |
| `section_header` | Extracted from `##` | `Required Documents` |
| `subsection_header` | Extracted from `###` | `Commercial Invoice` |
| `chunk_index` | Generated | `3` |
| `file_path` | Full path | `/path/to/doc.md` |

## Troubleshooting

### ChromaDB Telemetry Errors

```
Failed to send telemetry event: capture() takes 1 positional argument...
```

These are harmless telemetry errors and don't affect functionality. To disable telemetry:

```python
import chromadb
from chromadb.config import Settings
client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(anonymized_telemetry=False)
)
```

### Python Version Issues

ChromaDB requires Python 3.11 or 3.12. If you have multiple Python versions:

```bash
# Windows
py -3.11 -m venv venv

# Unix/macOS
python3.11 -m venv venv
```

### Collection Not Found

If verification fails with "collection not found":

```bash
# Re-run ingestion
python -m scripts.ingest --clear
```

### Import Errors

Ensure you're running from the `02_ingestion_pipeline` directory:

```bash
cd pilot_phase1_poc/02_ingestion_pipeline
python -m scripts.ingest  # Use -m syntax
```

### Low Retrieval Scores

If Tier 1/2/3 tests fail, the knowledge base content may have changed. Re-run ingestion and adjust test queries in `verify_ingestion.py` if needed.

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| chromadb | 0.5.23 | Vector database with default embeddings |
| python-frontmatter | 1.1.0 | YAML frontmatter parsing |
| langchain-text-splitters | 0.0.1 | Semantic text chunking |
| pyyaml | 6.0.1 | YAML parsing |
| python-dotenv | 1.0.0 | Environment variable loading |
| pytest | 9.0.2 | Testing framework |

## License

Internal use only - Waypoint Phase 1 POC
