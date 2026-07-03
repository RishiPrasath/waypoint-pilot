# 08 - Readiness Endpoint

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `GET /ready` to prove in-memory persistence and seed data are ready.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `3. Endpoints` and `8. Response Shapes`
- `../../docs/active/data-and-seed-handoff.md`
- `../../partner-source-springboot/build-sequence/08-readiness-endpoint.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `tests/services/test_readiness_service.py`, `tests/api/test_readiness_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/services/test_readiness_service.py
tests/api/test_readiness_endpoint.py
```

`tests/services/test_readiness_service.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/services/test_readiness_service.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from app.services.readiness import ReadinessService


def test_readiness_service_reports_seed_data_ready() -> None:
    checks = ReadinessService().check()

    assert checks == {
        "persistence": "UP",
        "seedData": "UP",
    }

```

`tests/api/test_readiness_endpoint.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/api/test_readiness_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from fastapi.testclient import TestClient

from app.main import app


def test_ready_returns_ready_response() -> None:
    client = TestClient(app)

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "READY",
        "service": "partner-source",
        "checks": {
            "persistence": "UP",
            "seedData": "UP",
        },
    }

```

Expected first result before implementation:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `ModuleNotFoundError for app.services.readiness or 404 for /ready`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
ModuleNotFoundError for app.services.readiness or 404 for /ready

```
## File Map

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/services/readiness.py`, `app/schemas/shared.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/services/readiness.py
app/schemas/shared.py
```

Update:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/api/health.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/api/health.py
```

## Exact Code

Create `app/services/readiness.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/services/readiness.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.seed.loader import load_seed_data


class ReadinessService:
    def check(self) -> dict[str, str]:
        store = load_seed_data()
        seed_data_loaded = bool(store.orders and store.drivers and store.assignments)

        return {
            "persistence": "UP",
            "seedData": "UP" if seed_data_loaded else "DOWN",
        }

```

Update `app/api/health.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/api/health.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schemas.shared import HealthResponse, ReadinessChecks, ReadinessResponse
from app.services.readiness import ReadinessService

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status="UP", service="partner-source")


@router.get("/ready", response_model=ReadinessResponse)
def get_readiness() -> ReadinessResponse | JSONResponse:
    checks = ReadinessService().check()
    ready = checks["persistence"] == "UP" and checks["seedData"] == "UP"
    body = ReadinessResponse(
        status="READY" if ready else "NOT_READY",
        service="partner-source",
        checks=ReadinessChecks(**checks),
    )

    if ready:
        return body

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=body.model_dump(),
    )

```

Expected ready response:

**Code Block Explanation**

- What this block does: Shows the exact JSON shape or response values for `{`, `"status": "READY",`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Use the field names and values as contract shape checks; spelling and casing matter.

```json
{
  "status": "READY",
  "service": "partner-source",
  "checks": {
    "persistence": "UP",
    "seedData": "UP"
  }
}

```

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/services/test_readiness_service.py tests/api/test_readiness_endpoint.py
python -m pytest

```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `Invoke-RestMethod http://localhost:8000/ready`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod http://localhost:8000/ready

```

## Done Criteria

- [x] Readiness tests pass.
- [x] Endpoint is outside `/api/v1`.
- [x] No database readiness check exists.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add database dependencies.
- Do not add deployment probe config.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Marked done after focused readiness tests and the full FastAPI suite passed.
