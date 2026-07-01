# 05 - Assignment Authorization Policy

## Purpose

Mirror the Spring Boot assignment authorization policy in Python.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `7. Seed Data` and `10. Acceptance Scenarios`
- `../../docs/active/data-and-seed-handoff.md`
- `../../partner-source-springboot/build-sequence/05-assignment-authorization-policy.md`

## Tests To Write First

Create:

```text
tests/domain/test_assignment_authorization_policy.py
```

Test cases:

- `DRV-2001` can update `ORD-1001`.
- `DRV-2002` cannot update `ORD-1001`.
- `DRV-2001` can reach the delivered-order invalid-transition path for `ORD-1003`.
- Cancelled assignment does not authorize a driver.

## Code To Implement

Create or extend:

```text
app/domain/assignments.py
app/domain/policies.py
```

Expected method:

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

## Commands To Run

```powershell
python -m pytest tests/domain/test_assignment_authorization_policy.py
python -m pytest
```

## Done Criteria

- [ ] FastAPI tests mirror Spring Boot behavior.
- [ ] `ORD-1003` completed-assignment edge case is named in a test.
- [ ] No HTTP code is required.

## Stop / Do Not Add

- Do not add authentication packages.
- Do not create status-event endpoint yet.

