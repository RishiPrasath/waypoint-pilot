# 13 - Driver Assignments

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `GET /api/v1/drivers/{driverId}/assignments`.

This lists active order work for a seeded driver.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `7. Seed Data`, `8. Response Shapes`, and `10. Acceptance Scenarios`
- `../../docs/active/data-and-seed-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Prereqs

- Task 12 driver profile works.
- Order and assignment repositories exist.
- Error envelope is centralized.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `src/test/java/com/waypoint/partnersource/driver/service/DriverAssignmentServiceTest.java`, `src/test/java/com/waypoint/partnersource/driver/api/DriverAssignmentControllerTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/driver/service/DriverAssignmentServiceTest.java
src/test/java/com/waypoint/partnersource/driver/api/DriverAssignmentControllerTest.java
```

`DriverAssignmentServiceTest.java` core tests:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `DriverAssignmentServiceTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
@Test
void returnsTwoActiveAssignmentsForDrv2001() {
    var store = SeedDataLoader.load();
    var service = new DriverAssignmentService(
            new InMemoryDriverRepository(store),
            new InMemoryAssignmentRepository(store),
            new InMemoryOrderRepository(store)
    );

    var response = service.listAssignments("DRV-2001", null, 1, 20);

    assertEquals(2, response.totalItems());
    assertEquals("ORD-1001", response.items().get(0).orderId());
    assertEquals("ORD-1002", response.items().get(1).orderId());
}

@Test
void availableDriverWithNoAssignmentsReturnsEmptyItems() {
    var store = SeedDataLoader.load();
    var service = new DriverAssignmentService(
            new InMemoryDriverRepository(store),
            new InMemoryAssignmentRepository(store),
            new InMemoryOrderRepository(store)
    );

    var response = service.listAssignments("DRV-2003", null, 1, 20);

    assertTrue(response.items().isEmpty());
    assertEquals(0, response.totalItems());
}

```

`DriverAssignmentControllerTest.java` should assert `/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20` returns `totalItems = 2` and item order IDs `ORD-1001`, `ORD-1002`.
## File Map

DTOs:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `driver/api/dto/DriverAssignmentItemResponse.java`, `driver/api/dto/DriverAssignmentsResponse.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
driver/api/dto/DriverAssignmentItemResponse.java
driver/api/dto/DriverAssignmentsResponse.java
```

Service/controller:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `driver/service/DriverAssignmentService.java`, `driver/api/DriverAssignmentController.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
driver/service/DriverAssignmentService.java
driver/api/DriverAssignmentController.java
```

## Exact Code

Create `DriverAssignmentItemResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `DriverAssignmentItemResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.driver.api.dto;

import com.waypoint.partnersource.assignment.domain.AssignmentStatus;
import com.waypoint.partnersource.order.api.dto.DeliveryWindowResponse;
import com.waypoint.partnersource.order.domain.OrderStatus;
import java.time.OffsetDateTime;

public record DriverAssignmentItemResponse(
        String assignmentId,
        String orderId,
        AssignmentStatus assignmentStatus,
        OrderStatus currentStatus,
        String recipientName,
        String deliveryAddressSummary,
        DeliveryWindowResponse deliveryWindow,
        OffsetDateTime lastUpdatedAt
) {
}

```

Create `DriverAssignmentsResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `DriverAssignmentsResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.driver.api.dto;

import java.util.List;

public record DriverAssignmentsResponse(
        String driverId,
        List<DriverAssignmentItemResponse> items,
        int page,
        int pageSize,
        int totalItems
) {
}

```

Service behavior:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for Service behavior.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
validate driver exists
load active assignments for driver
optionally filter by order current status
join each assignment to its order
return paged DriverAssignmentsResponse

```

Expected seed behavior:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for `DRV-2001 -> totalItems 2, ORD-1001 and ORD-1002`, `DRV-2003 -> totalItems 0, items []`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
DRV-2001 -> totalItems 2, ORD-1001 and ORD-1002
DRV-2003 -> totalItems 0, items []
DRV-9999 -> 404 DRIVER_NOT_FOUND

```

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd "-Dtest=DriverAssignmentServiceTest,DriverAssignmentControllerTest" test
.\mvnw.cmd test

```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `Invoke-RestMethod "http://localhost:8080/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20"`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod "http://localhost:8080/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20"

```

## Done Criteria

- [x] Active assignment list is correct.
- [x] Empty assignment list is represented as `items: []`.
- [x] Pagination fields match OpenAPI.
- [x] Missing driver and validation errors use ProblemDetail.

## Common Mistakes

- Including completed `ASN-3003` as active work.
- Returning assignment data without enriching order fields.
- Using `page_size` instead of `pageSize`.

## Stop / Do Not Add

- Do not add assignment creation endpoints.
- Do not include completed `ASN-3003` as active work.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized and exact assignment-list response behavior added.
- Implemented and marked done after focused tests and the full Maven suite passed.
