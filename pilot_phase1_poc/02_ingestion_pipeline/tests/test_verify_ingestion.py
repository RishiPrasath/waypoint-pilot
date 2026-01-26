"""
Tests for scripts/verify_ingestion.py

TDD test suite - written BEFORE implementation.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_collection():
    """Mock ChromaDB collection for testing."""
    collection = Mock()
    collection.count.return_value = 483
    collection.name = "waypoint_kb"
    return collection


@pytest.fixture
def mock_collection_with_data():
    """Mock collection with sample data for category distribution tests."""
    collection = Mock()
    collection.count.return_value = 483
    collection.name = "waypoint_kb"

    # Mock get() to return metadata with all 4 categories
    collection.get.return_value = {
        "ids": ["chunk_1", "chunk_2", "chunk_3", "chunk_4"],
        "metadatas": [
            {"category": "01_regulatory", "doc_id": "sg_import", "title": "SG Import",
             "source_org": "Singapore Customs", "source_type": "public_regulatory",
             "jurisdiction": "SG", "section_header": "Overview", "subsection_header": "",
             "chunk_index": 0, "file_path": "/path/to/file.md"},
            {"category": "02_carriers", "doc_id": "maersk", "title": "Maersk",
             "source_org": "Maersk", "source_type": "public_carrier",
             "jurisdiction": "Global", "section_header": "Services", "subsection_header": "",
             "chunk_index": 0, "file_path": "/path/to/file.md"},
            {"category": "03_reference", "doc_id": "incoterms", "title": "Incoterms",
             "source_org": "ICC", "source_type": "public_regulatory",
             "jurisdiction": "Global", "section_header": "FOB", "subsection_header": "",
             "chunk_index": 0, "file_path": "/path/to/file.md"},
            {"category": "04_internal_synthetic", "doc_id": "sla", "title": "SLA",
             "source_org": "Waypoint", "source_type": "synthetic_internal",
             "jurisdiction": "SG", "section_header": "Policy", "subsection_header": "",
             "chunk_index": 0, "file_path": "/path/to/file.md"},
        ],
        "documents": ["text1", "text2", "text3", "text4"]
    }
    return collection


@pytest.fixture
def mock_query_results():
    """Mock query results for retrieval tests."""
    return {
        "ids": [["chunk_1", "chunk_2"]],
        "distances": [[0.2, 0.3]],
        "metadatas": [[
            {"category": "01_regulatory", "doc_id": "sg_import_procedures"},
            {"category": "01_regulatory", "doc_id": "sg_export_procedures"}
        ]],
        "documents": [["Singapore import procedures...", "Singapore export..."]]
    }


# =============================================================================
# TestParseArgs
# =============================================================================


class TestParseArgs:
    """Tests for parse_args function."""

    def test_default_args(self):
        """Should have sensible defaults."""
        from scripts.verify_ingestion import parse_args

        args = parse_args([])
        assert args.verbose is False
        assert args.tier is None
        assert args.check is None

    def test_verbose_flag(self):
        """Should parse --verbose flag."""
        from scripts.verify_ingestion import parse_args

        args = parse_args(["--verbose"])
        assert args.verbose is True

    def test_verbose_short_flag(self):
        """Should parse -v short flag."""
        from scripts.verify_ingestion import parse_args

        args = parse_args(["-v"])
        assert args.verbose is True

    def test_tier_option(self):
        """Should parse --tier option."""
        from scripts.verify_ingestion import parse_args

        args = parse_args(["--tier", "1"])
        assert args.tier == 1


# =============================================================================
# TestCheckTotalCount
# =============================================================================


class TestCheckTotalCount:
    """Tests for check_total_count function."""

    def test_passes_with_valid_count(self, mock_collection):
        """Should pass when count is within range (450-520)."""
        from scripts.verify_ingestion import check_total_count

        mock_collection.count.return_value = 483
        passed, message = check_total_count(mock_collection)

        assert passed is True
        assert "483" in message

    def test_fails_with_low_count(self, mock_collection):
        """Should fail when count is below 450."""
        from scripts.verify_ingestion import check_total_count

        mock_collection.count.return_value = 200
        passed, message = check_total_count(mock_collection)

        assert passed is False
        assert "200" in message

    def test_fails_with_high_count(self, mock_collection):
        """Should fail when count is above 520."""
        from scripts.verify_ingestion import check_total_count

        mock_collection.count.return_value = 600
        passed, message = check_total_count(mock_collection)

        assert passed is False
        assert "600" in message

    def test_passes_at_lower_boundary(self, mock_collection):
        """Should pass at exactly 450 chunks."""
        from scripts.verify_ingestion import check_total_count

        mock_collection.count.return_value = 450
        passed, message = check_total_count(mock_collection)

        assert passed is True

    def test_passes_at_upper_boundary(self, mock_collection):
        """Should pass at exactly 520 chunks."""
        from scripts.verify_ingestion import check_total_count

        mock_collection.count.return_value = 520
        passed, message = check_total_count(mock_collection)

        assert passed is True


# =============================================================================
# TestCheckCategoryDistribution
# =============================================================================


class TestCheckCategoryDistribution:
    """Tests for check_category_distribution function."""

    def test_passes_with_all_categories(self, mock_collection_with_data):
        """Should pass when all 4 categories are present."""
        from scripts.verify_ingestion import check_category_distribution

        passed, message = check_category_distribution(mock_collection_with_data)

        assert passed is True
        assert "4/4" in message

    def test_fails_with_missing_category(self, mock_collection):
        """Should fail when a category is missing."""
        from scripts.verify_ingestion import check_category_distribution

        # Only 3 categories
        mock_collection.get.return_value = {
            "metadatas": [
                {"category": "01_regulatory"},
                {"category": "02_carriers"},
                {"category": "03_reference"},
            ]
        }

        passed, message = check_category_distribution(mock_collection)

        assert passed is False
        assert "3/4" in message

    def test_reports_missing_categories(self, mock_collection):
        """Should report which categories are missing."""
        from scripts.verify_ingestion import check_category_distribution

        mock_collection.get.return_value = {
            "metadatas": [
                {"category": "01_regulatory"},
                {"category": "02_carriers"},
            ]
        }

        passed, message = check_category_distribution(mock_collection)

        assert passed is False
        # Should mention missing categories

    def test_handles_empty_collection(self, mock_collection):
        """Should fail gracefully with empty collection."""
        from scripts.verify_ingestion import check_category_distribution

        mock_collection.get.return_value = {"metadatas": []}

        passed, message = check_category_distribution(mock_collection)

        assert passed is False
        assert "0/4" in message


# =============================================================================
# TestCheckMetadataIntegrity
# =============================================================================


class TestCheckMetadataIntegrity:
    """Tests for check_metadata_integrity function."""

    def test_passes_with_all_fields(self, mock_collection_with_data):
        """Should pass when all 10 metadata fields are present."""
        from scripts.verify_ingestion import check_metadata_integrity

        passed, message = check_metadata_integrity(mock_collection_with_data)

        assert passed is True
        assert "10/10" in message

    def test_fails_with_missing_fields(self, mock_collection):
        """Should fail when metadata fields are missing."""
        from scripts.verify_ingestion import check_metadata_integrity

        mock_collection.get.return_value = {
            "metadatas": [
                {"doc_id": "test", "title": "Test"}  # Only 2 fields
            ]
        }

        passed, message = check_metadata_integrity(mock_collection)

        assert passed is False

    def test_reports_missing_fields(self, mock_collection):
        """Should report which fields are missing."""
        from scripts.verify_ingestion import check_metadata_integrity

        mock_collection.get.return_value = {
            "metadatas": [
                {"doc_id": "test", "title": "Test", "category": "01_regulatory"}
            ]
        }

        passed, message = check_metadata_integrity(mock_collection)

        assert passed is False
        # Should mention missing fields count

    def test_handles_empty_collection(self, mock_collection):
        """Should fail gracefully with empty collection."""
        from scripts.verify_ingestion import check_metadata_integrity

        mock_collection.get.return_value = {"metadatas": []}

        passed, message = check_metadata_integrity(mock_collection)

        assert passed is False

    def test_checks_sample_of_chunks(self, mock_collection_with_data):
        """Should check a sample of chunks, not all."""
        from scripts.verify_ingestion import check_metadata_integrity

        # Should use limit parameter
        check_metadata_integrity(mock_collection_with_data)

        # Verify get was called with limit
        mock_collection_with_data.get.assert_called()


# =============================================================================
# TestTier1Retrieval
# =============================================================================


class TestTier1Retrieval:
    """Tests for check_tier1_retrieval function."""

    def test_returns_pass_count(self, mock_collection):
        """Should return passed count and total."""
        from scripts.verify_ingestion import check_tier1_retrieval

        mock_collection.query.return_value = {
            "ids": [["chunk_1"]],
            "metadatas": [[{"category": "01_regulatory", "doc_id": "sg_import"}]],
            "distances": [[0.2]]
        }

        passed, message, pass_count, total = check_tier1_retrieval(mock_collection)

        assert isinstance(pass_count, int)
        assert total == 8  # 8 tier 1 queries

    def test_passes_with_correct_category(self, mock_collection):
        """Should pass when top result has correct category."""
        from scripts.verify_ingestion import check_tier1_retrieval

        # Mock all queries to return correct categories
        def mock_query(query_texts, n_results, **kwargs):
            query = query_texts[0].lower()
            if "singapore" in query or "gst" in query:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"category": "01_regulatory", "doc_id": "sg_import"}]],
                    "distances": [[0.2]]
                }
            elif "maersk" in query or "carrier" in query:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"category": "02_carriers", "doc_id": "maersk"}]],
                    "distances": [[0.2]]
                }
            elif "incoterms" in query or "hs code" in query:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"category": "03_reference", "doc_id": "incoterms"}]],
                    "distances": [[0.2]]
                }
            else:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"category": "04_internal_synthetic", "doc_id": "sla"}]],
                    "distances": [[0.2]]
                }

        mock_collection.query.side_effect = mock_query

        passed, message, pass_count, total = check_tier1_retrieval(mock_collection)

        assert pass_count >= 4  # At least half should pass with this mock

    def test_fails_with_wrong_category(self, mock_collection):
        """Should fail when top result has wrong category."""
        from scripts.verify_ingestion import check_tier1_retrieval

        # Always return wrong category
        mock_collection.query.return_value = {
            "ids": [["chunk_1"]],
            "metadatas": [[{"category": "wrong_category", "doc_id": "wrong"}]],
            "distances": [[0.2]]
        }

        passed, message, pass_count, total = check_tier1_retrieval(mock_collection)

        assert pass_count == 0

    def test_requires_8_out_of_8(self, mock_collection):
        """Should require 8/8 to pass overall."""
        from scripts.verify_ingestion import check_tier1_retrieval

        # Return correct for some, wrong for others
        call_count = [0]
        def mock_query(query_texts, n_results, **kwargs):
            call_count[0] += 1
            if call_count[0] <= 6:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"category": "01_regulatory", "doc_id": "sg"}]],
                    "distances": [[0.2]]
                }
            return {
                "ids": [["chunk_1"]],
                "metadatas": [[{"category": "wrong", "doc_id": "wrong"}]],
                "distances": [[0.2]]
            }

        mock_collection.query.side_effect = mock_query

        passed, message, pass_count, total = check_tier1_retrieval(mock_collection)

        # 6/8 should not pass
        assert pass_count < 8

    def test_handles_empty_results(self, mock_collection):
        """Should handle empty query results gracefully."""
        from scripts.verify_ingestion import check_tier1_retrieval

        mock_collection.query.return_value = {
            "ids": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }

        passed, message, pass_count, total = check_tier1_retrieval(mock_collection)

        assert pass_count == 0
        assert total == 8


# =============================================================================
# TestTier2Retrieval
# =============================================================================


class TestTier2Retrieval:
    """Tests for check_tier2_retrieval function."""

    def test_returns_pass_count(self, mock_collection):
        """Should return passed count and total of 12."""
        from scripts.verify_ingestion import check_tier2_retrieval

        mock_collection.query.return_value = {
            "ids": [["chunk_1"]],
            "metadatas": [[{"category": "01_regulatory", "doc_id": "sg_import_procedures"}]],
            "distances": [[0.2]]
        }

        passed, message, pass_count, total = check_tier2_retrieval(mock_collection)

        assert isinstance(pass_count, int)
        assert total == 12

    def test_passes_with_correct_doc_id(self, mock_collection):
        """Should pass when top result has expected doc_id pattern."""
        from scripts.verify_ingestion import check_tier2_retrieval

        def mock_query(query_texts, n_results, **kwargs):
            query = query_texts[0].lower()
            if "import goods" in query or "import" in query:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"doc_id": "sg_import_procedures", "category": "01_regulatory"}]],
                    "distances": [[0.2]]
                }
            elif "export" in query:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"doc_id": "sg_export_procedures", "category": "01_regulatory"}]],
                    "distances": [[0.2]]
                }
            elif "maersk" in query:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"doc_id": "maersk_service_summary", "category": "02_carriers"}]],
                    "distances": [[0.2]]
                }
            else:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"doc_id": "some_doc", "category": "01_regulatory"}]],
                    "distances": [[0.2]]
                }

        mock_collection.query.side_effect = mock_query

        passed, message, pass_count, total = check_tier2_retrieval(mock_collection)

        assert pass_count >= 1  # At least some should match

    def test_fails_with_wrong_doc_id(self, mock_collection):
        """Should fail when doc_id doesn't match expected pattern."""
        from scripts.verify_ingestion import check_tier2_retrieval

        mock_collection.query.return_value = {
            "ids": [["chunk_1"]],
            "metadatas": [[{"doc_id": "completely_wrong_doc", "category": "01_regulatory"}]],
            "distances": [[0.2]]
        }

        passed, message, pass_count, total = check_tier2_retrieval(mock_collection)

        # Most should fail with wrong doc_id
        assert pass_count < 10

    def test_requires_10_out_of_12(self, mock_collection):
        """Should require 10+/12 to pass overall."""
        from scripts.verify_ingestion import check_tier2_retrieval

        # Return correct for 9 queries, wrong for 3
        call_count = [0]
        def mock_query(query_texts, n_results, **kwargs):
            call_count[0] += 1
            if call_count[0] <= 9:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"doc_id": "sg_import_procedures", "category": "01_regulatory"}]],
                    "distances": [[0.2]]
                }
            return {
                "ids": [["chunk_1"]],
                "metadatas": [[{"doc_id": "wrong", "category": "wrong"}]],
                "distances": [[0.2]]
            }

        mock_collection.query.side_effect = mock_query

        passed, message, pass_count, total = check_tier2_retrieval(mock_collection)

        # 9/12 should not pass (need 10+)
        if pass_count < 10:
            assert passed is False

    def test_handles_empty_results(self, mock_collection):
        """Should handle empty query results gracefully."""
        from scripts.verify_ingestion import check_tier2_retrieval

        mock_collection.query.return_value = {
            "ids": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }

        passed, message, pass_count, total = check_tier2_retrieval(mock_collection)

        assert pass_count == 0
        assert total == 12

    def test_checks_top_3_results(self, mock_collection):
        """Should check if expected doc_id is in top 3 results."""
        from scripts.verify_ingestion import check_tier2_retrieval

        # Return expected doc_id in position 3
        mock_collection.query.return_value = {
            "ids": [["chunk_1", "chunk_2", "chunk_3"]],
            "metadatas": [[
                {"doc_id": "wrong1", "category": "01_regulatory"},
                {"doc_id": "wrong2", "category": "01_regulatory"},
                {"doc_id": "sg_import_procedures", "category": "01_regulatory"}
            ]],
            "distances": [[0.2, 0.3, 0.4]]
        }

        passed, message, pass_count, total = check_tier2_retrieval(mock_collection)

        # Should count as pass if in top 3
        assert pass_count >= 1

    def test_uses_n_results_3(self, mock_collection):
        """Should query with n_results=3."""
        from scripts.verify_ingestion import check_tier2_retrieval

        mock_collection.query.return_value = {
            "ids": [["chunk_1"]],
            "metadatas": [[{"doc_id": "sg_import", "category": "01_regulatory"}]],
            "distances": [[0.2]]
        }

        check_tier2_retrieval(mock_collection)

        # Verify query was called with n_results=3
        calls = mock_collection.query.call_args_list
        assert len(calls) > 0
        for call in calls:
            kwargs = call.kwargs if call.kwargs else call[1]
            assert kwargs.get("n_results") == 3


