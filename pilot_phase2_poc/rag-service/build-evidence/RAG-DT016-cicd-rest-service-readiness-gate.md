# RAG-DT016 Evidence

Status: Complete

## Identity

Task: RAG-DT016 - CI/CD And REST Service Readiness Gate
Branch: `codex/rag-dt016-cicd-rest-readiness-gate`
Worktree: `C:\tmp\rag-dt016-cicd-rest-readiness-gate`
Starting main commit: `b8628fa`
PR: https://github.com/RishiPrasath/waypoint-pilot/pull/36
Implementation commit: `f529c99`
Merge commit: `97aa3e0a63f8cfb22ad918ac9142c5943038c448`

## Artifacts

- `.github/workflows/rag-service-ci.yml`
- `.github/workflows/rag-service-codeql.yml`
- `.github/dependabot.yml`
- `pilot_phase2_poc/rag-service/docs/design/cicd-rest-service-readiness-gate.md`
- `pilot_phase2_poc/rag-service/docs/design/experiments/cicd-rest-readiness/dt016-run-001/readiness-audit.md`
- `pilot_phase2_poc/rag-service/docs/design/experiments/cicd-rest-readiness/dt016-run-001/implemented-gaps.md`
- `pilot_phase2_poc/rag-service/docs/design/experiments/cicd-rest-readiness/dt016-run-001/decision-gate.md`
- `pilot_phase2_poc/rag-service/build-sequence/02-design-tasks/05-runtime-technical-design/RAG-DT016-cicd-rest-service-readiness-gate.md`
- `pilot_phase2_poc/rag-service/build-sequence/02-design-tasks/00-index.md`

## Baseline Checks

```powershell
Get-ChildItem -Path "$WorktreePath\.github\workflows" -Filter "*.yml"
Get-ChildItem -Path "$WorktreePath\.github\workflows" -Filter "*.yaml"
Test-Path "$ServiceRoot\pyproject.toml"
Test-Path "$ServiceRoot\app\main.py"
uv run python -m pytest -q
uv run ruff check .
uv run bandit -c pyproject.toml -r app
uv run pip-audit
docker --version
docker compose version
docker info --format '{{.ServerVersion}}'
```

Baseline result:

```text
workflow files before DT016:
- ingestion.yml
- partner-source-fastapi-ci.yml
- partner-source-springboot-ci.yml

pyproject.toml exists -> True
app/main.py exists -> True
uv run python -m pytest -q -> 12 passed
uv run ruff check . -> All checks passed
uv run bandit -c pyproject.toml -r app -> 30 low B101 findings from tests
uv run pip-audit -> No known vulnerabilities found
docker --version -> Docker version 28.5.1
docker compose version -> Docker Compose version v2.40.3-desktop.1
docker info -> 28.5.1
```

## Implemented Checks

```powershell
uv sync --dev --frozen
uv run python -m pytest -q
uv run ruff format --check .
uv run ruff check .
uv run bandit -c pyproject.toml -r app -x app/api/tests,app/core/tests,app/shared/tests,app/shared/vector_db/tests
uv run pip-audit
docker --version
docker compose version
docker info --format '{{.ServerVersion}}'
```

Result:

```text
uv sync --dev --frozen -> passed
uv run python -m pytest -q -> 12 passed
uv run ruff format --check . -> 44 files already formatted
uv run ruff check . -> All checks passed
uv run bandit ... -> No issues identified
uv run pip-audit -> No known vulnerabilities found
docker --version -> Docker version 28.5.1
docker compose version -> Docker Compose version v2.40.3-desktop.1
docker info -> 28.5.1
```

GitHub repository security setting check:

```powershell
gh api repos/RishiPrasath/waypoint-pilot --jq '{visibility,secret_scanning:.security_and_analysis.secret_scanning.status,codeql:.security_and_analysis.advanced_security.status,dependabot_security_updates:.security_and_analysis.dependabot_security_updates.status}'
```

Result:

```json
{"codeql":null,"dependabot_security_updates":"disabled","secret_scanning":"disabled","visibility":"public"}
```

## Decision

Gate result: `Pass With Deferred Items`

Implemented now:

- dedicated `rag-service` CI workflow;
- dedicated `rag-service` CodeQL workflow;
- Dependabot config;
- pytest `integration` marker;
- local CI-equivalent checks passing;
- Ruff formatting brought into compliance.

Deferred:

- secret scanning repository setting review;
- Dependabot security updates repository setting review;
- Qdrant service-container integration until BT012 + BT013;
- Docker image build/container smoke/Trivy until BT020.

## CI And Review

PR CI: Passed

- `RAG Service CI / Unit, lint, and security checks`: success
- `RAG Service CodeQL / Analyze Python`: success
- `CodeQL`: success

Main CI/CD after merge: Passed

- `RAG Service CI`: success for merge commit
  `97aa3e0a63f8cfb22ad918ac9142c5943038c448`
- `RAG Service CodeQL`: success for merge commit
  `97aa3e0a63f8cfb22ad918ac9142c5943038c448`

Human review: merged by owner on PR #36
AI review: Codex local verification and PR check inspection completed

## Issues And Recovery

- Initial branch creation hit an existing stale local branch from the prior
  DT016 task-definition PR. The branch was verified merged into `main`, deleted
  locally, and recreated from current `origin/main`.
- Initial Ruff format check would have failed on three existing files. `ruff
  format .` was run and the format check now passes.
- A temporary dependency change from `httpx2` to `httpx` was tested and reverted
  because the current FastAPI/Starlette stack expects `httpx2`.

## Follow-ups

- Repository security settings still require owner/admin review:
  secret scanning and Dependabot security updates were reported disabled.
- Qdrant service-container integration remains deferred until BT012 + BT013.
- Docker image build/container smoke/Trivy remains deferred until BT020.
- `RAG-DT017` remains the next design task before final build impact review.
