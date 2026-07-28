# RAG-BT020: Add Docker Local Run

Status: Planned

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT020` |
| Task Name | Add Docker Local Run |
| Build Stage | 06-ops-readiness - Ops Readiness |
| Source Question | RAG-Q019 |
| Decision / ADR | ADR-RAG-0010, ADR-RAG-0011, RAG-DT004, RAG-DT011, RAG-DT013 |
| Design Dependencies | RAG-DT004, RAG-DT011, RAG-DT014, RAG-DT021, RAG-DT023, RAG-DT025, RAG-DT013 |
| Depends On Build Tasks | RAG-BT018, RAG-BT023 |
| Branch | `codex/rag-bt020-docker-local-run` |
| Worktree Path | `C:\tmp\rag-bt020-docker-local-run` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT020-docker-local-run.md` |

## 1. Task Definition

Build: Docker/Compose local runnable setup.

Goal: run the FastAPI service and local Qdrant in a hardened local PoC
environment without implying production deployment readiness.

Module: `Dockerfile, docker-compose.yml, and docs/ops/`.

Design Gates:

- `RAG-DT004`
- `RAG-DT011`
- `RAG-DT014`
- `RAG-DT013`

DT014 Vector DB Test Handoff:

- Qdrant SDK/test-service ownership has moved to `RAG-BT023`. Consume its
  accepted test profile and CI evidence; do not create a competing collection
  lifecycle or integration environment here.
- Local command: `docker compose --profile test up -d qdrant`, then
  `uv run python -m pytest -m integration -q`, then
  `docker compose --profile test down`.
- CI command: GitHub Actions Qdrant service container plus
  `uv run python -m pytest -m integration -q`; Docker image build/smoke may be
  a separate CI job.
- Pytest marker: `integration`.
- Required environment variables: `QDRANT_URL`,
  `QDRANT_COLLECTION_PREFIX`, `QDRANT_TEST_TIMEOUT_SECONDS`,
  `RUN_QDRANT_INTEGRATION`; `QDRANT_API_KEY` optional and unset for isolated
  local/CI containers.
- Collection naming rule: `rag_test_rag_bt020_<run_id>` for ops smoke tests.
- Seed fixture: minimal Qdrant smoke fixture plus optional BT012/BT013 seeded
  fixture when retrieval integration exists.
- Payload contract: smoke fixture must include the standard DT014 lineage and
  vector contract fields.
- Cleanup rule: `docker compose --profile test down` must remove the Qdrant
  test service, and tests must delete task-owned collections.
- CI gate timing: Compose/local ops validates local reproduction; GitHub
  Actions service container remains the PR integration gate.

DT011 Docker/Local Ops Handoff:

- Implement `Dockerfile`, `docker-compose.yml`, `.dockerignore`, and
  `docs/ops/local-docker-run.md`.
- Default fast checks remain host-run and Docker-free:
  `uv run python -m pytest -q`.
- Compose must support a Qdrant-only local integration path:
  `docker compose --profile test up -d qdrant`.
- Compose must support an app runtime smoke path:
  `docker compose --profile app up --build`.
- App container must expose port `8000` and run `app.main:app` with Uvicorn.
- App container smoke must check `/health` and dependency-aware `/ready`.
- Do not use the current static-success `/ready` implementation as integration
  evidence. DT023/DT025 must assign the dependency-aware readiness change to an
  executable build task before BT020 begins.
- Qdrant readiness must use `/readyz`; verify the selected healthcheck command
  works in the chosen Qdrant image before relying on it.
- Bind Qdrant's published HTTP port to `127.0.0.1`; do not publish `6334`
  unless a task proves it is required. Unauthenticated Qdrant is allowed only
  for an isolated local/CI profile.
- Pin base and Qdrant images by immutable digest, run the app as a non-root
  user, and use a production-only/multi-stage app image.
- Container logs must be available through
  `docker compose logs --tail 100 rag-service` and
  `docker compose logs --tail 100 qdrant`.
- `.dockerignore` must exclude `.venv`, caches, local secrets, `.env` files,
  and unrelated repo material.
- Do not mount `legacy/phase1-kb-snapshot/` as runtime KB input.
- Docker image build and container smoke may join CI only after `RAG-DT016`
  approves or implements the relevant CI gate.

DT016 CI/CD Readiness Handoff:

- When Dockerfile and Compose exist, extend `rag-service` CI with Docker image
  build and container smoke checks.
- Add container vulnerability scanning and an SBOM when the image target
  exists; do not permit BT022 to pass while they are silently deferred.
- Container smoke must call app `/health`, app `/ready`, and Qdrant `/readyz`.
- Preserve the default non-Docker CI job even after Docker jobs are added.
- If Docker jobs are deferred, record the reason in BT020 evidence and the
  production-readiness review.

Acceptance Criteria:

- Docker image builds
- Compose starts service and Qdrant
- /health passes through Docker
- CI can build the Docker image after Docker files exist
- CI can run a container smoke test or record why it is deferred
- integration test command can run against Dockerized Qdrant
- config uses environment variables
- Qdrant ports are loopback-bound and image references are immutable
- app image runs non-root and container scan/SBOM evidence exists

Out Of Scope:

