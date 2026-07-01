# Spring Boot Partner Source Build Manual

This is the hand-build manual for the Spring Boot Partner Source implementation.

Use the numbered build sequence first:

```text
build-sequence\00-index.md
```

Use this manual as supporting detail with:

```text
..\MANUAL_BUILD_SEQUENCE.md
```

Rule:

```text
write the test
-> see it fail for the right reason
-> write the smallest code
-> run the focused test
-> run .\mvnw.cmd test
-> mark the checklist
```

## 0. Contract Sources

Before implementing behavior, check:

```text
..\docs\active\contract-handoff.md
..\docs\active\data-and-seed-handoff.md
..\docs\active\test-and-acceptance-handoff.md
..\docs\contracts\openapi\partner-source.v1.yaml
..\docs\contracts\shared-error-contract.md
```

## 1. Scaffold The Project

Create a Spring Boot Maven project in this folder.

Use:

| Setting | Value |
|---|---|
| Java | 21 |
| Build tool | Maven |
| Group | `com.waypoint` |
| Artifact | `partner-source-springboot` |
| Package | `com.waypoint.partnersource` |
| Dependencies | Spring Web, Spring Validation, Spring Boot Test |

Expected files:

```text
pom.xml
mvnw
mvnw.cmd
.mvn/wrapper/
src/main/java/com/waypoint/partnersource/PartnerSourceApplication.java
src/test/java/com/waypoint/partnersource/PartnerSourceApplicationTests.java
```

Run:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test
```

Stop: do not add real behavior until this passes.

## 2. Minimal Application Code

`src/main/java/com/waypoint/partnersource/PartnerSourceApplication.java`

```java
package com.waypoint.partnersource;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class PartnerSourceApplication {

    public static void main(String[] args) {
        SpringApplication.run(PartnerSourceApplication.class, args);
    }
}
```

`src/test/java/com/waypoint/partnersource/PartnerSourceApplicationTests.java`

```java
package com.waypoint.partnersource;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class PartnerSourceApplicationTests {

    @Test
    void contextLoads() {
    }
}
```

## 3. Add The Package Skeleton

Create this shape before adding real classes:

```text
src/main/java/com/waypoint/partnersource/
|-- order/
|   |-- api/
|   |-- domain/
|   |-- repository/
|   `-- service/
|-- driver/
|   |-- api/
|   |-- domain/
|   |-- repository/
|   `-- service/
|-- assignment/
|   |-- domain/
|   `-- repository/
`-- shared/
    |-- error/
    |-- health/
    `-- seed/
```

## 4. First Real TDD Slice: Status Transition Policy

Create the test first.

`src/test/java/com/waypoint/partnersource/order/domain/StatusTransitionPolicyTest.java`

```java
package com.waypoint.partnersource.order.domain;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

class StatusTransitionPolicyTest {

    private final StatusTransitionPolicy policy = new StatusTransitionPolicy();

    @Test
    void allowsOutForDeliveryToDelivered() {
        assertThat(policy.canTransition(OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED))
            .isTrue();
    }

    @Test
    void rejectsDeliveredToOutForDelivery() {
        assertThat(policy.canTransition(OrderStatus.DELIVERED, OrderStatus.OUT_FOR_DELIVERY))
            .isFalse();
    }

    @Test
    void allowsConfirmedToPickedUp() {
        assertThat(policy.canTransition(OrderStatus.CONFIRMED, OrderStatus.PICKED_UP))
            .isTrue();
    }

    @Test
    void rejectsDeliveryAttemptedToOutForDeliveryInSlice1() {
        assertThat(policy.canTransition(OrderStatus.DELIVERY_ATTEMPTED, OrderStatus.OUT_FOR_DELIVERY))
            .isFalse();
    }
}
```

Then add:

`src/main/java/com/waypoint/partnersource/order/domain/OrderStatus.java`

```java
package com.waypoint.partnersource.order.domain;

public enum OrderStatus {
    CREATED,
    CONFIRMED,
    PICKED_UP,
    IN_TRANSIT,
    OUT_FOR_DELIVERY,
    DELIVERY_ATTEMPTED,
    DELIVERED,
    CANCELLED
}
```

`src/main/java/com/waypoint/partnersource/order/domain/StatusTransitionPolicy.java`

