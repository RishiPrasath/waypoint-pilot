# Partner Source Contract Sync

This document explains how the Spring Boot and FastAPI implementations stay aligned with the same API contract.

## Local Contract Sources

| Source | Path |
|---|---|
| OpenAPI | `docs\contracts\openapi\partner-source.v1.yaml` |
| Shared errors | `docs\contracts\shared-error-contract.md` |
| Manual HTTP checklist | `docs\contracts\openapi\http\partner-source-slice1.http` |
| Contract handoff | `docs\active\contract-handoff.md` |
| Seed handoff | `docs\active\data-and-seed-handoff.md` |
| Test handoff | `docs\active\test-and-acceptance-handoff.md` |

## Rules

- Use `AGREED_SPEC.md` as the compact working spec while coding.
- Use `docs/` as the local source of truth for this implementation lane.
- Do not create a second contract truth inside Spring Boot.
- Do not create a second contract truth inside FastAPI.
- Local generated files are allowed later only if they record their source and generation command.
- FastAPI's generated OpenAPI output is convenience output, not the canonical contract.
- Spring Boot implementation behavior does not redefine the contract silently.
- Any deliberate endpoint, field, enum, seed, or error-code change must start in the canonical planning/contract files.

## Slice 1 Contract Targets

Both implementations must expose:

| Method | Path |
|---|---|
| `GET` | `/api/v1/orders/{orderId}/status` |
| `GET` | `/api/v1/orders/{orderId}/timeline` |
| `GET` | `/api/v1/drivers/{driverId}` |
| `GET` | `/api/v1/drivers/{driverId}/assignments` |
| `POST` | `/api/v1/orders/{orderId}/status-events` |
| `GET` | `/health` |
| `GET` | `/ready` |

## Shared Error Shape

Errors must follow the shared `ProblemDetail`-style envelope:

```json
{
  "type": "https://waypoint.local/problems/order-not-found",
  "title": "Order not found",
  "status": 404,
  "detail": "No order exists for orderId ORD-9999.",
  "instance": "/api/v1/orders/ORD-9999/status",
  "errorCode": "ORDER_NOT_FOUND",
  "correlationId": "req-123"
}
```

Required fields:

- `type`
- `title`
- `status`
- `detail`
- `instance`
- `errorCode`
- `correlationId`

## Approved Slice 1 Error Codes

- `INVALID_REQUEST`
- `ORDER_NOT_FOUND`
- `DRIVER_NOT_FOUND`
- `ASSIGNMENT_NOT_FOUND`
- `ORDER_NOT_ASSIGNED_TO_DRIVER`
- `INVALID_STATUS_TRANSITION`
- `INVALID_STATUS_EVENT`
- `INTERNAL_SERVER_ERROR`

## Manual Sync Checklist

Use this before claiming a slice is done:

- [ ] Endpoint path and HTTP method match OpenAPI.
- [ ] Request fields match OpenAPI.
- [ ] Response fields match OpenAPI.
- [ ] Error status and `errorCode` match shared error contract.
- [ ] Seed IDs and scenario expectations match seed handoff.
- [ ] Spring Boot and FastAPI tests assert the same behavior.
- [ ] Manual HTTP checklist result is the same for both implementations once both are available.
