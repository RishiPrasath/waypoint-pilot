# Partner Source Parity Report

## Summary

- Timestamp: `2026-07-05T11:58:41+08:00`
- Spring Boot base URL: `http://localhost:8080`
- FastAPI base URL: `http://localhost:8000`
- Total scenarios: `24`
- Passed: `24`
- Failed: `0`
- Skipped: `0`

## Scenario Results

| Scenario | Use Case | Method | Path | Expected | Spring Boot | FastAPI | Result |
|---|---|---|---|---:|---:|---:|---|
| service-health | Service liveness | GET | `/health` | 200 | 200 | 200 | PASS |
| service-readiness | Service readiness | GET | `/ready` | 200 | 200 | 200 | PASS |
| CSA-02-order-status-happy-path | CSA-02 | GET | `/api/v1/orders/ORD-1001/status` | 200 | 200 | 200 | PASS |
| CSA-03-order-timeline-happy-path | CSA-03 | GET | `/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20` | 200 | 200 | 200 | PASS |
| DA-01-driver-profile-happy-path | DA-01 | GET | `/api/v1/drivers/DRV-2001` | 200 | 200 | 200 | PASS |
| DA-02-driver-assignments-active-driver | DA-02 | GET | `/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20` | 200 | 200 | 200 | PASS |
| DA-02-driver-assignments-filtered-status | DA-02 | GET | `/api/v1/drivers/DRV-2001/assignments?status=OUT_FOR_DELIVERY&page=1&pageSize=20` | 200 | 200 | 200 | PASS |
| DA-02-driver-assignments-empty-driver | DA-02 | GET | `/api/v1/drivers/DRV-2003/assignments?page=1&pageSize=20` | 200 | 200 | 200 | PASS |
| CSA-01-order-status-missing-order | CSA-01 | GET | `/api/v1/orders/ORD-9999/status` | 404 | 404 | 404 | PASS |
| CSA-01-order-status-invalid-id | CSA-01 | GET | `/api/v1/orders/INVALID/status` | 400 | 400 | 400 | PASS |
| CSA-03-order-timeline-missing-order | CSA-03 | GET | `/api/v1/orders/ORD-9999/timeline?page=1&pageSize=20` | 404 | 404 | 404 | PASS |
| CSA-03-order-timeline-invalid-page | CSA-03 | GET | `/api/v1/orders/ORD-1001/timeline?page=0&pageSize=20` | 400 | 400 | 400 | PASS |
| DA-01-driver-profile-missing-driver | DA-01 | GET | `/api/v1/drivers/DRV-9999` | 404 | 404 | 404 | PASS |
| DA-01-driver-profile-invalid-id | DA-01 | GET | `/api/v1/drivers/INVALID` | 400 | 400 | 400 | PASS |
| DA-02-driver-assignments-invalid-status-filter | DA-02 | GET | `/api/v1/drivers/DRV-2001/assignments?status=NOT_A_STATUS&page=1&pageSize=20` | 400 | 400 | 400 | PASS |
| DA-02-driver-assignments-missing-driver | DA-02 | GET | `/api/v1/drivers/DRV-9999/assignments?page=1&pageSize=20` | 404 | 404 | 404 | PASS |
| DA-02-driver-assignments-invalid-page | DA-02 | GET | `/api/v1/drivers/DRV-2001/assignments?page=0&pageSize=20` | 400 | 400 | 400 | PASS |
| DA-05-status-event-unassigned-driver | DA-05 | POST | `/api/v1/orders/ORD-1001/status-events` | 403 | 403 | 403 | PASS |
| DA-05-status-event-missing-driver | DA-05 | POST | `/api/v1/orders/ORD-1001/status-events` | 404 | 404 | 404 | PASS |
| DA-05-status-event-invalid-transition | DA-05 | POST | `/api/v1/orders/ORD-1003/status-events` | 409 | 409 | 409 | PASS |
| DA-05-status-event-future-occurred-at | DA-05 | POST | `/api/v1/orders/ORD-1001/status-events` | 422 | 422 | 422 | PASS |
| DA-05-status-event-missing-order | DA-05 | POST | `/api/v1/orders/ORD-9999/status-events` | 404 | 404 | 404 | PASS |
| DA-05-status-event-malformed-body | DA-05 | POST | `/api/v1/orders/ORD-1001/status-events` | 400 | 400 | 400 | PASS |
| DA-06-status-event-delivered-happy-path | DA-06 | POST | `/api/v1/orders/ORD-1001/status-events` | 201 | 201 | 201 | PASS |
