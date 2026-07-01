# Partner Source Test Plan

## 1. Purpose

This document defines the Slice 1 test plan for `partner-source`.

The goal is to prove that the API contract, domain rules, seed data, and expected HTTP behavior are aligned before implementation continues.

This plan is design-first. It does not assume implementation code already exists.

It should stay aligned with:

- [domain-model-detail.md](domain-model-detail.md)
- [api-contract-detail.md](api-contract-detail.md)
- [seed-data-detail.md](seed-data-detail.md)
- [springboot-testing-playbook.md](springboot-testing-playbook.md)
- [../contracts/openapi/partner-source.v1.yaml](../contracts/openapi/partner-source.v1.yaml)

## 2. Testing Principle

Do not test random Spring Boot classes just because they exist.

Each test should prove one of these:

| Test Proves | Example |
|---|---|
| API contract behavior | `GET /api/v1/orders/ORD-1001/status` returns the required response fields. |
| Domain rule | `DELIVERED -> OUT_FOR_DELIVERY` is rejected. |
| Authorization boundary | `DRV-2002` cannot update `ORD-1001` because the order is not assigned to them. |
| Seed scenario | `DRV-2003` returns an empty assignment list. |
| Error contract | Missing order returns `ProblemDetail` with `ORDER_NOT_FOUND`. |

## 3. Test Levels

| Level | Tooling | Purpose |
|---|---|---|
| Domain unit | JUnit 5 | Test pure business rules such as status transitions and assignment authorization. |
| Service unit | JUnit 5 + Mockito | Test use-case logic with mocked repositories. |
| Controller/API | `@WebMvcTest` + `MockMvc` | Test HTTP method, path, status code, validation, and JSON response shape. |
| Repository behavior | Plain JUnit for in-memory repositories first | Test lookup, filtering, ordering, and save behavior over Slice 1 seed data. Convert to `@DataJpaTest` only when JPA is introduced later. |
| Integration | `@SpringBootTest` + `MockMvc` | Test full request path with seeded data. |
| Contract | OpenAPI validation + API assertions | Test that implementation behavior matches the shared OpenAPI contract. |

## 4. Slice 1 Endpoints Under Test

| Endpoint | Purpose |
|---|---|
| `GET /api/v1/orders/{orderId}/status` | Customer service reads current order status. |
| `GET /api/v1/orders/{orderId}/timeline` | Customer service reads order status history. |
| `GET /api/v1/drivers/{driverId}` | Delivery agent demo login/profile lookup. |
| `GET /api/v1/drivers/{driverId}/assignments` | Delivery agent retrieves assigned work. |
| `POST /api/v1/orders/{orderId}/status-events` | Delivery agent reports a new status event. |
| `GET /health` | Service liveness check. |
| `GET /ready` | Service readiness check. |

## 5. Seed Data Used By Tests

| Seed ID | Type | Test Purpose |
|---|---|---|
| `ORD-1001` | Order | Out-for-delivery happy path. |
| `ORD-1002` | Order | In-transit second assignment. |
| `ORD-1003` | Order | Delivered order for invalid transition tests. |
| `ORD-9999` | Missing order | Negative not-found test. |
| `DRV-2001` | Driver | Active driver with assignments. |
| `DRV-2002` | Driver | Valid but unassigned/unavailable driver. |
| `DRV-2003` | Driver | Available driver with no active assignments. |
| `DRV-9999` | Missing driver | Negative not-found test. |
| `ASN-3001` | Assignment | `DRV-2001` assigned to `ORD-1001`. |
| `ASN-3002` | Assignment | `DRV-2001` assigned to `ORD-1002`. |
| `ASN-3003` | Assignment | Completed assignment for `ORD-1003`. |
| `EVT-4001` to `EVT-4005` | Status events | Timeline for `ORD-1001`. |

## 6. Required Error Codes

The test plan must use the current OpenAPI error names.

