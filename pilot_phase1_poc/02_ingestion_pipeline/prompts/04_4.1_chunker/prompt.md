# Task 4.1: Create Chunking Engine Module

## Persona

> You are a Python developer specializing in NLP and text processing pipelines.
> You follow TDD practices - writing tests first, then implementation.
> You prioritize semantic chunking that preserves context and section structure.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. The chunking engine splits parsed documents into smaller chunks suitable for embedding and retrieval. Chunks must preserve metadata and maintain semantic coherence.

### Current State
- ✅ `scripts/process_docs.py` - Document processor (29 docs, 185K chars)
- ✅ `scripts/config.py` - Chunking config defined (CHUNK_SIZE, CHUNK_OVERLAP, SEPARATORS)
- ✅ `tests/test_process_docs.py` - 33 tests passing
- 📁 Knowledge base at `01_knowledge_base/kb/` with 29 documents

### Reference Documents
- Roadmap: `docs/01_implementation_roadmap.md`
- Config: `scripts/config.py`
- Document processor: `scripts/process_docs.py`

### Dependencies
- Task 3.1 (process_docs.py) ✅ Complete
- Task 3.2 (test_process_docs.py) ✅ Complete
- `langchain-text-splitters` package installed

---

## Task

### Objective
Create `scripts/chunker.py` that splits documents into semantic chunks while preserving metadata and section context. Follow TDD - write tests first in `tests/test_chunker.py`.

### Requirements

1. **`chunk_document(doc: dict) -> list[dict]`**
   - Main function that chunks a parsed document
   - Uses RecursiveCharacterTextSplitter from langchain
   - Preserves all 12 metadata fields from document
   - Adds chunk-specific fields (chunk_id, chunk_index, section_header, subsection_header)

2. **`generate_chunk_id(doc_id: str, index: int) -> str`**
   - Generate unique chunk ID
   - Format: `{doc_id}_chunk_{index:03d}` (zero-padded to 3 digits)
   - Example: `01_regulatory_sg_import_procedures_chunk_007`

3. **`extract_section_header(content: str, position: int) -> str`**
   - Find the most recent `## ` header before the chunk position
   - Return empty string if none found

4. **`extract_subsection_header(content: str, position: int) -> str`**
   - Find the most recent `### ` header before the chunk position
   - Return empty string if none found

5. **`chunk_all_documents(docs: list[dict]) -> list[dict]`**
   - Convenience function to chunk all documents
   - Returns flat list of all chunks

### Chunking Configuration (from config.py)

```python
CHUNK_SIZE = 600        # characters (~150 tokens)
CHUNK_OVERLAP = 90      # 15% overlap
SEPARATORS = ["\n## ", "\n### ", "\n\n", "\n"]
```

### Chunk Object Schema

Each chunk should have these fields:

```python
{
    # Chunk-specific fields
    "chunk_id": str,           # e.g., "01_regulatory_sg_import_procedures_chunk_007"
    "chunk_index": int,        # 0-based index within document
    "chunk_text": str,         # The actual chunk content
    "chunk_char_count": int,   # Length of chunk_text
    "section_header": str,     # Most recent ## header (or "")
    "subsection_header": str,  # Most recent ### header (or "")

    # Inherited from document (all 12 fields)
    "doc_id": str,
    "file_path": str,
    "title": str,
    "source_org": str,
    "source_urls": list,
    "source_type": str,
    "last_updated": str,
    "jurisdiction": str,
    "category": str,
    "use_cases": list,
    "content": str,            # Full document content (for reference)
    "char_count": int,         # Full document char count
}
```

### Expected Output
- ~350-400 total chunks from 29 documents
- Average ~12-14 chunks per document
- Each chunk ~400-600 characters

### Constraints
- Chunk size should not exceed 600 chars (soft limit, may be slightly over)
- Use langchain's RecursiveCharacterTextSplitter
- Preserve semantic boundaries (prefer splitting at headers/paragraphs)
- All document metadata must be preserved in each chunk

### TDD Requirements
- [ ] Test file created at `tests/test_chunker.py` FIRST
- [ ] Tests written for all functions before implementation
- [ ] Run tests to see them fail (Red)
- [ ] Implement code to make tests pass (Green)
- [ ] All tests pass

### Acceptance Criteria
- [ ] File created at `scripts/chunker.py`
- [ ] `chunk_document()` produces chunks with all fields
- [ ] `generate_chunk_id()` creates zero-padded IDs
- [ ] `extract_section_header()` finds correct headers
- [ ] `extract_subsection_header()` finds correct headers
- [ ] Total chunks ~350-400 from 29 documents
- [ ] All metadata preserved in chunks
- [ ] Tests written and passing

