# RAG-DT020: Post-Build Evaluation And Tuning Loop

Status: Blocked

## Sequence Entry

Start from `build-sequence/00-index.md`, then open the design lane index before
opening this task file. Task files should follow the canonical template in
`build-sequence/00-governance/01-task-template.md`.

| Field | Value |
|---|---|
| Task ID | `RAG-DT020` |
| Lane | design |
| Design Lane | 05-runtime-technical-design |
| Task Name | Post-Build Evaluation And Tuning Loop |
| Dependencies | `RAG-DT005`, `RAG-DT006`, `RAG-DT007`, `RAG-DT010`, `RAG-DT014`, `RAG-DT015`, `RAG-DT017`, `RAG-DT018`, `RAG-DT019`, `RAG-DT022`, `RAG-DT023` |
| Blocks | `RAG-DT013`, `RAG-BT019`, `RAG-BT022`, post-build adjustment work |
| Responsible | Evaluation owner |
| Accountable Approver | Product/domain-risk owner |
| Required Reviewers | Service owner, independent domain adjudicator |
| Branch | `codex/rag-dt020-post-build-evaluation-and-tuning-loop` |
| Worktree | `C:\tmp\rag-dt020-post-build-evaluation-and-tuning-loop` |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT020-post-build-evaluation-and-tuning-loop.md` |

## 1. Objective And Scope

> Reopened 2026-07-28. Replace baseline-relative-only acceptance with
> independently justified absolute gates, sample sizes, uncertainty reporting,
> attribution quality, unsafe-answer/false-refusal limits, indirect-injection
> success limits, and runtime latency/error/cost budgets from `RAG-DT022` and
> `RAG-DT023`.

Define what happens after the RAG service is built and evaluated. The build
should not stop at "the harness ran." It needs a governed loop for deciding
whether failures require source, chunking, embedding, retrieval, prompt, model,
schema, API, or CI/CD adjustments.

In scope:

- evaluation run types and when each one runs;
- regression baseline policy;
- pre-registered metrics and absolute thresholds;
- failure taxonomy;
- mapping failures to likely adjustment areas;
- tuning experiment workflow;
- baseline promotion and rejection rules;
- evidence/reporting structure;
- owner decision gates;
- how post-build findings become new tasks or accepted risks.

Out of scope:

- implementing the evaluation harness;
- running full post-build evaluation before the service exists;
- changing model, embedding, chunking, retrieval, or prompt decisions directly;
- production monitoring.

## 2. Dependencies And Gates

Required design inputs:

- `docs/design/chunking-experiment.md`
- `docs/evaluation/golden-questions.md`
- `docs/design/query-planning/query_planner_rules.yaml`
- `docs/design/embedding-benchmark-plan.md`
- `docs/design/llm-model-selection-decision.md`
- `docs/design/test-vector-db-ci-strategy.md`
- `docs/design/retrieval-strategy-and-fusion-contract.md`
- `docs/design/generation-and-query-api-contract.md`
- `RAG-BT019` evaluation harness task file
- `RAG-BT022` readiness review task file, which cannot establish a production
  claim while DT023 production-tier controls remain deferred

This task blocks `RAG-DT013`. A waiver or deferral is not gate evidence and
cannot authorize dependent non-fixture, external-provider, shared-service, or
production work. It must produce a `NO-GO`/blocked manifest entry for every
affected task; only explicitly listed fixture-only tasks may proceed.

## 3. Expected Artifacts

Create these durable artifacts:

```text
docs/design/post-build-evaluation-and-tuning-loop.md
docs/design/experiments/post-build-evaluation/dt020-run-002/evaluation-taxonomy.md
docs/design/experiments/post-build-evaluation/dt020-run-002/tuning-playbook.md
docs/design/experiments/post-build-evaluation/dt020-run-002/release-promotion-manifest.yaml
docs/design/experiments/post-build-evaluation/dt020-run-002/decision-log.md
docs/design/experiments/post-build-evaluation/dt020-run-002/decision-gate.md
build-evidence/RAG-DT020-post-build-evaluation-and-tuning-loop.md
```

The contract artifact should be the concise source of truth. The experiment
folder may contain the detailed taxonomy, playbook, and gate evidence.

## 4. Acceptance Criteria

- Evaluation run types are defined, including:
  - fast unit/regression checks;
  - Qdrant-backed integration checks;
  - end-to-end query API checks;
  - LLM-backed evaluation checks when credentials are intentionally supplied;
  - post-change comparison checks.
- The design defines which checks run locally, in PR CI, on `main`, and during
  owner-reviewed post-build assessment.
- Evaluation metrics and absolute pass/fail thresholds are pre-registered,
  including at least:
  - retrieval Recall@K / expected chunk presence;
  - ranking quality or MRR;
  - citation validity;
  - answer quality;
  - groundedness;
  - refusal/safety behavior;
  - irrelevant-query behavior;
  - malicious-query behavior;
  - latency;
  - provider/model errors;
  - malformed output handling.
- Failure categories map to likely adjustment areas:
  - source registry / source eligibility;
  - canonical/candidate corpus;
  - chunking;
  - embedding model;
  - vector DB payload/indexing;
  - retrieval strategy/fusion;
  - query planner;
  - prompt/generation;
  - output validation/retry/fallback;
  - query API contract;
  - CI/CD or local Docker environment.
- The design defines how tuning experiments are recorded.
- The design defines when a new baseline can be accepted.
- A promotion decision freezes and records the corpus release, evaluation
  dataset manifest, embedding model, retrieval configuration, model/prompt
  configuration, and runtime tier. Any tuning change requires a fresh held-out
  evaluation before promotion.
- The design defines when a failed evaluation creates a new build task,
  design task, bugfix task, or owner-accepted deferral.
- The design defines how `RAG-BT019` reports unit/mocked, Qdrant-backed, and
  LLM-backed results separately.
- Build Task Impact maps required updates to `RAG-BT019`, `RAG-BT022`, and any
  affected retrieval/generation/API tasks.

## 5. Preflight

Use a fresh branch and worktree.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt020"
$Slug = "post-build-evaluation-and-tuning-loop"
$Branch = "codex/$TaskId-$Slug"
$WorktreePath = Join-Path $WorktreeRoot "$TaskId-$Slug"

New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null
git -C $RepoRoot fetch origin
git -C $RepoRoot pull --ff-only origin main
git -C $RepoRoot config core.longpaths true
git -C $RepoRoot worktree add -b $Branch $WorktreePath origin/main
git -C $WorktreePath status --short --branch
```

