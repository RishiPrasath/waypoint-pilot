# RAG-BT009: Add Chunking Rules And Fixture Harness

Status: Planned

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT009` |
| Task Name | Add Chunking Rules And Fixture Harness |
| Build Stage | 01-ingestion - Ingestion |
| Source Question | RAG-Q011 |
| Decision / ADR | RAG-DT002, RAG-DT005, RAG-DT012, RAG-DT013 |
| Design Dependencies | RAG-DT002, RAG-DT005, RAG-DT012, RAG-DT013 |
| Depends On Build Tasks | see section 1 and section 3 |
| Branch | `codex/rag-bt009-chunking-fixture-harness` |
| Worktree Path | `C:\tmp\rag-bt009-chunking-fixture-harness` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT009-chunking-fixture-harness.md` |

## 1. Task Definition

Build: chunking rules and fixture harness.

Goal: make chunking behavior deterministic and testable before ingestion depends on it.

Module: `app/stages/stage_01_ingestion/chunkers/`.

Design Gates:

- `RAG-DT002`
- `RAG-DT005`
- `RAG-DT012`
- `RAG-DT013`

Acceptance Criteria:

- representative fixture source exists
- chunking function produces stable chunk IDs
- chunks preserve source metadata
- comparison report or fixture assertion records chosen rules
- legacy files are not treated as final chunking sources unless promoted

Out Of Scope:

- production ingestion pipeline
- final embedding model lock

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
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt009"
$Slug = "chunking-fixture-harness"
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
TASK_ID="rag-bt009"
SLUG="chunking-fixture-harness"
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
pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/tests/test_chunking.py
```

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/tests/test_chunking.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@(
  '# RAG-BT009 failing test placeholder',
  '# Replace this placeholder with the task-specific failing test after design gates are complete.',
  'def test_chunking_fixture_harness():',
  '    assert False, "Implement RAG-BT009 after design dependencies are confirmed"'
) | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/tests/test_chunking.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
# RAG-BT009 failing test placeholder
# Replace this placeholder with the task-specific failing test after design gates are complete.
def test_chunking_fixture_harness():
    assert False, "Implement RAG-BT009 after design dependencies are confirmed"
EOF
```

Expected initial failure:

```text
The test or acceptance check fails because chunking rules and fixture harness is not implemented yet.
```

## 4. Implementation

Implement only after the failing test or acceptance check exists.

Target implementation artifacts:

- `pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/chunkers/rules.py`
- `pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/chunkers/service.py`
- `pilot_phase2_poc/rag-service/docs/design/chunking-experiment.md`

### Windows PowerShell Implementation File Preparation

```powershell
$PrimaryImplPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/chunkers/rules.py"
New-Item -ItemType Directory -Force -Path (Split-Path $PrimaryImplPath) | Out-Null
# Create or update the implementation artifacts for RAG-BT009:
# pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/chunkers/rules.py; pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/chunkers/service.py; pilot_phase2_poc/rag-service/docs/design/chunking-experiment.md
```

### Linux / macOS Bash Implementation File Preparation

```bash
PRIMARY_IMPL_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/chunkers/rules.py"
mkdir -p "$(dirname "$PRIMARY_IMPL_PATH")"
# Create or update the implementation artifacts for RAG-BT009:
# pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/chunkers/rules.py; pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/chunkers/service.py; pilot_phase2_poc/rag-service/docs/design/chunking-experiment.md
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
uv run pytest "app/stages/stage_01_ingestion/tests/test_chunking.py" -q
uv run pytest -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest "app/stages/stage_01_ingestion/tests/test_chunking.py" -q
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
git -C $WorktreePath commit -m "build(rag): implement rag-bt009 chunking-fixture-harness"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): implement rag-bt009 chunking-fixture-harness"
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

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-BT009-chunking-fixture-harness.md`.
