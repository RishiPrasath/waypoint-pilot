# RAG-DT016 CI/CD And REST Service Readiness Gate

Status: In Review
Run: `dt016-run-001`
Date: 2026-07-18

## Purpose

This gate verifies that the `rag-service` CI/CD and REST-service testing runway
is strong enough before the project moves into architecture sufficiency review
and final build-task impact review.

This task is intentionally more than a report. It audits the current state,
implements required CI/CD gaps that can be fixed now, and records deferrals that
need later implementation or owner/admin action.

## Scope

In scope:

- GitHub Actions workflows for `rag-service`;
- CodeQL workflow coverage for Python;
- Dependabot configuration;
- local commands that mirror CI;
- current FastAPI app import, `/health`, `/ready`, config, error schema, and
  vector DB wrapper tests;
- Ruff format and lint checks;
- Bandit app-code security check;
- pip-audit dependency check;
- Docker/Docker Compose availability;
- accepted `RAG-DT014` and `RAG-DT011` test/runtime boundaries.

Out of scope:

- implementing ingestion, retrieval, generation, or evaluation behavior;
- implementing Dockerfile or `docker-compose.yml`;
- production deployment;
- changing the accepted vector DB strategy.

## Implemented CI/CD Readiness Changes

| Gap | Fix |
|---|---|
| No dedicated `rag-service` CI workflow | Added `.github/workflows/rag-service-ci.yml`. |
| No dedicated `rag-service` CodeQL workflow | Added `.github/workflows/rag-service-codeql.yml`. |
| No Dependabot config found | Added `.github/dependabot.yml` for GitHub Actions and `rag-service` Python dependencies. |
| Bandit command scanned pytest assertions in tests locally | Kept Bandit focused on app code with explicit test excludes in CI command. |
| Future `integration` marker was not registered | Added pytest `integration` marker in `pyproject.toml`. |
| Existing source formatting would fail a new Ruff format gate | Ran `ruff format` on the three files reported by the formatter. |

## CI Layer Decision

| Layer | Status After DT016 | Notes |
|---|---|---|
| Python environment and dependency install | Implemented | `uv sync --dev --frozen` in CI. |
| Fast unit/API tests | Implemented | `uv run python -m pytest -q`. |
| Ruff format and lint | Implemented | `ruff format --check .` and `ruff check .`. |
| Bandit app-code security check | Implemented | Excludes test directories, scans `app`. |
| pip-audit dependency check | Implemented | `uv run pip-audit`. |
| CodeQL | Implemented as workflow file | Requires GitHub Actions execution after PR. |
| Dependabot | Implemented as config file | Repo security update setting still reported disabled by GitHub API. |
| Secret scanning | Deferred owner/admin setting | GitHub API reported disabled; not safely changeable as a file-only branch fix. |
| Qdrant service-container integration | Correctly deferred | Required after BT012 + BT013 create real ingestion/retrieval fixtures. |
| Docker image build/container smoke | Correctly deferred | Owned by BT020 and later DT016/CI evolution once Dockerfile exists. |

## Local Verification Commands

```powershell
Set-Location pilot_phase2_poc/rag-service
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

Local result:

```text
pytest -> 12 passed
ruff format --check -> 44 files already formatted
ruff check -> All checks passed
bandit -> No issues identified
pip-audit -> No known vulnerabilities found
docker -> 28.5.1
docker compose -> v2.40.3-desktop.1
docker daemon -> 28.5.1
```

## REST Service Readiness

Current REST surface is adequate for pre-RAG CI:

- `app.main:app` imports;
- `/health` returns `{"status": "ok"}`;
- `/ready` returns `{"status": "ready"}`;
- config tests cover local defaults and secret repr redaction;
- error schema tests cover basic validation;
- vector DB wrapper tests are mocked and Docker-free.

Missing business endpoints are intentionally not implemented here. The query
API belongs to `RAG-BT018`.

## Qdrant And Docker Boundary

DT016 preserves the accepted split:

- default CI does not start Docker/Qdrant;
- local Qdrant integration remains pre-push/manual until real fixtures exist;
- GitHub Actions Qdrant service-container tests become required after BT012 and
  BT013;
- Docker image build and container smoke wait for BT020.

## Decision

Status: `Pass With Deferred Items`

The project now has a dedicated `rag-service` CI workflow target, CodeQL
workflow file, Dependabot config, registered integration marker, and local
commands that pass. DT013 remains blocked until DT017 is complete, but DT016 no
longer blocks it except for explicitly deferred owner/admin or future-code
items.

Deferred items:

- GitHub repo settings reported secret scanning disabled.
- GitHub repo settings reported Dependabot security updates disabled.
- Qdrant service-container integration remains deferred until BT012 + BT013.
- Docker image build/container smoke/Trivy remain deferred until BT020 creates
  Dockerfile and Compose implementation.
