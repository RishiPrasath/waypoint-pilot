# Task 2.2: Add New Metadata Preservation Tests

**Phase:** Phase 2 — Systematic Testing
**Initiative:** enhancement--poc-evaluation

---

## Persona

You are a **Python Test Engineer** with expertise in:
- pytest test design and fixtures
- ChromaDB vector database querying
- Data integrity and schema validation testing
- TDD (Red-Green-Refactor) workflow

You write thorough, well-structured tests that validate data flows through complex pipelines.

---

## Context

### Initiative
Waypoint Phase 1 POC — Week 4 Evaluation & Documentation. Task 0.4 added three new metadata fields (`source_urls`, `retrieval_keywords`, `use_cases`) to the ChromaDB ingestion pipeline. These fields power the new UX Sources and Related Documents sections. Task 2.2 adds tests to validate these fields are correctly preserved.

### Reference Documents
- Master rules: `./CLAUDE.md`
- Task 2.1 output: `./ai-workflow/enhancement--poc-evaluation/04-prompts/02-testing/task_2.1_ingestion_tests/02-output/TASK_2.1_OUTPUT.md`
- Roadmap Task 2.2: `./ai-workflow/enhancement--poc-evaluation/02-roadmap/IMPLEMENTATION_ROADMAP.md` (search "Task 2.2")

### Working Directory
`./pilot_phase1_poc/05_evaluation/`

### Current State
- T2.1 PASSED — all existing tests green (29 pytest + 33 verify + 47/50 retrieval = 94%)
- ChromaDB has 709 chunks from 30 documents
- Each chunk has **13 metadata fields** (10 original + 3 new from T0.4):
  `doc_id`, `title`, `source_org`, `source_type`, `jurisdiction`, `category`, `section_header`, `subsection_header`, `chunk_index`, `file_path`, `source_urls`, `retrieval_keywords`, `use_cases`

### How the 3 New Fields Flow

```
Frontmatter (YAML)         →  process_docs.py          →  chunker.py          →  ingest.py (ChromaDB)
─────────────────────────────────────────────────────────────────────────────────────────────────────
source_urls:                  _extract_source_urls()       list passthrough       ",".join() → string
  - url: "https://..."        → ["https://...", ...]       → ["https://...", ...]  → "https://...,https://..."
  - url: "https://..."

retrieval_keywords:           metadata.get(...) or []      list passthrough       ",".join() → string
  - GST                       → ["GST", "import GST"]     → ["GST", "import GST"] → "GST,import GST"
  - import GST

use_cases:                    metadata.get(..., [])        list passthrough       ",".join() → string
  - UC-1.1                    → ["UC-1.1", "UC-2.2"]      → ["UC-1.1", "UC-2.2"]  → "UC-1.1,UC-2.2"
  - UC-2.2
```

### Sample ChromaDB Data (verified)

**Regulatory doc** (`01_regulatory_sg_gst_guide`):
- `source_urls`: `"https://www.customs.gov.sg/businesses/valuation-duties-taxes-fees/goods-and-services-tax-gst/,https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/basics-of-gst/current-gst-rates"`
- `retrieval_keywords`: `"GST,goods and services tax,import GST,GST rate Singapore,9 percent,..."`
- `use_cases`: `"UC-1.1,UC-2.2"`
- `category`: `"01_regulatory"`

**Internal doc** (`04_internal_synthetic_booking_procedure`):
- `source_urls`: `"N/A"`
- `retrieval_keywords`: `"booking,LCL,FCL,lead time,..."`
- `use_cases`: `"UC-1.1,UC-1.2,UC-4.2"`
- `category`: `"04_internal_synthetic"`

### Dependencies
- **Requires**: T2.1 (PASSED)
- **Blocks**: None

---

## Task

### Objective
Create `tests/test_metadata_preservation.py` with pytest tests validating that `source_urls`, `retrieval_keywords`, `use_cases`, and `category` are correctly stored in ChromaDB chunk metadata after ingestion.

### TDD Approach
Since this tests **existing data** (ChromaDB was already ingested in T0.5), these are integration tests against the live ChromaDB instance. Write tests, then run them — they should pass immediately (no RED phase needed for data validation tests).

