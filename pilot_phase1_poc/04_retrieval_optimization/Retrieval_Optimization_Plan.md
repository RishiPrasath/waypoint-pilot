# Retrieval Optimization Plan

**Project**: Waypoint Phase 1 POC — Week 3
**Folder**: `04_retrieval_optimization/`
**Time box**: Thursday 5 Feb (evening) → Sunday 9 Feb (end of day)
**Executor**: Rishi (directing) + Claude Code (executing)
**Baseline**: 76% retrieval hit rate (adjusted to ~82% after reclassification), 29 docs, 483 chunks
**Target**: ≥80% minimum (adjusted), 90% stretch goal
**Agent Instructions**: Root `CLAUDE.md` (Week 3 section, same pattern as Week 1/2)

---

## Confirmed Decisions (Pre-Execution)

| # | Decision | Date | Context |
|---|----------|------|---------|
| 1 | Query #44 reclassified as out-of-scope | 2026-02-05 | Claims processing excluded per `01_scope_definition.md` |
| 2 | Queries #36, #38 reclassified as out-of-scope | 2026-02-05 | No use case mapping; refused deliveries and express upgrade not in scope |
| 3 | 80% target measured on adjusted query set | 2026-02-05 | Reclassified queries pass if appropriately declined |
| 4 | Full KB rebuild from scratch | 2026-02-05 | PDF discovery justifies full pass; retrieval-first guidelines applied uniformly |
| 5 | Build pdf_extractor.py as specified | 2026-02-05 | Repeatable tooling for PDF-to-markdown conversion |
| 6 | Claude Code scrapes autonomously | 2026-02-05 | Rishi spot-checks 3–5 docs at review point |
| 7 | Chunking: keep current config for initial test, experiment after | 2026-02-05 | Rebuild content first, then test chunking params separately |
| 8 | Retrieval params: start with top_k=5, tune after Task 7 | 2026-02-05 | Clean comparison against Week 2 baseline first |
| 9 | Target: 80% minimum, 90% stretch goal | 2026-02-05 | Adjusted baseline ~82%; push for 90% by fixing remaining 9 failures |
| 10 | Task 9 must swap ChromaDB and confirm E2E | 2026-02-05 | Week 3 ends with full system on improved KB |
| 11 | All 3 review gates kept | 2026-02-05 | Rishi available Thu/Fri/Sat/Sun |
| 12 | Synthetic docs: restructure + create 1–2 new | 2026-02-05 | Fill content gaps identified by audit |
| 13 | CLAUDE.md: add Week 3 section to root only | 2026-02-05 | Same pattern as Week 1/2, no component-level file |
| 14 | Query bank: keep same 50, reclassify only | 2026-02-05 | No swaps; keeps Week 2/3 results comparable |
| 15 | Task 8: iterate until 90% or Sunday buffer exhausted | 2026-02-05 | No hard round limit; time-box is Sunday evening |
| 16 | Task 10: full Week 3 retrospective | 2026-02-05 | Include time spent, decisions, chunking experiments, lessons |
| 17 | Document count: flexible, PDFs can push beyond 29 | 2026-02-05 | Audit drives baseline; discovered PDFs may add new docs |
| 18 | Chunking config must be parameterized in forked pipeline | 2026-02-05 | Enable experiments via .env/CLI without editing code |
| 19 | New folder: `04_retrieval_optimization/` | 2026-02-05 | Standalone workspace for Week 3 rework |
| 20 | Fork ingestion pipeline, don't modify original | 2026-02-05 | Keep `02_ingestion_pipeline` as stable baseline |
| 21 | Claims processing stays out of scope | 2026-02-05 | Per `01_scope_definition.md` |

---

## Adjusted Baseline & Targets

**Week 2 Baseline (raw)**: 38/50 = 76%

**Reclassifications**:
- Query #36 ("refused deliveries") → out-of-scope
- Query #38 ("upgrade to express service") → out-of-scope
- Query #44 ("file a claim for damaged cargo") → out-of-scope

