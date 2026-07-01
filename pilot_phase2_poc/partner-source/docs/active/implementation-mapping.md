# Spring Boot And FastAPI Implementation Mapping

This file explains how the same Partner Source API should be implemented in Spring Boot and FastAPI.

The goal is not to build yet. The goal is to understand the shape of the future code before we start.

## Core Idea

Spring Boot and FastAPI should implement the same API contract with different framework tools.

```text
OpenAPI contract
  -> same endpoint behavior
  -> same seed data
  -> same domain rules
  -> same errors
  -> Spring Boot implementation
  -> FastAPI implementation
```

The framework changes. The business behavior does not.

## Beginner Mental Model

Think of each implementation as five layers:

| Layer | What It Means | Spring Boot Shape | FastAPI Shape |
|---|---|---|---|
| API edge | Receives HTTP requests and returns HTTP responses. | controller classes with route annotations. | path operation functions on routers. |
| DTO/schema | Defines request and response JSON shapes. | Java records/classes used by controllers. | Pydantic models used as request/response models. |
| Service/use case | Orchestrates one business action. | service classes. | service functions or service classes. |
| Domain rule | Pure business rule with no web framework dependency. | plain Java classes or enums. | plain Python classes/functions/enums. |
| Repository | Reads/writes seed data. | repository interface plus in-memory implementation. | repository class or module backed by in-memory data. |

This is the main implementation rule: keep framework code at the outside, and keep business rules easy to test.

## Same Endpoint, Two Frameworks

Example endpoint:

```text
GET /api/v1/orders/{orderId}/status
```

| Step | Spring Boot | FastAPI |
|---|---|---|
| Route receives request | `OrderStatusController` method with `@GetMapping`. | router function with `@router.get`. |
| Path value enters code | `@PathVariable String orderId`. | function parameter `order_id`. |
| Controller delegates | calls `OrderStatusService.getStatus(orderId)`. | calls `order_status_service.get_status(order_id)`. |
| Service loads data | calls `OrderRepository.findById(orderId)`. | calls `OrderRepository.find_by_id(order_id)`. |
| Service maps result | maps domain object to response DTO. | maps domain object to response model. |
| API returns JSON | controller returns response DTO. | route returns Pydantic response model or compatible dict. |

The important beginner point: a controller/route should be thin. It should not contain all business logic.

## Endpoint Ownership Map

| Endpoint | Service/use case | Domain rule involved | Repository data |
|---|---|---|---|
| `GET /api/v1/orders/{orderId}/status` | order status lookup | none beyond not-found handling | orders, drivers, locations |
| `GET /api/v1/orders/{orderId}/timeline` | order timeline lookup | timeline sorted by `occurredAt` | orders, status events |
| `GET /api/v1/drivers/{driverId}` | driver profile lookup | none beyond not-found handling | drivers |
| `GET /api/v1/drivers/{driverId}/assignments` | driver assignment list | only active assignments in Slice 1 | drivers, assignments, orders |
| `POST /api/v1/orders/{orderId}/status-events` | create status event | assignment authorization, status transition validation | orders, drivers, assignments, status events |
| `GET /health` | liveness check | none | process is running |
| `GET /ready` | readiness check | seed data loaded | repositories and seed manifest |

## Spring Boot Implementation Shape

Use this shape when the Spring Boot codebase is created:

```text
src/main/java/.../partnersource
  PartnerSourceApplication.java
  order
    api
      OrderStatusController.java
      OrderTimelineController.java
      dto
    domain
      DeliveryOrder.java
      OrderStatus.java
      OrderStatusEvent.java
      StatusTransitionPolicy.java
    repository
      OrderRepository.java
      InMemoryOrderRepository.java
      StatusEventRepository.java
    service
      OrderStatusService.java
      OrderTimelineService.java
      StatusEventService.java
  driver
    api
      DriverController.java
      DriverAssignmentController.java
      dto
    domain
      DeliveryDriver.java
      DriverAvailabilityStatus.java
    repository
      DriverRepository.java
      InMemoryDriverRepository.java
    service
      DriverService.java
      DriverAssignmentService.java
  assignment
    domain
      DeliveryAssignment.java
      AssignmentStatus.java
      AssignmentAuthorizationPolicy.java
    repository
      AssignmentRepository.java
      InMemoryAssignmentRepository.java
  shared
    error
      ApiExceptionHandler.java
      ProblemDetailFactory.java
    health
      HealthController.java
      ReadinessController.java
    seed
      SeedDataLoader.java
      SeedDataManifest.java
```

