# Task 4.3 Output — User-Facing Guides (3 files)

**Status**: Complete
**Date**: 2026-02-10

## Files Created

| # | File | Audience | Description |
|---|------|----------|-------------|
| 1 | `documentation/guides/user_guide.md` | CS Agents | What is the co-pilot, how to ask effective questions, 4-section response card explained, when to escalate, 10 sample queries |
| 2 | `documentation/guides/deployment_notes.md` | Developers/IT | Prerequisites, 6-step install, full .env reference (14 vars), start commands, test commands, troubleshooting (11 issues) |
| 3 | `documentation/guides/known_limitations.md` | All stakeholders | Scope limits (8), technical limits (8), KB limits (6), Round 4 eval results, evaluation gaps, Phase 2 recommendations (10) |

## Validation Checklist

- [x] User guide covers CS agent workflow
- [x] User guide explains 4-section response card (answer, sources, related docs, confidence)
- [x] Deployment notes cover full installation from scratch
- [x] Deployment notes include troubleshooting section (11 common issues)
- [x] Known limitations comprehensive and honest
- [x] All 3 files created

## Key Content Highlights

### user_guide.md
- Effective question tips with comparison table (less effective vs more effective)
- 4-section response card breakdown with color codes and action guidance
- Escalation table mapping request types to recommended channels
- 10 sample queries across regulatory, carrier, reference, and internal policy categories

### deployment_notes.md
- Full .env reference with 14 variables (1 required, 13 optional with defaults)
- Copy-pasteable installation commands for Windows and macOS/Linux
- Directory structure overview
- 11-row troubleshooting table with problem → cause → solution

### known_limitations.md
- Round 4 evaluation results table (all 6 targets met)
- Honest evaluation gaps: confidence distribution skew, LLM nondeterminism, carrier-specific gaps
- 10 specific Phase 2 recommendations based on POC findings
- Explains the 2.0% hallucination measurement artifact (Q-39 baseline issue)
