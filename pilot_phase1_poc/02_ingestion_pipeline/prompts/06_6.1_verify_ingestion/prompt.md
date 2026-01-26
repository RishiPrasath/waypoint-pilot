# Task 6.1: Create Verification Script

## Persona

> You are a QA engineer specializing in RAG system validation.
> You follow TDD practices - writing tests first, then implementation.
> You design comprehensive test suites that verify both technical correctness and semantic relevance.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. The verification script validates that the ingestion pipeline correctly stored documents and that retrieval returns relevant results for expected queries.

### Current State
- ✅ `scripts/config.py` - Configuration module
- ✅ `scripts/process_docs.py` - Document processor (29 docs)
- ✅ `scripts/chunker.py` - Chunking engine (483 chunks)
- ✅ `scripts/ingest.py` - Main ingestion script
- ✅ 87 unit tests passing
- ✅ ChromaDB populated with 483 chunks

### Reference Documents
- Roadmap: `docs/01_implementation_roadmap.md`
- Use Cases: `pilot_phase1_poc/00_docs/02_use_cases.md`
- Ingestion script: `scripts/ingest.py`

### Dependencies
- Task 5.1 (ingest.py) ✅ Complete
- Task 5.2 (full ingestion run) ✅ Complete
- ChromaDB collection populated with 483 chunks

---

## Task

### Objective
Create `scripts/verify_ingestion.py` - a verification script that validates the ingestion quality through 6 checks. Follow TDD - write tests first in `tests/test_verify_ingestion.py`.

### Requirements

#### 1. CLI Interface
```bash
python scripts/verify_ingestion.py [OPTIONS]

Options:
  --verbose, -v     Show detailed results for each test
  --tier TIER       Run only specific tier (1, 2, or 3)
  --check CHECK     Run only specific check (1-6)
```

#### 2. Check 1: Total Chunk Count
- Verify ChromaDB collection has expected chunks
- Expected: 450-520 chunks (flexibility for minor changes)
- PASS if count in range, FAIL otherwise

#### 3. Check 2: Category Distribution
- Verify all 4 categories have chunks:
  - `01_regulatory` (largest)
  - `02_carriers`
  - `03_reference`
  - `04_internal_synthetic`
- PASS if all 4 present with reasonable distribution

#### 4. Check 3: Metadata Integrity
- Sample 10 random chunks
- Verify all required fields present:
  - `doc_id`, `title`, `source_org`, `source_type`
  - `jurisdiction`, `category`, `section_header`
  - `subsection_header`, `chunk_index`, `file_path`
- PASS if all sampled chunks have complete metadata

#### 5. Check 4: Tier 1 Retrieval Tests (8 queries)
Category-level queries - should return chunks from correct category:

| Query | Expected Category |
|-------|-------------------|
| "Singapore GST import requirements" | 01_regulatory |
| "ATIGA Certificate of Origin Form D" | 01_regulatory |
| "Maersk shipping services" | 02_carriers |
| "PIL ocean carrier Singapore" | 02_carriers |
| "Incoterms 2020 FOB CIF" | 03_reference |
| "HS code classification structure" | 03_reference |
| "Company escalation procedure" | 04_internal_synthetic |
| "Customer service SLA policy" | 04_internal_synthetic |

- PASS: Top-3 results include chunk from expected category
- Target: 8/8 pass

#### 6. Check 5: Tier 2 Retrieval Tests (12 queries)
Document-level queries - should return chunks from specific documents:

| Query | Expected Document (partial match) |
|-------|-----------------------------------|
| "Singapore export permit requirements" | sg_export_procedures |
| "Indonesia LARTAS import restrictions" | indonesia_lartas_overview |
| "Malaysia customs clearance process" | malaysia_customs_guide |
| "Vietnam import documentation" | vietnam_import_requirements |
| "Certificate of Origin application process" | sg_certificates_of_origin |
| "Free Trade Zone GST suspension" | sg_ftz_procedures |
| "Maersk container specifications" | maersk_shipping_guide |
| "ONE ocean carrier routes Asia" | one_carrier_overview |
| "Evergreen shipping services" | evergreen_shipping_services |
| "Incoterms delivery terms responsibility" | incoterms_2020_guide |
| "Freight forwarding SOP booking" | freight_forwarding_sop |
| "FTA comparison ATIGA RCEP" | fta_comparison_matrix |

