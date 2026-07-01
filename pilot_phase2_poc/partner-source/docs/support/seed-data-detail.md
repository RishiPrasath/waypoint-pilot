# Partner Source Data Model And Seed Data

## 1. Purpose

This document defines the planned Slice 1 seed data for `partner-source`.

The seed data is not filler. It is part of the API design because the project does not connect to a real logistics company's internal systems. Synthetic records must therefore prove the business flow, API fields, validation rules, and test scenarios.

The seed data should align with:

- [domain-model-detail.md](domain-model-detail.md)
- [api-contract-detail.md](api-contract-detail.md)
- [test-plan-detail.md](test-plan-detail.md)
- [../research/use-case-resource-map.md](../research/use-case-resource-map.md)
- [../archive/audits/api-design-verification-report.md](../archive/audits/api-design-verification-report.md)
- [../contracts/openapi/partner-source.v1.yaml](../contracts/openapi/partner-source.v1.yaml)

## 2. Seed Data Design Rule

Every seeded record must exist for a reason.

Use this rule:

```text
seed record
-> scenario it proves
-> endpoint it supports
-> validation rule it exercises
-> test case it enables
```

If a record does not support a scenario, endpoint, rule, or test, it should not be in the first seed set.

## 3. Persistence Choice

Start with in-memory repositories for the first slice.

Move to H2 or PostgreSQL only after these are stable:

- OpenAPI contract
- domain model
- seed scenario matrix
- request/response tests
- validation behavior

Reason:

The first goal is to prove the contract and operational flow. A database is useful, but it should not slow down the first design and contract validation loop.

## 4. Operational Flow To Prove

The seed data must prove this realistic driver flow:

```text
driver is available
-> driver receives an assignment
-> driver collects or picks up the goods
-> driver moves the order through delivery statuses
-> driver delivers successfully or reports an attempted delivery
-> customer service reads current status and timeline
```

For Slice 1, the core happy path is:

```text
AVAILABLE driver
-> ASSIGNED order
-> PICKED_UP / IN_TRANSIT / OUT_FOR_DELIVERY
-> DELIVERED
-> timeline is visible to customer service
```

For Slice 2, failed delivery becomes:

```text
OUT_FOR_DELIVERY
-> DELIVERY_ATTEMPTED
-> reason: recipient unavailable or address inaccessible
-> optional next attempt time
-> support summary explains what happens next
```

## 5. Driver Lifecycle Assumptions

The current API does not need to implement real workforce management.

For the prototype:

- drivers are seeded
- driver availability is seeded
- login is simulated by looking up a seeded driver
- assignments are seeded
- only assigned drivers can update assigned orders
- availability is read-only in Slice 1

### Driver Availability Meaning

| Availability | Meaning In Prototype | Can Receive Active Assignments? |
|---|---|---|
| `AVAILABLE` | Driver is active for the demo and can work assigned jobs. | Yes |
| `UNAVAILABLE` | Driver exists but is not taking delivery work. | No for new active work |
| `OFFLINE` | Driver is not active in the driver frontend. | No |

### Gap To Note

If the driver frontend needs a real "go active" or "go offline" action, the API will eventually need a driver availability update endpoint.

That is not required for Slice 1. Seeded availability is enough for the first week.

## 6. Slice 1 Seed Scenario Matrix

| Scenario ID | Scenario | Why It Exists | Main Endpoint |
|---|---|---|---|
| `S1-HAPPY-DELIVERY` | Active driver has an out-for-delivery order and marks it delivered. | Proves the core delivery-agent update loop. | `POST /api/v1/orders/{orderId}/status-events` |
| `S1-ASSIGNMENTS` | Active driver retrieves assigned orders. | Proves driver work-list display. | `GET /api/v1/drivers/{driverId}/assignments` |
| `S1-TIMELINE` | Customer service views the order timeline. | Proves status events are readable. | `GET /api/v1/orders/{orderId}/timeline` |
| `S1-STATUS` | Customer service asks where the order is. | Proves WISMO status response. | `GET /api/v1/orders/{orderId}/status` |
| `S1-NO-ASSIGNMENTS` | Available driver has no active assignments. | Proves empty work-list behavior. | `GET /api/v1/drivers/{driverId}/assignments` |
| `S1-UNASSIGNED-UPDATE` | Valid driver tries to update an order not assigned to them. | Proves `ORDER_NOT_ASSIGNED_TO_DRIVER`. | `POST /api/v1/orders/{orderId}/status-events` |
| `S1-INVALID-TRANSITION` | Delivered order is moved back to out-for-delivery. | Proves `INVALID_STATUS_TRANSITION`. | `POST /api/v1/orders/{orderId}/status-events` |
| `S1-MISSING-ORDER` | Unknown order is requested. | Proves `ORDER_NOT_FOUND`. | `GET /api/v1/orders/{orderId}/status` |
| `S1-MISSING-DRIVER` | Unknown driver is requested. | Proves `DRIVER_NOT_FOUND`. | `GET /api/v1/drivers/{driverId}` |

