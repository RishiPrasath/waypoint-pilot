# RAG-DT002: Create Phase 1 KB Source Audit Table

Status: Draft

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.

| Field | Value |
|---|---|
| Task ID | `RAG-DT002` |
| Task Name | Create Phase 1 KB Source Audit Table |
| Design Lane | 02-source-scope-and-registry |
| Source Question | Phase 1 KB scan and KB source audit |
| Decision / ADR | ADR-RAG-0013 |
| Related Planning Docs | `02-rag-db/research/phase1-kb-scan-report.md`, `02-rag-db/active/02-knowledge-source-plan.md` |
| Affected Build Tasks | RAG-BT008, RAG-BT009, RAG-BT012, RAG-BT013, RAG-BT019 |
| Branch | `codex/rag-dt002-phase1-kb-source-audit` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-dt002-phase1-kb-source-audit` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Draft |

## 1. Task Definition

Design: audit the Phase 1 KB source-by-source.

Goal: decide what should become canonical, reference, archived, or dropped
before Phase 2 ingestion.

Output Artifact:

```text
docs/design/phase1-kb-source-audit.md
```

Acceptance Criteria:

- audit table uses `legacy/phase1-kb-snapshot/` as the source audit input
- audit table has source ID, legacy path, source type, authority, target
  status, blocker, next action, and priority
- carrier/company marketing and synthetic SOPs are separated from public
  regulatory knowledge
- public customs/regulatory sources are identified for authority review
- nothing from the legacy snapshot is treated as canonical without explicit
  promotion evidence

Out Of Scope:

- final canonical KB migration
- scraping new sources

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-dt002"
$Slug = "phase1-kb-source-audit"
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
TASK_ID="rag-dt002"
SLUG="phase1-kb-source-audit"
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
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\phase1-kb-source-audit.md" -Pattern "source_id|target_status|next_action"
```

## 4. Design Work

Use the Phase 1 KB scan report and the copied legacy snapshot to classify each
source.

Legacy audit input:

```text
pilot_phase2_poc/rag-service/legacy/phase1-kb-snapshot/
```

The audit must classify legacy material before any selected source is promoted
into the Phase 2 KB design.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT008, RAG-BT009, RAG-BT012, RAG-BT013, RAG-BT019

Required Updates:

- Update source audit artifacts, chunking fixtures, ingestion fixture sources,
  retrieval expectations, evaluation source coverage, and the rule that
  `legacy/` is not an ingestible runtime KB path.

Deferred Impact:

- Final promotion depends on registry/schema and materialization tasks.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with Knowledge Base Curator and Logistics Domain Expert.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt002 phase1-kb-source-audit"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt002 phase1-kb-source-audit"
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