**Week 2 Baseline (adjusted)**: 41/50 = 82% (3 former failures now pass as appropriate declines)

**Remaining failures to fix (9)**:
| # | Query | Category | Current Score |
|---|-------|----------|---------------|
| 2 | How far in advance should I book an LCL shipment? | Booking | 0.057 |
| 5 | Do I need a commercial invoice for samples with no value? | Booking | -0.253 |
| 6 | What's a Bill of Lading and who issues it? | Booking | -0.070 |
| 7 | Can we ship without a packing list? | Booking | -0.024 |
| 15 | What's the ATIGA preferential duty rate? | Customs | 0.029 |
| 19 | How do I apply for a Customs ruling on HS code? | Customs | 0.340 |
| 31 | What's our standard delivery SLA for Singapore? | SLA | 0.185 |
| 32 | Is customs clearance included in door-to-door? | SLA | -0.038 |
| 37 | Do you handle import permit applications? | SLA | 0.203 |

**Targets**:
- **Minimum**: 80% adjusted (40/50) — already met on paper, must not regress
- **Stretch**: 90% adjusted (45/50) — requires fixing ≥4 of 9 remaining failures

---

## Folder Structure

```
pilot_phase1_poc/
└── 04_retrieval_optimization/
    ├── PLAN.md                          ← This document
    ├── REVISED_DOCUMENT_LIST.md         ← Task 3 output
    ├── kb/                              ← Fresh knowledge base (rebuilt)
    │   ├── 01_regulatory/
    │   │   ├── singapore_customs/
    │   │   │   ├── pdfs/                ← Source PDFs
    │   │   │   └── [markdown files]
    │   │   ├── asean_trade/
    │   │   │   ├── pdfs/
    │   │   │   └── [markdown files]
    │   │   └── country_specific/
    │   │       ├── pdfs/
    │   │       └── [markdown files]
    │   ├── 02_carriers/
    │   │   ├── ocean/
    │   │   │   ├── pdfs/
    │   │   │   └── [markdown files]
    │   │   └── air/
    │   │       ├── pdfs/
    │   │       └── [markdown files]
    │   ├── 03_reference/
    │   │   ├── incoterms/
    │   │   └── hs_codes/
    │   └── 04_internal_synthetic/
    │       ├── policies/
    │       ├── procedures/
    │       └── service_guides/
    ├── scripts/                         ← Forked + extended ingestion pipeline
    │   ├── pdf_extractor.py             ← NEW: PDF → markdown conversion
    │   ├── process_docs.py              ← Forked from 02_ingestion_pipeline
    │   ├── chunker.py                   ← Forked, potentially modified
    │   ├── ingest.py                    ← Forked, points to new kb/
    │   ├── config.py                    ← Forked, updated paths + parameterized chunking
    │   ├── retrieval_quality_test.py    ← Forked from 03_rag_pipeline/scripts
    │   ├── verify_ingestion.py          ← Forked
    │   └── view_chroma.py              ← Forked
    ├── chroma_db/                       ← New vector store
    ├── reports/
    │   ├── 01_audit_report.md           ← Task 1 output
    │   ├── 02_scope_reclassification.md ← Task 2 output
    │   ├── 03_retrieval_validation.md   ← Task 7 output (updated per phase)
    │   └── 04_final_comparison.md       ← Task 10 output (full retrospective)
    ├── prompts/                         ← PCTF task prompts (per convention)
    ├── logs/
    └── tests/
```

---

## Task Sequence Overview

```
PHASE 1: AUDIT (Thu evening – Fri morning)
  Task 1 → Task 2 → Task 3
  ⏸ Rishi reviews audit outputs, makes decisions

PHASE 2: INFRASTRUCTURE (Fri)
  Task 4 → Task 5

PHASE 3: KNOWLEDGE BASE REBUILD (Fri evening – Sat)
  Task 6 → Task 7
  ⏸ Rishi reviews KB quality, makes decisions

PHASE 4: INGESTION REFINEMENT & FINAL VALIDATION (Sun)
  Task 8 → Task 9 → Task 10
  ⏸ Rishi reviews final results
```

