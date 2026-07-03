# 11 - Order Timeline

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `GET /api/v1/orders/{orderId}/timeline`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `8. Response Shapes` and `10. Acceptance Scenarios`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/11-order-timeline.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `tests/services/test_order_timeline_service.py`, `tests/api/test_order_timeline_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/services/test_order_timeline_service.py
tests/api/test_order_timeline_endpoint.py
```

`tests/services/test_order_timeline_service.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/services/test_order_timeline_service.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from app.repositories.orders import InMemoryOrderRepository
from app.repositories.status_events import InMemoryStatusEventRepository
from app.seed.loader import load_seed_data
from app.services.order_timeline import OrderTimelineService


def test_get_order_timeline_returns_chronological_events() -> None:
    store = load_seed_data()
    service = OrderTimelineService(
        InMemoryOrderRepository(store),
        InMemoryStatusEventRepository(store),
    )

    response = service.get_timeline("ORD-1001", page=1, page_size=20)

    assert response is not None
    assert response.orderId == "ORD-1001"
    assert [item.eventId for item in response.items] == [
        "EVT-4001",
        "EVT-4002",
        "EVT-4003",
        "EVT-4004",
        "EVT-4005",
    ]
    assert response.totalItems == 5

```

`tests/api/test_order_timeline_endpoint.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/api/test_order_timeline_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from fastapi.testclient import TestClient

from app.main import app


def test_get_order_timeline_returns_contract_shape() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20")

    assert response.status_code == 200
    body = response.json()
    assert body["orderId"] == "ORD-1001"
    assert body["page"] == 1
    assert body["pageSize"] == 20
    assert body["totalItems"] == 5
    assert [item["eventId"] for item in body["items"]] == [
        "EVT-4001",
        "EVT-4002",
        "EVT-4003",
        "EVT-4004",
        "EVT-4005",
    ]

```
## File Map

Extend:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for Extend.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/schemas/orders.py
app/services/order_timeline.py
app/api/orders.py
```

Use existing repository and error handling.

## Exact Code

Extend `app/schemas/orders.py` with timeline response shapes:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/schemas/orders.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.domain.orders import ActorType


class TimelineEventResponse(BaseModel):
    eventId: str
    status: OrderStatus
    statusLabel: str
    occurredAt: datetime
    actorType: ActorType
    actorId: str


class OrderTimelineResponse(BaseModel):
    orderId: str
    items: list[TimelineEventResponse]
    page: int
    pageSize: int
    totalItems: int

```

Create `app/services/order_timeline.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/services/order_timeline.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.repositories.orders import InMemoryOrderRepository
from app.repositories.status_events import InMemoryStatusEventRepository
from app.schemas.orders import OrderTimelineResponse, TimelineEventResponse


class OrderTimelineService:
    def __init__(
        self,
        order_repository: InMemoryOrderRepository,
        status_event_repository: InMemoryStatusEventRepository,
    ) -> None:
        self._order_repository = order_repository
        self._status_event_repository = status_event_repository

    def get_timeline(
        self,
        order_id: str,
        page: int,
        page_size: int,
    ) -> OrderTimelineResponse | None:
        order = self._order_repository.find_by_id(order_id)
        if order is None:
            return None

        events = self._status_event_repository.find_by_order_id(order_id)
        start = (page - 1) * page_size
        end = start + page_size
        page_items = events[start:end]

        return OrderTimelineResponse(
            orderId=order_id,
            items=[
                TimelineEventResponse(
                    eventId=event.event_id,
                    status=event.new_status,
                    statusLabel=event.status_label,
                    occurredAt=event.occurred_at,
                    actorType=event.actor_type,
                    actorId=event.actor_id,
                )
                for event in page_items
            ],
            page=page,
            pageSize=page_size,
            totalItems=len(events),
        )

```

Extend `app/api/orders.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/api/orders.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.errors.exceptions import OrderNotFoundError
from app.repositories.status_events import InMemoryStatusEventRepository
from app.schemas.orders import OrderTimelineResponse
from app.services.order_timeline import OrderTimelineService


@router.get("/{order_id}/timeline", response_model=OrderTimelineResponse)
def get_order_timeline(
    order_id: str,
    page: int = 1,
    pageSize: int = 20,
) -> OrderTimelineResponse:
    service = OrderTimelineService(
        InMemoryOrderRepository(_STORE),
        InMemoryStatusEventRepository(_STORE),
    )
    response = service.get_timeline(order_id, page, pageSize)

    if response is None:
        raise OrderNotFoundError(order_id)

    return response

```

FastAPI query parameter note:

Use `pageSize`, not `page_size`, because the shared OpenAPI contract exposes `pageSize`.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/services/test_order_timeline_service.py tests/api/test_order_timeline_endpoint.py
python -m pytest
```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `Invoke-RestMethod "http://localhost:8000/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod "http://localhost:8000/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"
```

## Done Criteria

- [x] Timeline is chronological.
- [x] Pagination fields match OpenAPI.
- [x] Error envelope is reused.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add uncontracted sorting filters.
- Do not add delivery-attempt behavior.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Implemented with contract-correct `pageSize` and marked done after focused tests and the full pytest suite passed.
