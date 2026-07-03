# 06 - Seed Store And Repositories

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Create deterministic in-memory seed data and repository classes for FastAPI.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `7. Seed Data`
- `../../docs/active/data-and-seed-handoff.md`
- `../../partner-source-springboot/build-sequence/06-seed-store-and-repositories.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

Create these repository test files before implementation:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for Create these repository test files before implementation.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/repositories/test_orders_repository.py
tests/repositories/test_drivers_repository.py
tests/repositories/test_assignments_repository.py
tests/repositories/test_status_events_repository.py

```

`tests/repositories/test_orders_repository.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/repositories/test_orders_repository.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from app.domain.orders import OrderStatus
from app.repositories.orders import InMemoryOrderRepository
from app.seed.loader import load_seed_data


def test_find_existing_order_by_id() -> None:
    repo = InMemoryOrderRepository(load_seed_data())

    order = repo.find_by_id("ORD-1001")

    assert order is not None
    assert order.order_id == "ORD-1001"
    assert order.current_status == OrderStatus.OUT_FOR_DELIVERY


def test_missing_order_returns_none() -> None:
    repo = InMemoryOrderRepository(load_seed_data())

    assert repo.find_by_id("ORD-9999") is None

```

`tests/repositories/test_drivers_repository.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/repositories/test_drivers_repository.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from app.domain.drivers import DriverAvailabilityStatus
from app.repositories.drivers import InMemoryDriverRepository
from app.seed.loader import load_seed_data


def test_find_existing_driver_by_id() -> None:
    repo = InMemoryDriverRepository(load_seed_data())

    driver = repo.find_by_id("DRV-2001")

    assert driver is not None
    assert driver.driver_id == "DRV-2001"
    assert driver.availability_status == DriverAvailabilityStatus.AVAILABLE


def test_missing_driver_returns_none() -> None:
    repo = InMemoryDriverRepository(load_seed_data())

    assert repo.find_by_id("DRV-9999") is None

```

`tests/repositories/test_assignments_repository.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/repositories/test_assignments_repository.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from app.domain.assignments import DeliveryAssignmentStatus
from app.repositories.assignments import InMemoryAssignmentRepository
from app.seed.loader import load_seed_data


def test_find_active_assignments_for_driver() -> None:
    repo = InMemoryAssignmentRepository(load_seed_data())

    assignments = repo.find_by_driver_id("DRV-2001")

    assert [assignment.assignment_id for assignment in assignments] == [
        "ASN-3001",
        "ASN-3002",
    ]
    assert [assignment.order_id for assignment in assignments] == [
        "ORD-1001",
        "ORD-1002",
    ]


def test_available_driver_with_no_assignments_returns_empty_list() -> None:
    repo = InMemoryAssignmentRepository(load_seed_data())

    assert repo.find_by_driver_id("DRV-2003") == []


def test_completed_assignment_exists_but_is_not_active_driver_work() -> None:
    repo = InMemoryAssignmentRepository(load_seed_data())

    all_assignments = repo.find_all()
    completed = [assignment for assignment in all_assignments if assignment.assignment_id == "ASN-3003"]

    assert completed[0].status == DeliveryAssignmentStatus.COMPLETED
    assert "ASN-3003" not in [assignment.assignment_id for assignment in repo.find_by_driver_id("DRV-2001")]


def test_completed_assignment_can_be_found_by_order_id_for_invalid_transition_path() -> None:
    repo = InMemoryAssignmentRepository(load_seed_data())

    assignments = repo.find_by_order_id("ORD-1003")

    assert [assignment.assignment_id for assignment in assignments] == ["ASN-3003"]
    assert assignments[0].status == DeliveryAssignmentStatus.COMPLETED

```

`tests/repositories/test_status_events_repository.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/repositories/test_status_events_repository.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from app.domain.orders import OrderStatus
from app.repositories.status_events import InMemoryStatusEventRepository
from app.seed.loader import load_seed_data


def test_find_order_status_events_in_chronological_order() -> None:
    repo = InMemoryStatusEventRepository(load_seed_data())

    events = repo.find_by_order_id("ORD-1001")

    assert [event.event_id for event in events] == [
        "EVT-4001",
        "EVT-4002",
        "EVT-4003",
        "EVT-4004",
        "EVT-4005",
    ]
    assert events[-1].new_status == OrderStatus.OUT_FOR_DELIVERY


def test_missing_order_status_events_returns_empty_list() -> None:
    repo = InMemoryStatusEventRepository(load_seed_data())

    assert repo.find_by_order_id("ORD-9999") == []

```

