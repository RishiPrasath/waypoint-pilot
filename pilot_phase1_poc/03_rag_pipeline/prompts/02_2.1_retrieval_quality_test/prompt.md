# Task 2.1: Create Retrieval Quality Test Script

## Persona

> You are a Python developer with expertise in RAG systems and evaluation pipelines.
> You follow data-driven testing practices and generate clear, actionable reports.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. Week 1 completed ingestion (29 docs → 483 chunks). Before building the full RAG pipeline, we must validate retrieval quality using 50 test queries to ensure chunking effectiveness.

### Current State
- ChromaDB populated with 483 chunks (11 metadata fields including source_urls)
- 50 test queries defined in `00_docs/02_use_cases.md` (Test Query Bank section)
- Ingestion venv available at `03_rag_pipeline/ingestion/venv/`

### Reference Documents
- `00_docs/02_use_cases.md` - Test Query Bank (lines 394-456)
- `03_rag_pipeline/docs/00_week2_rag_pipeline_plan.md` - Retrieval quality requirements
- `03_rag_pipeline/ingestion/scripts/verify_ingestion.py` - Example query pattern

### Dependencies
- Task 1.1: Copy KB and Ingestion ✅
- Task 1.2: Fix source_urls ✅

---

## Task

### Objective
Create a Python script that tests all 50 queries against ChromaDB and generates detailed quality reports for decision-making.

### Requirements

1. **Create retrieval_quality_test.py**
   - Location: `03_rag_pipeline/scripts/retrieval_quality_test.py`
   - Uses ChromaDB from `../ingestion/chroma_db/`
   - Configurable top_k (default: 5) and threshold (default: 0.15)

2. **Implement 50 test queries** (from 02_use_cases.md):
   - Booking & Documentation (10 queries)
   - Customs & Regulatory (10 queries)
   - Carrier Information (10 queries)
   - SLA & Service (10 queries)
   - Edge Cases & Out-of-Scope (10 queries)

3. **For each query, capture**:
   - Query text and category
   - Top-5 retrieved chunks (doc_id, title, similarity score)
   - Whether relevant document appears in top-3 (hit/miss)
   - Section headers retrieved

4. **Generate outputs**:
   - JSON: `data/retrieval_test_results.json` (raw data)
   - Markdown: `reports/retrieval_quality_REPORT.md` (human-readable)

### Specifications

**Test Queries** (all 50 from 02_use_cases.md):

```python
TEST_QUERIES = {
    "booking_documentation": [
        "What documents are needed for sea freight Singapore to Indonesia?",
        "How far in advance should I book an LCL shipment?",
        "What's the difference between FCL and LCL?",
        "When is the SI cutoff for this week's Maersk sailing?",
        "Do I need a commercial invoice for samples with no value?",
        "What's a Bill of Lading and who issues it?",
        "Can we ship without a packing list?",
        "What does FOB Singapore mean?",
        "How do I amend a booking after confirmation?",
        "What's the free time at destination port?",
    ],
    "customs_regulatory": [
        "What's the GST rate for imports into Singapore?",
        "How do I find the HS code for electronics?",
        "Is Certificate of Origin required for Thailand?",
        "What permits are needed to import cosmetics to Indonesia?",
        "What's the ATIGA preferential duty rate?",
        "How does the Free Trade Zone work for re-exports?",
        "What's the de minimis threshold for Malaysia?",
        "Do I need halal certification for food to Indonesia?",
        "How do I apply for a Customs ruling on HS code?",
        "What's the difference between Form D and Form AK?",
    ],
    "carrier_information": [
        "Which carriers sail direct to Ho Chi Minh?",
        "What's the transit time to Port Klang?",
        "Does PIL offer reefer containers?",
        "How do I submit VGM to Maersk?",
        "Can I get an electronic Bill of Lading?",
        "What's the weight limit for a 40ft container?",
        "Does ONE service Surabaya?",
        "How do I track my shipment with Evergreen?",
        "What's the difference between Maersk and ONE service?",
        "Who do I contact for a booking amendment?",
    ],
    "sla_service": [
        "What's our standard delivery SLA for Singapore?",
        "Is customs clearance included in door-to-door?",
        "Do you provide cargo insurance?",
        "What happens if shipment is delayed?",
        "Are duties and taxes included in the quote?",
        "What's the process for refused deliveries?",
        "Do you handle import permit applications?",
        "How do I upgrade to express service?",
        "What's covered under standard liability?",
        "Can I get proof of delivery?",
    ],
    "edge_cases_out_of_scope": [
        "What's the current freight rate to Jakarta?",
        "Where is my shipment right now?",
        "Can you book a shipment for me?",
        "I want to file a claim for damaged cargo",
        "Can you ship hazmat by air?",
        "What's the weather forecast for shipping?",
        "Can you recommend a supplier in China?",
        "What's your company's financial status?",
        "How do I become a freight forwarder?",
        "What are your competitor's rates?",
    ],
}
```

**Expected Document Mappings** (for hit rate calculation):

