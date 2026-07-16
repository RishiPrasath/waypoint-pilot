# RAG-BT002: Add Health Endpoint

Status: Complete

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT002` |
| Task Name | Add Health Endpoint |
| Source Question | Codebase setup and local runnable increments |
| Decision / ADR | ADR-RAG-0001, ADR-RAG-0011 |
| Branch | `codex/rag-bt002-health-endpoint` |
| Worktree Path | `C:\tmp\rag-bt002-health-endpoint` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Complete |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT002-health-endpoint.md` |

## 1. Task Definition

Build: `/health` endpoint.

Goal: expose a simple route proving the app process is alive.

Module: `app/api/health.py`.

Acceptance Criteria:

- `GET /health` returns HTTP 200
- response body equals `{"status": "ok"}`
- route is registered in `app/main.py`

Out Of Scope:

- dependency readiness checks
- Qdrant checks
- LLM provider checks

## 2. Worktree And Branch Setup

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt002"
$Slug = "health-endpoint"
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
TASK_ID="rag-bt002"
SLUG="health-endpoint"
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

Expected failing reason before implementation: `/health` route is not
registered.

### Windows PowerShell Test File Creation

```powershell
$TestPath = "$WorktreePath\pilot_phase2_poc\rag-service\app\api\tests\test_health.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@'
from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_ok():
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
'@ | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/api/tests/test_health.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_ok():
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
EOF
```

## 4. Implementation

Add a health router and include it in the app.

### Windows PowerShell Implementation File Creation

```powershell
$HealthPath = "$WorktreePath\pilot_phase2_poc\rag-service\app\api\health.py"
@'
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
'@ | Set-Content -Path $HealthPath -Encoding UTF8
```

Register the router in `app/main.py`.

### Linux / macOS Bash Implementation File Creation

```bash
HEALTH_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/api/health.py"
cat > "$HEALTH_PATH" <<'EOF'
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
EOF
```

Register the router in `app/main.py`.

## 5. Test Execution

### Windows PowerShell

```powershell
cd "$WorktreePath\pilot_phase2_poc\rag-service"
uv run pytest app/api/tests/test_health.py -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest app/api/tests/test_health.py -q
```

## 6. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "feat(rag): add health endpoint"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "feat(rag): add health endpoint"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to `main`.

## 7. Merge

Merge after PR CI/CD and `main` CI/CD pass. Then clean up the worktree,
delete the merged local branch, and delete the merged remote branch when
permitted.

## Task Evidence

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-BT002-health-endpoint.md`.
