# RAG-DT010: Define Embedding Benchmark Fixture

Status: Draft

| Field | Value |
|---|---|
| Task ID | `RAG-DT010` |
| Task Name | Define Embedding Benchmark Fixture |
| Design Lane | 05-runtime-technical-design |
| Source Question | Embedding model benchmark decision |
| Decision / ADR | ADR-RAG-0002 |
| Related Planning Docs | `02-rag-db/research/vector-database-selection.md` |
| Affected Build Tasks | RAG-BT011, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019 |
| Branch | `codex/rag-dt010-embedding-benchmark-fixture` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-dt010-embedding-benchmark-fixture` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Draft |

## 1. Task Definition

Design: define local embedding benchmark fixture.

Goal: compare embedding model quality, latency, memory, and local hardware fit
before locking embedding defaults.

Output Artifact:

```text
docs/design/embedding-benchmark-plan.md
```

Acceptance Criteria:

- candidate embedding models are listed
- local hardware constraints are documented
- quality metric is defined
- latency and memory measurement are defined
- model swap path is documented

Out Of Scope:

- final embedding adapter implementation
- final model lock without benchmark evidence

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-dt010"
$Slug = "embedding-benchmark-fixture"
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
TASK_ID="rag-dt010"
SLUG="embedding-benchmark-fixture"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```
## 3. Acceptance Check

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\embedding-benchmark-plan.md" -Pattern "latency|memory|quality|model"
```

## 4. Design Work

Define benchmark fixture and measurement process.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT011, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019

Required Updates:

- Update embedding adapter interface, benchmark fixture, retrieval quality expectations, latency/memory acceptance, and model swap notes.

Deferred Impact:

- Final embedding model lock requires benchmark evidence.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with Embedding Specialist, Retrieval Engineer, and RAG Evaluation Lead.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt010 embedding-benchmark-fixture"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt010 embedding-benchmark-fixture"
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





