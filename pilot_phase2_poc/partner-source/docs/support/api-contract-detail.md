# Partner Source API Contract

## 1. Purpose

This document defines the human-readable Slice 1 API contract for `partner-source`.

It is the review layer before writing the formal OpenAPI YAML.

Slice 1 must prove the core operational loop:

```text
delivery agent retrieves assigned orders
delivery agent updates order status
customer service agent reads updated status and timeline
```

The contract is intentionally small because the implementation target is one week.

## 2. Contract Scope

### Included In Slice 1

```http
GET /api/v1/orders/{orderId}/status
GET /api/v1/orders/{orderId}/timeline
GET /api/v1/drivers/{driverId}
GET /api/v1/drivers/{driverId}/assignments
POST /api/v1/orders/{orderId}/status-events
GET /health
GET /ready
```

### Deferred To Slice 2 Or Later

```http
GET /api/v1/orders/{orderId}/support-summary
GET /api/v1/orders/{orderId}/exceptions
POST /api/v1/orders/{orderId}/delivery-attempts
GET /api/v1/orders/{orderId}/available-actions
GET /api/v1/orders/{orderId}/delivery-view
POST /api/v1/orders/{orderId}/exceptions
POST /api/v1/orders/{orderId}/notes
POST /api/v1/orders/{orderId}/assignments
```

## 3. Base URL And Versioning

Base API path:

```http
/api/v1
```

Operational endpoints:

```http
/health
/ready
```

Versioning decision:

- Use URL versioning for the MVP.
- Use `/api/v1` for all domain API endpoints.
- Keep health/readiness endpoints outside `/api/v1`.

## 4. Actors

| Actor | Role In Slice 1 |
|---|---|
| Customer Service Agent | Reads order status and timeline. |
| Delivery Agent | Reads driver profile, reads assignments, and creates status events. |
| BFF | API consumer that calls `partner-source`; frontend should not call `partner-source` directly. |
| System | Calls health and readiness endpoints. |

## 5. Resource Summary

| Resource | Slice 1 Role |
|---|---|
| `orders` | Stores current status, ETA, location, and assigned driver summary. |
| `drivers` | Stores seeded driver profile. |
| `assignments` | Connects drivers to assigned orders. |
| `status-events` | Append-only events created when delivery status changes. |
| `health` | Confirms process liveness. |
| `ready` | Confirms service readiness. |

## 6. Shared Conventions

### JSON Naming

Use `camelCase` for JSON fields.

Example:

```json
{
  "orderId": "ORD-1001",
  "currentStatus": "OUT_FOR_DELIVERY",
  "lastUpdatedAt": "2026-06-30T10:15:00+08:00"
}
```

### IDs

Use stable demo IDs:

```text
ORD-1001
DRV-2001
ASN-3001
EVT-4001
```

### Timestamps

Use ISO 8601 date-time strings with timezone offsets.

Example:

```text
2026-06-30T10:15:00+08:00
```

### Status Values

Slice 1 status values:

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

The implementation may seed later states such as `DELAYED`, `ON_HOLD`, `RETURNED`, or `FAILED_DELIVERY`, but Slice 1 tests should focus on the common operational path.

## 7. Shared Error Format

Use an RFC 9457-style problem response.

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

Common error codes:

| HTTP Status | Error Code | Meaning |
|---|---|---|
| `400` | `INVALID_REQUEST` | Request syntax or parameter format is invalid. |
| `403` | `ORDER_NOT_ASSIGNED_TO_DRIVER` | Driver is not allowed to update this order. |
| `404` | `ORDER_NOT_FOUND` | Order ID does not exist. |
| `404` | `DRIVER_NOT_FOUND` | Driver ID does not exist. |
| `404` | `ASSIGNMENT_NOT_FOUND` | No assignment exists for the requested driver/order relationship. |
| `409` | `INVALID_STATUS_TRANSITION` | Status transition is not allowed. |
| `422` | `INVALID_STATUS_EVENT` | Request is syntactically valid but semantically invalid. |
| `500` | `INTERNAL_SERVER_ERROR` | Unexpected server failure. |

Validation taxonomy:

