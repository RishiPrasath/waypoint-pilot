# 07 - Health Endpoint

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `GET /health`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `3. Endpoints` and `8. Response Shapes`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/07-health-endpoint.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `tests/api/test_health_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/api/test_health_endpoint.py
```

Use this exact test file before implementation:

**Test Block Explanation**

- What this block does: Shows the test code to write first for Use this exact test file before implementation.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_up() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "UP",
        "service": "partner-source",
    }

```

Expected first result before implementation:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `AssertionError because /health still returns 404`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
AssertionError because /health still returns 404

```
## File Map

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/api/health.py`, `app/schemas/shared.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/api/health.py
app/schemas/shared.py
```

Update:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/main.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/main.py
```

Include the health router in `create_app()`.

## Exact Code

Create `app/schemas/shared.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/schemas/shared.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class ReadinessChecks(BaseModel):
    persistence: str
    seedData: str


class ReadinessResponse(BaseModel):
    status: str
    service: str
    checks: ReadinessChecks

```

Create `app/api/health.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/api/health.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from fastapi import APIRouter

from app.schemas.shared import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status="UP", service="partner-source")

```

Update `app/main.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/main.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from fastapi import FastAPI

from app.api.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="Waypoint Partner Source API", version="1.0.0")
    app.include_router(health_router)
    return app


app = create_app()

```

The response body must be exactly:

**Code Block Explanation**

- What this block does: Shows the exact JSON shape or response values for The response body must be exactly.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Use the field names and values as contract shape checks; spelling and casing matter.

```json
{
  "status": "UP",
  "service": "partner-source"
}

```

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/api/test_health_endpoint.py
python -m pytest

```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `python -m uvicorn app.main:app --reload`, `Invoke-RestMethod http://localhost:8000/health`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m uvicorn app.main:app --reload
Invoke-RestMethod http://localhost:8000/health

```

## Done Criteria

- [x] TestClient test passes.
- [x] Endpoint is outside `/api/v1`.
- [x] JSON field names match OpenAPI.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add readiness logic here.
- Do not add external health check packages.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Marked done after `tests/api/test_health_endpoint.py` and the full FastAPI suite passed.