| Case | HTTP Status | Error Code |
|---|---:|---|
| Invalid request syntax, path, or query | `400` | `INVALID_REQUEST` |
| Missing order | `404` | `ORDER_NOT_FOUND` |
| Missing driver | `404` | `DRIVER_NOT_FOUND` |
| Missing assignment | `404` | `ASSIGNMENT_NOT_FOUND` |
| Driver is not assigned to order | `403` | `ORDER_NOT_ASSIGNED_TO_DRIVER` |
| Invalid lifecycle transition | `409` | `INVALID_STATUS_TRANSITION` |
| Semantically invalid status event | `422` | `INVALID_STATUS_EVENT` |
| Unexpected server error | `500` | `INTERNAL_SERVER_ERROR` |

Important correction:

```text
Do not use ORDER_TRANSITION_INVALID.
Use INVALID_STATUS_TRANSITION.
```

Validation taxonomy:

| Category | HTTP Status | Error Code | Example |
|---|---:|---|---|
| Invalid request shape | `400` | `INVALID_REQUEST` | malformed JSON, missing `driverId`, invalid enum value, invalid date-time format, invalid path/query format |
| Invalid lifecycle move | `409` | `INVALID_STATUS_TRANSITION` | `DELIVERED -> OUT_FOR_DELIVERY` |
| Invalid status-event meaning | `422` | `INVALID_STATUS_EVENT` | syntactically valid status event with unacceptable business meaning, such as an `occurredAt` far in the future |

## 7. Error Shape Contract

All API error tests should expect a `ProblemDetail`-style response.

Required fields:

```text
type
title
status
detail
instance
errorCode
correlationId
```

Minimum error-shape assertions:

| Assertion | Reason |
|---|---|
| `status` equals HTTP status code | Prevents body/status mismatch. |
| `errorCode` matches expected code | Lets BFF branch safely. |
| `correlationId` is present | Supports debugging. |
| `instance` matches request path | Supports traceability. |
| `detail` is non-empty | Supports human debugging. |

## 8. Domain Unit Tests

### 8.1 `StatusTransitionPolicyTest`

| Test Case | Input | Expected Result |
|---|---|---|
| Allows confirmation | `CREATED -> CONFIRMED` | Allowed |
| Allows pickup | `CONFIRMED -> PICKED_UP` | Allowed |
| Allows in transit | `PICKED_UP -> IN_TRANSIT` | Allowed |
| Allows out for delivery | `IN_TRANSIT -> OUT_FOR_DELIVERY` | Allowed |
| Allows delivery | `OUT_FOR_DELIVERY -> DELIVERED` | Allowed |
| Rejects backward move | `DELIVERED -> OUT_FOR_DELIVERY` | `INVALID_STATUS_TRANSITION` |
| Rejects terminal cancellation move | `CANCELLED -> IN_TRANSIT` | `INVALID_STATUS_TRANSITION` |

### 8.2 `AssignmentAuthorizationPolicyTest`

| Test Case | Seed Data | Expected Result |
|---|---|---|
| Assigned driver can update order | `DRV-2001`, `ORD-1001`, `ASN-3001` | Allowed |
| Unassigned driver cannot update order | `DRV-2002`, `ORD-1001` | `ORDER_NOT_ASSIGNED_TO_DRIVER` |
| Completed assignment does not count as active work | `ASN-3003` | Not active for new update unless deliberately allowed |

## 9. Service Tests

| Service | Test Case | Seed/Fixture | Expected Result |
|---|---|---|---|
| `OrderStatusService` | Existing order returns status | `ORD-1001` | `currentStatus = OUT_FOR_DELIVERY` |
| `OrderStatusService` | Missing order throws not found | `ORD-9999` | `ORDER_NOT_FOUND` |
| `OrderTimelineService` | Existing order returns timeline | `ORD-1001`, `EVT-4001` to `EVT-4005` | Chronological events |
| `DriverService` | Existing driver returns profile | `DRV-2001` | `availabilityStatus = AVAILABLE` |
| `DriverService` | Missing driver throws not found | `DRV-9999` | `DRIVER_NOT_FOUND` |
| `DriverAssignmentService` | Active driver returns active assignments | `DRV-2001`, `ASN-3001`, `ASN-3002` | Two active assignments |
| `DriverAssignmentService` | Available driver with no assignments returns empty list | `DRV-2003` | Empty `items` |
| `StatusEventService` | Assigned driver creates delivered event | `ORD-1001`, `DRV-2001`, `ASN-3001` | `newStatus = DELIVERED` |
| `StatusEventService` | Unassigned driver is rejected | `ORD-1001`, `DRV-2002` | `ORDER_NOT_ASSIGNED_TO_DRIVER` |
| `StatusEventService` | Invalid transition is rejected | `ORD-1003`, `OUT_FOR_DELIVERY` | `INVALID_STATUS_TRANSITION` |

