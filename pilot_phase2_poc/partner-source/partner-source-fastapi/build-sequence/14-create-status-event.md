# 14 - Create Status Event

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `POST /api/v1/orders/{orderId}/status-events`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `6`, `7`, `8`, `9`, and `10`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../docs/contracts/shared-error-contract.md`
- `../../partner-source-springboot/build-sequence/14-create-status-event.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `tests/services/test_status_events_service.py`, `tests/api/test_create_status_event_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/services/test_status_events_service.py
tests/api/test_create_status_event_endpoint.py
```

`tests/services/test_status_events_service.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/services/test_status_events_service.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from datetime import datetime, timezone

import pytest

from app.errors.exceptions import InvalidStatusTransitionError, OrderNotAssignedToDriverError
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.repositories.orders import InMemoryOrderRepository
from app.repositories.status_events import InMemoryStatusEventRepository
from app.schemas.orders import CreateStatusEventRequest
from app.seed.loader import load_seed_data
from app.services.status_events import CreateStatusEventService


def build_service() -> CreateStatusEventService:
    store = load_seed_data()
    return CreateStatusEventService(
        InMemoryOrderRepository(store),
        InMemoryDriverRepository(store),
        InMemoryAssignmentRepository(store),
        InMemoryStatusEventRepository(store),
    )


def test_assigned_driver_can_mark_order_delivered() -> None:
    service = build_service()

    response = service.create_status_event(
        "ORD-1001",
        CreateStatusEventRequest(
            driverId="DRV-2001",
            status="DELIVERED",
            occurredAt=datetime.now(timezone.utc),
        ),
    )

    assert response.previousStatus == "OUT_FOR_DELIVERY"
    assert response.newStatus == "DELIVERED"
    assert response.orderCurrentStatus == "DELIVERED"


def test_unassigned_driver_is_rejected_before_transition_check() -> None:
    service = build_service()

    with pytest.raises(OrderNotAssignedToDriverError):
        service.create_status_event(
            "ORD-1001",
            CreateStatusEventRequest(driverId="DRV-2002", status="DELIVERED"),
        )


def test_delivered_order_reaches_invalid_transition_path() -> None:
    service = build_service()

    with pytest.raises(InvalidStatusTransitionError):
        service.create_status_event(
            "ORD-1003",
            CreateStatusEventRequest(driverId="DRV-2001", status="OUT_FOR_DELIVERY"),
        )

```

`tests/api/test_create_status_event_endpoint.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/api/test_create_status_event_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app


def test_create_status_event_returns_201_and_mutates_order_status() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        json={
            "driverId": "DRV-2001",
            "status": "DELIVERED",
            "occurredAt": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 201
    assert response.json()["orderCurrentStatus"] == "DELIVERED"


def test_unassigned_driver_returns_403_problem_detail() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        json={"driverId": "DRV-2002", "status": "DELIVERED"},
    )

    assert response.status_code == 403
    assert response.json()["errorCode"] == "ORDER_NOT_ASSIGNED_TO_DRIVER"

```
## File Map

Extend schemas:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for Extend schemas.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/schemas/orders.py
```

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/services/status_events.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/services/status_events.py
```

Extend:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for Extend.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/api/orders.py
```

Service order:

1. Validate order exists.
2. Validate driver exists.
3. Validate assignment authorization.
4. Validate status transition.
5. Validate event semantics.
6. Append event.
7. Update order current status.
8. Return response.

## Exact Code

Extend `app/schemas/orders.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/schemas/orders.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.domain.orders import ActorType


class LocationSnapshot(BaseModel):
    label: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    capturedAt: datetime | None = None


class CreateStatusEventRequest(BaseModel):
    driverId: str
    status: OrderStatus
    occurredAt: datetime | None = None
    location: LocationSnapshot | None = None
    note: str | None = None
    proofOfDeliveryAvailable: bool | None = None


class StatusEventResponse(BaseModel):
    eventId: str
    orderId: str
    previousStatus: OrderStatus
    newStatus: OrderStatus
    statusLabel: str
    occurredAt: datetime
    actorType: ActorType
    actorId: str
    location: LocationSnapshot | None = None
    note: str | None = None
    proofOfDeliveryAvailable: bool | None = None
    orderCurrentStatus: OrderStatus

```

Create `app/services/status_events.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/services/status_events.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from dataclasses import replace
from datetime import datetime, timedelta, timezone

from app.domain.orders import ActorType, OrderStatusEvent
from app.errors.exceptions import (
    DriverNotFoundError,
    InvalidStatusEventError,
    InvalidStatusTransitionError,
    OrderNotAssignedToDriverError,
    OrderNotFoundError,
)
from app.domain.policies import AssignmentAuthorizationPolicy, StatusTransitionPolicy
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.repositories.orders import InMemoryOrderRepository
from app.repositories.status_events import InMemoryStatusEventRepository
from app.schemas.orders import CreateStatusEventRequest, StatusEventResponse


