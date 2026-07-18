# RAG-DT017 Evidence

Status: Complete

## Identity

Task: RAG-DT017 - Overall Architecture And Design Sufficiency Review
Branch: `codex/rag-dt017-architecture-sufficiency-review`
Worktree: `C:\tmp\rag-dt017-architecture-sufficiency-review`
Starting main commit: `abc1dd0`
PR: https://github.com/RishiPrasath/waypoint-pilot/pull/43
Implementation commit: `77339ff2a8fe203fb6cefa8022895684acdc3859`
Merge commit: `6f69eebb3a133ff07fce7fd11eea24f0b4276bd9`
Merged At: `2026-07-18T05:57:47Z`

Rebase note: this branch was rebased onto `origin/main` after PR #44 and PR
#45 added and closed out the `RAG-DT018`, `RAG-DT019`, and `RAG-DT020`
follow-up task sequence. DT017 artifacts were updated to recognize those task
files as created but not completed.

## Baseline Checks

```powershell
$ServiceRoot = Join-Path $WorktreePath "pilot_phase2_poc\rag-service"
Set-Location $ServiceRoot

Test-Path "$ServiceRoot\build-sequence\02-design-tasks\00-index.md"
Test-Path "$ServiceRoot\build-sequence\02-design-tasks\05-runtime-technical-design\RAG-DT016-cicd-rest-service-readiness-gate.md"
Test-Path "$ServiceRoot\build-sequence\02-design-tasks\06-build-impact-review\RAG-DT013-final-build-task-impact-review.md"
Get-ChildItem "$ServiceRoot\build-sequence\02-design-tasks" -Recurse -Filter "RAG-DT*.md"
Get-ChildItem "$ServiceRoot\docs\design" -Recurse -File
Get-ChildItem "$ServiceRoot\build-evidence" -Filter "RAG-DT*.md"
$env:RAG_GROQ_API_KEY = $null
uv run python -m pytest -q
git -C $WorktreePath diff --check
```

Result:

```text
required task/index paths -> True
design task files -> 20
design artifact files -> 44
design evidence files -> 16
$env:RAG_GROQ_API_KEY = $null; uv run python -m pytest -q -> 12 passed
git diff --check -> passed
```

Note: `RAG_GROQ_API_KEY` was cleared only inside the local pytest command so
the missing-secret tests match CI behavior without printing or persistently
changing local credentials.

## Specialist Review Coverage

Specialist review perspectives were recorded for:

1. FastAPI/API architecture
2. Python packaging and unit testing
3. Qdrant/vector database
4. Ingestion, source registry, and KB materialization
5. Chunking, retrieval, and evaluation
6. LLM/generation and prompt safety
7. CI/CD and local ops
8. Security and data governance
9. Frontend/API-consumer impact
10. Overall systems architect synthesis

## Additional Live Checks

GitHub repository settings check:

```powershell
gh api repos/RishiPrasath/waypoint-pilot --jq '{visibility,default_branch,secret_scanning:.security_and_analysis.secret_scanning.status,dependabot_security_updates:.security_and_analysis.dependabot_security_updates.status,advanced_security:.security_and_analysis.advanced_security.status}'
gh api repos/RishiPrasath/waypoint-pilot/branches/main/protection
gh api repos/RishiPrasath/waypoint-pilot/rulesets --jq '[.[] | {name,target,enforcement}]'
```

Result:

```json
{"advanced_security":null,"default_branch":"main","dependabot_security_updates":"disabled","secret_scanning":"disabled","visibility":"public"}
```

```text
branch protection -> not enabled or inaccessible
rulesets -> []
```

Dependency provenance check:

```powershell
uv run python -m pip show httpx2 httpcore2
```

Result:

```text
httpx2 2.7.0, home page https://github.com/pydantic/httpx2
httpcore2 2.7.0, home page https://github.com/pydantic/httpx2
```

Local `pip-audit` was already passing under DT016 and the DT017 baseline kept
the local test surface passing.

## Artifacts Created

```text
docs/design/architecture-sufficiency-review.md
docs/design/experiments/architecture-review/dt017-run-001/expert-review-findings.md
docs/design/experiments/architecture-review/dt017-run-001/gap-register.md
docs/design/experiments/architecture-review/dt017-run-001/recommended-follow-up-design-tasks.md
docs/design/experiments/architecture-review/dt017-run-001/decision-gate.md
build-evidence/RAG-DT017-architecture-sufficiency-review.md
```

## Existing Artifact Hygiene

This branch also updates:

```text
docs/design/cicd-rest-service-readiness-gate.md
```

from `Status: In Review` to `Status: Accepted for RAG-DT016`, because PR #42
already closed out DT016 in the task file and evidence.

## Decision

Gate result:

```text
Pass With Required Follow-Up Tasks
```

Required follow-up design tasks:

- `RAG-DT018: Retrieval Strategy Selection, Scoring, And Fusion Contract`
- `RAG-DT019: Generation Prompt, Safeguards, Output Schema, And Query API Contract`
- `RAG-DT020: Post-Build Evaluation And Tuning Loop`

The task files for these follow-ups now exist in the current sequence. They
must still be completed or explicitly waived before `RAG-DT013`.

Required owner decision/remediation items:

- repository enforcement/security settings;
- `httpx2`/`httpcore2` dependency provenance and accepted rationale.

## Follow-Ups

- PR #43 merged.
- PR CI/CD passed:
  - Unit, lint, and security checks: passed.
  - Analyze Python: passed.
  - CodeQL: passed.
- Main CI/CD passed for merge commit
  `6f69eebb3a133ff07fce7fd11eea24f0b4276bd9`:
  - RAG Service CI: https://github.com/RishiPrasath/waypoint-pilot/actions/runs/29633162175
  - RAG Service CodeQL: https://github.com/RishiPrasath/waypoint-pilot/actions/runs/29633162180
- Cleanup completed after merge:
  - Local `main` refreshed to merge commit `6f69eeb`.
  - Worktree `C:\tmp\rag-dt017-architecture-sufficiency-review` removed.
  - Local branch `codex/rag-dt017-architecture-sufficiency-review` deleted.
  - Remote branch `codex/rag-dt017-architecture-sufficiency-review` deleted.
