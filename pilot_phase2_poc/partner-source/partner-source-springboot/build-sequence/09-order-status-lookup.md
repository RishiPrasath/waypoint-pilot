# 09 - Order Status Lookup

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement the first contract data endpoint: `GET /api/v1/orders/{orderId}/status`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `8. Response Shapes` and `10. Acceptance Scenarios`
- `../../docs/active/contract-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Prereqs

- Task 06 repositories exist.
- Task 07/08 health endpoints are green.
- Task 10 will replace any temporary error handling.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `src/test/java/com/waypoint/partnersource/order/service/OrderStatusServiceTest.java`, `src/test/java/com/waypoint/partnersource/order/api/OrderStatusControllerTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/order/service/OrderStatusServiceTest.java
src/test/java/com/waypoint/partnersource/order/api/OrderStatusControllerTest.java
```

`OrderStatusServiceTest.java`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `OrderStatusServiceTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
package com.waypoint.partnersource.order.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.order.repository.InMemoryOrderRepository;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;
import org.springframework.web.server.ResponseStatusException;

class OrderStatusServiceTest {

    @Test
    void returnsSeededOrderStatus() {
        var service = new OrderStatusService(
                new InMemoryOrderRepository(SeedDataLoader.load()),
                new OrderResponseMapper()
        );

        var response = service.getStatus("ORD-1001");

        assertEquals("ORD-1001", response.orderId());
        assertEquals(OrderStatus.OUT_FOR_DELIVERY, response.currentStatus());
        assertEquals("DRV-2001", response.assignedDriver().driverId());
        assertNotNull(response.deliveryWindow());
    }

    @Test
    void missingOrderThrowsDomainException() {
        var service = new OrderStatusService(
                new InMemoryOrderRepository(SeedDataLoader.load()),
                new OrderResponseMapper()
        );

        var exception = assertThrows(ResponseStatusException.class, () -> service.getStatus("ORD-9999"));

        assertEquals(404, exception.getStatusCode().value());
    }
}

```

`OrderStatusControllerTest.java`:

**Test Block Explanation**

- What this block does: Shows the controller tests for the happy path, missing order path, and invalid order ID shape.
- Why it exists: It proves the HTTP endpoint matches the contract surface before Task 10 adds the final ProblemDetail body.
- How to read it: The mocked service controls the response for success and missing-order cases; the invalid ID test proves path validation is active.

```java
package com.waypoint.partnersource.order.api;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.waypoint.partnersource.order.api.dto.AssignedDriverSummaryResponse;
import com.waypoint.partnersource.order.api.dto.DeliveryWindowResponse;
import com.waypoint.partnersource.order.api.dto.OrderStatusResponse;
import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.order.service.OrderStatusService;
import java.time.OffsetDateTime;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.HttpStatus;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.server.ResponseStatusException;

