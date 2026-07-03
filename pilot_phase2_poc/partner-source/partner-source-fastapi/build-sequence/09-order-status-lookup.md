# 09 - Order Status Lookup

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `GET /api/v1/orders/{orderId}/status`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `8. Response Shapes` and `10. Acceptance Scenarios`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/09-order-status-lookup.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `tests/services/test_order_status_service.py`, `tests/api/test_order_status_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/services/test_order_status_service.py
tests/api/test_order_status_endpoint.py
```

`tests/services/test_order_status_service.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/services/test_order_status_service.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from app.repositories.orders import InMemoryOrderRepository
from app.seed.loader import load_seed_data
from app.services.order_status import OrderStatusService


def test_get_order_status_for_seeded_order() -> None:
    service = OrderStatusService(InMemoryOrderRepository(load_seed_data()))

    response = service.get_order_status("ORD-1001")

    assert response is not None
    assert response.orderId == "ORD-1001"
    assert response.currentStatus == "OUT_FOR_DELIVERY"
    assert response.assignedDriver is not None
    assert response.assignedDriver.driverId == "DRV-2001"


def test_missing_order_returns_none() -> None:
    service = OrderStatusService(InMemoryOrderRepository(load_seed_data()))

    assert service.get_order_status("ORD-9999") is None

```

`tests/api/test_order_status_endpoint.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/api/test_order_status_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from fastapi.testclient import TestClient

from app.main import app


def test_get_order_status_returns_contract_shape() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-1001/status")

    assert response.status_code == 200
    body = response.json()
    assert body["orderId"] == "ORD-1001"
    assert body["currentStatus"] == "OUT_FOR_DELIVERY"
    assert body["statusLabel"] == "Out for delivery"
    assert body["assignedDriver"]["driverId"] == "DRV-2001"


def test_get_missing_order_returns_404() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-9999/status")

    assert response.status_code == 404

```

Task 10 will tighten the missing-order response body to the shared ProblemDetail envelope.
## File Map

Schemas:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/schemas/orders.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/schemas/orders.py
```

Service/router:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/services/order_status.py`, `app/api/orders.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/services/order_status.py
app/api/orders.py
```

Update:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/main.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/main.py
```

Register the orders router.

## Exact Code

Create `app/schemas/orders.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/schemas/orders.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from datetime import datetime

from pydantic import BaseModel

from app.domain.orders import OrderStatus


class AssignedDriverResponse(BaseModel):
    driverId: str
    displayName: str


class DeliveryWindowResponse(BaseModel):
    start: datetime | None = None
    end: datetime | None = None


class LocationSnapshotResponse(BaseModel):
    label: str
    latitude: float | None = None
    longitude: float | None = None
    capturedAt: datetime | None = None


class OrderStatusResponse(BaseModel):
    orderId: str
    currentStatus: OrderStatus
    statusLabel: str
    estimatedDeliveryAt: datetime | None = None
    deliveryWindow: DeliveryWindowResponse
    currentLocation: LocationSnapshotResponse | None = None
    assignedDriver: AssignedDriverResponse | None = None
    lastUpdatedAt: datetime | None = None

```

Create `app/services/order_status.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/services/order_status.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.repositories.orders import InMemoryOrderRepository
from app.schemas.orders import (
    AssignedDriverResponse,
    DeliveryWindowResponse,
    LocationSnapshotResponse,
    OrderStatusResponse,
)


class OrderStatusService:
    def __init__(self, order_repository: InMemoryOrderRepository) -> None:
        self._order_repository = order_repository

    def get_order_status(self, order_id: str) -> OrderStatusResponse | None:
        order = self._order_repository.find_by_id(order_id)
        if order is None:
            return None

        assigned_driver = None
        if order.assigned_driver_id is not None and order.assigned_driver_name is not None:
            assigned_driver = AssignedDriverResponse(
                driverId=order.assigned_driver_id,
                displayName=order.assigned_driver_name,
            )

        current_location = None
        if order.current_location is not None:
            current_location = LocationSnapshotResponse(label=order.current_location)

        return OrderStatusResponse(
            orderId=order.order_id,
            currentStatus=order.current_status,
            statusLabel=order.status_label,
            estimatedDeliveryAt=order.estimated_delivery_at,
            deliveryWindow=DeliveryWindowResponse(
                start=order.delivery_window_start,
                end=order.delivery_window_end,
            ),
            currentLocation=current_location,
            assignedDriver=assigned_driver,
            lastUpdatedAt=order.last_updated_at,
        )

```

Create `app/api/orders.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/api/orders.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from fastapi import APIRouter, HTTPException, status

from app.repositories.orders import InMemoryOrderRepository
from app.schemas.orders import OrderStatusResponse
from app.seed.loader import load_seed_data
from app.services.order_status import OrderStatusService

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])
_STORE = load_seed_data()


@router.get("/{order_id}/status", response_model=OrderStatusResponse)
def get_order_status(order_id: str) -> OrderStatusResponse:
    service = OrderStatusService(InMemoryOrderRepository(_STORE))
    response = service.get_order_status(order_id)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return response

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


def create_app() -> FastAPI:
    app = FastAPI(title="Waypoint Partner Source API", version="1.0.0")
    app.include_router(health_router)
    app.include_router(orders_router)
    return app


app = create_app()

```

This task may use `HTTPException` temporarily. Task 10 replaces that temporary error behavior with the shared `ProblemDetail` envelope.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/services/test_order_status_service.py tests/api/test_order_status_endpoint.py
python -m pytest
```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `Invoke-RestMethod http://localhost:8000/api/v1/orders/ORD-1001/status`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod http://localhost:8000/api/v1/orders/ORD-1001/status
```

## Done Criteria

- [x] Success service and API tests pass.
- [x] Missing order test exists.
- [x] Invalid path ID validation remains deferred to Task 10.
- [x] JSON uses OpenAPI field names, such as `orderId` and `currentStatus`.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not implement timeline here.
- Do not implement status-event mutation.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Pre-flight aligned `currentLocation` and `deliveryWindow` guidance with the OpenAPI-style response shape before implementation.
- Marked done after focused order-status tests and the full FastAPI suite passed.
