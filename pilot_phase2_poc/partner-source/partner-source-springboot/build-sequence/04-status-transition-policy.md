# 04 - Status Transition Policy

## Purpose

Build the first real domain rule with TDD: which order status moves are allowed in Slice 1.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `6. Status Transition Rules`
- `../../docs/active/contract-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Tests To Write First

Create:

```text
src/test/java/com/waypoint/partnersource/order/domain/StatusTransitionPolicyTest.java
```

Test cases:

- `OUT_FOR_DELIVERY -> DELIVERED` is allowed.
- `DELIVERED -> OUT_FOR_DELIVERY` is rejected.
- `CONFIRMED -> PICKED_UP` is allowed.
- `DELIVERY_ATTEMPTED -> OUT_FOR_DELIVERY` is rejected in Slice 1.
- Unknown terminal paths from `DELIVERED` and `CANCELLED` are rejected.

Run and confirm the test fails because `OrderStatus` or `StatusTransitionPolicy` does not exist yet.

## Code To Implement

Create:

```text
src/main/java/com/waypoint/partnersource/order/domain/OrderStatus.java
src/main/java/com/waypoint/partnersource/order/domain/StatusTransitionPolicy.java
```

`OrderStatus` enum values must match OpenAPI:

```text
CREATED
CONFIRMED
PICKED_UP
IN_TRANSIT
OUT_FOR_DELIVERY
DELIVERY_ATTEMPTED
DELIVERED
CANCELLED
```

`StatusTransitionPolicy` should expose:

```java
public boolean canTransition(OrderStatus current, OrderStatus next)
```

Use the agreed transition table only.

## Commands To Run

Focused:

```powershell
.\mvnw.cmd -Dtest=StatusTransitionPolicyTest test
```

Full:

```powershell
.\mvnw.cmd test
```

## Expected Output

- First run fails because the policy does not exist.
- Final focused and full test runs pass.

## Done Criteria

- [ ] Tests prove allowed and rejected transitions.
- [ ] Policy has no Spring annotations.
- [ ] `DELIVERY_ATTEMPTED` is not expanded into Slice 1 behavior.

## Stop / Do Not Add

- Do not add controllers or services.
- Do not add status-event mutation yet.

