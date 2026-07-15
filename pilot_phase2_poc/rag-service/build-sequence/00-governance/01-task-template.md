# RAG-BTXXX Task Title

Status: Planned

| Field | Value |
|---|---|
| Task ID | RAG-BTXXX |
| Lane | Setup / Design / Build |
| Dependencies | None or task IDs |
| Blocks | None or task IDs |
| Branch | `codex/rag-btxxx-short-slug` |
| Worktree | `C:\tmp\rag-btxxx-short-slug` |
| Evidence | `build-evidence/RAG-BTXXX-short-slug.md` |

## Mandatory Execution Contract

This task follows `build-sequence/00-governance/`. Before implementation, create
the dedicated branch and worktree, confirm the dependency gate, and create the
matching evidence file. Run one PowerShell command per block. Use the canonical
Windows command conventions and record the exact outputs needed to prove the
acceptance criteria. Inline snippets in an existing task are reference-only when
they conflict with this contract; never use BOM-producing `Set-Content -Encoding
UTF8` or `uv run pytest`. No PR is allowed before the pre-PR evidence gate passes.

## 1. Objective

State the smallest outcome this task must deliver.

## 2. Dependencies

List the prerequisite task IDs and the evidence/status check that proves each is
complete.

## 3. Artifacts

List the files, directories, configuration, or tests that must be created or
changed.

## 4. Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## 5. Preflight

- [ ] `origin/main` fetched and task branch is based on it.
- [ ] Dedicated worktree path is correct and short enough for Windows.
- [ ] Worktree is clean before implementation.
- [ ] Required dependency evidence is present and complete.

## 6. Red Check

Describe the failing test or validation that demonstrates the missing behavior
before implementation. If a red check is not meaningful, explain why in the
evidence record.

## 7. Implementation

Describe the minimal implementation and any deliberate deviations.

## 8. Verification Matrix

| Check | Command | Expected result | Evidence location |
|---|---|---|---|
| Targeted test | `uv run python -m pytest ...` | Pass | Evidence file |
| Full task test | `uv run python -m pytest -q` | Pass | Evidence file |
| Static/security check | Task-specific | Pass or documented exception | Evidence file |
| Git check | `git status --short --branch` | Clean before handoff | Evidence file |

## 9. PR Handoff

- [ ] Evidence file is complete through the pre-PR gate.
- [ ] Task record links to the evidence file.
- [ ] Branch is pushed and PR URL is recorded in evidence.
- [ ] CI/check and review state are recorded before merge.

## 10. Merge and Closeout

- [ ] PR merged.
- [ ] `main` fast-forwarded to the merged commit.
- [ ] Worktree removed and pruned.
- [ ] Post-merge evidence committed and merged.
- [ ] Status changed to `Complete` only after all checks pass.

## 11. Out of Scope

Record work explicitly deferred to another task.
