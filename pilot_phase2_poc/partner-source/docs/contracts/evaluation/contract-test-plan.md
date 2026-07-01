# Contract Test Plan

## 1. Purpose

Contract tests protect the boundary between services.

For Slice 1, the most important boundary is:

```text
BFF -> partner-source
```

The goal is not to add new product scope. The goal is to prove that any `partner-source` implementation returns the same HTTP status codes, JSON fields, enum values, pagination shape, and error envelope promised by the shared OpenAPI contract.

## 2. Source Of Truth

| Contract Source | Purpose |
|---|---|
| `../openapi/partner-source.v1.yaml` | Canonical Partner Source API contract. |
| `../shared-error-contract.md` | Canonical `ProblemDetail` and `errorCode` rules. |
| `../openapi/http/partner-source-slice1.http` | Manual smoke checklist for the same contract. |
| `../../active/test-and-acceptance-handoff.md` | Module-level test coverage plan. |

If these disagree, fix the contract documents before implementation code.

## 3. Beginner Mental Model

Normal tests ask:

```text
Does my code work?
```

Contract tests ask:

```text
Can the next service safely depend on this response?
```

For this project, that means the BFF should not care whether the upstream service is the Spring Boot implementation or the FastAPI parity implementation.

## 4. Partner Source Slice 1 Contract Matrix

| Endpoint | Success Contract Checks | Error Contract Checks |
|---|---|---|
| `GET /api/v1/orders/{orderId}/status` | `200`; required fields from `OrderStatusResponse`; `currentStatus` uses `OrderStatus`; assigned driver object shape is stable. | `400 INVALID_REQUEST`; `404 ORDER_NOT_FOUND`; `500 INTERNAL_SERVER_ERROR` uses shared `ProblemDetail`. |
| `GET /api/v1/orders/{orderId}/timeline` | `200`; required fields from `OrderTimelineResponse`; `items` array shape; timeline events ordered by `occurredAt`; pagination fields are stable. | `400 INVALID_REQUEST`; `404 ORDER_NOT_FOUND`; `500 INTERNAL_SERVER_ERROR` uses shared `ProblemDetail`. |
| `GET /api/v1/drivers/{driverId}` | `200`; required fields from `DriverResponse`; `availabilityStatus` uses contract enum; `activeAssignmentCount` is numeric. | `400 INVALID_REQUEST`; `404 DRIVER_NOT_FOUND`; `500 INTERNAL_SERVER_ERROR` uses shared `ProblemDetail`. |
| `GET /api/v1/drivers/{driverId}/assignments` | `200`; required fields from `DriverAssignmentsResponse`; `items` array shape; assignment status/current status enums; pagination fields are stable. | `400 INVALID_REQUEST`; `404 DRIVER_NOT_FOUND`; `500 INTERNAL_SERVER_ERROR` uses shared `ProblemDetail`. |
| `POST /api/v1/orders/{orderId}/status-events` | `201`; required fields from `StatusEventResponse`; previous/new/current status fields use `OrderStatus`; event ID/order ID/driver ID patterns are stable. | `400 INVALID_REQUEST`; `403 ORDER_NOT_ASSIGNED_TO_DRIVER`; `404 ORDER_NOT_FOUND` or `DRIVER_NOT_FOUND`; `409 INVALID_STATUS_TRANSITION`; `422 INVALID_STATUS_EVENT`; `500 INTERNAL_SERVER_ERROR` uses shared `ProblemDetail`. |
| `GET /health` | `200`; `status = UP`; `service = partner-source`. | `500 INTERNAL_SERVER_ERROR` only if the endpoint itself fails unexpectedly. |
| `GET /ready` | `200`; `status = READY`; readiness checks include persistence and seed data. | `503`; `status = NOT_READY`; readiness checks identify what is down. |

## 5. Shared Error Contract Checks

Every error response must include:

```text
type
title
status
detail
instance
errorCode
correlationId
```

Required assertions:

| Check | Why |
|---|---|
| HTTP status equals body `status`. | Prevents confusing BFF branching. |
| `errorCode` is one of the approved codes. | Prevents implementation-only errors. |
| `correlationId` is present. | Keeps debugging consistent. |
| `instance` matches the request path. | Keeps support traces clear. |
| Deprecated codes are not returned. | Prevents drift such as `ORDER_TRANSITION_INVALID`. |

## 6. Spring Boot And FastAPI Parity

When both implementations exist, they must pass the same contract matrix.

| Check | Spring Boot | FastAPI |
|---|---|---|
| Same OpenAPI file | Required | Required |
| Same seed scenarios | Required | Required |
| Same success response fields | Required | Required |
| Same error envelope | Required | Required |
| Same `errorCode` values | Required | Required |
| Same enum values | Required | Required |
| Same pagination shape | Required | Required |

FastAPI may use different internal code, but it must not return a different public API shape.

## 7. First Practical Test Levels

Start simple. Do not build a complex contract-test framework before the first implementation exists.

| Level | When To Use | Example |
|---|---|---|
| OpenAPI validation | Before implementation and in CI later. | Validate `partner-source.v1.yaml` syntax and references. |
| HTTP assertion tests | After a local implementation exists. | Call `GET /status` and assert required fields. |
| Manual `.http` smoke checks | During beginner local testing. | Run the shared `.http` file after local startup. |
| Parity checks | After Spring Boot and FastAPI both exist. | Run the same request set against both base URLs. |

## 8. CI Growth Path

Add checks in this order:

1. Validate OpenAPI file.
2. Run Spring Boot tests that cover the contract matrix.
3. Run manual-equivalent HTTP assertions against local Spring Boot.
4. Add FastAPI contract-parity tests after FastAPI implementation exists.
5. Add BFF consumer contract checks after BFF integration begins.

## 9. Later Boundaries

These are real, but they are not first for Partner Source Slice 1:

| Boundary | Later Contract Focus |
|---|---|
| `BFF -> rag-db` | RAG query shape, cited answer envelope, source/citation errors. |
| `frontend -> BFF` | Chatbot, order status panel, driver workflow response shapes. |

Do not let later boundaries block the current `partner-source` Slice 1 contract plan.