```java
package com.waypoint.partnersource.order.domain;

import java.util.Map;
import java.util.Set;

public final class StatusTransitionPolicy {

    private static final Map<OrderStatus, Set<OrderStatus>> ALLOWED = Map.of(
        OrderStatus.CREATED, Set.of(OrderStatus.CONFIRMED, OrderStatus.CANCELLED),
        OrderStatus.CONFIRMED, Set.of(OrderStatus.PICKED_UP, OrderStatus.CANCELLED),
        OrderStatus.PICKED_UP, Set.of(OrderStatus.IN_TRANSIT),
        OrderStatus.IN_TRANSIT, Set.of(OrderStatus.OUT_FOR_DELIVERY),
        OrderStatus.OUT_FOR_DELIVERY, Set.of(OrderStatus.DELIVERED)
    );

    public boolean canTransition(OrderStatus current, OrderStatus next) {
        return ALLOWED.getOrDefault(current, Set.of()).contains(next);
    }
}
```

Run:

```powershell
.\mvnw.cmd -Dtest=StatusTransitionPolicyTest test
.\mvnw.cmd test
```

## 5. Assignment Authorization Policy

Write the test first.

`src/test/java/com/waypoint/partnersource/assignment/domain/AssignmentAuthorizationPolicyTest.java`

```java
package com.waypoint.partnersource.assignment.domain;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

class AssignmentAuthorizationPolicyTest {

    private final AssignmentAuthorizationPolicy policy = new AssignmentAuthorizationPolicy();

    @Test
    void allowsAssignedActiveDriverForOrder() {
        DeliveryAssignment assignment = new DeliveryAssignment(
            "ASN-3001",
            "ORD-1001",
            "DRV-2001",
            AssignmentStatus.ASSIGNED
        );

        assertThat(policy.canDriverUpdateOrder("DRV-2001", "ORD-1001", assignment)).isTrue();
    }

    @Test
    void rejectsDifferentDriver() {
        DeliveryAssignment assignment = new DeliveryAssignment(
            "ASN-3001",
            "ORD-1001",
            "DRV-2001",
            AssignmentStatus.ASSIGNED
        );

        assertThat(policy.canDriverUpdateOrder("DRV-2002", "ORD-1001", assignment)).isFalse();
    }

    @Test
    void rejectsCompletedAssignment() {
        DeliveryAssignment assignment = new DeliveryAssignment(
            "ASN-3001",
            "ORD-1001",
            "DRV-2001",
            AssignmentStatus.COMPLETED
        );

        assertThat(policy.canDriverUpdateOrder("DRV-2001", "ORD-1001", assignment)).isFalse();
    }
}
```

Add:

`src/main/java/com/waypoint/partnersource/assignment/domain/AssignmentStatus.java`

```java
package com.waypoint.partnersource.assignment.domain;

public enum AssignmentStatus {
    ASSIGNED,
    ACCEPTED,
    COMPLETED,
    CANCELLED
}
```

`src/main/java/com/waypoint/partnersource/assignment/domain/DeliveryAssignment.java`

```java
package com.waypoint.partnersource.assignment.domain;

public record DeliveryAssignment(
    String assignmentId,
    String orderId,
    String driverId,
    AssignmentStatus status
) {
}
```

`src/main/java/com/waypoint/partnersource/assignment/domain/AssignmentAuthorizationPolicy.java`

```java
package com.waypoint.partnersource.assignment.domain;

public final class AssignmentAuthorizationPolicy {

    public boolean canDriverUpdateOrder(
        String driverId,
        String orderId,
        DeliveryAssignment assignment
    ) {
        return assignment != null
            && assignment.status() == AssignmentStatus.ASSIGNED
            && assignment.driverId().equals(driverId)
            && assignment.orderId().equals(orderId);
    }
}
```

Run:

```powershell
.\mvnw.cmd -Dtest=AssignmentAuthorizationPolicyTest test
.\mvnw.cmd test
```

## 6. Seed Store And In-Memory Repositories

Start with repository tests, then add simple records and in-memory maps.

Minimum domain records:

`src/main/java/com/waypoint/partnersource/order/domain/DeliveryOrder.java`