Expected first result before repository implementation:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `ModuleNotFoundError for app.repositories.orders/drivers/assignments/status_events`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
ModuleNotFoundError for app.repositories.orders/drivers/assignments/status_events

```
## File Map

Domain:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/domain/orders.py`, `app/domain/drivers.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/domain/orders.py
app/domain/drivers.py
app/domain/assignments.py
```

Seed:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/seed/manifest.py`, `app/seed/loader.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/seed/manifest.py
app/seed/loader.py
app/seed/store.py
```

Repositories:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/repositories/orders.py`, `app/repositories/drivers.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/repositories/orders.py
app/repositories/drivers.py
app/repositories/assignments.py
app/repositories/status_events.py

```

Use dataclasses or plain classes for internal domain objects. Use Pydantic at the API schema edge.

## Exact Code

Replace `app/domain/orders.py` with this expanded domain file:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/domain/orders.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERY_ATTEMPTED = "DELIVERY_ATTEMPTED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class ActorType(str, Enum):
    SYSTEM = "SYSTEM"
    DRIVER = "DRIVER"
    SUPPORT_AGENT = "SUPPORT_AGENT"


@dataclass(frozen=True)
class DeliveryOrder:
    order_id: str
    current_status: OrderStatus
    status_label: str
    recipient_name: str
    delivery_address_summary: str
    estimated_delivery_at: datetime | None = None
    delivery_window_start: datetime | None = None
    delivery_window_end: datetime | None = None
    current_location: str | None = None
    assigned_driver_id: str | None = None
    assigned_driver_name: str | None = None
    last_updated_at: datetime | None = None


@dataclass(frozen=True)
class OrderStatusEvent:
    event_id: str
    order_id: str
    previous_status: OrderStatus | None
    new_status: OrderStatus
    status_label: str
    occurred_at: datetime
    actor_type: ActorType
    actor_id: str

```

Create `app/domain/drivers.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/domain/drivers.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from dataclasses import dataclass
from enum import Enum


class DriverAvailabilityStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    OFFLINE = "OFFLINE"


@dataclass(frozen=True)
class DeliveryDriver:
    driver_id: str
    display_name: str
    availability_status: DriverAvailabilityStatus

```

Replace `app/domain/assignments.py` with this expanded assignment model:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/domain/assignments.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from dataclasses import dataclass
from enum import Enum


class DeliveryAssignmentStatus(str, Enum):
    ASSIGNED = "ASSIGNED"
    ACCEPTED = "ACCEPTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class DeliveryAssignment:
    driver_id: str
    order_id: str
    status: DeliveryAssignmentStatus = DeliveryAssignmentStatus.ASSIGNED
    assignment_id: str | None = None

```

Create `app/seed/store.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/seed/store.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from dataclasses import dataclass

from app.domain.assignments import DeliveryAssignment
from app.domain.drivers import DeliveryDriver
from app.domain.orders import DeliveryOrder, OrderStatusEvent


@dataclass(frozen=True)
class SeedDataStore:
    orders: dict[str, DeliveryOrder]
    drivers: dict[str, DeliveryDriver]
    assignments: dict[str, DeliveryAssignment]
    status_events_by_order_id: dict[str, list[OrderStatusEvent]]

```

Create `app/seed/manifest.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/seed/manifest.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
SERVICE_NAME = "partner-source"

ORDER_IDS = {"ORD-1001", "ORD-1002", "ORD-1003", "ORD-1004"}
DRIVER_IDS = {"DRV-2001", "DRV-2002", "DRV-2003"}
ASSIGNMENT_IDS = {"ASN-3001", "ASN-3002", "ASN-3003", "ASN-3004"}
ACTIVE_SLICE_1_ASSIGNMENT_IDS = {"ASN-3001", "ASN-3002"}

```

