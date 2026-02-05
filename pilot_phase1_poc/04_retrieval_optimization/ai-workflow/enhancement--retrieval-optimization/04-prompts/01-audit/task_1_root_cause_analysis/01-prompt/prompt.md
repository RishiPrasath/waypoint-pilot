# Task 1: Root Cause Analysis of Retrieval Failures

---

## Persona

**Role**: Senior RAG Pipeline Engineer

**Expertise**:
- Vector database retrieval and similarity search
- Document chunking strategies and their impact on retrieval
- Semantic search debugging and optimization
- Knowledge base content analysis

---

## Context

### Background
Week 2 of the Waypoint POC achieved a 76% raw retrieval hit rate (82% adjusted after reclassifying 3 out-of-scope queries). Nine queries continue to fail retrieval. Before rebuilding the knowledge base, we need to understand exactly WHY each query fails to retrieve relevant content.

### Current State
- **Baseline**: 38/50 queries pass (76% raw), 41/50 adjusted (82%)
- **Failing queries**: 9 queries (#2, #5, #6, #7, #15, #19, #31, #32, #37)
- **Reclassified as out-of-scope**: #36, #38, #44 (excluded from this analysis)
- **KB location**: `pilot_phase1_poc/01_knowledge_base/kb/` (29 documents)
- **ChromaDB**: `pilot_phase1_poc/02_ingestion_pipeline/chroma_db/`

### References
| Document | Path | Purpose |
|----------|------|---------|
| Retrieval Quality Report | `03_rag_pipeline/reports/retrieval_quality_REPORT.md` | Baseline results with scores |
| Knowledge Base | `01_knowledge_base/kb/` | Raw markdown documents |
| Scope Definition | `00_docs/01_scope_definition.md` | What queries should be answerable |
| Use Cases | `00_docs/02_use_cases.md` | Test query bank and expected sources |

### Dependencies
- **Completed**: Week 2 RAG pipeline, retrieval quality test
- **Blocks**: Task 3 (Revised Document List)

---

## Task

### Objective
For each of the 9 failing queries, determine the root cause of retrieval failure and propose a specific fix.

### The 9 Failing Queries

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

### Requirements

For each query, perform the following analysis:

1. **Search raw markdown files** in `01_knowledge_base/kb/`:
   - Use text search (grep/find) for key terms and synonyms
   - Check semantic variations (e.g., "LCL" = "Less than Container Load")
   - Record whether the information exists and in which file/section

2. **Search ChromaDB chunks**:
   - Query the vector store with the exact query text
   - Examine the top-5 returned chunks
   - Record what was returned and relevance scores
   - Assess why the correct information wasn't retrieved (if it exists)

3. **Classify the root cause** into one of three categories:
   - **(a) Content missing**: The answer doesn't exist in any document
   - **(b) Content buried**: The answer exists but the chunk is too generic, too short, or split awkwardly
   - **(c) Terminology mismatch**: The answer exists and chunks well, but uses different words

4. **Propose a specific fix**:
   - For (a): Which document should contain this? What section to add?
   - For (b): How should the document be restructured?
   - For (c): What synonyms/aliases need to be added?

### Constraints
- Do NOT modify any files during this task - analysis only
- Focus on the 9 queries listed; ignore reclassified queries (#36, #38, #44)
- Be specific in fix proposals (document name, section, exact content needed)

### Acceptance Criteria
- [ ] All 9 failing queries analyzed
- [ ] Each query has raw document search results documented
- [ ] Each query has ChromaDB search results documented
- [ ] Each query has a root cause classification (a/b/c)
- [ ] Each query has a specific, actionable proposed fix
- [ ] Report saved to `04_retrieval_optimization/reports/01_audit_report.md`

---

## Format

### Output Structure
```
04_retrieval_optimization/
└── reports/
    └── 01_audit_report.md
```

### Report Format

```markdown
# Audit Report: Root Cause Analysis of Retrieval Failures

**Date**: YYYY-MM-DD
**Analyst**: Claude Code
**Queries Analyzed**: 9

## Executive Summary
[2-3 sentences summarizing findings - how many (a), (b), (c)]

## Analysis by Query

### Query #2: "How far in advance should I book an LCL shipment?"
- **Category**: Booking
- **Expected source**: [document that should answer this]
- **Raw doc search**: FOUND in [file X, section Y] / NOT FOUND
  - Search terms used: [list]
  - Results: [details]
- **Chunk search**:
  - Top chunk: [text snippet, score]
  - Why wrong: [explanation]
- **Root cause**: (a) missing / (b) buried / (c) terminology
- **Proposed fix**: [specific action - document, section, content]

[Repeat for all 9 queries]

## Summary Table

| Query # | Root Cause | Fix Type | Target Document |
|---------|------------|----------|-----------------|
| 2 | (a/b/c) | [action] | [doc] |
| ... | | | |

## Recommendations for Task 3
[Prioritized list of documents to modify/create]
```

### Validation Commands
```bash
# Verify report exists
dir pilot_phase1_poc\04_retrieval_optimization\reports\01_audit_report.md

# Grep for query mentions (should find all 9)
grep -c "Query #" pilot_phase1_poc/04_retrieval_optimization/reports/01_audit_report.md
```

---

## Notes
- Take time to thoroughly search raw documents - missing content is different from buried content
- When searching ChromaDB, note the relevance scores - low scores may indicate terminology issues
- The proposed fixes should be concrete enough to execute in Task 6
- This report feeds directly into Task 3 (Revised Document List)
