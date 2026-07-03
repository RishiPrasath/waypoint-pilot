# 01 - Project Setup

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Create the FastAPI parity module with Python 3.12+, FastAPI, pytest, and one tiny passing test.

## Source Docs To Read

- `../../AGREED_SPEC.md`
- `../../docs/active/fastapi-implementation-handoff.md`
- `../../docs/support/implementation-schematic-and-task-sequence.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `tests/test_app.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/test_app.py
```

Use this exact smoke test:

**Test Block Explanation**

- What this block does: Shows the test code to write first for Use this exact smoke test.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from fastapi.testclient import TestClient

from app.main import app


def test_app_starts() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code in {200, 404}

```

Why `200` or `404` is allowed here:

This task only proves the app imports and starts. The real `/health` endpoint is implemented in task 07.
## File Map

Preferred `uv` setup:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `uv`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
pyproject.toml
.python-version
app/__init__.py
app/main.py
tests/test_app.py

```

Minimum dependencies:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for Minimum dependencies.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
fastapi
uvicorn[standard]
pydantic
pytest
httpx

```

## Exact Code

Create `.python-version`:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for `.python-version`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
3.12
```

Create `pyproject.toml`:

**Code Block Explanation**

- What this block does: Shows the exact TOML configuration for `pyproject.toml`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read bracketed sections first, then the package, dependency, and pytest settings inside each section.

```toml
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

```

Create `app/__init__.py` as an empty file.

Create `app/main.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/main.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from fastapi import FastAPI


def create_app() -> FastAPI:
    return FastAPI(title="Waypoint Partner Source API", version="1.0.0")


app = create_app()

```

Create `tests/test_app.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `tests/test_app.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from fastapi.testclient import TestClient

from app.main import app


def test_app_starts() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code in {200, 404}

```

Why `200` or `404` is allowed here:

This task only proves the FastAPI app imports and starts. The real `/health` endpoint is implemented in task 07.

## Commands To Run

### 1. Open The Module Folder

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for 1. Open The Module Folder.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
Get-ChildItem -Force
```

Expected before scaffold:

**Command Block Explanation**

- What this block does: Shows the exact text commands for `README.md`, `build-sequence`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
README.md
build-sequence
```

### 2. Check Tools

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for 2. Check Tools.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

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

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `uv --version`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

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

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `uv sync --all-extras --dev`, `uv run pytest`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
uv sync --all-extras --dev
uv run pytest

```

### 3B. Create The FastAPI Project With Virtualenv

Use this option if `uv` is not installed.

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `uv`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

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

**Command Block Explanation**

- What this block does: Shows the exact text commands for `pyproject.toml or requirements.txt`, `.python-version if using uv`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

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

## Done Criteria

- [x] `python -m pytest` or `uv run pytest` passes.
- [x] App package is named `app`.
- [x] Dependency files exist.
- [x] `app/main.py` and `tests/test_app.py` exist.
- [x] No real Partner Source endpoint behavior was added yet.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add SQLAlchemy, Alembic, auth, Docker, or OpenAPI generation.
- Do not implement `/health` yet.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- The scaffold was implemented with `uv`, matching the preferred path in the task instructions.
- The project uses Python 3.13 locally, which satisfies the `>=3.12` requirement from the build book.
- The first test passes, so the skeleton is ready for the next task.