## 7. Driver Seed Records

| Driver ID | Display Name | Availability | Active Assignment Count | Scenario Purpose |
|---|---|---|---|---|
| `DRV-2001` | A. Kumar | `AVAILABLE` | `2` | Main active driver for happy path and assignment list. |
| `DRV-2002` | Maya Lee | `UNAVAILABLE` | `0` | Valid driver who should not have active demo work. Used for unassigned update tests. |
| `DRV-2003` | Ben Tan | `AVAILABLE` | `0` | Available driver with no current assignments. Proves empty assignment response. |
| `DRV-9999` | Not seeded | Not applicable | Not applicable | Missing-driver negative test. |

### Driver Design Notes

`DRV-2001` is the main demo identity for the delivery-agent frontend.

`DRV-2002` should exist because we need to distinguish:

- driver does not exist
- driver exists but is not assigned to this order
- driver exists but is unavailable

`DRV-2003` prevents the assignment endpoint from assuming every driver has work.

## 8. Order Seed Records

Use fixed timestamps so tests remain deterministic.

| Order ID | Recipient | Address Summary | Current Status | ETA | Delivery Window | Assigned Driver | Scenario Purpose |
|---|---|---|---|---|---|---|---|
| `ORD-1001` | Jamie Tan | Tampines, Singapore | `OUT_FOR_DELIVERY` | `2026-06-30T18:00:00+08:00` | `2026-06-30T14:00:00+08:00` to `2026-06-30T18:00:00+08:00` | `DRV-2001` | Main happy-path delivery order. |
| `ORD-1002` | Priya Nair | Jurong East, Singapore | `IN_TRANSIT` | `2026-07-01T12:00:00+08:00` | `2026-07-01T09:00:00+08:00` to `2026-07-01T12:00:00+08:00` | `DRV-2001` | Second active assignment and in-transit lifecycle example. |
| `ORD-1003` | Daniel Wong | Bedok, Singapore | `DELIVERED` | `null` | `2026-06-29T10:00:00+08:00` to `2026-06-29T14:00:00+08:00` | `DRV-2001` | Completed order used for invalid transition tests. |
| `ORD-1004` | Sofia Lim | Woodlands, Singapore | `OUT_FOR_DELIVERY` | `2026-06-30T20:00:00+08:00` | `2026-06-30T16:00:00+08:00` to `2026-06-30T20:00:00+08:00` | `DRV-2001` | Reserved for Slice 2 failed-attempt scenario. |
| `ORD-9999` | Not seeded | Not seeded | Not seeded | Not seeded | Not seeded | Not seeded | Missing-order negative test. |

### Order Design Notes

`ORD-1004` is included as a planned seed scenario but should not force Slice 1 to implement `delivery-attempts`.

If we want to keep Slice 1 even smaller, `ORD-1004` can remain documented only and be seeded in Slice 2.

## 9. Assignment Seed Records

| Assignment ID | Driver ID | Order ID | Assignment Status | Last Updated At | Scenario Purpose |
|---|---|---|---|---|---|
| `ASN-3001` | `DRV-2001` | `ORD-1001` | `ASSIGNED` | `2026-06-30T10:15:00+08:00` | Main active delivery job. |
| `ASN-3002` | `DRV-2001` | `ORD-1002` | `ASSIGNED` | `2026-06-30T11:00:00+08:00` | Second active job for assignment list. |
| `ASN-3003` | `DRV-2001` | `ORD-1003` | `COMPLETED` | `2026-06-29T13:45:00+08:00` | Completed assignment for delivered-order history. |
| `ASN-3004` | `DRV-2001` | `ORD-1004` | `ASSIGNED` | `2026-06-30T12:30:00+08:00` | Planned failed-attempt scenario for Slice 2. |

### Assignment Design Notes

The assignment list endpoint should normally return active work first.

For Slice 1, the driver assignment response for `DRV-2001` can include:

- `ASN-3001`
- `ASN-3002`

Whether completed assignment `ASN-3003` appears should depend on query filtering. If no filtering is implemented, keep the response simple and include only active assignments.

## 10. Status Event Seed Records

### `ORD-1001` Timeline

