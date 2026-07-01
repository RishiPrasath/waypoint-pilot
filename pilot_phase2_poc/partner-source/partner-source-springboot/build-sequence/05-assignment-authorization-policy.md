# 05 - Assignment Authorization Policy

## Purpose

Build the domain rule that decides whether a driver may create a status event for an order.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `7. Seed Data` and `10. Acceptance Scenarios`
- `../../docs/active/data-and-seed-handoff.md`
- `../../docs/active/test-and-acceptance-handoff.md`

## Tests To Write First

Create:

```text
src/test/java/com/waypoint/partnersource/assignment/domain/AssignmentAuthorizationPolicyTest.java
```

Test cases:

- `DRV-2001` can update `ORD-1001` through `ASN-3001`.
- `DRV-2002` cannot update `ORD-1001`.
- `DRV-2001` can reach the delivered-order invalid-transition path for `ORD-1003` through the agreed completed-assignment edge case.
- A cancelled assignment does not authorize a driver.

## Code To Implement

Create:

```text
src/main/java/com/waypoint/partnersource/assignment/domain/AssignmentStatus.java
src/main/java/com/waypoint/partnersource/assignment/domain/DeliveryAssignment.java
src/main/java/com/waypoint/partnersource/assignment/domain/AssignmentAuthorizationPolicy.java
```

Expected policy method:

```java
public boolean canDriverUpdateOrder(
    String driverId,
    String orderId,
    Collection<DeliveryAssignment> assignments
)
```

The policy must allow the agreed `ORD-1003` invalid-transition fixture to reach the transition rule, even though `ASN-3003` is completed.

## Commands To Run

```powershell
.\mvnw.cmd -Dtest=AssignmentAuthorizationPolicyTest test
.\mvnw.cmd test
```

## Done Criteria

- [ ] Authorization tests pass.
- [ ] No HTTP or repository code is required.
- [ ] The `ORD-1003` edge case is documented in the test name.

## Stop / Do Not Add

- Do not create status events yet.
- Do not add security/authentication.

