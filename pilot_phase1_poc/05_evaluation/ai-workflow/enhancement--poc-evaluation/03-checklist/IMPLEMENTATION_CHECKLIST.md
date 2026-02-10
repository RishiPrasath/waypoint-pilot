# Implementation Checklist

**Initiative:** enhancement--poc-evaluation
**Last Updated:** 2026-02-09

## Quick Links

- Plan: [DETAILED_PLAN.md](../01-plan/DETAILED_PLAN.md)
- Roadmap: [IMPLEMENTATION_ROADMAP.md](../02-roadmap/IMPLEMENTATION_ROADMAP.md)

---

## Phase 0: Setup

| Status | Task | Description | Roadmap Ref |
|:------:|------|-------------|-------------|
| [x] | Task 0.1 | Create 05_evaluation/ folder structure | Phase 0 |
| [x] | Task 0.2 | Copy codebase from 04_retrieval_optimization/ | Phase 0 |
| [x] | Task 0.3 | Setup environment (npm install, venv) | Phase 0 |
| [x] | Task 0.4 | Fix ingestion pipeline metadata (source_urls, retrieval_keywords, use_cases) | Phase 0 |
| [x] | Task 0.5 | Run fresh ingestion (--clear) | Phase 0 |
| [x] | Task 0.6 | Run ALL existing tests (pytest + Jest + retrieval 92%) | Phase 0 |

## Phase 1: UX Redesign

| Status | Task | Description | Roadmap Ref |
|:------:|------|-------------|-------------|
| [x] | Task 1.1 | Update system prompt for structured formatting | Phase 1 |
| [x] | Task 1.2 | Update backend pipeline (sources, relatedDocs, confidence) | Phase 1 |
| [x] | Task 1.3 | Implement new React frontend (TDD per section) | Phase 1 |
| [x] | Task 1.4 | Add Layer 1 inline documentation (JSDoc/docstrings) | Phase 1 |

## Phase 2: Systematic Testing

| Status | Task | Description | Roadmap Ref |
|:------:|------|-------------|-------------|
| [x] | Task 2.1 | Re-run existing ingestion tests (87 tests) | Phase 2 |
| [x] | Task 2.2 | Add new metadata preservation tests | Phase 2 |
| [x] | Task 2.3 | Re-run 50-query retrieval hit rate test | Phase 2 |
| [x] | Task 2.4 | Add generation unit tests | Phase 2 |
| [x] | Task 2.5 | Update citation service tests | Phase 2 |
| [x] | Task 2.6 | Update existing backend tests | Phase 2 |
| [x] | Task 2.7 | Add new endpoint tests | Phase 2 |
| [x] | Task 2.8 | Add error/edge case tests | Phase 2 |
| [x] | Task 2.9 | Component unit tests (from Phase 1 TDD) | Phase 2 |
| [x] | Task 2.10 | Visual verification via Chrome DevTools MCP | Phase 2 |
| [x] | Task 2.11 | Define expected-answer baselines (50 queries) | Phase 2 |
| [x] | Task 2.12 | Build automated evaluation harness | Phase 2 |
| [x] | Task 2.13 | Execute Round 2 and generate reports | Phase 2 |

## Phase 3: Fix-and-Retest Loop

| Status | Task | Description | Roadmap Ref |
|:------:|------|-------------|-------------|
| [x] | Task 3.1 | Failure analysis | Phase 3 |
| [x] | Task 3.2 | Apply fixes (prompt, KB, threshold, formatting) | Phase 3 |
| [ ] | Task 3.3 | Re-run evaluation (repeat until targets met) | Phase 3 |

## Phase 4: Documentation

| Status | Task | Description | Roadmap Ref |
|:------:|------|-------------|-------------|
| [ ] | Task 4.1 | Codebase documentation (Layers 2-4) | Phase 4 |
| [ ] | Task 4.2 | Architecture documentation (6 files) | Phase 4 |
| [ ] | Task 4.3 | User-facing guides (3 files) | Phase 4 |
| [ ] | Task 4.4 | Documentation index | Phase 4 |
| [ ] | Task 4.5 | Project-level README | Phase 4 |
| [ ] | Task 4.6 | POC Evaluation Report | Phase 4 |
| [ ] | Task 4.7 | Success criteria checklist | Phase 4 |
| [ ] | Task 4.8 | Lessons learned (full retrospective) | Phase 4 |
| [ ] | Task 4.9 | Phase 2 recommendations | Phase 4 |

## Phase 5: Demo Capture & Presentation

| Status | Task | Description | Roadmap Ref |
|:------:|------|-------------|-------------|
| [ ] | Task 5.1 | Select demo queries (8-10) | Phase 5 |
| [ ] | Task 5.2 | Build Selenium demo script | Phase 5 |
| [ ] | Task 5.3 | Record demo (screenshots + video) | Phase 5 |
| [ ] | Task 5.4 | Create React presentation app (16 slides) | Phase 5 |
| [ ] | Task 5.5 | Prepare Q&A responses | Phase 5 |

## Phase 6: Buffer, Polish & Finalize

| Status | Task | Description | Roadmap Ref |
|:------:|------|-------------|-------------|
| [ ] | Task 6.1 | Final smoke test | Phase 6 |
| [ ] | Task 6.2 | Backup (git commit) | Phase 6 |
| [ ] | Task 6.3 | Update CLAUDE.md (Week 4 complete) | Phase 6 |

---

## Checkpoints

| Status | Checkpoint | After Task | Feature |
|:------:|------------|------------|---------|
| [x] | CP 1 | Task 0.6 | Workspace setup + fresh ingestion |
| [x] | CP 2 | Task 1.4 | UX Redesign complete |
| [ ] | CP 3 | Task 3.3 | Round 2 metrics finalized |

---

## Progress Summary

| Phase | Total | Done | Progress |
|-------|-------|------|----------|
| Phase 0 — Setup | 6 | 6 | 100% |
| Phase 1 — UX Redesign | 4 | 4 | 100% |
| Phase 2 — Testing | 13 | 13 | 100% |
| Phase 3 — Fix Loop | 3 | 2 | 67% |
| Phase 4 — Documentation | 9 | 0 | 0% |
| Phase 5 — Demo | 5 | 0 | 0% |
| Phase 6 — Finalize | 3 | 0 | 0% |
| **Total** | **43** | **25** | **58%** |