### Test Cases to Implement

#### 1. Field Presence Tests
Test that every chunk in ChromaDB has the 3 new fields:
- `source_urls` key exists in metadata
- `retrieval_keywords` key exists in metadata
- `use_cases` key exists in metadata
- All values are strings (not lists, not None)

#### 2. Field Format Tests
- `source_urls` is comma-separated string (contains `,` when multiple URLs) or `"N/A"` for internal docs
- `retrieval_keywords` is comma-separated string
- `use_cases` is comma-separated string matching `UC-\d+\.\d+` pattern
- `category` matches one of: `01_regulatory`, `02_carriers`, `03_reference`, `04_internal_synthetic`

#### 3. Known-Value Spot Checks
Test specific documents have expected metadata values:

| doc_id | Field | Expected Contains |
|--------|-------|-------------------|
| `01_regulatory_sg_gst_guide` | `source_urls` | `customs.gov.sg` |
| `01_regulatory_sg_gst_guide` | `retrieval_keywords` | `GST` |
| `01_regulatory_sg_gst_guide` | `use_cases` | `UC-1.1` |
| `01_regulatory_sg_gst_guide` | `category` | `01_regulatory` |
| `02_carriers_maersk_service_summary` | `source_urls` | `maersk.com` |
| `02_carriers_maersk_service_summary` | `category` | `02_carriers` |
| `03_reference_incoterms_comparison` | `category` | `03_reference` |
| `04_internal_synthetic_booking_procedure` | `source_urls` | `N/A` |
| `04_internal_synthetic_booking_procedure` | `category` | `04_internal_synthetic` |

#### 4. Edge Case Tests
- Internal docs: `source_urls` is `"N/A"` (not empty string, not missing)
- Multi-URL docs: `source_urls` contains at least 2 URLs separated by commas
- All chunks from same doc share identical `source_urls`, `category`, `use_cases` values

#### 5. Category Coverage Test
- All 4 categories have at least 1 chunk in ChromaDB
- Category values on chunks match the folder-derived pattern (not frontmatter `category` field)

### Constraints
- Tests run against the **live ChromaDB** at `chroma_db/` (not mocked)
- Use `scripts.config` for `CHROMA_PERSIST_PATH` and `COLLECTION_NAME`
- Import chromadb and create client in a fixture
- Do NOT modify ingestion scripts or KB files
- Target: ~15-20 test cases

---

## Format

### File to Create
`./pilot_phase1_poc/05_evaluation/tests/test_metadata_preservation.py`

### Test Structure
```python
"""
Tests for metadata preservation through the ingestion pipeline.
Validates that source_urls, retrieval_keywords, use_cases, and category
fields are correctly stored in ChromaDB chunk metadata.
"""

import pytest
import chromadb
from scripts.config import CHROMA_PERSIST_PATH, COLLECTION_NAME


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


class TestFieldPresence:
    # source_urls, retrieval_keywords, use_cases exist on every chunk
    # All values are strings (not None, not list)
    ...

class TestFieldFormat:
    # Comma-separated string formats
    # Category values match expected set
    # use_cases pattern matches UC-N.N
    ...

class TestKnownValues:
    # Spot-check specific documents
    ...

class TestEdgeCases:
    # Internal docs have source_urls = "N/A"
    # Multi-URL docs have commas
    # Same-doc chunks share metadata
    ...

class TestCategoryCoverage:
    # All 4 categories present
    ...
```

### Run Command
```bash
cd pilot_phase1_poc/05_evaluation
venv/Scripts/python -m pytest tests/test_metadata_preservation.py -v
```

### Output Report
Create `TASK_2.2_OUTPUT.md` in the `02-output/` folder with:
- Summary of tests written
- Test results (pass/fail count)
- Any issues found
- Validation checklist

### Tracking Updates
After completion:
1. Update `IMPLEMENTATION_CHECKLIST.md` — mark Task 2.2 `[x]`
2. Update `IMPLEMENTATION_ROADMAP.md` — set Task 2.2 status to `✅ Complete`
3. Update progress totals (Phase 2: 2/13, Overall: 12/43, 28%)
