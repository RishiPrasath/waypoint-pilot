# Python Tests (pytest)

All Python tests are run with `python -m pytest tests/ -v` from the relevant workspace directory.

---

## test_process_docs.py (22 tests)

**Location**: `pilot_phase1_poc/02_ingestion_pipeline/tests/test_process_docs.py`

**What it tests**: The document processing pipeline that reads markdown files from the knowledge base, parses YAML frontmatter, extracts body content, and generates metadata.

**Imports under test**:
```python
from scripts.process_docs import (
    discover_documents, parse_frontmatter, extract_content,
    get_category_from_path, generate_doc_id,
    parse_document, load_all_documents,
)
```

**Fixtures**:
- `sample_frontmatter_content` -- markdown with valid YAML frontmatter (title, source_organization, source_urls, use_cases)
- `sample_no_frontmatter` -- markdown without frontmatter delimiters
- `sample_minimal_frontmatter` -- markdown with only `title` in frontmatter
- `real_document_path` / `real_carrier_path` / `real_reference_path` / `real_internal_path` -- paths to actual KB documents

**Test classes**:

### TestDiscoverDocuments (5 tests)
| Test | Description |
|------|-------------|
| `test_finds_all_29_documents` | Discovers exactly 29 `.md` files from `kb/` folder |
| `test_returns_sorted_paths` | Output is sorted alphabetically |
| `test_returns_path_objects` | All items are `pathlib.Path` instances |
| `test_all_files_are_markdown` | All files have `.md` extension |
| `test_all_files_exist` | All returned paths exist on disk |

### TestParseFrontmatter (5 tests)
| Test | Description |
|------|-------------|
| `test_parses_valid_yaml` | Extracts `title`, `source_organization` from YAML block |
| `test_returns_empty_dict_for_no_frontmatter` | Returns `{}` when no `---` delimiters |
| `test_handles_nested_source_urls` | Parses list-of-dicts for `source_urls[].url` |
| `test_handles_list_fields` | Parses `use_cases` as Python list `["UC-1.1", "UC-2.1"]` |
| `test_handles_empty_string` | Returns `{}` for empty input |

### TestExtractContent (4 tests)
| Test | Description |
|------|-------------|
| `test_removes_frontmatter` | Body content has no `---` or YAML fields |
| `test_strips_whitespace` | No leading/trailing newlines |
| `test_handles_no_frontmatter` | Returns full content when no frontmatter present |
| `test_preserves_content_structure` | Markdown headings and body text intact |

### TestGetCategoryFromPath (4 tests)
| Test | Description |
|------|-------------|
| `test_extracts_regulatory_category` | `01_regulatory` from regulatory path |
| `test_extracts_carriers_category` | `02_carriers` from carrier path |
| `test_extracts_reference_category` | `03_reference` from reference path |
| `test_extracts_internal_category` | `04_internal_synthetic` from internal path |

### TestGenerateDocId (3 tests)
| Test | Description |
|------|-------------|
| `test_creates_unique_id` | Format: `{category}_{filename}` (e.g., `01_regulatory_sg_import_procedures`) |
| `test_excludes_file_extension` | No `.md` in the generated ID |
| `test_includes_category_prefix` | Starts with category string |

### TestParseDocument (6 tests)
| Test | Description |
|------|-------------|
| `test_returns_all_12_fields` | Keys: `doc_id`, `file_path`, `title`, `source_org`, `source_urls`, `source_type`, `last_updated`, `jurisdiction`, `category`, `use_cases`, `content`, `char_count` |
| `test_maps_source_organization_to_source_org` | Renames field from frontmatter to metadata |
| `test_extracts_urls_from_nested_objects` | Flattens `source_urls[].url` to list of strings |
| `test_calculates_char_count` | `char_count == len(content)` |
| `test_content_excludes_frontmatter` | Body content has no YAML metadata |
| `test_file_path_is_absolute` | Stored as absolute path string |

