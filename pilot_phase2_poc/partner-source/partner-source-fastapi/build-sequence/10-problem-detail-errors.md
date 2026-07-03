# 10 - ProblemDetail Errors

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Centralize the shared ProblemDetail-style error envelope in FastAPI.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `9. Error Shape`
- `../../docs/contracts/shared-error-contract.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/10-problem-detail-errors.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `tests/api/test_problem_detail_errors.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/api/test_problem_detail_errors.py
```

Use this exact test file before implementation:

**Test Block Explanation**

- What this block does: Shows the test code to write first for Use this exact test file before implementation.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from fastapi.testclient import TestClient

from app.main import app


def assert_problem_detail(body: dict, error_code: str, status: int) -> None:
    assert body["type"]
    assert body["title"]
    assert body["status"] == status
    assert body["detail"]
    assert body["instance"]
    assert body["errorCode"] == error_code
    assert body["correlationId"]


def test_missing_order_uses_problem_detail() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-9999/status")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")
    assert_problem_detail(response.json(), "ORDER_NOT_FOUND", 404)


def test_invalid_order_id_uses_invalid_request_problem_detail() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/INVALID/status")

    assert response.status_code == 400
    assert_problem_detail(response.json(), "INVALID_REQUEST", 400)


def test_deprecated_transition_code_is_not_returned() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-9999/status")

    assert "ORDER_TRANSITION_INVALID" not in response.text

```

Expected first result before implementation:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `AssertionError because FastAPI default errors do not match ProblemDetail`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
AssertionError because FastAPI default errors do not match ProblemDetail

```
## File Map

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/errors/exceptions.py`, `app/errors/handlers.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/errors/exceptions.py
app/errors/handlers.py
app/schemas/errors.py
```

Update:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/main.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/main.py
```

Register exception handlers in `create_app()`.

Error handler output must match the shared contract exactly.

## Exact Code

Create `app/schemas/errors.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/schemas/errors.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from pydantic import BaseModel


class ProblemDetail(BaseModel):
    type: str
    title: str
    status: int
    detail: str
    instance: str
    errorCode: str
    correlationId: str

```

Create `app/errors/exceptions.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/errors/exceptions.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
class PartnerSourceError(Exception):
    def __init__(self, status_code: int, error_code: str, title: str, detail: str) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.title = title
        self.detail = detail


class InvalidRequestError(PartnerSourceError):
    def __init__(self, detail: str = "Invalid request.") -> None:
        super().__init__(400, "INVALID_REQUEST", "Invalid request", detail)


class OrderNotFoundError(PartnerSourceError):
    def __init__(self, order_id: str) -> None:
        super().__init__(404, "ORDER_NOT_FOUND", "Order not found", f"Order {order_id} was not found.")


class DriverNotFoundError(PartnerSourceError):
    def __init__(self, driver_id: str) -> None:
        super().__init__(404, "DRIVER_NOT_FOUND", "Driver not found", f"Driver {driver_id} was not found.")


class OrderNotAssignedToDriverError(PartnerSourceError):
    def __init__(self, order_id: str, driver_id: str) -> None:
        super().__init__(
            403,
            "ORDER_NOT_ASSIGNED_TO_DRIVER",
            "Order not assigned to driver",
            f"Order {order_id} is not assigned to driver {driver_id}.",
        )


class InvalidStatusTransitionError(PartnerSourceError):
    def __init__(self, detail: str = "Invalid status transition.") -> None:
        super().__init__(409, "INVALID_STATUS_TRANSITION", "Invalid status transition", detail)


class InvalidStatusEventError(PartnerSourceError):
    def __init__(self, detail: str = "Invalid status event.") -> None:
        super().__init__(422, "INVALID_STATUS_EVENT", "Invalid status event", detail)

```

Create `app/errors/handlers.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/errors/handlers.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.errors.exceptions import InvalidRequestError, PartnerSourceError
from app.schemas.errors import ProblemDetail


def _correlation_id(request: Request) -> str:
    return request.headers.get("X-Correlation-Id", "local-dev")


def _problem(request: Request, error: PartnerSourceError) -> ProblemDetail:
    return ProblemDetail(
        type=f"https://waypoint.local/problems/{error.error_code.lower()}",
        title=error.title,
        status=error.status_code,
        detail=error.detail,
        instance=str(request.url.path),
        errorCode=error.error_code,
        correlationId=_correlation_id(request),
    )


async def partner_source_error_handler(request: Request, exc: PartnerSourceError) -> JSONResponse:
    problem = _problem(request, exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=problem.model_dump(),
        media_type="application/problem+json",
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    error = InvalidRequestError("Request validation failed.")
    problem = _problem(request, error)
    return JSONResponse(
        status_code=400,
        content=problem.model_dump(),
        media_type="application/problem+json",
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(PartnerSourceError, partner_source_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)

```

Update `app/main.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/main.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.orders import router as orders_router
from app.errors.handlers import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(title="Waypoint Partner Source API", version="1.0.0")
    register_exception_handlers(app)
    app.include_router(health_router)
    app.include_router(orders_router)
    return app


app = create_app()

```

Replace temporary `HTTPException` usage in `app/api/orders.py` with `OrderNotFoundError`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `HTTPException`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.errors.exceptions import OrderNotFoundError


if response is None:
    raise OrderNotFoundError(order_id)

```

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/api/test_problem_detail_errors.py
python -m pytest

```

Manual missing-order check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Manual missing-order check.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
try {
  Invoke-RestMethod http://localhost:8000/api/v1/orders/ORD-9999/status
} catch {
  $_.ErrorDetails.Message
}

```

## Done Criteria

- [x] All error responses include required fields.
- [x] HTTP status matches body `status`.
- [x] `correlationId` is present.
- [x] `application/problem+json` is used for API errors.
- [x] FastAPI validation errors map to `400 INVALID_REQUEST`.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not expose stack traces.
- Do not rename `correlationId` to `requestId`.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Implemented and marked done after focused tests and the full pytest suite passed.