---

## PHASE 1: AUDIT

### Task 1: Root Cause Analysis of Retrieval Failures

**Purpose**: Determine exactly why each of the 9 remaining failing queries fails — content missing, content buried in bad chunks, or terminology mismatch.

**Note**: Queries #36, #38, #44 have been reclassified as out-of-scope and are excluded from this analysis.

**Inputs**:
- 9 failing queries from `03_rag_pipeline/reports/retrieval_quality_REPORT.md` (query numbers: 2, 5, 6, 7, 15, 19, 31, 32, 37)
- Raw documents in `01_knowledge_base/kb/`
- ChromaDB at `02_ingestion_pipeline/chroma_db/`

**Sequence**:
1. Parse the retrieval quality report to extract the 9 failing queries
2. For each failing query:
   a. **Search raw markdown files** in `01_knowledge_base/kb/` — text search for key terms and synonyms. Record whether the information exists and which file/section it's in.
   b. **Search ChromaDB chunks** — query the vector store, examine the top-5 returned chunks. Record what was returned and why it didn't match.
   c. **Classify the root cause**:
      - **(a) Content missing**: The answer doesn't exist in any document
      - **(b) Content buried**: The answer exists but the chunk it lands in is too generic, too short, or split awkwardly across chunk boundaries
      - **(c) Terminology mismatch**: The answer exists and chunks well, but the query uses different words than the document
3. For each failure, propose a specific fix (new document, restructure section, add synonyms)

**Output**: `04_retrieval_optimization/reports/01_audit_report.md`

**Output format per query**:
```
### Query #[N]: "[query text]"
- **Expected source**: [document that should answer this]
- **Raw doc search**: [FOUND in file X, section Y / NOT FOUND]
- **Chunk search**: [top chunk returned, score, why wrong]
- **Root cause**: (a) missing / (b) buried / (c) terminology
- **Proposed fix**: [specific action]
```

**Acceptance Criteria**:
- [ ] All 9 failing queries analysed
- [ ] Each has a root cause classification (a/b/c)
- [ ] Each has a specific proposed fix
- [ ] Report saved

**Estimated Time**: 1–1.5 hours

---

### Task 2: Scope Reclassification of All 50 Test Queries

**Purpose**: Re-evaluate every test query against `01_scope_definition.md` and `02_use_cases.md`. Apply the pre-confirmed reclassifications and check for any additional mismatches.

**Pre-confirmed reclassifications**:
- Query #36 ("refused deliveries") → out-of-scope
- Query #38 ("upgrade to express service") → out-of-scope
- Query #44 ("file a claim for damaged cargo") → out-of-scope

**Inputs**:
- 50 test queries from `00_docs/02_use_cases.md` (Test Query Bank section)
- Scope definition: `00_docs/01_scope_definition.md`
- Use case catalog: `00_docs/02_use_cases.md`

**Key scope rules** (from 01_scope_definition.md):
- **In scope**: Shipment booking, customs/documentation, carrier selection guidance
- **Secondary**: COD procedures (P2), SLA inquiries (P2), service scope clarification (P3)
- **Out of scope**: Live tracking, actual booking execution, rate quotations, claims processing, hazmat/DG, multi-country regulatory comparison

**Sequence**:
1. For each of the 50 queries, determine:
   - Which use case it maps to (UC-X.X)
   - Priority level (P1/P2/P3/Out of scope)
   - Current categorisation in the test bank
   - Whether current categorisation is correct