```java
package com.waypoint.partnersource.order.domain;

import java.time.OffsetDateTime;

public record DeliveryOrder(
    String orderId,
    OrderStatus currentStatus,
    String assignedDriverId,
    OffsetDateTime lastUpdatedAt
) {
    public DeliveryOrder withStatus(OrderStatus nextStatus, OffsetDateTime updatedAt) {
        return new DeliveryOrder(orderId, nextStatus, assignedDriverId, updatedAt);
    }
}
```

`src/main/java/com/waypoint/partnersource/driver/domain/DeliveryDriver.java`

```java
package com.waypoint.partnersource.driver.domain;

public record DeliveryDriver(
    String driverId,
    String displayName,
    String availabilityStatus
) {
}
```

Seed store:

`src/main/java/com/waypoint/partnersource/shared/seed/SeedDataStore.java`

```java
package com.waypoint.partnersource.shared.seed;

import com.waypoint.partnersource.assignment.domain.AssignmentStatus;
import com.waypoint.partnersource.assignment.domain.DeliveryAssignment;
import com.waypoint.partnersource.driver.domain.DeliveryDriver;
import com.waypoint.partnersource.order.domain.DeliveryOrder;
import com.waypoint.partnersource.order.domain.OrderStatus;
import java.time.OffsetDateTime;
import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.stereotype.Component;

@Component
public class SeedDataStore {

    public Map<String, DeliveryOrder> ordersById() {
        Map<String, DeliveryOrder> orders = new LinkedHashMap<>();
        orders.put("ORD-1001", new DeliveryOrder(
            "ORD-1001",
            OrderStatus.OUT_FOR_DELIVERY,
            "DRV-2001",
            OffsetDateTime.parse("2026-07-01T09:00:00+08:00")
        ));
        return orders;
    }

    public Map<String, DeliveryDriver> driversById() {
        Map<String, DeliveryDriver> drivers = new LinkedHashMap<>();
        drivers.put("DRV-2001", new DeliveryDriver("DRV-2001", "Aisha Tan", "AVAILABLE"));
        drivers.put("DRV-2003", new DeliveryDriver("DRV-2003", "Ravi Kumar", "AVAILABLE"));
        return drivers;
    }

    public Map<String, DeliveryAssignment> assignmentsById() {
        Map<String, DeliveryAssignment> assignments = new LinkedHashMap<>();
        assignments.put("ASN-3001", new DeliveryAssignment(
            "ASN-3001",
            "ORD-1001",
            "DRV-2001",
            AssignmentStatus.ASSIGNED
        ));
        return assignments;
    }
}
```

Repository pattern:

`src/main/java/com/waypoint/partnersource/order/repository/OrderRepository.java`

```java
package com.waypoint.partnersource.order.repository;

import com.waypoint.partnersource.order.domain.DeliveryOrder;
import java.util.Optional;

public interface OrderRepository {
    Optional<DeliveryOrder> findById(String orderId);
    void save(DeliveryOrder order);
}
```

`src/main/java/com/waypoint/partnersource/order/repository/InMemoryOrderRepository.java`

```java
package com.waypoint.partnersource.order.repository;

import com.waypoint.partnersource.order.domain.DeliveryOrder;
import com.waypoint.partnersource.shared.seed.SeedDataStore;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;
import org.springframework.stereotype.Repository;

@Repository
public class InMemoryOrderRepository implements OrderRepository {

    private final Map<String, DeliveryOrder> orders;

    public InMemoryOrderRepository(SeedDataStore seedDataStore) {
        this.orders = new LinkedHashMap<>(seedDataStore.ordersById());
    }

    @Override
    public Optional<DeliveryOrder> findById(String orderId) {
        return Optional.ofNullable(orders.get(orderId));
    }

    @Override
    public void save(DeliveryOrder order) {
        orders.put(order.orderId(), order);
    }
}
```

Add driver and assignment repositories using the same pattern.

## 7. Health Endpoint

Test first:

`src/test/java/com/waypoint/partnersource/shared/health/HealthControllerTest.java`

```java
package com.waypoint.partnersource.shared.health;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(HealthController.class)
class HealthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void returnsUp() throws Exception {
        mockMvc.perform(get("/health"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("UP"))
            .andExpect(jsonPath("$.service").value("partner-source"));
    }
}
```

Implementation:

`src/main/java/com/waypoint/partnersource/shared/health/HealthController.java`

```java
package com.waypoint.partnersource.shared.health;

import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {

    @GetMapping("/health")
    public Map<String, String> getHealth() {
        return Map.of(
            "status", "UP",
            "service", "partner-source"
        );
    }
}
```

## 8. Readiness Endpoint

Implementation shape:

`src/main/java/com/waypoint/partnersource/shared/health/ReadinessService.java`

```java
package com.waypoint.partnersource.shared.health;

import com.waypoint.partnersource.shared.seed.SeedDataStore;
import org.springframework.stereotype.Service;

@Service
public class ReadinessService {

    private final SeedDataStore seedDataStore;

    public ReadinessService(SeedDataStore seedDataStore) {
        this.seedDataStore = seedDataStore;
    }

    public boolean isReady() {
        return !seedDataStore.ordersById().isEmpty()
            && !seedDataStore.driversById().isEmpty();
    }
}
```

`src/main/java/com/waypoint/partnersource/shared/health/ReadinessController.java`

```java
package com.waypoint.partnersource.shared.health;

import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReadinessController {

    private final ReadinessService readinessService;

    public ReadinessController(ReadinessService readinessService) {
        this.readinessService = readinessService;
    }

    @GetMapping("/ready")
    public Map<String, Object> getReadiness() {
        return Map.of(
            "status", readinessService.isReady() ? "READY" : "NOT_READY",
            "service", "partner-source",
            "checks", Map.of(
                "persistence", "UP",
                "seedData", readinessService.isReady() ? "UP" : "DOWN"
            )
        );
    }
}
```

## 9. Shared Error Envelope

Add after the first negative API path exists.

`src/main/java/com/waypoint/partnersource/shared/error/ErrorCode.java`

```java
package com.waypoint.partnersource.shared.error;

public enum ErrorCode {
    INVALID_REQUEST,
    ORDER_NOT_FOUND,
    DRIVER_NOT_FOUND,
    ASSIGNMENT_NOT_FOUND,
    ORDER_NOT_ASSIGNED_TO_DRIVER,
    INVALID_STATUS_TRANSITION,
    INVALID_STATUS_EVENT,
    INTERNAL_SERVER_ERROR
}
```

`src/main/java/com/waypoint/partnersource/shared/error/PartnerSourceException.java`

```java
package com.waypoint.partnersource.shared.error;

import org.springframework.http.HttpStatus;

public class PartnerSourceException extends RuntimeException {

    private final HttpStatus status;
    private final ErrorCode errorCode;
    private final String title;
    private final String type;

    private PartnerSourceException(
        HttpStatus status,
        ErrorCode errorCode,
        String title,
        String detail,
        String type
    ) {
        super(detail);
        this.status = status;
        this.errorCode = errorCode;
        this.title = title;
        this.type = type;
    }

    public static PartnerSourceException orderNotFound(String orderId) {
        return new PartnerSourceException(
            HttpStatus.NOT_FOUND,
            ErrorCode.ORDER_NOT_FOUND,
            "Order not found",
            "No order exists for orderId " + orderId + ".",
            "https://waypoint.local/problems/order-not-found"
        );
    }

    public HttpStatus status() {
        return status;
    }

    public ErrorCode errorCode() {
        return errorCode;
    }

    public String title() {
        return title;
    }

    public String type() {
        return type;
    }
}
```

`src/main/java/com/waypoint/partnersource/shared/error/ApiExceptionHandler.java`

```java
package com.waypoint.partnersource.shared.error;

import jakarta.servlet.http.HttpServletRequest;
import java.net.URI;
import org.springframework.http.MediaType;
import org.springframework.http.ProblemDetail;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(PartnerSourceException.class)
    public ResponseEntity<ProblemDetail> handlePartnerSourceException(
        PartnerSourceException exception,
        HttpServletRequest request
    ) {
        ProblemDetail body = ProblemDetail.forStatusAndDetail(
            exception.status(),
            exception.getMessage()
        );

        body.setType(URI.create(exception.type()));
        body.setTitle(exception.title());
        body.setInstance(URI.create(request.getRequestURI()));
        body.setProperty("errorCode", exception.errorCode().name());
        body.setProperty("correlationId", correlationIdFrom(request));

        return ResponseEntity
            .status(exception.status())
            .contentType(MediaType.APPLICATION_PROBLEM_JSON)
            .body(body);
    }

    private String correlationIdFrom(HttpServletRequest request) {
        String header = request.getHeader("X-Correlation-Id");
        return header == null || header.isBlank() ? "req-local" : header;
    }
}
```

