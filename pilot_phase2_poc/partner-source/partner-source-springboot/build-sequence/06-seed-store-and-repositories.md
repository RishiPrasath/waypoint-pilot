# 06 - Seed Store And Repositories

## Purpose

Create deterministic in-memory seed data and repository interfaces used by later services.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `7. Seed Data`
- `../../docs/active/data-and-seed-handoff.md`
- `../../docs/support/seed-data-detail.md`

## Tests To Write First

Create:

```text
src/test/java/com/waypoint/partnersource/order/repository/InMemoryOrderRepositoryTest.java
src/test/java/com/waypoint/partnersource/driver/repository/InMemoryDriverRepositoryTest.java
src/test/java/com/waypoint/partnersource/assignment/repository/InMemoryAssignmentRepositoryTest.java
src/test/java/com/waypoint/partnersource/order/repository/InMemoryStatusEventRepositoryTest.java
```

Test cases:

- `ORD-1001` exists and current status is `OUT_FOR_DELIVERY`.
- `ORD-9999` is missing.
- `DRV-2001` exists and is `AVAILABLE`.
- `DRV-9999` is missing.
- `DRV-2001` has active assignments `ASN-3001` and `ASN-3002`.
- `DRV-2003` has no active assignments.
- `ORD-1001` has events `EVT-4001` through `EVT-4005` in chronological order.

## Code To Implement

Domain:

```text
order/domain/DeliveryOrder.java
order/domain/OrderStatusEvent.java
order/domain/LocationSnapshot.java
order/domain/DeliveryWindow.java
order/domain/ActorType.java
driver/domain/DeliveryDriver.java
driver/domain/DriverAvailabilityStatus.java
```

Seed:

```text
shared/seed/SeedDataManifest.java
shared/seed/SeedDataStore.java
shared/seed/SeedDataLoader.java
```

Repositories:

```text
order/repository/OrderRepository.java
order/repository/InMemoryOrderRepository.java
order/repository/StatusEventRepository.java
order/repository/InMemoryStatusEventRepository.java
driver/repository/DriverRepository.java
driver/repository/InMemoryDriverRepository.java
assignment/repository/AssignmentRepository.java
assignment/repository/InMemoryAssignmentRepository.java
```

Keep repository APIs small: `findById`, `save` where mutation is needed, and query methods needed by endpoints.

## Commands To Run

```powershell
.\mvnw.cmd -Dtest=InMemoryOrderRepositoryTest,InMemoryDriverRepositoryTest,InMemoryAssignmentRepositoryTest,InMemoryStatusEventRepositoryTest test
.\mvnw.cmd test
```

## Done Criteria

- [ ] All agreed seed IDs exist or are deliberately absent.
- [ ] Repositories are in-memory only.
- [ ] No database dependencies were added.
- [ ] Timeline seed order is deterministic.

## Stop / Do Not Add

- Do not add JPA, H2, PostgreSQL, `@Entity`, or `JpaRepository`.
- Do not add HTTP controllers in this step.

