# RAG-DT018: Retrieval Strategy Selection, Scoring, And Fusion Contract

Status: Blocked

## Sequence Entry

Start from `build-sequence/00-index.md`, then open the design lane index before
opening this task file. Task files should follow the canonical template in
`build-sequence/00-governance/01-task-template.md`.

| Field | Value |
|---|---|
| Task ID | `RAG-DT018` |
| Lane | design |
| Design Lane | 05-runtime-technical-design |
| Task Name | Retrieval Strategy Selection, Scoring, And Fusion Contract |
| Dependencies | `RAG-DT005`, `RAG-DT006`, `RAG-DT007`, `RAG-DT010`, `RAG-DT012`, `RAG-DT014`, `RAG-DT017`, `RAG-DT022`, `RAG-DT024` |
| Blocks | `RAG-DT013`, `RAG-BT013`, `RAG-BT014`, `RAG-BT018`, `RAG-BT019` |
| Responsible | Retrieval engineer |
| Accountable Approver | RAG evaluation owner |
| Required Reviewers | Domain SME, service owner |
| Branch | `codex/rag-dt018-retrieval-strategy-selection-and-fusion-contract` |
| Worktree | `C:\tmp\rag-dt018-retrieval-strategy-selection-and-fusion-contract` |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT018-retrieval-strategy-selection-and-fusion-contract.md` |

## 1. Objective And Scope

> Reopened 2026-07-28. The fixed semantic/lexical weights and low-confidence
> thresholds were selected without an independent hybrid benchmark. Complete
> `RAG-DT022` and compare semantic-only, lexical-only, RRF/DBSF, and weighted
> fusion on calibration data, then validate the frozen choice on held-out data.
> Per-query normalized rank scores alone must not be treated as calibrated
> evidence confidence.

Define how the RAG service chooses the right retrieval behavior for each query
scenario before semantic, lexical, hybrid, API, or evaluation build tasks start.

This task exists because having a semantic baseline and a hybrid retrieval task
is not enough. The design also needs a scenario-level decision contract that
answers:

- when retrieval is allowed;
- when no retrieval is safer;
- when semantic-only retrieval is enough;
- when lexical or exact-match behavior should dominate;
- when metadata filters must be hard filters;
- how semantic and lexical candidates are fused;
- what low-confidence retrieval should do before generation.

In scope:

- retrieval-mode decision matrix by query scenario;
- query-planner-output to retrieval-mode mapping;
- semantic, lexical, hybrid, metadata-filtered, exact-match boosted,
  metadata-only, and no-retrieval modes;
- lexical method selection or accepted baseline;
- tokenization and normalization rules;
- candidate-pool sizing;
- score normalization and fusion;
- metadata filter and boost behavior;
- deterministic tie-breaking;
- rerank hook input/output contract;
- low-confidence retrieval behavior;
- evaluation expectations for retrieval behavior.

Out of scope:

- runtime implementation;
- Qdrant schema changes unless needed as a design requirement;
- LLM answer generation;
- final production corpus promotion.

## 2. Dependencies And Gates

Required design inputs:

- `docs/design/chunking-experiment.md`
- `docs/evaluation/golden-questions.md`
- `docs/design/query-planning/query_planner_rules.yaml`
- `docs/design/query-planning/query_planner_tests.yaml`
- `docs/design/embedding-benchmark-plan.md`
- `docs/design/test-vector-db-ci-strategy.md`
- `docs/design/source-snapshot-and-markdown-candidates.md`
- `RAG-DT017` architecture sufficiency findings, if completed

This task blocks `RAG-DT013`. A waiver or deferral is not gate evidence and
cannot authorize dependent non-fixture, external-provider, shared-service, or
production work. It must produce a `NO-GO`/blocked manifest entry for every
affected task; only explicitly listed fixture-only tasks may proceed.

## 3. Expected Artifacts

Create these durable artifacts:

```text
docs/design/retrieval-strategy-and-fusion-contract.md
docs/design/experiments/retrieval-strategy/dt018-run-002/retrieval-scenario-matrix.md
docs/design/experiments/retrieval-strategy/dt018-run-002/scoring-options.md
docs/design/experiments/retrieval-strategy/dt018-run-002/calibration-report.md
docs/design/experiments/retrieval-strategy/dt018-run-002/heldout-report.md
docs/design/experiments/retrieval-strategy/dt018-run-002/decision-gate.md
build-evidence/RAG-DT018-retrieval-strategy-selection-and-fusion-contract.md
```

The contract artifact should be the concise source of truth. The experiment
folder may contain longer research notes, comparisons, and gate evidence.

## 4. Acceptance Criteria

- A retrieval-mode decision matrix exists and covers at least:
  - in-scope natural language questions;
  - exact document/title/source questions;
  - HS code, article number, tariff, permit, and named-procedure questions;
  - market-constrained questions;
  - source-boundary questions;
  - ambiguous questions;
  - irrelevant questions;
  - operational/live-status questions;
  - partner-source/internal-procedure questions;
  - malicious/prompt-injection questions;
  - license-sensitive/cite-only questions.
- The design states which scenarios use:
  - no retrieval;
  - metadata-only lookup;
  - semantic-only baseline retrieval;
  - lexical-only diagnostic retrieval;
  - exact-match boosted retrieval;
  - metadata-filtered hybrid retrieval;
  - fused hybrid retrieval;
  - rerank hook, even if no-op initially.
- The design defines lexical tokenization and normalization rules.
- The design defines candidate-pool sizes for semantic, lexical, and fused
  retrieval.
- The design defines score normalization and fusion behavior.
- The design defines hard metadata filters versus optional metadata boosts.
- The design defines deterministic tie-breaking.
- The design defines low-confidence retrieval handling before generation.
- Semantic-only, lexical-only, weighted hybrid, and rank-fusion alternatives
  remain candidates until selected by the DT022 calibration procedure; weights,
  boosts, candidate pools, and abstention thresholds are frozen before the
  held-out run.
- Held-out reporting includes retrieval quality, claim/span attribution,
  false-answer and false-abstention rates, confidence calibration, and
  uncertainty. Per-query normalized ranks are ordering signals, not calibrated
  confidence.
- The design maps DT006 golden questions and DT007 planner test classes to the
  expected retrieval modes.
- The design states how hybrid retrieval should preserve or improve the DT010
  semantic baseline.
- A Build Task Impact section maps required updates to `RAG-BT013`,
  `RAG-BT014`, `RAG-BT018`, and `RAG-BT019`.

## 5. Preflight

Use a fresh branch and worktree.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt018"
$Slug = "retrieval-strategy-selection-and-fusion-contract"
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

Before writing the reopened design, confirm the historical contract is marked
as superseded input and no new decision-gate artifact already exists:

```powershell
$ServiceRoot = Join-Path $WorktreePath "pilot_phase2_poc/rag-service"
Test-Path "$ServiceRoot\docs\design\experiments\retrieval-strategy\dt018-run-002\decision-gate.md"
```

Expected result before the task is implemented:

```text
False
```

## 7. Implementation Or Design Work

Perform the design work in this order:

1. Review current planner classifications and DT022 calibration/held-out cases.
2. Review current chunking and embedding benchmark assumptions as historical
   fixture evidence only.
3. Identify retrieval scenarios that need different behavior.
4. Define the retrieval-mode decision matrix.
5. Define the lexical method and normalization assumptions.
6. Compare semantic-only, lexical-only, weighted hybrid, and rank-fusion
   candidates on calibration data only.
7. Freeze the candidate configuration, then measure it once on held-out data.
8. Define metadata filter, metadata boost, and source-eligibility behavior.
9. Define low-confidence and no-evidence behavior.
10. Define rerank hook input/output, even if reranking is deferred.
11. Record calibration, held-out, and uncertainty evidence; then update
    affected build-task impact notes and the decision gate.

Research is allowed when method details need external grounding, but the final
contract must be grounded in the actual Waypoint RAG service corpus, planner
rules, golden questions, and build tasks.

## 8. Verification Matrix

| Check | Command / Evidence | Required Result |
|---|---|---|
| Contract exists | `Test-Path docs/design/retrieval-strategy-and-fusion-contract.md` | `True` |
| Scenario matrix exists | `Test-Path docs/design/experiments/retrieval-strategy/dt018-run-002/retrieval-scenario-matrix.md` | `True` |
| Calibration and holdout | `Test-Path docs/design/experiments/retrieval-strategy/dt018-run-002/calibration-report.md`; `Test-Path docs/design/experiments/retrieval-strategy/dt018-run-002/heldout-report.md` | Both `True` |
| Decision gate exists | `Test-Path docs/design/experiments/retrieval-strategy/dt018-run-002/decision-gate.md` | `True` |
| Build impact recorded | Search contract for `RAG-BT013`, `RAG-BT014`, `RAG-BT018`, `RAG-BT019` | All present |
| Evidence exists | `Test-Path build-evidence/RAG-DT018-retrieval-strategy-selection-and-fusion-contract.md` | `True` |

## 8.1 Proposed Decision Summary

The prior weighted-fusion formula, thresholds, and boost caps are historical
inputs only. This reopened task does not select a runtime default. It must
compare candidates under DT022, freeze the choice before held-out measurement,
and state the result with uncertainty. No-retrieval planner classifications
remain a hard precondition before source search; license-sensitive and cite-only
sources remain excluded from answerable retrieval until a later task records
explicit reuse approval.

## 9. PR Handoff

The PR description must include:

- retrieval modes selected;
- fusion/scoring decision;
- low-confidence behavior;
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

- LLM reranking as a runtime dependency;
- production-scale retrieval benchmark;
- production corpus promotion;
- external search integration;
- partner-source/internal source retrieval.
