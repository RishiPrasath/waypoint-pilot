# RAG-DT006: Define Golden Questions And Answer Rubrics

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-DT006` |
| Task Name | Define Golden Questions And Answer Rubrics |
| Design Lane | 04-chunking-and-evaluation-design |
| Source Question | Evaluation and use-case decision |
| Decision / ADR | ADR-RAG-0008 |
| Related Planning Docs | `02-rag-db/active/07-evaluation-plan.md` |
| Affected Build Tasks | RAG-BT019, RAG-BT013, RAG-BT014, RAG-BT018 |
| Branch | `codex/rag-dt006-golden-questions` |
| Worktree Path | `C:\tmp\rag-dt006-golden-questions` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `build-evidence/RAG-DT006-golden-questions.md` |

## Mandatory Execution Contract

This task follows `build-sequence/00-governance/`. Its matching execution record
must be maintained at the Evidence path above. Run one PowerShell command per
block, use the canonical Windows/Python command conventions, and record the
exact checks and results in the evidence file. The pre-PR evidence gate is
mandatory; `Complete` requires merged closeout, clean `main`, and worktree
cleanup.


## 1. Task Definition

Design: define golden questions and answer rubrics.

Goal: make evaluation possible before the evaluation harness is built.

Output Artifact:

```text
docs/evaluation/golden-questions.md
```

Acceptance Criteria:

- questions map to supported use cases
- expected source types are listed
- expected approved source IDs or citation IDs are listed for positive cases
- APAC trade-lane questions are included
- negative cases include order status, driver assignment, partner operational
  procedure, irrelevant, and malicious/prompt-injection questions
- legacy Phase 1 KB examples can inform coverage gaps but cannot become
  expected sources unless audited/promoted
- answer quality rubric exists
- citation requirements exist
- irrelevant and malicious examples are included

Out Of Scope:

- evaluation runner code

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt006"
$Slug = "golden-questions"
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
TASK_ID="rag-dt006"
SLUG="golden-questions"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```
## 3. Acceptance Check

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\evaluation\golden-questions.md" -Pattern "rubric|citation|approved_source|order status|partner-source|malicious"
```

## 4. Design Work

Create the first golden question set and scoring rubric.

Separate retrieval scoring from answer scoring. Retrieval cases should define
expected source or citation matches, while answer cases should define grounded
response quality, refusal behavior, and citation requirements.

Review the legacy snapshot for useful examples and coverage gaps:

```text
pilot_phase2_poc/rag-service/legacy/phase1-kb-snapshot/
```

Golden answers must cite approved Phase 2 source candidates, not legacy files
directly, unless a design task explicitly promotes the source.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT019, RAG-BT013, RAG-BT014, RAG-BT018

Required Updates:

- Update evaluation harness cases, expected source matches, retrieval acceptance
  checks, API contract expectations, and the distinction between legacy examples
  and approved expected sources.

Deferred Impact:

- Golden set may expand after KB materialization.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with RAG Evaluation Lead and Logistics Domain Expert.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt006 golden-questions"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt006 golden-questions"
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





