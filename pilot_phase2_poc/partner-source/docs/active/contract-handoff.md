# Partner Source Contract Handoff

This file explains how the local Partner Source implementation codebases should consume the API contract.

## Source Of Truth

Do not create separate Spring Boot and FastAPI API truth files.

The shared contract files are local to this implementation lane:

- OpenAPI: `../contracts/openapi/partner-source.v1.yaml`
- Shared errors: `../contracts/shared-error-contract.md`
- Manual HTTP checklist: `../contracts/openapi/http/partner-source-slice1.http`

Spring Boot and FastAPI must both match these files.

## Slice 1 Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/v1/orders/{orderId}/status` | Read current order status. |
| `GET` | `/api/v1/orders/{orderId}/timeline` | Read chronological order status events. |
| `GET` | `/api/v1/drivers/{driverId}` | Read seeded driver profile. |
| `GET` | `/api/v1/drivers/{driverId}/assignments` | Read active assignments for a driver. |
| `POST` | `/api/v1/orders/{orderId}/status-events` | Create a valid driver status event. |
| `GET` | `/health` | Check process liveness. |
| `GET` | `/ready` | Check persistence and seed-data readiness. |

## Shared Behavior Rules

- Use JSON field names from the OpenAPI contract.
- Keep IDs deterministic and human-readable, such as `ORD-1001` and `DRV-2001`.
- Keep timestamps as ISO-8601 date-time values with timezone offsets.
- Keep health/readiness endpoints outside `/api/v1`.
- Treat status events as append-only.
- Validate assignment authorization before accepting driver status updates.
- Validate status transitions before mutating current order status.

## Error Contract

All errors should follow the shared ProblemDetail-style shape.

| HTTP status | Error code | Meaning |
|---|---|---|
| `400` | `INVALID_REQUEST` | Request shape, parameter, enum, or validation problem. |
| `403` | `ORDER_NOT_ASSIGNED_TO_DRIVER` | Driver exists but is not allowed to update the order. |
| `404` | `ORDER_NOT_FOUND` | Order ID does not exist. |
| `404` | `DRIVER_NOT_FOUND` | Driver ID does not exist. |
| `404` | `ASSIGNMENT_NOT_FOUND` | Required assignment relationship does not exist. |
| `409` | `INVALID_STATUS_TRANSITION` | Status move is not allowed. |
| `422` | `INVALID_STATUS_EVENT` | Request shape is valid but event meaning is unacceptable. |

## Spring Boot And FastAPI Parity

Parity means both implementations return the same contract behavior for the same seed data.

They may use different internal packages, frameworks, and test tools. They must not invent different endpoints, fields, statuses, error codes, seed scenarios, or business rules.
