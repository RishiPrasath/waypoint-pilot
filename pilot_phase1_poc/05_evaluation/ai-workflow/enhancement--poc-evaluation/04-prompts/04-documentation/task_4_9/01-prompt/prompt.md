# Task 4.9 Prompt — Phase 2 Recommendations

## Persona
Technical lead writing a concise 1-page recommendation list to guide Phase 2 scoping (Decision #14).

## Context
- **Initiative**: enhancement--poc-evaluation
- **Task**: 4.9 — Phase 2 recommendations
- **Phase**: 4 (Documentation) — FINAL TASK in Phase 4
- **Dependencies**: T4.8 (Lessons learned) — complete
- **Blocks**: None
- **Workspace**: `pilot_phase1_poc/05_evaluation/`

### POC Results Driving Recommendations
- All 6 evaluation targets met (87.2% deflection, 96.0% citation, 2.0% hallucination, 100% OOS, 1,182ms latency, stable)
- 30-document KB with 94% retrieval hit rate — quality is high but scope is narrow
- Confidence distribution skewed: 86% Low, 14% Medium, 0% High
- LLM nondeterminism causes citation variability between runs
- No live system integration, no multi-turn, no authentication
- Singapore-centric; ASEAN coverage is shallow

### Gaps Identified During Evaluation
From `reports/lessons_learned.md` and `documentation/guides/known_limitations.md`:

**Feature gaps:**
1. No live system integration (TMS/WMS, tracking, rates, bookings)
2. No multi-turn conversation (no session memory)
3. No authentication or access control
4. No rate limiting or usage monitoring
5. Single LLM provider (Groq) with no failover

**KB gaps:**
6. No container specifications (weight limits, dimensions)
7. No port-specific transit times or route tables
8. Shallow ASEAN coverage (MY, ID, TH, VN, PH)
9. No dynamic content ingestion or scheduled updates
10. 30 documents — limited carrier and internal procedure coverage

**Technical gaps:**
11. Confidence scoring poorly calibrated (86% Low)
12. Citation matching relies on LLM format compliance
13. No semantic evaluation (keyword-only harness)
14. No logging, monitoring, or analytics in production

### Prioritization Framework
Recommendations should be ordered by:
- **Impact**: How much value does this add for end users (CS agents)?
- **Feasibility**: How much effort relative to POC baseline?
- **Risk**: What breaks if this isn't addressed?

## Task

Create **1 Phase 2 recommendations document** at `reports/phase2_recommendations.md`.

**Requirements:**
- **Maximum 1 page** (~80-120 lines) — concise bullet list, not prose
- Organized into 4 categories: Features, Knowledge Base, Infrastructure, Model & Pipeline
- Each recommendation: one-line description + brief rationale (why it matters, based on POC findings)
- Prioritized within each category (highest impact first)
- Include a priority summary table at the top (P1 = must-have, P2 = should-have, P3 = nice-to-have)
- Reference specific POC data points where relevant (e.g., "confidence calibration — currently 86% Low")
- No detailed scoping or timelines — just direction

## Validation
- [ ] Recommendations cover features, infrastructure, KB, and model
- [ ] Prioritized by impact
- [ ] Concise (1 page or less)
- [ ] Based on actual POC findings (not generic)
- [ ] Actionable items

## Output

Create output report: `04-prompts/04-documentation/task_4_9/02-output/TASK_4.9_OUTPUT.md`

## Update on Completion

**MANDATORY — Update ALL 7 tracking locations:**
1. **Checklist**: `03-checklist/IMPLEMENTATION_CHECKLIST.md` — mark T4.9 `[x]`, update Phase 4 progress (9/9, 100%), Total (37/45, 82%)
2. **Roadmap Progress Tracker**: Phase 4 → `9`, Status → `✅ Complete`, Total → `37 | 82%`
3. **Roadmap Quick Reference**: T4.9 → `✅ Complete`
4. **Roadmap Detailed Entry**: T4.9 Status → `✅ Complete`, validation checkboxes `[x]`
5. **Bootstrap file**: `ai-workflow-bootstrap-prompt-v3.md` → `37/45 -- 82%`
6. **CLAUDE.md** (root): → `37/45 — 82%`
7. **AGENTS.md** (root): → `37/45 -- 82%`
