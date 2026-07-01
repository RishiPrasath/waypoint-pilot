# Partner Source Agreed Slice 1 Spec

This is the local implementation copy of the agreed Slice 1 behavior.

Local source-of-truth files are:

```text
docs\00-index.md
docs\active\
docs\contracts\
```

Use this file while building so you do not have to hunt across planning docs for every task.

If this file conflicts with local copied reference notes under `docs/support`, `docs/archive`, or `docs/research`, follow this file. Those folders may preserve older pre-freeze planning context.

## 1. Product Goal

Build a synthetic logistics partner API that gives Waypoint stable demo data for orders, drivers, assignments, and status events.

Slice 1 proves this loop:

```text
seeded order
-> assigned driver
-> current status lookup
-> timeline lookup
-> driver assignment lookup
-> driver creates a valid status event
```

## 2. Implementations

| Implementation | Role |
|---|---|
| Spring Boot | Reference implementation. Build first. |
| FastAPI | Parity implementation. Must match the same contract behavior. |

Both implementations must use in-memory repositories for Slice 1.

Do not add PostgreSQL, H2, JPA, SQLAlchemy, Actuator, authentication, Docker deployment, or OpenAPI server generation in Slice 1.

## 3. Endpoints

| Order | Method | Path | Purpose |
|---:|---|---|---|
| 1 | `GET` | `/health` | Process liveness. |
| 2 | `GET` | `/ready` | In-memory persistence and seed-data readiness. |
| 3 | `GET` | `/api/v1/orders/{orderId}/status` | Read current order status. |
| 4 | `GET` | `/api/v1/orders/{orderId}/timeline` | Read chronological order status events. |
| 5 | `GET` | `/api/v1/drivers/{driverId}` | Read seeded driver profile. |
| 6 | `GET` | `/api/v1/drivers/{driverId}/assignments` | Read active assignments for a driver. |
| 7 | `POST` | `/api/v1/orders/{orderId}/status-events` | Create a valid driver status event. |

## 4. ID Formats

| ID | Pattern | Example |
|---|---|---|
| Order | `^ORD-[0-9]{4}$` | `ORD-1001` |
| Driver | `^DRV-[0-9]{4}$` | `DRV-2001` |
| Assignment | `^ASN-[0-9]{4}$` | `ASN-3001` |
| Event | `^EVT-[0-9]{4}$` | `EVT-4001` |

Invalid ID format returns `400 INVALID_REQUEST`.

## 5. Enums

### OrderStatus

```text
CREATED
CONFIRMED
PICKED_UP
IN_TRANSIT
OUT_FOR_DELIVERY
DELIVERY_ATTEMPTED
DELIVERED
CANCELLED
```

### AssignmentStatus

```text
ASSIGNED
ACCEPTED
COMPLETED
CANCELLED
```

### ActorType

```text
SYSTEM
DRIVER
SUPPORT_AGENT
```

### DriverAvailabilityStatus

```text
AVAILABLE
UNAVAILABLE
OFFLINE
```

## 6. Status Transition Rules

| Current status | Allowed next status |
|---|---|
| `CREATED` | `CONFIRMED`, `CANCELLED` |
| `CONFIRMED` | `PICKED_UP`, `CANCELLED` |
| `PICKED_UP` | `IN_TRANSIT` |
| `IN_TRANSIT` | `OUT_FOR_DELIVERY` |
| `OUT_FOR_DELIVERY` | `DELIVERED` |
| `DELIVERY_ATTEMPTED` | none in Slice 1 |
| `DELIVERED` | none |
| `CANCELLED` | none |

Important: `DELIVERY_ATTEMPTED` may exist in the enum but must not introduce delivery-attempt behavior in Slice 1.

## 7. Seed Data

### Drivers

| ID | Availability | Role |
|---|---|---|
| `DRV-2001` | `AVAILABLE` | Main active driver with two active assignments. |
| `DRV-2002` | `UNAVAILABLE` | Valid but unassigned driver for authorization tests. |
| `DRV-2003` | `AVAILABLE` | Available driver with no assignments. |
| `DRV-9999` | none | Missing-driver negative test ID. |

### Orders

