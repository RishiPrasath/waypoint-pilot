# Partner Source FastAPI

Fresh FastAPI parity implementation folder for Waypoint Phase 2 Partner Source.

This folder is intentionally not scaffolded yet. Build it from scratch by hand when you are ready.

## Role

FastAPI proves the same Partner Source contract can be implemented in Python.

It must not become a second product or a second source of API truth.

## Starting Choices

| Area | Choice |
|---|---|
| Python | 3.12 or newer |
| Framework | FastAPI |
| Server | `uvicorn[standard]` |
| Tests | pytest, httpx, FastAPI `TestClient` |
| Dependency manager | Prefer `uv`; requirements files are acceptable for the first scaffold |
| Persistence | In-memory repositories only |
| Health | Custom `/health` and `/ready` |

Do not add SQLAlchemy, Alembic, background workers, authentication packages, Docker, deployment config, or OpenAPI server generation for Slice 1.

## First Manual Setup Target

Create the app here with:

```text
pyproject.toml or requirements files
.python-version
app/main.py
app/api/
app/schemas/
app/domain/
app/repositories/
app/services/
app/seed/
app/errors/
tests/
```

If using `uv`, first validation command:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
uv sync --locked --all-extras --dev
uv run pytest
```

If using requirements files first:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
```

## First Real TDD Target

Mirror the Spring Boot status transition tests:

```text
tests/domain/test_status_transition_policy.py
```

Follow the root checklist:

```text
..\MANUAL_BUILD_SEQUENCE.md
```

Use the numbered human build sequence for all instructions:

```text
build-sequence\00-index.md
```

For agreed behavior, use:

```text
..\AGREED_SPEC.md
```

Older long-form manuals are archived under `..\docs\archive\manuals\` for history only.