| Event ID | Status | Actor Type | Actor ID | Occurred At | Location Label | Note |
|---|---|---|---|---|---|---|
| `EVT-4001` | `CREATED` | `SYSTEM` | `SYSTEM` | `2026-06-30T08:00:00+08:00` | `null` | Order created. |
| `EVT-4002` | `CONFIRMED` | `SYSTEM` | `SYSTEM` | `2026-06-30T08:10:00+08:00` | `null` | Order confirmed by partner source. |
| `EVT-4003` | `PICKED_UP` | `DRIVER` | `DRV-2001` | `2026-06-30T09:30:00+08:00` | Tampines Collection Point | Goods collected by driver. |
| `EVT-4004` | `IN_TRANSIT` | `DRIVER` | `DRV-2001` | `2026-06-30T09:50:00+08:00` | Tampines Delivery Hub | Package in transit. |
| `EVT-4005` | `OUT_FOR_DELIVERY` | `DRIVER` | `DRV-2001` | `2026-06-30T10:15:00+08:00` | Tampines Delivery Hub | Loaded onto delivery vehicle. |

Expected current status before happy-path update:

```text
ORD-1001.currentStatus = OUT_FOR_DELIVERY
```

Expected valid update:

```text
POST /api/v1/orders/ORD-1001/status-events
driverId: DRV-2001
status: DELIVERED
```

Expected new event:

| Event ID | Status | Actor Type | Actor ID | Occurred At | Location Label | Note |
|---|---|---|---|---|---|---|
| generated | `DELIVERED` | `DRIVER` | `DRV-2001` | request or server timestamp | Customer address | Left with reception. |

### `ORD-1002` Timeline

| Event ID | Status | Actor Type | Actor ID | Occurred At | Location Label | Note |
|---|---|---|---|---|---|---|
| `EVT-4101` | `CREATED` | `SYSTEM` | `SYSTEM` | `2026-06-30T09:00:00+08:00` | `null` | Order created. |
| `EVT-4102` | `CONFIRMED` | `SYSTEM` | `SYSTEM` | `2026-06-30T09:15:00+08:00` | `null` | Order confirmed. |
| `EVT-4103` | `PICKED_UP` | `DRIVER` | `DRV-2001` | `2026-06-30T10:30:00+08:00` | Jurong Collection Point | Goods collected. |
| `EVT-4104` | `IN_TRANSIT` | `DRIVER` | `DRV-2001` | `2026-06-30T11:00:00+08:00` | West Hub | Package in transit. |

Expected current status:

```text
ORD-1002.currentStatus = IN_TRANSIT
```

### `ORD-1003` Timeline

| Event ID | Status | Actor Type | Actor ID | Occurred At | Location Label | Note |
|---|---|---|---|---|---|---|
| `EVT-4201` | `CREATED` | `SYSTEM` | `SYSTEM` | `2026-06-29T08:00:00+08:00` | `null` | Order created. |
| `EVT-4202` | `OUT_FOR_DELIVERY` | `DRIVER` | `DRV-2001` | `2026-06-29T10:30:00+08:00` | Bedok Delivery Hub | Loaded for delivery. |
| `EVT-4203` | `DELIVERED` | `DRIVER` | `DRV-2001` | `2026-06-29T13:45:00+08:00` | Customer address | Delivered to recipient. |

Expected invalid update:

```text
POST /api/v1/orders/ORD-1003/status-events
driverId: DRV-2001
status: OUT_FOR_DELIVERY
```

Expected result:

```text
409 INVALID_STATUS_TRANSITION
```

## 11. Location Seed Records

Locations should remain simple in Slice 1.

| Label | Latitude | Longitude | Purpose |
|---|---:|---:|---|
| Tampines Collection Point | `1.3521` | `103.9448` | Pickup and east-region demo location. |
| Tampines Delivery Hub | `1.3521` | `103.9448` | Current location for `ORD-1001`. |
| Jurong Collection Point | `1.3329` | `103.7436` | Pickup location for `ORD-1002`. |
| West Hub | `1.3349` | `103.7465` | Current location for `ORD-1002`. |
| Bedok Delivery Hub | `1.3236` | `103.9273` | Completed-order history. |
| Customer address | synthetic | synthetic | Used for delivered event response. |

The exact coordinates are not the core feature. They only support realistic response shapes.

## 12. Slice 2 Failed Delivery Seed Plan

Failed delivery is realistic, but it should not overload Slice 1.

Use `ORD-1004` for this later scenario:

```text
driver reaches address
-> address inaccessible or recipient unavailable
-> driver records delivery attempt
-> order status becomes DELIVERY_ATTEMPTED
-> support summary can explain next step
```

### Planned Delivery Attempt Record

| Field | Planned Value |
|---|---|
| `attemptId` | `ATT-5001` |
| `orderId` | `ORD-1004` |
| `driverId` | `DRV-2001` |
| `reasonCode` | `RECIPIENT_UNAVAILABLE` or `ADDRESS_INACCESSIBLE` |
| `attemptedAt` | `2026-06-30T18:30:00+08:00` |
| `note` | Recipient was unavailable at delivery location. |
| `nextAttemptAt` | `2026-07-01T10:00:00+08:00` |

