# RAG-BT013: Add Semantic Retrieval Baseline

Status: Planned

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT013` |
| Task Name | Add Semantic Retrieval Baseline |
| Build Stage | 03-retrieval - Retrieval |
| Source Question | RAG-Q009, RAG-Q017 |
| Decision / ADR | ADR-RAG-0007, RAG-DT005, RAG-DT012, RAG-DT013 |
| Design Dependencies | RAG-BT012, RAG-DT005, RAG-DT012, RAG-DT014, RAG-DT013 |
| Depends On Build Tasks | see section 1 and section 3 |
| Branch | `codex/rag-bt013-semantic-retrieval-baseline` |
| Worktree Path | `C:\tmp\rag-bt013-semantic-retrieval-baseline` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT013-semantic-retrieval-baseline.md` |

## 1. Task Definition

Build: semantic retrieval baseline.

Goal: retrieve expected chunks from seeded fixture data with metadata filters.

Module: `app/stages/stage_03_retrieval/`.

Design Gates:

- `RAG-BT012`
- `RAG-DT005`
- `RAG-DT012`
- `RAG-DT014`
- `RAG-DT013`

Acceptance Criteria:

- retriever interface exists
- seeded semantic retrieval returns expected chunk
- metadata filter limits results correctly
- result includes source ID and chunk ID
- result metadata preserves source lineage and candidate hash from the DT012
  manifest when seeded from source-derived candidates

Out Of Scope:

- hybrid retrieval
- reranking
- generation

DT012 Retrieval Fixture Contract:

- Seed retrieval tests only from fixture ingestion outputs that can trace back
  to `knowledge_base/snapshots/first-pass-snapshot-manifest.md`.
- Retrieval assertions must include `document_id`, `snapshot_id`, source URI,
  and candidate SHA-256 when the fixture originates from DT012 candidates.
- Do not seed `APAC-215` as retrievable domain content.

DT005 Retrieval Chunk Contract:

- Seed semantic retrieval from `hybrid_structure_recursive_v1` chunks or ingestion outputs
  that preserve the same metadata shape as
  `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl`.
- Retrieval tests must assert `chunk_id`, `heading_path`, `chunk_strategy`,
  `candidate_sha256`, `section_part_index`, `recursive_split_applied`, and
  source lineage in addition to semantic match.
- Fixed-window baseline chunks are not the semantic baseline seed format.

## 2. Worktree And Branch Setup

Create the branch and worktree before creating tests or implementation files.
Do not write task code directly on `main`.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt013"
$Slug = "semantic-retrieval-baseline"
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
TASK_ID="rag-bt013"
SLUG="semantic-retrieval-baseline"
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
pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/tests/test_semantic_retrieval.py
```

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/tests/test_semantic_retrieval.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@(
  '# RAG-BT013 failing test placeholder',
  '# Replace this placeholder with the task-specific failing test after design gates are complete.',
  'def test_semantic_retrieval_baseline():',
  '    assert False, "Implement RAG-BT013 after design dependencies are confirmed"'
) | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/tests/test_semantic_retrieval.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
# RAG-BT013 failing test placeholder
# Replace this placeholder with the task-specific failing test after design gates are complete.
def test_semantic_retrieval_baseline():
    assert False, "Implement RAG-BT013 after design dependencies are confirmed"
EOF
```

Expected initial failure:

```text
The test or acceptance check fails because semantic retrieval baseline is not implemented yet.
```

## 4. Implementation

Implement only after the failing test or acceptance check exists.

Target implementation artifacts:

- `pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/service.py`
- `pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/schemas.py`

### Windows PowerShell Implementation File Preparation

```powershell
$PrimaryImplPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/service.py"
New-Item -ItemType Directory -Force -Path (Split-Path $PrimaryImplPath) | Out-Null
# Create or update the implementation artifacts for RAG-BT013:
# pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/service.py; pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/schemas.py
```

### Linux / macOS Bash Implementation File Preparation

```bash
PRIMARY_IMPL_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/service.py"
mkdir -p "$(dirname "$PRIMARY_IMPL_PATH")"
# Create or update the implementation artifacts for RAG-BT013:
# pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/service.py; pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/schemas.py
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
uv run pytest "app/stages/stage_03_retrieval/tests/test_semantic_retrieval.py" -q
uv run pytest -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest "app/stages/stage_03_retrieval/tests/test_semantic_retrieval.py" -q
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
git -C $WorktreePath commit -m "build(rag): implement rag-bt013 semantic-retrieval-baseline"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): implement rag-bt013 semantic-retrieval-baseline"
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

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-BT013-semantic-retrieval-baseline.md`.