### TestLoadAllDocuments (6 tests -- integration)
| Test | Description |
|------|-------------|
| `test_loads_all_29_documents` | Loads all 29 documents from KB |
| `test_all_documents_have_required_fields` | All 12 fields present on every document |
| `test_total_char_count_reasonable` | Total chars between 180,000 and 200,000 |
| `test_category_distribution` | 14 regulatory, 6 carriers, 3 reference, 6 internal |
| `test_all_doc_ids_unique` | No duplicate document IDs |
| `test_all_documents_have_content` | Every document has non-empty content and positive char_count |

---

## test_pdf_extractor.py (22 tests)

**Location**: `pilot_phase1_poc/05_evaluation/tests/test_pdf_extractor.py` (copied from `04_retrieval_optimization/tests/`)

**What it tests**: PDF-to-markdown extraction tool using `pymupdf4llm` and `fitz`. Tests use mocked PDF libraries to avoid requiring real PDF files.

**Imports under test**:
```python
from scripts.pdf_extractor import (
    assess_quality, clean_extracted_content, extract_pdf_to_markdown,
    generate_frontmatter, process_batch, process_single, write_markdown_file,
)
```

**Test classes**:

### TestCleanExtractedContent (6 tests)
| Test | Description |
|------|-------------|
| `test_collapses_blank_lines` | 3+ blank lines collapse to 2 |
| `test_normalizes_unicode_smart_quotes` | Smart quotes become straight quotes |
| `test_normalizes_unicode_em_dashes` | Em/en dashes become `--` |
| `test_strips_trailing_whitespace` | No trailing spaces on any line |
| `test_ends_with_single_newline` | Exactly one trailing newline |
| `test_preserves_meaningful_structure` | Double newlines (paragraph breaks) preserved |

### TestAssessQuality (6 tests)
| Test | Description |
|------|-------------|
| `test_high_quality` | >= 500 chars with headings = HIGH |
| `test_high_quality_many_headings` | 1000 chars + 10 headings = HIGH |
| `test_medium_quality_short_with_headings` | 200-499 chars with headings = MEDIUM |
| `test_medium_quality_long_no_headings` | >= 500 chars but 0 headings = MEDIUM |
| `test_low_quality_very_short` | < 200 chars = LOW |
| `test_low_quality_empty` | Empty string = LOW |

### TestGenerateFrontmatter (4 tests)
| Test | Description |
|------|-------------|
| `test_has_required_fields` | 12 required YAML fields present (title, source_organization, source_urls, source_pdfs, etc.) |
| `test_autofills_title` | Title extracted from first heading |
| `test_autofills_filename` | `source_pdfs[0].filename` matches input filename |
| `test_parseable_yaml` | Output parses as valid YAML dict |

### TestWriteMarkdownFile (2 tests)
| Test | Description |
|------|-------------|
| `test_creates_file` | Writes file with frontmatter + content |
| `test_creates_parent_dirs` | Creates intermediate directories |

### TestExtractPdfToMarkdown (3 tests, mocked)
| Test | Description |
|------|-------------|
| `test_process_single_with_mock_pdf` | Full extraction pipeline with mocked `pymupdf4llm` |
| `test_process_single_custom_output` | `--output` flag writes to custom path |
| `test_process_single_output_dir` | `--output-dir` flag writes to specified directory |

### TestProcessBatch (5 tests, mocked)
| Test | Description |
|------|-------------|
| `test_batch_processes_all_pdfs` | Processes all `.pdf` files in directory |
| `test_batch_skips_existing` | Skips PDFs with existing `.md` counterparts |
| `test_batch_force_reprocesses` | `--force` flag reprocesses existing files |
| `test_batch_generates_csv` | Generates `extraction_summary.csv` with filename, quality, pages, chars |
| `test_batch_with_output_dir` | Writes to specified output directory |

### TestErrorHandling (2 tests)
| Test | Description |
|------|-------------|
| `test_encrypted_pdf_graceful` | Encrypted PDF returns result with LOW quality, 0 chars (no crash) |
| `test_missing_file_raises_error` | Missing PDF file raises `FileNotFoundError` |

---

## test_verify_ingestion.py (5 test classes, multiple tests per class)