### API Gap For Slice 2

To fully support this scenario, the design will need:

- `DeliveryAttempt` domain object
- `CreateDeliveryAttemptRequest`
- `DeliveryAttemptResponse`
- `DeliveryAttemptReasonCode`
- `POST /api/v1/orders/{orderId}/delivery-attempts`
- support-summary fields for latest attempt and next action

This is not required for the first implementation slice unless failed delivery is moved into week-one scope.

## 13. API And Domain Gaps Identified

| Gap | Current Status | Recommendation |
|---|---|---|
| Driver can go active/offline | Not supported by API. Availability is seeded only. | Keep seeded for Slice 1. Add update endpoint later only if driver frontend requires it. |
| Failed attempt reason | Not supported in Slice 1 except `DELIVERY_ATTEMPTED` status. | Add `DeliveryAttempt` in Slice 2. |
| Recipient unavailable/address inaccessible | Not fully represented in current OpenAPI. | Represent through Slice 2 delivery-attempt reason codes. |
| Full delivery address | Only `deliveryAddressSummary` exists. | Keep summary for Slice 1. Add richer `delivery-view` later if needed. |
| Proof of delivery visibility | Can be returned from status-event response, but not clearly in `GET /status`. | Decide before implementing delivered-but-not-found support. |
| Assignment creation | Not part of Slice 1 public API. | Keep assignments seeded or admin-only for now. |

## 14. Seed To Endpoint Coverage

| Endpoint | Seed Data Needed | Covered By |
|---|---|---|
| `GET /api/v1/orders/{orderId}/status` | order, current status, ETA, delivery window, assigned driver, latest location | `ORD-1001`, `ORD-1002`, `ORD-1003` |
| `GET /api/v1/orders/{orderId}/timeline` | order and status events | `EVT-4001` to `EVT-4005`, `EVT-4101` to `EVT-4104`, `EVT-4201` to `EVT-4203` |
| `GET /api/v1/drivers/{driverId}` | driver profile | `DRV-2001`, `DRV-2002`, `DRV-2003` |
| `GET /api/v1/drivers/{driverId}/assignments` | driver, assignments, lightweight order fields | `DRV-2001`, `DRV-2003`, `ASN-3001`, `ASN-3002` |
| `POST /api/v1/orders/{orderId}/status-events` | order, driver, assignment, current status, transition rule | `ORD-1001`, `ORD-1003`, `DRV-2001`, `DRV-2002`, `ASN-3001` |

## 15. Seed To Test Coverage

| Test Case | Seed Data Used | Expected Result |
|---|---|---|
| Existing order returns current status | `ORD-1001` | `200`, `currentStatus = OUT_FOR_DELIVERY` |
| Missing order returns not found | `ORD-9999` | `404 ORDER_NOT_FOUND` |
| Existing driver returns profile | `DRV-2001` | `200`, `availabilityStatus = AVAILABLE` |
| Missing driver returns not found | `DRV-9999` | `404 DRIVER_NOT_FOUND` |
| Active driver sees assigned orders | `DRV-2001`, `ASN-3001`, `ASN-3002` | `200`, two active assignment items |
| Available driver with no work sees empty list | `DRV-2003` | `200`, empty `items` |
| Assigned driver marks order delivered | `ORD-1001`, `DRV-2001`, `ASN-3001` | `201`, `newStatus = DELIVERED` |
| Unassigned driver cannot update order | `ORD-1001`, `DRV-2002` | `403 ORDER_NOT_ASSIGNED_TO_DRIVER` |
| Delivered order cannot move backward | `ORD-1003`, `DRV-2001`, `ASN-3003` | `409 INVALID_STATUS_TRANSITION` |
| Timeline returns chronological events | `ORD-1001`, `EVT-4001` to `EVT-4005` | `200`, events ordered by `occurredAt` |

## 16. Recommended Slice Boundary

### Keep In Slice 1

- seeded drivers
- seeded driver availability
- seeded assignments
- status timeline
- current status lookup
- assignment lookup
- status-event creation
- assignment authorization check
- status transition check

### Move To Slice 2

- delivery attempts
- failed attempt reason codes
- recipient unavailable support answer
- address inaccessible support answer
- support summary
- richer driver delivery view
- driver availability update endpoint

## 17. Final Recommendation

Use this seed plan to make the prototype feel operational without pretending to be a full logistics system.

The seed data should first prove:

```text
available driver
-> active assignments
-> status lifecycle
-> successful delivery
-> support-visible timeline
```

Then the second slice can prove:

```text
delivery attempted
-> failed attempt reason
-> support summary
-> next practical customer answer
```

This keeps the first implementation realistic, testable, and small enough for a solo developer to complete.
