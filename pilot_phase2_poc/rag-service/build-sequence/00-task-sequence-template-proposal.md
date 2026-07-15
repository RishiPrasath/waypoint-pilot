# RAG Service Task Sequence Template Proposal

Status: Proposal - not approved for canonical use
Date: 2026-07-15

## Purpose

Make every setup, design, and build task executable, auditable, and closable
without relying on chat history or undocumented recovery steps.

This proposal responds to the issues found while running RAG-BT000 and
RAG-BT001:

- Windows long-path failure during worktree checkout
- branch created even though worktree checkout failed
- PowerShell UTF-8 BOM broke `pyproject.toml`
- `uv run pytest` did not reliably import the local `app` package
- commands pasted together were interpreted as one command
- empty directories were not preserved by Git
- worktree deletion failed while the terminal or IDE still held the path
- task files stayed `Draft` after implementation
- execution evidence was blank or split across multiple locations
- post-merge evidence required an unplanned follow-up PR

## Proposed Folder Layout

```text
build-sequence/
  00-index.md                         # canonical sequence and gate rules
  00-governance/
    01-task-template.md               # canonical task specification template
    02-evidence-template.md           # canonical execution evidence template
    03-closeout-checklist.md          # mandatory post-merge closeout
    04-command-conventions.md         # PowerShell, uv, Git, path rules
    05-status-model.md                 # lifecycle and transition rules
  01-setup-tasks/
    00-index.md
    RAG-BT000-*.md
    RAG-BT001-*.md
  02-design-tasks/
    00-index.md
    ...
  03-build-tasks/
    00-index.md
    ...

build-evidence/
  README.md
  RAG-BT000-prove-workflow.md
  RAG-BT001-fastapi-skeleton.md
  ...
```

The task files remain in their current lanes. The new governance files become
the single source of truth for how tasks are written and executed. Evidence
remains outside `build-sequence/` and is linked from each task file.

## Proposed Task File Template

Each task file should contain only the task specification and a pointer to its
evidence. It should not contain a second blank evidence form.

```markdown
# RAG-$TaskId: $TaskName

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-$TaskId` |
| Lane | setup / design / build |
| Dependencies | task IDs or `none` |
| Blocks | task IDs or `none` |
| Branch | `codex/rag-$task_slug` |
| Worktree | standard worktree path |
| Evidence | `build-evidence/RAG-$TaskId-$slug.md` |

## 1. Objective And Scope

## 2. Dependencies And Gates

## 3. Expected Artifacts

## 4. Acceptance Criteria

Every criterion must be objectively checkable.

## 5. Preflight

Run the preflight checklist before writing files.

## 6. Red Check

Write the failing test or failing acceptance check first.

## 7. Implementation

Use one command per code block. Windows commands must be BOM-safe.

## 8. Verification Matrix

| Check | Command | Expected result |
|---|---|---|

## 9. PR Handoff

## 10. Merge And Closeout

## 11. Out Of Scope And Deferred Work
```

## Proposed Evidence Template

The evidence file is the execution record. It is created on the task branch,
updated before the PR is merged, and completed by a documented closeout commit
after merge if post-merge facts are not yet known.

```markdown
# RAG-$TaskId Evidence

Status: In Progress / In Review / Merged / Complete / Blocked

## Identity

Task:
Branch:
Worktree:
Starting main commit:

## Preflight

Main status:
Long-path setting:
Worktree status:

## Red Check

Command:
Result:

## Implementation

Files changed:
Implementation commit:

## Verification

| Check | Command | Result | Evidence |
|---|---|---|---|

## Pull Request

PR URL:
PR checks:
Review result:

## Merge Closeout

Merged main commit:
Main verification:
Worktree removed:
Branch cleanup:

## Issues And Recovery

## Follow-ups
```

Blank fields are not allowed. Use an explicit value such as `N/A - no
rag-service CI exists until RAG-BT004` when a check is not applicable.

## Proposed Status Model

```text
Planned
  -> Ready
  -> In Progress
  -> In Review
  -> Merged
  -> Complete