| ID | Current status | Purpose |
|---|---|---|
| `ORD-1001` | `OUT_FOR_DELIVERY` | Main happy-path delivery order. |
| `ORD-1002` | `IN_TRANSIT` | Second active assignment and in-transit example. |
| `ORD-1003` | `DELIVERED` | Delivered order for invalid transition tests. |
| `ORD-1004` | reserved | Slice 2 fixture. Do not expand Slice 1 around it. |
| `ORD-9999` | none | Missing-order negative test ID. |

### Assignments

| ID | Driver | Order | Status | Purpose |
|---|---|---|---|---|
| `ASN-3001` | `DRV-2001` | `ORD-1001` | `ASSIGNED` | Main active delivery job. |
| `ASN-3002` | `DRV-2001` | `ORD-1002` | `ASSIGNED` | Second active delivery job. |
| `ASN-3003` | `DRV-2001` | `ORD-1003` | `COMPLETED` | Delivered-order history and invalid transition scenario. |
| `ASN-3004` | `DRV-2001` | `ORD-1004` | `ASSIGNED` | Slice 2 planning fixture. |

Implementation decision for invalid transition:

```text
For ORD-1003, validate order/driver existence first, then allow the delivered-order invalid-transition rule to return 409 INVALID_STATUS_TRANSITION even though ASN-3003 is completed.
```

This keeps both implementations aligned with the manual HTTP checklist.

### Timeline Seeds

| Order | Events | Expected behavior |
|---|---|---|
| `ORD-1001` | `EVT-4001` to `EVT-4005` | Chronological timeline ending at `OUT_FOR_DELIVERY`. |
| `ORD-1002` | `EVT-4101` to `EVT-4104` | Chronological timeline ending at `IN_TRANSIT`. |
| `ORD-1003` | `EVT-4201` to `EVT-4203` | Chronological timeline ending at `DELIVERED`. |

## 8. Response Shapes

Match the canonical OpenAPI JSON fields.

### HealthResponse

Required:

```text
status
service
```

Example:

```json
{
  "status": "UP",
  "service": "partner-source"
}
```

### ReadinessResponse

Required:

```text
status
service
checks.persistence
checks.seedData
```

Example:

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

### OrderStatusResponse

Required:

```text
orderId
currentStatus
statusLabel
estimatedDeliveryAt
deliveryWindow
lastUpdatedAt
```

Optional or nullable:

```text
currentLocation
assignedDriver
```

Example key values for `ORD-1001`:

```json
{
  "orderId": "ORD-1001",
  "currentStatus": "OUT_FOR_DELIVERY",
  "statusLabel": "Out for delivery",
  "assignedDriver": {
    "driverId": "DRV-2001",
    "displayName": "A. Kumar"
  }
}
```

### OrderTimelineResponse

Required:

```text
orderId
items
page
pageSize
totalItems
```

For `ORD-1001`, `totalItems` is `5`, with events ordered from `EVT-4001` through `EVT-4005`.

### DriverResponse

Required:

```text
driverId
displayName
availabilityStatus
activeAssignmentCount
```

For `DRV-2001`, `activeAssignmentCount` is `2`.

### DriverAssignmentsResponse

Required:

```text
driverId
items
page
pageSize
totalItems
```

For `DRV-2001`, `totalItems` is `2`, including `ORD-1001` and `ORD-1002`.

For `DRV-2003`, `items` is empty and `totalItems` is `0`.

### StatusEventResponse

Required:

```text
eventId
orderId
previousStatus
newStatus
statusLabel
occurredAt
actorType
actorId
orderCurrentStatus
```

For successful delivery of `ORD-1001`:

```text
previousStatus = OUT_FOR_DELIVERY
newStatus = DELIVERED
actorType = DRIVER
actorId = DRV-2001
orderCurrentStatus = DELIVERED
```

## 9. Error Shape

All errors use a `ProblemDetail`-style response.

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

Approved error codes:

```text
INVALID_REQUEST
ORDER_NOT_FOUND
DRIVER_NOT_FOUND
ASSIGNMENT_NOT_FOUND
ORDER_NOT_ASSIGNED_TO_DRIVER
INVALID_STATUS_TRANSITION
INVALID_STATUS_EVENT
INTERNAL_SERVER_ERROR
```

Status mapping:

| HTTP status | Error code | When |
|---:|---|---|
| `400` | `INVALID_REQUEST` | Bad path/query/body shape, invalid enum, invalid date-time, unknown field. |
| `403` | `ORDER_NOT_ASSIGNED_TO_DRIVER` | Driver exists but is not assigned to update the order. |
| `404` | `ORDER_NOT_FOUND` | Order ID does not exist. |
| `404` | `DRIVER_NOT_FOUND` | Driver ID does not exist. |
| `404` | `ASSIGNMENT_NOT_FOUND` | Required assignment relationship does not exist. |
| `409` | `INVALID_STATUS_TRANSITION` | Status move violates lifecycle rules. |
| `422` | `INVALID_STATUS_EVENT` | Request shape is valid but event meaning is unacceptable, such as a far-future `occurredAt`. |
| `500` | `INTERNAL_SERVER_ERROR` | Unexpected server failure. |

## 10. Acceptance Scenarios

| Request | Expected |
|---|---|
| `GET /health` | `200`, `status = UP`, `service = partner-source`. |
| `GET /ready` | `200`, `status = READY`, `checks.persistence = UP`, `checks.seedData = UP`. |
| `GET /api/v1/orders/ORD-1001/status` | `200`, `currentStatus = OUT_FOR_DELIVERY`, `assignedDriver.driverId = DRV-2001`. |
| `GET /api/v1/orders/ORD-9999/status` | `404 ORDER_NOT_FOUND`. |
| `GET /api/v1/orders/INVALID/status` | `400 INVALID_REQUEST`. |
| `GET /api/v1/orders/ORD-1001/timeline?page=1&pageSize=20` | `200`, `totalItems = 5`, chronological events. |
| `GET /api/v1/drivers/DRV-2001` | `200`, `availabilityStatus = AVAILABLE`, `activeAssignmentCount = 2`. |
| `GET /api/v1/drivers/DRV-9999` | `404 DRIVER_NOT_FOUND`. |
| `GET /api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20` | `200`, `totalItems = 2`. |
| `GET /api/v1/drivers/DRV-2003/assignments?page=1&pageSize=20` | `200`, empty `items`. |
| `POST /api/v1/orders/ORD-1001/status-events` with `DRV-2002`, `DELIVERED` | `403 ORDER_NOT_ASSIGNED_TO_DRIVER`. |
| `POST /api/v1/orders/ORD-1001/status-events` with `DRV-9999`, `DELIVERED` | `404 DRIVER_NOT_FOUND`. |
| `POST /api/v1/orders/ORD-1003/status-events` with `DRV-2001`, `OUT_FOR_DELIVERY` | `409 INVALID_STATUS_TRANSITION`. |
| `POST /api/v1/orders/ORD-1001/status-events` with far-future `occurredAt` | `422 INVALID_STATUS_EVENT`. |
| `POST /api/v1/orders/ORD-9999/status-events` | `404 ORDER_NOT_FOUND`. |
| `POST /api/v1/orders/ORD-1001/status-events` with malformed body | `400 INVALID_REQUEST`. |
| `POST /api/v1/orders/ORD-1001/status-events` with `DRV-2001`, `DELIVERED` | `201`, order current status becomes `DELIVERED`. |

## 11. Build Order

Build in this exact order:

1. Spring Boot project scaffold and tiny test.
2. Spring Boot CI proof.
3. FastAPI project scaffold and tiny test.
4. FastAPI CI proof.
5. Status transition policy in Spring Boot, then FastAPI.
6. Assignment authorization policy in Spring Boot, then FastAPI.
7. Seed store and in-memory repositories in Spring Boot, then FastAPI.
8. `/health` in Spring Boot, then FastAPI.
9. `/ready` in Spring Boot, then FastAPI.
10. `GET /orders/{orderId}/status` in Spring Boot, then FastAPI.
11. Shared error envelope in Spring Boot, then FastAPI.
12. `GET /orders/{orderId}/timeline` in Spring Boot, then FastAPI.
13. `GET /drivers/{driverId}` in Spring Boot, then FastAPI.
14. `GET /drivers/{driverId}/assignments` in Spring Boot, then FastAPI.
15. `POST /orders/{orderId}/status-events` in Spring Boot, then FastAPI.
16. Manual HTTP checklist.
17. Contract/parity checks.