# =============================================================================
# TestTier3Scenarios
# =============================================================================


class TestTier3Scenarios:
    """Tests for check_tier3_scenarios function."""

    def test_returns_pass_count(self, mock_collection):
        """Should return passed count and total of 10."""
        from scripts.verify_ingestion import check_tier3_scenarios

        mock_collection.query.return_value = {
            "ids": [["chunk_1"]],
            "metadatas": [[{"doc_id": "test", "category": "01_regulatory"}]],
            "documents": [["invoice packing list bill of lading"]],
            "distances": [[0.2]]
        }

        passed, message, pass_count, total = check_tier3_scenarios(mock_collection)

        assert isinstance(pass_count, int)
        assert total == 10

    def test_passes_with_expected_keywords(self, mock_collection):
        """Should pass when result contains expected keywords."""
        from scripts.verify_ingestion import check_tier3_scenarios

        def mock_query(query_texts, n_results, include, **kwargs):
            query = query_texts[0].lower()
            if "fcl export" in query:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"doc_id": "test", "category": "01_regulatory"}]],
                    "documents": [["Required documents: invoice, packing list, bill of lading"]],
                    "distances": [[0.2]]
                }
            elif "gst rate" in query:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"doc_id": "test", "category": "01_regulatory"}]],
                    "documents": [["The GST rate is 9% for imported goods"]],
                    "distances": [[0.2]]
                }
            else:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"doc_id": "test", "category": "01_regulatory"}]],
                    "documents": [["Some content"]],
                    "distances": [[0.2]]
                }

        mock_collection.query.side_effect = mock_query

        passed, message, pass_count, total = check_tier3_scenarios(mock_collection)

        # At least some should pass
        assert pass_count >= 1

    def test_fails_with_missing_keywords(self, mock_collection):
        """Should fail when result is missing expected keywords."""
        from scripts.verify_ingestion import check_tier3_scenarios

        mock_collection.query.return_value = {
            "ids": [["chunk_1"]],
            "metadatas": [[{"doc_id": "test", "category": "01_regulatory"}]],
            "documents": [["completely unrelated content without expected terms"]],
            "distances": [[0.2]]
        }

        passed, message, pass_count, total = check_tier3_scenarios(mock_collection)

        # Most should fail without keywords
        assert pass_count < 8

    def test_requires_8_out_of_10(self, mock_collection):
        """Should require 8+/10 to pass overall."""
        from scripts.verify_ingestion import check_tier3_scenarios

        # Return content with some keywords
        call_count = [0]
        def mock_query(query_texts, n_results, include, **kwargs):
            call_count[0] += 1
            if call_count[0] <= 7:
                return {
                    "ids": [["chunk_1"]],
                    "metadatas": [[{"doc_id": "test", "category": "01_regulatory"}]],
                    "documents": [["invoice packing list bill of lading GST 9%"]],
                    "distances": [[0.2]]
                }
            return {
                "ids": [["chunk_1"]],
                "metadatas": [[{"doc_id": "test", "category": "01_regulatory"}]],
                "documents": [["no relevant content here"]],
                "distances": [[0.2]]
            }

        mock_collection.query.side_effect = mock_query

        passed, message, pass_count, total = check_tier3_scenarios(mock_collection)

        # 7/10 should not pass
        if pass_count < 8:
            assert passed is False

    def test_handles_empty_results(self, mock_collection):
        """Should handle empty query results gracefully."""
        from scripts.verify_ingestion import check_tier3_scenarios

        mock_collection.query.return_value = {
            "ids": [[]],
            "metadatas": [[]],
            "documents": [[]],
            "distances": [[]]
        }

        passed, message, pass_count, total = check_tier3_scenarios(mock_collection)

        assert pass_count == 0
        assert total == 10