- cloud deployment
- Kubernetes

DT004 KB Path Contract:

- Local Docker/Compose volumes may mount `knowledge_base/` but must not mount `legacy/` as runtime KB input.
- Runtime config must point to the registry under `knowledge_base/registry/`.
- Container smoke tests must use approved fixture/canonical material or explicitly mocked KB input.

## 2. Worktree And Branch Setup

Create the branch and worktree before creating tests or implementation files.
Do not write task code directly on `main`.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt020"
$Slug = "docker-local-run"
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
TASK_ID="rag-bt020"
SLUG="docker-local-run"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
git -C "$REPO_ROOT" config core.longpaths true
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```

## 3. Test Code

Write the failing test or acceptance check first. If a design dependency changes
this task, update this section before implementation starts.

Primary test or acceptance path:

```text
pilot_phase2_poc/rag-service/tests/ops/test_docker_compose_contract.py
```

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/tests/ops/test_docker_compose_contract.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@(
  '# RAG-BT020 failing test placeholder',
  '# Replace this placeholder with the task-specific failing test after design gates are complete.',
  'def test_docker_local_run():',
  '    assert False, "Implement RAG-BT020 after design dependencies are confirmed"'
) | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/tests/ops/test_docker_compose_contract.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
# RAG-BT020 failing test placeholder
# Replace this placeholder with the task-specific failing test after design gates are complete.
def test_docker_local_run():
    assert False, "Implement RAG-BT020 after design dependencies are confirmed"
EOF
```

Expected initial failure:

```text
The test or acceptance check fails because Docker/Compose local runnable setup is not implemented yet.
```

## 4. Implementation

Implement only after the failing test or acceptance check exists.

Target implementation artifacts:

- `pilot_phase2_poc/rag-service/Dockerfile`
- `pilot_phase2_poc/rag-service/docker-compose.yml`
- `pilot_phase2_poc/rag-service/docs/ops/local-docker-run.md`

### Windows PowerShell Implementation File Preparation

```powershell
$PrimaryImplPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/Dockerfile"
New-Item -ItemType Directory -Force -Path (Split-Path $PrimaryImplPath) | Out-Null
# Create or update the implementation artifacts for RAG-BT020:
# pilot_phase2_poc/rag-service/Dockerfile; pilot_phase2_poc/rag-service/docker-compose.yml; pilot_phase2_poc/rag-service/docs/ops/local-docker-run.md
```

### Linux / macOS Bash Implementation File Preparation

```bash
PRIMARY_IMPL_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/Dockerfile"
mkdir -p "$(dirname "$PRIMARY_IMPL_PATH")"
# Create or update the implementation artifacts for RAG-BT020:
# pilot_phase2_poc/rag-service/Dockerfile; pilot_phase2_poc/rag-service/docker-compose.yml; pilot_phase2_poc/rag-service/docs/ops/local-docker-run.md
```

Implementation Notes:

- Keep the change limited to this task's module and directly required shared files.
- Keep tests inside the module they verify.
- Update docs when behavior, configuration, schema, or operational evidence changes.
- Record any accepted shortcut in the task evidence and backlog/follow-up notes.

## 5. Test Execution

Run the module-local test first, then the service-level checks available at that
point in the build sequence.

### Windows PowerShell

```powershell
Set-Location "$WorktreePath\pilot_phase2_poc\rag-service"
uv run pytest "tests/ops/test_docker_compose_contract.py" -q
uv run pytest -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest "tests/ops/test_docker_compose_contract.py" -q
uv run pytest -q
```

Record:

- command run
- initial failing result
- fix applied
- final passing result
- any skipped or deferred check with reason

## 6. Branch Workflow

Use the task branch created at the start. Keep the PR small and task-sized.

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "build(rag): implement rag-bt020 docker-local-run"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): implement rag-bt020 docker-local-run"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a pull request to `main`.

Required PR checks:

- CI pipeline runs
- CI passes
- AI scans the diff or PR for bugs, missing tests, security risks, design drift, and unclear code
- human owner reviews the PR
- accepted findings are fixed

## 7. Merge

Merge only after CI passes and the PR is reviewed. After merge, confirm `main`
CI/CD also runs successfully, then clean up the worktree, delete the merged
local branch, and delete the merged remote branch when permitted.

### Windows PowerShell

```powershell
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" worktree remove $WorktreePath
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" worktree prune
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" fetch origin
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" pull --ff-only origin main
```

### Linux / macOS Bash

```bash
git -C "$REPO_ROOT" worktree remove "$WORKTREE_PATH"
git -C "$REPO_ROOT" worktree prune
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
```

Record:

- PR URL
- CI result before merge
- merge commit
- `main` CI/CD result after merge
- unresolved risks
- follow-up debt entries, if any

## Task Evidence

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-BT020-docker-local-run.md`.

## DT013 Final Design Handoff

- Prove app and Qdrant Docker profiles, `/health`, `/ready`, Qdrant readiness, `.dockerignore`, and runtime env handling.
- Ensure Docker/local ops do not mount or ingest `legacy/phase1-kb-snapshot/` as runtime corpus.
- Carry Docker image smoke and container scan proof or explicit deferral into production readiness.
