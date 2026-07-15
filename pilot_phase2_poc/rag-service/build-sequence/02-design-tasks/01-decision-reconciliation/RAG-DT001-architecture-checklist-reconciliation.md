# RAG-DT001: Reconcile Architecture Checklist With Accepted ADRs

Status: Draft

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.

| Field | Value |
|---|---|
| Task ID | `RAG-DT001` |
| Task Name | Reconcile Architecture Checklist With Accepted ADRs |
| Design Lane | 01-decision-reconciliation |
| Source Question | RAG-Q018, RAG-Q022 |
| Decision / ADR | Accepted ADRs and architecture checklist |
| Related Planning Docs | `02-rag-db/planning/architecture-confirmation-checklist.md`, `02-rag-db/adrs/` |
| Affected Build Tasks | All setup and final build tasks |
| Branch | `codex/rag-dt001-architecture-checklist-reconciliation` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-dt001-architecture-checklist-reconciliation` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Draft |

## 1. Task Definition

Design: reconcile architecture checklist/status with accepted ADRs and current
implementation-lane decisions.

Goal: prevent old `Open` or stale planning statuses from blocking or confusing
the build sequence.

Output Artifact:

```text
docs/planning/architecture-confirmation-checklist.md
```

Acceptance Criteria:

- accepted ADRs are reflected in the architecture checklist
- stale `Open` statuses are corrected or explicitly explained
- any remaining undecided item is linked to a design task
- build sequence can identify which foundation tasks are unblocked

Out Of Scope:

- runtime code
- FastAPI scaffold

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-dt001"
$Slug = "architecture-checklist-reconciliation"
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
TASK_ID="rag-dt001"
SLUG="architecture-checklist-reconciliation"
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
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\planning\architecture-confirmation-checklist.md" -Pattern "Open|Accepted|Blocked"
```

## 4. Design Work

Review accepted ADRs and update the checklist to match the current decision
state.

## 5. Build Task Impact

Affected Build Tasks:

- All setup and final build tasks

Required Updates:

- Update task gates if ADR/checklist status changes.

Deferred Impact:

- None yet.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Verify each checklist row links to an ADR, design task, or explicit deferral.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt001 architecture-checklist-reconciliation"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt001 architecture-checklist-reconciliation"
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







