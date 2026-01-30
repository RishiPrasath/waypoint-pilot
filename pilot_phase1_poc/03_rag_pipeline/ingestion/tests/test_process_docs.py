"""
Tests for scripts/process_docs.py

Comprehensive test suite covering all public functions with
happy path, edge cases, and integration tests.
"""

import pytest
from pathlib import Path

from scripts.process_docs import (
    discover_documents,
    parse_frontmatter,
    extract_content,
    get_category_from_path,
    generate_doc_id,
    parse_document,
    load_all_documents,
)
from scripts.config import KNOWLEDGE_BASE_PATH


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def sample_frontmatter_content():
    """Sample markdown with valid frontmatter."""
    return '''---
title: Test Document
source_organization: Test Org
source_urls:
  - url: https://example.com
    description: Test URL
source_type: public_regulatory
last_updated: 2025-01-26
jurisdiction: SG
category: customs
use_cases: [UC-1.1, UC-2.1]
---

# Test Content

This is test content.
'''


@pytest.fixture
def sample_no_frontmatter():
    """Sample markdown without frontmatter."""
    return '''# Just Content

No frontmatter here.
'''


@pytest.fixture
def sample_minimal_frontmatter():
    """Sample markdown with minimal frontmatter (missing optional fields)."""
    return '''---
title: Minimal Doc
---

# Minimal Content

Only title in frontmatter.
'''


@pytest.fixture
def real_document_path():
    """Path to a real document in knowledge base (kb/ folder)."""
    return KNOWLEDGE_BASE_PATH / "01_regulatory/singapore_customs/sg_import_procedures.md"


@pytest.fixture
def real_carrier_path():
    """Path to a carrier document."""
    return KNOWLEDGE_BASE_PATH / "02_carriers/ocean/maersk_service_summary.md"


@pytest.fixture
def real_reference_path():
    """Path to a reference document."""
    return KNOWLEDGE_BASE_PATH / "03_reference/incoterms/incoterms_2020_reference.md"


@pytest.fixture
def real_internal_path():
    """Path to an internal synthetic document."""
    return KNOWLEDGE_BASE_PATH / "04_internal_synthetic/procedures/booking_procedure.md"


# =============================================================================
# TestDiscoverDocuments
# =============================================================================


class TestDiscoverDocuments:
    """Tests for discover_documents function."""

    def test_finds_all_29_documents(self):
        """Should discover exactly 29 content documents from kb/ folder."""
        # Arrange
        path = KNOWLEDGE_BASE_PATH

        # Act
        docs = discover_documents(path)

        # Assert
        assert len(docs) == 29

    def test_returns_sorted_paths(self):
        """Should return paths in sorted order."""
        # Arrange
        path = KNOWLEDGE_BASE_PATH

        # Act
        docs = discover_documents(path)

        # Assert
        assert docs == sorted(docs)

    def test_returns_path_objects(self):
        """Should return list of Path objects."""
        # Arrange
        path = KNOWLEDGE_BASE_PATH

        # Act
        docs = discover_documents(path)

        # Assert
        assert all(isinstance(doc, Path) for doc in docs)

    def test_all_files_are_markdown(self):
        """All discovered files should have .md extension."""
        # Arrange
        path = KNOWLEDGE_BASE_PATH

        # Act
        docs = discover_documents(path)

        # Assert
        assert all(doc.suffix == ".md" for doc in docs)

    def test_all_files_exist(self):
        """All discovered files should exist on disk."""
        # Arrange
        path = KNOWLEDGE_BASE_PATH

        # Act
        docs = discover_documents(path)

        # Assert
        assert all(doc.exists() for doc in docs)


# =============================================================================
# TestParseFrontmatter
# =============================================================================