| Category | HTTP Status | Error Code | Examples |
|---|---:|---|---|
| Invalid request shape | `400` | `INVALID_REQUEST` | malformed JSON, unknown field, missing required field, invalid ID format, invalid query parameter, invalid enum value, invalid date-time format |
| Invalid lifecycle move | `409` | `INVALID_STATUS_TRANSITION` | `DELIVERED -> OUT_FOR_DELIVERY`, `CANCELLED -> IN_TRANSIT` |
| Invalid status-event meaning | `422` | `INVALID_STATUS_EVENT` | syntactically valid event whose business meaning is unacceptable, such as an `occurredAt` far in the future |

## 8. Endpoint: Get Order Status

```http
GET /api/v1/orders/{orderId}/status
```

### Purpose

Return the current operational status for one order.

### Actor

Customer Service Agent through the BFF.

### Resource

`orders`

### Request

Path parameters:

| Name | Type | Required | Rule |
|---|---|---|---|
| `orderId` | string | yes | Must match a seeded or stored order ID, such as `ORD-1001`. |

### Success Response

Status:

```http
200 OK
```

Body:

```json
{
  "orderId": "ORD-1001",
  "currentStatus": "OUT_FOR_DELIVERY",
  "statusLabel": "Out for delivery",
  "currentLocation": {
    "label": "Tampines Delivery Hub",
    "latitude": 1.3521,
    "longitude": 103.9448,
    "capturedAt": "2026-06-30T10:15:00+08:00"
  },
  "estimatedDeliveryAt": "2026-06-30T18:00:00+08:00",
  "deliveryWindow": {
    "start": "2026-06-30T14:00:00+08:00",
    "end": "2026-06-30T18:00:00+08:00"
  },
  "assignedDriver": {
    "driverId": "DRV-2001",
    "displayName": "A. Kumar"
  },
  "lastUpdatedAt": "2026-06-30T10:15:00+08:00"
}
```

### Error Responses

| Status | Error Code | Case |
|---|---|---|
| `400` | `INVALID_REQUEST` | `orderId` is blank or malformed. |
| `404` | `ORDER_NOT_FOUND` | No order exists for the provided `orderId`. |

### Validation Rules

- `orderId` must not be blank.
- The API must not leak internal-only operational notes.
- The response should be safe for the BFF to transform into a customer answer.

### Test Cases

| Case | Expected Result |
|---|---|
| Existing order `ORD-1001` | Returns `200` with current status. |
| Missing order `ORD-9999` | Returns `404 ORDER_NOT_FOUND`. |
| Blank order ID | Returns `400 INVALID_REQUEST`. |
| Status updated by driver first | Returns the newly updated status. |

## 9. Endpoint: Get Order Timeline

```http
GET /api/v1/orders/{orderId}/timeline
```

### Purpose

Return the chronological status-event history for one order.

### Actor

Customer Service Agent through the BFF.

### Resource

`status-events`

### Request

Path parameters:

| Name | Type | Required | Rule |
|---|---|---|---|
| `orderId` | string | yes | Must match a seeded or stored order ID. |

Optional query parameters:

| Name | Type | Required | Rule |
|---|---|---|---|
| `page` | integer | no | Default `1`; must be greater than or equal to `1`. |
| `pageSize` | integer | no | Default `20`; maximum `100`. |

### Success Response

Status:

```http
200 OK
```

Body:

```json
{
  "orderId": "ORD-1001",
  "items": [
    {
      "eventId": "EVT-4001",
      "status": "CREATED",
      "statusLabel": "Created",
      "occurredAt": "2026-06-30T08:00:00+08:00",
      "actorType": "SYSTEM",
      "actorId": "SYSTEM",
      "location": null,
      "note": "Order created"
    },
    {
      "eventId": "EVT-4002",
      "status": "OUT_FOR_DELIVERY",
      "statusLabel": "Out for delivery",
      "occurredAt": "2026-06-30T10:15:00+08:00",
      "actorType": "DRIVER",
      "actorId": "DRV-2001",
      "location": {
        "label": "Tampines Delivery Hub",
        "latitude": 1.3521,
        "longitude": 103.9448,
        "capturedAt": "2026-06-30T10:15:00+08:00"
      },
      "note": "Loaded onto delivery vehicle"
    }
  ],
  "page": 1,
  "pageSize": 20,
  "totalItems": 2
}
```

### Error Responses