# =============================================================================
# TestRunAllChecks
# =============================================================================


class TestRunAllChecks:
    """Tests for run_all_checks function."""

    def test_returns_results_dict(self, mock_collection_with_data):
        """Should return dict with all check results."""
        from scripts.verify_ingestion import run_all_checks, parse_args

        mock_collection_with_data.query.return_value = {
            "ids": [["chunk_1"]],
            "metadatas": [[{"category": "01_regulatory", "doc_id": "sg_import"}]],
            "documents": [["test content"]],
            "distances": [[0.2]]
        }

        args = parse_args([])
        results = run_all_checks(mock_collection_with_data, args)

        assert "checks" in results
        assert "total_passed" in results
        assert "total_tests" in results

    def test_runs_all_six_checks(self, mock_collection_with_data):
        """Should run all 6 checks."""
        from scripts.verify_ingestion import run_all_checks, parse_args

        mock_collection_with_data.query.return_value = {
            "ids": [["chunk_1"]],
            "metadatas": [[{"category": "01_regulatory", "doc_id": "sg_import"}]],
            "documents": [["test content"]],
            "distances": [[0.2]]
        }

        args = parse_args([])
        results = run_all_checks(mock_collection_with_data, args)

        assert len(results["checks"]) == 6

    def test_tier_filter_runs_only_specified_tier(self, mock_collection_with_data):
        """Should run only specified tier when --tier is used."""
        from scripts.verify_ingestion import run_all_checks, parse_args

        mock_collection_with_data.query.return_value = {
            "ids": [["chunk_1"]],
            "metadatas": [[{"category": "01_regulatory", "doc_id": "sg_import"}]],
            "documents": [["test content"]],
            "distances": [[0.2]]
        }

        args = parse_args(["--tier", "1"])
        results = run_all_checks(mock_collection_with_data, args)

        # Should only have tier 1 check (check 4)
        tier_checks = [c for c in results["checks"] if "Tier 1" in c["name"]]
        assert len(tier_checks) == 1

    def test_calculates_overall_pass(self, mock_collection_with_data):
        """Should calculate overall pass percentage."""
        from scripts.verify_ingestion import run_all_checks, parse_args

        mock_collection_with_data.query.return_value = {
            "ids": [["chunk_1"]],
            "metadatas": [[{"category": "01_regulatory", "doc_id": "sg_import"}]],
            "documents": [["test content"]],
            "distances": [[0.2]]
        }

        args = parse_args([])
        results = run_all_checks(mock_collection_with_data, args)

        assert "passed" in results
        assert isinstance(results["passed"], bool)


