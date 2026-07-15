# RAG-BT007: Add Source Registry Schema Validation

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-BT007` |
| Task Name | Add Source Registry Schema Validation |
| Build Stage | 01-ingestion - Ingestion |
| Source Question | RAG-Q013, RAG-Q006 |
| Decision / ADR | ADR-RAG-0005, ADR-RAG-0013, RAG-DT004, RAG-DT008, RAG-DT013 |
| Design Dependencies | RAG-DT004, RAG-DT008, RAG-DT013 |
| Depends On Build Tasks | see section 1 and section 3 |
| Branch | `codex/rag-bt007-source-registry-validation` |
| Worktree Path | `C:\tmp\rag-bt007-source-registry-validation` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `build-evidence/RAG-BT007-source-registry-validation.md` |

## Mandatory Execution Contract

This task follows `build-sequence/00-governance/`. Its matching execution record
must be maintained at the Evidence path above. Run one PowerShell command per
block, use the canonical Windows/Python command conventions, and record the
exact checks and results in the evidence file. The pre-PR evidence gate is
mandatory; `Complete` requires merged closeout, clean `main`, and worktree
cleanup.


## 1. Task Definition

Build: source registry validation.

Goal: validate KB source registry entries before ingestion can use them.

Module: `knowledge_base/registry/ and app/stages/stage_01_ingestion/`.

Design Gates:

- `RAG-DT004`
- `RAG-DT008`
- `RAG-DT013`

Acceptance Criteria:

- registry schema exists
- valid sample source passes validation
- missing required fields fail deterministically
- invalid source status fails deterministically
- legacy audit rows default to non-retrieval-eligible unless promoted

Out Of Scope:

- ingesting source content
- scraping sources

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
$TaskId = "rag-bt007"
$Slug = "source-registry-validation"
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
TASK_ID="rag-bt007"
SLUG="source-registry-validation"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```

## 3. Test Code

Write the failing test or acceptance check first. If a design dependency changes
this task, update this section before implementation starts.

Primary test or acceptance path:

```text
pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/tests/test_source_registry.py
```

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/tests/test_source_registry.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@(
  '# RAG-BT007 failing test placeholder',
  '# Replace this placeholder with the task-specific failing test after design gates are complete.',
  'def test_source_registry_validation():',
  '    assert False, "Implement RAG-BT007 after design dependencies are confirmed"'
) | Set-Content -Path $TestPath -Encoding utf8NoBOM
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/tests/test_source_registry.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
# RAG-BT007 failing test placeholder
# Replace this placeholder with the task-specific failing test after design gates are complete.
def test_source_registry_validation():
    assert False, "Implement RAG-BT007 after design dependencies are confirmed"
EOF
```

Expected initial failure:

```text
The test or acceptance check fails because source registry validation is not implemented yet.
```

## 4. Implementation

Implement only after the failing test or acceptance check exists.

Target implementation artifacts:

- `pilot_phase2_poc/rag-service/knowledge_base/registry/source_registry.schema.json`
- `pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/source_registry.py`

### Windows PowerShell Implementation File Preparation

```powershell
$PrimaryImplPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/knowledge_base/registry/source_registry.schema.json"
New-Item -ItemType Directory -Force -Path (Split-Path $PrimaryImplPath) | Out-Null
# Create or update the implementation artifacts for RAG-BT007:
# pilot_phase2_poc/rag-service/knowledge_base/registry/source_registry.schema.json; pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/source_registry.py
```

### Linux / macOS Bash Implementation File Preparation

```bash
PRIMARY_IMPL_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/knowledge_base/registry/source_registry.schema.json"
mkdir -p "$(dirname "$PRIMARY_IMPL_PATH")"
# Create or update the implementation artifacts for RAG-BT007:
# pilot_phase2_poc/rag-service/knowledge_base/registry/source_registry.schema.json; pilot_phase2_poc/rag-service/app/stages/stage_01_ingestion/source_registry.py
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
uv run python -m pytest "app/stages/stage_01_ingestion/tests/test_source_registry.py" -q
uv run python -m pytest -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run python -m pytest "app/stages/stage_01_ingestion/tests/test_source_registry.py" -q
uv run python -m pytest -q
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
git -C $WorktreePath commit -m "build(rag): implement rag-bt007 source-registry-validation"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): implement rag-bt007 source-registry-validation"
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
CI/CD also runs successfully, then clean up the worktree.

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