| Status | Error Code | Case |
|---|---|---|
| `400` | `INVALID_REQUEST` | Invalid `page` or `pageSize`. |
| `404` | `ORDER_NOT_FOUND` | No order exists for the provided `orderId`. |

### Validation Rules

- Timeline events must be sorted by `occurredAt` ascending.
- Events must belong to the requested order.
- Pagination values must be bounded.

### Test Cases

| Case | Expected Result |
|---|---|
| Existing order with seeded events | Returns `200` with timeline items. |
| Existing order after status update | Timeline includes newly created event. |
| Missing order | Returns `404 ORDER_NOT_FOUND`. |
| Invalid pagination | Returns `400 INVALID_REQUEST`. |

## 10. Endpoint: Get Driver

```http
GET /api/v1/drivers/{driverId}
```

### Purpose

Return a seeded driver profile for the driver frontend demo flow.

### Actor

Delivery Agent through the BFF.

### Resource

`drivers`

### Request

Path parameters:

| Name | Type | Required | Rule |
|---|---|---|---|
| `driverId` | string | yes | Must match a seeded or stored driver ID, such as `DRV-2001`. |

### Success Response

Status:

```http
200 OK
```

Body:

```json
{
  "driverId": "DRV-2001",
  "displayName": "A. Kumar",
  "availabilityStatus": "AVAILABLE",
  "activeAssignmentCount": 2
}
```

### Error Responses

| Status | Error Code | Case |
|---|---|---|
| `400` | `INVALID_REQUEST` | `driverId` is blank or malformed. |
| `404` | `DRIVER_NOT_FOUND` | No driver exists for the provided `driverId`. |

### Validation Rules

- `driverId` must not be blank.
- Do not model real authentication in Slice 1.
- Keep the response small and demo-safe.

### Test Cases

| Case | Expected Result |
|---|---|
| Existing driver `DRV-2001` | Returns `200` with driver profile. |
| Missing driver `DRV-9999` | Returns `404 DRIVER_NOT_FOUND`. |
| Blank driver ID | Returns `400 INVALID_REQUEST`. |

## 11. Endpoint: List Driver Assignments

```http
GET /api/v1/drivers/{driverId}/assignments
```

### Purpose

Return the orders assigned to one driver.

This endpoint supports the driver frontend work list.

### Actor

Delivery Agent through the BFF.

### Resource

`assignments`

### Request

Path parameters:

| Name | Type | Required | Rule |
|---|---|---|---|
| `driverId` | string | yes | Must match a seeded or stored driver ID. |

Optional query parameters:

| Name | Type | Required | Rule |
|---|---|---|---|
| `status` | string | no | Optional order status filter. |
| `page` | integer | no | Default `1`; must be greater than or equal to `1`. |
| `pageSize` | integer | no | Default `20`; maximum `100`. |

### Success Response

Status:

```http
200 OK
```

Body:

```json
{
  "driverId": "DRV-2001",
  "items": [
    {
      "assignmentId": "ASN-3001",
      "orderId": "ORD-1001",
      "assignmentStatus": "ASSIGNED",
      "currentStatus": "OUT_FOR_DELIVERY",
      "recipientName": "Jamie Tan",
      "deliveryAddressSummary": "Tampines, Singapore",
      "deliveryWindow": {
        "start": "2026-06-30T14:00:00+08:00",
        "end": "2026-06-30T18:00:00+08:00"
      },
      "lastUpdatedAt": "2026-06-30T10:15:00+08:00"
    },
    {
      "assignmentId": "ASN-3002",
      "orderId": "ORD-1002",
      "assignmentStatus": "ASSIGNED",
      "currentStatus": "IN_TRANSIT",
      "recipientName": "Priya Nair",
      "deliveryAddressSummary": "Jurong East, Singapore",
      "deliveryWindow": {
        "start": "2026-07-01T09:00:00+08:00",
        "end": "2026-07-01T12:00:00+08:00"
      },
      "lastUpdatedAt": "2026-06-30T11:00:00+08:00"
    }
  ],
  "page": 1,
  "pageSize": 20,
  "totalItems": 2
}
```

### Error Responses

| Status | Error Code | Case |
|---|---|---|
| `400` | `INVALID_REQUEST` | Invalid query parameter. |
| `404` | `DRIVER_NOT_FOUND` | No driver exists for the provided `driverId`. |

### Validation Rules

