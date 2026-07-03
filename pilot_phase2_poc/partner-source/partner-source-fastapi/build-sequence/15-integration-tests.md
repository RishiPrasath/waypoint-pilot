# 15 - Integration Tests

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Prove the FastAPI app works through the full TestClient stack.

## Source Docs To Read

- `../../docs/active/test-and-acceptance-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/15-integration-tests.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `tests/integration/test_slice1_flow.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/integration/test_slice1_flow.py
```

Use this exact integration test file:

**Test Block Explanation**

- What this block does: Shows the test code to write first for Use this exact integration test file.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app


def test_slice1_happy_path_status_event_flow() -> None:
    client = TestClient(app)

    before = client.get("/api/v1/orders/ORD-1001/status")
    assert before.status_code == 200
    assert before.json()["currentStatus"] == "OUT_FOR_DELIVERY"

    created = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        json={
            "driverId": "DRV-2001",
            "status": "DELIVERED",
            "occurredAt": datetime.now(timezone.utc).isoformat(),
        },
    )
    assert created.status_code == 201
    assert created.json()["previousStatus"] == "OUT_FOR_DELIVERY"
    assert created.json()["newStatus"] == "DELIVERED"
    assert created.json()["orderCurrentStatus"] == "DELIVERED"


def test_slice1_negative_paths_match_contract_error_codes() -> None:
    client = TestClient(app)

    unassigned = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        json={"driverId": "DRV-2002", "status": "DELIVERED"},
    )
    assert unassigned.status_code == 403
    assert unassigned.json()["errorCode"] == "ORDER_NOT_ASSIGNED_TO_DRIVER"

    missing_driver = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        json={"driverId": "DRV-9999", "status": "DELIVERED"},
    )
    assert missing_driver.status_code == 404
    assert missing_driver.json()["errorCode"] == "DRIVER_NOT_FOUND"

    invalid_transition = client.post(
        "/api/v1/orders/ORD-1003/status-events",
        json={"driverId": "DRV-2001", "status": "OUT_FOR_DELIVERY"},
    )
    assert invalid_transition.status_code == 409
    assert invalid_transition.json()["errorCode"] == "INVALID_STATUS_TRANSITION"

```
## File Map

Only add test support if needed. The app behavior should already exist from prior steps.

Possible helper:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for Possible helper.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
tests/helpers/json_assertions.py
```

## Exact Code

Create `tests/integration/test_slice1_flow.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `tests/integration/test_slice1_flow.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app


def test_slice1_happy_path_status_event_flow() -> None:
    client = TestClient(app)

    before = client.get("/api/v1/orders/ORD-1001/status")
    assert before.status_code == 200
    assert before.json()["currentStatus"] == "OUT_FOR_DELIVERY"

    created = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        json={
            "driverId": "DRV-2001",
            "status": "DELIVERED",
            "occurredAt": datetime.now(timezone.utc).isoformat(),
        },
    )
    assert created.status_code == 201
    assert created.json()["previousStatus"] == "OUT_FOR_DELIVERY"
    assert created.json()["newStatus"] == "DELIVERED"
    assert created.json()["orderCurrentStatus"] == "DELIVERED"


def test_slice1_negative_paths_match_contract_error_codes() -> None:
    client = TestClient(app)

    unassigned = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        json={"driverId": "DRV-2002", "status": "DELIVERED"},
    )
    assert unassigned.status_code == 403
    assert unassigned.json()["errorCode"] == "ORDER_NOT_ASSIGNED_TO_DRIVER"

    missing_driver = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        json={"driverId": "DRV-9999", "status": "DELIVERED"},
    )
    assert missing_driver.status_code == 404
    assert missing_driver.json()["errorCode"] == "DRIVER_NOT_FOUND"

    invalid_transition = client.post(
        "/api/v1/orders/ORD-1003/status-events",
        json={"driverId": "DRV-2001", "status": "OUT_FOR_DELIVERY"},
    )
    assert invalid_transition.status_code == 409
    assert invalid_transition.json()["errorCode"] == "INVALID_STATUS_TRANSITION"

```

Create `tests/integration/__init__.py` as an empty file if the folder needs package discovery.

Optional helper `tests/helpers/json_assertions.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `tests/helpers/json_assertions.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
def assert_problem_detail(body: dict, error_code: str, status: int) -> None:
    assert body["errorCode"] == error_code
    assert body["status"] == status
    assert body["type"]
    assert body["title"]
    assert body["detail"]
    assert body["instance"]
    assert body["correlationId"]

```

If you add the helper, use it in integration tests instead of repeating the same error-envelope assertions.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/integration/test_slice1_flow.py
python -m pytest
```

## Done Criteria

- [x] Main happy path works through HTTP.
- [x] Representative error path returns ProblemDetail.
- [x] Full pytest suite passes.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not start external services.
- Do not add databases.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Implemented and marked done after focused integration tests and the full pytest suite passed.
