"""
PDF to Markdown extraction tool for Waypoint knowledge base.

Converts PDF files to well-structured markdown with YAML frontmatter
templates, quality assessment, and batch processing support. Output
integrates with the existing ingestion pipeline (process_docs → chunker → ingest).

Uses pymupdf4llm for text extraction.

Usage:
    # Single file
    python scripts/pdf_extractor.py path/to/file.pdf

    # Single file with custom output
    python scripts/pdf_extractor.py file.pdf --output path/to/output.md
    python scripts/pdf_extractor.py file.pdf --output-dir path/to/dir/

    # Batch mode
    python scripts/pdf_extractor.py --batch path/to/pdfs/
    python scripts/pdf_extractor.py --batch path/to/pdfs/ --force
"""

import argparse
import csv
import logging
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

# Ensure parent directory is in path for direct script execution
sys.path.insert(0, str(Path(__file__).parent.parent))

import fitz
import pymupdf4llm

from scripts.config import LOG_LEVEL, PIPELINE_ROOT

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Content cleaning
# ---------------------------------------------------------------------------


def clean_extracted_content(content: str) -> str:
    """
    Remove PDF artifacts, normalize whitespace and Unicode.

    Applies:
    - Smart quotes → straight quotes
    - Em/en-dashes → --
    - Collapse 3+ blank lines to 2
    - Strip trailing whitespace per line
    - Ensure single trailing newline

    Args:
        content: Raw extracted markdown text

    Returns:
        Cleaned markdown text
    """
    text = content

    # Normalize Unicode: smart quotes → straight quotes
    text = text.replace("\u201c", '"')  # left double
    text = text.replace("\u201d", '"')  # right double
    text = text.replace("\u2018", "'")  # left single
    text = text.replace("\u2019", "'")  # right single

    # Em-dash and en-dash → --
    text = text.replace("\u2014", "--")  # em-dash
    text = text.replace("\u2013", "--")  # en-dash

    # Normalize other common Unicode replacements
    text = text.replace("\u2026", "...")  # ellipsis
    text = text.replace("\u00a0", " ")   # non-breaking space

    # Strip trailing whitespace from each line
    lines = [line.rstrip() for line in text.split("\n")]
    text = "\n".join(lines)

    # Collapse 3+ consecutive blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Ensure ends with exactly one newline
    text = text.rstrip("\n") + "\n"

    return text


# ---------------------------------------------------------------------------
# Quality assessment
# ---------------------------------------------------------------------------


def assess_quality(content: str, heading_count: int) -> str:
    """
    Assess extraction quality and return a flag.

    Args:
        content: Extracted text content
        heading_count: Number of markdown headings found

    Returns:
        "HIGH", "MEDIUM", or "LOW"
    """
    char_count = len(content)

    if char_count >= 500 and heading_count >= 1:
        return "HIGH"
    elif char_count >= 200:
        return "MEDIUM"
    else:
        return "LOW"


# ---------------------------------------------------------------------------
# Title extraction
# ---------------------------------------------------------------------------


def _extract_title(content: str, filename: str) -> str:
    """
    Extract title from first heading in content, fallback to filename.

    Args:
        content: Markdown content
        filename: PDF filename (without extension) as fallback

    Returns:
        Extracted or derived title string
    """
    # Look for first H1 or H2
    match = re.search(r"^#{1,2}\s+(.+)$", content, re.MULTILINE)
    if match:
        # Strip any leading # characters (PDF extraction may double them)
        title = match.group(1).strip().lstrip("#").strip()
        if title:
            return title

    # Fallback: clean up filename
    return filename.replace("_", " ").replace("-", " ").title()


# ---------------------------------------------------------------------------
# Frontmatter generation
# ---------------------------------------------------------------------------