- Driver must exist before assignments are listed.
- Pagination values must be bounded.
- Optional `status` filter must match a known `OrderStatus`.
- Assignment response can include lightweight order details to avoid a separate `delivery-view` endpoint in Slice 1.

### Test Cases

| Case | Expected Result |
|---|---|
| Existing driver with assignments | Returns `200` with assignment items. |
| Existing driver with no assignments | Returns `200` with empty `items`. |
| Missing driver | Returns `404 DRIVER_NOT_FOUND`. |
| Invalid status filter | Returns `400 INVALID_REQUEST`. |

## 12. Endpoint: Create Order Status Event

```http
POST /api/v1/orders/{orderId}/status-events
```

### Purpose

Create a new status event for an order.

This is the main delivery-agent write endpoint for Slice 1.

The endpoint should:

1. Validate the order exists.
2. Validate the driver exists.
3. Validate the driver is assigned to the order.
4. Validate the requested status transition is allowed.
5. Create a status event.
6. Update the order current status.
7. Return the created event and updated current status.

### Actor

Delivery Agent through the BFF.

### Resource

`status-events`

### Request

Path parameters:

| Name | Type | Required | Rule |
|---|---|---|---|
| `orderId` | string | yes | Must match a seeded or stored order ID. |

Request body:

```json
{
  "driverId": "DRV-2001",
  "status": "DELIVERED",
  "occurredAt": "2026-06-30T15:45:00+08:00",
  "location": {
    "label": "Customer address",
    "latitude": 1.3521,
    "longitude": 103.9448,
    "capturedAt": "2026-06-30T15:45:00+08:00"
  },
  "note": "Left with reception",
  "proofOfDeliveryAvailable": true
}
```

Required request fields:

| Field | Type | Required | Rule |
|---|---|---|---|
| `driverId` | string | yes | Must match an existing driver assigned to the order. |
| `status` | string | yes | Must be a valid `OrderStatus`. |
| `occurredAt` | string | no | ISO 8601 date-time; server can default to current time if omitted. |
| `location` | object | no | Optional location snapshot. |
| `note` | string | no | Optional short operational note. |
| `proofOfDeliveryAvailable` | boolean | no | Relevant when status is `DELIVERED`. |

### Success Response

Status:

```http
201 Created
```

Body:

```json
{
  "eventId": "EVT-4006",
  "orderId": "ORD-1001",
  "previousStatus": "OUT_FOR_DELIVERY",
  "newStatus": "DELIVERED",
  "statusLabel": "Delivered",
  "occurredAt": "2026-06-30T15:45:00+08:00",
  "actorType": "DRIVER",
  "actorId": "DRV-2001",
  "location": {
    "label": "Customer address",
    "latitude": 1.3521,
    "longitude": 103.9448,
    "capturedAt": "2026-06-30T15:45:00+08:00"
  },
  "note": "Left with reception",
  "proofOfDeliveryAvailable": true,
  "orderCurrentStatus": "DELIVERED"
}
```

### Error Responses

| Status | Error Code | Case |
|---|---|---|
| `400` | `INVALID_REQUEST` | Request body shape is invalid: malformed JSON, unknown field, missing required field, invalid enum value, or invalid date-time format. |
| `403` | `ORDER_NOT_ASSIGNED_TO_DRIVER` | Driver exists but is not assigned to this order. |
| `404` | `ORDER_NOT_FOUND` | No order exists for the provided `orderId`. |
| `404` | `DRIVER_NOT_FOUND` | No driver exists for the provided `driverId`. |
| `409` | `INVALID_STATUS_TRANSITION` | Requested transition is not allowed. |
| `422` | `INVALID_STATUS_EVENT` | Request body shape is valid, but the status event meaning is invalid. |

### Validation Rules

- `orderId` must exist.
- `driverId` must exist.
- Driver must be assigned to the order.
- `status` must be known; unknown enum values return `400 INVALID_REQUEST`.
- Status transition must be allowed.
- `occurredAt` must be a valid date-time; invalid date-time format returns `400 INVALID_REQUEST`.
- `occurredAt` must not be far in the future; valid date-time with unacceptable business timing returns `422 INVALID_STATUS_EVENT`.
- `note` should have a maximum length, such as `500` characters.
- If `status` is `DELIVERED`, `proofOfDeliveryAvailable` may be included.
- Creating a status event must update the order's current status.
- Creating a status event must make the event visible in the timeline endpoint.

