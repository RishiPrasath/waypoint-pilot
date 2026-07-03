# 06 - Seed Store And Repositories

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Create deterministic in-memory seed data and repository classes used by later services.

This turns the agreed seed tables into reusable Java objects without adding a database.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `7. Seed Data`
- `../../docs/active/data-and-seed-handoff.md`
- `../../docs/support/seed-data-detail.md`

## Prereqs

- Tasks 04 and 05 are complete.
- Domain packages exist.
- Keep repositories in-memory only.

## Tests To Write First

Create these repository tests before implementation:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for Create these repository tests before implementation.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/order/repository/InMemoryOrderRepositoryTest.java
src/test/java/com/waypoint/partnersource/driver/repository/InMemoryDriverRepositoryTest.java
src/test/java/com/waypoint/partnersource/assignment/repository/InMemoryAssignmentRepositoryTest.java
src/test/java/com/waypoint/partnersource/order/repository/InMemoryStatusEventRepositoryTest.java

```

`InMemoryOrderRepositoryTest.java`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `InMemoryOrderRepositoryTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
package com.waypoint.partnersource.order.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class InMemoryOrderRepositoryTest {

    @Test
    void findsSeededOrder() {
        var repository = new InMemoryOrderRepository(SeedDataLoader.load());

        var order = repository.findById("ORD-1001");

        assertTrue(order.isPresent());
        assertEquals(OrderStatus.OUT_FOR_DELIVERY, order.get().currentStatus());
    }

    @Test
    void missingOrderReturnsEmpty() {
        var repository = new InMemoryOrderRepository(SeedDataLoader.load());

        assertTrue(repository.findById("ORD-9999").isEmpty());
    }
}

```

`InMemoryDriverRepositoryTest.java`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `InMemoryDriverRepositoryTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
package com.waypoint.partnersource.driver.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.waypoint.partnersource.driver.domain.DriverAvailabilityStatus;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class InMemoryDriverRepositoryTest {

    @Test
    void findsSeededDriver() {
        var repository = new InMemoryDriverRepository(SeedDataLoader.load());

        var driver = repository.findById("DRV-2001");

        assertTrue(driver.isPresent());
        assertEquals(DriverAvailabilityStatus.AVAILABLE, driver.get().availabilityStatus());
    }

    @Test
    void missingDriverReturnsEmpty() {
        var repository = new InMemoryDriverRepository(SeedDataLoader.load());

        assertTrue(repository.findById("DRV-9999").isEmpty());
    }
}

```

`InMemoryAssignmentRepositoryTest.java`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `InMemoryAssignmentRepositoryTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
package com.waypoint.partnersource.assignment.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.waypoint.partnersource.assignment.domain.AssignmentStatus;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class InMemoryAssignmentRepositoryTest {

    @Test
    void findsActiveAssignmentsForDriver() {
        var repository = new InMemoryAssignmentRepository(SeedDataLoader.load());

        var assignments = repository.findActiveByDriverId("DRV-2001");

        assertEquals(2, assignments.size());
        assertEquals("ASN-3001", assignments.get(0).assignmentId());
        assertEquals("ASN-3002", assignments.get(1).assignmentId());
    }

    @Test
    void completedAssignmentExistsButIsNotActiveWork() {
        var repository = new InMemoryAssignmentRepository(SeedDataLoader.load());

        assertFalse(repository.findActiveByDriverId("DRV-2001").stream()
                .anyMatch(assignment -> "ASN-3003".equals(assignment.assignmentId())));
        assertEquals(AssignmentStatus.COMPLETED, repository.findById("ASN-3003").orElseThrow().status());
    }

    @Test
    void reservedSlice2AssignmentExistsButIsNotActiveWork() {
        var repository = new InMemoryAssignmentRepository(SeedDataLoader.load());

        assertTrue(repository.findById("ASN-3004").isPresent());
        assertFalse(repository.findActiveByDriverId("DRV-2001").stream()
                .anyMatch(assignment -> "ASN-3004".equals(assignment.assignmentId())));
    }
}

