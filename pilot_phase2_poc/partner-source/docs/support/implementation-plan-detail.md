# Partner Source Implementation Plan

## 1. Purpose

This plan converts the accepted Slice 1 API design into an implementation sequence.

The immediate goal is to plan a beginner-friendly Spring Boot `partner-source` implementation path using the approved OpenAPI contract, deterministic seed data, in-memory repositories, and TDD-driven implementation.

Because the Slice 1 API surface has been reduced, Spring Boot and FastAPI can be multitasked after the shared contract is frozen. Spring Boot remains the primary beginner/reference implementation. FastAPI is a contract-parity implementation and must not add endpoints, fields, statuses, persistence, or behavior beyond the frozen contract.

## 2. Governing Decisions

| Decision | Impact |
|---|---|
| ADR-0003 Contract-first rule | OpenAPI and shared contracts define the implementation target. |
| ADR-0005 Implementation order | Build `partner-source` first, then `rag-db`, BFF, and frontend. |
| ADR-0006 Persistence strategy | Use in-memory repositories for Slice 1. Defer H2/PostgreSQL. |
| ADR-0007 Health/readiness strategy | Use custom `/health` and `/ready`. Defer Actuator. |

## 3. Slice 1 Scope

Implement only these endpoints first:

```http
GET /api/v1/orders/{orderId}/status
GET /api/v1/orders/{orderId}/timeline
GET /api/v1/drivers/{driverId}
GET /api/v1/drivers/{driverId}/assignments
POST /api/v1/orders/{orderId}/status-events
GET /health
GET /ready
```

## 4. Explicitly Deferred

Do not implement these in Slice 1:

- PostgreSQL
- H2 unless the implementation gets blocked by in-memory limitations
- Spring Boot Actuator
- authentication and authorization framework
- delivery attempts
- exceptions
- support summary
- driver availability updates
- BFF-specific response shaping

## 5. Implementation Structure

Recommended Spring Boot package structure:

```text
partner-source
-> order
   -> api
   -> domain
   -> repository
   -> service
-> driver
   -> api
   -> domain
   -> repository
   -> service
-> assignment
   -> api
   -> domain
   -> repository
   -> service
-> shared
   -> config
   -> error
   -> openapi
-> seed
```

Purpose of each package:

| Package | Responsibility |
|---|---|
| `order` | Order status, order timeline, status events, and lifecycle policy. |
| `driver` | Driver profile reads and driver availability facts used by Slice 1. |
| `assignment` | Driver-to-order assignment queries and authorization support. |
| `api` | Controllers plus request/response DTOs that match OpenAPI. |
| `domain` | Business concepts and rules for the feature. |
| `repository` | Plain repository interfaces and in-memory implementations for Slice 1. |
| `service` | Application use cases and orchestration for the feature. |
| `shared` | Cross-feature error handling, config, and OpenAPI helpers. |
| `seed` | Deterministic synthetic seed-data creation. |

## 6. TDD Implementation Order

Implement one behavior at a time, with tests first.

### Step 1: Domain Rules

Write tests first:

- `StatusTransitionPolicyTest`
- `AssignmentAuthorizationPolicyTest`

Then implement:

- allowed status transitions
- rejected backward transition, especially `DELIVERED -> OUT_FOR_DELIVERY`
- driver assignment rule, especially `DRV-2002` rejected for `ORD-1001`

### Step 2: Seed Data And Repositories

Write tests first:

- `OrderRepositoryTest`
- `DriverRepositoryTest`
- `AssignmentRepositoryTest`
- `StatusEventRepositoryTest`

Then implement:

- deterministic seed records from `05-data-model-and-seed-data.md`
- in-memory repository interfaces and classes
- lookup behavior for existing and missing records
- assignment filtering by driver and status
- timeline ordering by `occurredAt`

### Step 3: Services

Write tests first:

- `OrderStatusServiceTest`
- `OrderTimelineServiceTest`
- `DriverServiceTest`
- `DriverAssignmentServiceTest`
- `StatusEventServiceTest`

Then implement:

- current order status lookup
- order timeline lookup
- driver profile lookup
- driver assignment lookup
- status-event creation
- order current-status update after a valid event
- missing-resource and invalid-operation exceptions

### Step 4: Error Handling

Write tests first:

- ProblemDetail mapping tests
- validation error tests

Then implement:

- shared ProblemDetail shape
- `correlationId`
- canonical error codes from the shared error contract
- correct HTTP statuses for not found, forbidden, invalid transition, invalid request, and invalid event

### Step 5: Controllers

Write controller tests first:

- `OrderStatusControllerTest`
- `OrderTimelineControllerTest`
- `DriverControllerTest`
- `DriverAssignmentControllerTest`
- `StatusEventControllerTest`
- `OperationsControllerTest`

Then implement:

- all Slice 1 endpoints
- request validation
- query parameter validation
- OpenAPI-aligned response DTOs
- custom `/health` and `/ready`

### Step 6: Integration And Contract Checks

Write or run:

- Spring Boot integration tests over seeded data
- manual `.http` checklist requests
- OpenAPI response-shape checks where practical

The implementation is not complete until the manual checklist and automated tests agree on the same behavior.

## 7. CI/CD Gate

Add GitHub Actions after the first meaningful automated test suite exists.

Minimum first workflow:

```text
checkout
setup-java
run tests
```

Do not spend time on deployment automation until local tests and API behavior are stable.

## 8. FastAPI Equivalent Timing

Start the FastAPI equivalent after Spring Boot has enough reference behavior to mirror. FastAPI remains a parity implementation and must not expand scope.

The FastAPI version should:

- use the same OpenAPI contract
- produce the same response shapes
- use equivalent seed data
- pass equivalent manual `.http` scenarios
- prove that `partner-source` behavior is portable across frameworks
- avoid adding implementation-only behavior that Spring Boot does not share

## 9. Design Gates Before Coding

Before implementation starts, confirm:

- OpenAPI Slice 1 contract is accepted
- shared error contract is accepted
- seed data is accepted
- test plan is accepted
- manual `.http` checklist is accepted
- ADR-0006 persistence strategy is accepted
- ADR-0007 health/readiness strategy is accepted

## 10. Done Criteria

Slice 1 implementation is done when:

- all Slice 1 endpoints exist
- all agreed seed scenarios are represented
- all planned automated tests pass
- manual `.http` checklist passes against local Spring Boot
- `ProblemDetail` errors match the shared error contract
- `/health` returns process liveness
- `/ready` checks in-memory persistence and seed data
- the code can be run and tested with documented commands
