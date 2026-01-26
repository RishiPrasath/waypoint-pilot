"""
Tests for scripts/ingest.py

TDD test suite - written BEFORE implementation.
"""

import pytest
from pathlib import Path


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_collection():
    """Mock ChromaDB collection for testing."""
    from unittest.mock import Mock
    collection = Mock()
    collection.count.return_value = 0
    collection.add.return_value = None
    return collection


# =============================================================================
# TestParseArgs
# =============================================================================


class TestParseArgs:
    """Tests for parse_args function."""

    def test_default_args(self):
        """Should have sensible defaults."""
        from scripts.ingest import parse_args

        args = parse_args([])
        assert args.verbose is False
        assert args.dry_run is False
        assert args.category is None
        assert args.clear is False

    def test_verbose_flag(self):
        """Should parse --verbose flag."""
        from scripts.ingest import parse_args

        args = parse_args(["--verbose"])
        assert args.verbose is True

    def test_verbose_short_flag(self):
        """Should parse -v short flag."""
        from scripts.ingest import parse_args

        args = parse_args(["-v"])
        assert args.verbose is True

    def test_dry_run_flag(self):
        """Should parse --dry-run flag."""
        from scripts.ingest import parse_args

        args = parse_args(["--dry-run"])
        assert args.dry_run is True

    def test_dry_run_short_flag(self):
        """Should parse -d short flag."""
        from scripts.ingest import parse_args

        args = parse_args(["-d"])
        assert args.dry_run is True

    def test_category_option(self):
        """Should parse --category option."""
        from scripts.ingest import parse_args

        args = parse_args(["--category", "01_regulatory"])
        assert args.category == "01_regulatory"

    def test_clear_flag(self):
        """Should parse --clear flag."""
        from scripts.ingest import parse_args

        args = parse_args(["--clear"])
        assert args.clear is True

    def test_combined_flags(self):
        """Should handle multiple flags together."""
        from scripts.ingest import parse_args

        args = parse_args(["--verbose", "--dry-run", "--category", "02_carriers"])
        assert args.verbose is True
        assert args.dry_run is True
        assert args.category == "02_carriers"


# =============================================================================
# TestInitializeChromadb
# =============================================================================


class TestInitializeChromadb:
    """Tests for initialize_chromadb function."""

    def test_returns_client_and_collection(self):
        """Should return tuple of client and collection."""
        from scripts.ingest import initialize_chromadb

        client, collection = initialize_chromadb()
        assert client is not None
        assert collection is not None

    def test_collection_has_correct_name(self):
        """Collection should have configured name."""
        from scripts.ingest import initialize_chromadb
        from scripts.config import COLLECTION_NAME

        client, collection = initialize_chromadb()
        assert collection.name == COLLECTION_NAME

    def test_client_is_persistent(self):
        """Client should be persistent (not ephemeral)."""
        from scripts.ingest import initialize_chromadb
        from scripts.config import CHROMA_PERSIST_PATH

        client, collection = initialize_chromadb()
        # Persistent client creates files
        assert CHROMA_PERSIST_PATH.exists()


# =============================================================================
# TestIngestDocument
# =============================================================================


class TestIngestDocument:
    """Tests for ingest_document function."""

    def test_returns_chunk_count(self):
        """Should return number of chunks ingested."""
        from scripts.ingest import ingest_document, initialize_chromadb
        from scripts.process_docs import parse_document
        from scripts.config import KNOWLEDGE_BASE_PATH

        path = KNOWLEDGE_BASE_PATH / "01_regulatory/singapore_customs/sg_import_procedures.md"
        doc = parse_document(path)
        _, collection = initialize_chromadb()

        count = ingest_document(doc, collection, dry_run=True, verbose=False)
        assert count > 0
        assert count == 8  # Known chunk count for this doc

    def test_dry_run_does_not_add_to_collection(self, mock_collection):
        """Dry run should not call collection.add()."""
        from scripts.ingest import ingest_document
        from scripts.process_docs import parse_document
        from scripts.config import KNOWLEDGE_BASE_PATH

        path = KNOWLEDGE_BASE_PATH / "01_regulatory/singapore_customs/sg_import_procedures.md"
        doc = parse_document(path)

        count = ingest_document(doc, mock_collection, dry_run=True, verbose=False)
        assert count > 0
        mock_collection.add.assert_not_called()

    def test_normal_run_adds_to_collection(self):
        """Normal run should add chunks to collection."""
        from scripts.ingest import ingest_document, initialize_chromadb
        from scripts.process_docs import parse_document
        from scripts.config import KNOWLEDGE_BASE_PATH

        path = KNOWLEDGE_BASE_PATH / "01_regulatory/singapore_customs/sg_import_procedures.md"
        doc = parse_document(path)
        _, collection = initialize_chromadb()

        # Clear first
        try:
            existing_ids = collection.get()["ids"]
            if existing_ids:
                collection.delete(ids=existing_ids)
        except Exception:
            pass

        initial_count = collection.count()
        chunk_count = ingest_document(doc, collection, dry_run=False, verbose=False)

        assert collection.count() == initial_count + chunk_count


