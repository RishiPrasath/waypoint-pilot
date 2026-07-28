# RAG-DT013: Final Build Task Impact Review

Status: Blocked

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-DT013` |
| Task Name | Final Build Task Impact Review |
| Design Lane | 06-build-impact-review |
| Source Question | Design-to-build transition |
| Decision / ADR | design-to-build-transition-plan.md |
| Related Planning Docs | `build-sequence/02-design-tasks/`, `build-sequence/03-build-tasks/`, `02-rag-db/planning/confirmed-build-sequence.md` |
| Affected Build Tasks | All 03-build-tasks files |
| Branch | `codex/rag-dt013-final-build-task-impact-review` |
| Worktree Path | `C:\tmp\rag-dt013-final-build-task-impact-review` |
| Owner | Architecture/service owner |
| Accountable Approver | Service owner |
| Required Reviewers | RAG/data, platform, security, evaluation, QA, and documentation owners |
| AI Review Partner | Codex |
| Status | Blocked |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT013-final-build-task-impact-review.md` |

## 1. Task Definition

> Revision 2 reopened on 2026-07-28 after independent RAG/data, platform/
> security/operations, and delivery-control review. The previous completion and
> evidence remain historical. They do not authorize final build work.
>
> Re-run this gate only after `RAG-DT021` through `RAG-DT025` and reopened
> `RAG-DT015`, `RAG-DT018`, `RAG-DT019`, and `RAG-DT020` are complete. The
> Revision 2 outcome must be `GO` or `NO-GO`; unresolved conditions must be
> assigned to blocking tasks rather than carried as unowned prose.

Design: review completed design decisions and update affected final build task
files before implementation begins.

Goal: prevent final build tasks from using stale assumptions after KB,
chunking, metadata, model, Docker, CI/CD readiness, query-planning, retrieval
strategy, generation/API contract, safeguard, or evaluation-tuning decisions
are completed.

Output Artifact:

```text
docs/design/final-build-task-impact-review.md
docs/planning/dt013-revision2-closure-manifest.md
```

Acceptance Criteria:

- each completed design task is mapped to affected build tasks
- build task acceptance criteria are updated where design decisions changed
  implementation expectations
- build tasks do not ingest or test against `legacy/phase1-kb-snapshot/` unless
  a design task explicitly says it is an audit fixture
- any unresolved design decision is explicitly deferred with risk and owner
- a deferral is not authorization: it creates a `NO-GO`/blocked closure-manifest
  entry for every dependent non-fixture, external-provider, shared-service, or
  production task. Only individually named fixture-only tasks may proceed.
- `RAG-DT016` is complete, and any CI/CD readiness gaps it identified have been
  either implemented and proven or explicitly deferred with owner signoff
- `RAG-DT017` is complete, and any architecture/design sufficiency gaps it
  identified have been resolved through new design tasks or explicitly deferred
  with owner signoff
- `RAG-DT018` is complete, and retrieval strategy selection, scoring, fusion,
  rerank hook, and low-confidence retrieval behavior have been mapped to
  affected build tasks, or explicitly deferred with owner signoff
- `RAG-DT019` is complete, and generation prompt, safeguard behavior, output
  schema, query API contract, and runtime LLM/provider config names have been
  mapped to affected build tasks, or explicitly deferred with owner signoff
- `RAG-DT020` is complete, and post-build evaluation, tuning, baseline
  promotion, and failure-remediation workflow have been mapped to affected
  build tasks, or explicitly deferred with owner signoff
- G0 through G6 are evaluated with evidence: credential/model containment;
  source trust and corpus lifecycle; valid evaluation; runtime reliability;
  API/error contract; build-task executability; and explicit final
  authorization.
- the closure manifest names every authorized task, its authorization class
  (fixture-only, non-fixture, external-provider, shared-service, or
  production), required evidence, accountable owner, and expiry/review date.
- an authorization is valid only if the manifest records the accountable
  approver identity, required-reviewer approvals, approval timestamp, evidence
  paths or hashes, expiry, and authorization class. A missing field means the
  task is blocked.
- any fixture-only task permitted before non-fixture authorization is listed by
  task ID and has a test namespace; absence from the manifest means it remains
  blocked. Fixture authorization never overrides registry lifecycle state.
- no non-fixture corpus ingestion, live provider call, shared-service launch,
  or production claim is authorized without the corresponding gate evidence.
