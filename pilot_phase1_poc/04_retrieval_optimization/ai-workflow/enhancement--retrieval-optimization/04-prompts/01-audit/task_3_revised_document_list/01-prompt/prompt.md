# Task 3: Define Revised Document List

---

## Persona

**Role**: Knowledge Base Architect / Content Strategist

**Expertise**:
- Document management and information architecture
- Retrieval-optimized content design
- Freight forwarding domain knowledge
- RAG system content preparation

---

## Context

### Background
Tasks 1 and 2 have identified specific issues with the current knowledge base:
- **Task 1**: 9 failing queries with root causes (5 missing content, 3 buried content, 1 terminology mismatch)
- **Task 2**: 38 in-scope queries mapped to use cases; 3 reclassified as out-of-scope

This task produces the definitive document list for rebuilding the KB in Phase 3.

### Current State
- **Current KB**: 29 documents across 4 categories
- **Week 2 result**: 76% raw → 82% adjusted after reclassification
- **Goal**: ≥80% minimum, 90% stretch

### Task 1 Findings (Root Cause Analysis)

| Query # | Issue | Root Cause | Target Document | Required Fix |
|---------|-------|------------|-----------------|--------------|
| 2 | LCL booking advance time | (a) Missing | booking_procedure.md | Add recommended lead times section |
| 5 | Commercial invoice for samples | (a) Missing | booking_procedure.md | Add samples/zero-value guidance |
| 6 | Bill of Lading definition | (b) Buried | booking_procedure.md | Add B/L definition paragraph |
| 7 | Ship without packing list | (b) Buried | booking_procedure.md | Add mandatory documents statement |
| 15 | ATIGA duty rate | (c) Terminology | atiga_overview.md | Add "duty rate" terminology |
| 19 | Customs ruling application | (a) Missing | sg_hs_classification.md | Expand ruling application process |
| 31 | Delivery SLA Singapore | (a) Missing | sla_policy.md | Add delivery SLA section |
| 32 | Customs in door-to-door | (a) Missing | service_terms_conditions.md | Add door-to-door inclusions |
| 37 | Handle import permits | (b) Buried | service_terms_conditions.md | Add import permit statement |

### Task 2 Findings (Scope Reclassification)

**In-Scope Distribution**:
| Priority | Count | Key Use Cases |
|----------|-------|---------------|
| P1 | 24 | UC-1.1 (5), UC-1.2 (4), UC-2.x (7), UC-3.1 (7) |
| P2 | 10 | UC-2.4 (3), UC-3.2 (3), UC-3.3 (1), UC-4.1 (4) |
| P3 | 4 | UC-4.2 (4) |

