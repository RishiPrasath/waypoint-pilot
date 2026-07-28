# RAG-DT019: Generation Prompt, Safeguards, Output Schema, And Query API Contract

Status: Blocked

## Sequence Entry

Start from `build-sequence/00-index.md`, then open the design lane index before
opening this task file. Task files should follow the canonical template in
`build-sequence/00-governance/01-task-template.md`.

| Field | Value |
|---|---|
| Task ID | `RAG-DT019` |
| Lane | design |
| Design Lane | 05-runtime-technical-design |
| Task Name | Generation Prompt, Safeguards, Output Schema, And Query API Contract |
| Dependencies | `RAG-DT006`, `RAG-DT007`, `RAG-DT009`, `RAG-DT015`, `RAG-DT017`, `RAG-DT018`, `RAG-DT021`, `RAG-DT022`, `RAG-DT023`, `RAG-DT024` |
| Blocks | `RAG-DT013`, `RAG-BT015`, `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, `RAG-BT019`, frontend/BFF query consumers |
| Responsible | API/service owner |
| Accountable Approver | Service owner |
| Required Reviewers | Security owner, BFF/API consumer owner |
| Branch | `codex/rag-dt019-generation-prompt-safeguards-output-schema-and-query-api-contract` |
| Worktree | `C:\tmp\rag-dt019-generation-prompt-safeguards-output-schema-and-query-api-contract` |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT019-generation-prompt-safeguards-output-schema-and-query-api-contract.md` |

## 1. Objective And Scope

> Reopened 2026-07-28. Revise this contract after `RAG-DT021` through
> `RAG-DT024` to add deployment-tier API controls, indirect-injection behavior,
> claim-to-span citation support, provider lifecycle/fallback behavior, request
> and resource limits, and the reconciled versioned API/error schema.

Define the generation prompt contract, safeguard behavior, output schema, and
query API consumer contract before generation, validation, query endpoint, or
evaluation build tasks start.

This task exists because current generation expectations are spread across the
query planner, LLM evaluation fixture, LLM model selection run, output
validation task, and query API task. Implementation needs one accepted contract
so prompt behavior, citations, refusal fields, validation, and API responses do
not drift.

In scope:

- generation message roles and boundaries;
- retrieved-context formatting;
- rule that retrieved chunks are untrusted data;
- citation instructions and citation object schema;
- refusal and safe-response schema;
- low-confidence/no-evidence answer behavior;
- JSON output schema;
- validation, retry, and fallback expectations;
- API request and response schema;
- error-envelope mapping;
- planner/retrieval/generation metadata exposed to callers;
- provider/model/latency metadata policy;
- environment variable naming for LLM/runtime provider settings;
- FastAPI testing and dependency override expectations.

Out of scope:

- runtime implementation;
- frontend UI implementation;
- changing the selected LLM provider/model unless evidence requires reopening
  the model decision;
- adding a separate moderation/safeguard model unless explicitly decided.

## 2. Dependencies And Gates

Required design inputs:

- `docs/evaluation/golden-questions.md`
- `docs/design/query-planning/query_planner_rules.yaml`
- `docs/design/query-planning/query_planner_tests.yaml`
- `docs/design/llm-model-evaluation-plan.md`
- `docs/design/llm-model-selection-decision.md`
- `docs/design/retrieval-strategy-and-fusion-contract.md`
- relevant `RAG-BT015` through `RAG-BT019` task files

This task blocks `RAG-DT013`. A waiver or deferral is not gate evidence and
cannot authorize dependent non-fixture, external-provider, shared-service, or
production work. It must produce a `NO-GO`/blocked manifest entry for every
affected task; only explicitly listed fixture-only tasks may proceed.

## 3. Expected Artifacts

Create these durable artifacts:

```text
docs/design/generation-and-query-api-contract.md
docs/design/experiments/generation-api-contract/dt019-run-002/prompt-contract.md
docs/design/experiments/generation-api-contract/dt019-run-002/response-schema.json
docs/design/experiments/generation-api-contract/dt019-run-002/api-examples.md
docs/design/experiments/generation-api-contract/dt019-run-002/error-contract.md
docs/design/experiments/generation-api-contract/dt019-run-002/decision-gate.md
build-evidence/RAG-DT019-generation-prompt-safeguards-output-schema-and-query-api-contract.md
```

The contract artifact should be the concise source of truth. The experiment
folder may contain schema drafts, examples, and decision evidence.

## 4. Acceptance Criteria

- Prompt/message roles are defined, including system/developer/user boundaries.
- Retrieved-context formatting is defined and includes required chunk metadata.
- Retrieved chunks are explicitly treated as untrusted data.
- Citation instructions are defined.
- Factual claims cite approved source spans. Curator boundaries, eligibility
  warnings, and safe-refusal rationale are labeled as service policy notices,
  never represented as source citations.
