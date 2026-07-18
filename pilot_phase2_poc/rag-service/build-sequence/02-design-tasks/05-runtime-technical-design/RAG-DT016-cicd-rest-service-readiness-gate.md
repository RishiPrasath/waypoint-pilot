# RAG-DT016: CI/CD And REST Service Readiness Gate

Status: In Review

## Sequence Entry

Start from `build-sequence/00-index.md`, then open the design lane index before
opening this task file. Task files should follow the canonical template in
`build-sequence/00-governance/01-task-template.md`.

| Field | Value |
|---|---|
| Task ID | `RAG-DT016` |
| Task Name | CI/CD And REST Service Readiness Gate |
| Design Lane | 05-runtime-technical-design |
| Source Question | CI/CD readiness before final build task impact review |
| Decision / ADR | ADR-RAG-0010, ADR-RAG-0011, RAG-DT014, RAG-DT011 |
| Related Planning Docs | `build-sequence/00-index.md`, `build-sequence/01-setup-tasks/RAG-BT004-stage-1-ci.md`, `build-sequence/02-design-tasks/05-runtime-technical-design/RAG-DT014-test-vector-db-ci-strategy.md` |
| Affected Build Tasks | RAG-BT004, RAG-BT010, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT018, RAG-BT019, RAG-BT020, and any task that relies on CI/CD gates |
| Branch | `codex/rag-dt016-cicd-rest-readiness-gate` |
| Worktree Path | `C:\tmp\rag-dt016-cicd-rest-readiness-gate` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | In Review |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT016-cicd-rest-service-readiness-gate.md` |

## 1. Task Definition

Design and build-readiness gate: audit the complete RAG service CI/CD
environment, identify gaps, implement the necessary CI/CD fixes, and prove the
pipeline works before `RAG-DT013` performs the final build task impact review.

Goal: do not begin final RAG implementation with a weak or unproven CI/CD
runway.

Output Artifacts:

```text
docs/design/cicd-rest-service-readiness-gate.md
docs/design/experiments/cicd-rest-readiness/dt016-run-001/readiness-audit.md
docs/design/experiments/cicd-rest-readiness/dt016-run-001/implemented-gaps.md
docs/design/experiments/cicd-rest-readiness/dt016-run-001/decision-gate.md
build-evidence/RAG-DT016-cicd-rest-service-readiness-gate.md
```

Allowed Implementation Scope:

- GitHub Actions workflow files.
- CI helper scripts or documented commands.
- pytest marker/config updates needed for CI parity.
- lightweight REST service tests that exercise already-built endpoints.
- Docker/Qdrant CI job wiring only when it matches accepted `RAG-DT014` and
  available implementation state.

Out Of Scope:

- new RAG runtime behavior such as ingestion, retrieval, generation, or
  evaluation implementation;
- production deployment;
- cloud infrastructure;
- changing the accepted vector DB strategy from `RAG-DT014`.

Acceptance Criteria:

- current GitHub Actions workflows are audited;
- local service commands are audited;
- current FastAPI/REST surface is audited against already-built endpoints;
- current pytest, ruff, bandit, pip-audit, CodeQL, Dependabot, and secret
  scanning posture is checked where applicable;
- Docker Desktop/local Docker ability is checked when relevant;
- accepted `RAG-DT014` three-layer vector DB test strategy is mapped onto CI/CD:
  in-memory fast checks, local Docker/Compose pre-push checks, GitHub Actions
  Qdrant service-container checks;
- gaps are listed with severity, affected build tasks, and owner decision;
- necessary CI/CD gaps are implemented in the same task branch;
- implemented gaps are proven locally and, where applicable, in GitHub Actions;
- any deferred gap has a reason, owner signoff, and downstream task impact;
- final readiness gate says either `Pass`, `Pass With Deferred Items`, or
  `Fail`;
- `RAG-DT013` is blocked until this gate is complete.

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing readiness artifacts.
Do not write task changes directly on `main`.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt016"
$Slug = "cicd-rest-readiness-gate"
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
TASK_ID="rag-dt016"
SLUG="cicd-rest-readiness-gate"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```

## 3. Acceptance Check

Run these checks before making changes so the task starts from the real repo
state:

### Windows PowerShell

```powershell
$ServiceRoot = Join-Path $WorktreePath "pilot_phase2_poc\rag-service"
Set-Location $ServiceRoot

Get-ChildItem -Path "$WorktreePath\.github\workflows" -Filter "*.yml" -ErrorAction SilentlyContinue
Get-ChildItem -Path "$WorktreePath\.github\workflows" -Filter "*.yaml" -ErrorAction SilentlyContinue
Test-Path "$ServiceRoot\pyproject.toml"
Test-Path "$ServiceRoot\app\main.py"
uv run python -m pytest -q
uv run ruff check .
uv run bandit -c pyproject.toml -r app
uv run pip-audit
docker --version
docker compose version
docker info --format '{{.ServerVersion}}'
```

Record every result in the evidence file. If Docker is not running, record
whether Docker Desktop can be started from the command line and whether the
daemon becomes ready.

Expected baseline:

- unit tests should pass from the service root;
- lint/static/security checks should either pass or produce concrete gaps to
  fix in this task;
- Docker/Qdrant checks may be advisory until the accepted local ops design and
  relevant retrieval implementation exist.

## 4. Design And Implementation Work

### 4.1 Audit The Existing CI/CD Surface

Inspect and document:

- workflow files under `.github/workflows/`;
- Dependabot configuration;
- CodeQL/security workflow configuration;
- `pyproject.toml` pytest, ruff, bandit, and dependency groups;
- existing service endpoints and tests;
- current build-sequence CI expectations from `RAG-BT004`, `RAG-DT014`, and
  `RAG-DT011`;