## 10. Controller/API Tests

Controller tests should use `MockMvc` or equivalent HTTP-layer testing.

### 10.1 Order Status

| Request | Expected Status | Key Assertions |
|---|---:|---|
| `GET /api/v1/orders/ORD-1001/status` | `200` | `orderId = ORD-1001`, `currentStatus = OUT_FOR_DELIVERY`, `assignedDriver.driverId = DRV-2001` |
| `GET /api/v1/orders/ORD-9999/status` | `404` | `errorCode = ORDER_NOT_FOUND`, `status = 404` |
| `GET /api/v1/orders/INVALID/status` | `400` | `errorCode = INVALID_REQUEST` |

### 10.2 Order Timeline

| Request | Expected Status | Key Assertions |
|---|---:|---|
| `GET /api/v1/orders/ORD-1001/timeline` | `200` | `orderId = ORD-1001`, `items` not empty, events ordered by `occurredAt` |
| `GET /api/v1/orders/ORD-9999/timeline` | `404` | `errorCode = ORDER_NOT_FOUND` |
| `GET /api/v1/orders/ORD-1001/timeline?page=0` | `400` | `errorCode = INVALID_REQUEST` |

### 10.3 Driver Profile

| Request | Expected Status | Key Assertions |
|---|---:|---|
| `GET /api/v1/drivers/DRV-2001` | `200` | `driverId = DRV-2001`, `availabilityStatus = AVAILABLE`, `activeAssignmentCount = 2` |
| `GET /api/v1/drivers/DRV-9999` | `404` | `errorCode = DRIVER_NOT_FOUND` |
| `GET /api/v1/drivers/INVALID` | `400` | `errorCode = INVALID_REQUEST` |

### 10.4 Driver Assignments

| Request | Expected Status | Key Assertions |
|---|---:|---|
| `GET /api/v1/drivers/DRV-2001/assignments` | `200` | two active assignment items, includes `ORD-1001` and `ORD-1002` |
| `GET /api/v1/drivers/DRV-2003/assignments` | `200` | `items` empty, `totalItems = 0` |
| `GET /api/v1/drivers/DRV-9999/assignments` | `404` | `errorCode = DRIVER_NOT_FOUND` |
| `GET /api/v1/drivers/DRV-2001/assignments?page=0` | `400` | `errorCode = INVALID_REQUEST` |

### 10.5 Create Status Event

| Request | Expected Status | Key Assertions |
|---|---:|---|
| `POST /api/v1/orders/ORD-1001/status-events` with `DRV-2001`, `DELIVERED` | `201` | `previousStatus = OUT_FOR_DELIVERY`, `newStatus = DELIVERED`, `orderCurrentStatus = DELIVERED` |
| `POST /api/v1/orders/ORD-1001/status-events` with `DRV-2002`, `DELIVERED` | `403` | `errorCode = ORDER_NOT_ASSIGNED_TO_DRIVER` |
| `POST /api/v1/orders/ORD-1003/status-events` with `OUT_FOR_DELIVERY` | `409` | `errorCode = INVALID_STATUS_TRANSITION` |
| `POST /api/v1/orders/ORD-9999/status-events` | `404` | `errorCode = ORDER_NOT_FOUND` |
| `POST /api/v1/orders/ORD-1001/status-events` with missing `driverId` | `400` | `errorCode = INVALID_REQUEST` |
| `POST /api/v1/orders/ORD-1001/status-events` with unknown status enum | `400` | `errorCode = INVALID_REQUEST` |
| `POST /api/v1/orders/ORD-1001/status-events` with syntactically valid but semantically invalid event | `422` | `errorCode = INVALID_STATUS_EVENT` |

## 11. Repository Tests

