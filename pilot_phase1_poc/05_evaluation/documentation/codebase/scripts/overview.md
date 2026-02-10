# Scripts Overview

Layer 3 documentation for all Python scripts in the Waypoint Co-Pilot pipeline.

---

## Runtime Environment

| Property | Value |
|----------|-------|
| Language | Python 3.11+ |
| Virtual Environment | `venv/` (per workspace) |
| Activation | `venv/Scripts/activate` (Windows) |
| Package Manager | pip with `requirements.txt` |

---

## Script Categories

### Ingestion Pipeline

| Script | Purpose | Entry Point |
|--------|---------|-------------|
| `ingest.py` | Orchestrates full ingestion: discover, parse, chunk, embed, store | `python scripts/ingest.py` |
| `process_docs.py` | Discovers markdown files and parses YAML frontmatter into structured dicts | Module import or `python -m scripts.process_docs` |
| `chunker.py` | Splits documents into semantic chunks preserving metadata and section context | Module import or `python -m scripts.chunker` |
| `config.py` | Central configuration: paths, chunk params, collection name, logging | Module import only |

### Query Bridge

| Script | Purpose | Entry Point |
|--------|---------|-------------|
| `query_chroma.py` | JSON stdin/stdout bridge for Node.js backend to query ChromaDB | `echo '{"query":"..."}' \| python scripts/query_chroma.py` |

### Testing

| Script | Purpose | Entry Point |
|--------|---------|-------------|
| `retrieval_quality_test.py` | 50-query hit rate test against ChromaDB with per-category reporting | `python scripts/retrieval_quality_test.py` |
| `evaluation_harness.py` | Sends 50 queries to live API, checks against baselines, generates reports | `python scripts/evaluation_harness.py` |

### Utilities

| Script | Purpose | Entry Point |
|--------|---------|-------------|
| `verify_ingestion.py` | Post-ingestion validation: chunk count, categories, metadata, retrieval tiers | `python -m scripts.verify_ingestion` |
| `view_chroma.py` | Debug utility to inspect ChromaDB collection contents | `python -m scripts.view_chroma` |
| `pdf_extractor.py` | Converts PDF files to markdown with frontmatter templates | `python scripts/pdf_extractor.py <file.pdf>` |

### Configuration

| Script | Purpose |
|--------|---------|
| `config.py` | Loads `.env`, resolves paths relative to `PIPELINE_ROOT`, exports all constants |

---

## Common Patterns

### Path Resolution

All scripts resolve paths relative to `PIPELINE_ROOT`, which is computed as:

```python
PIPELINE_ROOT = Path(__file__).parent.parent.resolve()
```

This means `PIPELINE_ROOT` points to the workspace root (e.g., `05_evaluation/`), and all other paths are derived from it:

- `CHROMA_PERSIST_PATH` = `PIPELINE_ROOT / "chroma_db"`
- `KNOWLEDGE_BASE_PATH` = `PIPELINE_ROOT / "kb"`
- `LOG_DIR` = `PIPELINE_ROOT / "logs"`

### Configuration Import

Every script that needs paths, chunk parameters, or collection names imports from `config.py`:

```python
from scripts.config import CHROMA_PERSIST_PATH, COLLECTION_NAME, CHUNK_SIZE
```

### sys.path Setup

Scripts that serve as direct entry points (not just module imports) add the parent directory to `sys.path` so that `from scripts.config import ...` works:

```python
sys.path.insert(0, str(Path(__file__).parent.parent))
```

This is present in `ingest.py`, `verify_ingestion.py`, `pdf_extractor.py`, `evaluation_harness.py`, and `retrieval_quality_test.py`.

### ChromaDB Initialization

All scripts that interact with ChromaDB follow the same pattern:

```python
client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_PATH))
embedding_fn = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_fn
)
```

The default embedding function uses all-MiniLM-L6-v2 via ONNX, producing 384-dimensional vectors. No API key is required.

---

## Dependencies

| Package | Version | Used By |
|---------|---------|---------|
| `chromadb` | 0.5.23 | ingest, query_chroma, verify_ingestion, view_chroma, retrieval_quality_test |
| `python-frontmatter` | - | process_docs |
| `langchain-text-splitters` | - | chunker |
| `requests` | - | evaluation_harness |
| `python-dotenv` | - | config |
| `pymupdf4llm` | - | pdf_extractor |
| `PyMuPDF` (fitz) | - | pdf_extractor |
| `pyyaml` | - | pdf_extractor (frontmatter generation) |

Install all dependencies:

```bash
cd pilot_phase1_poc/05_evaluation
py -3.11 -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```

---

## Data Flow

```
kb/*.md
  |
  v
process_docs.py  -->  discover_documents()  -->  parse_document()
  |
  v
chunker.py       -->  chunk_document()  -->  chunk_all_documents()
  |
  v
ingest.py        -->  ingest_document()  -->  ChromaDB (chroma_db/)
  |
  v
query_chroma.py  <--  Node.js backend (stdin JSON)  -->  stdout JSON
  |
  v
evaluation_harness.py  -->  POST /api/query  -->  evaluation reports
```

---

## Quick Reference Commands

```bash
# Full ingestion (clear and re-ingest)
python scripts/ingest.py --clear

# Dry run (process without storing)
python scripts/ingest.py --dry-run

# Verify ingestion quality
python -m scripts.verify_ingestion --verbose

# View ChromaDB contents
python -m scripts.view_chroma
python -m scripts.view_chroma --search "customs"

# Run retrieval quality test (50 queries)
python scripts/retrieval_quality_test.py

# Run evaluation harness (requires live backend on port 3000)
python scripts/evaluation_harness.py --delay 10

# Extract a PDF to markdown
python scripts/pdf_extractor.py path/to/file.pdf
```