- whether GitHub Actions currently runs on PR and `main`;
- whether CI failures are visible and actionable.

### 4.2 Audit The REST Service Test Surface

List the REST service checks that should exist before final RAG implementation:

- app import smoke test;
- health endpoint test;
- readiness endpoint test;
- error envelope/schema checks, if already implemented;
- config/settings checks, if already implemented;
- no accidental dependency on legacy KB material;
- no accidental need for Docker in the default unit-test path.

Do not implement missing business/RAG endpoints here. If an endpoint belongs to
a later build task, mark it as a downstream requirement rather than building it
early.

### 4.3 Define Required CI/CD Layers

The readiness gate should assess these layers:

```text
Layer 1: Python environment and dependency install
Layer 2: fast unit/API tests
Layer 3: lint/static checks
Layer 4: security/dependency checks
Layer 5: Docker/Qdrant integration checks from RAG-DT014
Layer 6: Docker image build and container smoke checks
Layer 7: post-merge main verification
```

Classify each layer as:

```text
Implemented and passing
Implemented but failing
Missing and required now
Missing but correctly deferred
Not applicable yet
```

### 4.4 Implement Required Gaps

Implement gaps that are required before `RAG-DT013` can safely approve final
build tasks. Examples:

- add or repair GitHub Actions workflow jobs for service-root tests;
- add missing pytest marker registration;
- align workflow commands with `uv run python -m pytest -q`;
- add ruff/bandit/pip-audit jobs if Stage 1 CI expects them;
- ensure workflow working directory is `pilot_phase2_poc/rag-service`;
- add artifact/log capture for CI failures if practical;
- add advisory/manual Qdrant integration workflow shape when code is not ready
  for required service-backed tests yet;
- document exact local commands that mirror CI.

Do not overbuild. If a gap depends on future runtime code, document it as
deferred and add the handoff requirement to the affected build task.

### 4.5 Prove The Implemented Gaps

For every implemented gap, record:

- file changed;
- reason;
- local command used;
- local result;
- PR CI result, check name, and URL or run identifier when available;
- whether it should become required before merge now or later.

## 5. Build Task Impact

Affected Build Tasks:

- `RAG-BT004`: Stage 1 CI expectations may need correction or expansion.
- `RAG-BT010`: Qdrant wrapper smoke tests must align with CI markers and
  service-container strategy.
- `RAG-BT012`: fixture ingestion must know when Qdrant integration becomes
  required.
- `RAG-BT013`: semantic retrieval acceptance must use the proven CI gate.
- `RAG-BT014`: hybrid retrieval acceptance must use the proven CI gate.
- `RAG-BT018`: generation/API integration must not assume an untested service
  pipeline.
- `RAG-BT019`: evaluation harness must separate unit/mock checks from
  Qdrant-backed CI checks.
- `RAG-BT020`: Docker/local run must consume the proven local/CI split.

Required Updates:

- Add CI/CD readiness handoff blocks to affected build tasks where this task
  changes acceptance criteria or commands.
- Mark whether Qdrant integration is required immediately, advisory, or
  deferred until a specific build task exists.
- Ensure final build task files do not claim a CI job exists until this task
  proves it.

Deferred Impact:

- production deployment pipeline remains out of scope;
- cloud infrastructure remains out of scope;
- full container image security scanning may be deferred until Docker image
  build exists, but the deferral must be explicit.

Impact Review Status:

- Pending `RAG-DT013` review after this task is complete.

## 6. Verification

Minimum local verification:

### Windows PowerShell

```powershell
$ServiceRoot = Join-Path $WorktreePath "pilot_phase2_poc\rag-service"
Set-Location $ServiceRoot

uv run python -m pytest -q
uv run ruff check .
uv run bandit -c pyproject.toml -r app
uv run pip-audit
git -C $WorktreePath diff --check
```

Required artifact checks:

```powershell
Test-Path "$ServiceRoot\docs\design\cicd-rest-service-readiness-gate.md"
Test-Path "$ServiceRoot\docs\design\experiments\cicd-rest-readiness\dt016-run-001\readiness-audit.md"
Test-Path "$ServiceRoot\docs\design\experiments\cicd-rest-readiness\dt016-run-001\implemented-gaps.md"
Test-Path "$ServiceRoot\docs\design\experiments\cicd-rest-readiness\dt016-run-001\decision-gate.md"
Test-Path "$ServiceRoot\build-evidence\RAG-DT016-cicd-rest-service-readiness-gate.md"
Select-String -Path "$ServiceRoot\build-sequence\02-design-tasks\00-index.md" -Pattern "RAG-DT016.*In Review|RAG-DT016.*Complete"
```

PR verification:

- open a PR from the task branch;
- wait for GitHub Actions checks;
- record each check status in evidence;
- fix CI failures that belong to this task;
- do not mark the task complete if required CI/CD gaps remain unimplemented or
  unproven.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service .github
git -C $WorktreePath commit -m "docs(rag): add cicd rest readiness gate task"
git -C $WorktreePath push -u origin $Branch
```

Open a PR to `main`.

## 8. Merge

Merge only after review and required checks pass. Then clean up the worktree,
delete the merged local branch, and delete the merged remote branch when
permitted.

Record:

- PR URL;
- CI result before merge;
- merge commit;
- `main` CI/CD result after merge;
- unresolved risks;
- follow-up debt entries, if any.

## Task Evidence

Evidence must be recorded in
`pilot_phase2_poc/rag-service/build-evidence/RAG-DT016-cicd-rest-service-readiness-gate.md`.