```

`InMemoryStatusEventRepositoryTest.java`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `InMemoryStatusEventRepositoryTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
package com.waypoint.partnersource.order.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class InMemoryStatusEventRepositoryTest {

    @Test
    void findsChronologicalEventsForOrder() {
        var repository = new InMemoryStatusEventRepository(SeedDataLoader.load());

        var events = repository.findByOrderId("ORD-1001");

        assertEquals(5, events.size());
        assertEquals("EVT-4001", events.get(0).eventId());
        assertEquals("EVT-4005", events.get(4).eventId());
        assertEquals(OrderStatus.OUT_FOR_DELIVERY, events.get(4).newStatus());
    }

    @Test
    void missingOrderEventsReturnEmptyList() {
        var repository = new InMemoryStatusEventRepository(SeedDataLoader.load());

        assertTrue(repository.findByOrderId("ORD-9999").isEmpty());
    }
}

```
## File Map

Domain:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `order/domain/ActorType.java`, `order/domain/DeliveryOrder.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
order/domain/ActorType.java
order/domain/DeliveryOrder.java
order/domain/OrderStatusEvent.java
driver/domain/DriverAvailabilityStatus.java
driver/domain/DeliveryDriver.java

```

Seed/repositories:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for Seed/repositories.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
shared/seed/SeedDataStore.java
shared/seed/SeedDataLoader.java
shared/seed/SeedDataConfig.java
order/repository/InMemoryOrderRepository.java
driver/repository/InMemoryDriverRepository.java
assignment/repository/InMemoryAssignmentRepository.java
order/repository/InMemoryStatusEventRepository.java

```

## Exact Code

Create `ActorType.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `ActorType.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.domain;

public enum ActorType {
    SYSTEM,
    DRIVER,
    SUPPORT_AGENT
}

```

Create `DriverAvailabilityStatus.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `DriverAvailabilityStatus.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.driver.domain;

public enum DriverAvailabilityStatus {
    AVAILABLE,
    UNAVAILABLE,
    OFFLINE
}

```

Create `DeliveryDriver.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `DeliveryDriver.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.driver.domain;

public record DeliveryDriver(String driverId, String displayName, DriverAvailabilityStatus availabilityStatus) {
}

```

Create `DeliveryOrder.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `DeliveryOrder.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.domain;

import java.time.OffsetDateTime;

public record DeliveryOrder(
        String orderId,
        OrderStatus currentStatus,
        String statusLabel,
        String recipientName,
        String deliveryAddressSummary,
        OffsetDateTime estimatedDeliveryAt,
        OffsetDateTime deliveryWindowStart,
        OffsetDateTime deliveryWindowEnd,
        String currentLocation,
        String assignedDriverId,
        String assignedDriverName,
        OffsetDateTime lastUpdatedAt
) {
    public DeliveryOrder withCurrentStatus(OrderStatus status, String label, OffsetDateTime updatedAt) {
        return new DeliveryOrder(orderId, status, label, recipientName, deliveryAddressSummary,
                estimatedDeliveryAt, deliveryWindowStart, deliveryWindowEnd, currentLocation,
                assignedDriverId, assignedDriverName, updatedAt);
    }
}

```

Create `OrderStatusEvent.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `OrderStatusEvent.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.domain;

import java.time.OffsetDateTime;

public record OrderStatusEvent(
        String eventId,
        String orderId,
        OrderStatus previousStatus,
        OrderStatus newStatus,
        String statusLabel,
        OffsetDateTime occurredAt,
        ActorType actorType,
        String actorId
) {
}

```

Create `SeedDataStore.java` as a holder for mutable in-memory maps:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `SeedDataStore.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.shared.seed;

import com.waypoint.partnersource.assignment.domain.DeliveryAssignment;
import com.waypoint.partnersource.driver.domain.DeliveryDriver;
import com.waypoint.partnersource.order.domain.DeliveryOrder;
import com.waypoint.partnersource.order.domain.OrderStatusEvent;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public final class SeedDataStore {
    private final Map<String, DeliveryOrder> orders;
    private final Map<String, DeliveryDriver> drivers;
    private final Map<String, DeliveryAssignment> assignments;
    private final Map<String, List<OrderStatusEvent>> statusEventsByOrderId;

    public SeedDataStore(Map<String, DeliveryOrder> orders, Map<String, DeliveryDriver> drivers,
                         Map<String, DeliveryAssignment> assignments,
                         Map<String, List<OrderStatusEvent>> statusEventsByOrderId) {
        this.orders = new ConcurrentHashMap<>(orders);
        this.drivers = new ConcurrentHashMap<>(drivers);
        this.assignments = new ConcurrentHashMap<>(assignments);
        this.statusEventsByOrderId = new ConcurrentHashMap<>(statusEventsByOrderId);
    }

    public Map<String, DeliveryOrder> orders() { return orders; }
    public Map<String, DeliveryDriver> drivers() { return drivers; }
    public Map<String, DeliveryAssignment> assignments() { return assignments; }
    public Map<String, List<OrderStatusEvent>> statusEventsByOrderId() { return statusEventsByOrderId; }
}

