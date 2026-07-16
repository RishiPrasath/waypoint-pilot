# RAG-DT004: Confirm KB Folder Layout And Registry Storage

Status: Complete

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-DT004` |
| Task Name | Confirm KB Folder Layout And Registry Storage |
| Design Lane | 03-kb-materialization |
| Source Question | KB structure decision |
| Decision / ADR | ADR-RAG-0005, ADR-RAG-0013 |
| Related Planning Docs | `02-rag-db/active/02-knowledge-source-plan.md` |
| Affected Build Tasks | RAG-BT007, RAG-BT008, RAG-BT009, RAG-BT012, RAG-BT019, RAG-BT020 |
| Branch | `codex/rag-dt004-kb-folder-layout` |
| Worktree Path | `C:\tmp\rag-dt004-kb-folder-layout` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Complete |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT004-kb-folder-layout.md` |

## 1. Task Definition

Design: confirm the KB folder layout and source registry storage path.

Goal: make ingestion, registry validation, snapshots, canonical/reference, and
archive paths stable before build work depends on them.

Output Artifact:

```text
knowledge_base/README.md
```

Acceptance Criteria:

- exact KB folders are listed
- legacy audit folder boundary is documented separately from the approved KB
- source registry path is fixed
- snapshot/hash policy is described
- canonical/reference/archive/drop rules are clear
- ingestion is prohibited from reading `legacy/` directly

Out Of Scope:

- ingesting content
- validating registry rows in code

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt004"
$Slug = "kb-folder-layout"
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
TASK_ID="rag-dt004"
SLUG="kb-folder-layout"
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
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\knowledge_base\README.md" -Pattern "registry|canonical|reference|archive|snapshots"
```

## 4. Design Work

Document accepted KB folder structure.

Also document that the copied Phase 1 KB lives outside the approved KB
materialization path:

```text
pilot_phase2_poc/rag-service/legacy/phase1-kb-snapshot/
```

The final `knowledge_base/` structure must remain clean until design tasks
promote audited material into canonical, reference, archive, snapshot, or
candidate layers.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT007, RAG-BT008, RAG-BT009, RAG-BT012, RAG-BT019, RAG-BT020

Required Updates:

- Update paths for registry, canonical/reference/archive/snapshot folders,
  ingestion fixtures, Docker volume assumptions, and the explicit rule that
  legacy snapshot material is audit-only.

Deferred Impact:

- Internal folder details may evolve until KB materialization is reviewed.

Impact Review Status:

- Pending RAG-DT013 review.

Accepted Path Contract:

- Registry: `knowledge_base/registry/source_registry.yaml`
- Registry schema: `knowledge_base/registry/source_registry.schema.json`
- Snapshots: `knowledge_base/snapshots/`
- Cleaned candidates: `knowledge_base/candidates/`
- Canonical retrieval material: `knowledge_base/canonical/`
- Non-runtime review/reference material: `knowledge_base/reference/`
- Superseded/rejected material: `knowledge_base/archive/`
- Temporary untrusted intake: `knowledge_base/drop/`
- Legacy audit input only: `legacy/phase1-kb-snapshot/`

## 6. Verification

Review with Documentation Steward and Knowledge Base Curator.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt004 kb-folder-layout"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt004 kb-folder-layout"
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
## Task Evidence

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-DT004-kb-folder-layout.md`.