**Out-of-Scope**: 12 queries (10 Edge Cases + #36, #38 reclassified)

### References
| Document | Path | Purpose |
|----------|------|---------|
| KB Blueprint | `00_docs/03_knowledge_base_blueprint.md` | Original document plan |
| Task 1 Report | `04_retrieval_optimization/reports/01_audit_report.md` | Fixes needed |
| Task 2 Report | `04_retrieval_optimization/reports/02_scope_reclassification.md` | Query mapping |
| Current KB | `01_knowledge_base/kb/` | Existing 29 documents |

### Dependencies
- **Completed**: Task 1 (Root Cause Analysis), Task 2 (Scope Reclassification)
- **Blocks**: Task 6 (Scraping Execution)

---

## Task

### Objective
Produce a comprehensive, actionable document list that:
1. Addresses all 9 failing queries identified in Task 1
2. Ensures coverage for all P1 and P2 use cases from Task 2
3. Specifies exact actions per document (no ambiguity)
4. Includes retrieval-first guidelines for content creation

### Requirements

1. **Audit Existing 29 Documents**
   - List all current documents with their categories
   - Map each document to use cases it supports
   - Identify documents requiring updates vs. carry forward

2. **Apply Task 1 Fixes**
   - For each of the 9 fixes, specify:
     - Target document (existing or new)
     - Exact content to add/modify
     - Section placement

3. **Apply Task 2 Insights**
   - Verify every P1 use case has document coverage
   - Verify every P2 use case has document coverage
   - Note P3 use cases with coverage gaps (lower priority)

4. **Identify New Documents**
   - Propose 1-2 new synthetic documents if needed
   - Justify each new document with specific gaps it fills
   - Consider: FAQ document for common customer questions

5. **Assign Actions Per Document**
   Use these action codes:
   | Action | Description |
   |--------|-------------|
   | **CARRY FORWARD** | No changes needed, copy as-is |
   | **RESTRUCTURE** | Same content, improved for retrieval |
   | **ENRICH** | Add specific content sections |
   | **RE-SCRAPE** | Source URL changed, fetch fresh |
   | **CREATE** | New document needed |

6. **Define Retrieval-First Guidelines**
   - Frontloading key terms
   - Self-contained sections
   - Explicit answers to common questions
   - Synonym inclusion

7. **Define Frontmatter Template**
   - Required metadata fields
   - Use case tagging format
   - Priority indicators

### Constraints
- Maximum 35 documents total (KB size constraint)
- Prioritize fixing P1 issues over adding new P2/P3 content
- All document actions must be specific and executable
- Do not modify original KB files - this is a planning document only

### Acceptance Criteria
- [ ] All 29 current documents listed with status
- [ ] All 9 Task 1 fixes mapped to specific documents
- [ ] All P1 use cases have document coverage
- [ ] All P2 use cases have document coverage
- [ ] 1-2 new documents proposed (if needed) with justification
- [ ] Every document has a specific action code
- [ ] Retrieval-first guidelines documented
- [ ] Frontmatter template defined
- [ ] Saved to `04_retrieval_optimization/REVISED_DOCUMENT_LIST.md`

---

## Format

### Output Structure
```
04_retrieval_optimization/
└── REVISED_DOCUMENT_LIST.md
```

### Report Format

```markdown
# Revised Document List

**Date**: YYYY-MM-DD
**Author**: Claude Code
**Total Documents**: [count]

## Executive Summary
[2-3 sentences: document count, key changes, expected impact]

## Current KB Inventory

### 01_regulatory/ (X documents)
| # | File | Use Cases | Action | Notes |
|---|------|-----------|--------|-------|
| 1 | sg_export_procedures.md | UC-1.1 | CARRY FORWARD | |
| 2 | ... | | | |

### 02_carriers/ (X documents)
...

### 03_reference/ (X documents)
...

### 04_internal_synthetic/ (X documents)
...

## Task 1 Fixes Applied

### Fix 1: Query #2 - LCL Booking Lead Time
- **Target**: booking_procedure.md
- **Action**: ENRICH
- **Content to Add**:
  ```markdown
  ## Recommended Booking Lead Times
  ...
  ```
- **Section Placement**: After Section 3 (Booking Request)

[Repeat for all 9 fixes]

## Use Case Coverage Matrix

| Use Case | Priority | Primary Document | Backup Document | Status |
|----------|----------|------------------|-----------------|--------|
| UC-1.1 | P1 | booking_procedure.md | sg_export_procedures.md | ✅ Covered |
| UC-1.2 | P1 | booking_procedure.md | carrier_summaries | ✅ Covered |
| ... | | | | |

## New Documents

### [Document Name]
- **Type**: Synthetic Internal
- **Purpose**: [gap it fills]
- **Use Cases**: UC-X.X, UC-Y.Y
- **Justification**: [why needed]
- **Priority**: P1/P2

## Document Action Summary

| Action | Count | Documents |
|--------|-------|-----------|
| CARRY FORWARD | X | [list] |
| RESTRUCTURE | X | [list] |
| ENRICH | X | [list] |
| RE-SCRAPE | X | [list] |
| CREATE | X | [list] |

## Retrieval-First Guidelines

### 1. Frontload Key Terms
...

### 2. Self-Contained Sections
...

### 3. Explicit Q&A Format
...

### 4. Synonym Inclusion
...

## Updated Frontmatter Template

```yaml
---
title: [Document Title]
source_org: [Organization name]
source_urls:
  - [Primary URL]
source_type: [public_regulatory | public_carrier | synthetic_internal]
last_updated: YYYY-MM-DD
jurisdiction: [SG | MY | ID | TH | VN | PH | ASEAN | Global]
category: [customs | carrier | policy | procedure | reference]
use_cases: [UC-1.1, UC-2.3]
priority: [P1 | P2 | P3]
retrieval_keywords: [term1, term2, term3]
---
```

## Implementation Notes

[Any special instructions for Phase 3 execution]
```

### Validation Commands
```bash
# Verify report exists
dir pilot_phase1_poc\04_retrieval_optimization\REVISED_DOCUMENT_LIST.md

# Count documents listed
grep -c "| [0-9]" pilot_phase1_poc/04_retrieval_optimization/REVISED_DOCUMENT_LIST.md
```

---

## Notes

- Focus on actionability - every item should be executable in Task 6
- The existing 29 documents are a solid foundation; minimize unnecessary changes
- Task 1 found that `booking_procedure.md` needs the most updates (4 fixes)
- Consider creating an FAQ document to consolidate common customer questions
- Retrieval-first guidelines should be practical, not theoretical