- no final build task starts with stale KB, metadata, chunking, query, model, or
  Docker/CI, retrieval, generation/API, safeguard, or evaluation assumptions
- final build sequence remains aligned with `../00-index.md`

Out Of Scope:

- runtime implementation
- writing production code
- running final build tasks

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt013"
$Slug = "final-build-task-impact-review"
$Branch = "codex/$TaskId-$Slug"
$WorktreePath = Join-Path $WorktreeRoot "$TaskId-$Slug"

New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null
git -C $RepoRoot fetch origin
git -C $RepoRoot pull --ff-only origin main
git -C $RepoRoot config core.longpaths true
git -C $RepoRoot worktree add -b $Branch $WorktreePath origin/main
git -C $WorktreePath status --short --branch
```

### Linux / macOS Bash

```bash
REPO_ROOT="$HOME/code/waypoint-pilot"
WORKTREE_ROOT="$HOME/code/waypoint-pilot-worktrees"
TASK_ID="rag-dt013"
SLUG="final-build-task-impact-review"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
git -C "$REPO_ROOT" config core.longpaths true
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```
## 3. Acceptance Check

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\final-build-task-impact-review.md" -Pattern "design_task|affected_build_task|decision|action"
```

## 4. Design Work

Create a build-impact matrix with these columns:

- `design_task`
- `decision_or_output`
- `affected_build_task`
- `required_update`
- `status`
- `owner`
- `risk_if_not_updated`
- `authorization_class`
- `evidence_gate`
- `authorized_or_blocked`
- `accountable_approver`
- `required_reviewer_approvals`
- `approval_timestamp`
- `evidence_path_or_hash`
- `expiry_or_review_date`

At minimum, review these impact areas:

- legacy Phase 1 KB snapshot boundary and non-ingestion rule
- KB folder layout and source registry path
- source registry schema
- source snapshot and markdown candidate rules
- chunking strategy and chunk metadata
- golden questions and expected retrieval matches
- query planner vocabulary and safeguard rules
- retrieval strategy selection by scenario
- semantic, lexical, hybrid, metadata-only, exact-match boosted, and
  no-retrieval mode assumptions
- retrieval scoring, score normalization, fusion, metadata filter/boost,
  low-confidence behavior, and rerank hook contract
- LLM model evaluation fixture
- generation prompt/message contract
- retrieved-context formatting and untrusted-chunk safeguards
- output schema, citation schema, refusal schema, and API consumer contract
- runtime LLM/provider environment variable naming
- embedding benchmark fixture
- test vector DB and CI integration strategy
- Docker/local ops and CI integration strategy
- post-build evaluation, tuning, baseline promotion, and failure-remediation
  workflow
- G0 containment record, G1 source trust, G2 corpus lifecycle, G3 evaluation
  validity, G4 runtime reliability, G5 API/error contract, and G6 task
  executability evidence

## 5. Build Task Impact

Affected Build Tasks:

- All 03-build-tasks files

Required Updates:

- Update every affected build task before implementation starts.

Deferred Impact:

- A deferred decision remains only as a named blocked manifest entry with risk,
  accountable owner, evidence gap, and expiry/review date; it cannot authorize
  dependent work except a separately named fixture-only task.

Impact Review Status:

- This task is the final impact review and authorization gate. Its Revision 2
  closure manifest, not historical task status, is the only authority for
  starting a build task.

## 6. Verification

Review with the accountable service owner, RAG Architect, Test Engineer, CI/CD
Engineer, RAG Evaluation Lead, security owner, and Documentation Steward.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt013 final-build-task-impact-review"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt013 final-build-task-impact-review"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to main.

Required PR checks:

- CI pipeline runs
- CI passes
- AI scans the design artifact and affected build-task updates
- human owner reviews the PR
- accepted findings are fixed

## 8. Merge

Merge only after CI passes and the PR is reviewed. Record PR URL, CI result,
merge commit, unresolved risks, and follow-up debt entries if any. Then clean up
the worktree.

### Windows PowerShell

```powershell
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" worktree remove $WorktreePath
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" worktree prune
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" pull --ff-only origin main
```

### Linux / macOS Bash

```bash
git -C "$REPO_ROOT" worktree remove "$WORKTREE_PATH"
git -C "$REPO_ROOT" worktree prune
git -C "$REPO_ROOT" pull --ff-only origin main
```
## Task Evidence

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-DT013-final-build-task-impact-review.md`.
