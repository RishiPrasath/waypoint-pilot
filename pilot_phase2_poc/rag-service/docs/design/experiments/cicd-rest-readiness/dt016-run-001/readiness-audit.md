# DT016 Readiness Audit

Run: `dt016-run-001`
Status: In Review

## Baseline Findings

| Area | Finding | Severity | Action |
|---|---|---|---|
| RAG service CI workflow | No dedicated `rag-service` workflow existed. Existing workflows targeted Phase 1 ingestion and partner-source modules. | High | Implemented `.github/workflows/rag-service-ci.yml`. |
| CodeQL | No dedicated CodeQL workflow file was present for `rag-service`. | High | Implemented `.github/workflows/rag-service-codeql.yml`. |
| Dependabot | No `.github/dependabot.yml` file was present. | High | Implemented config for GitHub Actions and Python dependencies. |
| Secret scanning | GitHub API reported `secret_scanning: disabled`. | High | Deferred owner/admin setting; cannot be proven through file-only branch change. |
| Dependabot security updates | GitHub API reported `dependabot_security_updates: disabled`. | Medium | Config added; repo setting remains owner/admin follow-up. |
| Bandit | Baseline command scanned tests and reported 30 low-severity `assert_used` findings. | Medium | Workflow uses explicit test exclusions for app-code scan. |
| Ruff format | New format gate would fail on three existing files. | Medium | Ran `ruff format .`. |
| Pytest marker | Future `integration` marker was unregistered. | Medium | Registered marker in `pyproject.toml`. |
| REST tests | App import, health, readiness, config, error schema, and mocked vector DB tests exist. | None | No change needed. |
| Docker | Docker CLI, Compose, and daemon are available locally. | None | Recorded as available; no Docker CI added yet. |
| Qdrant integration | Accepted DT014 strategy exists but real fixtures are not implemented yet. | None | Correctly deferred until BT012 + BT013. |

## Existing Workflow Inventory

Observed before DT016 implementation:

```text
.github/workflows/ingestion.yml
.github/workflows/partner-source-fastapi-ci.yml
.github/workflows/partner-source-springboot-ci.yml
```

These workflows do not provide dedicated `rag-service` CI coverage.

Added by DT016:

```text
.github/workflows/rag-service-ci.yml
.github/workflows/rag-service-codeql.yml
.github/dependabot.yml
```

## REST Surface Audit

| Check | Status |
|---|---|
| App import smoke | Covered by existing tests. |
| `/health` endpoint | Covered by existing tests. |
| `/ready` endpoint | Covered by existing tests. |
| Config/settings tests | Covered by existing tests. |
| Error schema tests | Covered by existing tests. |
| Query API endpoint | Not applicable yet; owned by BT018. |
| RAG runtime endpoints | Not applicable yet; future build tasks. |

## CI Layer Audit

| Layer | Status |
|---|---|
| Python dependency install | Implemented by `uv sync --dev --frozen`. |
| Unit/API tests | Implemented by `uv run python -m pytest -q`. |
| Ruff format | Implemented by `uv run ruff format --check .`. |
| Ruff lint | Implemented by `uv run ruff check .`. |
| Bandit | Implemented by app-code scan with test exclusions. |
| pip-audit | Implemented. |
| CodeQL | Implemented as workflow file. |
| Dependabot | Implemented as config file; security updates setting follow-up. |
| Secret scanning | Owner/admin repo setting follow-up. |
| Qdrant service-container integration | Deferred until BT012 + BT013. |
| Docker image build/smoke | Deferred until BT020. |

## GitHub Repository Security API Check

Command:

```powershell
gh api repos/RishiPrasath/waypoint-pilot --jq '{visibility,secret_scanning:.security_and_analysis.secret_scanning.status,codeql:.security_and_analysis.advanced_security.status,dependabot_security_updates:.security_and_analysis.dependabot_security_updates.status}'
```

Result:

```json
{"codeql":null,"dependabot_security_updates":"disabled","secret_scanning":"disabled","visibility":"public"}
```

Interpretation:

- CodeQL workflow file is now added and must be proven by GitHub Actions.
- Secret scanning and Dependabot security updates may require repository
  settings changes beyond file-only CI implementation.