STATUS_LABELS = {
    "CREATED": "Created",
    "CONFIRMED": "Confirmed",
    "PICKED_UP": "Picked up",
    "IN_TRANSIT": "In transit",
    "OUT_FOR_DELIVERY": "Out for delivery",
    "DELIVERY_ATTEMPTED": "Delivery attempted",
    "DELIVERED": "Delivered",
    "CANCELLED": "Cancelled",
}


class CreateStatusEventService:
    def __init__(
        self,
        order_repository: InMemoryOrderRepository,
        driver_repository: InMemoryDriverRepository,
        assignment_repository: InMemoryAssignmentRepository,
        status_event_repository: InMemoryStatusEventRepository,
    ) -> None:
        self._order_repository = order_repository
        self._driver_repository = driver_repository
        self._assignment_repository = assignment_repository
        self._status_event_repository = status_event_repository
        self._assignment_policy = AssignmentAuthorizationPolicy()
        self._transition_policy = StatusTransitionPolicy()

    def create_status_event(
        self,
        order_id: str,
        request: CreateStatusEventRequest,
    ) -> StatusEventResponse:
        order = self._order_repository.find_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)

        driver = self._driver_repository.find_by_id(request.driverId)
        if driver is None:
            raise DriverNotFoundError(request.driverId)

        assignments = self._assignment_repository.find_by_order_id(order_id)
        if not self._assignment_policy.can_driver_update_order(request.driverId, order_id, assignments):
            raise OrderNotAssignedToDriverError(order_id, request.driverId)

        if not self._transition_policy.can_transition(order.current_status, request.status):
            raise InvalidStatusTransitionError(
                f"Cannot transition order {order_id} from {order.current_status.value} to {request.status.value}."
            )

        occurred_at = request.occurredAt or datetime.now(timezone.utc)
        if occurred_at > datetime.now(timezone.utc) + timedelta(minutes=5):
            raise InvalidStatusEventError("occurredAt cannot be in the far future.")

        event = OrderStatusEvent(
            event_id=self._next_event_id(order_id),
            order_id=order_id,
            previous_status=order.current_status,
            new_status=request.status,
            status_label=STATUS_LABELS[request.status.value],
            occurred_at=occurred_at,
            actor_type=ActorType.DRIVER,
            actor_id=request.driverId,
        )

        self._status_event_repository.append(event)
        updated_order = replace(
            order,
            current_status=request.status,
            status_label=STATUS_LABELS[request.status.value],
            last_updated_at=occurred_at,
        )
        self._order_repository.save(updated_order)

        return StatusEventResponse(
            eventId=event.event_id,
            orderId=event.order_id,
            previousStatus=event.previous_status,
            newStatus=event.new_status,
            statusLabel=event.status_label,
            occurredAt=event.occurred_at,
            actorType=event.actor_type,
            actorId=event.actor_id,
            location=request.location,
            note=request.note,
            proofOfDeliveryAvailable=request.proofOfDeliveryAvailable,
            orderCurrentStatus=updated_order.current_status,
        )

```

Extend `app/api/orders.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/api/orders.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from fastapi import status

from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.schemas.orders import CreateStatusEventRequest, StatusEventResponse
from app.services.status_events import CreateStatusEventService


@router.post(
    "/{order_id}/status-events",
    response_model=StatusEventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order_status_event(
    order_id: str,
    request: CreateStatusEventRequest,
) -> StatusEventResponse:
    service = CreateStatusEventService(
        InMemoryOrderRepository(_STORE),
        InMemoryDriverRepository(_STORE),
        InMemoryAssignmentRepository(_STORE),
        InMemoryStatusEventRepository(_STORE),
    )
    return service.create_status_event(order_id, request)

```

The validation order matters:

1. Missing order returns `404 ORDER_NOT_FOUND`.
2. Missing driver returns `404 DRIVER_NOT_FOUND`.
3. Existing but unassigned driver returns `403 ORDER_NOT_ASSIGNED_TO_DRIVER`.
4. Assigned driver with invalid lifecycle move returns `409 INVALID_STATUS_TRANSITION`.
5. Semantically invalid event data returns `422 INVALID_STATUS_EVENT`.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/services/test_status_events_service.py tests/api/test_create_status_event_endpoint.py
python -m pytest
```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `$body = @{`, `driverId = "DRV-2001"`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
$body = @{
  driverId = "DRV-2001"
  status = "DELIVERED"
  occurredAt = "2026-06-30T15:45:00+08:00"
  note = "Left with reception"
  proofOfDeliveryAvailable = $true
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/api/v1/orders/ORD-1001/status-events `
  -ContentType "application/json" `
  -Body $body

```

## Done Criteria

- [x] All success and negative tests pass.
- [x] Mutation is visible through status lookup and timeline.
- [x] Error status and `errorCode` match the shared contract.
- [x] No extra status-event fields are invented.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add proof upload, signatures, photos, delivery-attempt flows, or external integrations.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Implemented with generated next event IDs and a shared resettable in-memory app store; marked done after focused tests and the full pytest suite passed.