- Citation object schema includes at least:
  - `document_id`;
  - `snapshot_id`;
  - `chunk_id`;
  - `chunk_strategy`;
  - `heading_path`;
  - `source_uri`;
  - `candidate_sha256`;
  - source eligibility / reuse boundary fields when applicable.
- Refusal and safe-response behavior is defined for:
  - irrelevant questions;
  - unsupported operational/live-status questions;
  - partner-source/internal-procedure questions;
  - malicious/prompt-injection questions;
  - license-sensitive/cite-only questions;
  - ambiguous questions;
  - low-confidence/no-evidence retrieval.
- JSON output schema is provided and validates representative positive,
  boundary, refusal, and error examples.
- API request/response examples are provided for `POST /api/v1/query` or the
  selected path.
- API response fields include planner, retrieval, generation, citation, and
  safe-response information needed by BFF/frontend consumers.
- Error-envelope behavior is mapped for validation failures, provider failures,
  retries exhausted, malformed model output, timeout, and unavailable
  dependencies.
- Exactly two response classes are defined: HTTP `200` typed RAG responses for
  answers, refusals, no-evidence, and clarification; and one versioned problem
  response for transport/error outcomes (`422`, `429`, `502`, `503`, `504`).
  The problem response includes a stable code, public-safe message, request ID,
  retryability, and no raw backend exception or provider body.
- Runtime LLM/provider environment variable names are selected or alias rules
  are documented.
- Build Task Impact maps required updates to `RAG-BT015`, `RAG-BT016`,
  `RAG-BT017`, `RAG-BT018`, and `RAG-BT019`.

## 5. Preflight

Use a fresh branch and worktree.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt019"
$Slug = "generation-prompt-safeguards-output-schema-and-query-api-contract"
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

Before writing the reopened design, confirm the historical contract is input
only and no fresh decision-gate artifact already exists:

```powershell
$ServiceRoot = Join-Path $WorktreePath "pilot_phase2_poc/rag-service"
Test-Path "$ServiceRoot\docs\design\experiments\generation-api-contract\dt019-run-002\decision-gate.md"
```

Expected result before the task is implemented:

```text
False
```

## 7. Implementation Or Design Work

Perform the design work in this order:

1. Review DT022 acceptance gates, DT023 configuration/readiness contract, and
   planner safe-response classes.
2. Review the currently supported model/fallback result from `RAG-DT015` and
   retrieval output metadata from `RAG-DT018`.
4. Define prompt/message roles and context boundaries.
5. Define retrieved context formatting and untrusted-data rules.
6. Define answer, source-citation, policy-notice, safe-refusal, and error
   schemas with the two response classes.
7. Define validation, retry, fallback, malformed-output behavior, and public
   error mapping for `422`, `429`, `502`, `503`, and `504`.
8. Define API request/response examples for positive and safe-response cases.
9. Define environment variable naming for LLM/provider runtime settings.
10. Map contract fields to affected build tasks.
11. Record the decision gate and evidence.

Research is allowed when API contract or prompt-safety details need external
grounding, but the final contract must be specific to the Waypoint RAG service
and its accepted fixtures.

## 8. Verification Matrix

| Check | Command / Evidence | Required Result |
|---|---|---|
| Contract exists | `Test-Path docs/design/generation-and-query-api-contract.md` | `True` |
| Prompt contract exists | `Test-Path docs/design/experiments/generation-api-contract/dt019-run-002/prompt-contract.md` | `True` |
| Schema exists | `Test-Path docs/design/experiments/generation-api-contract/dt019-run-002/response-schema.json` | `True` |
| Error contract exists | `Test-Path docs/design/experiments/generation-api-contract/dt019-run-002/error-contract.md` | `True` |
| Examples exist | `Test-Path docs/design/experiments/generation-api-contract/dt019-run-002/api-examples.md` | `True` |
| Build impact recorded | Search contract for `RAG-BT015`, `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, `RAG-BT019` | All present |
| Evidence exists | `Test-Path build-evidence/RAG-DT019-generation-prompt-safeguards-output-schema-and-query-api-contract.md` | `True` |

## 8.1 Proposed Decision Summary

`POST /api/v1/query` remains a candidate endpoint path; this reopened task
does not accept an API or model default until its dependencies are accepted.
The historical `llama-3.3-70b-versatile` selection and `dt019-run-001` schema
are superseded inputs, not current defaults. The fresh contract must use the
DT015 selected-or-deferred model result, DT018 frozen retrieval result, DT022
evaluation gate, and DT023 configuration/readiness rules. It must prove the
two response classes are non-contradictory and that source citations cannot be
confused with policy notices.

## 9. PR Handoff

The PR description must include:

- prompt/message contract summary;
- safeguard and refusal decisions;
- API schema summary;
- environment variable naming decision;
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

- frontend UI implementation;
- LLM moderation/safeguard model selection;
- model replacement;
- provider migration;
- production prompt A/B testing.