class TestParseFrontmatter:
    """Tests for parse_frontmatter function."""

    def test_parses_valid_yaml(self, sample_frontmatter_content):
        """Should parse valid YAML frontmatter."""
        # Act
        result = parse_frontmatter(sample_frontmatter_content)

        # Assert
        assert result["title"] == "Test Document"
        assert result["source_organization"] == "Test Org"

    def test_returns_empty_dict_for_no_frontmatter(self, sample_no_frontmatter):
        """Should return {} for content without frontmatter."""
        # Act
        result = parse_frontmatter(sample_no_frontmatter)

        # Assert
        assert result == {}

    def test_handles_nested_source_urls(self, sample_frontmatter_content):
        """Should parse nested source_urls structure."""
        # Act
        result = parse_frontmatter(sample_frontmatter_content)

        # Assert
        assert len(result["source_urls"]) == 1
        assert result["source_urls"][0]["url"] == "https://example.com"

    def test_handles_list_fields(self, sample_frontmatter_content):
        """Should parse use_cases as list."""
        # Act
        result = parse_frontmatter(sample_frontmatter_content)

        # Assert
        assert result["use_cases"] == ["UC-1.1", "UC-2.1"]

    def test_handles_empty_string(self):
        """Should return empty dict for empty string."""
        # Act
        result = parse_frontmatter("")

        # Assert
        assert result == {}


# =============================================================================
# TestExtractContent
# =============================================================================


class TestExtractContent:
    """Tests for extract_content function."""

    def test_removes_frontmatter(self, sample_frontmatter_content):
        """Should return content without YAML block."""
        # Act
        result = extract_content(sample_frontmatter_content)

        # Assert
        assert "---" not in result
        assert "title:" not in result
        assert "# Test Content" in result

    def test_strips_whitespace(self, sample_frontmatter_content):
        """Should strip leading/trailing whitespace."""
        # Act
        result = extract_content(sample_frontmatter_content)

        # Assert
        assert result == result.strip()
        assert not result.startswith("\n")
        assert not result.endswith("\n")

    def test_handles_no_frontmatter(self, sample_no_frontmatter):
        """Should return original content if no frontmatter."""
        # Act
        result = extract_content(sample_no_frontmatter)

        # Assert
        assert "# Just Content" in result
        assert "No frontmatter here." in result

    def test_preserves_content_structure(self, sample_frontmatter_content):
        """Should preserve markdown structure in content."""
        # Act
        result = extract_content(sample_frontmatter_content)

        # Assert
        assert "# Test Content" in result
        assert "This is test content." in result


# =============================================================================
# TestGetCategoryFromPath
# =============================================================================


class TestGetCategoryFromPath:
    """Tests for get_category_from_path function."""

    def test_extracts_regulatory_category(self, real_document_path):
        """Should extract '01_regulatory' from path."""
        # Act
        result = get_category_from_path(real_document_path)

        # Assert
        assert result == "01_regulatory"

    def test_extracts_carriers_category(self, real_carrier_path):
        """Should extract '02_carriers' from path."""
        # Act
        result = get_category_from_path(real_carrier_path)

        # Assert
        assert result == "02_carriers"

    def test_extracts_reference_category(self, real_reference_path):
        """Should extract '03_reference' from path."""
        # Act
        result = get_category_from_path(real_reference_path)

        # Assert
        assert result == "03_reference"

    def test_extracts_internal_category(self, real_internal_path):
        """Should extract '04_internal_synthetic' from path."""
        # Act
        result = get_category_from_path(real_internal_path)

        # Assert
        assert result == "04_internal_synthetic"


# =============================================================================
# TestGenerateDocId
# =============================================================================


class TestGenerateDocId:
    """Tests for generate_doc_id function."""

    def test_creates_unique_id(self, real_document_path):
        """Should create ID in format: {category}_{filename}."""
        # Act
        result = generate_doc_id(real_document_path)

        # Assert
        assert result == "01_regulatory_sg_import_procedures"

    def test_excludes_file_extension(self, real_document_path):
        """Should not include .md in doc_id."""
        # Act
        result = generate_doc_id(real_document_path)

        # Assert
        assert ".md" not in result

    def test_includes_category_prefix(self, real_carrier_path):
        """Should include category as prefix."""
        # Act
        result = generate_doc_id(real_carrier_path)

        # Assert
        assert result.startswith("02_carriers_")