Create `app/seed/loader.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/seed/loader.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from datetime import datetime, timezone

from app.domain.assignments import DeliveryAssignment, DeliveryAssignmentStatus
from app.domain.drivers import DeliveryDriver, DriverAvailabilityStatus
from app.domain.orders import ActorType, DeliveryOrder, OrderStatus, OrderStatusEvent
from app.seed.store import SeedDataStore


def _utc(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)


def load_seed_data() -> SeedDataStore:
    drivers = {
        "DRV-2001": DeliveryDriver("DRV-2001", "A. Kumar", DriverAvailabilityStatus.AVAILABLE),
        "DRV-2002": DeliveryDriver("DRV-2002", "B. Santos", DriverAvailabilityStatus.UNAVAILABLE),
        "DRV-2003": DeliveryDriver("DRV-2003", "C. Lee", DriverAvailabilityStatus.AVAILABLE),
    }

    orders = {
        "ORD-1001": DeliveryOrder(
            order_id="ORD-1001",
            current_status=OrderStatus.OUT_FOR_DELIVERY,
            status_label="Out for delivery",
            recipient_name="Jamie Tan",
            delivery_address_summary="Tampines, Singapore",
            assigned_driver_id="DRV-2001",
            assigned_driver_name="A. Kumar",
            last_updated_at=_utc("2026-07-02T09:00:00"),
        ),
        "ORD-1002": DeliveryOrder(
            order_id="ORD-1002",
            current_status=OrderStatus.IN_TRANSIT,
            status_label="In transit",
            recipient_name="Priya Nair",
            delivery_address_summary="Jurong East, Singapore",
            assigned_driver_id="DRV-2001",
            assigned_driver_name="A. Kumar",
            last_updated_at=_utc("2026-07-02T08:30:00"),
        ),
        "ORD-1003": DeliveryOrder(
            order_id="ORD-1003",
            current_status=OrderStatus.DELIVERED,
            status_label="Delivered",
            recipient_name="Mei Wong",
            delivery_address_summary="Woodlands, Singapore",
            assigned_driver_id="DRV-2001",
            assigned_driver_name="A. Kumar",
            last_updated_at=_utc("2026-07-01T18:00:00"),
        ),
        "ORD-1004": DeliveryOrder(
            order_id="ORD-1004",
            current_status=OrderStatus.OUT_FOR_DELIVERY,
            status_label="Out for delivery",
            recipient_name="Reserved Slice 2",
            delivery_address_summary="Singapore",
            assigned_driver_id="DRV-2001",
            assigned_driver_name="A. Kumar",
            last_updated_at=_utc("2026-07-02T10:00:00"),
        ),
    }

    assignments = {
        "ASN-3001": DeliveryAssignment("DRV-2001", "ORD-1001", DeliveryAssignmentStatus.ASSIGNED, "ASN-3001"),
        "ASN-3002": DeliveryAssignment("DRV-2001", "ORD-1002", DeliveryAssignmentStatus.ASSIGNED, "ASN-3002"),
        "ASN-3003": DeliveryAssignment("DRV-2001", "ORD-1003", DeliveryAssignmentStatus.COMPLETED, "ASN-3003"),
        "ASN-3004": DeliveryAssignment("DRV-2001", "ORD-1004", DeliveryAssignmentStatus.ASSIGNED, "ASN-3004"),
    }

    status_events_by_order_id = {
        "ORD-1001": [
            OrderStatusEvent("EVT-4001", "ORD-1001", None, OrderStatus.CREATED, "Created", _utc("2026-07-02T05:00:00"), ActorType.SYSTEM, "system"),
            OrderStatusEvent("EVT-4002", "ORD-1001", OrderStatus.CREATED, OrderStatus.CONFIRMED, "Confirmed", _utc("2026-07-02T06:00:00"), ActorType.SYSTEM, "system"),
            OrderStatusEvent("EVT-4003", "ORD-1001", OrderStatus.CONFIRMED, OrderStatus.PICKED_UP, "Picked up", _utc("2026-07-02T07:00:00"), ActorType.DRIVER, "DRV-2001"),
            OrderStatusEvent("EVT-4004", "ORD-1001", OrderStatus.PICKED_UP, OrderStatus.IN_TRANSIT, "In transit", _utc("2026-07-02T08:00:00"), ActorType.DRIVER, "DRV-2001"),
            OrderStatusEvent("EVT-4005", "ORD-1001", OrderStatus.IN_TRANSIT, OrderStatus.OUT_FOR_DELIVERY, "Out for delivery", _utc("2026-07-02T09:00:00"), ActorType.DRIVER, "DRV-2001"),
        ],
        "ORD-1002": [
            OrderStatusEvent("EVT-4101", "ORD-1002", None, OrderStatus.CREATED, "Created", _utc("2026-07-02T05:30:00"), ActorType.SYSTEM, "system"),
            OrderStatusEvent("EVT-4102", "ORD-1002", OrderStatus.CREATED, OrderStatus.CONFIRMED, "Confirmed", _utc("2026-07-02T06:30:00"), ActorType.SYSTEM, "system"),
            OrderStatusEvent("EVT-4103", "ORD-1002", OrderStatus.CONFIRMED, OrderStatus.PICKED_UP, "Picked up", _utc("2026-07-02T07:30:00"), ActorType.DRIVER, "DRV-2001"),
            OrderStatusEvent("EVT-4104", "ORD-1002", OrderStatus.PICKED_UP, OrderStatus.IN_TRANSIT, "In transit", _utc("2026-07-02T08:30:00"), ActorType.DRIVER, "DRV-2001"),
        ],
        "ORD-1003": [
            OrderStatusEvent("EVT-4201", "ORD-1003", None, OrderStatus.CREATED, "Created", _utc("2026-07-01T15:00:00"), ActorType.SYSTEM, "system"),
            OrderStatusEvent("EVT-4202", "ORD-1003", OrderStatus.CREATED, OrderStatus.OUT_FOR_DELIVERY, "Out for delivery", _utc("2026-07-01T17:00:00"), ActorType.DRIVER, "DRV-2001"),
            OrderStatusEvent("EVT-4203", "ORD-1003", OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED, "Delivered", _utc("2026-07-01T18:00:00"), ActorType.DRIVER, "DRV-2001"),
        ],
    }

    return SeedDataStore(
        orders=orders,
        drivers=drivers,
        assignments=assignments,
        status_events_by_order_id=status_events_by_order_id,
    )

```