### Initial Transition Rules

| Current Status | Allowed New Status |
|---|---|
| `CREATED` | `CONFIRMED`, `CANCELLED` |
| `CONFIRMED` | `PICKED_UP`, `CANCELLED` |
| `PICKED_UP` | `IN_TRANSIT` |
| `IN_TRANSIT` | `OUT_FOR_DELIVERY` |
| `OUT_FOR_DELIVERY` | `DELIVERED` |
| `DELIVERY_ATTEMPTED` | none in Slice 1 |
| `DELIVERED` | none |
| `CANCELLED` | none |

### Test Cases

| Case | Expected Result |
|---|---|
| Assigned driver creates valid status event | Returns `201` with created event. |
| Timeline requested after event creation | Timeline includes new event. |
| Order status requested after event creation | Current status reflects new status. |
| Missing order | Returns `404 ORDER_NOT_FOUND`. |
| Missing driver | Returns `404 DRIVER_NOT_FOUND`. |
| Driver not assigned to order | Returns `403 ORDER_NOT_ASSIGNED_TO_DRIVER`. |
| Invalid status value | Returns `400 INVALID_REQUEST`. |
| Semantically invalid status event | Returns `422 INVALID_STATUS_EVENT`. |
| Invalid transition | Returns `409 INVALID_STATUS_TRANSITION`. |

## 13. Endpoint: Health Check

```http
GET /health
```

### Purpose

Confirm the service process is alive.

### Actor

System.

### Resource

`health`

### Success Response

Status:

```http
200 OK
```

Body:

```json
{
  "status": "UP",
  "service": "partner-source"
}
```

### Test Cases

| Case | Expected Result |
|---|---|
| Service is running | Returns `200` with `status` set to `UP`. |

## 14. Endpoint: Readiness Check

```http
GET /ready
```

### Purpose

Confirm the service is ready to handle API requests.

In Slice 1, readiness checks application startup, in-memory persistence availability, and deterministic seed-data loading.

### Actor

System.

### Resource

`ready`

### Success Response

Status:

```http
200 OK
```

Body:

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

### Error Response

Status:

```http
503 Service Unavailable
```

Body:

```json
{
  "status": "NOT_READY",
  "service": "partner-source",
  "checks": {
    "persistence": "DOWN",
    "seedData": "DOWN"
  }
}
```

### Test Cases

| Case | Expected Result |
|---|---|
| Service, in-memory persistence, and seed data are ready | Returns `200 READY`. |
| In-memory persistence or seed data is unavailable | Returns `503 NOT_READY`. |

## 15. Slice 1 Acceptance Criteria

Slice 1 is complete when:

- Customer service can retrieve current order status.
- Customer service can retrieve order timeline.
- Delivery agent can retrieve driver profile.
- Delivery agent can retrieve assigned orders.
- Delivery agent can create a valid status event.
- Invalid status transitions are rejected.
- A created status event appears in the order timeline.
- A created status event updates current order status.
- Health and readiness endpoints work.

## 16. OpenAPI Implications

The first OpenAPI YAML should include only this Slice 1 contract.

Recommended file:

```text
docs/contracts/openapi/partner-source.v1.yaml
```

Required OpenAPI components:

- `OrderStatusResponse`
- `OrderTimelineResponse`
- `StatusEventResponse`
- `CreateStatusEventRequest`
- `DriverResponse`
- `DriverAssignmentsResponse`
- `DriverAssignmentItem`
- `DeliveryWindow`
- `LocationSnapshot`
- `AssignedDriverSummary`
- `ProblemDetail`
- shared path parameters for `orderId` and `driverId`

## 17. Review Questions

1. Should assignments include enough delivery detail for the driver frontend, or do we still need a separate `delivery-view` endpoint later?
2. Should `occurredAt` be supplied by the driver frontend, or should the server always set it?
3. Resolved by the Slice 1 design freeze: `DELIVERY_ATTEMPTED` remains an enum value, but creating new delivery-attempt behavior waits until the `delivery-attempts` slice.

## 18. Resolved Decisions

| Question | Decision |
|---|---|
| What should readiness check for Slice 1? | Resolved by ADR-0007. Slice 1 readiness checks in-memory persistence and seed-data availability. |
