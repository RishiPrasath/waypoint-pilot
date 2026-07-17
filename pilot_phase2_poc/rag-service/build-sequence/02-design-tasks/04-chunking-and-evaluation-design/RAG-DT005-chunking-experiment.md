# RAG-DT005: Run Chunking Experiment During KB Curation

Status: Complete

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-DT005` |
| Task Name | Run Chunking Experiment During KB Curation |
| Design Lane | 04-chunking-and-evaluation-design |
| Source Question | RAG-Q011 chunking decision |
| Decision / ADR | active/03-ingestion-plan.md |
| Related Planning Docs | `02-rag-db/active/03-ingestion-plan.md`, `02-rag-db/active/02-knowledge-source-plan.md` |
| Affected Build Tasks | RAG-BT009, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019 |
| Branch | `codex/rag-dt005-chunking-experiment` |
| Worktree Path | `C:\tmp\rag-dt005-chunking-experiment` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Complete |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT005-chunking-experiment.md` |

## 1. Task Definition

Design: compare chunking strategies using representative canonical sources.

Goal: choose chunking rules after KB structure and representative source shape
are known.

Output Artifact:

```text
docs/design/chunking-experiment.md
docs/design/experiments/chunking/dt005-run-001/queue-manifest.json
docs/design/experiments/chunking/dt005-run-001/chunks-fixed-window-baseline.jsonl
docs/design/experiments/chunking/dt005-run-001/chunks-structure-aware-v1.jsonl
docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl
docs/design/experiments/chunking/dt005-run-001/comparison-report.md
```

Acceptance Criteria:

- representative sources are selected
- representative source shapes include procedure pages, tables, FAQs, dynamic
  lookup snapshots, bilingual or translated pages, and license-sensitive
  summary-only sources where those appear in the approved candidates
- legacy Phase 1 KB files may be used to understand document shape, but only
  audited/promoted candidates may drive the final chunking decision
- at least two chunking strategies are compared
- the experiment is manifest-driven and queue-shaped
- candidate hashes are verified before chunking
- generated chunk records are stored as JSONL
- metadata carried by each chunk is documented
- chosen strategy and rejected alternatives are recorded
- retrieval impact is described

Out Of Scope:

- production ingestion pipeline
- final embedding model lock

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt005"
$Slug = "chunking-experiment"
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
TASK_ID="rag-dt005"
SLUG="chunking-experiment"
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
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\chunking-experiment.md" -Pattern "chosen strategy|metadata|rejected|retrieval impact"
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\chunking-experiment.md" -Pattern "run_id|queue-manifest|jsonl|hash_verified"
```

## 4. Design Work

Run small, representative chunking experiments and record results.

The experiment must be pipeline-shaped, even though production ingestion and a
production queue backend remain out of scope. Use this local design-run shape:

```text
snapshot manifest -> queue item -> candidate loader -> hash verification
-> markdown parser -> chunking strategy -> JSONL chunk records -> report
```

The experiment set must include APAC trade-lane material and at least one
structured/table-heavy source so the final chunking rule is not optimized only
for clean prose.

Use the legacy snapshot only as source-shape evidence:

```text
pilot_phase2_poc/rag-service/legacy/phase1-kb-snapshot/
```

Final chunking rules must be based on audited/promoted Phase 2 source
candidates, not the legacy folder as a runtime input.

Accepted result:

- `hybrid_structure_recursive_v1` is the chosen strategy.
- `structure_aware_v1` is retained as a structure-only comparison strategy.
- `fixed_window_baseline_v1` is the rejected baseline.
- `APAC-215` is recorded as skipped because it is metadata-only and
  license-sensitive.
- The runner records both normalized text SHA-256 and raw checkout SHA-256 so
  Windows CRLF checkout behavior does not break canonical markdown hash checks.
- Each candidate is assessed against the hybrid strategy and recursive fallback
  behavior is recorded per chunk.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT009, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019

Required Updates:

- Update chunking rules, chunk metadata expectations, ingestion output,
  retrieval tests, evaluation fixture expectations, and fixture paths so they do
  not accidentally ingest `legacy/`.
- Point affected build tasks to
  `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl`
  as the design fixture shape for future implementation.

Deferred Impact:

- Embedding model lock remains in RAG-DT010.
- Production queue backend and worker execution remain out of scope until the
  ingestion pipeline build tasks.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with RAG Architect, Retrieval Engineer, and RAG Evaluation Lead.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt005 chunking-experiment"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt005 chunking-experiment"
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

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-DT005-chunking-experiment.md`.