Create `app/repositories/orders.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/repositories/orders.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.domain.orders import DeliveryOrder
from app.seed.store import SeedDataStore


class InMemoryOrderRepository:
    def __init__(self, store: SeedDataStore) -> None:
        self._store = store

    def find_by_id(self, order_id: str) -> DeliveryOrder | None:
        return self._store.orders.get(order_id)

    def save(self, order: DeliveryOrder) -> None:
        self._store.orders[order.order_id] = order

```

Create `app/repositories/drivers.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/repositories/drivers.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.domain.drivers import DeliveryDriver
from app.seed.store import SeedDataStore


class InMemoryDriverRepository:
    def __init__(self, store: SeedDataStore) -> None:
        self._store = store

    def find_by_id(self, driver_id: str) -> DeliveryDriver | None:
        return self._store.drivers.get(driver_id)

```

Create `app/repositories/assignments.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/repositories/assignments.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.domain.assignments import DeliveryAssignment, DeliveryAssignmentStatus
from app.seed.manifest import ACTIVE_SLICE_1_ASSIGNMENT_IDS
from app.seed.store import SeedDataStore


class InMemoryAssignmentRepository:
    def __init__(self, store: SeedDataStore) -> None:
        self._store = store

    def find_by_driver_id(self, driver_id: str) -> list[DeliveryAssignment]:
        return [
            assignment
            for assignment in self._store.assignments.values()
            if assignment.driver_id == driver_id
            and assignment.assignment_id in ACTIVE_SLICE_1_ASSIGNMENT_IDS
            and assignment.status in {
                DeliveryAssignmentStatus.ASSIGNED,
                DeliveryAssignmentStatus.ACCEPTED,
            }
        ]

    def find_by_order_id(self, order_id: str) -> list[DeliveryAssignment]:
        return [
            assignment
            for assignment in self._store.assignments.values()
            if assignment.order_id == order_id
        ]

    def find_all(self) -> list[DeliveryAssignment]:
        return list(self._store.assignments.values())

```

Create `app/repositories/status_events.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/repositories/status_events.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.domain.orders import OrderStatusEvent
from app.seed.store import SeedDataStore


class InMemoryStatusEventRepository:
    def __init__(self, store: SeedDataStore) -> None:
        self._store = store

    def find_by_order_id(self, order_id: str) -> list[OrderStatusEvent]:
        return sorted(
            self._store.status_events_by_order_id.get(order_id, []),
            key=lambda event: event.occurred_at,
        )

    def append(self, event: OrderStatusEvent) -> None:
        self._store.status_events_by_order_id.setdefault(event.order_id, []).append(event)

```

Repository rule:

Repositories return domain objects only. They must not import FastAPI, Pydantic schemas, HTTP exceptions, SQLAlchemy, or database clients.

Active driver work rule:

`find_by_driver_id("DRV-2001")` is the Slice 1 active-driver-work query. It must return only `ASN-3001` and `ASN-3002`. Keep `ASN-3004` in seed data because the agreed spec reserves it as a Slice 2 fixture, but do not return it from the Slice 1 active assignment query.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/repositories
python -m pytest
```

## Done Criteria

- [x] Seed data matches agreed IDs and scenarios.
- [x] Repositories are in-memory only.
- [x] Tests prove missing IDs.
- [x] `find_by_driver_id("DRV-2001")` returns only `ASN-3001` and `ASN-3002`.
- [x] `ASN-3004` remains seeded but is not returned as active Slice 1 driver work.
- [x] No SQLAlchemy or database dependency exists.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Returning `ASN-3004` from `find_by_driver_id` just because it is seeded as `ASSIGNED`; it is reserved for Slice 2.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add SQLAlchemy, Alembic, or database URLs.
- Do not add API routers in this step.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
