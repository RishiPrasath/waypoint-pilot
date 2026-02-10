"""
Tests for pdf_extractor.py — PDF to markdown extraction tool.

TDD Red phase: Write all tests before implementation.
"""

import csv
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from scripts.pdf_extractor import (
    assess_quality,
    clean_extracted_content,
    extract_pdf_to_markdown,
    generate_frontmatter,
    process_batch,
    process_single,
    write_markdown_file,
)


# ---------------------------------------------------------------------------
# clean_extracted_content tests
# ---------------------------------------------------------------------------


class TestCleanExtractedContent:
    def test_collapses_blank_lines(self):
        """3+ consecutive blank lines should collapse to 2."""
        content = "Line 1\n\n\n\n\nLine 2"
        result = clean_extracted_content(content)
        assert "\n\n\n" not in result
        assert "Line 1\n\n" in result
        assert "Line 2" in result

    def test_normalizes_unicode_smart_quotes(self):
        """Smart quotes should become straight quotes."""
        content = "\u201cHello\u201d and \u2018world\u2019"
        result = clean_extracted_content(content)
        assert '"Hello"' in result
        assert "'world'" in result

    def test_normalizes_unicode_em_dashes(self):
        """Em-dashes and en-dashes should become --."""
        content = "value\u2014other and range\u2013end"
        result = clean_extracted_content(content)
        assert "value--other" in result
        assert "range--end" in result

    def test_strips_trailing_whitespace(self):
        """Trailing spaces on each line should be removed."""
        content = "Line 1   \nLine 2  \nLine 3"
        result = clean_extracted_content(content)
        lines = result.split("\n")
        for line in lines:
            assert line == line.rstrip(), f"Trailing whitespace on: {repr(line)}"

    def test_ends_with_single_newline(self):
        """Output should end with exactly one newline."""
        content = "Some content\n\n\n"
        result = clean_extracted_content(content)
        assert result.endswith("\n")
        assert not result.endswith("\n\n")

    def test_preserves_meaningful_structure(self):
        """Double newlines (paragraph breaks) should be preserved."""
        content = "Paragraph 1\n\nParagraph 2"
        result = clean_extracted_content(content)
        assert "Paragraph 1\n\nParagraph 2" in result


# ---------------------------------------------------------------------------
# assess_quality tests
# ---------------------------------------------------------------------------


class TestAssessQuality:
    def test_high_quality(self):
        """>=500 chars with headings should be HIGH."""
        content = "x" * 500
        assert assess_quality(content, heading_count=3) == "HIGH"

    def test_high_quality_many_headings(self):
        """Long content with many headings is HIGH."""
        content = "x" * 1000
        assert assess_quality(content, heading_count=10) == "HIGH"

    def test_medium_quality_short_with_headings(self):
        """200-499 chars with some headings should be MEDIUM."""
        content = "x" * 300
        assert assess_quality(content, heading_count=2) == "MEDIUM"

    def test_medium_quality_long_no_headings(self):
        """>=500 chars but no headings should be MEDIUM."""
        content = "x" * 600
        assert assess_quality(content, heading_count=0) == "MEDIUM"

    def test_low_quality_very_short(self):
        """<200 chars should be LOW."""
        content = "x" * 100
        assert assess_quality(content, heading_count=0) == "LOW"

    def test_low_quality_empty(self):
        """Empty content should be LOW."""
        assert assess_quality("", heading_count=0) == "LOW"


# ---------------------------------------------------------------------------
# generate_frontmatter tests
# ---------------------------------------------------------------------------


class TestGenerateFrontmatter:
    def _make_result(self, **overrides):
        base = {
            "content": "# Test\n\nSome content here.",
            "page_count": 5,
            "char_count": 500,
            "heading_count": 3,
            "quality": "HIGH",
            "title": "Test Document",
            "source_filename": "test_doc.pdf",
        }
        base.update(overrides)
        return base

    def test_has_required_fields(self):
        """Frontmatter should contain all required YAML fields."""
        result = self._make_result()
        fm_str = generate_frontmatter(result)
        parsed = yaml.safe_load(fm_str)

        required_fields = [
            "title",
            "source_organization",
            "source_urls",
            "source_pdfs",
            "source_type",
            "last_updated",
            "jurisdiction",
            "category",
            "use_cases",
            "keywords",
            "answers_queries",
            "related_documents",
        ]
        for field in required_fields:
            assert field in parsed, f"Missing field: {field}"

    def test_autofills_title(self):
        """Title should be extracted from the first heading."""
        result = self._make_result(title="My Custom Title")
        fm_str = generate_frontmatter(result)
        parsed = yaml.safe_load(fm_str)
        assert "My Custom Title" in parsed["title"]

    def test_autofills_filename(self):
        """source_pdfs should contain the original PDF filename."""
        result = self._make_result(source_filename="customs_guide.pdf")
        fm_str = generate_frontmatter(result)
        parsed = yaml.safe_load(fm_str)
        assert len(parsed["source_pdfs"]) >= 1
        assert parsed["source_pdfs"][0]["filename"] == "customs_guide.pdf"

    def test_parseable_yaml(self):
        """Generated frontmatter should parse as valid YAML."""
        result = self._make_result()
        fm_str = generate_frontmatter(result)
        parsed = yaml.safe_load(fm_str)
        assert isinstance(parsed, dict)

    def test_todo_placeholders_present(self):
        """Fields not auto-filled should have [TODO] placeholders."""
        result = self._make_result()
        fm_str = generate_frontmatter(result)
        assert "[TODO" in fm_str


