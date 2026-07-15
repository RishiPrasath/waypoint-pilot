# RAG-BT021: Add Observability And Ops Notes

Status: Draft

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.

| Field | Value |
|---|---|
| Task ID | `RAG-BT021` |
| Task Name | Add Observability And Ops Notes |
| Build Stage | 06-ops-readiness - Ops Readiness |
| Source Question | RAG-Q018, engineering defaults |
| Decision / ADR | ADR-RAG-0011, RAG-DT013 |
| Design Dependencies | RAG-BT018, RAG-DT013 |
| Depends On Build Tasks | see section 1 and section 3 |
| Branch | `codex/rag-bt021-observability-ops-notes` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-bt021-observability-ops-notes` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Draft |

## 1. Task Definition

Build: logging, trace IDs, and operational notes.

Goal: make local debugging and future production operation understandable.

Module: `app/core/ and docs/ops/`.

Design Gates:

- `RAG-BT018`
- `RAG-DT013`

Acceptance Criteria:

- query ID exists in request lifecycle
- key failure paths are logged safely
- logs redact secrets
- ops checklist exists

Out Of Scope:

- full telemetry backend
- production alerting

## 2. Worktree And Branch Setup

Create the branch and worktree before creating tests or implementation files.
Do not write task code directly on `main`.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-bt021"
$Slug = "observability-ops-notes"
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
TASK_ID="rag-bt021"
SLUG="observability-ops-notes"
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
pilot_phase2_poc/rag-service/app/core/tests/test_logging.py
```

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/core/tests/test_logging.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@(
  '# RAG-BT021 failing test placeholder',
  '# Replace this placeholder with the task-specific failing test after design gates are complete.',
  'def test_observability_ops_notes():',
  '    assert False, "Implement RAG-BT021 after design dependencies are confirmed"'
) | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/core/tests/test_logging.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
# RAG-BT021 failing test placeholder
# Replace this placeholder with the task-specific failing test after design gates are complete.
def test_observability_ops_notes():
    assert False, "Implement RAG-BT021 after design dependencies are confirmed"
EOF
```

Expected initial failure:

```text
The test or acceptance check fails because logging, trace IDs, and operational notes is not implemented yet.
```

## 4. Implementation

Implement only after the failing test or acceptance check exists.

Target implementation artifacts:

- `pilot_phase2_poc/rag-service/app/core/logging.py`
- `pilot_phase2_poc/rag-service/docs/ops/observability.md`

### Windows PowerShell Implementation File Preparation

```powershell
$PrimaryImplPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/core/logging.py"
New-Item -ItemType Directory -Force -Path (Split-Path $PrimaryImplPath) | Out-Null
# Create or update the implementation artifacts for RAG-BT021:
# pilot_phase2_poc/rag-service/app/core/logging.py; pilot_phase2_poc/rag-service/docs/ops/observability.md
```

### Linux / macOS Bash Implementation File Preparation

```bash
PRIMARY_IMPL_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/core/logging.py"
mkdir -p "$(dirname "$PRIMARY_IMPL_PATH")"
# Create or update the implementation artifacts for RAG-BT021:
# pilot_phase2_poc/rag-service/app/core/logging.py; pilot_phase2_poc/rag-service/docs/ops/observability.md
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
uv run pytest "app/core/tests/test_logging.py" -q
uv run pytest -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest "app/core/tests/test_logging.py" -q
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
git -C $WorktreePath commit -m "build(rag): implement rag-bt021 observability-ops-notes"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): implement rag-bt021 observability-ops-notes"
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

## 8. Task Evidence

Branch:
Worktree:
PR:
Commit:
Merge Commit:

Design Gates Confirmed:
-

Files Changed:
-

Tests Written First:
-

Tests Run:
-

CI Result Before Merge:

Main CI/CD Result After Merge:

AI Review Findings:
-

Human Review Notes:
-

Security Impact:
-

Evaluation Impact:
-

Docker / Seed Data Impact:
-

Issues Encountered:
-

Resolution:
-

Debt / Follow-Ups:
-


