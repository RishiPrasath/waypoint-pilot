# 04 - Status Transition Policy

## Purpose

Mirror the Spring Boot status transition policy in Python with pytest-first development.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `6. Status Transition Rules`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/04-status-transition-policy.md`

## Tests To Write First

Create:

```text
tests/domain/test_status_transition_policy.py
```

Test cases:

- `OUT_FOR_DELIVERY -> DELIVERED` is allowed.
- `DELIVERED -> OUT_FOR_DELIVERY` is rejected.
- `CONFIRMED -> PICKED_UP` is allowed.
- `DELIVERY_ATTEMPTED -> OUT_FOR_DELIVERY` is rejected in Slice 1.
- Terminal statuses have no outgoing transitions.

Run and confirm the test fails because the enum or policy does not exist.

## Code To Implement

Create:

```text
app/domain/orders.py
app/domain/policies.py
```

`OrderStatus` enum values must match OpenAPI exactly.

Expected policy shape:

```python
class StatusTransitionPolicy:
    def can_transition(self, current: OrderStatus, next_status: OrderStatus) -> bool:
        ...
```

## Commands To Run

```powershell
python -m pytest tests/domain/test_status_transition_policy.py
python -m pytest
```

## Done Criteria

- [ ] Tests match Spring Boot cases.
- [ ] Policy uses no FastAPI app/router code.
- [ ] `DELIVERY_ATTEMPTED` remains non-expanding Slice 1 enum behavior.

## Stop / Do Not Add

- Do not add routers or services.
- Do not add status-event mutation.