@WebMvcTest(OrderStatusController.class)
class OrderStatusControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    OrderStatusService orderStatusService;

    @Test
    void getOrderStatusReturnsContractShape() throws Exception {
        when(orderStatusService.getStatus("ORD-1001"))
                .thenReturn(new OrderStatusResponse(
                        "ORD-1001",
                        OrderStatus.OUT_FOR_DELIVERY,
                        "Out for delivery",
                        null,
                        null,
                        new DeliveryWindowResponse(null, null),
                        new AssignedDriverSummaryResponse("DRV-2001", "A. Kumar"),
                        OffsetDateTime.parse("2026-07-02T09:00:00+08:00")
                ));

        mockMvc.perform(get("/api/v1/orders/ORD-1001/status"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.orderId").value("ORD-1001"))
                .andExpect(jsonPath("$.currentStatus").value("OUT_FOR_DELIVERY"))
                .andExpect(jsonPath("$.statusLabel").value("Out for delivery"))
                .andExpect(jsonPath("$.deliveryWindow").exists())
                .andExpect(jsonPath("$.assignedDriver.driverId").value("DRV-2001"));
    }

    @Test
    void getMissingOrderReturnsNotFound() throws Exception {
        when(orderStatusService.getStatus("ORD-9999"))
                .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Order not found"));

        mockMvc.perform(get("/api/v1/orders/ORD-9999/status"))
                .andExpect(status().isNotFound());
    }

    @Test
    void invalidOrderIdReturnsBadRequest() throws Exception {
        mockMvc.perform(get("/api/v1/orders/INVALID/status"))
                .andExpect(status().isBadRequest());
    }
}

```
## File Map

DTOs:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `order/api/dto/AssignedDriverSummaryResponse.java`, `order/api/dto/DeliveryWindowResponse.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
src/main/java/com/waypoint/partnersource/order/api/dto/AssignedDriverSummaryResponse.java
src/main/java/com/waypoint/partnersource/order/api/dto/DeliveryWindowResponse.java
src/main/java/com/waypoint/partnersource/order/api/dto/LocationSnapshotResponse.java
src/main/java/com/waypoint/partnersource/order/api/dto/OrderStatusResponse.java

```

Service/controller:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `order/service/OrderResponseMapper.java`, `order/service/OrderStatusService.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
src/main/java/com/waypoint/partnersource/order/service/OrderResponseMapper.java
src/main/java/com/waypoint/partnersource/order/service/OrderStatusService.java
src/main/java/com/waypoint/partnersource/order/api/OrderStatusController.java

```

## Exact Code

Create `AssignedDriverSummaryResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `src/main/java/com/waypoint/partnersource/order/api/dto/AssignedDriverSummaryResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.api.dto;

public record AssignedDriverSummaryResponse(String driverId, String displayName) {}

```

Create `DeliveryWindowResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `src/main/java/com/waypoint/partnersource/order/api/dto/DeliveryWindowResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: `start` and `end` are nullable for the current seed data; Task 10/contract hardening can make this stricter once seed dates are filled.

```java
package com.waypoint.partnersource.order.api.dto;

import java.time.OffsetDateTime;

public record DeliveryWindowResponse(OffsetDateTime start, OffsetDateTime end) {}

```

Create `LocationSnapshotResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `src/main/java/com/waypoint/partnersource/order/api/dto/LocationSnapshotResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: The current seed stores location as a label string, so latitude, longitude, and capturedAt stay nullable for Task 9.

```java
package com.waypoint.partnersource.order.api.dto;

import java.time.OffsetDateTime;

public record LocationSnapshotResponse(String label, Double latitude, Double longitude, OffsetDateTime capturedAt) {}

```

Create `OrderStatusResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `OrderStatusResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.api.dto;

import com.waypoint.partnersource.order.domain.OrderStatus;
import java.time.OffsetDateTime;

public record OrderStatusResponse(
        String orderId,
        OrderStatus currentStatus,
        String statusLabel,
        LocationSnapshotResponse currentLocation,
        OffsetDateTime estimatedDeliveryAt,
        DeliveryWindowResponse deliveryWindow,
        AssignedDriverSummaryResponse assignedDriver,
        OffsetDateTime lastUpdatedAt
) {
}

```

Create `OrderResponseMapper.java`:

**Code Block Explanation**

- What this block does: Shows the exact mapper code for converting the seeded `DeliveryOrder` domain record into the OpenAPI response shape.
- Why it exists: It keeps field-name and nested-object mapping out of the controller, which makes later timeline/status-event work easier to follow.
- How to read it: The top-level delivery-window object is always present, while its current seeded start/end values may be null.

```java
package com.waypoint.partnersource.order.service;

import com.waypoint.partnersource.order.api.dto.AssignedDriverSummaryResponse;
import com.waypoint.partnersource.order.api.dto.DeliveryWindowResponse;
import com.waypoint.partnersource.order.api.dto.LocationSnapshotResponse;
import com.waypoint.partnersource.order.api.dto.OrderStatusResponse;
import com.waypoint.partnersource.order.domain.DeliveryOrder;
import org.springframework.stereotype.Component;

@Component
public class OrderResponseMapper {

    public OrderStatusResponse toStatusResponse(DeliveryOrder order) {
        AssignedDriverSummaryResponse assignedDriver = null;
        if (order.assignedDriverId() != null && order.assignedDriverName() != null) {
            assignedDriver = new AssignedDriverSummaryResponse(
                    order.assignedDriverId(),
                    order.assignedDriverName()
            );
        }

        DeliveryWindowResponse deliveryWindow = new DeliveryWindowResponse(
                order.deliveryWindowStart(),
                order.deliveryWindowEnd()
        );

        LocationSnapshotResponse currentLocation = null;
        if (order.currentLocation() != null) {
            currentLocation = new LocationSnapshotResponse(order.currentLocation(), null, null, null);
        }

        return new OrderStatusResponse(
                order.orderId(),
                order.currentStatus(),
                order.statusLabel(),
                currentLocation,
                order.estimatedDeliveryAt(),
                deliveryWindow,
                assignedDriver,
                order.lastUpdatedAt()
        );
    }
}

```

Create `OrderStatusService.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `OrderStatusService.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.service;

import com.waypoint.partnersource.order.api.dto.OrderStatusResponse;
import com.waypoint.partnersource.order.repository.InMemoryOrderRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class OrderStatusService {
    private final InMemoryOrderRepository orderRepository;
    private final OrderResponseMapper mapper;

    public OrderStatusService(InMemoryOrderRepository orderRepository, OrderResponseMapper mapper) {
        this.orderRepository = orderRepository;
        this.mapper = mapper;
    }

    public OrderStatusResponse getStatus(String orderId) {
        return orderRepository.findById(orderId)
                .map(mapper::toStatusResponse)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Order not found"));
    }
}

```

Create `OrderStatusController.java`:

**Code Block Explanation**

- What this block does: Shows the exact controller code for `GET /api/v1/orders/{orderId}/status`.
- Why it exists: It exposes the first contract data endpoint without adding timeline, mutation, auth, or the final Task 10 error envelope.
- How to read it: The explicit pattern check keeps Task 9's malformed-ID behavior deterministic before Task 10 adds centralized validation mapping.

```java
package com.waypoint.partnersource.order.api;

import com.waypoint.partnersource.order.api.dto.OrderStatusResponse;
import com.waypoint.partnersource.order.service.OrderStatusService;
import java.util.regex.Pattern;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api/v1/orders")
public class OrderStatusController {
    private static final Pattern ORDER_ID_PATTERN = Pattern.compile("^ORD-[0-9]{4}$");

    private final OrderStatusService orderStatusService;

    public OrderStatusController(OrderStatusService orderStatusService) {
        this.orderStatusService = orderStatusService;
    }

    @GetMapping("/{orderId}/status")
    public OrderStatusResponse getOrderStatus(@PathVariable String orderId) {
        if (!ORDER_ID_PATTERN.matcher(orderId).matches()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Invalid orderId");
        }

        return orderStatusService.getStatus(orderId);
    }
}

```

This task may use `ResponseStatusException` temporarily. Task 10 replaces that temporary error behavior with the shared ProblemDetail envelope.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd "-Dtest=OrderStatusServiceTest,OrderStatusControllerTest" test
.\mvnw.cmd test
```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `Invoke-RestMethod http://localhost:8080/api/v1/orders/ORD-1001/status`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod http://localhost:8080/api/v1/orders/ORD-1001/status
```

## Done Criteria

- [x] Success service test passes.
- [x] Success controller test passes.
- [x] Missing order test exists.
- [x] Invalid path ID test exists.
- [x] JSON field names match OpenAPI exactly.

## Common Mistakes

- Returning field names that differ from OpenAPI.
- Forgetting the invalid order ID `400` check.
- Implementing timeline in this task.

## Stop / Do Not Add

- Do not implement timeline here.
- Do not add status-event mutation here.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized and exact DTO/service/controller guidance added.
- Pre-flight corrected missing DTO package/import snippets, PowerShell-safe Maven command quoting, and temporary Task 9 error handling before implementation.
- Marked done after focused order-status tests and the full Maven suite passed.
