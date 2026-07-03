# 13 - Driver Assignments

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `GET /api/v1/drivers/{driverId}/assignments`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `7. Seed Data`, `8. Response Shapes`, and `10. Acceptance Scenarios`
- `../../docs/active/data-and-seed-handoff.md`
- `../../partner-source-springboot/build-sequence/13-driver-assignments.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `tests/services/test_driver_assignments_service.py`, `tests/api/test_driver_assignments_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/services/test_driver_assignments_service.py
tests/api/test_driver_assignments_endpoint.py
```

`tests/services/test_driver_assignments_service.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/services/test_driver_assignments_service.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.repositories.orders import InMemoryOrderRepository
from app.seed.loader import load_seed_data
from app.services.driver_assignments import DriverAssignmentsService


def test_list_active_assignments_for_driver() -> None:
    store = load_seed_data()
    service = DriverAssignmentsService(
        InMemoryDriverRepository(store),
        InMemoryAssignmentRepository(store),
        InMemoryOrderRepository(store),
    )

    response = service.list_assignments("DRV-2001", page=1, page_size=20)

    assert response.driverId == "DRV-2001"
    assert response.totalItems == 2
    assert [item.orderId for item in response.items] == ["ORD-1001", "ORD-1002"]


def test_available_driver_with_no_work_returns_empty_page() -> None:
    store = load_seed_data()
    service = DriverAssignmentsService(
        InMemoryDriverRepository(store),
        InMemoryAssignmentRepository(store),
        InMemoryOrderRepository(store),
    )

    response = service.list_assignments("DRV-2003", page=1, page_size=20)

    assert response.items == []
    assert response.totalItems == 0

```

`tests/api/test_driver_assignments_endpoint.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/api/test_driver_assignments_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from fastapi.testclient import TestClient

from app.main import app


def test_list_driver_assignments_returns_two_active_items() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20")

    assert response.status_code == 200
    body = response.json()
    assert body["driverId"] == "DRV-2001"
    assert body["totalItems"] == 2
    assert [item["orderId"] for item in body["items"]] == ["ORD-1001", "ORD-1002"]


def test_driver_with_no_assignments_returns_empty_items() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/drivers/DRV-2003/assignments?page=1&pageSize=20")

    assert response.status_code == 200
    assert response.json()["items"] == []

```
## File Map

Extend:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for Extend.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/schemas/drivers.py
app/services/driver_assignments.py
app/api/drivers.py
```

Use order and assignment repositories to enrich assignment items.

## Exact Code

Extend `app/schemas/drivers.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/schemas/drivers.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
class DriverAssignmentItem(BaseModel):
    assignmentId: str
    orderId: str
    assignmentStatus: DeliveryAssignmentStatus
    currentStatus: OrderStatus
    recipientName: str
    deliveryAddressSummary: str
    deliveryWindow: DeliveryWindowResponse
    lastUpdatedAt: datetime


class DriverAssignmentsResponse(BaseModel):
    driverId: str
    items: list[DriverAssignmentItem]
    page: int
    pageSize: int
    totalItems: int

```

Create `app/services/driver_assignments.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/services/driver_assignments.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.errors.exceptions import DriverNotFoundError
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.repositories.orders import InMemoryOrderRepository
from app.schemas.drivers import DriverAssignmentItem, DriverAssignmentsResponse
from app.schemas.orders import DeliveryWindowResponse


class DriverAssignmentsService:
    def __init__(
        self,
        driver_repository: InMemoryDriverRepository,
        assignment_repository: InMemoryAssignmentRepository,
        order_repository: InMemoryOrderRepository,
    ) -> None:
        self._driver_repository = driver_repository
        self._assignment_repository = assignment_repository
        self._order_repository = order_repository

    def list_assignments(
        self,
        driver_id: str,
        status: OrderStatus | None,
        page: int,
        page_size: int,
    ) -> DriverAssignmentsResponse:
        driver = self._driver_repository.find_by_id(driver_id)
        if driver is None:
            raise DriverNotFoundError(driver_id)

        items: list[DriverAssignmentItem] = []
        for assignment in self._assignment_repository.find_by_driver_id(driver_id):
            order = self._order_repository.find_by_id(assignment.order_id)
            if order is None:
                continue
            if status is not None and order.current_status != status:
                continue

            items.append(
                DriverAssignmentItem(
                    assignmentId=assignment.assignment_id or "",
                    orderId=assignment.order_id,
                    assignmentStatus=assignment.status,
                    currentStatus=order.current_status,
                    recipientName=order.recipient_name,
                    deliveryAddressSummary=order.delivery_address_summary,
                    deliveryWindow=DeliveryWindowResponse(
                        start=order.delivery_window_start,
                        end=order.delivery_window_end,
                    ),
                    lastUpdatedAt=order.last_updated_at,
                )
            )

        start = (page - 1) * page_size
        end = start + page_size

        return DriverAssignmentsResponse(
            driverId=driver_id,
            items=items[start:end],
            page=page,
            pageSize=page_size,
            totalItems=len(items),
        )

```

Extend `app/api/drivers.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/api/drivers.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.repositories.orders import InMemoryOrderRepository
from app.schemas.drivers import DriverAssignmentsResponse
from app.services.driver_assignments import DriverAssignmentsService


@router.get("/{driver_id}/assignments", response_model=DriverAssignmentsResponse)
def list_driver_assignments(
    driver_id: str,
    status: OrderStatus | None = None,
    page: int = 1,
    pageSize: int = 20,
) -> DriverAssignmentsResponse:
    service = DriverAssignmentsService(
        InMemoryDriverRepository(_STORE),
        InMemoryAssignmentRepository(_STORE),
        InMemoryOrderRepository(_STORE),
    )
    return service.list_assignments(driver_id, status, page, pageSize)

```

Expected seed behavior:

- `DRV-2001` returns `totalItems = 2`, with `ORD-1001` and `ORD-1002`.
- `DRV-2003` returns `items = []` and `totalItems = 0`.
- `DRV-9999` returns `404 DRIVER_NOT_FOUND`.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/services/test_driver_assignments_service.py tests/api/test_driver_assignments_endpoint.py
python -m pytest
```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `Invoke-RestMethod "http://localhost:8000/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20"`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod "http://localhost:8000/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20"
```

## Done Criteria

- [x] Active assignment list is correct.
- [x] Empty assignment list returns `items: []`.
- [x] Pagination fields match OpenAPI.
- [x] Missing driver and validation errors use ProblemDetail.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add assignment creation endpoints.
- Do not include completed `ASN-3003` as active work.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Implemented with contract-correct `pageSize` and marked done after focused tests and the full pytest suite passed.