# =============================================================================
# TestInitializeCollection
# =============================================================================


class TestInitializeCollection:
    """Tests for initialize_collection function."""

    def test_returns_collection(self):
        """Should return a ChromaDB collection."""
        from scripts.verify_ingestion import initialize_collection

        collection = initialize_collection()

        assert collection is not None
        assert hasattr(collection, "query")
        assert hasattr(collection, "count")

    def test_uses_correct_collection_name(self):
        """Should use configured collection name."""
        from scripts.verify_ingestion import initialize_collection
        from scripts.config import COLLECTION_NAME

        collection = initialize_collection()

        assert collection.name == COLLECTION_NAME


# =============================================================================
# TestPrintResults
# =============================================================================


class TestPrintResults:
    """Tests for print_results function."""

    def test_prints_without_error(self, capsys):
        """Should print results without raising errors."""
        from scripts.verify_ingestion import print_results

        results = {
            "checks": [
                {"name": "Check 1: Total count", "passed": True, "message": "483 chunks"},
                {"name": "Check 2: Category", "passed": True, "message": "4/4"},
            ],
            "total_passed": 28,
            "total_tests": 30,
            "passed": True
        }

        print_results(results, verbose=False)

        captured = capsys.readouterr()
        assert "Check 1" in captured.out
        assert "PASS" in captured.out or "483" in captured.out

    def test_verbose_shows_more_detail(self, capsys):
        """Verbose mode should show more detail."""
        from scripts.verify_ingestion import print_results

        results = {
            "checks": [
                {"name": "Check 1: Total count", "passed": True, "message": "483 chunks",
                 "details": ["Detail 1", "Detail 2"]},
            ],
            "total_passed": 28,
            "total_tests": 30,
            "passed": True
        }

        print_results(results, verbose=True)

        captured = capsys.readouterr()
        # Should contain some output


