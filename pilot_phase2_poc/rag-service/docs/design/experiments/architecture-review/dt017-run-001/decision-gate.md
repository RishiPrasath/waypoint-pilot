# DT017 Decision Gate

Status: In Review
Run: `dt017-run-001`
Date: 2026-07-18

## Decision

```text
Pass With Required Follow-Up Tasks
```

## Meaning

The architecture/design is not blocked or failed. The completed design tasks,
current setup code, CI/CD posture, and final build sequence are directionally
sufficient.

However, `RAG-DT013` should not proceed until the owner either:

1. accepts, creates, and completes the required follow-up design tasks; or
2. explicitly waives those follow-up tasks and accepts the related High risks.

## Required Follow-Up Design Tasks

| Proposed Task | Required Before DT013? | Reason | Owner Decision |
|---|---|---|---|
| `RAG-DT018: Hybrid Retrieval Scoring And Fusion Contract` | Yes, unless waived | Hybrid retrieval ranking behavior is too implicit for final build-task impact review. | Pending |
| `RAG-DT019: Generation Prompt, Output Schema, And Query API Consumer Contract` | Yes, unless waived | Prompt, output, citation, refusal, and API consumer contracts are too implicit for implementation. | Pending |

## Required Owner Decision / Remediation Items

| Item | Severity | Required Before DT013? | Owner Decision |
|---|---|---|---|
| GitHub repository enforcement/security settings: secret scanning disabled, Dependabot security updates disabled, no `main` branch protection, no rulesets. | High | Yes: enable or explicitly accept risk. | Pending |
| `httpx2`/`httpcore2` dependency provenance and selection rationale. | High | Yes: document acceptance or replace. | Pending |

## DT013 Handoff

`RAG-DT013` should update affected build tasks with:

- environment-variable naming normalization;
- explicit `/api/v1/query` contract details;
- broader future test exclusion strategy for Bandit;
- normalized-text SHA semantics for markdown candidates;
- candidate-vs-canonical fixture wording;
- inert nested `.github/` cleanup or note;
- production data-governance deferrals.

## Final Gate Statement

`RAG-DT013` remains blocked until the required follow-up design tasks and owner
decision items above are created/completed or explicitly waived.

