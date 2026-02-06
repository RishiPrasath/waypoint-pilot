# Task 5: Build PDF Extraction Script

## Persona

**Role**: Senior Python Developer / Document Processing Engineer

**Expertise**:
- PDF parsing and text extraction (PyMuPDF / pymupdf4llm)
- Markdown generation and structure preservation
- CLI tool design with argparse
- Test-driven development with pytest
- Windows-compatible file operations with pathlib

---

## Context

### Background

Phase 2 infrastructure is partially complete. Task 4 set up the `04_retrieval_optimization/` workspace with a forked ingestion pipeline, parameterized chunking, and empty `kb/` folders with `pdfs/` subfolders. Task 6 (KB Rebuild) will scrape source websites and discover downloadable PDFs. This script provides the tooling to convert those PDFs into markdown documents that integrate with the existing ingestion pipeline.

Many government and regulatory sources (Singapore Customs, ASEAN trade bodies) publish key information as PDF documents. The current KB was built from web scraping only — adding PDF extraction unlocks content that may resolve several of the 9 failing queries identified in Task 1.

### Current State

- **Workspace**: `04_retrieval_optimization/` is set up with scripts, venv, and empty `kb/` folders (Task 4 ✅)
- **Dependencies**: `pymupdf4llm>=0.0.17` is already in `requirements.txt` and installed in venv
- **KB Structure**: Each category folder has a `pdfs/` subfolder ready for PDF files
- **Ingestion Pipeline**: Expects `.md` files in `kb/` with YAML frontmatter — `process_docs.py` discovers `*.md` files recursively via `discover_documents()`
- **No PDFs exist yet** — they'll be downloaded during Task 6

### References

| Document | Path | Purpose |
|----------|------|---------|
| Implementation Roadmap | `04_retrieval_optimization/ai-workflow/.../02-roadmap/IMPLEMENTATION_ROADMAP.md` | Task 5 checklist |
| Detailed Plan | `04_retrieval_optimization/ai-workflow/.../01-plan/DETAILED_PLAN.md` | Retrieval-first guidelines, frontmatter template |
| Revised Document List | `04_retrieval_optimization/REVISED_DOCUMENT_LIST.md` | Documents and their actions |
| config.py | `04_retrieval_optimization/scripts/config.py` | Path constants (PIPELINE_ROOT, KNOWLEDGE_BASE_PATH) |
| process_docs.py | `04_retrieval_optimization/scripts/process_docs.py` | Shows how `.md` files are consumed downstream |
| requirements.txt | `04_retrieval_optimization/requirements.txt` | Already includes pymupdf4llm |
| pymupdf4llm docs | https://pymupdf.readthedocs.io/en/latest/ | Library documentation |

### Dependencies

- **Completed**: Task 4 (Folder Setup)
- **Blocks**: Task 6 (KB Rebuild — will use this script to process downloaded PDFs)

---

## Task

### Objective

Create `scripts/pdf_extractor.py` — a CLI tool that converts PDF files to well-structured markdown with YAML frontmatter templates, quality assessment flags, and batch processing support. The output `.md` files must integrate seamlessly with the existing ingestion pipeline (`process_docs.py` → `chunker.py` → `ingest.py`).

### Requirements

1. **Single file mode**: Convert one PDF to markdown
   ```bash
   python scripts/pdf_extractor.py path/to/file.pdf
   ```
   - Extract text content using `pymupdf4llm`
   - Output markdown file alongside the PDF (same directory, `.md` extension)
   - Include a YAML frontmatter **template** with placeholder values for manual completion
   - Print summary: page count, character count, quality flag

2. **Batch mode**: Convert all PDFs in a directory
   ```bash
   python scripts/pdf_extractor.py --batch path/to/pdfs/
   ```
   - Process all `*.pdf` files in the directory
   - Skip files that already have a corresponding `.md` file (unless `--force`)
   - Generate a batch summary CSV (`extraction_summary.csv` in the same directory)
   - Print summary table: filename, pages, chars, quality flag

3. **Output file options**:
   ```bash
   python scripts/pdf_extractor.py file.pdf --output path/to/output.md
   python scripts/pdf_extractor.py file.pdf --output-dir path/to/dir/
   ```
   - `--output`: Write to specific file path (single mode only)
   - `--output-dir`: Write output file(s) to a specific directory (works in both modes)
   - Default (no flag): Write `.md` next to the source PDF

