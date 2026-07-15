# RAG-DT013: Final Build Task Impact Review

Status: Draft

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.

| Field | Value |
|---|---|
| Task ID | `RAG-DT013` |
| Task Name | Final Build Task Impact Review |
| Design Lane | 06-build-impact-review |
| Source Question | Design-to-build transition |
| Decision / ADR | design-to-build-transition-plan.md |
| Related Planning Docs | `build-sequence/02-design-tasks/`, `build-sequence/03-build-tasks/`, `02-rag-db/planning/confirmed-build-sequence.md` |
| Affected Build Tasks | All 03-build-tasks files |
| Branch | `codex/rag-dt013-final-build-task-impact-review` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-dt013-final-build-task-impact-review` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Draft |

## 1. Task Definition

Design: review completed design decisions and update affected final build task
files before implementation begins.

Goal: prevent final build tasks from using stale assumptions after KB,
chunking, metadata, model, Docker, or query-planning decisions are completed.

Output Artifact:

```text
docs/design/final-build-task-impact-review.md
```

Acceptance Criteria:

- each completed design task is mapped to affected build tasks
- build task acceptance criteria are updated where design decisions changed
  implementation expectations
- build tasks do not ingest or test against `legacy/phase1-kb-snapshot/` unless
  a design task explicitly says it is an audit fixture
- any unresolved design decision is explicitly deferred with risk and owner
- no final build task starts with stale KB, metadata, chunking, query, model, or
  Docker assumptions
- final build sequence remains aligned with `../00-index.md`

Out Of Scope:

- runtime implementation
- writing production code
- running final build tasks

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-dt013"
$Slug = "final-build-task-impact-review"
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
TASK_ID="rag-dt013"
SLUG="final-build-task-impact-review"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
git -C "$REPO_ROOT" config core.longpaths true
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```
## 3. Acceptance Check

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\final-build-task-impact-review.md" -Pattern "design_task|affected_build_task|decision|action"
```

## 4. Design Work

Create a build-impact matrix with these columns:

- `design_task`
- `decision_or_output`
- `affected_build_task`
- `required_update`
- `status`
- `owner`
- `risk_if_not_updated`

At minimum, review these impact areas:

- legacy Phase 1 KB snapshot boundary and non-ingestion rule
- KB folder layout and source registry path
- source registry schema
- source snapshot and markdown candidate rules
- chunking strategy and chunk metadata
- golden questions and expected retrieval matches
- query planner vocabulary and safeguard rules
- LLM model evaluation fixture
- embedding benchmark fixture
- test vector DB and CI integration strategy
- Docker/local ops and CI integration strategy

## 5. Build Task Impact

Affected Build Tasks:

- All 03-build-tasks files

Required Updates:

- Update every affected build task before implementation starts.

Deferred Impact:

- Only explicitly deferred decisions may remain.

Impact Review Status:

- This task is the final impact review gate.

## 6. Verification

Review with RAG Architect, Test Engineer, CI/CD Engineer, RAG Evaluation Lead,
and Documentation Steward.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt013 final-build-task-impact-review"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt013 final-build-task-impact-review"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to main.

Required PR checks:

- CI pipeline runs
- CI passes
- AI scans the design artifact and affected build-task updates
- human owner reviews the PR
- accepted findings are fixed

## 8. Merge

Merge only after CI passes and the PR is reviewed. Record PR URL, CI result,
merge commit, unresolved risks, and follow-up debt entries if any. Then clean up
the worktree.

### Windows PowerShell

```powershell
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" worktree remove $WorktreePath
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" worktree prune
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" pull --ff-only origin main
```

### Linux / macOS Bash

```bash
git -C "$REPO_ROOT" worktree remove "$WORKTREE_PATH"
git -C "$REPO_ROOT" worktree prune
git -C "$REPO_ROOT" pull --ff-only origin main
```
## 9. Task Evidence

Branch:
Worktree:
PR:
Commit:

Design Artifact:

Affected Build Tasks:

Files Changed:
-

Checks Run:
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







