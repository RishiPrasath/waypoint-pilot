# RAG-DT012: Source Snapshot And Canonical Markdown Candidates

Status: Planned

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-DT012` |
| Task Name | Source Snapshot And Canonical Markdown Candidates |
| Design Lane | 03-kb-materialization |
| Source Question | KB enrichment and re-scrape plan |
| Decision / ADR | knowledge-source-plan.md |
| Related Planning Docs | `02-rag-db/research/kb-enrichment-rescrape-plan.md`, `02-rag-db/research/authoritative-sources-apac.md` |
| Affected Build Tasks | RAG-BT008, RAG-BT009, RAG-BT012, RAG-BT013, RAG-BT019 |
| Branch | `codex/rag-dt012-source-snapshot-and-canonical-markdown-candidates` |
| Worktree Path | `C:\tmp\rag-dt012-source-snapshot-and-canonical-markdown-candidates` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT012-source-snapshot-and-canonical-markdown-candidates.md` |

## 1. Task Definition

Design: define and execute the source snapshot and cleaned markdown candidate
plan for approved source registry entries.

Goal: bridge the gap between registered authoritative sources and
representative source-derived markdown documents that can be reviewed,
chunked, and later ingested.

Output Artifacts:

```text
docs/design/source-snapshot-and-markdown-candidates.md
knowledge_base/snapshots/
knowledge_base/candidates/
```

Acceptance Criteria:

- approved source registry candidates are selected for the first pass
- legacy Phase 1 KB material is treated as historical audit input, not as raw
  authoritative source snapshots
- raw snapshot policy is documented
- cleaned markdown candidate rules are documented
- source lineage, source URL, retrieval status, license status, and content hash
  expectations are defined
- no invented regulatory content is allowed
- source-derived summaries or explainers must cite source lineage
- representative candidate documents are available for chunking experiments

Out Of Scope:

- production scraping automation
- final ingestion pipeline
- embedding or indexing

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt012"
$Slug = "source-snapshot-and-canonical-markdown-candidates"
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
TASK_ID="rag-dt012"
SLUG="source-snapshot-and-canonical-markdown-candidates"
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
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\source-snapshot-and-markdown-candidates.md" -Pattern "snapshot|candidate|lineage|license|hash"
```

## 4. Design Work

Create the source snapshot and canonical markdown candidate plan.

The plan must answer:

- how legacy Phase 1 KB files are referenced as audit evidence without treating
  them as approved Phase 2 snapshots
- which approved registry sources are included in the first materialization pass
- how raw snapshots are stored and identified
- how cleaned markdown candidates are created from authoritative sources
- how source-derived summaries are distinguished from copied source text
- how license-sensitive material is handled
- how content hashes and scrape/snapshot IDs are recorded
- which candidate documents are representative enough for chunking experiments

Use this wording:

```text
source-derived canonical markdown candidates
```

Use this legacy audit input path when comparing against Phase 1 material:

```text
pilot_phase2_poc/rag-service/legacy/phase1-kb-snapshot/
```

Do not use this wording as the default:

```text
synthetic regulatory content
```

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT008, RAG-BT009, RAG-BT012, RAG-BT013, RAG-BT019

Required Updates:

- Update candidate document paths, snapshot/hash expectations, source lineage
  fields, chunking input fixtures, ingestion acceptance checks, and the legacy
  boundary rule for historical Phase 1 material.

Deferred Impact:

- Production scraping automation remains out of scope.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with Knowledge Base Curator, Logistics Domain Expert, RAG Architect, and
Security Reviewer.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt012 source-snapshot-and-canonical-markdown-candidates"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt012 source-snapshot-and-canonical-markdown-candidates"
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

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-DT012-source-snapshot-and-canonical-markdown-candidates.md`.