```

Create `SeedDataLoader.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `SeedDataLoader.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.shared.seed;

import com.waypoint.partnersource.assignment.domain.AssignmentStatus;
import com.waypoint.partnersource.assignment.domain.DeliveryAssignment;
import com.waypoint.partnersource.driver.domain.DeliveryDriver;
import com.waypoint.partnersource.driver.domain.DriverAvailabilityStatus;
import com.waypoint.partnersource.order.domain.ActorType;
import com.waypoint.partnersource.order.domain.DeliveryOrder;
import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.order.domain.OrderStatusEvent;

import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public final class SeedDataLoader {
    private SeedDataLoader() {
    }

    public static SeedDataStore load() {
        var drivers = Map.of(
                "DRV-2001", new DeliveryDriver("DRV-2001", "A. Kumar", DriverAvailabilityStatus.AVAILABLE),
                "DRV-2002", new DeliveryDriver("DRV-2002", "B. Santos", DriverAvailabilityStatus.UNAVAILABLE),
                "DRV-2003", new DeliveryDriver("DRV-2003", "C. Lee", DriverAvailabilityStatus.AVAILABLE)
        );

        var orders = Map.of(
                "ORD-1001", new DeliveryOrder("ORD-1001", OrderStatus.OUT_FOR_DELIVERY, "Out for delivery",
                        "Jamie Tan", "Tampines, Singapore", null, null, null, null,
                        "DRV-2001", "A. Kumar", at("2026-07-02T09:00:00")),
                "ORD-1002", new DeliveryOrder("ORD-1002", OrderStatus.IN_TRANSIT, "In transit",
                        "Priya Nair", "Jurong East, Singapore", null, null, null, null,
                        "DRV-2001", "A. Kumar", at("2026-07-02T08:30:00")),
                "ORD-1003", new DeliveryOrder("ORD-1003", OrderStatus.DELIVERED, "Delivered",
                        "Mei Wong", "Woodlands, Singapore", null, null, null, null,
                        "DRV-2001", "A. Kumar", at("2026-07-01T18:00:00")),
                "ORD-1004", new DeliveryOrder("ORD-1004", OrderStatus.OUT_FOR_DELIVERY, "Out for delivery",
                        "Reserved Slice 2", "Singapore", null, null, null, null,
                        "DRV-2001", "A. Kumar", at("2026-07-02T10:00:00"))
        );

        var assignments = Map.of(
                "ASN-3001", new DeliveryAssignment("ASN-3001", "ORD-1001", "DRV-2001", AssignmentStatus.ASSIGNED),
                "ASN-3002", new DeliveryAssignment("ASN-3002", "ORD-1002", "DRV-2001", AssignmentStatus.ASSIGNED),
                "ASN-3003", new DeliveryAssignment("ASN-3003", "ORD-1003", "DRV-2001", AssignmentStatus.COMPLETED),
                "ASN-3004", new DeliveryAssignment("ASN-3004", "ORD-1004", "DRV-2001", AssignmentStatus.ASSIGNED)
        );

        Map<String, List<OrderStatusEvent>> statusEventsByOrderId = Map.of(
                "ORD-1001", new ArrayList<>(List.of(
                        new OrderStatusEvent("EVT-4001", "ORD-1001", null, OrderStatus.CREATED,
                                "Created", at("2026-07-02T05:00:00"), ActorType.SYSTEM, "system"),
                        new OrderStatusEvent("EVT-4002", "ORD-1001", OrderStatus.CREATED, OrderStatus.CONFIRMED,
                                "Confirmed", at("2026-07-02T06:00:00"), ActorType.SYSTEM, "system"),
                        new OrderStatusEvent("EVT-4003", "ORD-1001", OrderStatus.CONFIRMED, OrderStatus.PICKED_UP,
                                "Picked up", at("2026-07-02T07:00:00"), ActorType.DRIVER, "DRV-2001"),
                        new OrderStatusEvent("EVT-4004", "ORD-1001", OrderStatus.PICKED_UP, OrderStatus.IN_TRANSIT,
                                "In transit", at("2026-07-02T08:00:00"), ActorType.DRIVER, "DRV-2001"),
                        new OrderStatusEvent("EVT-4005", "ORD-1001", OrderStatus.IN_TRANSIT, OrderStatus.OUT_FOR_DELIVERY,
                                "Out for delivery", at("2026-07-02T09:00:00"), ActorType.DRIVER, "DRV-2001")
                )),
                "ORD-1002", new ArrayList<>(List.of(
                        new OrderStatusEvent("EVT-4101", "ORD-1002", null, OrderStatus.CREATED,
                                "Created", at("2026-07-02T05:30:00"), ActorType.SYSTEM, "system"),
                        new OrderStatusEvent("EVT-4102", "ORD-1002", OrderStatus.CREATED, OrderStatus.CONFIRMED,
                                "Confirmed", at("2026-07-02T06:30:00"), ActorType.SYSTEM, "system"),
                        new OrderStatusEvent("EVT-4103", "ORD-1002", OrderStatus.CONFIRMED, OrderStatus.PICKED_UP,
                                "Picked up", at("2026-07-02T07:30:00"), ActorType.DRIVER, "DRV-2001"),
                        new OrderStatusEvent("EVT-4104", "ORD-1002", OrderStatus.PICKED_UP, OrderStatus.IN_TRANSIT,
                                "In transit", at("2026-07-02T08:30:00"), ActorType.DRIVER, "DRV-2001")
                )),
                "ORD-1003", new ArrayList<>(List.of(
                        new OrderStatusEvent("EVT-4201", "ORD-1003", null, OrderStatus.CREATED,
                                "Created", at("2026-07-01T15:00:00"), ActorType.SYSTEM, "system"),
                        new OrderStatusEvent("EVT-4202", "ORD-1003", OrderStatus.CREATED, OrderStatus.OUT_FOR_DELIVERY,
                                "Out for delivery", at("2026-07-01T17:00:00"), ActorType.DRIVER, "DRV-2001"),
                        new OrderStatusEvent("EVT-4203", "ORD-1003", OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED,
                                "Delivered", at("2026-07-01T18:00:00"), ActorType.DRIVER, "DRV-2001")
                ))
        );

        return new SeedDataStore(orders, drivers, assignments, statusEventsByOrderId);
    }

    private static OffsetDateTime at(String value) {
        return OffsetDateTime.parse(value + "+08:00");
    }
}

```