4. **Frontmatter template**: Every output file starts with a YAML frontmatter template:
   ```yaml
   ---
   title: "[EXTRACTED: first heading or filename]"
   source_organization: "[TODO: Organization name]"
   source_urls:
     - url: "[TODO: Source webpage URL]"
       description: "[TODO: What this page covers]"
       retrieved_date: YYYY-MM-DD
   source_pdfs:
     - filename: "original_filename.pdf"
       source_url: "[TODO: URL where PDF was downloaded]"
       description: "[EXTRACTED: first heading or filename]"
       retrieved_date: YYYY-MM-DD
   source_type: "[TODO: public_regulatory | public_carrier | synthetic_internal]"
   last_updated: YYYY-MM-DD
   jurisdiction: "[TODO: SG | MY | ID | TH | VN | PH | ASEAN | Global]"
   category: "[TODO: customs | carrier | policy | procedure | reference]"
   use_cases: []
   keywords: []
   answers_queries: []
   related_documents: []
   ---
   ```
   - Auto-fill `title` from first heading (H1 or H2) found in extracted content, fallback to filename
   - Auto-fill `source_pdfs.filename` from the actual PDF filename
   - Auto-fill `retrieved_date` with today's date
   - All other fields use `[TODO: ...]` placeholders

5. **Content cleaning**: After extraction, clean common PDF artifacts:
   - Remove excessive blank lines (collapse 3+ consecutive blank lines to 2)
   - Remove page headers/footers that repeat across pages (detect and strip)
   - Normalize Unicode characters (smart quotes → straight quotes, em-dashes → --)
   - Strip trailing whitespace from all lines
   - Ensure file ends with a single newline

6. **Quality assessment**: Assign a quality flag to each extracted file:
   - **HIGH**: ≥500 chars extracted, has structure (headings), <10% suspected garbled text
   - **MEDIUM**: ≥200 chars, limited structure, or some extraction issues
   - **LOW**: <200 chars, no structure, mostly garbled/image-only content
   - Quality flag is logged and included in batch summary CSV but NOT in the markdown output

7. **Batch summary CSV** (generated in batch mode):
   ```csv
   filename,pages,chars,headings,quality,output_file
   document1.pdf,12,8543,15,HIGH,document1.md
   document2.pdf,3,234,0,LOW,document2.md
   ```

8. **Logging**: Use Python `logging` module
   - INFO: File being processed, quality flag, output path
   - WARNING: Extraction issues (low quality, encoding problems)
   - DEBUG: Page-by-page extraction details
   - Respect `LOG_LEVEL` from config.py

### Specifications

```python
# Core function signatures

def extract_pdf_to_markdown(pdf_path: Path) -> dict:
    """
    Extract text from a PDF and convert to markdown.

    Returns:
        {
            "content": str,          # Extracted markdown text
            "page_count": int,       # Number of pages
            "char_count": int,       # Character count of content
            "heading_count": int,    # Number of markdown headings found
            "quality": str,          # "HIGH" | "MEDIUM" | "LOW"
            "title": str,            # Extracted title (first heading or filename)
            "source_filename": str,  # Original PDF filename
        }
    """

def clean_extracted_content(content: str) -> str:
    """Remove PDF artifacts, normalize whitespace and Unicode."""

def assess_quality(content: str, heading_count: int) -> str:
    """Return quality flag: HIGH, MEDIUM, or LOW."""

def generate_frontmatter(extraction_result: dict) -> str:
    """Generate YAML frontmatter template from extraction metadata."""

def write_markdown_file(output_path: Path, frontmatter: str, content: str) -> None:
    """Write the final markdown file with frontmatter + content."""

def process_single(pdf_path: Path, output_path: Path | None = None, output_dir: Path | None = None) -> dict:
    """Process a single PDF. Returns extraction result dict."""

def process_batch(input_dir: Path, output_dir: Path | None = None, force: bool = False) -> list[dict]:
    """Process all PDFs in a directory. Returns list of extraction results."""
```

### Constraints

- **DO NOT modify** any existing scripts in `04_retrieval_optimization/scripts/` — this is a new file only
- **DO NOT modify** anything in `02_ingestion_pipeline/` or `01_knowledge_base/kb/` (protected paths)
- Use `pymupdf4llm` for extraction (already installed) — do NOT install additional PDF libraries
- All paths must work on Windows (use `pathlib.Path`, not hardcoded slashes)
- Import config values from `scripts.config` (PIPELINE_ROOT, LOG_LEVEL) — don't duplicate config
- Output `.md` files must be parseable by the existing `process_docs.py` (YAML frontmatter + markdown content)
- Handle edge cases gracefully: encrypted PDFs, image-only PDFs, empty PDFs, corrupted files

### Acceptance Criteria

