# 14 - Create Status Event

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `POST /api/v1/orders/{orderId}/status-events`, the final Slice 1 write endpoint.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `6`, `7`, `8`, `9`, and `10`
- `../../docs/active/contract-handoff.md`
- `../../docs/active/data-and-seed-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../docs/contracts/shared-error-contract.md`

## Prereqs

- Tasks 04, 05, 06, and 10 are complete.
- Status lookup and timeline work before mutation is added.
- In-memory store preserves changes during a running app/test context.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `src/test/java/com/waypoint/partnersource/order/service/StatusEventServiceTest.java`, `src/test/java/com/waypoint/partnersource/order/api/StatusEventControllerTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/order/service/StatusEventServiceTest.java
src/test/java/com/waypoint/partnersource/order/api/StatusEventControllerTest.java
```

`StatusEventServiceTest.java` core success test:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `StatusEventServiceTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
@Test
void assignedDriverCanCreateDeliveredStatusEvent() {
    var store = SeedDataLoader.load();
    var service = new StatusEventService(
            new InMemoryOrderRepository(store),
            new InMemoryDriverRepository(store),
            new InMemoryAssignmentRepository(store),
            new InMemoryStatusEventRepository(store),
            new AssignmentAuthorizationPolicy(),
            new StatusTransitionPolicy()
    );

    var response = service.createStatusEvent(
            "ORD-1001",
            new CreateStatusEventRequest("DRV-2001", OrderStatus.DELIVERED, OffsetDateTime.now(), null, null, null)
    );

    assertEquals(OrderStatus.OUT_FOR_DELIVERY, response.previousStatus());
    assertEquals(OrderStatus.DELIVERED, response.newStatus());
    assertEquals(OrderStatus.DELIVERED, response.orderCurrentStatus());
}

```

Add service negative tests for:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for Add service negative tests for.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
DRV-2002 on ORD-1001 -> ORDER_NOT_ASSIGNED_TO_DRIVER
DRV-9999 on ORD-1001 -> DRIVER_NOT_FOUND
ORD-9999 -> ORDER_NOT_FOUND
DRV-2001 on ORD-1003 to OUT_FOR_DELIVERY -> INVALID_STATUS_TRANSITION
far-future occurredAt -> INVALID_STATUS_EVENT

```

`StatusEventControllerTest.java` should assert success returns `201` and unassigned driver returns `403 ORDER_NOT_ASSIGNED_TO_DRIVER`.
## File Map

DTOs:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `order/api/dto/CreateStatusEventRequest.java`, `order/api/dto/StatusEventResponse.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
order/api/dto/CreateStatusEventRequest.java
order/api/dto/StatusEventResponse.java
```

Service/controller:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `order/service/StatusEventService.java`, `order/api/StatusEventController.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
order/service/StatusEventService.java
order/api/StatusEventController.java
```

## Exact Code

Create `CreateStatusEventRequest.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `CreateStatusEventRequest.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.api.dto;

import com.waypoint.partnersource.order.domain.OrderStatus;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import java.time.OffsetDateTime;

public record CreateStatusEventRequest(
        @NotBlank @Pattern(regexp = "^DRV-[0-9]{4}$") String driverId,
        @NotNull OrderStatus status,
        OffsetDateTime occurredAt,
        LocationSnapshotResponse location,
        String note,
        Boolean proofOfDeliveryAvailable
) {
}

```

Create `StatusEventResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `StatusEventResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.api.dto;

import com.waypoint.partnersource.order.domain.ActorType;
import com.waypoint.partnersource.order.domain.OrderStatus;
import java.time.OffsetDateTime;

public record StatusEventResponse(
        String eventId,
        String orderId,
        OrderStatus previousStatus,
        OrderStatus newStatus,
        String statusLabel,
        OffsetDateTime occurredAt,
        ActorType actorType,
        String actorId,
        LocationSnapshotResponse location,
        String note,
        Boolean proofOfDeliveryAvailable,
        OrderStatus orderCurrentStatus
) {
}

```

Service validation order:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for Service validation order.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
1. Validate order exists -> ORDER_NOT_FOUND
2. Validate driver exists -> DRIVER_NOT_FOUND
3. Validate assignment authorization -> ORDER_NOT_ASSIGNED_TO_DRIVER
4. Validate status transition -> INVALID_STATUS_TRANSITION
5. Validate event semantics -> INVALID_STATUS_EVENT
6. Append event
7. Update order current status
8. Return StatusEventResponse

```

Use `AssignmentAuthorizationPolicy` and `StatusTransitionPolicy`; do not duplicate their logic in the service.

Controller path:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for Controller path.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
POST /api/v1/orders/{orderId}/status-events
```

Return HTTP `201 CREATED` for success.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd "-Dtest=StatusEventServiceTest,StatusEventControllerTest" test
.\mvnw.cmd test
```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `$body = @{`, `driverId = "DRV-2001"`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
$body = @{
  driverId = "DRV-2001"
  status = "DELIVERED"
  occurredAt = "2026-07-02T10:30:00+08:00"
  note = "Left with reception"
  proofOfDeliveryAvailable = $true
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/v1/orders/ORD-1001/status-events -ContentType "application/json" -Body $body

```

## Done Criteria

- [x] All success and negative tests pass.
- [x] Mutation is visible through status lookup and timeline.
- [x] Error status and `errorCode` match the shared contract.
- [x] No extra status-event fields are invented.

## Common Mistakes

- Checking status transition before assignment authorization.
- Returning `403` for `ORD-1003` instead of `409 INVALID_STATUS_TRANSITION`.
- Reinitializing seed data per request and losing mutation.

## Stop / Do Not Add

- Do not add proof upload, signatures, photos, delivery-attempt flows, or external integrations.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized and exact status-event DTO/service/controller behavior added.
- Implemented and marked done after focused tests and the full Maven suite passed.