Create `SeedDataConfig.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `SeedDataConfig.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.shared.seed;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SeedDataConfig {
    @Bean
    SeedDataStore seedDataStore() {
        return SeedDataLoader.load();
    }
}

```

Repository rules:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for Repository rules.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
findById returns Optional<T>
missing records return Optional.empty()
list methods return List<T>
repositories do not use JPA or SQL

```

Create `InMemoryOrderRepository.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `InMemoryOrderRepository.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.repository;

import com.waypoint.partnersource.order.domain.DeliveryOrder;
import com.waypoint.partnersource.shared.seed.SeedDataStore;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public class InMemoryOrderRepository {
    private final SeedDataStore store;

    public InMemoryOrderRepository(SeedDataStore store) {
        this.store = store;
    }

    public Optional<DeliveryOrder> findById(String orderId) {
        return Optional.ofNullable(store.orders().get(orderId));
    }

    public void save(DeliveryOrder order) {
        store.orders().put(order.orderId(), order);
    }
}

```

Create `InMemoryDriverRepository.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `InMemoryDriverRepository.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.driver.repository;

import com.waypoint.partnersource.driver.domain.DeliveryDriver;
import com.waypoint.partnersource.shared.seed.SeedDataStore;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public class InMemoryDriverRepository {
    private final SeedDataStore store;

    public InMemoryDriverRepository(SeedDataStore store) {
        this.store = store;
    }

    public Optional<DeliveryDriver> findById(String driverId) {
        return Optional.ofNullable(store.drivers().get(driverId));
    }
}

```