def generate_frontmatter(extraction_result: dict) -> str:
    """
    Generate YAML frontmatter template from extraction metadata.

    Auto-fills title, source PDF filename, and retrieved date.
    Other fields use [TODO] placeholders for manual completion.

    Args:
        extraction_result: Dict from extract_pdf_to_markdown()

    Returns:
        YAML frontmatter string (without --- delimiters)
    """
    today = date.today().isoformat()
    title = extraction_result["title"]
    filename = extraction_result["source_filename"]

    frontmatter = {
        "title": title,
        "source_organization": "[TODO: Organization name]",
        "source_urls": [
            {
                "url": "[TODO: Source webpage URL]",
                "description": "[TODO: What this page covers]",
                "retrieved_date": today,
            }
        ],
        "source_pdfs": [
            {
                "filename": filename,
                "source_url": "[TODO: URL where PDF was downloaded]",
                "description": title,
                "retrieved_date": today,
            }
        ],
        "source_type": "[TODO: public_regulatory | public_carrier | synthetic_internal]",
        "last_updated": today,
        "jurisdiction": "[TODO: SG | MY | ID | TH | VN | PH | ASEAN | Global]",
        "category": "[TODO: customs | carrier | policy | procedure | reference]",
        "use_cases": [],
        "keywords": [],
        "answers_queries": [],
        "related_documents": [],
    }

    # Use yaml.dump for clean serialization
    import yaml

    return yaml.dump(
        frontmatter,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=120,
    )


# ---------------------------------------------------------------------------
# File writing
# ---------------------------------------------------------------------------


def write_markdown_file(
    output_path: Path, frontmatter: str, content: str
) -> None:
    """
    Write the final markdown file with frontmatter + content.

    Args:
        output_path: Path to write the .md file
        frontmatter: YAML frontmatter string (without --- delimiters)
        content: Cleaned markdown content
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    full_content = f"---\n{frontmatter}---\n\n{content}"

    output_path.write_text(full_content, encoding="utf-8")
    logger.info(f"Wrote: {output_path}")


# ---------------------------------------------------------------------------
# PDF extraction
# ---------------------------------------------------------------------------


def extract_pdf_to_markdown(pdf_path: Path) -> dict:
    """
    Extract text from a PDF and convert to markdown.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Dict with keys: content, page_count, char_count, heading_count,
        quality, title, source_filename
    """
    logger.info(f"Extracting: {pdf_path.name}")

    md_text = pymupdf4llm.to_markdown(str(pdf_path))

    # Clean the content
    cleaned = clean_extracted_content(md_text)

    # Count headings
    heading_count = len(re.findall(r"^#{1,6}\s+", cleaned, re.MULTILINE))

    # Get page count via PyMuPDF directly
    doc = fitz.open(str(pdf_path))
    page_count = len(doc)
    doc.close()

    # Extract title
    title = _extract_title(cleaned, pdf_path.stem)

    # Assess quality
    quality = assess_quality(cleaned, heading_count)

    result = {
        "content": cleaned,
        "page_count": page_count,
        "char_count": len(cleaned),
        "heading_count": heading_count,
        "quality": quality,
        "title": title,
        "source_filename": pdf_path.name,
    }

    logger.info(
        f"  → {page_count} pages, {len(cleaned)} chars, "
        f"{heading_count} headings, quality={quality}"
    )

    return result


# ---------------------------------------------------------------------------
# Single file processing
# ---------------------------------------------------------------------------


def process_single(
    pdf_path: Path,
    output_path: Path | None = None,
    output_dir: Path | None = None,
) -> dict:
    """
    Process a single PDF file to markdown.

    Args:
        pdf_path: Path to the PDF file
        output_path: Optional specific output file path
        output_dir: Optional output directory (filename derived from PDF)

    Returns:
        Extraction result dict

    Raises:
        FileNotFoundError: If pdf_path does not exist
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Determine output path
    if output_path:
        out = Path(output_path)
    elif output_dir:
        out = Path(output_dir) / pdf_path.with_suffix(".md").name
    else:
        out = pdf_path.with_suffix(".md")

    # Extract
    try:
        result = extract_pdf_to_markdown(pdf_path)
    except Exception as e:
        logger.warning(f"Extraction failed for {pdf_path.name}: {e}")
        result = {
            "content": "",
            "page_count": 0,
            "char_count": 0,
            "heading_count": 0,
            "quality": "LOW",
            "title": pdf_path.stem.replace("_", " ").title(),
            "source_filename": pdf_path.name,
        }

    # Generate frontmatter and write
    fm = generate_frontmatter(result)
    write_markdown_file(out, fm, result["content"])

    result["output_file"] = str(out)
    return result