- [ ] `scripts/pdf_extractor.py` exists and is executable
- [ ] Single mode: `python scripts/pdf_extractor.py test.pdf` produces `test.md` with frontmatter
- [ ] Batch mode: `python scripts/pdf_extractor.py --batch pdfs/` processes all PDFs and writes CSV
- [ ] `--output` flag works for custom output path
- [ ] `--output-dir` flag works for custom output directory
- [ ] `--force` flag re-processes files that already have `.md` counterparts
- [ ] Frontmatter auto-fills title, filename, and date; other fields have `[TODO]` placeholders
- [ ] Content cleaning removes excess blank lines, normalizes Unicode
- [ ] Quality flags assigned correctly (HIGH/MEDIUM/LOW)
- [ ] Batch CSV generated with correct columns
- [ ] Graceful handling of: encrypted PDFs, image-only PDFs, empty PDFs, missing files
- [ ] All tests pass: `python -m pytest tests/test_pdf_extractor.py -v`
- [ ] Output `.md` is parseable by `process_docs.py` (frontmatter + content structure)

---

## Format

### Output Structure

```
04_retrieval_optimization/
├── scripts/
│   └── pdf_extractor.py          # NEW: PDF extraction CLI tool
└── tests/
    └── test_pdf_extractor.py     # NEW: Tests for PDF extraction
```

### Code Style

- Python 3.11+ type hints on all function signatures
- Docstrings for all public functions
- Use `pathlib.Path` for all path operations
- Use `argparse` for CLI argument parsing
- Follow existing conventions from `process_docs.py` and `config.py`
- Use `if __name__ == "__main__":` for CLI entry point

### Test Plan (TDD)

Write tests **before** implementation. Test file: `tests/test_pdf_extractor.py`

**Unit tests** (no real PDFs required — mock pymupdf4llm):

| # | Test | Description |
|---|------|-------------|
| 1 | `test_clean_extracted_content_collapses_blank_lines` | 3+ blank lines → 2 |
| 2 | `test_clean_extracted_content_normalizes_unicode` | Smart quotes → straight quotes |
| 3 | `test_clean_extracted_content_strips_trailing_whitespace` | Trailing spaces removed |
| 4 | `test_assess_quality_high` | ≥500 chars + headings → HIGH |
| 5 | `test_assess_quality_medium` | ≥200 chars, limited structure → MEDIUM |
| 6 | `test_assess_quality_low` | <200 chars, no structure → LOW |
| 7 | `test_generate_frontmatter_has_required_fields` | All YAML fields present |
| 8 | `test_generate_frontmatter_autofills_title` | Title extracted from heading |
| 9 | `test_generate_frontmatter_autofills_filename` | PDF filename in source_pdfs |
| 10 | `test_generate_frontmatter_parseable_yaml` | Output parses as valid YAML |
| 11 | `test_write_markdown_file_creates_file` | File created with correct content |
| 12 | `test_process_single_with_mock_pdf` | Full pipeline with mocked extraction |
| 13 | `test_process_batch_skips_existing` | Existing `.md` files skipped (no `--force`) |
| 14 | `test_process_batch_force_reprocesses` | `--force` overwrites existing `.md` |
| 15 | `test_process_single_encrypted_pdf_graceful` | Encrypted PDF logs warning, doesn't crash |
| 16 | `test_process_single_missing_file_graceful` | Missing file raises clear error |

### Validation Commands

```bash
cd pilot_phase1_poc/04_retrieval_optimization
venv\Scripts\activate

# Run tests (TDD - write these first)
python -m pytest tests/test_pdf_extractor.py -v

# Verify script is importable
python -c "from scripts.pdf_extractor import extract_pdf_to_markdown; print('Import OK')"

# Verify CLI help works
python scripts/pdf_extractor.py --help

# Integration test: create a test PDF and extract it
python -c "
import fitz
doc = fitz.open()
page = doc.new_page()
page.insert_text((72, 72), '# Test Document\n\nThis is a test PDF for extraction validation.', fontsize=12)
doc.save('tests/test_sample.pdf')
doc.close()
print('Test PDF created')
"
python scripts/pdf_extractor.py tests/test_sample.pdf --output tests/test_sample_output.md
python -c "
from scripts.process_docs import parse_frontmatter, extract_content
content = open('tests/test_sample_output.md', encoding='utf-8').read()
fm = parse_frontmatter(content)
print('Frontmatter parsed:', bool(fm))
print('Title:', fm.get('title', 'MISSING'))
body = extract_content(content)
print('Content length:', len(body))
print('Integration OK')
"
```

---

## Notes

- `pymupdf4llm` wraps PyMuPDF (fitz) and provides `to_markdown()` which preserves headings, tables, and lists. Use this as the primary extraction method.
- The script will be used extensively in Task 6 where 30 documents may have associated PDFs. Batch mode performance matters — log progress with tqdm if processing >5 files.
- Quality flags help Task 6 decide whether to trust PDF content or prefer web-scraped content. LOW quality PDFs likely need manual review or alternative sourcing.
- The frontmatter template intentionally uses `[TODO]` placeholders — Task 6 will fill these in during the scraping process, or they can be filled manually.
