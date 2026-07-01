# FastAPI Partner Source Build Manual

This is the hand-build manual for the FastAPI Partner Source implementation.

Use the numbered build sequence first:

```text
build-sequence\00-index.md
```

Use this manual as supporting detail with:

```text
..\MANUAL_BUILD_SEQUENCE.md
```

Rule:

```text
mirror the contract behavior
-> write pytest first
-> see it fail for the right reason
-> write the smallest code
-> run focused pytest
-> run full pytest
-> mark the checklist
```

FastAPI is a parity implementation. It must not invent a second API.

## 0. Contract Sources

Before implementing behavior, check:

```text
..\docs\active\contract-handoff.md
..\docs\active\data-and-seed-handoff.md
..\docs\active\test-and-acceptance-handoff.md
..\docs\contracts\openapi\partner-source.v1.yaml
..\docs\contracts\shared-error-contract.md
```

## 1. Scaffold The Project

Recommended fresh layout:

```text
pyproject.toml
.python-version
app/
|-- __init__.py
|-- main.py
|-- api/
|-- schemas/
|-- domain/
|-- repositories/
|-- services/
|-- seed/
`-- errors/
tests/
|-- domain/
|-- repositories/
|-- services/
|-- api/
`-- contract/
```

Use Python 3.12 or newer.

## 2. Option A: Use `uv`

Create `.python-version`:

```text
3.12
```

Create `pyproject.toml`:

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
    "httpx",
    "pytest",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

Run:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
uv sync --all-extras --dev
uv run pytest
```

## 3. Option B: Use Requirements Files First

Create `requirements.txt`:

```text
fastapi
uvicorn[standard]
pydantic
```

Create `requirements-dev.txt`:

```text
httpx
pytest
```

Run:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
```

## 4. Minimal Application Code

`app/main.py`

```python
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="Waypoint Partner Source API", version="1.0.0")
    return app


app = create_app()
```

`tests/test_app.py`

```python
from fastapi.testclient import TestClient

from app.main import app


def test_app_starts() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code in {200, 404}
```

Run:

```powershell
python -m pytest
```

Stop: do not add real behavior until pytest passes.

## 5. First Real TDD Slice: Status Transition Policy

Write the test first.

`tests/domain/test_status_transition_policy.py`

```python
from app.domain.orders import OrderStatus
from app.domain.policies import StatusTransitionPolicy


def test_allows_out_for_delivery_to_delivered() -> None:
    policy = StatusTransitionPolicy()

    assert policy.can_transition(
        OrderStatus.OUT_FOR_DELIVERY,
        OrderStatus.DELIVERED,
    )


def test_rejects_delivered_to_out_for_delivery() -> None:
    policy = StatusTransitionPolicy()

    assert not policy.can_transition(
        OrderStatus.DELIVERED,
        OrderStatus.OUT_FOR_DELIVERY,
    )


def test_allows_confirmed_to_picked_up() -> None:
    policy = StatusTransitionPolicy()

    assert policy.can_transition(
        OrderStatus.CONFIRMED,
        OrderStatus.PICKED_UP,
    )


def test_rejects_delivery_attempted_to_out_for_delivery_in_slice1() -> None:
    policy = StatusTransitionPolicy()

    assert not policy.can_transition(
        OrderStatus.DELIVERY_ATTEMPTED,
        OrderStatus.OUT_FOR_DELIVERY,
    )
```

Add:

`app/domain/orders.py`

```python
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
```

`app/domain/policies.py`

```python
from app.domain.orders import OrderStatus


ALLOWED_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.CREATED: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
    OrderStatus.CONFIRMED: {OrderStatus.PICKED_UP, OrderStatus.CANCELLED},
    OrderStatus.PICKED_UP: {OrderStatus.IN_TRANSIT},
    OrderStatus.IN_TRANSIT: {OrderStatus.OUT_FOR_DELIVERY},
    OrderStatus.OUT_FOR_DELIVERY: {OrderStatus.DELIVERED},
}


class StatusTransitionPolicy:
    def can_transition(
        self,
        current: OrderStatus,
        next_status: OrderStatus,
    ) -> bool:
        return next_status in ALLOWED_TRANSITIONS.get(current, set())
```

Run:

