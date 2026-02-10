# PDF Extraction

Layer 3 documentation for `pdf_extractor.py`.

This script converts PDF files to well-structured markdown with YAML frontmatter templates, quality assessment, and batch processing support. Output integrates with the existing ingestion pipeline (`process_docs` -> `chunker` -> `ingest`).

**Important:** PDF extracts are reference material only. Their content is selectively merged into main KB documents. The `pdfs/` subdirectories are excluded from ingestion by `discover_documents()` in `process_docs.py`.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `pymupdf4llm` | PDF to markdown conversion |
| `PyMuPDF` (fitz) | PDF page count and low-level access |
| `pyyaml` | YAML frontmatter serialization |

---

## CLI Interface

```
usage: pdf_extractor.py [-h] [--batch] [--output OUTPUT] [--output-dir OUTPUT_DIR] [--force] input

positional arguments:
  input                 Path to a PDF file (single mode) or directory (with --batch)

optional arguments:
  --batch               Process all PDFs in the input directory
  --output OUTPUT       Output file path (single mode only)
  --output-dir OUTPUT_DIR  Output directory for .md files
  --force               Reprocess files that already have .md counterparts
```

---

## Functions

### `clean_extracted_content(content: str) -> str`

Removes PDF artifacts and normalizes whitespace and Unicode characters.

**Parameters:**
- `content` (`str`): Raw extracted markdown text from pymupdf4llm

**Returns:** Cleaned markdown text.

**Transformations applied:**
| Input | Output | Description |
|-------|--------|-------------|
| `\u201c` / `\u201d` | `"` | Smart double quotes to straight |
| `\u2018` / `\u2019` | `'` | Smart single quotes to straight |
| `\u2014` | `--` | Em-dash |
| `\u2013` | `--` | En-dash |
| `\u2026` | `...` | Ellipsis |
| `\u00a0` | ` ` | Non-breaking space to regular space |
| 3+ blank lines | 2 blank lines | Collapse excessive whitespace |
| Trailing whitespace per line | Stripped | Clean line endings |

Output always ends with exactly one newline.

---

### `assess_quality(content: str, heading_count: int) -> str`

Assesses extraction quality based on content length and heading count.

**Parameters:**
- `content` (`str`): Extracted text content
- `heading_count` (`int`): Number of markdown headings found

**Returns:** Quality flag string.

| Condition | Result |
|-----------|--------|
| chars >= 500 AND headings >= 1 | `"HIGH"` |
| chars >= 200 | `"MEDIUM"` |
| Otherwise | `"LOW"` |

---

### `_extract_title(content: str, filename: str) -> str`

Extracts a title from the first H1 or H2 heading in the content.

**Parameters:**
- `content` (`str`): Markdown content
- `filename` (`str`): PDF filename stem as fallback

**Returns:** Extracted title string. Falls back to cleaned filename if no heading found.

**Regex:** `^#{1,2}\s+(.+)$` (multiline)

---

### `generate_frontmatter(extraction_result: dict) -> str`

Generates a YAML frontmatter template from extraction metadata. Auto-fills title, source PDF filename, and retrieved date. Other fields use `[TODO]` placeholders for manual completion.

**Parameters:**
- `extraction_result` (`dict`): Return value from `extract_pdf_to_markdown()`

**Returns:** YAML frontmatter string (without `---` delimiters).

**Generated fields:**
| Field | Value |
|-------|-------|
| `title` | Extracted from content |
| `source_organization` | `[TODO: Organization name]` |
| `source_urls` | List with one `[TODO]` entry |
| `source_pdfs` | List with filename and `[TODO]` URL |
| `source_type` | `[TODO: public_regulatory \| ...]` |
| `last_updated` | Today's date (ISO format) |
| `jurisdiction` | `[TODO: SG \| MY \| ...]` |
| `category` | `[TODO: customs \| carrier \| ...]` |
| `use_cases` | Empty list |
| `keywords` | Empty list |
| `answers_queries` | Empty list |
| `related_documents` | Empty list |

---

### `write_markdown_file(output_path: Path, frontmatter: str, content: str) -> None`

Writes the final markdown file with frontmatter and content.

**Parameters:**
- `output_path` (`Path`): Path to write the `.md` file
- `frontmatter` (`str`): YAML frontmatter string (without `---` delimiters)
- `content` (`str`): Cleaned markdown content

