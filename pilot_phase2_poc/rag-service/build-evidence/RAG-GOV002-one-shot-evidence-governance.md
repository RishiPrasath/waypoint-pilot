# RAG-GOV002 One-Shot Evidence Governance

Status: Ready for Merge
Branch: `codex/rag-one-shot-evidence-governance`
Date: 2026-07-21

## Purpose

Correct the governance workflow so evidence is included in the same task PR
instead of requiring a second metadata-only closeout PR after merge.

## Changes

- Updated the evidence template to remove committed merge-commit/main-CI
  requirements.
- Updated the closeout checklist to require one task PR with evidence included.
- Updated the status model so `Ready for Merge` evidence is valid for a
  completed task waiting on PR merge.
- Updated trunk workflow rules to forbid closeout PRs for metadata already
  available from GitHub.
- Updated the governance checker to accept `Status: Ready for Merge` evidence
  for complete tasks.

## Verification

| Check | Command | Result |
|---|---|---|
| Governance gate | `uv run python scripts/check_build_sequence_governance.py` | Passed |
| Tests | `uv run python -m pytest -q` | 12 passed |
| Formatting | `uv run ruff format --check .` | Passed |
| Lint | `uv run ruff check .` | Passed |
| Diff whitespace | `git diff --check` | Passed |

## PR Handoff

PR: Pending until opened; update this same branch before merge if required.
PR CI/CD: GitHub PR checks are source of truth.
Merge commit: Recorded by GitHub after merge; no closeout PR required.
Main CI/CD: Recorded by GitHub after merge; no closeout PR required.
Cleanup: Pull main and prune worktree after merge; no closeout PR required.