```powershell
python -m pytest tests/domain/test_status_transition_policy.py
python -m pytest
```

## 6. Assignment Authorization Policy

Write the test first.

`tests/domain/test_assignment_authorization_policy.py`

```python
from app.domain.assignments import AssignmentStatus, DeliveryAssignment
from app.domain.policies import AssignmentAuthorizationPolicy


def test_allows_assigned_active_driver_for_order() -> None:
    assignment = DeliveryAssignment(
        assignment_id="ASN-3001",
        order_id="ORD-1001",
        driver_id="DRV-2001",
        status=AssignmentStatus.ASSIGNED,
    )

    policy = AssignmentAuthorizationPolicy()

    assert policy.can_driver_update_order("DRV-2001", "ORD-1001", assignment)


def test_rejects_different_driver() -> None:
    assignment = DeliveryAssignment(
        assignment_id="ASN-3001",
        order_id="ORD-1001",
        driver_id="DRV-2001",
        status=AssignmentStatus.ASSIGNED,
    )

    policy = AssignmentAuthorizationPolicy()

    assert not policy.can_driver_update_order("DRV-2002", "ORD-1001", assignment)


def test_rejects_completed_assignment() -> None:
    assignment = DeliveryAssignment(
        assignment_id="ASN-3001",
        order_id="ORD-1001",
        driver_id="DRV-2001",
        status=AssignmentStatus.COMPLETED,
    )

    policy = AssignmentAuthorizationPolicy()

    assert not policy.can_driver_update_order("DRV-2001", "ORD-1001", assignment)
```

Add:

`app/domain/assignments.py`

```python
from dataclasses import dataclass
from enum import Enum


class AssignmentStatus(str, Enum):
    ASSIGNED = "ASSIGNED"
    ACCEPTED = "ACCEPTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class DeliveryAssignment:
    assignment_id: str
    order_id: str
    driver_id: str
    status: AssignmentStatus
```

Append to `app/domain/policies.py`:

```python
from app.domain.assignments import AssignmentStatus, DeliveryAssignment


class AssignmentAuthorizationPolicy:
    def can_driver_update_order(
        self,
        driver_id: str,
        order_id: str,
        assignment: DeliveryAssignment | None,
    ) -> bool:
        return (
            assignment is not None
            and assignment.status == AssignmentStatus.ASSIGNED
            and assignment.driver_id == driver_id
            and assignment.order_id == order_id
        )
```

Run:

```powershell
python -m pytest tests/domain/test_assignment_authorization_policy.py
python -m pytest
```

## 7. Seed Store And Repositories

Domain records:

`app/domain/orders.py`

```python
from dataclasses import dataclass, replace
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


@dataclass(frozen=True)
class DeliveryOrder:
    order_id: str
    current_status: OrderStatus
    assigned_driver_id: str | None
    last_updated_at: datetime

    def with_status(
        self,
        next_status: OrderStatus,
        updated_at: datetime,
    ) -> "DeliveryOrder":
        return replace(self, current_status=next_status, last_updated_at=updated_at)
```

`app/domain/drivers.py`

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class DeliveryDriver:
    driver_id: str
    display_name: str
    availability_status: str
```

Seed store:

`app/seed/store.py`

```python
from datetime import datetime

from app.domain.assignments import AssignmentStatus, DeliveryAssignment
from app.domain.drivers import DeliveryDriver
from app.domain.orders import DeliveryOrder, OrderStatus


class SeedDataStore:
    def orders_by_id(self) -> dict[str, DeliveryOrder]:
        return {
            "ORD-1001": DeliveryOrder(
                order_id="ORD-1001",
                current_status=OrderStatus.OUT_FOR_DELIVERY,
                assigned_driver_id="DRV-2001",
                last_updated_at=datetime.fromisoformat("2026-07-01T09:00:00+08:00"),
            )
        }

    def drivers_by_id(self) -> dict[str, DeliveryDriver]:
        return {
            "DRV-2001": DeliveryDriver("DRV-2001", "Aisha Tan", "AVAILABLE"),
            "DRV-2003": DeliveryDriver("DRV-2003", "Ravi Kumar", "AVAILABLE"),
        }

    def assignments_by_id(self) -> dict[str, DeliveryAssignment]:
        return {
            "ASN-3001": DeliveryAssignment(
                assignment_id="ASN-3001",
                order_id="ORD-1001",
                driver_id="DRV-2001",
                status=AssignmentStatus.ASSIGNED,
            )
        }
