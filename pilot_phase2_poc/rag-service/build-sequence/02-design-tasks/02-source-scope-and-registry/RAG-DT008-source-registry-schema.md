# RAG-DT008: Define Source Registry Schema And Validation Rules

Status: Draft

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.

| Field | Value |
|---|---|
| Task ID | `RAG-DT008` |
| Task Name | Define Source Registry Schema And Validation Rules |
| Design Lane | 02-source-scope-and-registry |
| Source Question | Source registry and metadata decision |
| Decision / ADR | active/02-knowledge-source-plan.md |
| Related Planning Docs | `02-rag-db/active/02-knowledge-source-plan.md` |
| Affected Build Tasks | RAG-BT007, RAG-BT008, RAG-BT012, RAG-BT013, RAG-BT014 |
| Branch | `codex/rag-dt008-source-registry-schema` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-dt008-source-registry-schema` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Draft |

## 1. Task Definition

Design: define source registry schema and validation rules.

Goal: make source registry validation buildable and auditable.

Output Artifact:

```text
knowledge_base/registry/source_registry.schema.json
```

Acceptance Criteria:

- required fields are listed
- allowed source statuses are listed
- retrieval eligibility rules are defined
- promotion gates are defined
- canonical registry names follow the source plan: `document_id`,
  `source_uri`, `authority_level`, `source_status`, `promotion_status`, and
  `retrieval_eligible`
- APAC source fields are represented: `source_access_pattern`, `language`,
  `translation_review_required`, `dynamic_lookup_snapshot`,
  `legal_disclaimer`, `license_sensitive`, `reuse_mode`, and
  `retrieval_namespace`
- registry schema can represent legacy audit inputs without making them
  retrieval eligible
- validation failure behavior is described

Out Of Scope:

- validator runtime code

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-dt008"
$Slug = "source-registry-schema"
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
TASK_ID="rag-dt008"
SLUG="source-registry-schema"
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
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\knowledge_base\registry\source_registry.schema.json" -Pattern "document_id|source_uri|authority_level|source_status|promotion_status|retrieval_eligible"
```

## 4. Design Work

Define the registry schema and validation acceptance criteria.

Use examples from the legacy snapshot to verify that the schema can represent
audit-only material:

```text
pilot_phase2_poc/rag-service/legacy/phase1-kb-snapshot/
```

Legacy rows must default to non-retrieval-eligible until promoted by source
audit and KB materialization decisions.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT007, RAG-BT008, RAG-BT012, RAG-BT013, RAG-BT014

Required Updates:

- Update registry validation tests, metadata fields, retrieval eligibility
  rules, ingestion source checks, and default non-ingestible treatment for
  legacy audit rows.

Deferred Impact:

- Schema may need migration notes after source materialization.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with Knowledge Base Curator and Test Engineer.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt008 source-registry-schema"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt008 source-registry-schema"
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







