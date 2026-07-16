# RAG-BT003: Add Readiness Endpoint

Status: Complete

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT003` |
| Task Name | Add Readiness Endpoint |
| Source Question | Codebase setup and local runnable increments |
| Decision / ADR | ADR-RAG-0011 |
| Branch | `codex/rag-bt003-readiness-endpoint` |
| Worktree Path | `C:\tmp\rag-bt003-readiness-endpoint` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Complete |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT003-readiness-endpoint.md` |

## 1. Task Definition

Build: `/ready` endpoint.

Goal: expose a route for local readiness without checking unavailable external
systems yet.

Module: `app/api/ready.py` or `app/api/health.py`.

Acceptance Criteria:

- `GET /ready` returns HTTP 200 for the default local app
- response includes readiness status
- future dependency checks can be added without changing route shape

Out Of Scope:

- real Qdrant readiness
- real LLM provider readiness

## 2. Worktree And Branch Setup

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt003"
$Slug = "readiness-endpoint"
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
TASK_ID="rag-bt003"
SLUG="readiness-endpoint"
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

Expected failing reason before implementation: `/ready` route is not
registered.

### Windows PowerShell Test File Creation

```powershell
$TestPath = "$WorktreePath\pilot_phase2_poc\rag-service\app\api\tests\test_ready.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@'
from fastapi.testclient import TestClient

from app.main import app


def test_ready_endpoint_returns_ready():
    response = TestClient(app).get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
'@ | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/api/tests/test_ready.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
from fastapi.testclient import TestClient

from app.main import app


def test_ready_endpoint_returns_ready():
    response = TestClient(app).get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
EOF
```

## 4. Implementation

Add readiness route and register it.

### Windows PowerShell Implementation File Creation

```powershell
$ReadyPath = "$WorktreePath\pilot_phase2_poc\rag-service\app\api\ready.py"
@'
from fastapi import APIRouter

router = APIRouter()


@router.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}
'@ | Set-Content -Path $ReadyPath -Encoding UTF8
```

### Linux / macOS Bash Implementation File Creation

```bash
READY_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/api/ready.py"
cat > "$READY_PATH" <<'EOF'
from fastapi import APIRouter

router = APIRouter()


@router.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}
EOF
```

## 5. Test Execution

### Windows PowerShell

```powershell
cd "$WorktreePath\pilot_phase2_poc\rag-service"
uv run pytest app/api/tests/test_ready.py -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest app/api/tests/test_ready.py -q
```

## 6. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "feat(rag): add readiness endpoint"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "feat(rag): add readiness endpoint"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to `main`.

## 7. Merge

Merge after review, PR CI/CD, and `main` CI/CD. Then clean up the worktree,
delete the merged local branch, and delete the merged remote branch when
permitted.

## Task Evidence

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-BT003-readiness-endpoint.md`.
