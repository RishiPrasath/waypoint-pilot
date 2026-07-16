# RAG-DT011: Define Docker And Local Ops Design

Status: Deferred

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-DT011` |
| Task Name | Define Docker And Local Ops Design |
| Design Lane | 05-runtime-technical-design |
| Source Question | Docker/local ops and CI design |
| Decision / ADR | ADR-RAG-0010, ADR-RAG-0011 |
| Related Planning Docs | `02-rag-db/planning/definition-of-done.md`, `02-rag-db/planning/cicd-pipeline-proposal.md` |
| Affected Build Tasks | RAG-BT020, RAG-BT021, RAG-BT022, RAG-BT004 |
| Branch | `codex/rag-dt011-docker-local-ops-design` |
| Worktree Path | `C:\tmp\rag-dt011-docker-local-ops-design` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Deferred |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT011-docker-local-ops-design.md` |

## 1. Task Definition

Design: define Docker/local ops design when deployment/local runtime scope is
ready.

Goal: avoid overbuilding deployment before the environment is decided, while
still preparing a local runnable path.

Output Artifact:

```text
docs/design/docker-local-ops.md
```

Acceptance Criteria:

- app Docker scope is defined
- Qdrant Docker dependency is defined
- broader Docker/local runtime scope consumes the test-vector-DB strategy from
  `RAG-DT014`
- distinction between unit tests and integration tests is defined
- environment variables are listed
- health/readiness checks are defined
- logs and seed commands are described

Out Of Scope:

- cloud deployment
- Kubernetes

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt011"
$Slug = "docker-local-ops-design"
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
TASK_ID="rag-dt011"
SLUG="docker-local-ops-design"
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
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\docker-local-ops.md" -Pattern "Docker|Qdrant|integration|health|logs"
```

## 4. Design Work

Define local Docker and ops design only when this deferred task is activated.

Use `RAG-DT014` as the single owner of the Qdrant test vector DB and CI
integration-test strategy. This task should not re-decide the service-container
vs Docker Compose test approach unless `RAG-DT014` is explicitly reopened.

The design must answer how local Docker and broader ops will consume the test
DB decision:

- how the app container, Qdrant dependency, and local developer commands fit
  together
- what collection/bootstrap/seed step is required for integration tests
- which tests stay pure unit tests and which tests require Dockerized services
- how health/readiness checks prove the service and Qdrant are available
- whether Docker image build, container smoke test, and Trivy scan belong in
  this task or a later readiness task

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT020, RAG-BT021, RAG-BT022, RAG-BT004

Required Updates:

- Update Docker/Compose scope, CI Docker stage assumptions,
  health/readiness smoke checks, and ops notes based on the `RAG-DT014` test
  vector DB decision.

Deferred Impact:

- Deferred until Docker/local runtime scope is activated.

Impact Review Status:

- Deferred until this design task is activated; then pending RAG-DT013 review.

## 6. Verification

Review with CI/CD Engineer and Security Reviewer.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt011 docker-local-ops-design"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt011 docker-local-ops-design"
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

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-DT011-docker-local-ops-design.md`.