Creates parent directories automatically via `mkdir(parents=True, exist_ok=True)`.

**Output format:**
```markdown
---
title: ...
source_organization: ...
---

[content here]
```

---

### `extract_pdf_to_markdown(pdf_path: Path) -> dict`

Core extraction function. Converts a PDF to markdown using pymupdf4llm, cleans the output, and assesses quality.

**Parameters:**
- `pdf_path` (`Path`): Path to the PDF file

**Returns:** Dictionary with:

| Key | Type | Description |
|-----|------|-------------|
| `content` | `str` | Cleaned markdown text |
| `page_count` | `int` | Number of PDF pages |
| `char_count` | `int` | Length of cleaned content |
| `heading_count` | `int` | Number of markdown headings |
| `quality` | `str` | `"HIGH"`, `"MEDIUM"`, or `"LOW"` |
| `title` | `str` | Extracted or derived title |
| `source_filename` | `str` | Original PDF filename |

**Example:**
```python
from pathlib import Path
from scripts.pdf_extractor import extract_pdf_to_markdown

result = extract_pdf_to_markdown(Path("docs/customs_guide.pdf"))
print(result["page_count"])   # 12
print(result["quality"])      # "HIGH"
print(result["title"])        # "Singapore Customs Import Guide"
```

---

### `process_single(pdf_path: Path, output_path: Path | None = None, output_dir: Path | None = None) -> dict`

Processes a single PDF file to markdown with frontmatter.

**Parameters:**
- `pdf_path` (`Path`): Path to the PDF file
- `output_path` (`Path | None`): Explicit output file path (optional)
- `output_dir` (`Path | None`): Output directory -- filename derived from PDF (optional)

**Returns:** Extraction result dict (same as `extract_pdf_to_markdown()` plus `output_file` key).

**Output path resolution order:**
1. `output_path` if provided
2. `output_dir / {pdf_stem}.md` if provided
3. `{pdf_path_without_extension}.md` (same directory as PDF)

**Raises:** `FileNotFoundError` if `pdf_path` does not exist.

If extraction fails internally, returns a result dict with `quality="LOW"` and empty content rather than raising.

---

### `process_batch(input_dir: Path, output_dir: Path | None = None, force: bool = False) -> list[dict]`

Processes all PDF files in a directory.

**Parameters:**
- `input_dir` (`Path`): Directory containing PDF files
- `output_dir` (`Path | None`): Optional output directory for `.md` files
- `force` (`bool`): If True, reprocesses files that already have `.md` counterparts (default False)

**Returns:** List of extraction result dicts.

**Skip logic:** If an `.md` file already exists for a given PDF and `force=False`, that PDF is skipped.

**Side effect:** Writes `extraction_summary.csv` to `input_dir` with columns: `filename`, `pages`, `chars`, `headings`, `quality`, `output_file`.

---

### `_write_batch_csv(input_dir: Path, results: list[dict]) -> None`

Internal helper. Writes `extraction_summary.csv` to the input directory.

---

### `main()`

CLI entry point. Parses arguments, dispatches to `process_single()` or `process_batch()`, and prints results.

---

## Usage Examples

```bash
# Single file extraction
python scripts/pdf_extractor.py document.pdf

# Single file with custom output
python scripts/pdf_extractor.py document.pdf --output output.md
python scripts/pdf_extractor.py document.pdf --output-dir extracted/

# Batch mode -- all PDFs in a directory
python scripts/pdf_extractor.py --batch pdfs/

# Batch mode -- force reprocessing existing files
python scripts/pdf_extractor.py --batch pdfs/ --force
```

### Single File Output

```
Extracted: customs_guide.pdf
  Pages:    12
  Chars:    15432
  Headings: 8
  Quality:  HIGH
  Output:   customs_guide.md
```

### Batch Output

```
======================================================================
Batch Extraction Summary: 5 files processed
======================================================================
Filename                            Pages   Chars Quality
----------------------------------- ----- ------- --------
customs_guide.pdf                      12   15432 HIGH
trade_rules.pdf                         8    9871 HIGH
summary.pdf                             2    1203 MEDIUM
appendix.pdf                            1     187 LOW
reference.pdf                           4    4521 HIGH
```