2. Apply the 3 pre-confirmed reclassifications (#36, #38, #44)
3. Check remaining queries for additional mismatches
4. Flag any further reclassification candidates for Rishi's review

**Output**: `04_retrieval_optimization/reports/02_scope_reclassification.md`

**Output format**: Table with columns — Query #, Query Text, Current Category, Mapped UC, Priority, Reclassified Category, Change? (Y/N), Notes

**Important**: The query bank itself (in `02_use_cases.md`) is NOT modified. Reclassifications are tracked only in this report and in the retrieval test scoring logic.

**Acceptance Criteria**:
- [ ] All 50 queries reclassified
- [ ] Pre-confirmed reclassifications (#36, #38, #44) applied
- [ ] Each mapped to a use case or marked out-of-scope with justification
- [ ] Additional mismatches highlighted for Rishi's review
- [ ] Report saved

**Estimated Time**: 45 min – 1 hour

---

**⏸ REVIEW POINT 1**: Rishi reviews Task 1 and Task 2 outputs. Decides:
- Which root cause fixes to pursue
- Whether any additional reclassifications flagged in Task 2 should be accepted
- Confirms direction for Task 3

---

### Task 3: Define the Revised Document List

**Purpose**: Based on the audit (Task 1) and reclassification (Task 2), produce the definitive list of documents for the new KB — what to re-scrape, what to restructure, what new docs to create, and what PDFs to look for.

**Inputs**:
- `04_retrieval_optimization/reports/01_audit_report.md` (Task 1)
- `04_retrieval_optimization/reports/02_scope_reclassification.md` (Task 2)
- Existing document list: `01_knowledge_base/PROGRESS_CHECKLIST.md`
- KB blueprint: `00_docs/03_knowledge_base_blueprint.md`
- Use case catalog: `00_docs/02_use_cases.md`

**Sequence**:
1. Start with the existing 29-document list
2. Apply Task 1 fixes:
   - New documents needed for root cause (a) failures
   - Documents needing restructure for root cause (b) failures
   - Documents needing enrichment for root cause (c) failures
3. Apply Task 2 reclassifications:
   - Remove any documents only needed for out-of-scope queries
   - Add any documents needed for queries reclassified as in-scope
4. Identify where 1–2 new synthetic documents should be created to fill content gaps (per confirmed decision)
5. Cross-reference against use case catalog to ensure every P1 and P2 use case has a document home
6. For each document, specify:
   - Action: **RE-SCRAPE** / **RESTRUCTURE** / **CREATE NEW** / **CARRY FORWARD**
   - Source URL(s) with "scan for PDFs" note where applicable
   - Target test queries it must answer
   - Retrieval-first content notes
7. Document count is flexible — if PDFs discovered during scraping add valuable new content, they become new documents

**Retrieval-first content guidelines** (apply to all documents):
1. **Key Facts summary** — first 600 characters must be a natural-language paragraph with the most important retrievable facts (not a table of contents)
2. **Customer-language headers** — section headers should match how customers ask questions
3. **Self-contained paragraphs** for critical facts — not buried in tables only
4. **One concept per section** — split mixed sections for cleaner chunking
5. **Synonym/alias mentions** — all common names for a concept in the first paragraph where it appears
6. **Cross-references** — related documents listed at the bottom

**Updated scraper rules** (apply to all re-scraped documents):
1. When visiting a source website, scan the page for downloadable PDFs, guides, circulars, manuals
2. Download relevant PDFs to the `pdfs/` subfolder within the document's category folder
3. Only download PDFs directly relevant to the document's topic
4. File types to look for: PDF, XLSX (tariff schedules). Skip: ZIP, installers, video
5. Record the PDF source URL in frontmatter under `source_pdfs`

**Updated frontmatter template**:
```yaml
---
title: [Document Title]
source_organization: [Org Name]
source_urls:
  - url: https://...
    description: [what this page covers]
    retrieved_date: YYYY-MM-DD
source_pdfs:
  - filename: [local filename in pdfs/]
    source_url: https://...
    description: [what this PDF covers]
    retrieved_date: YYYY-MM-DD
source_type: [public_regulatory | public_carrier | synthetic_internal]
last_updated: YYYY-MM-DD
jurisdiction: [SG | MY | ID | TH | VN | PH | ASEAN | Global]
category: [customs | carrier | policy | procedure | reference]
use_cases: [UC-1.1, UC-2.3]
keywords: [keyword1, keyword2, keyword3]
answers_queries:
  - "Query text this document should answer"
related_documents: [other_doc_id_1, other_doc_id_2]
---
```

**Output**: `04_retrieval_optimization/REVISED_DOCUMENT_LIST.md`

**Acceptance Criteria**:
- [ ] Every P1 and P2 use case has at least one document assigned
- [ ] Every in-scope failing query (from Task 1) has a fix assigned to a document
- [ ] Each document has an action (re-scrape/restructure/create/carry forward)
- [ ] Each re-scrape document includes "scan for PDFs" instruction
- [ ] 1–2 new synthetic documents identified where content gaps exist
- [ ] Updated frontmatter template documented
- [ ] Retrieval-first content guidelines documented
- [ ] Saved to `04_retrieval_optimization/REVISED_DOCUMENT_LIST.md`

**Estimated Time**: 1–1.5 hours

---

**⏸ REVIEW POINT 1 (continued)**: Rishi reviews the revised document list. Approves, adjusts, or rejects specific documents before scraping begins.

---

## PHASE 2: INFRASTRUCTURE

### Task 4: Set Up 04_retrieval_optimization Folder

**Purpose**: Create the folder structure and fork the ingestion pipeline with parameterized chunking config.

**Sequence**:
1. Create the `04_retrieval_optimization/` directory structure as specified in the Folder Structure section
2. Copy ingestion pipeline from `02_ingestion_pipeline/`:
   - `scripts/*.py` → `04_retrieval_optimization/scripts/`
   - `requirements.txt` → `04_retrieval_optimization/`
   - `.env` and `.env.example` → `04_retrieval_optimization/`
   - `tests/` → `04_retrieval_optimization/tests/`
   - Do NOT copy: `chroma_db/`, `logs/`, `venv/`, `__pycache__/`
3. Copy `retrieval_quality_test.py` from `03_rag_pipeline/scripts/`
4. Update `config.py`:
   - `KNOWLEDGE_BASE_PATH` → points to `04_retrieval_optimization/kb/`
   - `CHROMA_PERSIST_PATH` → points to `04_retrieval_optimization/chroma_db/`
   - **Parameterize chunking**: `CHUNK_SIZE`, `CHUNK_OVERLAP`, and `SEPARATORS` must be configurable via `.env` variables with current values as defaults:
     ```python
     CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "600"))
     CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "90"))
     ```
5. Create empty `kb/` category folders with `pdfs/` subfolders
6. Set up Python virtual environment
7. Verify pipeline runs (empty KB, no errors)

**Acceptance Criteria**:
- [ ] All folders created
- [ ] Pipeline scripts copied and paths updated
- [ ] Chunking parameters configurable via `.env` (CHUNK_SIZE, CHUNK_OVERLAP)
- [ ] Virtual environment working
- [ ] `process_docs.py` runs without errors on empty KB
- [ ] `retrieval_quality_test.py` present and importable

**Estimated Time**: 30–45 min

---

### Task 5: Build PDF Extraction Script

**Purpose**: Create a script that extracts text from PDF files and produces clean markdown with frontmatter template, so the existing pipeline can ingest them.

**Sequence**:
1. Add `pymupdf4llm` to `requirements.txt`
2. Create `scripts/pdf_extractor.py` with:
   - **Single file mode**: `python scripts/pdf_extractor.py path/to/file.pdf`
   - **Batch mode**: `python scripts/pdf_extractor.py --batch path/to/pdfs/`
   - Output markdown goes to the PARENT directory of the `pdfs/` folder (e.g., input `kb/01_regulatory/singapore_customs/pdfs/guide.pdf` → output `kb/01_regulatory/singapore_customs/guide.md`)
3. Script must:
   - Extract text with `pymupdf4llm.to_markdown()`
   - Add template frontmatter (with `TO_BE_FILLED` placeholders for Claude Code to complete during scraping)
   - Clean up extraction artifacts (repeated headers/footers, excessive blank lines, page numbers mid-text)
   - Log quality metrics per file: pages, characters, sections detected, tables detected
   - Flag quality: **HIGH** (>1000 chars, sections found) / **MEDIUM** (>500 chars, no sections) / **LOW** (<500 chars, possible image PDF)
   - In batch mode, output a summary CSV: `pdf_extraction_summary.csv`
4. Write tests in `tests/test_pdf_extractor.py`

**Acceptance Criteria**:
- [ ] Script processes single PDF to markdown
- [ ] Script processes batch of PDFs
- [ ] Frontmatter template added to each output
- [ ] Quality flags generated (HIGH/MEDIUM/LOW)
- [ ] Tests pass
- [ ] `pymupdf4llm` added to `requirements.txt`

**Estimated Time**: 1–1.5 hours

---

## PHASE 3: KNOWLEDGE BASE REBUILD

### Task 6: Execute Scraping with Improved Strategy

**Purpose**: Rebuild the knowledge base from scratch using the revised document list (Task 3), applying retrieval-first content guidelines and PDF discovery.

**Execution mode**: Claude Code scrapes autonomously. Rishi spot-checks 3–5 documents at the review point.

**Inputs**:
- `04_retrieval_optimization/REVISED_DOCUMENT_LIST.md` (approved by Rishi)
- Retrieval-first content guidelines (documented in Task 3)
- Updated scraper rules (documented in Task 3)
- Updated frontmatter template (documented in Task 3)

**Per-document workflow**:
1. Navigate to the source URL
2. Scrape the page content
3. **Scan the page for downloadable PDFs/documents** — look for links to guides, manuals, circulars, tariff schedules (link text containing "Download", "Guide", "Manual", "Circular", "Handbook", or `.pdf` extension)
4. Download relevant PDFs to the category's `pdfs/` folder
5. Run `pdf_extractor.py` on any downloaded PDFs
6. Create/write the markdown document following retrieval-first guidelines:
   - Key Facts summary in the first 600 characters
   - Customer-language section headers
   - Self-contained paragraphs for critical facts
   - Synonym/alias mentions
   - Complete frontmatter with all fields filled (no `TO_BE_FILLED` placeholders)
   - Cross-references to related documents
7. **Auto-review**: Read the document back and check:
   - Key Facts summary present and contains most important retrievable content?
   - Section headers phrased as customers would ask?
   - Critical facts in self-contained paragraphs (not only in tables)?
   - Frontmatter complete?
   - Content would plausibly answer the document's assigned target queries?
   - Flag any issues to `reports/scraping_issues_log.md`

**Document count**: Starts with the revised list (~29+ documents). If PDFs discovered during scraping contain valuable new content, they may be added as additional documents. No hard cap.

**Sub-task execution order** (follows the revised document list):
```
6a: Singapore Customs documents (re-scrape with PDF discovery)
6b: ASEAN Trade documents (re-scrape with PDF discovery)
6c: Country-specific documents (re-scrape with PDF discovery)
6d: Ocean carrier documents (re-scrape with PDF discovery)
6e: Air carrier documents (re-scrape with PDF discovery)
6f: Reference documents (restructure with retrieval-first guidelines)
6g: Synthetic internal documents (restructure existing + create 1–2 new)
```

After each sub-task, report: documents created (count), PDFs downloaded (count), issues flagged (count), estimated coverage of target queries.

**Acceptance Criteria**:
- [ ] All documents from the revised list created in `04_retrieval_optimization/kb/`
- [ ] Every document follows retrieval-first guidelines
- [ ] PDFs downloaded where found and extracted
- [ ] Frontmatter complete on every document — no `TO_BE_FILLED` placeholders
- [ ] 1–2 new synthetic documents created where content gaps identified
- [ ] Auto-review issues logged
- [ ] Sub-task reports generated

**Estimated Time**: 4–6 hours (largest task — Claude Code does the heavy lifting, Rishi spot-checks)

---

### Task 7: Initial Ingestion and Retrieval Validation

**Purpose**: Ingest the new KB into ChromaDB and run the retrieval quality test to measure improvement. Uses current chunking/retrieval params for clean baseline comparison.

**Retrieval test parameters** (same as Week 2 for clean comparison):
- `top_k = 5`
- `threshold = 0.15`
- Chunking: `CHUNK_SIZE = 600`, `CHUNK_OVERLAP = 90`

**Scoring**: Reclassified queries (#36, #38, #44) pass if the system would appropriately decline them. All other queries scored as before.

**Sequence**:
1. Run `ingest.py` to process all documents in the new `kb/` into `chroma_db/`
2. Verify ingestion: document count, chunk count, chunk distribution by category
3. Run `retrieval_quality_test.py` with all 50 queries against the new vector store
4. Compare results to the Week 2 baseline:
   - Overall (raw): 76% → ?
   - Overall (adjusted): 82% → ?
   - Booking: 60%, Customs: 80%, Carrier: 100%, SLA: 50%, Edge Cases: 90%
5. Identify any new failures introduced and any old failures now fixed
6. Produce a validation report

**Output**: `04_retrieval_optimization/reports/03_retrieval_validation.md`

**Output format**:
```
## Retrieval Validation — Round 1 (Baseline Params)

### Parameters
- Chunking: 600 chars / 90 overlap
- Retrieval: top_k=5, threshold=0.15

### Summary
| Category | Old Hit Rate | New Hit Rate (raw) | New Hit Rate (adjusted) | Delta |
|----------|-------------|-------------------|------------------------|-------|

### Newly Fixed Queries
[List queries that now pass]

### New Regressions
[List queries that now fail — investigate each]

### Remaining Failures
[List queries still failing — next steps per query]
```

**Acceptance Criteria**:
- [ ] All documents ingested successfully
- [ ] Retrieval quality test runs against new vector store
- [ ] Results compared to both raw (76%) and adjusted (82%) baselines
- [ ] Minimum target: ≥80% adjusted (must not regress below adjusted baseline)
- [ ] No unexplained regressions
- [ ] Report saved

**Estimated Time**: 1 hour

---

**⏸ REVIEW POINT 2**: Rishi reviews retrieval results. Decides:
- If adjusted hit rate ≥80%: proceed to Phase 4
- If <80%: identify specific fixes and loop back to adjust documents before proceeding
- Whether to proceed with chunking/retrieval param experiments in Task 8

---

## PHASE 4: INGESTION REFINEMENT & FINAL VALIDATION

### Task 8: Fix Remaining Failures + Parameter Experiments

**Purpose**: Address remaining retrieval failures through two tracks: (1) content-level fixes, (2) chunking and retrieval parameter experiments.

**Track A: Content Fixes**

For each remaining failure, apply the quickest effective fix:
- **Missing content**: Add a paragraph or section to the relevant document
- **Bad chunk boundary**: Adjust section structure so the answer lands in a clean chunk
- **Terminology**: Add synonyms to the relevant section

**Track B: Parameter Experiments** (after content fixes)

Test different chunking and retrieval configurations against the improved KB:

1. **Baseline** (already measured in Task 7): CHUNK_SIZE=600, CHUNK_OVERLAP=90, top_k=5
2. **Experiment A**: CHUNK_SIZE=800, CHUNK_OVERLAP=120, top_k=5
3. **Experiment B**: CHUNK_SIZE=1000, CHUNK_OVERLAP=150, top_k=5
4. **Experiment C**: Best chunk config from above + top_k=10
5. Additional experiments as results suggest

For each experiment:
- Update `.env` with new params
- Re-run `ingest.py` (full re-ingest)
- Re-run `retrieval_quality_test.py`
- Record results in validation report

**Stop condition**: Keep iterating until 90% adjusted hit rate achieved OR Sunday evening buffer exhausted. No hard round limit.

**Output**: Updated `04_retrieval_optimization/reports/03_retrieval_validation.md` with round-by-round results appended, including parameter experiment results.

**Acceptance Criteria**:
- [ ] Each remaining failure investigated
- [ ] Content fixes applied where achievable
- [ ] At least 2–3 chunking/retrieval parameter experiments run
- [ ] Best configuration identified and documented
- [ ] Re-tests confirm fixes and best params
- [ ] Remaining unfixable failures documented with explanation

**Estimated Time**: 2–4 hours (flexible, uses Sunday buffer if needed)

---

### Task 9: Update RAG Pipeline to Use New KB

**Purpose**: Point the working RAG pipeline (`03_rag_pipeline/`) at the new ChromaDB so the full end-to-end system uses the improved knowledge base.

**Sequence**:
1. Stop any running server in `03_rag_pipeline/`
2. Backup existing ChromaDB: rename `03_rag_pipeline/` vector store to `_backup`
3. Copy final `chroma_db/` from `04_retrieval_optimization/` to the location `03_rag_pipeline/` expects (check its retrieval service config)
4. If chunking/retrieval params changed from experiments, update `03_rag_pipeline/` config accordingly
5. Start server: `cd 03_rag_pipeline && npm run dev`
6. Manual smoke test: submit a test query via curl or browser
7. Run the E2E test suite to confirm no regressions

**Acceptance Criteria**:
- [ ] RAG pipeline serves responses from the new KB
- [ ] Health check passes
- [ ] Manual test query returns correct, cited response
- [ ] E2E test suite passes (30/30 or documented regressions)
- [ ] Any param changes from experiments propagated to RAG pipeline config

**Estimated Time**: 30–45 min

---

### Task 10: Final Comparison Report (Week 3 Retrospective)

**Purpose**: Comprehensive Week 3 retrospective — side-by-side comparison of Week 2 vs. optimised retrieval, plus decisions, experiments, time spent, and lessons learned.

**Sequence**:
1. Run the full retrieval quality test one final time
2. Run the E2E test suite one final time
3. Compile results into a full retrospective report

**Output**: `04_retrieval_optimization/reports/04_final_comparison.md`

**Sections**:
1. **Executive Summary** — one paragraph, key numbers, whether targets met
2. **Retrieval Quality Comparison** — old vs. new hit rate per category (raw and adjusted), delta
3. **Knowledge Base Changes** — document count, chunk count, PDFs added, new docs created, docs restructured
4. **Query-Level Detail** — queries fixed, queries reclassified, queries still failing with explanations
5. **Parameter Experiments** — chunking configs tested, retrieval params tested, results table, best config selected
6. **E2E Test Results** — pass rate, regressions, latency changes
7. **Time Spent** — actual hours per phase vs. estimated
8. **Decisions Made** — summary of all pre-execution and mid-execution decisions
9. **Lessons Learned** — what worked, what didn't, what to do differently
10. **Recommendations for Week 4** — outstanding issues, suggested focus areas for evaluation, param tuning still needed

**Acceptance Criteria**:
- [ ] Report covers all 10 sections
- [ ] Numbers are from actual test runs, not estimates
- [ ] Clear before/after comparison (raw and adjusted)
- [ ] Parameter experiment results documented
- [ ] Time tracking included
- [ ] Actionable recommendations for Week 4
- [ ] Report saved

**Estimated Time**: 1–1.5 hours

---

**⏸ REVIEW POINT 3**: Rishi reviews final results. Week 3 complete.

---

## Time Budget

| Phase | Tasks | Estimated | Day |
|---|---|---|---|
| **Phase 1: Audit** | Task 1, 2, 3 | 3–4 hours | Thu eve – Fri morning |
| *Review point 1* | Rishi reviews | 30 min | Fri |
| **Phase 2: Infrastructure** | Task 4, 5 | 1.5–2 hours | Fri |
| **Phase 3: KB Rebuild** | Task 6, 7 | 5–7 hours | Fri eve – Sat |
| *Review point 2* | Rishi reviews | 30 min | Sat |
| **Phase 4: Refinement** | Task 8, 9, 10 | 3.5–6 hours | Sun |
| *Review point 3* | Rishi reviews | 30 min | Sun |
| **Total** | | **~15–21 hours** | |

**Buffer**: Sunday evening is buffer for Task 8 iterations (push for 90% stretch goal).
