# Spring Boot API Fundamentals For Partner Source

## 1. Purpose

This document explains the Spring Boot basics needed to build the `partner-source` API.

It is written for a beginner and maps each concept back to the current Waypoint Phase 2 design.

## 2. What Spring Boot Is

Spring Boot is a Java framework that helps you build backend applications without manually configuring every small piece.

Beginner mental model:

```text
Java = programming language
Spring Framework = large Java backend toolbox
Spring Boot = faster, opinionated way to build Spring applications
Spring MVC = web/API layer
Repository = code boundary for reading/writing data
Spring Data JPA + Hibernate = later database tooling, not Slice 1
```

For `partner-source`, Spring Boot will expose synthetic logistics data through REST APIs.

Example:

```text
BFF asks:
GET /api/v1/orders/ORD-1001/status

partner-source returns:
current status, ETA, assigned driver, latest location, last update time
```

## 3. Basic API Request Flow

A typical Spring Boot API request should flow like this:

```text
HTTP request
-> Controller
-> request DTO validation
-> Service
-> domain policy checks
-> Repository
-> database or in-memory store
-> Service maps result
-> response DTO
-> HTTP response
```

For this project:

```text
GET /api/v1/orders/ORD-1001/status
-> OrderController
-> OrderStatusService
-> DeliveryOrderRepository
-> DeliveryOrder
-> OrderStatusResponse
```

## 4. Spring Boot Building Blocks

| Concept | What It Is | Partner-Source Example |
|---|---|---|
| Controller | Receives HTTP requests and returns responses. | `OrderController`, `DriverController` |
| DTO | API request or response shape. | `OrderStatusResponse`, `CreateStatusEventRequest` |
| Service | Coordinates application use cases. | `OrderStatusService`, `StatusEventService` |
| Domain model | Business objects and rules. | `DeliveryOrder`, `DeliveryAssignment` |
| Policy | Business rule class. | `StatusTransitionPolicy`, `AssignmentAuthorizationPolicy` |
| Repository | Data access interface. | `DeliveryOrderRepository`, `DeliveryDriverRepository` |
| Entity | Database-mapped object, deferred until JPA is introduced. | `DeliveryOrderEntity`, `OrderStatusEventEntity` later |
| Mapper | Converts entities/domain objects into DTOs. | `OrderStatusMapper` |
| Validator | Checks request shape before processing. | `@NotNull`, `@Pattern`, `@Size` |
| Exception handler | Converts failures into standard API errors. | `ProblemDetail`, `@RestControllerAdvice` |
| Seed loader | Loads synthetic demo records. | `SeedDataLoader` |

## 5. Recommended Package Structure

Use feature-based packages.

```text
com.waypoint.partnersource
  PartnerSourceApplication.java

  order
    api
      OrderController.java
      OrderStatusResponse.java
      OrderTimelineResponse.java
    domain
      DeliveryOrder.java
      OrderStatus.java
      OrderStatusEvent.java
      StatusTransitionPolicy.java
    repository
      DeliveryOrderRepository.java
      InMemoryDeliveryOrderRepository.java
      OrderStatusEventRepository.java
      InMemoryOrderStatusEventRepository.java
    service
      OrderStatusService.java
      StatusEventService.java

  driver
    api
    domain
    repository
    service

  assignment
    api
    domain
    repository
    service

  shared
    error
    config
    openapi

  seed
    SeedDataLoader.java
```

Why:

- `order`, `driver`, and `assignment` match the domain language.
- It keeps related classes together.
- It is easier to navigate than one giant `controller` folder.
- It can grow later when `delivery-attempts` and `exceptions` are added.

## 6. Controllers

A controller maps HTTP endpoints to Java methods.

Example:

```java
@RestController
@RequestMapping("/api/v1/orders")
class OrderController {

    @GetMapping("/{orderId}/status")
    OrderStatusResponse getOrderStatus(@PathVariable String orderId) {
        return orderStatusService.getOrderStatus(orderId);
    }
}
```

For `partner-source`:

| Controller | Endpoint Responsibility |
|---|---|
| `OrderController` | `GET /orders/{orderId}/status`, `GET /orders/{orderId}/timeline` |
| `DriverController` | `GET /drivers/{driverId}`, `GET /drivers/{driverId}/assignments` |
| `StatusEventController` or `OrderController` | `POST /orders/{orderId}/status-events` |
| `HealthController` or `OperationsController` | Custom `/health` and `/ready` endpoints for Slice 1 |

Actuator is deferred by ADR-0007. Do not add Actuator for Slice 1 just to expose health checks.

Rule:

```text
Keep controllers thin.
Controllers receive requests and delegate.
Services make decisions.
```

## 7. DTOs vs Entities

A DTO is an API shape.

An entity is a database shape.

Do not expose database entities directly as API responses.

Slice 1 boundary:

```text
OpenAPI schema
-> Java DTO
-> service/domain object
-> plain repository interface
-> in-memory repository implementation
```

Reason:

- avoids leaking internal database fields
- keeps the BFF dependent on the API contract, not storage
- lets the database design change without breaking clients
- keeps validation tied to request models

When JPA is introduced later, add entity objects behind the same repository boundary.

