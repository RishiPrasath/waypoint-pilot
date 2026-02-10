"""
Tests for metadata preservation through the ingestion pipeline.

Validates that source_urls, retrieval_keywords, use_cases, and category
fields are correctly stored in ChromaDB chunk metadata after ingestion.

Runs against the live ChromaDB instance (not mocked).
"""

import re
import sys
from pathlib import Path

import pytest

# Ensure parent directory is in path for direct script execution
sys.path.insert(0, str(Path(__file__).parent.parent))

import chromadb
from scripts.config import CHROMA_PERSIST_PATH, COLLECTION_NAME


EXPECTED_CATEGORIES = {
    "01_regulatory",
    "02_carriers",
    "03_reference",
    "04_internal_synthetic",
}

USE_CASE_PATTERN = re.compile(r"^UC-\d+\.\d+$")


@pytest.fixture(scope="module")
def collection():
    """Get the ChromaDB collection for testing."""
    client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_PATH))
    return client.get_collection(COLLECTION_NAME)


@pytest.fixture(scope="module")
def all_metadata(collection):
    """Get all chunk metadata from the collection."""
    result = collection.get(include=["metadatas"])
    return result["metadatas"]


def _get_doc_chunks(collection, doc_id):
    """Helper: get all chunks for a given doc_id."""
    result = collection.get(where={"doc_id": doc_id}, include=["metadatas"])
    return result["metadatas"]


# ─────────────────────────────────────────────────────────────────────────────
# Field Presence Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestFieldPresence:
    """Every chunk must have the 3 new metadata fields as strings."""

    def test_source_urls_present_on_all_chunks(self, all_metadata):
        for i, m in enumerate(all_metadata):
            assert "source_urls" in m, f"Chunk {i} missing source_urls"

    def test_retrieval_keywords_present_on_all_chunks(self, all_metadata):
        for i, m in enumerate(all_metadata):
            assert "retrieval_keywords" in m, f"Chunk {i} missing retrieval_keywords"

    def test_use_cases_present_on_all_chunks(self, all_metadata):
        for i, m in enumerate(all_metadata):
            assert "use_cases" in m, f"Chunk {i} missing use_cases"

    def test_source_urls_is_string(self, all_metadata):
        for i, m in enumerate(all_metadata):
            assert isinstance(m["source_urls"], str), (
                f"Chunk {i} source_urls is {type(m['source_urls']).__name__}, expected str"
            )

    def test_retrieval_keywords_is_string(self, all_metadata):
        for i, m in enumerate(all_metadata):
            assert isinstance(m["retrieval_keywords"], str), (
                f"Chunk {i} retrieval_keywords is {type(m['retrieval_keywords']).__name__}, expected str"
            )

    def test_use_cases_is_string(self, all_metadata):
        for i, m in enumerate(all_metadata):
            assert isinstance(m["use_cases"], str), (
                f"Chunk {i} use_cases is {type(m['use_cases']).__name__}, expected str"
            )