Repository behavior tests are required for Slice 1 because in-memory repositories are part of the planned implementation.

Use plain JUnit tests against in-memory repositories first. Convert or add `@DataJpaTest` only when JPA/H2/PostgreSQL persistence is introduced later.

| Repository Behavior | Expected Result |
|---|---|
| Find order by ID | `ORD-1001` exists, `ORD-9999` does not. |
| Find driver by ID | `DRV-2001` exists, `DRV-9999` does not. |
| Find active assignments by driver | `DRV-2001` returns `ASN-3001`, `ASN-3002`. |
| Find no assignments by driver | `DRV-2003` returns empty list. |
| Find assignment by driver and order | `DRV-2001` + `ORD-1001` exists. |
| Find timeline by order | `ORD-1001` events sorted by `occurredAt`. |
| Save status event | New event can be appended. |

## 12. Integration Tests

Integration tests should be few but meaningful.

| Integration Test | Flow | Expected Result |
|---|---|---|
| Status lookup flow | seeded data -> `GET /status` | `200`, current order facts returned |
| Assignment flow | seeded data -> `GET /drivers/DRV-2001/assignments` | two active assignments |
| Timeline flow | seeded data -> `GET /timeline` | chronological events |
| Status update flow | seeded data -> `POST /status-events` -> `GET /status` | status becomes `DELIVERED` |
| Invalid transition flow | delivered order -> invalid status event | `409 INVALID_STATUS_TRANSITION` |
| Unassigned driver flow | unassigned driver -> status event | `403 ORDER_NOT_ASSIGNED_TO_DRIVER` |

## 13. Contract Tests

Contract tests protect BFF compatibility.

Minimum contract checks:

| Contract Check | Purpose |
|---|---|
| OpenAPI file is valid | Prevents broken contract syntax. |
| Response bodies include required fields | Prevents missing fields. |
| Error responses match `ProblemDetail` | Keeps BFF error handling stable. |
| Enum values match OpenAPI | Prevents implementation-only statuses. |
| Status codes match OpenAPI | Prevents accidental `200` for failed business rules. |

These checks can be local at first and later added to GitHub Actions.

## 14. Manual Request Checklist

The `.http` file should mirror the core tests.

Required request groups:

- happy-path order status
- missing order
- order timeline
- driver profile
- missing driver
- driver assignments
- driver with no assignments
- valid status event
- unassigned-driver status event
- invalid-transition status event

Each request should include comments for:

```text
Expected status
Expected key fields
Expected errorCode when failed
```

## 15. TDD Implementation Order

Recommended test-first order:

1. `StatusTransitionPolicyTest`
2. `AssignmentAuthorizationPolicyTest`
3. repository behavior tests for seed lookup, filtering, timeline ordering, and status-event append
4. `OrderStatusServiceTest`
5. `DriverServiceTest`
6. `DriverAssignmentServiceTest`
7. `StatusEventServiceTest`
8. ProblemDetail and validation error mapping tests
9. `OrderControllerTest`
10. `DriverControllerTest`
11. `DriverAssignmentsControllerTest`
12. `StatusEventControllerTest`
13. integration tests
14. manual `.http` checklist
15. contract validation checks

This order keeps the implementation anchored to behavior instead of framework ceremony.

## 16. Exit Gate

The test design is ready for implementation when:

- [ ] all Slice 1 endpoints have at least one happy-path test
- [ ] all required error cases have a planned test
- [ ] seed data maps to planned tests
- [ ] `ProblemDetail` shape is tested
- [x] `400`, `409`, and `422` validation taxonomy is frozen
- [ ] `INVALID_STATUS_TRANSITION` is used instead of `ORDER_TRANSITION_INVALID`
- [ ] driver authorization is tested
- [ ] timeline ordering is tested
- [x] manual `.http` checklist is aligned
- [ ] CI can run the tests with one command

## 17. Current Recommendation

Use this test plan as the implementation guardrail.

Do not start with broad end-to-end tests.

Start with:

```text
domain policy tests
-> seed/repository behavior tests
-> service tests
-> error handling tests
-> controller tests
-> integration/manual checks
-> contract checks
```

This gives enough safety without drowning the first week in test infrastructure.
