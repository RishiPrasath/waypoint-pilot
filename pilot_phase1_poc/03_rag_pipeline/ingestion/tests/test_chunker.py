"""
Tests for scripts/chunker.py

TDD test suite - written BEFORE implementation.
"""

import pytest

from scripts.config import KNOWLEDGE_BASE_PATH, CHUNK_SIZE
from scripts.process_docs import parse_document, load_all_documents


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def real_document():
    """Load a real document for testing."""
    path = KNOWLEDGE_BASE_PATH / "01_regulatory/singapore_customs/sg_import_procedures.md"
    return parse_document(path)


@pytest.fixture
def real_carrier_document():
    """Load a carrier document for testing."""
    path = KNOWLEDGE_BASE_PATH / "02_carriers/ocean/maersk_service_summary.md"
    return parse_document(path)


@pytest.fixture
def sample_content_with_headers():
    """Sample content with section headers."""
    return """# Main Title

## Section One

This is content in section one. It has some text.

### Subsection 1.1

More detailed content in the subsection.

## Section Two

Content in the second section.

### Subsection 2.1

Even more content here.
"""


# =============================================================================
# TestGenerateChunkId
# =============================================================================


class TestGenerateChunkId:
    """Tests for generate_chunk_id function."""

    def test_creates_zero_padded_id(self):
        """Should create ID with 3-digit zero-padded index."""
        from scripts.chunker import generate_chunk_id

        result = generate_chunk_id("doc_123", 7)
        assert result == "doc_123_chunk_007"

    def test_handles_single_digit(self):
        """Should zero-pad single digit index."""
        from scripts.chunker import generate_chunk_id

        result = generate_chunk_id("test_doc", 0)
        assert result == "test_doc_chunk_000"

    def test_handles_double_digit(self):
        """Should zero-pad double digit index."""
        from scripts.chunker import generate_chunk_id

        result = generate_chunk_id("test_doc", 42)
        assert result == "test_doc_chunk_042"

    def test_handles_triple_digit(self):
        """Should handle triple digit index without extra padding."""
        from scripts.chunker import generate_chunk_id

        result = generate_chunk_id("test_doc", 150)
        assert result == "test_doc_chunk_150"

    def test_preserves_doc_id(self):
        """Should preserve the full doc_id in chunk_id."""
        from scripts.chunker import generate_chunk_id

        result = generate_chunk_id("01_regulatory_sg_import_procedures", 5)
        assert result.startswith("01_regulatory_sg_import_procedures_chunk_")


# =============================================================================
# TestExtractSectionHeader
# =============================================================================


class TestExtractSectionHeader:
    """Tests for extract_section_header function."""

    def test_finds_section_header(self, sample_content_with_headers):
        """Should find ## header before position."""
        from scripts.chunker import extract_section_header

        # Position somewhere in Section One content
        pos = sample_content_with_headers.find("This is content")
        result = extract_section_header(sample_content_with_headers, pos)
        assert result == "Section One"

    def test_finds_later_section_header(self, sample_content_with_headers):
        """Should find most recent ## header."""
        from scripts.chunker import extract_section_header

        # Position in Section Two
        pos = sample_content_with_headers.find("Content in the second")
        result = extract_section_header(sample_content_with_headers, pos)
        assert result == "Section Two"

    def test_returns_empty_when_no_header(self):
        """Should return empty string if no ## header before position."""
        from scripts.chunker import extract_section_header

        content = "Just some content without any headers at all."
        result = extract_section_header(content, 20)
        assert result == ""

    def test_returns_empty_when_position_before_header(self, sample_content_with_headers):
        """Should return empty if position is before any ## header."""
        from scripts.chunker import extract_section_header

        # Position at very start
        result = extract_section_header(sample_content_with_headers, 5)
        assert result == ""

    def test_ignores_subsection_headers(self):
        """Should not match ### headers, only ## headers."""
        from scripts.chunker import extract_section_header

        content = "### Only Subsection\n\nSome content here."
        result = extract_section_header(content, 30)
        assert result == ""


# =============================================================================
# TestExtractSubsectionHeader
# =============================================================================


class TestExtractSubsectionHeader:
    """Tests for extract_subsection_header function."""

    def test_finds_subsection_header(self, sample_content_with_headers):
        """Should find ### header before position."""
        from scripts.chunker import extract_subsection_header

        # Position in Subsection 1.1 content
        pos = sample_content_with_headers.find("More detailed content")
        result = extract_subsection_header(sample_content_with_headers, pos)
        assert result == "Subsection 1.1"

    def test_finds_later_subsection_header(self, sample_content_with_headers):
        """Should find most recent ### header."""
        from scripts.chunker import extract_subsection_header

        # Position in Subsection 2.1
        pos = sample_content_with_headers.find("Even more content")
        result = extract_subsection_header(sample_content_with_headers, pos)
        assert result == "Subsection 2.1"

    def test_returns_empty_when_no_subsection(self):
        """Should return empty string if no ### header."""
        from scripts.chunker import extract_subsection_header

        content = "## Section Only\n\nNo subsections here."
        result = extract_subsection_header(content, 30)
        assert result == ""

    def test_returns_empty_when_position_before_header(self, sample_content_with_headers):
        """Should return empty if position is before any ### header."""
        from scripts.chunker import extract_subsection_header

        # Position before first subsection
        pos = sample_content_with_headers.find("This is content")
        result = extract_subsection_header(sample_content_with_headers, pos)
        assert result == ""


# =============================================================================
# TestChunkDocument
# =============================================================================