```python
EXPECTED_SOURCES = {
    # Booking queries → should retrieve from these docs
    "What documents are needed for sea freight Singapore to Indonesia?": ["sg_export_procedures", "indonesia_import"],
    "What does FOB Singapore mean?": ["incoterms_2020_reference", "incoterms_comparison"],
    # Customs queries
    "What's the GST rate for imports into Singapore?": ["sg_gst_guide"],
    "Is Certificate of Origin required for Thailand?": ["sg_certificates_of_origin", "atiga_overview"],
    # Carrier queries
    "Which carriers sail direct to Ho Chi Minh?": ["pil_service", "maersk_service", "one_service"],
    # SLA queries
    "What's our standard delivery SLA for Singapore?": ["sla_policy"],
    # Out-of-scope should return LOW scores or irrelevant docs
}
```

**Report Structure**:

```markdown
# Retrieval Quality Report

**Generated**: [timestamp]
**Total Queries**: 50
**Top-K**: 5
**Threshold**: 0.15

## Summary

| Category | Queries | Hits (Top-3) | Hit Rate |
|----------|---------|--------------|----------|
| Booking & Documentation | 10 | X | X% |
| Customs & Regulatory | 10 | X | X% |
| Carrier Information | 10 | X | X% |
| SLA & Service | 10 | X | X% |
| Edge Cases | 10 | X | X% |
| **TOTAL** | 50 | X | X% |

## Decision Gate

| Quality Level | Threshold | Action |
|---------------|-----------|--------|
| ≥75% | PROCEED | Build retrieval service |
| 60-74% | INVESTIGATE | Review failures, minor fixes |
| <60% | REMEDIATE | Chunking optimization needed |

**Result**: [PROCEED/INVESTIGATE/REMEDIATE]

## Top 10 Failures

| Query | Expected | Got | Score |
|-------|----------|-----|-------|
| ... | ... | ... | ... |

## Per-Category Details

### Booking & Documentation
| Query | Top Result | Score | Hit? |
| ... | ... | ... | ... |

[repeat for each category]
```

### Constraints
- Use existing ChromaDB embeddings (don't re-embed)
- Don't modify ingestion code
- Script must work from `03_rag_pipeline/` directory
- Create `data/` and `reports/` directories if needed

### Acceptance Criteria
- [ ] Script created at `scripts/retrieval_quality_test.py`
- [ ] All 50 queries tested
- [ ] JSON output at `data/retrieval_test_results.json`
- [ ] Markdown report at `reports/retrieval_quality_REPORT.md`
- [ ] Hit rate calculated per category
- [ ] Top 10 failures documented with analysis
- [ ] Decision gate recommendation included

### TDD Requirements
- [ ] Test file at `tests/test_retrieval_quality.py` (optional - script is primarily evaluation)

---

## Format

### Output Structure

```
03_rag_pipeline/
├── scripts/
│   └── retrieval_quality_test.py
├── data/
│   └── retrieval_test_results.json
├── reports/
│   └── retrieval_quality_REPORT.md
└── tests/
    └── test_retrieval_quality.py (optional)
```

### Code Style

```python
"""
Retrieval Quality Test Script

Tests 50 queries against ChromaDB and generates quality reports.
"""

import json
from datetime import datetime
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

# Configuration
TOP_K = 5
THRESHOLD = 0.15
CHROMA_PATH = Path(__file__).parent.parent / "ingestion" / "chroma_db"
COLLECTION_NAME = "waypoint_kb"

def run_query(collection, query: str, top_k: int = TOP_K) -> list[dict]:
    """Run a single query and return results with scores."""
    pass

def calculate_hit_rate(results: list[dict], expected_sources: dict) -> float:
    """Calculate hit rate for a set of results."""
    pass

def generate_json_report(results: dict, output_path: Path):
    """Save raw results to JSON."""
    pass

def generate_markdown_report(results: dict, output_path: Path):
    """Generate human-readable markdown report."""
    pass

def main():
    """Run all tests and generate reports."""
    pass

if __name__ == "__main__":
    main()
```

### Validation Commands

```bash
cd pilot_phase1_poc/03_rag_pipeline

# Create directories
mkdir -p data reports

# Run from ingestion venv (has chromadb)
cd ingestion
venv/Scripts/activate
cd ..

# Run test script
python scripts/retrieval_quality_test.py

# Verify outputs
cat reports/retrieval_quality_REPORT.md
cat data/retrieval_test_results.json | python -m json.tool | head -50
```

### Expected Output

```
Running retrieval quality tests...

Testing booking_documentation (10 queries)...
  [1/10] "What documents are needed..." → sg_export_procedures (0.32) ✓
  [2/10] "How far in advance..." → booking_procedure (0.28) ✓
  ...

Testing customs_regulatory (10 queries)...
  ...

=== SUMMARY ===
Total queries: 50
Overall hit rate: XX%
Decision: [PROCEED/INVESTIGATE/REMEDIATE]

Reports generated:
  - data/retrieval_test_results.json
  - reports/retrieval_quality_REPORT.md
```
