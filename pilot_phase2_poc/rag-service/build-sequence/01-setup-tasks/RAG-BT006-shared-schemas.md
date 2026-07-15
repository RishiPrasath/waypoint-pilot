# RAG-BT006: Add Shared Schemas And Error Envelope

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-BT006` |
| Task Name | Add Shared Schemas And Error Envelope |
| Source Question | API response schema and validation |
| Decision / ADR | ADR-RAG-0001, ADR-RAG-0011 |
| Branch | `codex/rag-bt006-shared-schemas` |
| Worktree Path | `C:\tmp\rag-bt006-shared-schemas` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `build-evidence/RAG-BT006-shared-schemas.md` |

## Mandatory Execution Contract

This task follows `build-sequence/00-governance/`. Its matching execution record
must be maintained at the Evidence path above. Run one PowerShell command per
block, use the canonical Windows/Python command conventions, and record the
exact checks and results in the evidence file. The pre-PR evidence gate is
mandatory; `Complete` requires merged closeout, clean `main`, and worktree
cleanup.


## 1. Task Definition

Build: shared response schemas and error envelope.

Goal: provide stable response/error models before endpoint and generation work.

Module: `app/shared/schemas/` and `app/shared/errors/`.

Acceptance Criteria:

- base error model validates required fields
- response version field exists if accepted by design
- validation tests pass

Out Of Scope:

- `/api/v1/query`
- generated answer schema finalization if not designed yet

## 2. Worktree And Branch Setup

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt006"
$Slug = "shared-schemas"
$Branch = "codex/$TaskId-$Slug"
$WorktreePath = Join-Path $WorktreeRoot "$TaskId-$Slug"
New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null
git -C $RepoRoot fetch origin
git -C $RepoRoot worktree add -b $Branch $WorktreePath origin/main
git -C $WorktreePath status --short --branch
```

### Linux / macOS Bash

```bash
REPO_ROOT="$HOME/code/waypoint-pilot"
WORKTREE_ROOT="$HOME/code/waypoint-pilot-worktrees"
TASK_ID="rag-bt006"
SLUG="shared-schemas"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"
mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```

## 3. Test Code

Expected failing reason before implementation: `ErrorResponse` is not
implemented.

### Windows PowerShell Test File Creation

```powershell
$TestPath = "$WorktreePath\pilot_phase2_poc\rag-service\app\shared\tests\test_error_schema.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@'
from app.shared.errors.schemas import ErrorResponse


def test_error_response_requires_code_and_message():
    error = ErrorResponse(error_code="bad_request", message="Invalid request")

    assert error.error_code == "bad_request"
    assert error.message == "Invalid request"
'@ | Set-Content -Path $TestPath -Encoding utf8NoBOM
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/shared/tests/test_error_schema.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
from app.shared.errors.schemas import ErrorResponse


def test_error_response_requires_code_and_message():
    error = ErrorResponse(error_code="bad_request", message="Invalid request")

    assert error.error_code == "bad_request"
    assert error.message == "Invalid request"
EOF
```

## 4. Implementation

Add shared Pydantic schemas and error models.

### Windows PowerShell Implementation File Creation

```powershell
$SchemaPath = "$WorktreePath\pilot_phase2_poc\rag-service\app\shared\errors\schemas.py"
New-Item -ItemType Directory -Force -Path (Split-Path $SchemaPath) | Out-Null
@'
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error_code: str
    message: str
'@ | Set-Content -Path $SchemaPath -Encoding utf8NoBOM
```

### Linux / macOS Bash Implementation File Creation

```bash
SCHEMA_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/shared/errors/schemas.py"
mkdir -p "$(dirname "$SCHEMA_PATH")"
cat > "$SCHEMA_PATH" <<'EOF'
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error_code: str
    message: str
EOF
```

## 5. Test Execution

### Windows PowerShell

```powershell
cd "$WorktreePath\pilot_phase2_poc\rag-service"
uv run python -m pytest app/shared/tests -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run python -m pytest app/shared/tests -q
```

## 6. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "feat(rag): add shared error schemas"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "feat(rag): add shared error schemas"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to `main`.

## 7. Merge

Merge after review and CI. Then clean up the worktree.

## 8. Task Evidence

Branch:
Worktree:
PR:
Commit:

Files Changed:
-

Tests Run:
-

CI Result:

AI Review Findings:
-

Human Review Notes:
-

Issues Encountered:
-

Resolution:
-

Debt / Follow-Ups:
-