class TestChunkDocument:
    """Tests for chunk_document function."""

    def test_produces_multiple_chunks(self, real_document):
        """Should produce multiple chunks from document."""
        from scripts.chunker import chunk_document

        chunks = chunk_document(real_document)
        assert len(chunks) > 1

    def test_chunks_have_chunk_specific_fields(self, real_document):
        """Each chunk should have chunk-specific fields."""
        from scripts.chunker import chunk_document

        chunks = chunk_document(real_document)
        chunk_fields = {"chunk_id", "chunk_index", "chunk_text",
                        "chunk_char_count", "section_header", "subsection_header"}

        for chunk in chunks:
            assert chunk_fields.issubset(chunk.keys()), f"Missing chunk fields"

    def test_chunks_have_document_metadata(self, real_document):
        """Each chunk should have all document metadata fields."""
        from scripts.chunker import chunk_document

        chunks = chunk_document(real_document)
        doc_fields = {"doc_id", "file_path", "title", "source_org",
                      "source_urls", "source_type", "last_updated",
                      "jurisdiction", "category", "use_cases",
                      "content", "char_count"}

        for chunk in chunks:
            assert doc_fields.issubset(chunk.keys()), f"Missing doc fields"

    def test_preserves_document_metadata(self, real_document):
        """Chunks should preserve original document metadata values."""
        from scripts.chunker import chunk_document

        chunks = chunk_document(real_document)
        for chunk in chunks:
            assert chunk["doc_id"] == real_document["doc_id"]
            assert chunk["title"] == real_document["title"]
            assert chunk["source_org"] == real_document["source_org"]
            assert chunk["jurisdiction"] == real_document["jurisdiction"]

    def test_chunk_ids_are_unique(self, real_document):
        """All chunk IDs within a document should be unique."""
        from scripts.chunker import chunk_document

        chunks = chunk_document(real_document)
        chunk_ids = [c["chunk_id"] for c in chunks]
        assert len(chunk_ids) == len(set(chunk_ids))

    def test_chunk_ids_are_zero_padded(self, real_document):
        """Chunk IDs should have zero-padded indices."""
        from scripts.chunker import chunk_document

        chunks = chunk_document(real_document)
        # First chunk should end with _chunk_000
        assert chunks[0]["chunk_id"].endswith("_chunk_000")

    def test_chunk_indices_are_sequential(self, real_document):
        """Chunk indices should be sequential starting from 0."""
        from scripts.chunker import chunk_document

        chunks = chunk_document(real_document)
        indices = [c["chunk_index"] for c in chunks]
        assert indices == list(range(len(chunks)))

    def test_chunk_text_not_empty(self, real_document):
        """Each chunk should have non-empty text."""
        from scripts.chunker import chunk_document

        chunks = chunk_document(real_document)
        for chunk in chunks:
            assert chunk["chunk_text"].strip(), f"Empty chunk at index {chunk['chunk_index']}"

    def test_chunk_char_count_matches_text(self, real_document):
        """chunk_char_count should match length of chunk_text."""
        from scripts.chunker import chunk_document

        chunks = chunk_document(real_document)
        for chunk in chunks:
            assert chunk["chunk_char_count"] == len(chunk["chunk_text"])

    def test_chunks_respect_size_limit(self, real_document):
        """Most chunks should be near CHUNK_SIZE (some variation allowed)."""
        from scripts.chunker import chunk_document

        chunks = chunk_document(real_document)
        # Allow some flexibility - chunks can be up to 20% over due to separator logic
        max_allowed = CHUNK_SIZE * 1.2

        for chunk in chunks[:-1]:  # Exclude last chunk which may be smaller
            assert chunk["chunk_char_count"] <= max_allowed, \
                f"Chunk {chunk['chunk_index']} too large: {chunk['chunk_char_count']}"


# =============================================================================
# TestChunkAllDocuments
# =============================================================================


class TestChunkAllDocuments:
    """Tests for chunk_all_documents function."""

    def test_returns_flat_list(self):
        """Should return flat list of all chunks."""
        from scripts.chunker import chunk_all_documents

        docs = load_all_documents()
        chunks = chunk_all_documents(docs)

        assert isinstance(chunks, list)
        assert all(isinstance(c, dict) for c in chunks)

    def test_produces_expected_chunk_count(self):
        """Should produce ~350-400 total chunks from 29 documents."""
        from scripts.chunker import chunk_all_documents

        docs = load_all_documents()
        chunks = chunk_all_documents(docs)

        # Allow range of 300-500 for flexibility
        assert 300 <= len(chunks) <= 500, f"Unexpected chunk count: {len(chunks)}"

    def test_all_chunks_have_required_fields(self):
        """All chunks should have all required fields."""
        from scripts.chunker import chunk_all_documents

        docs = load_all_documents()
        chunks = chunk_all_documents(docs)

        required_fields = {
            "chunk_id", "chunk_index", "chunk_text", "chunk_char_count",
            "section_header", "subsection_header",
            "doc_id", "file_path", "title", "source_org", "source_urls",
            "source_type", "last_updated", "jurisdiction", "category",
            "use_cases", "content", "char_count"
        }

        for chunk in chunks[:10]:  # Check first 10 for speed
            assert required_fields.issubset(chunk.keys())

    def test_chunks_from_all_categories(self):
        """Should have chunks from all 4 categories."""
        from scripts.chunker import chunk_all_documents

        docs = load_all_documents()
        chunks = chunk_all_documents(docs)

        categories = set(c["category"] for c in chunks)
        expected = {"01_regulatory", "02_carriers", "03_reference", "04_internal_synthetic"}
        assert categories == expected

    def test_all_chunk_ids_globally_unique(self):
        """All chunk IDs across all documents should be unique."""
        from scripts.chunker import chunk_all_documents

        docs = load_all_documents()
        chunks = chunk_all_documents(docs)

        chunk_ids = [c["chunk_id"] for c in chunks]
        assert len(chunk_ids) == len(set(chunk_ids)), "Duplicate chunk IDs found"
