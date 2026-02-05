# Retrieval Optimization - Test Plan

**Initiative**: Retrieval Optimization (Week 3)
**Last Updated**: 2026-02-05

---

## Test Overview

| Test Type | Tool | When Run | Success Criteria |
|-----------|------|----------|------------------|
| Unit Tests | pytest | After code changes | All tests pass |
| Ingestion Verify | verify_ingestion.py | After each ingestion | Doc/chunk counts match |
| Retrieval Quality | retrieval_quality_test.py | After ingestion | ≥80% adjusted hit rate |
| E2E Tests | e2e_test.py | After RAG update | 30/30 pass |

---

## 1. Unit Tests

### Location
`pilot_phase1_poc/04_retrieval_optimization/tests/`

### Test Files
| File | Module Tested | Key Tests |
|------|---------------|-----------|
| `test_process_docs.py` | `scripts/process_docs.py` | Document parsing, frontmatter |
| `test_chunker.py` | `scripts/chunker.py` | Chunking, metadata |
| `test_pdf_extractor.py` | `scripts/pdf_extractor.py` | PDF extraction, quality flags |

### Running Unit Tests
```bash
cd pilot_phase1_poc/04_retrieval_optimization
venv\Scripts\activate
python -m pytest tests/ -v
```

### Coverage Requirements
- All public functions must have at least one test
- Edge cases for chunk boundaries
- Error handling for malformed documents

---

## 2. Ingestion Verification

### Purpose
Verify that all documents are properly ingested into ChromaDB.

### Checks
1. **Document Count**: Expected vs. actual documents processed
2. **Chunk Count**: Within expected range (varies with content)
3. **Category Distribution**: All 4 categories present
4. **Metadata Completeness**: All required fields populated

### Running Verification
```bash
python scripts/verify_ingestion.py
python scripts/verify_ingestion.py --verbose
```

### Expected Output
```
Documents processed: [N]
Chunks created: [M]
Categories: 4/4
Metadata coverage: 100%
Status: PASS
```

---

## 3. Retrieval Quality Test

### Purpose
Measure retrieval accuracy against the 50-query test bank.

### Test Configuration
| Parameter | Value | Notes |
|-----------|-------|-------|
| top_k | 5 | Number of chunks retrieved |
| threshold | 0.15 | Minimum relevance score |
| query_set | 50 | All queries from 02_use_cases.md |

### Scoring Rules

**In-Scope Queries** (47 after reclassification):
- **Pass**: Top-k results include relevant chunk(s)
- **Fail**: No relevant chunk in top-k

**Out-of-Scope Queries** (#36, #38, #44):
- **Pass**: System would appropriately decline (or low-relevance results)
- **Fail**: N/A - these are expected to not match

### Running Retrieval Test
```bash
python scripts/retrieval_quality_test.py
python scripts/retrieval_quality_test.py --verbose
python scripts/retrieval_quality_test.py --category Booking
```

### Expected Output
```
=== Retrieval Quality Test Results ===

Overall (Raw): XX/50 (XX%)
Overall (Adjusted): XX/50 (XX%)

By Category:
  Booking: X/10 (XX%)
  Customs: X/10 (XX%)
  Carrier: X/10 (XX%)
  SLA: X/10 (XX%)
  Edge Cases: X/10 (XX%)

Failures:
  Query #X: [query text] - [reason]
  ...
```

### Targets
| Metric | Minimum | Stretch |
|--------|---------|---------|
| Overall (Adjusted) | 80% (40/50) | 90% (45/50) |
| No new regressions | 0 | 0 |

---

## 4. E2E Tests

### Purpose
Validate the complete RAG pipeline from query to response.

### Test Scope
- API health check
- Query processing
- Retrieval accuracy
- LLM response generation
- Source citation

### Running E2E Tests
```bash
cd pilot_phase1_poc/03_rag_pipeline
npm test
python -m scripts.e2e_test
```

### Expected Results
- 30/30 tests pass
- Response latency <5s
- All responses include source citations

---

## 5. Parameter Experiment Tests

### Purpose
Compare retrieval quality across different chunking/retrieval configurations.

### Configurations to Test
| Experiment | CHUNK_SIZE | CHUNK_OVERLAP | top_k |
|------------|------------|---------------|-------|
| Baseline | 600 | 90 | 5 |
| A | 800 | 120 | 5 |
| B | 1000 | 150 | 5 |
| C | Best from A/B | Best | 10 |

### Test Protocol
1. Update `.env` with new parameters
2. Re-run `ingest.py --clear`
3. Run `retrieval_quality_test.py`
4. Record results in validation report

### Results Template
| Experiment | Adjusted Hit Rate | Delta vs. Baseline | Notes |
|------------|-------------------|-------------------|-------|
| Baseline | XX% | - | |
| A | XX% | +/-X% | |
| B | XX% | +/-X% | |
| C | XX% | +/-X% | |

---

## 6. Pre-Completion Checklist

Before marking any task complete:

- [ ] Unit tests pass (`pytest tests/ -v`)
- [ ] Ingestion verification passes (`verify_ingestion.py`)
- [ ] Retrieval quality meets target (`retrieval_quality_test.py`)
- [ ] No regressions from previous runs
- [ ] Code follows style guidelines
- [ ] Documentation updated

---

## Validation Commands Quick Reference

```bash
# Activate environment
cd pilot_phase1_poc/04_retrieval_optimization
venv\Scripts\activate

# Unit tests
python -m pytest tests/ -v

# Ingestion
python scripts/ingest.py --clear
python scripts/verify_ingestion.py

# Retrieval quality
python scripts/retrieval_quality_test.py

# E2E (from RAG pipeline)
cd ../03_rag_pipeline
npm test
```