# ---------------------------------------------------------------------------
# write_markdown_file tests
# ---------------------------------------------------------------------------


class TestWriteMarkdownFile:
    def test_creates_file(self, tmp_path):
        """write_markdown_file should create a file with frontmatter + content."""
        output = tmp_path / "output.md"
        frontmatter_str = "---\ntitle: Test\n---"
        content = "# Heading\n\nBody text."

        write_markdown_file(output, frontmatter_str, content)

        assert output.exists()
        text = output.read_text(encoding="utf-8")
        assert "---" in text
        assert "title: Test" in text
        assert "# Heading" in text
        assert "Body text." in text

    def test_creates_parent_dirs(self, tmp_path):
        """Should create parent directories if they don't exist."""
        output = tmp_path / "subdir" / "deep" / "output.md"
        write_markdown_file(output, "---\ntitle: Test\n---", "Content")
        assert output.exists()


# ---------------------------------------------------------------------------
# extract_pdf_to_markdown tests (mocked)
# ---------------------------------------------------------------------------


class TestExtractPdfToMarkdown:
    def _mock_fitz(self, mock_fitz_mod, page_count=5):
        """Helper to set up fitz mock with a given page count."""
        mock_doc = MagicMock()
        mock_doc.__len__ = MagicMock(return_value=page_count)
        mock_fitz_mod.open.return_value = mock_doc

    @patch("scripts.pdf_extractor.fitz")
    @patch("scripts.pdf_extractor.pymupdf4llm")
    def test_process_single_with_mock_pdf(self, mock_lib, mock_fitz, tmp_path):
        """Full pipeline should work with mocked pymupdf4llm extraction."""
        # Create a fake PDF file (just needs to exist for path checks)
        pdf_file = tmp_path / "sample.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 fake content")

        mock_lib.to_markdown.return_value = (
            "# Sample Document\n\n"
            "This is the extracted content from the PDF.\n\n"
            "## Section 2\n\n"
            "More content here with details about customs procedures.\n" * 10
        )
        self._mock_fitz(mock_fitz, page_count=3)

        result = process_single(pdf_file)

        assert result["source_filename"] == "sample.pdf"
        assert result["page_count"] == 3
        assert result["char_count"] > 0
        assert result["quality"] in ("HIGH", "MEDIUM", "LOW")
        assert result["title"] == "Sample Document"

        # Check output file was created
        output_md = pdf_file.with_suffix(".md")
        assert output_md.exists()

        # Check it's parseable by reading it
        text = output_md.read_text(encoding="utf-8")
        assert "---" in text
        assert "Sample Document" in text

    @patch("scripts.pdf_extractor.fitz")
    @patch("scripts.pdf_extractor.pymupdf4llm")
    def test_process_single_custom_output(self, mock_lib, mock_fitz, tmp_path):
        """--output flag should write to a custom path."""
        pdf_file = tmp_path / "input.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 fake")
        output_file = tmp_path / "custom_output.md"

        mock_lib.to_markdown.return_value = "# Title\n\nContent.\n" * 20
        self._mock_fitz(mock_fitz)

        result = process_single(pdf_file, output_path=output_file)

        assert output_file.exists()
        assert not pdf_file.with_suffix(".md").exists()

    @patch("scripts.pdf_extractor.fitz")
    @patch("scripts.pdf_extractor.pymupdf4llm")
    def test_process_single_output_dir(self, mock_lib, mock_fitz, tmp_path):
        """--output-dir flag should write to a specific directory."""
        pdf_file = tmp_path / "input.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 fake")
        out_dir = tmp_path / "output_dir"
        out_dir.mkdir()

        mock_lib.to_markdown.return_value = "# Title\n\nContent.\n" * 20
        self._mock_fitz(mock_fitz)

        result = process_single(pdf_file, output_dir=out_dir)

        expected = out_dir / "input.md"
        assert expected.exists()


# ---------------------------------------------------------------------------
# process_batch tests (mocked)
# ---------------------------------------------------------------------------