# =============================================================================
# TestRunIngestion
# =============================================================================


class TestRunIngestion:
    """Tests for run_ingestion function."""

    def test_dry_run_returns_zero_stored(self):
        """Dry run should return stored=0."""
        from scripts.ingest import parse_args, run_ingestion

        args = parse_args(["--dry-run"])
        result = run_ingestion(args)

        assert result["stored"] == 0
        assert result["chunks_processed"] > 0

    def test_returns_summary_dict(self):
        """Should return dict with expected keys."""
        from scripts.ingest import parse_args, run_ingestion

        args = parse_args(["--dry-run"])
        result = run_ingestion(args)

        expected_keys = {"documents_processed", "documents_failed",
                         "chunks_processed", "stored", "elapsed_time"}
        assert expected_keys.issubset(result.keys())

    def test_category_filter_regulatory(self):
        """Should only process regulatory category (14 docs)."""
        from scripts.ingest import parse_args, run_ingestion

        args = parse_args(["--dry-run", "--category", "01_regulatory"])
        result = run_ingestion(args)

        assert result["documents_processed"] == 14

    def test_category_filter_carriers(self):
        """Should only process carriers category (6 docs)."""
        from scripts.ingest import parse_args, run_ingestion

        args = parse_args(["--dry-run", "--category", "02_carriers"])
        result = run_ingestion(args)

        assert result["documents_processed"] == 6

    def test_category_filter_reference(self):
        """Should only process reference category (3 docs)."""
        from scripts.ingest import parse_args, run_ingestion

        args = parse_args(["--dry-run", "--category", "03_reference"])
        result = run_ingestion(args)

        assert result["documents_processed"] == 3

    def test_category_filter_internal(self):
        """Should only process internal_synthetic category (6 docs)."""
        from scripts.ingest import parse_args, run_ingestion

        args = parse_args(["--dry-run", "--category", "04_internal_synthetic"])
        result = run_ingestion(args)

        assert result["documents_processed"] == 6

    def test_processes_all_29_documents(self):
        """Should process all 29 documents without filter."""
        from scripts.ingest import parse_args, run_ingestion

        args = parse_args(["--dry-run"])
        result = run_ingestion(args)

        assert result["documents_processed"] == 29

    def test_produces_expected_chunk_count(self):
        """Should produce ~483 chunks from all documents."""
        from scripts.ingest import parse_args, run_ingestion

        args = parse_args(["--dry-run"])
        result = run_ingestion(args)

        # Allow some flexibility
        assert 400 <= result["chunks_processed"] <= 550

    def test_elapsed_time_is_positive(self):
        """Elapsed time should be positive."""
        from scripts.ingest import parse_args, run_ingestion

        args = parse_args(["--dry-run"])
        result = run_ingestion(args)

        assert result["elapsed_time"] > 0


# =============================================================================
# TestFullIngestion (Integration)
# =============================================================================


class TestFullIngestion:
    """Integration tests for full ingestion."""

    def test_full_ingestion_stores_chunks(self):
        """Full ingestion should store chunks in ChromaDB."""
        from scripts.ingest import parse_args, run_ingestion, initialize_chromadb

        # Run with clear to start fresh
        args = parse_args(["--clear"])
        result = run_ingestion(args)

        # Verify stored count
        _, collection = initialize_chromadb()
        assert collection.count() == result["stored"]
        assert result["stored"] > 400  # Should have ~483 chunks

    def test_chunks_have_correct_metadata(self):
        """Stored chunks should have correct metadata fields."""
        from scripts.ingest import initialize_chromadb

        _, collection = initialize_chromadb()

        if collection.count() == 0:
            pytest.skip("No chunks in collection - run full ingestion first")

        # Get a sample chunk
        sample = collection.get(limit=1, include=["metadatas"])

        if sample["metadatas"]:
            metadata = sample["metadatas"][0]
            expected_fields = {"doc_id", "title", "source_org", "category",
                              "jurisdiction", "section_header", "chunk_index"}
            assert expected_fields.issubset(metadata.keys())
