# Evaluation & Documentation - Test Plan

**Initiative:** enhancement--poc-evaluation
**Last Updated:** 2026-02-09

---

## Test Categories

| Category | Purpose | Count |
|----------|---------|-------|
| Ingestion Unit (Python/pytest) | Document processing, chunking, metadata | ~87 existing + new metadata tests |
| Retrieval Quality (Python) | 50-query hit rate validation | 50 |
| Backend Unit (Jest) | API routes, services, pipeline | ~105 existing + new endpoint/error tests |
| Frontend Unit (Vitest) | React components, rendering | New (4 sections) |
| E2E Evaluation | Full pipeline 50-query automated test | 50 |
| Visual Verification | Chrome DevTools MCP interactive | Manual |

---

## Test Cases by Layer

### Layer 1: Ingestion Pipeline

| ID | Description | Type | Status |
|----|-------------|------|--------|
| L1.1 | Re-run all 87 existing ingestion tests | Unit | ⬜ |
| L1.2 | Validate source_urls preserved in ChromaDB chunks | Unit | ⬜ |
| L1.3 | Validate category field preserved per chunk | Unit | ⬜ |
| L1.4 | Validate retrieval_keywords preserved per chunk | Unit | ⬜ |

### Layer 2: RAG Pipeline

| ID | Description | Type | Status |
|----|-------------|------|--------|
| L2.1 | Re-run 50-query retrieval hit rate (target: 92%) | Integration | ⬜ |
| L2.2 | Context assembly / formatting tests | Unit | ⬜ |
| L2.3 | Prompt construction with new formatting instructions | Unit | ⬜ |
| L2.4 | LLM call handling and error cases | Unit | ⬜ |
| L2.5 | Citation service: source_urls flow through enrichment | Unit | ⬜ |
| L2.6 | Citation service: category flow through enrichment | Unit | ⬜ |

### Layer 3: Express Backend

| ID | Description | Type | Status |
|----|-------------|------|--------|
| L3.1 | Update api.test.js for new response structure | Unit | ⬜ |
| L3.2 | Update pipeline.test.js for new response structure | Unit | ⬜ |
| L3.3 | Update retrieval.test.js for new response structure | Unit | ⬜ |
| L3.4 | Update llm.test.js for new response structure | Unit | ⬜ |
| L3.5 | /api/query returns all 4 sections with correct types | Integration | ⬜ |
| L3.6 | sources array shape validation | Integration | ⬜ |
| L3.7 | relatedDocs array shape validation | Integration | ⬜ |
| L3.8 | Empty query handling | Edge Case | ⬜ |
| L3.9 | Very long query handling | Edge Case | ⬜ |
| L3.10 | Groq API timeout handling | Edge Case | ⬜ |
| L3.11 | ChromaDB connection failure handling | Edge Case | ⬜ |

### Layer 4: React Frontend

| ID | Description | Type | Status |
|----|-------------|------|--------|
| L4.1 | Answer section: markdown rendering (headers, lists, bold) | Unit | ⬜ |
| L4.2 | Sources section: clickable URLs with org name | Unit | ⬜ |
| L4.3 | Related Documents: category chips with icons | Unit | ⬜ |
| L4.4 | Confidence Footer: colored badge + stats | Unit | ⬜ |
| L4.5 | Visual: all 4 sections render at desktop resolution | Visual | ⬜ |

### Layer 5: E2E Evaluation

| ID | Description | Type | Status |
|----|-------------|------|--------|
| L5.1 | 50 queries execute via POST /api/query | E2E | ⬜ |
| L5.2 | must_contain keyword validation per query | E2E | ⬜ |
| L5.3 | must_not_contain hallucination detection | E2E | ⬜ |
| L5.4 | expected_docs retrieval validation | E2E | ⬜ |
| L5.5 | Citation presence validation | E2E | ⬜ |
| L5.6 | Latency threshold (< 5s) validation | E2E | ⬜ |
| L5.7 | OOS query handling validation | E2E | ⬜ |
| L5.8 | Deflection rate calculation | E2E | ⬜ |

---

## Commands

```bash
# Python tests (ingestion + retrieval)
cd pilot_phase1_poc/05_evaluation
venv/Scripts/activate
python -m pytest tests/ -v

# Retrieval quality
python scripts/retrieval_quality_test.py

# Jest tests (backend)
npm test

# Frontend tests (Vitest)
cd client && npm test

# E2E evaluation harness
python scripts/evaluation_test.py
```