## 8. Validation

Validation checks whether an incoming request is shaped correctly.

Common annotations:

```java
@NotNull
@NotBlank
@Pattern
@Size
@Min
@Max
```

Example:

```java
record CreateStatusEventRequest(
    @NotBlank String driverId,
    @NotNull OrderStatus status,
    @Size(max = 500) String note
) {}
```

Important distinction:

```text
Validation says:
status is present and is a known enum value.

Domain policy says:
this status transition is allowed or rejected.
```

## 9. Service Layer

The service layer coordinates use cases.

Creating a status event should roughly follow this flow:

```text
find order
-> find driver
-> check assignment
-> check transition
-> create status event
-> update current order status
-> return response DTO
```

Recommended services:

| Service | Responsibility |
|---|---|
| `OrderStatusService` | Current status and timeline reads. |
| `DriverService` | Driver profile reads. |
| `DriverAssignmentService` | Assignment list queries. |
| `StatusEventService` | Creates status events and updates order status. |

## 10. Repositories And Slice 1 Persistence

Repositories access data.

For Slice 1, use plain Java repository interfaces with in-memory implementations. This keeps the first implementation focused on API behavior, seed data, and domain rules.

Example:

```java
interface DeliveryOrderRepository {
    Optional<DeliveryOrder> findByOrderId(String orderId);
}
```

Likely repositories:

```text
DeliveryOrderRepository
DeliveryDriverRepository
DeliveryAssignmentRepository
OrderStatusEventRepository
```

Useful queries:

```text
findByOrderId(orderId)
findByDriverId(driverId)
findByDriverIdAndAssignmentStatus(driverId, ASSIGNED)
findByOrderIdOrderByOccurredAtAsc(orderId)
```

Spring Data JPA and Hibernate are later learning topics. They should be introduced after the Slice 1 contract and behavior are stable.

## 11. Database Choice

Recommended path:

```text
in-memory first for Slice 1
-> H2 for simple local persistence
-> PostgreSQL for realistic integration testing
```

| Option | Use |
|---|---|
| In-memory repositories | Fastest way to prove contract and service logic. |
| H2 | Easy local/demo/test database. |
| PostgreSQL | More realistic database for serious integration testing. |

Do not rely on H2 forever. It is useful, but PostgreSQL behavior can differ.

## 12. Profiles And Configuration

Profiles let the same app run with different settings.

Recommended profiles:

```text
application.yml
application-local.yml
application-test.yml
application-postgres.yml
```

| Profile | Purpose |
|---|---|
| `local` | Run locally with in-memory setup first. |
| `test` | Run automated tests. |
| `postgres` | Run against local PostgreSQL. |

## 13. Seed Data

Seed data is fake but structured data.

For this project, seed data must prove the API:

```text
available driver
-> assigned order
-> pickup
-> in transit
-> out for delivery
-> delivered
-> timeline visible to support
```

Recommended beginner implementation:

```text
Start with a Java-based seed loader for clarity.
Move to SQL scripts or migrations later if needed.
```

## 14. Error Handling

Use centralized error handling.

Spring concepts:

```java
@RestControllerAdvice
@ExceptionHandler
ProblemDetail
```

Important error cases:

| Error | HTTP Status |
|---|---|
| `ORDER_NOT_FOUND` | `404` |
| `DRIVER_NOT_FOUND` | `404` |
| `ORDER_NOT_ASSIGNED_TO_DRIVER` | `403` |
| `INVALID_STATUS_TRANSITION` | `409` |
| `INVALID_STATUS_EVENT` | `422` |
| `INVALID_REQUEST` | `400` |

## 15. OpenAPI Alignment

OpenAPI is the contract.

For this project:

```text
Local source of truth:
docs/contracts/openapi/partner-source.v1.yaml

Spring Boot implementation:
must match the YAML

Generated Swagger UI:
useful for local testing, but not the source of truth
```

## 16. Source Links

- [Spring Boot documentation](https://docs.spring.io/spring-boot/index.html)
- [Spring Boot - Structuring Your Code](https://docs.spring.io/spring-boot/reference/using/structuring-your-code.html)
- [Spring Framework - Request Mapping](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-requestmapping.html)
- [Spring Framework - Validation](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-validation.html)
- [Spring Boot - Validation](https://docs.spring.io/spring-boot/reference/io/validation.html)
- [Spring Framework - REST Exception Responses](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html)
- [Spring Data JPA - Repository Definitions](https://docs.spring.io/spring-data/jpa/reference/repositories/definition.html)
- [Hibernate ORM User Guide](https://docs.hibernate.org/orm/6.4/userguide/html_single/)
- [Spring Boot - Data Access](https://docs.spring.io/spring-boot/how-to/data-access.html)
- [Spring Boot - Profiles](https://docs.spring.io/spring-boot/reference/features/profiles.html)
- [Spring Boot - Database Initialization](https://docs.spring.io/spring-boot/how-to/data-initialization.html)
- [springdoc-openapi Getting Started](https://springdoc.org/getting-started.html)
- [H2 Database](https://h2database.com/)
- [PostgreSQL](https://www.postgresql.org/)
