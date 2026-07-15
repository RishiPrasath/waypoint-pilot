# RAG-BT000: Prove Branch, Worktree, PR, And Evidence Workflow

Status: Complete

| Field | Value |
|---|---|
| Task ID | `RAG-BT000` |
| Task Name | Prove Branch, Worktree, PR, And Evidence Workflow |
| Source Question | Engineering defaults and task auditability |
| Decision / ADR | ADR-RAG-0011, ADR-RAG-0014 |
| Branch | `codex/rag-bt000-prove-workflow` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-bt000-prove-workflow` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Complete |

## 1. Task Definition

Build: a no-runtime-change workflow proof for branch, worktree, evidence, PR,
CI, merge, and cleanup.

Goal: prove the development workflow before feature coding starts.

Module: repository workflow only.

Acceptance Criteria:

- branch is created from `origin/main`
- dedicated worktree exists
- evidence file is created under `pilot_phase2_poc/rag-service/build-evidence/`
- branch can be pushed
- PR can be opened
- PR CI/CD result is recorded if CI exists
- `main` CI/CD result is recorded after merge if CI exists
- worktree cleanup command is recorded

Out Of Scope:

- FastAPI scaffold
- runtime code
- design decisions

## 2. Worktree And Branch Setup

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-bt000"
$Slug = "prove-workflow"
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
TASK_ID="rag-bt000"
SLUG="prove-workflow"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```

## 3. Test Code Or Acceptance Check

Expected result: command output shows the new task branch and a clean worktree.

### Windows PowerShell

```powershell
git -C $WorktreePath status --short --branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short --branch
```

## 4. Implementation

Create an evidence file only.

### Windows PowerShell

```powershell
$EvidencePath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/build-evidence/RAG-BT000-prove-workflow.md"
New-Item -ItemType Directory -Force -Path (Split-Path $EvidencePath) | Out-Null
@'
# RAG-BT000 Evidence

Branch:
Worktree:
Local status:
PR:
PR CI/CD:
Main CI/CD:
Cleanup:
'@ | Set-Content -Path $EvidencePath -Encoding UTF8
```

### Linux / macOS Bash

```bash
EVIDENCE_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/build-evidence/RAG-BT000-prove-workflow.md"
mkdir -p "$(dirname "$EVIDENCE_PATH")"
cat > "$EVIDENCE_PATH" <<'EOF'
# RAG-BT000 Evidence

Branch:
Worktree:
Local status:
PR:
PR CI/CD:
Main CI/CD:
Cleanup:
EOF
```

## 5. Test Execution

### Windows PowerShell

```powershell
git -C $WorktreePath status --short --branch
Test-Path $EvidencePath
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short --branch
test -f "$EVIDENCE_PATH"
```

## 6. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath add pilot_phase2_poc/rag-service/build-evidence/RAG-BT000-prove-workflow.md
git -C $WorktreePath commit -m "docs(rag): prove task workflow"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service/build-evidence/RAG-BT000-prove-workflow.md
git -C "$WORKTREE_PATH" commit -m "docs(rag): prove task workflow"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to `main` and record the PR URL.

## 7. Merge

Merge only after review and PR CI/CD. Then confirm `main` CI/CD and clean up.

### Windows PowerShell

```powershell
git -C $RepoRoot worktree remove $WorktreePath
git -C $RepoRoot worktree prune
git -C $RepoRoot pull --ff-only origin main
```

### Linux / macOS Bash

```bash
git -C "$REPO_ROOT" worktree remove "$WORKTREE_PATH"
git -C "$REPO_ROOT" worktree prune
git -C "$REPO_ROOT" pull --ff-only origin main
```

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

Closeout:
- Workflow proof completed and recorded in the task evidence file.
