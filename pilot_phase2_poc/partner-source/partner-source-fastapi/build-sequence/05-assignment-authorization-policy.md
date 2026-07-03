# 05 - Assignment Authorization Policy

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Build the domain rule that decides whether a driver is allowed to create a status event for an order.

This task exists because the later `POST /api/v1/orders/{orderId}/status-events` endpoint must reject status updates from drivers who are not assigned to that order. The rule stays in the domain layer so the HTTP layer can call one clear policy instead of duplicating assignment checks.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `7. Seed Data` and `10. Acceptance Scenarios`
- `../../docs/active/data-and-seed-handoff.md`
- `../../partner-source-springboot/build-sequence/05-assignment-authorization-policy.md`

## Prereqs

- Task `04 - Status Transition Policy` is complete.
- `app/domain/__init__.py` exists.
- `tests/domain/` exists.
- Read the source docs above before writing code.
- Keep this as domain-only code. Do not add routers or repositories in this task.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `tests/domain/test_assignment_authorization_policy.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/domain/test_assignment_authorization_policy.py
```

Write these tests before implementation:

**Test Block Explanation**

- What this block does: Shows the test code to write first for Write these tests before implementation.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from app.domain.assignments import DeliveryAssignment, DeliveryAssignmentStatus
from app.domain.policies import AssignmentAuthorizationPolicy


def test_driver_can_update_order_through_assigned_assignment() -> None:
    policy = AssignmentAuthorizationPolicy()
    assignments = [
        DeliveryAssignment(
            driver_id="DRV-2001",
            order_id="ORD-1001",
            status=DeliveryAssignmentStatus.ASSIGNED,
        )
    ]

    assert policy.can_driver_update_order(
        "DRV-2001",
        "ORD-1001",
        assignments,
    )


def test_unassigned_driver_cannot_update_order() -> None:
    policy = AssignmentAuthorizationPolicy()
    assignments = [
        DeliveryAssignment(
            driver_id="DRV-2001",
            order_id="ORD-1001",
            status=DeliveryAssignmentStatus.ASSIGNED,
        )
    ]

    assert not policy.can_driver_update_order(
        "DRV-2002",
        "ORD-1001",
        assignments,
    )


def test_completed_assignment_keeps_authorized_for_delivered_order_invalid_transition_path() -> None:
    policy = AssignmentAuthorizationPolicy()
    assignments = [
        DeliveryAssignment(
            driver_id="DRV-2001",
            order_id="ORD-1003",
            status=DeliveryAssignmentStatus.COMPLETED,
        )
    ]

    assert policy.can_driver_update_order(
        "DRV-2001",
        "ORD-1003",
        assignments,
    )


def test_cancelled_assignment_does_not_authorize_driver() -> None:
    policy = AssignmentAuthorizationPolicy()
    assignments = [
        DeliveryAssignment(
            driver_id="DRV-2001",
            order_id="ORD-1001",
            status=DeliveryAssignmentStatus.CANCELLED,
        )
    ]

    assert not policy.can_driver_update_order(
        "DRV-2001",
        "ORD-1001",
        assignments,
    )

```

Expected first result before implementation:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `ModuleNotFoundError or ImportError for app.domain.assignments`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
ModuleNotFoundError or ImportError for app.domain.assignments

```

## File Map

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/domain/assignments.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/domain/assignments.py
```

Update:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/domain/policies.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/domain/policies.py
```

Expected method:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `class AssignmentAuthorizationPolicy:`, `def can_driver_update_order(`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
class AssignmentAuthorizationPolicy:
    def can_driver_update_order(
        self,
        driver_id: str,
        order_id: str,
        assignments: Iterable[DeliveryAssignment],
    ) -> bool:
        ...

```

## Exact Code

Create `app/domain/assignments.py`:

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

```

Add these imports near the top of `app/domain/policies.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/domain/policies.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from collections.abc import Iterable

from app.domain.assignments import DeliveryAssignment, DeliveryAssignmentStatus

```

Keep the existing `StatusTransitionPolicy` from task 04. Add this class below it:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `StatusTransitionPolicy`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
class AssignmentAuthorizationPolicy:
    def can_driver_update_order(
        self,
        driver_id: str,
        order_id: str,
        assignments: Iterable[DeliveryAssignment],
    ) -> bool:
        return any(
            assignment.driver_id == driver_id
            and assignment.order_id == order_id
            and assignment.status
            in {
                DeliveryAssignmentStatus.ASSIGNED,
                DeliveryAssignmentStatus.ACCEPTED,
                DeliveryAssignmentStatus.COMPLETED,
            }
            for assignment in assignments
        )

```

Why `COMPLETED` is included:

`ORD-1003` is already `DELIVERED`, and its seed assignment `ASN-3003` is `COMPLETED`. The agreed spec says that this case must reach the invalid-transition rule and return `409 INVALID_STATUS_TRANSITION` later, not get blocked early as `403 ORDER_NOT_ASSIGNED_TO_DRIVER`.

Why `CANCELLED` is excluded:

A cancelled assignment is not valid proof that the driver may update the order.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/domain/test_assignment_authorization_policy.py
python -m pytest
```

## Done Criteria

- [x] FastAPI tests mirror Spring Boot behavior.
- [x] `ORD-1003` completed-assignment edge case is named in a test.
- [x] No HTTP code is required.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Forgetting the `ACCEPTED` enum value from the agreed spec.
- Treating `COMPLETED` as unauthorized and accidentally breaking the `ORD-1003` invalid-transition acceptance scenario.
- Treating `CANCELLED` as authorized.
- Replacing task 04 status transition code while editing `app/domain/policies.py`.
- Adding endpoints, seed repositories, dependencies, or auth code in this domain-only task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add authentication packages.
- Do not create status-event endpoint yet.
- Do not create seed repositories yet.
- Do not add FastAPI routers.
- Do not add database models.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Replaced placeholder `Exact Code` content with exact FastAPI test and domain code.