```

Repository pattern:

`app/repositories/orders.py`

```python
from app.domain.orders import DeliveryOrder
from app.seed.store import SeedDataStore


class OrderRepository:
    def __init__(self, seed_data_store: SeedDataStore) -> None:
        self._orders = dict(seed_data_store.orders_by_id())

    def find_by_id(self, order_id: str) -> DeliveryOrder | None:
        return self._orders.get(order_id)

    def save(self, order: DeliveryOrder) -> None:
        self._orders[order.order_id] = order
```

Add driver and assignment repositories using the same pattern.

## 8. Health Endpoint

Test first:

`tests/api/test_health_api.py`

```python
from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_up() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "UP"
    assert response.json()["service"] == "partner-source"
```

Router:

`app/api/health.py`

```python
from fastapi import APIRouter

router = APIRouter(tags=["Operations"])


@router.get("/health")
def get_health() -> dict[str, str]:
    return {"status": "UP", "service": "partner-source"}
```

Update `app/main.py`:

```python
from fastapi import FastAPI

from app.api import health


def create_app() -> FastAPI:
    app = FastAPI(title="Waypoint Partner Source API", version="1.0.0")
    app.include_router(health.router)
    return app


app = create_app()
```

## 9. Readiness Endpoint

Add to `app/api/health.py`:

```python
from app.seed.store import SeedDataStore


@router.get("/ready")
def get_readiness() -> dict[str, object]:
    seed_data_store = SeedDataStore()
    ready = bool(seed_data_store.orders_by_id()) and bool(seed_data_store.drivers_by_id())
    return {
        "status": "READY" if ready else "NOT_READY",
        "service": "partner-source",
        "checks": {
            "persistence": "UP",
            "seedData": "UP" if ready else "DOWN",
        },
    }
```

Add a test before implementing if you are following strict TDD:

```python
def test_ready_returns_ready_when_seed_data_loaded() -> None:
    client = TestClient(app)

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "READY"
    assert response.json()["service"] == "partner-source"
    assert response.json()["checks"]["persistence"] == "UP"
    assert response.json()["checks"]["seedData"] == "UP"
```

## 10. Shared Error Envelope

`app/errors/exceptions.py`

```python
class PartnerSourceError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        error_code: str,
        title: str,
        detail: str,
        problem_type: str,
    ) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.error_code = error_code
        self.title = title
        self.detail = detail
        self.problem_type = problem_type

    @classmethod
    def order_not_found(cls, order_id: str) -> "PartnerSourceError":
        return cls(
            status_code=404,
            error_code="ORDER_NOT_FOUND",
            title="Order not found",
            detail=f"No order exists for orderId {order_id}.",
            problem_type="https://waypoint.local/problems/order-not-found",
        )
```

`app/errors/handlers.py`

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors.exceptions import PartnerSourceError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(PartnerSourceError)
    async def partner_source_error_handler(
        request: Request,
        exc: PartnerSourceError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            media_type="application/problem+json",
            content={
                "type": exc.problem_type,
                "title": exc.title,
                "status": exc.status_code,
                "detail": exc.detail,
                "instance": request.url.path,
                "errorCode": exc.error_code,
                "correlationId": request.headers.get("X-Correlation-Id", "req-local"),
            },
        )
```

Update `app/main.py`:

```python
from fastapi import FastAPI

from app.api import health
from app.errors.handlers import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(title="Waypoint Partner Source API", version="1.0.0")
    app.include_router(health.router)
    register_exception_handlers(app)
    return app


app = create_app()
```

## 11. First Contract Endpoint: Order Status Lookup

Schema:

`app/schemas/orders.py`

```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.orders import OrderStatus


class OrderStatusResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    orderId: str = Field(pattern=r"^ORD-[0-9]{4}$")
    currentStatus: OrderStatus
    statusLabel: str
    currentLocation: dict | None = None
    estimatedDeliveryAt: datetime | None
    deliveryWindow: dict
    assignedDriver: dict | None = None
    lastUpdatedAt: datetime
```