- PASS: Top-5 results include chunk from expected document
- Target: 10+/12 pass

#### 7. Check 6: Tier 3 Scenario Tests (10 queries)
Complex queries that span multiple concepts:

| Query | Expected Keywords in Results |
|-------|------------------------------|
| "What documents needed FCL export Singapore to Jakarta" | export, Indonesia, commercial invoice, Bill of Lading |
| "Certificate of Origin ASEAN preferential rates" | Form D, ATIGA, Rules of Origin |
| "GST treatment goods stored FTZ Singapore" | GST, Free Trade Zone, suspended |
| "Transit time Singapore to Port Klang ocean" | transit, Malaysia, days |
| "Dangerous goods lithium battery shipping" | IMDG, UN, hazardous |
| "LCL consolidation booking lead time" | LCL, days, booking |
| "VGM verified gross mass container" | VGM, weight, SOLAS |
| "Import permit food products Indonesia" | BPOM, halal, Indonesia |
| "Customs duty preferential tariff ASEAN" | duty, preferential, FTA |
| "Bill of Lading vs Sea Waybill difference" | BL, waybill, document |

- PASS: Results contain at least 2 of expected keywords
- Target: 8+/10 pass

### Output Format

```
================================================================================
Waypoint Ingestion Verification
================================================================================

Configuration:
  Collection: waypoint_kb
  Total Chunks: 483

--------------------------------------------------------------------------------
Check 1: Total Chunk Count
--------------------------------------------------------------------------------
  Expected: 450-520 chunks
  Actual:   483 chunks
  Status:   PASS ✓

--------------------------------------------------------------------------------
Check 2: Category Distribution
--------------------------------------------------------------------------------
  01_regulatory:        245 chunks (50.7%)
  02_carriers:           98 chunks (20.3%)
  03_reference:          52 chunks (10.8%)
  04_internal_synthetic: 88 chunks (18.2%)
  Status: PASS ✓ (all 4 categories present)

--------------------------------------------------------------------------------
Check 3: Metadata Integrity
--------------------------------------------------------------------------------
  Sampled: 10 chunks
  Complete: 10/10
  Status: PASS ✓

--------------------------------------------------------------------------------
Check 4: Tier 1 - Category Retrieval (8 queries)
--------------------------------------------------------------------------------
  [1/8] "Singapore GST import requirements"
        Expected: 01_regulatory | Found: 01_regulatory | PASS
  [2/8] "ATIGA Certificate of Origin Form D"
        Expected: 01_regulatory | Found: 01_regulatory | PASS
  ...
  Tier 1 Results: 8/8 PASS

--------------------------------------------------------------------------------
Check 5: Tier 2 - Document Retrieval (12 queries)
--------------------------------------------------------------------------------
  [1/12] "Singapore export permit requirements"
         Expected: sg_export_procedures | Found: sg_export_procedures | PASS
  ...
  Tier 2 Results: 11/12 PASS

--------------------------------------------------------------------------------
Check 6: Tier 3 - Scenario Tests (10 queries)
--------------------------------------------------------------------------------
  [1/10] "What documents needed FCL export Singapore to Jakarta"
         Keywords: export ✓, Indonesia ✓, commercial invoice ✓, Bill of Lading ✓
         Status: PASS (4/4 keywords)
  ...
  Tier 3 Results: 9/10 PASS

================================================================================
SUMMARY
================================================================================
  Check 1 (Chunk Count):      PASS
  Check 2 (Categories):       PASS
  Check 3 (Metadata):         PASS
  Check 4 (Tier 1):           8/8 PASS
  Check 5 (Tier 2):           11/12 PASS
  Check 6 (Tier 3):           9/10 PASS

  Overall: 28/30 tests passed (93.3%)
  Status: PASS ✓
================================================================================
```

### Constraints
- Use ChromaDB's built-in query method
- Query with `n_results=5` for retrieval tests
- Case-insensitive keyword matching
- Handle Unicode gracefully (use `[PASS]`/`[FAIL]` instead of ✓/✗ for Windows)