## 6. Red Check

Before writing the reopened design, confirm no fresh decision-gate artifact
already exists:

```powershell
$ServiceRoot = Join-Path $WorktreePath "pilot_phase2_poc/rag-service"
Test-Path "$ServiceRoot\docs\design\experiments\post-build-evaluation\dt020-run-002\decision-gate.md"
```

Expected result before the task is implemented:

```text
False
```

## 7. Implementation Or Design Work

Perform the design work in this order:

1. Review DT022 valid evaluation evidence and the DT015, DT018, DT019, and
   DT023 accepted decision inputs.
2. Review `RAG-BT019` and identify what its reports must contain.
3. Define evaluation run types and environments.
4. Pre-register metrics, absolute thresholds, and threshold ownership.
5. Define failure taxonomy.
6. Map failure categories to likely adjustment areas.
7. Define tuning experiment evidence structure.
8. Define frozen-release acceptance, rejection, rollback, and fresh-held-out
   re-evaluation rules.
9. Define owner decision gates after evaluation.
10. Map required build-task updates.
11. Record the decision gate and evidence.

## 8. Verification Matrix

| Check | Command / Evidence | Required Result |
|---|---|---|
| Contract exists | `Test-Path docs/design/post-build-evaluation-and-tuning-loop.md` | `True` |
| Taxonomy exists | `Test-Path docs/design/experiments/post-build-evaluation/dt020-run-002/evaluation-taxonomy.md` | `True` |
| Tuning playbook exists | `Test-Path docs/design/experiments/post-build-evaluation/dt020-run-002/tuning-playbook.md` | `True` |
| Frozen release | `Test-Path docs/design/experiments/post-build-evaluation/dt020-run-002/release-promotion-manifest.yaml` | `True` |
| Decision gate exists | `Test-Path docs/design/experiments/post-build-evaluation/dt020-run-002/decision-gate.md` | `True` |
| Build impact recorded | Search contract for `RAG-BT019` and `RAG-BT022` | Both present |
| Evidence exists | `Test-Path build-evidence/RAG-DT020-post-build-evaluation-and-tuning-loop.md` | `True` |

## 9. PR Handoff

The PR description must include:

- evaluation loop summary;
- failure taxonomy summary;
- tuning/baseline decision rules;
- affected build tasks;
- verification commands;
- evidence path.

## 10. Merge And Closeout

After merge:

- refresh `main`;
- verify the task file status and evidence metadata are closed out;
- prune/remove the task worktree;
- delete the local branch;
- delete the remote branch when permitted;
- confirm `RAG-DT013` still waits for this task or records a blocked manifest
  entry for each affected authorization class.

## 11. Out Of Scope And Deferred Work

Deferred unless explicitly approved during the task:

- production observability and SLOs;
- automated online evaluation;
- user-feedback collection;
- production corpus promotion;
- model replacement;
- external benchmark suites.
