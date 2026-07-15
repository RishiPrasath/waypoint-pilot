# RAG-BT012: Add Fixture Ingestion Pipeline

Status: Draft

| Field | Value |
|---|---|
| Task ID | `RAG-BT012` |
| Task Name | Add Fixture Ingestion Pipeline |
| Build Stage | 01-ingestion - Ingestion |
| Source Question | RAG-Q011, RAG-Q013 |
| Decision / ADR | RAG-DT004, RAG-DT005, RAG-DT008, RAG-DT012, RAG-DT013 |
| Design Dependencies | RAG-DT004, RAG-DT005, RAG-DT008, RAG-DT012, RAG-DT014, RAG-DT013, RAG-BT010, RAG-BT011 |
| Depends On Build Tasks | see section 1 and section 3 |
| Branch | `codex/rag-bt012-fixture-ingestion-pipeline` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-bt012-fixture-ingestion-pipeline` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Draft |

## 1. Task Definition

Build: fixture ingestion pipeline.

Goal: parse, chunk, embed, and index an approved fixture source through testable boundaries.

Module: `app/stages/stage_01_ingestion/`.

Design Gates:

- `RAG-DT004`
- `RAG-DT005`
- `RAG-DT008`
- `RAG-DT012`
- `RAG-DT014`
- `RAG-DT013`
- `RAG-BT010`
- `RAG-BT011`

Acceptance Criteria:

- fixture source is parsed
- chunks are produced with metadata
- embeddings are generated through adapter
- vector DB wrapper receives upsert calls
- ingestion report is produced
- legacy snapshot is not directly ingestible

Out Of Scope:

- full production scraping
- bulk ingestion of unreviewed KB material

Legacy KB Guardrail:

```text
legacy/phase1-kb-snapshot is audit input only.
It must not be ingested directly.
Only audited/promoted material may become fixture, candidate, or canonical KB content.
```

## 2. Worktree And Branch Setup

Create the branch and worktree before creating tests or implementation files.
Do not write task code directly on `main`.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-bt012"
$Slug = "fixture-ingestion-pipeline"
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
TASK_ID="rag-bt012"
SLUG="fixture-ingestion-pipeline"
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
pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/tests/test_fixture_ingestion.py
```

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/tests/test_fixture_ingestion.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@(
  '# RAG-BT012 failing test placeholder',
  '# Replace this placeholder with the task-specific failing test after design gates are complete.',
  'def test_fixture_ingestion_pipeline():',
  '    assert False, "Implement RAG-BT012 after design dependencies are confirmed"'
) | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/tests/test_fixture_ingestion.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
# RAG-BT012 failing test placeholder
# Replace this placeholder with the task-specific failing test after design gates are complete.
def test_fixture_ingestion_pipeline():
    assert False, "Implement RAG-BT012 after design dependencies are confirmed"
EOF
```

Expected initial failure:

```text
The test or acceptance check fails because fixture ingestion pipeline is not implemented yet.
```

## 4. Implementation

Implement only after the failing test or acceptance check exists.

Target implementation artifacts:

- `pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/service.py`
- `pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/reporting.py`

### Windows PowerShell Implementation File Preparation

```powershell
$PrimaryImplPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/service.py"
New-Item -ItemType Directory -Force -Path (Split-Path $PrimaryImplPath) | Out-Null
# Create or update the implementation artifacts for RAG-BT012:
# pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/service.py; pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/reporting.py
```

### Linux / macOS Bash Implementation File Preparation

```bash
PRIMARY_IMPL_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/service.py"
mkdir -p "$(dirname "$PRIMARY_IMPL_PATH")"
# Create or update the implementation artifacts for RAG-BT012:
# pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/service.py; pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/reporting.py
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
uv run pytest "app/stages/stage_01_ingestion/tests/test_fixture_ingestion.py" -q
uv run pytest -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest "app/stages/stage_01_ingestion/tests/test_fixture_ingestion.py" -q
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
git -C $WorktreePath commit -m "build(rag): implement rag-bt012 fixture-ingestion-pipeline"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): implement rag-bt012 fixture-ingestion-pipeline"
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
