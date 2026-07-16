# RAG-DT003: Create APAC Source Candidate Registry

Status: Complete

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-DT003` |
| Task Name | Create APAC Source Candidate Registry |
| Design Lane | 02-source-scope-and-registry |
| Source Question | RAG-Q012 APAC authoritative-source research |
| Decision / ADR | ADR-RAG-0012 |
| Related Planning Docs | `02-rag-db/research/authoritative-sources-apac.md`, `02-rag-db/active/02-knowledge-source-plan.md` |
| Affected Build Tasks | RAG-BT008, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019 |
| Branch | `codex/rag-dt003-apac-source-candidate-registry` |
| Worktree Path | `D:\Code\Github\waypoint-pilot-worktrees\rag-dt003-apac-source-candidate-registry` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Complete |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT003-apac-source-candidate-registry.md` |

## 1. Task Definition

Design: create candidate source rows for APAC authoritative sources.

Goal: identify official customs, trade, logistics, Incoterms, and regional
sources before canonical KB creation.

Output Artifact:

```text
knowledge_base/registry/source_registry.yaml
```

Acceptance Criteria:

- first-pass markets are listed
- source owner and `source_uri` are captured
- `document_id`, `authority_level`, `source_status`, `promotion_status`, and
  `retrieval_eligible` are captured using the source registry vocabulary
- authority, freshness, access, and license/reuse status are captured
- APAC-specific fields are captured where relevant: `source_access_pattern`,
  `language`, `translation_review_required`, `dynamic_lookup_snapshot`,
  `legal_disclaimer`, `license_sensitive`, `reuse_mode`, and
  `retrieval_namespace`
- promotion blockers are visible

Out Of Scope:

- scraping
- cleaned canonical markdown

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt003"
$Slug = "apac-source-candidate-registry"
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
TASK_ID="rag-dt003"
SLUG="apac-source-candidate-registry"
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
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\knowledge_base\registry\source_registry.yaml" -Pattern "document_id|source_uri|authority_level|source_status|promotion_status|retrieval_eligible"
```

## 4. Design Work

Use APAC research evidence to create candidate registry rows.

The first-pass registry should cover core APAC markets and trade-lane source
assembly needs, including official customs/trade authorities, regional
agreement sources, and license-sensitive global standards bodies where they are
needed for citation or summary-only treatment.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT008, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019

Required Updates:

- Update source registry rows, ingestion fixture source list, retrieval metadata expectations, and golden source coverage.

Deferred Impact:

- Scraping/materialization handled by RAG-DT012.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with Logistics Domain Expert and Knowledge Base Curator.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt003 apac-source-candidate-registry"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt003 apac-source-candidate-registry"
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

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-DT003-apac-source-candidate-registry.md`.
