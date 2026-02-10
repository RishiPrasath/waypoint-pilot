# Scripts — Python Ingestion, Retrieval, and Evaluation

Python scripts for document ingestion into ChromaDB, retrieval quality testing, and automated evaluation harness. Uses all-MiniLM-L6-v2 embeddings (384-d) with chunk size 600 / overlap 90.

## File Structure

| File | Purpose |
|------|---------|
| `config.py` | Paths, chunk params, collection name, thresholds |
| `ingest.py` | Main ingestion entry point (--clear, --dry-run, --verbose) |
| `process_docs.py` | Document discovery, frontmatter parsing, body extraction |
| `chunker.py` | Text chunking with overlap and metadata propagation |
| `pdf_extractor.py` | PDF-to-markdown extraction (reference material) |
| `query_chroma.py` | ChromaDB query interface (reads JSON from stdin) |
| `retrieval_quality_test.py` | 50-query retrieval hit rate test suite |
| `evaluation_harness.py` | Full pipeline evaluation (deflection, citation, hallucination) |
| `verify_ingestion.py` | Post-ingestion chunk count and metadata validation |
| `view_chroma.py` | ChromaDB collection inspector / debug viewer |

## Quick Start

```bash
cd pilot_phase1_poc/05_evaluation
venv\Scripts\activate                       # Windows

python scripts/ingest.py --clear            # Full re-ingestion
python scripts/ingest.py --dry-run          # Test without storing
python scripts/retrieval_quality_test.py    # Retrieval hit rate
python scripts/evaluation_harness.py        # Full evaluation suite
python scripts/verify_ingestion.py          # Validate chunk counts
```

## Key Configuration

- **KB path**: `kb/` (30 docs, pdfs/ excluded from ingestion)
- **ChromaDB**: `chroma_db/` (709 chunks, collection `waypoint_kb`)
- **Chunk size**: 600 chars / 90 overlap

## Detailed Docs

See [detailed documentation](../documentation/codebase/scripts/overview.md) for pipeline flow, configuration options, and script interactions.