# ---------------------------------------------------------------------------
# Batch processing
# ---------------------------------------------------------------------------


def process_batch(
    input_dir: Path,
    output_dir: Path | None = None,
    force: bool = False,
) -> list[dict]:
    """
    Process all PDFs in a directory.

    Args:
        input_dir: Directory containing PDF files
        output_dir: Optional output directory for .md files
        force: If True, reprocess files that already have .md counterparts

    Returns:
        List of extraction result dicts
    """
    input_dir = Path(input_dir)
    pdf_files = sorted(input_dir.glob("*.pdf"))

    if not pdf_files:
        logger.warning(f"No PDF files found in {input_dir}")
        return []

    logger.info(f"Found {len(pdf_files)} PDF files in {input_dir}")

    results = []

    for pdf_file in pdf_files:
        # Determine where the .md would be written
        if output_dir:
            md_file = Path(output_dir) / pdf_file.with_suffix(".md").name
        else:
            md_file = pdf_file.with_suffix(".md")

        # Skip if .md already exists and not forcing
        if md_file.exists() and not force:
            logger.info(f"Skipping {pdf_file.name} (.md already exists)")
            continue

        result = process_single(
            pdf_file,
            output_dir=output_dir,
        )
        results.append(result)

    # Generate batch summary CSV
    _write_batch_csv(input_dir, results)

    logger.info(f"Batch complete: {len(results)} files processed")
    return results


def _write_batch_csv(input_dir: Path, results: list[dict]) -> None:
    """Write extraction_summary.csv to the input directory."""
    csv_path = input_dir / "extraction_summary.csv"

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["filename", "pages", "chars", "headings", "quality", "output_file"],
        )
        writer.writeheader()
        for r in results:
            writer.writerow(
                {
                    "filename": r["source_filename"],
                    "pages": r["page_count"],
                    "chars": r["char_count"],
                    "headings": r["heading_count"],
                    "quality": r["quality"],
                    "output_file": Path(r.get("output_file", "")).name,
                }
            )

    logger.info(f"Wrote batch summary: {csv_path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main():
    """CLI entry point for pdf_extractor."""
    parser = argparse.ArgumentParser(
        description="Extract PDF files to markdown for the Waypoint knowledge base.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python scripts/pdf_extractor.py document.pdf\n"
            "  python scripts/pdf_extractor.py document.pdf --output out.md\n"
            "  python scripts/pdf_extractor.py --batch pdfs/ --force\n"
        ),
    )

    parser.add_argument(
        "input",
        help="Path to a PDF file (single mode) or directory (with --batch)",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all PDFs in the input directory",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path (single mode only)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory for .md files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reprocess files that already have .md counterparts",
    )

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    input_path = Path(args.input)

    if args.batch:
        if not input_path.is_dir():
            parser.error(f"--batch requires a directory, got: {input_path}")

        results = process_batch(
            input_path,
            output_dir=Path(args.output_dir) if args.output_dir else None,
            force=args.force,
        )

        # Print summary table
        print(f"\n{'='*70}")
        print(f"Batch Extraction Summary: {len(results)} files processed")
        print(f"{'='*70}")
        print(f"{'Filename':<35} {'Pages':>5} {'Chars':>7} {'Quality':<8}")
        print(f"{'-'*35} {'-'*5} {'-'*7} {'-'*8}")
        for r in results:
            print(
                f"{r['source_filename']:<35} "
                f"{r['page_count']:>5} "
                f"{r['char_count']:>7} "
                f"{r['quality']:<8}"
            )

    else:
        if not input_path.suffix.lower() == ".pdf":
            parser.error(f"Expected a .pdf file, got: {input_path}")

        result = process_single(
            input_path,
            output_path=Path(args.output) if args.output else None,
            output_dir=Path(args.output_dir) if args.output_dir else None,
        )

        print(f"\nExtracted: {result['source_filename']}")
        print(f"  Pages:    {result['page_count']}")
        print(f"  Chars:    {result['char_count']}")
        print(f"  Headings: {result['heading_count']}")
        print(f"  Quality:  {result['quality']}")
        print(f"  Output:   {result.get('output_file', 'N/A')}")


if __name__ == "__main__":
    main()
