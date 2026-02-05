# Task 2: Scope Reclassification of All 50 Test Queries

---

## Persona

**Role**: Quality Assurance Analyst / Scope Validator

**Expertise**:
- Freight forwarding domain knowledge
- Requirements analysis and scope management
- Test case categorization and validation
- Regulatory compliance understanding

---

## Context

### Background
The Week 2 retrieval test used 50 queries across 5 categories. Three queries (#36, #38, #44) have been pre-confirmed as out-of-scope. Before rebuilding the KB, we need to validate that all 50 queries are correctly categorized against the official scope definition.

### Pre-Confirmed Reclassifications
| Query # | Query Text | New Category | Reason |
|---------|------------|--------------|--------|
| 36 | What's the process for refused deliveries? | Out-of-scope | No use case mapping |
| 38 | How do I upgrade to express service? | Out-of-scope | No use case mapping |
| 44 | I want to file a claim for damaged cargo | Out-of-scope | Claims processing excluded per scope |

### Current State
- **Total queries**: 50
- **Week 2 result**: 38/50 pass (76% raw)
- **After reclassification**: 41/50 pass (82% adjusted)
- **Goal**: Ensure every query is correctly mapped to scope

### References
| Document | Path | Purpose |
|----------|------|---------|
| Scope Definition | `00_docs/01_scope_definition.md` | Official in/out scope boundaries |
| Use Cases | `00_docs/02_use_cases.md` | Test query bank and use case catalog |
| Task 1 Report | `04_retrieval_optimization/reports/01_audit_report.md` | 9 failing queries analysis |

### Dependencies
- **Completed**: Task 1 (Root Cause Analysis)
- **Blocks**: Task 3 (Revised Document List)

---

## Task

### Objective
Map all 50 test queries to their corresponding use cases and priority levels. Apply pre-confirmed reclassifications and identify any additional mismatches for review.

### Scope Rules (from 01_scope_definition.md)

**In Scope - Primary (P1)**:
| Category | Description |
|----------|-------------|
| Shipment Booking | Booking procedures, documentation requirements, lead times |
| Customs & Documentation | HS codes, duties, import/export requirements, certificates |
| Carrier Selection Guidance | Carrier capabilities, transit times, service comparisons |

**In Scope - Secondary (P2/P3)**:
| Category | Priority | Description |
|----------|----------|-------------|
| COD Procedures | P2 | Cash-on-delivery workflows |
| SLA Inquiries | P2 | Service level terms |
| Service Scope Clarification | P3 | What's included/excluded |

**Out of Scope**:
- Live TMS/WMS integration
- Real-time tracking queries
- Actual booking execution
- Rate quotations
- **Claims processing** ← Query #44
- Hazmat/DG shipments
- Multi-country regulatory comparison

### Requirements

1. **Read the 50 test queries** from `00_docs/02_use_cases.md` (Test Query Bank section)

2. **For each query, determine**:
   - Which use case it maps to (UC-X.X) or "None"
   - Priority level: P1 / P2 / P3 / Out-of-scope
   - Current category in test bank
   - Whether current categorization is correct

3. **Apply pre-confirmed reclassifications**:
   - Query #36 → Out-of-scope
   - Query #38 → Out-of-scope
   - Query #44 → Out-of-scope

4. **Flag additional candidates** for Rishi's review if:
   - Query doesn't map to any use case
   - Query is ambiguously in/out of scope
   - Query category seems misaligned

5. **Do NOT modify** the original query bank (`02_use_cases.md`)
   - Reclassifications are tracked only in the report
   - Scoring logic will use this report

### Constraints
- Analysis only - do not modify `02_use_cases.md`
- Be conservative - only flag clear mismatches
- Document reasoning for any new reclassification candidates

### Acceptance Criteria
- [ ] All 50 queries reviewed
- [ ] Each query mapped to a use case or marked "None"
- [ ] Each query assigned a priority (P1/P2/P3/Out-of-scope)
- [ ] Pre-confirmed reclassifications (#36, #38, #44) applied
- [ ] Any additional mismatches flagged with justification
- [ ] Report saved to `04_retrieval_optimization/reports/02_scope_reclassification.md`

---

## Format

### Output Structure
```
04_retrieval_optimization/
└── reports/
    └── 02_scope_reclassification.md
```

### Report Format

```markdown
# Scope Reclassification Report

**Date**: YYYY-MM-DD
**Analyst**: Claude Code
**Total Queries**: 50

## Executive Summary
[1-2 sentences: X queries in-scope, Y out-of-scope, Z flagged for review]

## Pre-Confirmed Reclassifications

| Query # | Query | Old Category | New Category | Reason |
|---------|-------|--------------|--------------|--------|
| 36 | ... | SLA | Out-of-scope | No use case mapping |
| 38 | ... | SLA | Out-of-scope | No use case mapping |
| 44 | ... | Edge Cases | Out-of-scope | Claims processing excluded |

## Full Query Mapping

| # | Query | Current Category | Mapped UC | Priority | Correct? | Notes |
|---|-------|------------------|-----------|----------|----------|-------|
| 1 | What documents... | Booking | UC-1.1 | P1 | ✅ | |
| 2 | How far in advance... | Booking | UC-1.2 | P1 | ✅ | |
...

## Additional Reclassification Candidates

[List any queries flagged for Rishi's review with justification]

### Query #[N]: "[text]"
- **Current**: [category]
- **Issue**: [why it might be out-of-scope]
- **Recommendation**: [keep / reclassify]
- **Awaiting**: Rishi's decision

## Summary Statistics

| Category | P1 | P2 | P3 | Out-of-scope | Total |
|----------|----|----|----|----|-------|
| Booking | X | | | | X |
| Customs | X | | | | X |
| Carrier | X | | | | X |
| SLA | | X | X | X | X |
| Edge Cases | | | | X | X |
| **Total** | X | X | X | X | 50 |

## Impact on Metrics

| Metric | Before | After |
|--------|--------|-------|
| In-scope queries | 50 | [new count] |
| Out-of-scope queries | 0 | [new count] |
| Adjusted baseline | 76% | [new %] |
```

### Validation Commands
```bash
# Verify report exists
dir pilot_phase1_poc\04_retrieval_optimization\reports\02_scope_reclassification.md

# Count query rows (should be 50)
grep -c "^| [0-9]" pilot_phase1_poc/04_retrieval_optimization/reports/02_scope_reclassification.md
```

---

## Notes
- The 3 pre-confirmed reclassifications are already decided - just document them
- Focus on clear scope violations, not borderline cases
- If a query is answerable with KB content, it's likely in-scope
- The 9 failing queries from Task 1 were verified as IN SCOPE (6 P1, 3 P2/P3)
- This report will be used to adjust retrieval scoring in later tasks
