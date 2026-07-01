# 02 - Manual Request Matrix

## Purpose

Define the request matrix that both Spring Boot and FastAPI must satisfy.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `10. Acceptance Scenarios`
- `../../docs/contracts/openapi/http/partner-source-slice1.http`
- `../../docs/active/test-and-acceptance-handoff.md`

## Tests To Write First

Future automated parity tests should encode the same matrix.

Suggested file later:

```text
parity/tests/test_request_matrix.py
```

## Request Matrix

| Scenario | Method | Path | Expected |
|---|---|---|---|
| Health | `GET` | `/health` | `200`, `status = UP` |
| Ready | `GET` | `/ready` | `200`, `status = READY` |
| Order status | `GET` | `/api/v1/orders/ORD-1001/status` | `200`, `currentStatus = OUT_FOR_DELIVERY` before mutation |
| Missing order status | `GET` | `/api/v1/orders/ORD-9999/status` | `404 ORDER_NOT_FOUND` |
| Order timeline | `GET` | `/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20` | `200`, chronological events |
| Driver profile | `GET` | `/api/v1/drivers/DRV-2001` | `200`, `activeAssignmentCount = 2` |
| Missing driver | `GET` | `/api/v1/drivers/DRV-9999` | `404 DRIVER_NOT_FOUND` |
| Driver assignments | `GET` | `/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20` | `200`, two active items |
| Empty assignments | `GET` | `/api/v1/drivers/DRV-2003/assignments?page=1&pageSize=20` | `200`, empty `items` |
| Unassigned update | `POST` | `/api/v1/orders/ORD-1001/status-events` | `403 ORDER_NOT_ASSIGNED_TO_DRIVER` |
| Missing driver update | `POST` | `/api/v1/orders/ORD-1001/status-events` | `404 DRIVER_NOT_FOUND` |
| Invalid transition | `POST` | `/api/v1/orders/ORD-1003/status-events` | `409 INVALID_STATUS_TRANSITION` |
| Semantic event failure | `POST` | `/api/v1/orders/ORD-1001/status-events` | `422 INVALID_STATUS_EVENT` |
| Successful delivery | `POST` | `/api/v1/orders/ORD-1001/status-events` | `201`, `orderCurrentStatus = DELIVERED` |

## Commands To Run

Run manually against each app:

```powershell
$spring = "http://localhost:8080"
$fastapi = "http://localhost:8000"
Invoke-RestMethod "$spring/health"
Invoke-RestMethod "$fastapi/health"
```

## Done Criteria

- [ ] Matrix matches `AGREED_SPEC.md`.
- [ ] Matrix is used for both implementations.
- [ ] State-changing success request is run with a fresh app state or documented reset.

## Stop / Do Not Add

- Do not add endpoints outside this matrix for Slice 1.
