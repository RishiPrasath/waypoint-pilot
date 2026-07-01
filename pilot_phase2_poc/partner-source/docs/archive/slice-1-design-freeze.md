# Partner Source Slice 1 Design Freeze

## 1. Status

Status: accepted for implementation planning

This document freezes the `partner-source` Slice 1 API design so implementation can proceed without reopening scope on every endpoint.

## 2. Main Goal

Build a Spring Boot `partner-source` API that exposes synthetic logistics partner data to Waypoint through a stable contract.

The API must support customer-service order-status questions and delivery-agent status updates using deterministic seed data.

## 3. Actors In Scope

| Actor | In Scope |
|---|---|
| Customer Service Agent | Looks up order status and order timeline to answer customer delivery questions. |
| Delivery Agent | Looks up assigned work and updates order status events. |
| System | Checks service health and readiness. |

## 4. Slice 1 Resources Frozen

These resources are frozen for Slice 1:

- `orders`
- `drivers`
- `assignments`
- `status-events`
- `health`
- `ready`

## 5. Slice 1 Endpoints Frozen

```http
GET /api/v1/orders/{orderId}/status
GET /api/v1/orders/{orderId}/timeline
GET /api/v1/drivers/{driverId}
GET /api/v1/drivers/{driverId}/assignments
POST /api/v1/orders/{orderId}/status-events
GET /health
GET /ready
```

## 6. Deferred Resources

These resources are real, but they are out of scope for Slice 1:

- `delivery-attempts`
- `exceptions`
- `support-summary`
- `delivery-view`
- driver availability update endpoint
- BFF-specific response shapes
- H2/PostgreSQL persistence
- Spring Boot Actuator

## 7. Contract Sources

The implementation must follow:

| Contract | Path |
|---|---|
| OpenAPI contract | `90-shared/contracts/openapi/partner-source.v1.yaml` |
| Shared error contract | `90-shared/contracts/shared-error-contract.md` |
| Manual request checklist | `90-shared/contracts/openapi/http/partner-source-slice1.http` |
| API prose contract | `01-partner-source/04-api-contract.md` |

## 8. Seed Scenarios Frozen

Slice 1 seed data must support:

- `ORD-1001` out-for-delivery happy path
- `ORD-1002` in-transit second assignment
- `ORD-1003` delivered order for invalid transition tests
- `ORD-9999` missing-order negative test
- `DRV-2001` active driver with two active assignments
- `DRV-2002` valid but unassigned/unavailable driver
- `DRV-2003` available driver with no active assignments
- `DRV-9999` missing-driver negative test
- `EVT-4001` to `EVT-4005` timeline for `ORD-1001`

## 9. Domain Rules Frozen

The implementation must enforce:

- missing order returns `ORDER_NOT_FOUND`
- missing driver returns `DRIVER_NOT_FOUND`
- unassigned driver update returns `ORDER_NOT_ASSIGNED_TO_DRIVER`
- invalid status transition returns `INVALID_STATUS_TRANSITION`
- semantically invalid status event returns `INVALID_STATUS_EVENT`
- valid status event appends to timeline
- valid status event updates order current status
- timeline responses are ordered by `occurredAt`

Canonical Slice 1 status transition table:

| Current Status | Allowed Next Statuses |
|---|---|
| `CREATED` | `CONFIRMED`, `CANCELLED` |
| `CONFIRMED` | `PICKED_UP`, `CANCELLED` |
| `PICKED_UP` | `IN_TRANSIT` |
| `IN_TRANSIT` | `OUT_FOR_DELIVERY` |
| `OUT_FOR_DELIVERY` | `DELIVERED` |
| `DELIVERY_ATTEMPTED` | none in Slice 1 |
| `DELIVERED` | none |
| `CANCELLED` | none |

`DELIVERY_ATTEMPTED` remains in the enum because the contract may need to read historical or future-compatible data, but creating new delivery-attempt behavior is deferred until the `delivery-attempts` slice.

## 10. Implementation Decisions Frozen

| Topic | Decision |
|---|---|
| Implementation strategy | Spring Boot and FastAPI can be multitasked after the contract is frozen because Slice 1 scope is intentionally small. |
| Spring Boot | Primary beginner/reference implementation. |
| FastAPI | Contract-parity implementation; must not add endpoints, fields, statuses, persistence, or behavior beyond the frozen OpenAPI contract. |
| Persistence | In-memory repositories for Slice 1 |
| Database | H2/PostgreSQL deferred |
| Health/readiness | Custom `/health` and `/ready` |
| Actuator | Deferred |
| Testing style | TDD-driven |
| CI/CD | Add GitHub Actions after meaningful tests exist |

## 11. Readiness Contract Frozen

`/ready` must check the selected Slice 1 persistence strategy and seed data:

```json
{
  "status": "READY",
  "service": "partner-source",
  "checks": {
    "persistence": "UP",
    "seedData": "UP"
  }
}
```

## 12. Design Freeze Checklist

- [x] Actor use cases are in scope.
- [x] Slice 1 resources are frozen.
- [x] Deferred resources are explicitly out of scope.
- [x] Domain model supports all Slice 1 endpoints.
- [x] Seed data proves all Slice 1 scenarios.
- [x] OpenAPI is the implementation contract.
- [x] Shared error contract is aligned.
- [x] Test plan covers the contract.
- [x] Manual requests are runnable.
- [x] Implementation plan is current.

## 13. Next Step

Implementation can start with TDD against the frozen `partner-source` Slice 1 contract.

Spring Boot remains the primary learning/reference implementation. FastAPI can be multitasked as a contract-parity implementation only after the shared contract, seed scenarios, and manual request expectations are frozen.

The first coding task should be domain-policy tests:

1. `StatusTransitionPolicyTest`
2. `AssignmentAuthorizationPolicyTest`
