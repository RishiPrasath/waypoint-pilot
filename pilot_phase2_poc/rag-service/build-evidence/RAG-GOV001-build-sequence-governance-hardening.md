# RAG-GOV001 Build Sequence Governance Hardening Evidence

Status: In Review
Branch: `codex/rag-build-sequence-governance-hardening`
Date: 2026-07-21

## Purpose

Close the governance gaps identified after the design-to-build readiness scan:
status drift, missing executable enforcement, inactive nested workflow files,
and unclear trunk/CI closeout expectations.

## Changes

- Added `scripts/check_build_sequence_governance.py`.
- Wired the governance checker into repository-root RAG service CI.
- Removed service-local `.github` workflow/config files because they are inert
  inside `pilot_phase2_poc/rag-service`.
- Standardized stale evidence statuses to `Status: Complete`.
- Added trunk workflow and CI gate rules.
- Clarified the Qdrant config naming condition in the final build impact
  review.

## Verification

| Check | Command | Result |
|---|---|---|
| Governance gate | `uv run python scripts/check_build_sequence_governance.py` | Passed |
| Test suite | `uv run python -m pytest -q` | 12 passed |
| Formatting | `uv run ruff format --check .` | Passed |
| Lint | `uv run ruff check .` | Passed |
| Bandit | `uv run bandit -c pyproject.toml -r app -x app/api/tests,app/core/tests,app/shared/tests,app/shared/vector_db/tests` | No issues identified |
| pip-audit | `uv run pip-audit` | No known vulnerabilities found |
| Diff whitespace | `git diff --check` | Passed |

## PR / CI / Merge

PR:
PR CI/CD:
Merge commit:
Main CI/CD:
Cleanup:
