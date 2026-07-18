# DT016 Implemented Gaps

Run: `dt016-run-001`

## Implemented In This Branch

| Gap | Files Changed | Verification |
|---|---|---|
| Dedicated `rag-service` CI workflow missing | `.github/workflows/rag-service-ci.yml` | Local equivalent commands pass. PR GitHub Actions pending. |
| Dedicated CodeQL workflow missing | `.github/workflows/rag-service-codeql.yml` | Workflow file added. PR GitHub Actions pending. |
| Dependabot config missing | `.github/dependabot.yml` | Config file added. Repo setting still needs owner/admin review. |
| Bandit scans tests and reports pytest asserts | `.github/workflows/rag-service-ci.yml` | `uv run bandit -c pyproject.toml -r app -x ...` reports no issues. |
| `integration` marker missing | `pyproject.toml` | `uv run python -m pytest -q` passes. |
| Ruff format gate would fail | formatted three files | `uv run ruff format --check .` passes. |

## New `rag-service` CI Workflow

The CI workflow runs:

```text
uv sync --dev --frozen
uv run python -m pytest -q
uv run ruff format --check .
uv run ruff check .
uv run bandit -c pyproject.toml -r app -x app/api/tests,app/core/tests,app/shared/tests,app/shared/vector_db/tests
uv run pip-audit
```

It runs on:

- PRs touching `pilot_phase2_poc/rag-service/**`;
- pushes to `main` touching `pilot_phase2_poc/rag-service/**`;
- manual dispatch.

## Correct Deferrals

| Deferred Item | Reason | Owner |
|---|---|---|
| Qdrant service-container integration job | Requires real ingestion/retrieval fixtures from BT012 + BT013. | BT012/BT013 with DT014 contract. |
| Docker image build and container smoke | Requires Dockerfile and Compose from BT020. | BT020. |
| Trivy image scan | Requires image build target from BT020. | BT020/BT022 or later CI hardening. |
| Secret scanning repo setting | GitHub API reports disabled; branch file changes cannot prove setting activation. | Owner/admin. |
| Dependabot security updates repo setting | Config added, API still reports disabled. | Owner/admin. |

## Local Verification Result

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
