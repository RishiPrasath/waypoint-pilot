# 01 - Project Setup

## Status

- Status: Not Started
- Last Updated: 2026-07-02

## Purpose

Create the FastAPI parity module with Python 3.12+, FastAPI, pytest, and one tiny passing test.

## Source Docs To Read

- `../../AGREED_SPEC.md`
- `../../docs/active/fastapi-implementation-handoff.md`
- `../../docs/support/implementation-schematic-and-task-sequence.md`

## Tests To Write First

Create the first scaffold test:

```text
tests/test_app.py
```

Expected behavior:

- FastAPI app imports.
- TestClient can call `/health`.
- It is acceptable for `/health` to return `404` before the health endpoint task.

## Code To Implement

Preferred `uv` setup:

```text
pyproject.toml
.python-version
app/__init__.py
app/main.py
tests/test_app.py
```

Minimum dependencies:

```text
fastapi
uvicorn[standard]
pydantic
pytest
httpx
```

## Commands To Run

### 1. Open The Module Folder

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
Get-ChildItem -Force
```

Expected before scaffold:

```text
README.md
build-sequence
```

### 2. Check Tools

```powershell
py -0p
python --version
git --version
```

Expected:

- Python `3.12` or newer is available.
- Git is available.

### 3A. Create The FastAPI Project With `uv`

Use this option if `uv --version` works.

```powershell
$ErrorActionPreference = "Stop"

cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi

uv --version

@'
[project]
name = "partner-source-fastapi"
version = "0.1.0"
description = "Waypoint Partner Source FastAPI parity implementation"
requires-python = ">=3.12"
dependencies = [
    "fastapi",
    "uvicorn[standard]",
    "pydantic",
]

[dependency-groups]
dev = [
    "pytest",
    "httpx",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
'@ | Set-Content -Path pyproject.toml -Encoding UTF8

@'
3.12
'@ | Set-Content -Path .python-version -Encoding UTF8

New-Item -ItemType Directory -Force -Path `
  app,app\api,app\schemas,app\domain,app\repositories,app\services,app\seed,app\errors,tests | Out-Null

New-Item -ItemType File -Force -Path `
  app\__init__.py,app\api\__init__.py,app\schemas\__init__.py,app\domain\__init__.py,`
  app\repositories\__init__.py,app\services\__init__.py,app\seed\__init__.py,app\errors\__init__.py | Out-Null

@'
from fastapi import FastAPI


def create_app() -> FastAPI:
    return FastAPI(title="Waypoint Partner Source API", version="1.0.0")


app = create_app()
'@ | Set-Content -Path app\main.py -Encoding UTF8

@'
from fastapi.testclient import TestClient

from app.main import app


def test_app_starts() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code in {200, 404}
'@ | Set-Content -Path tests\test_app.py -Encoding UTF8
```

Run:

```powershell
uv sync --all-extras --dev
uv run pytest
```

### 3B. Create The FastAPI Project With Virtualenv

Use this option if `uv` is not installed.

```powershell
$ErrorActionPreference = "Stop"

cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi

@'
fastapi
uvicorn[standard]
pydantic
'@ | Set-Content -Path requirements.txt -Encoding UTF8

@'
pytest
httpx
'@ | Set-Content -Path requirements-dev.txt -Encoding UTF8

py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

New-Item -ItemType Directory -Force -Path `
  app,app\api,app\schemas,app\domain,app\repositories,app\services,app\seed,app\errors,tests | Out-Null

New-Item -ItemType File -Force -Path `
  app\__init__.py,app\api\__init__.py,app\schemas\__init__.py,app\domain\__init__.py,`
  app\repositories\__init__.py,app\services\__init__.py,app\seed\__init__.py,app\errors\__init__.py | Out-Null

@'
from fastapi import FastAPI


def create_app() -> FastAPI:
    return FastAPI(title="Waypoint Partner Source API", version="1.0.0")


app = create_app()
'@ | Set-Content -Path app\main.py -Encoding UTF8

@'
from fastapi.testclient import TestClient

from app.main import app


def test_app_starts() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code in {200, 404}
'@ | Set-Content -Path tests\test_app.py -Encoding UTF8

python -m pytest
```

Expected generated files:

```text
pyproject.toml or requirements.txt
.python-version if using uv
app/main.py
app/__init__.py
app/api/
app/schemas/
app/domain/
app/repositories/
app/services/
app/seed/
app/errors/
tests/test_app.py
```

## Expected Output

```text
1 passed
```

## Done Criteria

- [ ] `python -m pytest` or `uv run pytest` passes.
- [ ] App package is named `app`.
- [ ] Dependency files exist.
- [ ] `app/main.py` and `tests/test_app.py` exist.
- [ ] No real Partner Source endpoint behavior was added yet.

## Change Notes

- This task starts as a clean scaffold target and should be updated if the actual FastAPI setup differs from the draft commands.
- Keep the note short and factual if the module ends up using a slightly different toolchain or file layout.

## Stop / Do Not Add

- Do not add SQLAlchemy, Alembic, auth, Docker, or OpenAPI generation.
- Do not implement `/health` yet.