class TestProcessBatch:
    def _mock_fitz(self, mock_fitz_mod, page_count=5):
        mock_doc = MagicMock()
        mock_doc.__len__ = MagicMock(return_value=page_count)
        mock_fitz_mod.open.return_value = mock_doc

    @patch("scripts.pdf_extractor.fitz")
    @patch("scripts.pdf_extractor.pymupdf4llm")
    def test_batch_processes_all_pdfs(self, mock_lib, mock_fitz, tmp_path):
        """Batch mode should process all PDF files in directory."""
        mock_lib.to_markdown.return_value = "# Doc\n\nContent.\n" * 20
        self._mock_fitz(mock_fitz)

        for name in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
            (tmp_path / name).write_bytes(b"%PDF-1.4 fake")

        results = process_batch(tmp_path)

        assert len(results) == 3
        assert (tmp_path / "doc1.md").exists()
        assert (tmp_path / "doc2.md").exists()
        assert (tmp_path / "doc3.md").exists()

    @patch("scripts.pdf_extractor.fitz")
    @patch("scripts.pdf_extractor.pymupdf4llm")
    def test_batch_skips_existing(self, mock_lib, mock_fitz, tmp_path):
        """Batch mode should skip PDFs that already have .md counterparts."""
        mock_lib.to_markdown.return_value = "# Doc\n\nContent.\n" * 20
        self._mock_fitz(mock_fitz)

        (tmp_path / "doc1.pdf").write_bytes(b"%PDF-1.4 fake")
        (tmp_path / "doc2.pdf").write_bytes(b"%PDF-1.4 fake")
        # Pre-create doc1.md so it should be skipped
        (tmp_path / "doc1.md").write_text("existing", encoding="utf-8")

        results = process_batch(tmp_path)

        assert len(results) == 1
        assert results[0]["source_filename"] == "doc2.pdf"

    @patch("scripts.pdf_extractor.fitz")
    @patch("scripts.pdf_extractor.pymupdf4llm")
    def test_batch_force_reprocesses(self, mock_lib, mock_fitz, tmp_path):
        """--force should reprocess files that already have .md counterparts."""
        mock_lib.to_markdown.return_value = "# Doc\n\nContent.\n" * 20
        self._mock_fitz(mock_fitz)

        (tmp_path / "doc1.pdf").write_bytes(b"%PDF-1.4 fake")
        (tmp_path / "doc1.md").write_text("old content", encoding="utf-8")

        results = process_batch(tmp_path, force=True)

        assert len(results) == 1
        # File should be overwritten with new content
        new_content = (tmp_path / "doc1.md").read_text(encoding="utf-8")
        assert new_content != "old content"

    @patch("scripts.pdf_extractor.fitz")
    @patch("scripts.pdf_extractor.pymupdf4llm")
    def test_batch_generates_csv(self, mock_lib, mock_fitz, tmp_path):
        """Batch mode should generate extraction_summary.csv."""
        mock_lib.to_markdown.return_value = "# Doc\n\nContent.\n" * 20
        self._mock_fitz(mock_fitz)

        (tmp_path / "doc1.pdf").write_bytes(b"%PDF-1.4 fake")

        process_batch(tmp_path)

        csv_path = tmp_path / "extraction_summary.csv"
        assert csv_path.exists()

        with open(csv_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 1
            assert "filename" in rows[0]
            assert "quality" in rows[0]
            assert "pages" in rows[0]
            assert "chars" in rows[0]

    @patch("scripts.pdf_extractor.fitz")
    @patch("scripts.pdf_extractor.pymupdf4llm")
    def test_batch_with_output_dir(self, mock_lib, mock_fitz, tmp_path):
        """Batch mode with --output-dir writes files to specified dir."""
        mock_lib.to_markdown.return_value = "# Doc\n\nContent.\n" * 20
        self._mock_fitz(mock_fitz)

        pdf_dir = tmp_path / "pdfs"
        pdf_dir.mkdir()
        (pdf_dir / "doc1.pdf").write_bytes(b"%PDF-1.4 fake")

        out_dir = tmp_path / "output"
        out_dir.mkdir()

        results = process_batch(pdf_dir, output_dir=out_dir)

        assert (out_dir / "doc1.md").exists()
        # CSV should still go in input dir
        assert (pdf_dir / "extraction_summary.csv").exists()


# ---------------------------------------------------------------------------
# Error handling tests
# ---------------------------------------------------------------------------


class TestErrorHandling:
    @patch("scripts.pdf_extractor.pymupdf4llm")
    def test_encrypted_pdf_graceful(self, mock_lib, tmp_path):
        """Encrypted PDF should not crash, returns result with LOW quality."""
        pdf_file = tmp_path / "encrypted.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 fake encrypted")

        mock_lib.to_markdown.side_effect = Exception(
            "cannot open encrypted document"
        )

        result = process_single(pdf_file)

        assert result is not None
        assert result["quality"] == "LOW"
        assert result["char_count"] == 0

    def test_missing_file_raises_error(self, tmp_path):
        """Missing PDF file should raise FileNotFoundError."""
        pdf_file = tmp_path / "nonexistent.pdf"

        with pytest.raises(FileNotFoundError):
            process_single(pdf_file)