---

## Format

### Output Structure
```
scripts/
└── chunker.py

tests/
├── test_process_docs.py
└── test_chunker.py      # New file (create FIRST - TDD)
```

### Code Style
- Python 3.11+ type hints
- Docstrings for all public functions
- Import config values from `scripts.config`
- Use logging for debug output

### Module Structure
```python
"""
Chunking engine for Waypoint knowledge base.

Splits documents into semantic chunks while preserving
metadata and section context for RAG retrieval.
"""

import logging
import re
from typing import Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter

from scripts.config import CHUNK_SIZE, CHUNK_OVERLAP, SEPARATORS

logger = logging.getLogger(__name__)


def generate_chunk_id(doc_id: str, index: int) -> str:
    """Generate zero-padded chunk ID."""
    ...


def extract_section_header(content: str, position: int) -> str:
    """Extract most recent ## header before position."""
    ...


def extract_subsection_header(content: str, position: int) -> str:
    """Extract most recent ### header before position."""
    ...


def chunk_document(doc: dict) -> list[dict]:
    """Split document into chunks with metadata."""
    ...


def chunk_all_documents(docs: list[dict]) -> list[dict]:
    """Chunk all documents and return flat list."""
    ...
```

### Test Structure (Create FIRST)
```python
"""
Tests for scripts/chunker.py
"""

import pytest
from scripts.chunker import (
    generate_chunk_id,
    extract_section_header,
    extract_subsection_header,
    chunk_document,
    chunk_all_documents,
)
from scripts.process_docs import parse_document, load_all_documents
from scripts.config import KNOWLEDGE_BASE_PATH, CHUNK_SIZE


class TestGenerateChunkId:
    def test_creates_zero_padded_id(self):
        """Should create ID with 3-digit zero-padded index."""
        result = generate_chunk_id("doc_123", 7)
        assert result == "doc_123_chunk_007"

    def test_handles_large_index(self):
        """Should handle index > 99."""
        result = generate_chunk_id("doc_123", 150)
        assert result == "doc_123_chunk_150"


class TestExtractSectionHeader:
    def test_finds_section_header(self):
        """Should find ## header before position."""
        content = "# Title\n\n## Section One\n\nSome content here."
        result = extract_section_header(content, 40)
        assert result == "Section One"

    def test_returns_empty_when_no_header(self):
        """Should return empty string if no ## header."""
        content = "Just some content without headers."
        result = extract_section_header(content, 20)
        assert result == ""


class TestChunkDocument:
    def test_produces_chunks(self, real_document):
        """Should produce multiple chunks from document."""
        chunks = chunk_document(real_document)
        assert len(chunks) > 1

    def test_chunks_have_required_fields(self, real_document):
        """Each chunk should have all required fields."""
        chunks = chunk_document(real_document)
        required = {"chunk_id", "chunk_index", "chunk_text", "doc_id", "title"}
        for chunk in chunks:
            assert required.issubset(chunk.keys())

    def test_preserves_document_metadata(self, real_document):
        """Chunks should preserve original document metadata."""
        chunks = chunk_document(real_document)
        for chunk in chunks:
            assert chunk["doc_id"] == real_document["doc_id"]
            assert chunk["title"] == real_document["title"]


@pytest.fixture
def real_document():
    """Load a real document for testing."""
    path = KNOWLEDGE_BASE_PATH / "01_regulatory/singapore_customs/sg_import_procedures.md"
    return parse_document(path)
```

### Validation Commands
```bash
# Run tests first (TDD - should fail initially)
python -m pytest tests/test_chunker.py -v

# After implementation - verify chunk count
python -c "from scripts.process_docs import load_all_documents; from scripts.chunker import chunk_all_documents; docs = load_all_documents(); chunks = chunk_all_documents(docs); print(f'Total chunks: {len(chunks)}')"

# Verify chunk structure
python -c "from scripts.process_docs import parse_document; from scripts.chunker import chunk_document; from scripts.config import KNOWLEDGE_BASE_PATH; doc = parse_document(KNOWLEDGE_BASE_PATH / '01_regulatory/singapore_customs/sg_import_procedures.md'); chunks = chunk_document(doc); print(f'Chunks: {len(chunks)}'); print(f'Fields: {list(chunks[0].keys())}')"
```

---

## Execution Checklist (TDD Order)

1. [ ] Create `tests/test_chunker.py` with all test cases
2. [ ] Run tests - verify they fail (Red)
3. [ ] Create `scripts/chunker.py` with implementation
4. [ ] Run tests - verify they pass (Green)
5. [ ] Verify total chunks ~350-400
6. [ ] Update REPORT.md