# =============================================================================
# TestParseDocument
# =============================================================================


class TestParseDocument:
    """Tests for parse_document function."""

    def test_returns_all_12_fields(self, real_document_path):
        """Should return dict with all 12 required fields."""
        # Act
        result = parse_document(real_document_path)

        # Assert
        expected_fields = {
            "doc_id", "file_path", "title", "source_org",
            "source_urls", "source_type", "last_updated",
            "jurisdiction", "category", "use_cases",
            "content", "char_count"
        }
        assert set(result.keys()) == expected_fields

    def test_maps_source_organization_to_source_org(self, real_document_path):
        """Should map source_organization → source_org."""
        # Act
        result = parse_document(real_document_path)

        # Assert
        assert "source_org" in result
        assert result["source_org"] == "Singapore Customs"

    def test_extracts_urls_from_nested_objects(self, real_document_path):
        """Should extract url field from nested source_urls."""
        # Act
        result = parse_document(real_document_path)

        # Assert
        assert isinstance(result["source_urls"], list)
        assert len(result["source_urls"]) > 0
        assert all(isinstance(url, str) for url in result["source_urls"])
        assert all(url.startswith("http") for url in result["source_urls"])

    def test_calculates_char_count(self, real_document_path):
        """Should include accurate char_count."""
        # Act
        result = parse_document(real_document_path)

        # Assert
        assert result["char_count"] == len(result["content"])
        assert result["char_count"] > 0

    def test_content_excludes_frontmatter(self, real_document_path):
        """Content should not contain frontmatter."""
        # Act
        result = parse_document(real_document_path)

        # Assert
        assert "source_organization:" not in result["content"]
        assert "---\ntitle:" not in result["content"]

    def test_file_path_is_absolute(self, real_document_path):
        """File path should be absolute string."""
        # Act
        result = parse_document(real_document_path)

        # Assert
        assert isinstance(result["file_path"], str)
        path = Path(result["file_path"])
        assert path.is_absolute()


# =============================================================================
# TestLoadAllDocuments
# =============================================================================


class TestLoadAllDocuments:
    """Tests for load_all_documents function."""

    def test_loads_all_29_documents(self):
        """Should load exactly 29 documents."""
        # Act
        docs = load_all_documents()

        # Assert
        assert len(docs) == 29

    def test_all_documents_have_required_fields(self):
        """Each document should have all 12 fields."""
        # Arrange
        expected_fields = {
            "doc_id", "file_path", "title", "source_org",
            "source_urls", "source_type", "last_updated",
            "jurisdiction", "category", "use_cases",
            "content", "char_count"
        }

        # Act
        docs = load_all_documents()

        # Assert
        for doc in docs:
            assert set(doc.keys()) == expected_fields, f"Missing fields in {doc['doc_id']}"

    def test_total_char_count_reasonable(self):
        """Total chars should be ~185,000."""
        # Act
        docs = load_all_documents()
        total_chars = sum(d["char_count"] for d in docs)

        # Assert
        assert 180000 < total_chars < 200000

    def test_category_distribution(self):
        """Should have correct count per category."""
        # Arrange
        expected = {
            "01_regulatory": 14,
            "02_carriers": 6,
            "03_reference": 3,
            "04_internal_synthetic": 6,
        }

        # Act
        docs = load_all_documents()
        actual = {}
        for doc in docs:
            cat = doc["category"]
            actual[cat] = actual.get(cat, 0) + 1

        # Assert
        assert actual == expected

    def test_all_doc_ids_unique(self):
        """All document IDs should be unique."""
        # Act
        docs = load_all_documents()
        doc_ids = [d["doc_id"] for d in docs]

        # Assert
        assert len(doc_ids) == len(set(doc_ids))

    def test_all_documents_have_content(self):
        """All documents should have non-empty content."""
        # Act
        docs = load_all_documents()

        # Assert
        for doc in docs:
            assert doc["content"], f"Empty content in {doc['doc_id']}"
            assert doc["char_count"] > 0, f"Zero char_count in {doc['doc_id']}"
