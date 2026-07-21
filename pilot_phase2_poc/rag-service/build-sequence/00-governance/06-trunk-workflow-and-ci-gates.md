# Trunk Workflow and CI Gates

Status: Accepted
Owner: solo developer
Last updated: 2026-07-21

## Purpose

This file locks the working rules that prevent build-sequence drift while the
RAG service is built through short-lived task branches.

## Required workflow

1. Start every task from fresh `origin/main`.
2. Use a short-lived `codex/` branch or worktree for the task.
3. Keep one implementation concern per branch unless a governance fix must be
   bundled to make the branch safe.
4. Create or update build evidence in the same branch before opening the PR.
5. Do not mark a task `Complete` unless the same PR includes the required
   evidence with `Status: Complete` or `Status: Ready for Merge`.
6. If the PR URL/check summary must be recorded in evidence, update that same
   branch before merge.
7. Merge only after local checks and GitHub Actions pass.
8. After merge, pull fresh main and prune task worktrees.
9. Do not create a second closeout PR only for merge commit, main CI, or cleanup
   metadata; GitHub and local git are the source of truth for those facts.

## CI-enforced rules

`scripts/check_build_sequence_governance.py` runs in repository-root
`.github/workflows/rag-service-ci.yml` and enforces:

- completed task files must point to an existing evidence file;
- completed task evidence must say `Status: Complete` or
  `Status: Ready for Merge`;
- final build task files must retain the DT013 final design handoff;
- service-local `.github` workflow/config files are forbidden because GitHub
  only executes workflows from the repository-root `.github/workflows` folder;
- `In Review` or `Complete` tasks must not still contain failing-test
  placeholders;
- design documents must not remain at `Status: Proposed`.

## Accepted placeholder rule

Planned build tasks may contain red-test placeholders. The placeholder is a
planning signal only. Before a task moves to `In Review`, those placeholders
must be replaced by task-specific tests that exercise the actual implementation
contract.

## Qdrant config naming rule

Qdrant-backed tasks may use ecosystem-standard `QDRANT_*` names for service
integration settings, but runtime application settings must document the exact
external environment variables and any `RAG_*` aliases they support before the
owning task can close. `RAG-BT012`, `RAG-BT013`, and `RAG-BT020` must not close
with ambiguous Qdrant config names.

## Canonical KB promotion rule

Fixture and candidate material can be used to build ingestion, retrieval, and
evaluation behavior. Production readiness cannot treat that material as the
canonical production KB until a later task explicitly promotes the accepted
source set and records the promotion evidence.

## Local artifact rule

Editor-only files such as `.code-workspace` files must not be staged unless a
task explicitly says they are part of the deliverable.

## One-shot evidence rule

Every task PR must carry its own evidence. Post-merge closeout PRs are reserved
for correcting material mistakes, not for bookkeeping that GitHub already
records.
