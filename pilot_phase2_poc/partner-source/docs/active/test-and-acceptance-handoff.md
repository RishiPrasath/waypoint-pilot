# Partner Source Test And Acceptance Handoff

This file explains what tests prove the Partner Source Slice 1 plan is ready.

## Testing Principle

Do not test random framework classes just because they exist. Test the behavior promised by the contract, domain rules, seed data, and error model.

Testing must be part of the implementation workflow from the beginning:

```text
write failing test
-> implement smallest passing code
-> refactor while green
-> run local module tests
-> let CI verify the slice
```

CI should be set up before real endpoint work starts, but TDD happens locally. CI proves that the tests still pass after each slice.

## Required Test Levels

| Level | Purpose |
|---|---|
| Domain tests | Prove status transition and assignment authorization rules. |
| Repository tests | Prove deterministic seed lookup behavior. |
| Service tests | Prove use cases and error paths without HTTP noise. |
| Controller/API tests | Prove HTTP method, path, status, validation, and JSON shape. |
| Integration tests | Prove seeded flows work through the application stack. |
| Contract checks | Prove implementation behavior matches OpenAPI and shared errors. |
| Manual HTTP checklist | Let a beginner exercise the API by hand. |

## First TDD And CI Order

1. Spring Boot module skeleton, one tiny test, and Spring Boot CI workflow.
2. FastAPI module skeleton, one tiny test, and FastAPI CI workflow.
3. `StatusTransitionPolicyTest` in Spring Boot, then mirrored in FastAPI.
4. `AssignmentAuthorizationPolicyTest` in Spring Boot, then mirrored in FastAPI.
5. seed repository tests in Spring Boot, then mirrored in FastAPI.
6. `/health` controller/router tests.
7. `/ready` readiness tests.
8. status lookup service and API tests.
9. ProblemDetail and validation mapping tests.
10. timeline service and API tests.
11. driver profile service and API tests.
12. driver assignment service and API tests.
13. status event service and API tests.
14. integration tests.
15. manual `.http` checklist.
16. contract validation and parity checks.

## Core Acceptance Scenarios

| Request | Expected result |
|---|---|
| `GET /api/v1/orders/ORD-1001/status` | `200`, current status is `OUT_FOR_DELIVERY`. |
| `GET /api/v1/orders/ORD-9999/status` | `404 ORDER_NOT_FOUND`. |
| `GET /api/v1/orders/ORD-1001/timeline` | `200`, events are chronological. |
| `GET /api/v1/drivers/DRV-2001` | `200`, driver exists and is available. |
| `GET /api/v1/drivers/DRV-9999` | `404 DRIVER_NOT_FOUND`. |
| `GET /api/v1/drivers/DRV-2001/assignments` | `200`, two active assignment items. |
| `GET /api/v1/drivers/DRV-2003/assignments` | `200`, empty `items`. |
| `POST /api/v1/orders/ORD-1001/status-events` with `DRV-2001`, `DELIVERED` | `201`, order current status becomes `DELIVERED`. |
| `POST /api/v1/orders/ORD-1001/status-events` with `DRV-2002`, `DELIVERED` | `403 ORDER_NOT_ASSIGNED_TO_DRIVER`. |
| `POST /api/v1/orders/ORD-1003/status-events` with backward status | `409 INVALID_STATUS_TRANSITION`. |
| `GET /health` | `200 UP`. |
| `GET /ready` | `200 READY` when in-memory persistence and seed data are loaded. |

## Shared Contract Gates

- OpenAPI file is valid.
- Required paths exist.
- Responses match expected HTTP status codes.
- Error responses match the shared ProblemDetail-style contract.
- Spring Boot and FastAPI produce equivalent results for the same manual request checklist.

## Supporting Files

- Contract test plan: `../contracts/evaluation/contract-test-plan.md`
- Manual HTTP checklist: `../contracts/openapi/http/partner-source-slice1.http`
- Implementation schematic and task sequence reference: `../support/implementation-schematic-and-task-sequence.md`
- Spring Boot testing guide: `../support/springboot-testing-playbook.md`
- FastAPI testing guide: `../support/fastapi-testing-playbook.md`
