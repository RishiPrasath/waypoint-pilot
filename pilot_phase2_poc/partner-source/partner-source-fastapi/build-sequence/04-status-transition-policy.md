# 04 - Status Transition Policy

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Mirror the Spring Boot status transition policy in Python with pytest-first development.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `6. Status Transition Rules`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/04-status-transition-policy.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `tests/domain/test_status_transition_policy.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/domain/test_status_transition_policy.py
```

Use this exact test file before implementation:

**Test Block Explanation**

- What this block does: Shows the test code to write first for Use this exact test file before implementation.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from app.domain.orders import OrderStatus
from app.domain.policies import StatusTransitionPolicy


def test_out_for_delivery_can_transition_to_delivered() -> None:
    policy = StatusTransitionPolicy()

    assert policy.can_transition(
        OrderStatus.OUT_FOR_DELIVERY,
        OrderStatus.DELIVERED,
    ) is True


def test_delivered_cannot_transition_back_to_out_for_delivery() -> None:
    policy = StatusTransitionPolicy()

    assert policy.can_transition(
        OrderStatus.DELIVERED,
        OrderStatus.OUT_FOR_DELIVERY,
    ) is False


def test_confirmed_can_transition_to_picked_up() -> None:
    policy = StatusTransitionPolicy()

    assert policy.can_transition(
        OrderStatus.CONFIRMED,
        OrderStatus.PICKED_UP,
    ) is True


def test_delivery_attempted_cannot_transition_to_out_for_delivery() -> None:
    policy = StatusTransitionPolicy()

    assert policy.can_transition(
        OrderStatus.DELIVERY_ATTEMPTED,
        OrderStatus.OUT_FOR_DELIVERY,
    ) is False


def test_terminal_statuses_have_no_outgoing_transitions() -> None:
    policy = StatusTransitionPolicy()

    assert policy.can_transition(OrderStatus.DELIVERED, OrderStatus.CANCELLED) is False
    assert policy.can_transition(OrderStatus.CANCELLED, OrderStatus.CREATED) is False


def test_created_cannot_transition_directly_to_delivered() -> None:
    policy = StatusTransitionPolicy()

    assert policy.can_transition(OrderStatus.CREATED, OrderStatus.DELIVERED) is False

```

Expected first result before implementation:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `ModuleNotFoundError or ImportError for app.domain.orders/app.domain.policies`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
ModuleNotFoundError or ImportError for app.domain.orders/app.domain.policies

```
## File Map

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/domain/orders.py`, `app/domain/policies.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/domain/orders.py
app/domain/policies.py
```

`OrderStatus` enum values must match OpenAPI exactly.

Expected policy shape:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `class StatusTransitionPolicy:`, `def can_transition(self, current: OrderStatus, next_status: OrderStatus) -> bool:`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
class StatusTransitionPolicy:
    def can_transition(self, current: OrderStatus, next_status: OrderStatus) -> bool:
        ...
```

## Exact Code

Create `app/domain/orders.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/domain/orders.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

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

Create `app/domain/policies.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/domain/policies.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.domain.orders import OrderStatus


class StatusTransitionPolicy:
    _ALLOWED_TRANSITIONS = {
        OrderStatus.CREATED: {
            OrderStatus.CONFIRMED,
            OrderStatus.CANCELLED,
        },
        OrderStatus.CONFIRMED: {
            OrderStatus.PICKED_UP,
            OrderStatus.CANCELLED,
        },
        OrderStatus.PICKED_UP: {
            OrderStatus.IN_TRANSIT,
        },
        OrderStatus.IN_TRANSIT: {
            OrderStatus.OUT_FOR_DELIVERY,
        },
        OrderStatus.OUT_FOR_DELIVERY: {
            OrderStatus.DELIVERED,
        },
        OrderStatus.DELIVERY_ATTEMPTED: set(),
        OrderStatus.DELIVERED: set(),
        OrderStatus.CANCELLED: set(),
    }

    def can_transition(
        self,
        current_status: OrderStatus,
        next_status: OrderStatus,
    ) -> bool:
        return next_status in self._ALLOWED_TRANSITIONS.get(current_status, set())

```

Do not add delivery-attempt behavior. `DELIVERY_ATTEMPTED` exists as an enum value only and has no outgoing transitions in Slice 1.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/domain/test_status_transition_policy.py
python -m pytest
```

## Done Criteria

- [x] Tests match Spring Boot cases.
- [x] Policy uses no FastAPI app/router code.
- [x] `DELIVERY_ATTEMPTED` remains non-expanding Slice 1 enum behavior.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add routers or services.
- Do not add status-event mutation.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
