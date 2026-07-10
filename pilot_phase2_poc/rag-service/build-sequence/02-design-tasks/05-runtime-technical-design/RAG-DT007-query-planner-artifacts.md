# RAG-DT007: Define Query Planner Vocabulary And Rules

Status: Draft

| Field | Value |
|---|---|
| Task ID | `RAG-DT007` |
| Task Name | Define Query Planner Vocabulary And Rules |
| Design Lane | 05-runtime-technical-design |
| Source Question | Query planning decision |
| Decision / ADR | active/05-query-planning.md |
| Related Planning Docs | `02-rag-db/active/05-query-planning.md`, `02-rag-db/active/06-safeguards.md` |
| Affected Build Tasks | RAG-BT015, RAG-BT018, RAG-BT019 |
| Branch | `codex/rag-dt007-query-planner-artifacts` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-dt007-query-planner-artifacts` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Draft |

## 1. Task Definition

Design: define deterministic query planner artifacts.

Goal: create vocabulary and rule files before query-planning code is built.

Output Artifacts:

```text
docs/design/query-planning/planner_vocabulary.json
docs/design/query-planning/query_planner_rules.yaml
docs/design/query-planning/query_planner_tests.yaml
```

Acceptance Criteria:

- key logistics terms are listed
- country/market aliases are listed
- Incoterm terms are listed
- relevance and out-of-scope rules are defined
- test cases are defined

Out Of Scope:

- planner runtime code
- LLM planner

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-dt007"
$Slug = "query-planner-artifacts"
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
TASK_ID="rag-dt007"
SLUG="query-planner-artifacts"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```
## 3. Acceptance Check

```powershell
Get-ChildItem "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\query-planning"
```

## 4. Design Work

Create deterministic planner artifacts.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT015, RAG-BT018, RAG-BT019

Required Updates:

- Update query safeguard/planner test cases, vocabulary file paths, relevance rules, and API behavior for irrelevant or malicious questions.

Deferred Impact:

- LLM-based planning remains out of scope unless later approved.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with Terminology Researcher, RAG Architect, and Prompt And Safety
Engineer.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt007 query-planner-artifacts"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt007 query-planner-artifacts"
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





