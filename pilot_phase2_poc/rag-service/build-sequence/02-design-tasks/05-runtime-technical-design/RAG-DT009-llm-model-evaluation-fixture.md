# RAG-DT009: Define LLM Model Evaluation Fixture

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-DT009` |
| Task Name | Define LLM Model Evaluation Fixture |
| Design Lane | 05-runtime-technical-design |
| Source Question | LLM model selection process |
| Decision / ADR | ADR-RAG-0003 |
| Related Planning Docs | `02-rag-db/research/llm-provider-selection.md` |
| Affected Build Tasks | RAG-BT016, RAG-BT017, RAG-BT018, RAG-BT019 |
| Branch | `codex/rag-dt009-llm-model-evaluation-fixture` |
| Worktree Path | `C:\tmp\rag-dt009-llm-model-evaluation-fixture` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `build-evidence/RAG-DT009-llm-model-evaluation-fixture.md` |

## Mandatory Execution Contract

This task follows `build-sequence/00-governance/`. Its matching execution record
must be maintained at the Evidence path above. Run one PowerShell command per
block, use the canonical Windows/Python command conventions, and record the
exact checks and results in the evidence file. The pre-PR evidence gate is
mandatory; `Complete` requires merged closeout, clean `main`, and worktree
cleanup.


## 1. Task Definition

Design: define model evaluation fixture for Groq/OpenAI-compatible models.

Goal: compare candidate models using simulated or retrieved chunks before
locking final generation model.

Output Artifact:

```text
docs/design/llm-model-evaluation-plan.md
```

Acceptance Criteria:

- candidate model listing process is defined
- simulated chunk test set is defined
- quality rubric is defined
- latency measurement is defined
- schema adherence and citation behavior are scored

Out Of Scope:

- live production model calls
- final model lock without evidence

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt009"
$Slug = "llm-model-evaluation-fixture"
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
TASK_ID="rag-dt009"
SLUG="llm-model-evaluation-fixture"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```
## 3. Acceptance Check

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\llm-model-evaluation-plan.md" -Pattern "quality|latency|schema|citation"
```

## 4. Design Work

Define model evaluation process and fixture data.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT016, RAG-BT017, RAG-BT018, RAG-BT019

Required Updates:

- Update generation adapter candidates, mocked provider tests, response quality rubric, latency capture, schema adherence, and citation checks.

Deferred Impact:

- Final model lock requires evaluation evidence.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with LLM Integration Engineer and RAG Evaluation Lead.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt009 llm-model-evaluation-fixture"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt009 llm-model-evaluation-fixture"
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