### Spring Boot Rules

- Controllers translate HTTP to service calls.
- DTOs match the OpenAPI JSON fields.
- Services own use-case flow.
- Domain policies stay plain and easy to unit test.
- Repositories hide the in-memory storage details.
- Error handling is centralized instead of repeated in every controller.
- `/health` and `/ready` stay custom for Slice 1.

## FastAPI Implementation Shape

Use this shape when the FastAPI codebase is created:

```text
app
  main.py
  api
    orders.py
    drivers.py
    health.py
  schemas
    orders.py
    drivers.py
    errors.py
  domain
    orders.py
    drivers.py
    assignments.py
    policies.py
  repositories
    orders.py
    drivers.py
    assignments.py
    status_events.py
  services
    order_status.py
    order_timeline.py
    driver_profile.py
    driver_assignments.py
    status_events.py
  seed
    manifest.py
    loader.py
  errors
    exceptions.py
    handlers.py
```

### FastAPI Rules

- Route functions translate HTTP to service calls.
- Pydantic models match the OpenAPI JSON fields.
- Services own use-case flow.
- Domain policies stay plain and easy to unit test.
- Repositories hide the in-memory storage details.
- Error handlers return the shared ProblemDetail-style shape.
- `/health` and `/ready` stay custom for Slice 1.

## What Should Be Identical

| Area | Must Match |
|---|---|
| Endpoints | Same method and path. |
| Request fields | Same names, required fields, and validation meaning. |
| Response fields | Same names, nesting, enum values, and timestamp format. |
| Seed data | Same order, driver, assignment, and event scenarios. |
| Domain rules | Same transition table and assignment authorization rule. |
| Error behavior | Same HTTP status and error code for the same failure. |
| Tests | Same acceptance scenarios, even if test syntax differs. |

## What Can Differ

| Area | Spring Boot | FastAPI |
|---|---|---|
| Language | Java. | Python. |
| Web entrypoint | controller class. | router function. |
| DTO/schema type | Java record/class. | Pydantic model. |
| Dependency wiring | Spring beans and constructor injection. | imports, app setup, or FastAPI dependency functions where useful. |
| Test style | JUnit, Spring Boot Test, MockMvc. | pytest and FastAPI test client. |
| CI command | Maven test/verify command. | Python test command. |

These differences are implementation details. They should not change the API behavior.

## Recommended Beginner Build Order

Do not start by building all endpoints in both frameworks.

Use one small flow first:

```text
1. StatusTransitionPolicy
2. AssignmentAuthorizationPolicy
3. seed repositories
4. GET /api/v1/orders/{orderId}/status
5. GET /health
6. GET /ready
7. repeat the same flow in FastAPI
8. compare responses against the manual HTTP checklist
```

After this first flow works in both frameworks, expand to:

1. order timeline
2. driver profile
3. driver assignments
4. create status event
5. contract checks
6. separate CI/CD pipelines

## First Discussion Questions

Before implementation starts, answer these:

| Question | Recommended answer for now |
|---|---|
| Do we generate server code from OpenAPI? | No. Use OpenAPI as the contract and write beginner-readable code by hand. |
| Do we create one repo or two? | Treat Spring Boot and FastAPI as separate codebases or separate modules with separate pipelines. |
| Do we share seed data as files? | Eventually yes, but for the first beginner implementation, document the seed manifest first and keep both implementations aligned manually. |
| Do we use a real database? | No. In-memory repositories for Slice 1. |
| Do we implement all endpoints at once? | No. Implement one vertical flow first, then repeat the pattern. |
| Which implementation starts first? | Spring Boot starts first as the reference, but FastAPI can follow closely once the first flow is clear. |

## Framework References

These are framework references, not new project decisions:

- Spring MVC maps controller methods to HTTP routes with annotations such as `@RequestMapping`, `@GetMapping`, and `@PostMapping`: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-requestmapping.html
- Spring Boot testing supports MVC controller tests through `@WebMvcTest` and MockMvc-style testing: https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html
- FastAPI uses request bodies and Pydantic models for typed request/response shapes: https://fastapi.tiangolo.com/tutorial/body/
- FastAPI response models document, validate, convert, and filter output data: https://fastapi.tiangolo.com/tutorial/response-model/
- FastAPI dependency functions can provide shared resources or services to route functions: https://fastapi.tiangolo.com/tutorial/dependencies/
- FastAPI documents testing with its test client: https://fastapi.tiangolo.com/tutorial/testing/