Create `InMemoryAssignmentRepository.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `InMemoryAssignmentRepository.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.assignment.repository;

import com.waypoint.partnersource.assignment.domain.AssignmentStatus;
import com.waypoint.partnersource.assignment.domain.DeliveryAssignment;
import com.waypoint.partnersource.shared.seed.SeedDataStore;
import org.springframework.stereotype.Repository;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.Set;

@Repository
public class InMemoryAssignmentRepository {
    private static final Set<String> ACTIVE_SLICE_1_ASSIGNMENT_IDS = Set.of("ASN-3001", "ASN-3002");

    private final SeedDataStore store;

    public InMemoryAssignmentRepository(SeedDataStore store) {
        this.store = store;
    }

    public Optional<DeliveryAssignment> findById(String assignmentId) {
        return Optional.ofNullable(store.assignments().get(assignmentId));
    }

    public List<DeliveryAssignment> findActiveByDriverId(String driverId) {
        return store.assignments().values().stream()
                .filter(assignment -> assignment.driverId().equals(driverId))
                .filter(assignment -> ACTIVE_SLICE_1_ASSIGNMENT_IDS.contains(assignment.assignmentId()))
                .filter(assignment -> assignment.status() == AssignmentStatus.ASSIGNED
                        || assignment.status() == AssignmentStatus.ACCEPTED)
                .sorted(Comparator.comparing(DeliveryAssignment::assignmentId))
                .toList();
    }

    public List<DeliveryAssignment> findByOrderId(String orderId) {
        return store.assignments().values().stream()
                .filter(assignment -> assignment.orderId().equals(orderId))
                .sorted(Comparator.comparing(DeliveryAssignment::assignmentId))
                .toList();
    }

    public List<DeliveryAssignment> findAll() {
        return store.assignments().values().stream()
                .sorted(Comparator.comparing(DeliveryAssignment::assignmentId))
                .toList();
    }
}

```

Create `InMemoryStatusEventRepository.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `InMemoryStatusEventRepository.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.repository;

import com.waypoint.partnersource.order.domain.OrderStatusEvent;
import com.waypoint.partnersource.shared.seed.SeedDataStore;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

@Repository
public class InMemoryStatusEventRepository {
    private final SeedDataStore store;

    public InMemoryStatusEventRepository(SeedDataStore store) {
        this.store = store;
    }

    public List<OrderStatusEvent> findByOrderId(String orderId) {
        return store.statusEventsByOrderId().getOrDefault(orderId, List.of()).stream()
                .sorted(Comparator.comparing(OrderStatusEvent::occurredAt))
                .toList();
    }

    public void append(OrderStatusEvent event) {
        store.statusEventsByOrderId()
                .computeIfAbsent(event.orderId(), ignored -> new ArrayList<>())
                .add(event);
    }
}

```

Active driver work rule:

`findActiveByDriverId("DRV-2001")` is the Slice 1 active-driver-work query. It must return only `ASN-3001` and `ASN-3002`. Keep `ASN-3004` in seed data because the agreed spec reserves it as a Slice 2 fixture, but do not return it from the Slice 1 active assignment query.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd -Dtest=InMemoryOrderRepositoryTest,InMemoryDriverRepositoryTest,InMemoryAssignmentRepositoryTest,InMemoryStatusEventRepositoryTest test
.\mvnw.cmd test
```

## Done Criteria

- [x] Repository tests pass.
- [x] Seed IDs exactly match `AGREED_SPEC.md`.
- [x] No database dependency exists.
- [x] Repositories return deterministic results.
- [x] `findActiveByDriverId("DRV-2001")` returns only `ASN-3001` and `ASN-3002`.
- [x] `ASN-3004` remains seeded but is not returned as active Slice 1 driver work.

## Common Mistakes

- Including completed `ASN-3003` in active driver work.
- Returning `ASN-3004` from `findActiveByDriverId` just because it is seeded as `ASSIGNED`; it is reserved for Slice 2.
- Forgetting `DRV-2003` should exist with no assignments.
- Reinitializing seed data per request and losing mutations.
- Adding H2, JPA, or SQL repositories.

## Stop / Do Not Add

- Do not add JPA, H2, PostgreSQL, or SQL migrations.
- Do not expose HTTP endpoints in this task.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized and expanded with exact domain, seed, and repository guidance.
