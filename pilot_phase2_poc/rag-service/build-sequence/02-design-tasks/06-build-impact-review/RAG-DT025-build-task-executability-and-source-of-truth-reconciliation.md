# RAG-DT025: Build Task Executability And Source-Of-Truth Reconciliation

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-DT025` |
| Lane | design / delivery control |
| Dependencies | `RAG-DT021`, `RAG-DT022`, `RAG-DT023`, `RAG-DT024`, reopened `RAG-DT015`, `RAG-DT018`, `RAG-DT019`, `RAG-DT020` |
| Blocks | `RAG-DT013` and final build-task authorization; safe fixture-only mechanics require explicit `RAG-DT013` Revision 2 authorization |
| Responsible | Delivery/governance owner |
| Accountable approver | Architecture/service owner |
| Required reviewers | RAG/data, platform, security, evaluation, and QA owners |
| Branch | `codex/rag-dt025-task-executability-reconciliation` |
| Worktree | `C:\tmp\rag-dt025-task-executability-reconciliation` |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT025-task-executability-reconciliation.md` |

## 1. Objective And Scope

Make the final build backlog executable, dependency-correct, and governed by
one current source of truth before `RAG-DT013` is rerun.

The current planned task files are structured shells. Generic “failing test
placeholder” instructions and invalid commands such as running pytest on a
Markdown review artifact do not satisfy acceptance-check-first delivery.

## 2. Dependencies And Gates

Run after the new and reopened technical decisions are complete. This task
must not resolve conflicts by copying stale statuses across files.

## 3. Expected Artifacts

```text
docs/planning/build-task-executability-and-handoff-matrix.md
docs/planning/source-of-truth-status-matrix.md
docs/planning/exception-and-deferral-register.md
docs/planning/dt013-revision2-authorization-matrix-draft.md
build-evidence/RAG-DT025-task-executability-reconciliation.md
```

It must also update every affected file under `build-sequence/03-build-tasks/`.
`RAG-DT025` prepares the draft authorization input; only `RAG-DT013` may
create, approve, and publish `dt013-revision2-closure-manifest.md`.

## 4. Acceptance Criteria

- Every task has explicit task IDs in `Dependencies` and `Blocks`; “see
  section” is not accepted.
- Every red check is task-specific, executable in PowerShell, and fails for the
  intended missing behavior.
- Test code is stored in a testable file type and implementation evidence is
  stored in its intended artifact; Markdown is never passed to pytest as
  Python.
- Commands use accepted environment-variable names and paths.
- The configuration matrix uses the actual `RAG_` settings names and marks bare
  `QDRANT_*` and `RAG_ENV` instructions as reconciled or historical.
- Acceptance criteria trace to design decisions, runtime behavior, negative
  cases, and evidence.
- Indexes, task statuses, architecture checklist, design artifacts, registry
  metadata, and evidence history distinguish current state from historical
  completion.
- Historical evidence is preserved and labeled superseded where appropriate.
- Every build task and exception/deferral declares `Responsible`, `Accountable
  Approver`, `Required Reviewers`, estimated effort/risk, rollback boundary,
  handoff evidence, authorization class, and expiry/review date.
- The authorization matrix separates safe fixture-only mechanics from
  non-fixture corpus, external-provider, shared-service, and production work;
  it records the owner, evidence, and expiry for every exception or deferral.
- Governance checks fail on stale status claims, invalid verification commands,
  placeholders in ready tasks, and missing design dependencies.

## 5. Preflight

Run the governance script, full tests, and searches for `Pending`, `Draft`,
`In Review`, `placeholder`, bare `QDRANT_`, and `pytest *.md`. Classify each
hit as current, historical, or stale before editing.

## 6. Red Check

Add failing governance tests for at least:

- a current index marking a reopened task complete;
- a ready task containing a generic failing-test placeholder;
- a task invoking pytest on Markdown;
- a final build task missing a mandatory design dependency.
- a task whose current configuration instruction conflicts with the canonical
  `RAG_` matrix or treats a historical model decision as an active default.

## 7. Implementation Or Design Work

1. Build a single status/dependency/authorization matrix.
2. Reconcile all current source-of-truth artifacts.
3. Rewrite each final build task’s red check and verification matrix.
4. Normalize environment names and exact dependencies.
5. Classify every build task as fixture-only, non-fixture, external-provider,
   shared-service, or production; do not use the fixture classification to
   override registry eligibility.
6. Add the full RACI fields, effort/risk, rollback, handoff evidence,
   authorization class, and any exception/deferral expiry.
7. Extend governance checks and tests.
8. Rerun `RAG-DT013` only after this task passes.

## 8. Verification Matrix

| Check | Required Result |
|---|---|
| Governance negative tests | Each injected defect fails for the intended reason |
| Task commands | Every documented command is syntactically/executably valid |
| Status matrix | No current source-of-truth contradiction remains |
| Dependency matrix | Every build task traces to all mandatory design gates |
| Authorization matrix | Draft input preserves all non-fixture blocks; DT013 alone publishes the approved closure manifest |
| Full checks | Governance, pytest, Ruff, Bandit, and pip-audit pass |

## 9. PR Handoff

Provide the complete status/dependency matrix, rewritten task list, negative
governance-test evidence, unresolved deferrals, and the exact order for the
reopened `RAG-DT013`.

## 10. Merge And Closeout

Require delivery, technical, QA, operations, and documentation-owner review.
Do not close with placeholders or with evidence that only checks file
existence.

## 11. Out Of Scope And Deferred Work

Runtime RAG implementation is out of scope. Making the implementation tasks
executable and internally consistent is not deferrable.