## 10. First Contract Endpoint: Order Status Lookup

DTO:

`src/main/java/com/waypoint/partnersource/order/api/dto/OrderStatusResponse.java`

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

Create the nested DTO records used above before compiling:

```text
LocationSnapshotResponse
DeliveryWindowResponse
AssignedDriverSummaryResponse
```

Service:

`src/main/java/com/waypoint/partnersource/order/service/OrderStatusService.java`

```java
package com.waypoint.partnersource.order.service;

import com.waypoint.partnersource.order.api.dto.OrderStatusResponse;
import com.waypoint.partnersource.order.domain.DeliveryOrder;
import com.waypoint.partnersource.order.repository.OrderRepository;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import org.springframework.stereotype.Service;

@Service
public class OrderStatusService {

    private final OrderRepository orderRepository;

    public OrderStatusService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public OrderStatusResponse getStatus(String orderId) {
        DeliveryOrder order = orderRepository.findById(orderId)
            .orElseThrow(() -> PartnerSourceException.orderNotFound(orderId));

        return new OrderStatusResponse(
            order.orderId(),
            order.currentStatus(),
            labelFor(order),
            null,
            null,
            null,
            null,
            order.lastUpdatedAt()
        );
    }

    private String labelFor(DeliveryOrder order) {
        return order.currentStatus().name().replace('_', ' ');
    }
}
```

Controller:

`src/main/java/com/waypoint/partnersource/order/api/OrderStatusController.java`

```java
package com.waypoint.partnersource.order.api;

import com.waypoint.partnersource.order.api.dto.OrderStatusResponse;
import com.waypoint.partnersource.order.service.OrderStatusService;
import jakarta.validation.constraints.Pattern;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/orders")
@Validated
public class OrderStatusController {

    private final OrderStatusService orderStatusService;

    public OrderStatusController(OrderStatusService orderStatusService) {
        this.orderStatusService = orderStatusService;
    }

    @GetMapping("/{orderId}/status")
    public OrderStatusResponse getOrderStatus(
        @PathVariable @Pattern(regexp = "^ORD-[0-9]{4}$") String orderId
    ) {
        return orderStatusService.getStatus(orderId);
    }
}
```

## 11. Remaining Endpoint Order

Build in this order:

1. `GET /api/v1/orders/{orderId}/timeline`
2. `GET /api/v1/drivers/{driverId}`
3. `GET /api/v1/drivers/{driverId}/assignments`
4. `POST /api/v1/orders/{orderId}/status-events`

For each endpoint:

```text
service test
-> controller test
-> success implementation
-> not-found/error test
-> error implementation
-> full .\mvnw.cmd test
```

## 12. CI Manual

Create this from repo root:

`C:\Users\prasa\Documents\Github\waypoint-pilot\.github\workflows\partner-source-springboot-ci.yml`

```yaml
name: Partner Source Spring Boot CI

on:
  pull_request:
    paths:
      - "pilot_phase2_poc/partner-source/partner-source-springboot/**"
      - ".github/workflows/partner-source-springboot-ci.yml"
  push:
    branches: [main]
    paths:
      - "pilot_phase2_poc/partner-source/partner-source-springboot/**"
      - ".github/workflows/partner-source-springboot-ci.yml"

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: pilot_phase2_poc/partner-source/partner-source-springboot
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "21"
          cache: maven
      - run: chmod +x ./mvnw
      - run: ./mvnw test
```

## 13. Done Criteria

Spring Boot is ready for FastAPI parity work when:

- [ ] scaffold test passes locally
- [ ] CI proves the scaffold test
- [ ] `StatusTransitionPolicyTest` passes
- [ ] `AssignmentAuthorizationPolicyTest` passes
- [ ] seed repositories pass
- [ ] `/health` passes
- [ ] `/ready` passes
- [ ] order status lookup success and not-found tests pass
- [ ] shared error envelope tests pass
