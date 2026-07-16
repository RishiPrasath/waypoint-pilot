# RAG-BT019: Add Evaluation Harness

Status: Planned

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT019` |
| Task Name | Add Evaluation Harness |
| Build Stage | 05-evaluation - Evaluation |
| Source Question | RAG-Q010, RAG-Q023 |
| Decision / ADR | ADR-RAG-0008, RAG-DT004, RAG-DT006, RAG-DT012, RAG-DT013 |
| Design Dependencies | RAG-DT004, RAG-DT006, RAG-DT012, RAG-DT014, RAG-BT018, RAG-DT013 |
| Depends On Build Tasks | see section 1 and section 3 |
| Branch | `codex/rag-bt019-evaluation-harness` |
| Worktree Path | `C:\tmp\rag-bt019-evaluation-harness` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT019-evaluation-harness.md` |

## 1. Task Definition

Build: golden-question evaluation harness.

Goal: run regression checks for retrieval, citations, answer quality, irrelevant queries, and malicious queries.

Module: `app/stages/stage_05_evaluation/`.

Design Gates:

- `RAG-DT004`
- `RAG-DT006`
- `RAG-DT012`
- `RAG-DT014`
- `RAG-BT018`
- `RAG-DT013`

Acceptance Criteria:

- golden question fixture exists
- runner produces pass/fail report
- citation validity is checked
- irrelevant and malicious query cases are included
- legacy examples are not expected sources unless promoted

Out Of Scope:

- large-scale evaluation suite
- manual domain signoff

Legacy KB Guardrail:

```text
legacy/phase1-kb-snapshot is audit input only.
It must not be ingested directly.
Only audited/promoted material may become fixture, candidate, or canonical KB content.
```

DT004 KB Path Contract:

- Golden answers and citation checks must cite approved `canonical/` material or explicitly scoped `reference/` review material.
- Evaluation fixtures may use legacy files only as coverage-gap examples, never as expected runtime sources.
- Evaluation reports must flag any answer that cites `legacy/`, `drop/`, or `archive/` material as a source.

DT012 Evaluation Source Contract:

- Golden-question citations may reference DT012 source-derived candidates only
  when the fixture explicitly records candidate provenance from
  `knowledge_base/snapshots/first-pass-snapshot-manifest.md`.
- Citation validity checks must compare returned source lineage against
  `document_id`, `snapshot_id`, source URI, reuse mode, license sensitivity,
  retrieval eligibility, and candidate SHA-256.
- License-sensitive metadata-only candidates such as `APAC-215` may be used to
  test exclusion behavior, not expected answer content.

## 2. Worktree And Branch Setup

Create the branch and worktree before creating tests or implementation files.
Do not write task code directly on `main`.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt019"
$Slug = "evaluation-harness"
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
TASK_ID="rag-bt019"
SLUG="evaluation-harness"
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
pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/tests/test_evaluation_runner.py
```

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/tests/test_evaluation_runner.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@(
  '# RAG-BT019 failing test placeholder',
  '# Replace this placeholder with the task-specific failing test after design gates are complete.',
  'def test_evaluation_harness():',
  '    assert False, "Implement RAG-BT019 after design dependencies are confirmed"'
) | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/tests/test_evaluation_runner.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
# RAG-BT019 failing test placeholder
# Replace this placeholder with the task-specific failing test after design gates are complete.
def test_evaluation_harness():
    assert False, "Implement RAG-BT019 after design dependencies are confirmed"
EOF
```

Expected initial failure:

```text
The test or acceptance check fails because golden-question evaluation harness is not implemented yet.
```

## 4. Implementation

Implement only after the failing test or acceptance check exists.

Target implementation artifacts:

- `pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/runner.py`
- `pilot_phase2_poc/rag-service/docs/evaluation/golden-questions.md`

### Windows PowerShell Implementation File Preparation

```powershell
$PrimaryImplPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/runner.py"
New-Item -ItemType Directory -Force -Path (Split-Path $PrimaryImplPath) | Out-Null
# Create or update the implementation artifacts for RAG-BT019:
# pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/runner.py; pilot_phase2_poc/rag-service/docs/evaluation/golden-questions.md
```

### Linux / macOS Bash Implementation File Preparation

```bash
PRIMARY_IMPL_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/runner.py"
mkdir -p "$(dirname "$PRIMARY_IMPL_PATH")"
# Create or update the implementation artifacts for RAG-BT019:
# pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/runner.py; pilot_phase2_poc/rag-service/docs/evaluation/golden-questions.md
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
uv run pytest "app/stages/stage_05_evaluation/tests/test_evaluation_runner.py" -q
uv run pytest -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest "app/stages/stage_05_evaluation/tests/test_evaluation_runner.py" -q
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
git -C $WorktreePath commit -m "build(rag): implement rag-bt019 evaluation-harness"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): implement rag-bt019 evaluation-harness"
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

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-BT019-evaluation-harness.md`.