Service:

`app/services/order_status.py`

```python
from app.errors.exceptions import PartnerSourceError
from app.repositories.orders import OrderRepository
from app.schemas.orders import OrderStatusResponse


class OrderStatusService:
    def __init__(self, order_repository: OrderRepository) -> None:
        self.order_repository = order_repository

    def get_status(self, order_id: str) -> OrderStatusResponse:
        order = self.order_repository.find_by_id(order_id)
        if order is None:
            raise PartnerSourceError.order_not_found(order_id)

        return OrderStatusResponse(
            orderId=order.order_id,
            currentStatus=order.current_status,
            statusLabel=order.current_status.value.replace("_", " "),
            currentLocation=None,
            estimatedDeliveryAt=None,
            deliveryWindow={
                "start": "2026-06-30T14:00:00+08:00",
                "end": "2026-06-30T18:00:00+08:00",
            },
            assignedDriver={
                "driverId": order.assigned_driver_id,
                "displayName": "A. Kumar",
            },
            lastUpdatedAt=order.last_updated_at,
        )
```

Route:

`app/api/orders.py`

```python
from typing import Annotated

from fastapi import APIRouter, Path

from app.repositories.orders import OrderRepository
from app.schemas.orders import OrderStatusResponse
from app.seed.store import SeedDataStore
from app.services.order_status import OrderStatusService

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.get("/{order_id}/status", response_model=OrderStatusResponse)
def get_order_status(
    order_id: Annotated[str, Path(pattern=r"^ORD-[0-9]{4}$")],
) -> OrderStatusResponse:
    service = OrderStatusService(OrderRepository(SeedDataStore()))
    return service.get_status(order_id)
```

Update `app/main.py`:

```python
from fastapi import FastAPI

from app.api import health, orders
from app.errors.handlers import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(title="Waypoint Partner Source API", version="1.0.0")
    app.include_router(health.router)
    app.include_router(orders.router)
    register_exception_handlers(app)
    return app


app = create_app()
```

API test:

`tests/api/test_orders_api.py`

```python
from fastapi.testclient import TestClient

from app.main import app


def test_get_order_status_returns_seeded_status() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-1001/status")

    assert response.status_code == 200
    body = response.json()
    assert body["orderId"] == "ORD-1001"
    assert body["currentStatus"] == "OUT_FOR_DELIVERY"


def test_get_order_status_missing_order_returns_problem_detail() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-9999/status")

    assert response.status_code == 404
    body = response.json()
    assert body["errorCode"] == "ORDER_NOT_FOUND"
    assert body["correlationId"]
```

## 12. Remaining Endpoint Order

Build in this order:

1. `GET /api/v1/orders/{orderId}/timeline`
2. `GET /api/v1/drivers/{driverId}`
3. `GET /api/v1/drivers/{driverId}/assignments`
4. `POST /api/v1/orders/{orderId}/status-events`

For each endpoint:

```text
service pytest
-> TestClient success test
-> success implementation
-> error pytest
-> error implementation
-> full python -m pytest
```

## 13. CI Manual

Create this from repo root:

`C:\Users\prasa\Documents\Github\waypoint-pilot\.github\workflows\partner-source-fastapi-ci.yml`

Requirements-file version:

```yaml
name: Partner Source FastAPI CI

on:
  pull_request:
    paths:
      - "pilot_phase2_poc/partner-source/partner-source-fastapi/**"
      - ".github/workflows/partner-source-fastapi-ci.yml"
  push:
    branches: [main]
    paths:
      - "pilot_phase2_poc/partner-source/partner-source-fastapi/**"
      - ".github/workflows/partner-source-fastapi-ci.yml"

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: pilot_phase2_poc/partner-source/partner-source-fastapi
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: python -m pip install --upgrade pip
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: python -m pytest
```

## 14. Done Criteria

FastAPI is ready for parity checks when:

- [ ] scaffold pytest passes locally
- [ ] CI proves scaffold pytest
- [ ] status transition tests match Spring Boot
- [ ] assignment authorization tests match Spring Boot
- [ ] seed repositories pass
- [ ] `/health` passes
- [ ] `/ready` passes
- [ ] order status lookup success and not-found tests pass
- [ ] shared error envelope tests pass
