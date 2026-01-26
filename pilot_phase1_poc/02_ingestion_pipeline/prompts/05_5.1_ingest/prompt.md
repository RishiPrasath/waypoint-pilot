# Task 5.1: Create Main Ingestion Script

## Persona

> You are a Python developer building production-ready data pipelines.
> You follow TDD practices - writing tests first, then implementation.
> You prioritize clear CLI interfaces, robust error handling, and informative logging.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. The ingestion script is the main entry point that orchestrates the entire pipeline: discovering documents, parsing, chunking, embedding, and storing in ChromaDB.

### Current State
- ✅ `scripts/config.py` - Configuration module
- ✅ `scripts/process_docs.py` - Document processor (29 docs, 185K chars)
- ✅ `scripts/chunker.py` - Chunking engine (483 chunks)
- ✅ `tests/test_process_docs.py` - 33 tests
- ✅ `tests/test_chunker.py` - 29 tests
- 📁 ChromaDB configured with default embeddings (all-MiniLM-L6-v2, 384-d)

### Reference Documents
- Roadmap: `docs/01_implementation_roadmap.md`
- Config: `scripts/config.py`
- Process docs: `scripts/process_docs.py`
- Chunker: `scripts/chunker.py`

### Dependencies
- Task 4.1 (chunker.py) ✅ Complete
- Task 4.2 (test_chunker.py) ✅ Complete
- ChromaDB with default embeddings

---

## Task

### Objective
Create `scripts/ingest.py` - the main CLI script that orchestrates the full ingestion pipeline. Follow TDD - write tests first in `tests/test_ingest.py`.

### Requirements

1. **CLI Interface** (using argparse)
   ```bash
   python scripts/ingest.py [OPTIONS]

   Options:
     --verbose, -v     Show detailed chunk information
     --dry-run, -d     Process without storing to ChromaDB
     --category CAT    Only process specific category (e.g., 01_regulatory)
     --clear           Clear existing collection before ingesting
   ```

2. **`initialize_chromadb() -> tuple[Client, Collection]`**
   - Create persistent ChromaDB client
   - Get or create collection with default embedding function
   - Return client and collection objects

3. **`ingest_document(doc: dict, collection, dry_run: bool, verbose: bool) -> int`**
   - Chunk the document
   - Add chunks to collection (unless dry_run)
   - Return number of chunks ingested
   - Log progress

4. **`run_ingestion(args) -> dict`**
   - Main orchestration function
   - Discover and parse documents
   - Filter by category if specified
   - Clear collection if --clear flag
   - Process each document
   - Handle failures gracefully
   - Return summary stats

5. **`main()`**
   - Parse CLI arguments
   - Setup logging
   - Run ingestion
   - Print summary

### ChromaDB Integration

```python
import chromadb
from chromadb.utils import embedding_functions

# Initialize client with persistence
client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_PATH))

# Get default embedding function (all-MiniLM-L6-v2, 384-d)
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

# Get or create collection
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_fn,
    metadata={"description": "Waypoint knowledge base"}
)

# Add chunks to collection
collection.add(
    ids=[chunk["chunk_id"] for chunk in chunks],
    documents=[chunk["chunk_text"] for chunk in chunks],
    metadatas=[{
        "doc_id": chunk["doc_id"],
        "title": chunk["title"],
        "source_org": chunk["source_org"],
        "source_type": chunk["source_type"],
        "jurisdiction": chunk["jurisdiction"],
        "category": chunk["category"],
        "section_header": chunk["section_header"],
        "subsection_header": chunk["subsection_header"],
        "chunk_index": chunk["chunk_index"],
    } for chunk in chunks]
)
```

### Output Format

```
Waypoint Ingestion Pipeline
===========================

Configuration:
  Knowledge Base: C:\...\01_knowledge_base\kb
  ChromaDB Path:  C:\...\chroma_db
  Collection:     waypoint_kb
  Dry Run:        No

Processing documents...
  [1/29] 01_regulatory_sg_import_procedures: 8 chunks ✓
  [2/29] 01_regulatory_sg_export_procedures: 6 chunks ✓
  ...
  [29/29] 04_internal_synthetic_escalation_procedure: 20 chunks ✓

Summary:
  Documents processed: 29
  Documents failed:    0
  Total chunks:        483
  Time elapsed:        12.3s

Done! Collection 'waypoint_kb' now contains 483 chunks.
```

### Error Handling

- Skip failed documents, continue with others
- Log errors with document ID
- Show failure summary at end
- Return non-zero exit code if any failures