In Progress -> Blocked
Planned -> Deferred
```

Rules:

- `Complete` requires merged code or design, passing required checks, evidence,
  and worktree closeout.
- `Blocked` requires a written blocker and next unblock condition.
- `Deferred` requires an owner and reason.
- The next task cannot start while a required predecessor is not `Complete` or
  explicitly `Deferred`.

## Proposed Windows Preflight

Commands must be shown separately and executed separately:

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-bt001"
$Slug = "fastapi-skeleton"
$Branch = "codex/$TaskId-$Slug"
$WorktreePath = Join-Path $WorktreeRoot "$TaskId-$Slug"

Set-Location $RepoRoot
git -C $RepoRoot status --short --branch
git -C $RepoRoot fetch origin
git -C $RepoRoot pull --ff-only origin main
git -C $RepoRoot config core.longpaths true
git -C $RepoRoot config --get core.longpaths
git -C $RepoRoot worktree add -b $Branch $WorktreePath origin/main
git -C $WorktreePath status --short --branch
```

If checkout fails after the branch is created, the recovery procedure must be
documented and must reuse the existing branch rather than attempting to create
it again. A shorter worktree path such as `C:\tmp\rag-$TaskId` is an approved
fallback.

## Proposed Windows File-Writing Rule

Do not use `Set-Content -Encoding UTF8` for TOML, YAML, JSON, or Python files
when the parser rejects a BOM. Use a shared helper in the command convention
document:

```powershell
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
```

## Proposed Python Test Rule

Use this as the standard local invocation:

```powershell
uv run python -m pytest -q
```

If console-script pytest is retained, `pyproject.toml` must include an
explicit project-root configuration such as:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
```

## Proposed Git Structure Rule

Acceptance criteria must never depend on empty directories. Every required
placeholder directory must contain one of:

- a real placeholder module
- `__init__.py` when it is a Python package
- `.gitkeep` when it is only a future storage directory
- `README.md` when it needs human guidance

The structural acceptance test must verify the committed tree, not only the
local filesystem.

## Proposed Closeout Sequence

1. Run local tests and checks.
2. Complete the pre-PR evidence gate below.
3. Confirm `git status` is clean except for intended changes.
4. Commit and push the task branch.
5. Open the PR and record its URL in evidence.
6. Wait for review and checks.
7. Merge the PR.
8. From the main repository root, fetch and fast-forward `main`.
9. Confirm the merged commit contains the task.
10. Move the terminal out of the task worktree and close any IDE terminal using
   it.
11. Remove the worktree; if removal fails, stop and diagnose rather than
   repeatedly answering the prompt.
12. Prune worktree metadata.
13. Delete the merged local task branch.
14. Delete the merged remote task branch when permitted.
15. Complete post-merge evidence in a closeout commit/PR.
16. Mark the task `Complete` only after the closeout evidence is merged.

## Proposed Pre-PR Evidence Gate

The PR must not be opened until the task evidence file exists on the task
branch and contains:

- task ID, branch, worktree, and starting `main` commit
- clean preflight result
- long-path configuration result on Windows
- the expected failing test or acceptance check and its result
- implementation files changed
- passing local test commands and results
- structural or contract checks required by the task
- known issues and recovery steps
- `PR: Pending PR creation`
- `PR checks: Pending PR creation`
- `Merged main commit: Pending merge`
- `Worktree cleanup: Pending merge`

No required field may be blank. `Pending ...` and `N/A - reason` are valid
evidence values; empty fields are not.

After the PR is opened, update the evidence with the PR URL and check results
before merge. After merge, complete the merged commit and cleanup fields in the
closeout commit/PR. This makes evidence a gate at every transition rather than
an after-the-fact report.

## Proposed Approval Boundary

This file is a proposal only. After approval:

1. add the governance templates under `build-sequence/00-governance/`
2. update `build-sequence/00-index.md` with the status and closeout gates
3. update lane indexes to reference the canonical template
4. rewrite future task files before starting RAG-BT002
5. optionally migrate BT000 and BT001 records to the new format

Existing task files should not be bulk-rewritten until the template is
approved.