# ─────────────────────────────────────────────────────────────────────────────
# Field Format Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestFieldFormat:
    """Fields must follow expected formats."""

    def test_category_values_in_expected_set(self, all_metadata):
        for i, m in enumerate(all_metadata):
            assert m["category"] in EXPECTED_CATEGORIES, (
                f"Chunk {i} has unexpected category: {m['category']}"
            )

    def test_source_urls_is_csv_or_na(self, all_metadata):
        """source_urls is either N/A, empty, or comma-separated URLs."""
        for i, m in enumerate(all_metadata):
            val = m["source_urls"]
            if val and val != "N/A":
                urls = val.split(",")
                for url in urls:
                    assert url.strip().startswith("http"), (
                        f"Chunk {i} has non-URL in source_urls: {url.strip()!r}"
                    )

    def test_use_cases_match_pattern(self, all_metadata):
        """use_cases entries match UC-N.N pattern."""
        for i, m in enumerate(all_metadata):
            val = m["use_cases"]
            if val:
                for uc in val.split(","):
                    assert USE_CASE_PATTERN.match(uc.strip()), (
                        f"Chunk {i} has invalid use_case format: {uc.strip()!r}"
                    )

    def test_retrieval_keywords_non_empty_for_most_docs(self, all_metadata):
        """Most chunks should have non-empty retrieval_keywords."""
        non_empty = sum(1 for m in all_metadata if m["retrieval_keywords"])
        ratio = non_empty / len(all_metadata)
        assert ratio > 0.5, (
            f"Only {ratio:.0%} of chunks have retrieval_keywords, expected >50%"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Known-Value Spot Checks
# ─────────────────────────────────────────────────────────────────────────────


class TestKnownValues:
    """Specific documents must have expected metadata values."""

    def test_gst_guide_source_urls(self, collection):
        chunks = _get_doc_chunks(collection, "01_regulatory_sg_gst_guide")
        assert len(chunks) > 0, "No chunks found for sg_gst_guide"
        assert "customs.gov.sg" in chunks[0]["source_urls"]

    def test_gst_guide_retrieval_keywords(self, collection):
        chunks = _get_doc_chunks(collection, "01_regulatory_sg_gst_guide")
        assert "GST" in chunks[0]["retrieval_keywords"]

    def test_gst_guide_use_cases(self, collection):
        chunks = _get_doc_chunks(collection, "01_regulatory_sg_gst_guide")
        assert "UC-1.1" in chunks[0]["use_cases"]

    def test_gst_guide_category(self, collection):
        chunks = _get_doc_chunks(collection, "01_regulatory_sg_gst_guide")
        assert chunks[0]["category"] == "01_regulatory"

    def test_maersk_source_urls(self, collection):
        chunks = _get_doc_chunks(collection, "02_carriers_maersk_service_summary")
        assert len(chunks) > 0, "No chunks found for maersk_service_summary"
        assert "maersk.com" in chunks[0]["source_urls"]

    def test_maersk_category(self, collection):
        chunks = _get_doc_chunks(collection, "02_carriers_maersk_service_summary")
        assert chunks[0]["category"] == "02_carriers"

    def test_incoterms_category(self, collection):
        chunks = _get_doc_chunks(collection, "03_reference_incoterms_comparison_chart")
        assert len(chunks) > 0, "No chunks found for incoterms_comparison_chart"
        assert chunks[0]["category"] == "03_reference"

    def test_booking_procedure_source_urls_na(self, collection):
        chunks = _get_doc_chunks(collection, "04_internal_synthetic_booking_procedure")
        assert len(chunks) > 0, "No chunks found for booking_procedure"
        assert chunks[0]["source_urls"] == "N/A"

    def test_booking_procedure_category(self, collection):
        chunks = _get_doc_chunks(collection, "04_internal_synthetic_booking_procedure")
        assert chunks[0]["category"] == "04_internal_synthetic"


# ─────────────────────────────────────────────────────────────────────────────
# Edge Cases
# ─────────────────────────────────────────────────────────────────────────────


class TestEdgeCases:
    """Edge cases: N/A URLs, multi-URL docs, same-doc consistency."""

    def test_internal_docs_have_no_external_urls(self, collection):
        """Synthetic_internal docs should have source_urls = 'N/A' or empty string (no real URLs)."""
        result = collection.get(
            where={"source_type": "synthetic_internal"}, include=["metadatas"]
        )
        for m in result["metadatas"]:
            val = m["source_urls"]
            assert val in ("N/A", ""), (
                f"Internal doc {m['doc_id']} has unexpected source_urls={val!r}"
            )
            if val and val != "N/A":
                assert not val.startswith("http"), (
                    f"Internal doc {m['doc_id']} has external URL: {val}"
                )

    def test_multi_url_doc_has_comma_separated_urls(self, collection):
        """sg_gst_guide has 2 URLs — verify comma separation."""
        chunks = _get_doc_chunks(collection, "01_regulatory_sg_gst_guide")
        urls = chunks[0]["source_urls"].split(",")
        assert len(urls) >= 2, (
            f"Expected >=2 URLs for sg_gst_guide, got {len(urls)}: {chunks[0]['source_urls']}"
        )

    def test_same_doc_chunks_share_source_urls(self, collection):
        """All chunks from the same document must have identical source_urls."""
        chunks = _get_doc_chunks(collection, "01_regulatory_sg_gst_guide")
        assert len(chunks) > 1, "Need multiple chunks to test consistency"
        expected = chunks[0]["source_urls"]
        for i, m in enumerate(chunks[1:], start=1):
            assert m["source_urls"] == expected, (
                f"Chunk {i} source_urls differs from chunk 0"
            )

    def test_same_doc_chunks_share_category(self, collection):
        """All chunks from the same document must have identical category."""
        chunks = _get_doc_chunks(collection, "02_carriers_maersk_service_summary")
        assert len(chunks) > 1, "Need multiple chunks to test consistency"
        expected = chunks[0]["category"]
        for i, m in enumerate(chunks[1:], start=1):
            assert m["category"] == expected, (
                f"Chunk {i} category differs from chunk 0"
            )

    def test_same_doc_chunks_share_use_cases(self, collection):
        """All chunks from the same document must have identical use_cases."""
        chunks = _get_doc_chunks(collection, "01_regulatory_sg_gst_guide")
        assert len(chunks) > 1, "Need multiple chunks to test consistency"
        expected = chunks[0]["use_cases"]
        for i, m in enumerate(chunks[1:], start=1):
            assert m["use_cases"] == expected, (
                f"Chunk {i} use_cases differs from chunk 0"
            )


# ─────────────────────────────────────────────────────────────────────────────
# Category Coverage
# ─────────────────────────────────────────────────────────────────────────────


class TestCategoryCoverage:
    """All 4 KB categories must be represented in ChromaDB."""

    def test_all_four_categories_present(self, all_metadata):
        found = {m["category"] for m in all_metadata}
        for cat in EXPECTED_CATEGORIES:
            assert cat in found, f"Category {cat} not found in ChromaDB"

    def test_each_category_has_multiple_chunks(self, all_metadata):
        counts = {}
        for m in all_metadata:
            counts[m["category"]] = counts.get(m["category"], 0) + 1
        for cat in EXPECTED_CATEGORIES:
            assert counts.get(cat, 0) >= 10, (
                f"Category {cat} has only {counts.get(cat, 0)} chunks, expected >=10"
            )