### Constraints
- Use ChromaDB default embeddings (no external API)
- Batch operations where possible
- Clear progress indication
- Support both Windows and Unix paths

### TDD Requirements
- [ ] Test file created at `tests/test_ingest.py` FIRST
- [ ] Tests written for CLI parsing, dry-run, category filter
- [ ] Run tests to see them fail (Red)
- [ ] Implement code to make tests pass (Green)
- [ ] All tests pass

### Acceptance Criteria
- [ ] File created at `scripts/ingest.py`
- [ ] `--verbose` shows chunk details
- [ ] `--dry-run` processes without storing
- [ ] `--category` filters correctly
- [ ] `--clear` clears existing collection
- [ ] Initializes ChromaDB with default embeddings
- [ ] Stores all chunks with metadata
- [ ] Handles failures gracefully
- [ ] Shows progress and summary
- [ ] Tests written and passing

---

## Format

### Output Structure
```
scripts/
├── config.py
├── process_docs.py
├── chunker.py
└── ingest.py          # New file

tests/
├── test_process_docs.py
├── test_chunker.py
└── test_ingest.py     # New file (create FIRST - TDD)
```

### Code Style
- Python 3.11+ type hints
- argparse for CLI
- logging module for output
- tqdm for progress bars (optional)

### Module Structure
```python
"""
Main ingestion script for Waypoint knowledge base.

Orchestrates the full pipeline: discover, parse, chunk, embed, store.
"""

import argparse
import logging
import sys
import time
from typing import Optional

import chromadb
from chromadb.utils import embedding_functions

from scripts.config import (
    CHROMA_PERSIST_PATH,
    COLLECTION_NAME,
    KNOWLEDGE_BASE_PATH,
)
from scripts.process_docs import discover_documents, parse_document
from scripts.chunker import chunk_document

logger = logging.getLogger(__name__)


def parse_args(args: Optional[list] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    ...


def initialize_chromadb():
    """Initialize ChromaDB client and collection."""
    ...


def ingest_document(doc: dict, collection, dry_run: bool, verbose: bool) -> int:
    """Ingest a single document into ChromaDB."""
    ...


def run_ingestion(args: argparse.Namespace) -> dict:
    """Run the full ingestion pipeline."""
    ...


def main():
    """Main entry point."""
    ...


if __name__ == "__main__":
    main()
```

### Test Structure (Create FIRST)
```python
"""
Tests for scripts/ingest.py
"""

import pytest
from unittest.mock import Mock, patch
from scripts.ingest import parse_args, run_ingestion


class TestParseArgs:
    def test_default_args(self):
        """Should have sensible defaults."""
        args = parse_args([])
        assert args.verbose is False
        assert args.dry_run is False
        assert args.category is None

    def test_verbose_flag(self):
        """Should parse --verbose flag."""
        args = parse_args(["--verbose"])
        assert args.verbose is True

    def test_dry_run_flag(self):
        """Should parse --dry-run flag."""
        args = parse_args(["--dry-run"])
        assert args.dry_run is True

    def test_category_option(self):
        """Should parse --category option."""
        args = parse_args(["--category", "01_regulatory"])
        assert args.category == "01_regulatory"


class TestRunIngestion:
    def test_dry_run_does_not_store(self):
        """Dry run should process but not store."""
        args = parse_args(["--dry-run"])
        result = run_ingestion(args)
        assert result["stored"] == 0

    def test_category_filter(self):
        """Should only process specified category."""
        args = parse_args(["--dry-run", "--category", "01_regulatory"])
        result = run_ingestion(args)
        assert result["documents_processed"] == 14  # 14 regulatory docs
```

### Validation Commands
```bash
# Run tests first (TDD)
python -m pytest tests/test_ingest.py -v

# Dry run (no storage)
python scripts/ingest.py --dry-run

# Full ingestion
python scripts/ingest.py

# Verbose mode
python scripts/ingest.py --verbose --dry-run

# Single category
python scripts/ingest.py --category 01_regulatory --dry-run

# Verify in ChromaDB
python -c "import chromadb; c = chromadb.PersistentClient('./chroma_db'); col = c.get_collection('waypoint_kb'); print(f'Chunks in collection: {col.count()}')"
```

---

## Execution Checklist (TDD Order)

1. [ ] Create `tests/test_ingest.py` with test cases
2. [ ] Run tests - verify they fail (Red)
3. [ ] Create `scripts/ingest.py` with implementation
4. [ ] Run tests - verify they pass (Green)
5. [ ] Run full ingestion: `python scripts/ingest.py`
6. [ ] Verify ChromaDB collection has 483 chunks
7. [ ] Update REPORT.md
