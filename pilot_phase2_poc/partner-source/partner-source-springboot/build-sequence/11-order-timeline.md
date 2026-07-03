# 11 - Order Timeline

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `GET /api/v1/orders/{orderId}/timeline`.

This returns chronological status events for a seeded order.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `8. Response Shapes` and `10. Acceptance Scenarios`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../docs/active/data-and-seed-handoff.md`

## Prereqs

- Task 06 status-event repository exists.
- Task 10 ProblemDetail handling exists.
- Reuse order repository and error handling.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `src/test/java/com/waypoint/partnersource/order/service/OrderTimelineServiceTest.java`, `src/test/java/com/waypoint/partnersource/order/api/OrderTimelineControllerTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/order/service/OrderTimelineServiceTest.java
src/test/java/com/waypoint/partnersource/order/api/OrderTimelineControllerTest.java
```

`OrderTimelineServiceTest.java` core test:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `OrderTimelineServiceTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
@Test
void returnsChronologicalTimelineForOrd1001() {
    var store = SeedDataLoader.load();
    var service = new OrderTimelineService(
            new InMemoryOrderRepository(store),
            new InMemoryStatusEventRepository(store)
    );

    var response = service.getTimeline("ORD-1001", 1, 20);

    assertEquals("ORD-1001", response.orderId());
    assertEquals(5, response.totalItems());
    assertEquals("EVT-4001", response.items().get(0).eventId());
    assertEquals("EVT-4005", response.items().get(4).eventId());
}

```

`OrderTimelineControllerTest.java` should assert:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `OrderTimelineControllerTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
mockMvc.perform(get("/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.orderId").value("ORD-1001"))
        .andExpect(jsonPath("$.page").value(1))
        .andExpect(jsonPath("$.pageSize").value(20))
        .andExpect(jsonPath("$.totalItems").value(5))
        .andExpect(jsonPath("$.items[0].eventId").value("EVT-4001"))
        .andExpect(jsonPath("$.items[4].eventId").value("EVT-4005"));

```
## File Map

DTOs:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `order/api/dto/TimelineEventResponse.java`, `order/api/dto/OrderTimelineResponse.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
order/api/dto/TimelineEventResponse.java
order/api/dto/OrderTimelineResponse.java
```

Service/controller:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `order/service/OrderTimelineService.java`, `order/api/OrderTimelineController.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
order/service/OrderTimelineService.java
order/api/OrderTimelineController.java
```

## Exact Code

Create `TimelineEventResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `TimelineEventResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.api.dto;

import com.waypoint.partnersource.order.domain.ActorType;
import com.waypoint.partnersource.order.domain.OrderStatus;
import java.time.OffsetDateTime;

public record TimelineEventResponse(
        String eventId,
        OrderStatus status,
        String statusLabel,
        OffsetDateTime occurredAt,
        ActorType actorType,
        String actorId
) {
}

```

Create `OrderTimelineResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `OrderTimelineResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.api.dto;

import java.util.List;

public record OrderTimelineResponse(
        String orderId,
        List<TimelineEventResponse> items,
        int page,
        int pageSize,
        int totalItems
) {
}

```

Create `OrderTimelineService.java` to validate the order exists, load events sorted by `occurredAt`, page the list, and return `OrderTimelineResponse`.

Create `OrderTimelineController.java` with:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for `OrderTimelineController.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
GET /api/v1/orders/{orderId}/timeline?page=1&pageSize=20
```

Use `pageSize`, not `page_size`.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd "-Dtest=OrderTimelineServiceTest,OrderTimelineControllerTest" test
.\mvnw.cmd test
```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `Invoke-RestMethod "http://localhost:8080/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod "http://localhost:8080/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"
```

## Done Criteria

- [x] Timeline is chronological.
- [x] Pagination fields match OpenAPI.
- [x] Error envelope is reused.
- [x] No mutation happens in this endpoint.

## Common Mistakes

- Returning events in hash-map order.
- Using `page_size` instead of `pageSize`.
- Adding sorting query parameters not in the contract.

## Stop / Do Not Add

- Do not implement delivery-attempt behavior.
- Do not add sorting query parameters not in the contract.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized and exact timeline DTO/service/controller direction added.
- Implemented and marked done after focused tests and the full Maven suite passed.