### TDD Requirements
- [ ] Test file created at `tests/test_verify_ingestion.py` FIRST
- [ ] Tests for each check function
- [ ] Run tests to see them fail (Red)
- [ ] Implement code to make tests pass (Green)
- [ ] All tests pass

### Acceptance Criteria
- [ ] File created at `scripts/verify_ingestion.py`
- [ ] Check 1: Chunk count validation works
- [ ] Check 2: Category distribution works
- [ ] Check 3: Metadata integrity works
- [ ] Check 4: Tier 1 tests implemented (8 queries)
- [ ] Check 5: Tier 2 tests implemented (12 queries)
- [ ] Check 6: Tier 3 tests implemented (10 queries)
- [ ] Clear pass/fail reporting
- [ ] Summary with total pass rate
- [ ] Overall: 28+/30 tests pass

---

## Format

### Output Structure
```
scripts/
├── config.py
├── process_docs.py
├── chunker.py
├── ingest.py
└── verify_ingestion.py    # New file

tests/
├── test_process_docs.py
├── test_chunker.py
├── test_ingest.py
└── test_verify_ingestion.py  # New file (create FIRST - TDD)
```

### Code Style
- Python 3.11+ type hints
- argparse for CLI
- Functions for each check
- Clear separation of test definition and execution

### Module Structure
```python
"""
Verification script for Waypoint ingestion pipeline.

Validates chunk count, category distribution, metadata integrity,
and retrieval quality across three tiers.
"""

import argparse
import random
from typing import Optional

import chromadb
from chromadb.utils import embedding_functions

from scripts.config import CHROMA_PERSIST_PATH, COLLECTION_NAME

# Test definitions
TIER_1_TESTS = [
    {"query": "...", "expected_category": "01_regulatory"},
    # ...
]

TIER_2_TESTS = [
    {"query": "...", "expected_doc": "sg_export_procedures"},
    # ...
]

TIER_3_TESTS = [
    {"query": "...", "expected_keywords": ["export", "Indonesia", ...]},
    # ...
]


def parse_args(args: Optional[list] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    ...


def get_collection():
    """Get ChromaDB collection."""
    ...


def check_chunk_count(collection, verbose: bool = False) -> tuple[bool, dict]:
    """Check 1: Verify total chunk count."""
    ...


def check_category_distribution(collection, verbose: bool = False) -> tuple[bool, dict]:
    """Check 2: Verify all categories present."""
    ...


def check_metadata_integrity(collection, verbose: bool = False) -> tuple[bool, dict]:
    """Check 3: Verify metadata completeness."""
    ...


def check_tier1_retrieval(collection, verbose: bool = False) -> tuple[bool, dict]:
    """Check 4: Category-level retrieval tests."""
    ...


def check_tier2_retrieval(collection, verbose: bool = False) -> tuple[bool, dict]:
    """Check 5: Document-level retrieval tests."""
    ...


def check_tier3_scenarios(collection, verbose: bool = False) -> tuple[bool, dict]:
    """Check 6: Complex scenario tests."""
    ...


def run_verification(args: argparse.Namespace) -> dict:
    """Run all verification checks."""
    ...


def print_summary(results: dict):
    """Print verification summary."""
    ...


def main():
    """Main entry point."""
    ...


if __name__ == "__main__":
    main()
```

### Validation Commands
```bash
# Run tests first (TDD)
python -m pytest tests/test_verify_ingestion.py -v

# Run full verification
python -m scripts.verify_ingestion

# Run with verbose output
python -m scripts.verify_ingestion --verbose

# Run specific tier
python -m scripts.verify_ingestion --tier 1

# Run specific check
python -m scripts.verify_ingestion --check 4
```

---

## Execution Checklist (TDD Order)

1. [ ] Create `tests/test_verify_ingestion.py` with test cases
2. [ ] Run tests - verify they fail (Red)
3. [ ] Create `scripts/verify_ingestion.py` with implementation
4. [ ] Run tests - verify they pass (Green)
5. [ ] Run full verification: `python -m scripts.verify_ingestion`
6. [ ] Verify 28+/30 tests pass
7. [ ] Update REPORT.md