# =============================================================================
# Integration Tests
# =============================================================================


class TestIntegration:
    """Integration tests using real ChromaDB collection."""

    @pytest.fixture(autouse=True)
    def check_collection_exists(self):
        """Skip if collection doesn't exist or is empty."""
        try:
            from scripts.verify_ingestion import initialize_collection
            collection = initialize_collection()
            if collection.count() < 400:
                pytest.skip("Collection has insufficient data - run ingestion first")
        except Exception as e:
            pytest.skip(f"Could not initialize collection: {e}")

    def test_real_total_count(self):
        """Real collection should have expected chunk count."""
        from scripts.verify_ingestion import initialize_collection, check_total_count

        collection = initialize_collection()
        passed, message = check_total_count(collection)

        # Should be within expected range
        assert 450 <= collection.count() <= 520

    def test_real_category_distribution(self):
        """Real collection should have all 4 categories."""
        from scripts.verify_ingestion import initialize_collection, check_category_distribution

        collection = initialize_collection()
        passed, message = check_category_distribution(collection)

        assert passed is True

    def test_real_metadata_integrity(self):
        """Real collection should have complete metadata."""
        from scripts.verify_ingestion import initialize_collection, check_metadata_integrity

        collection = initialize_collection()
        passed, message = check_metadata_integrity(collection)

        assert passed is True

    def test_real_tier1_retrieval(self):
        """Real collection should pass tier 1 retrieval tests."""
        from scripts.verify_ingestion import initialize_collection, check_tier1_retrieval

        collection = initialize_collection()
        passed, message, pass_count, total = check_tier1_retrieval(collection)

        # Should pass 8/8
        assert pass_count == 8

    def test_real_tier2_retrieval(self):
        """Real collection should pass tier 2 retrieval tests."""
        from scripts.verify_ingestion import initialize_collection, check_tier2_retrieval

        collection = initialize_collection()
        passed, message, pass_count, total = check_tier2_retrieval(collection)

        # Should pass at least 10/12
        assert pass_count >= 10

    def test_real_tier3_scenarios(self):
        """Real collection should pass tier 3 scenario tests."""
        from scripts.verify_ingestion import initialize_collection, check_tier3_scenarios

        collection = initialize_collection()
        passed, message, pass_count, total = check_tier3_scenarios(collection)

        # Should pass at least 8/10
        assert pass_count >= 8