**Location**: `pilot_phase1_poc/02_ingestion_pipeline/tests/test_verify_ingestion.py`

**What it tests**: Post-ingestion verification checks against ChromaDB. Uses mock collections for unit tests and real collections for integration tests.

**Test classes and key tests**:

### TestParseArgs (4 tests)
- Default args, `--verbose` flag, `-v` short flag, `--tier` option

### TestCheckTotalCount (5 tests)
- Valid count (450-520 range), too low (200), too high (600), boundary values

### TestCheckCategoryDistribution (4 tests)
- All 4 categories present (4/4 pass), missing category (3/4 fail), empty collection

### TestCheckMetadataIntegrity (5 tests)
- All 10 metadata fields present (10/10), missing fields, empty collection

### TestTier1Retrieval (5 tests)
- 8 category-level queries, correct/wrong category matching, 8/8 requirement, empty results

### TestTier2Retrieval (7 tests)
- 12 document-level queries, correct/wrong doc_id matching, 10+/12 requirement, top-3 checking, n_results=3

### TestTier3Scenarios (5 tests)
- 10 keyword-presence queries, expected/missing keywords, 8+/10 requirement, empty results

### TestRunAllChecks (4 tests)
- Returns results dict, runs all 6 checks, tier filter, overall pass calculation

### TestIntegration (6 tests)
- Real ChromaDB: total count, category distribution, metadata integrity, tier 1/2/3 retrieval

---

## test_retrieval_quality.py / retrieval_quality_test.py (6 effective test categories)

**Location**: `pilot_phase1_poc/05_evaluation/scripts/retrieval_quality_test.py`

**What it tests**: Runs 50 queries against the live ChromaDB instance and evaluates retrieval hit rate. This is a quality measurement script rather than a traditional unit test, but it functions as a test with pass/fail criteria.

**Test categories** (50 queries across 5 domains):
1. **Booking & Documentation** (10 queries) -- sea freight docs, LCL bookings, FCL vs LCL, SI cutoff
2. **Customs & Regulatory** (10 queries) -- GST rates, HS codes, certificates of origin, permits
3. **Carrier Information** (10 queries) -- direct sailings, transit times, reefer containers, VGM
4. **Internal Procedures** (10 queries) -- booking workflows, SLAs, escalation, COD procedures
5. **Out-of-Scope** (10 queries) -- live tracking, rate quotes, booking changes (expected: no relevant results)

**Baselines**:
- Week 3 optimized: 92% raw hit rate (46/50 queries)
- Adjusted (excluding 3 reclassified OOS queries): ~98%

**Run command**:
```bash
cd pilot_phase1_poc/05_evaluation
python scripts/retrieval_quality_test.py
```

---

## test_metadata_preservation.py (26 tests across 5 classes)

**Location**: `pilot_phase1_poc/05_evaluation/tests/test_metadata_preservation.py`

**What it tests**: Validates that metadata fields (`source_urls`, `retrieval_keywords`, `use_cases`, `category`) are correctly stored in ChromaDB after ingestion. Runs against the live ChromaDB instance.

### TestFieldPresence (6 tests)
- `source_urls`, `retrieval_keywords`, `use_cases` present on all chunks; all three are strings

### TestFieldFormat (4 tests)
- Category values in expected set; `source_urls` is CSV or N/A; `use_cases` match UC-N.N pattern; most chunks have non-empty `retrieval_keywords`

### TestKnownValues (9 tests)
- GST guide: `customs.gov.sg` in source_urls, `GST` in keywords, `UC-1.1` in use_cases, `01_regulatory` category
- Maersk: `maersk.com` in source_urls, `02_carriers` category
- Incoterms: `03_reference` category
- Booking procedure: `N/A` source_urls, `04_internal_synthetic` category

### TestEdgeCases (5 tests)
- Internal docs have no external URLs; multi-URL doc has comma-separated URLs; same-doc chunks share source_urls, category, and use_cases

### TestCategoryCoverage (2 tests)
- All 4 categories present; each category has >= 10 chunks
