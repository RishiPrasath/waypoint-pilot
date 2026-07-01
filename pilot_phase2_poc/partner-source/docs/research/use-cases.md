# Partner Source Use Cases

## 1. Scope

`partner-source` is a mock logistics-company data source.

Current Slice 1 status:

```text
This document includes broader product/use-case research.
The frozen Slice 1 implementation scope is smaller and is defined in 15-slice-1-design-freeze.md.
Use cases marked "should build", "later", or involving delivery attempts, exceptions, support summary, delivery view, customer actions, delays, holds, returns, or failed delivery are Slice 2/later unless the design freeze is deliberately reopened.
```

It should expose realistic operational facts for Waypoint, but it should not pretend to be a full carrier platform. The project does not have access to real logistics internal systems, live GPS feeds, claims teams, route optimization engines, warehouse operations, or customer identity data.

The practical scope is:

- seeded synthetic orders
- seeded synthetic drivers
- seeded driver-order assignments
- order status events
- delivery attempts
- simple exception reasons
- ETA and delivery window fields
- customer-safe support summaries

The API should be useful enough for the BFF, chatbot, support-agent view, and driver frontend to demonstrate the full loop:

```text
delivery agent updates order -> partner-source stores operational fact -> customer service agent/chatbot reads updated fact
```

## 2. Actors

| Actor | Main Intent | Access Pattern | MVP Role |
|---|---|---|---|
| Customer Service Agent | Answer customer questions about deliveries. | Mostly read-only. | Looks up order status, timeline, delays, delivery attempts, and support summary. |
| Delivery Agent | Report what happened during delivery. | Read assigned work, then write status updates. | Retrieves assigned orders and updates order status. |

## 3. Boundary Rules

`partner-source` should own:

- order records
- driver records
- assignments
- status events
- delivery attempts
- exception flags
- ETA/delivery windows
- delivery notes
- synthetic support facts

`partner-source` should not own:

- chatbot wording
- customer-facing final answer tone
- RAG responses
- BFF response shaping
- frontend rendering
- real authentication beyond demo identity checks
- real route planning
- real GPS telemetry
- real claims processing
- payment or customs workflow execution

The BFF is responsible for shaping these facts for the chatbot, support-agent view, or driver frontend.

## 4. Customer Service Agent Use Cases

The customer service agent handles customer questions. In the MVP, this actor should not update operational status. They only read facts that were seeded or reported by a delivery agent.

### CSA-01: Look Up Order By Order ID

Customer question:

- "Can you check my order?"
- "Where is order `ORD-1001`?"

API:

```http
GET /api/v1/orders/{orderId}/status
```

Result:

- confirms whether the order exists
- returns current order status
- returns latest update timestamp
- returns ETA if available

MVP priority: must build.

### CSA-02: View Current Order Status

Customer question:

- "Where is my order?"
- "Has it shipped?"
- "Is it out for delivery?"

API:

```http
GET /api/v1/orders/{orderId}/status
```

Synthetic example:

```text
ORD-1001
status: OUT_FOR_DELIVERY
latest event: Loaded onto delivery vehicle
eta: 2026-06-30T18:00:00+08:00
latest location: Tampines Delivery Hub
```

MVP priority: must build.

### CSA-03: View Order Timeline

Customer question:

- "What happened to my shipment?"
- "When was it picked up?"
- "Why has it been in transit for so long?"

API:

```http
GET /api/v1/orders/{orderId}/timeline
```

Synthetic example:

```text
CREATED -> CONFIRMED -> PICKED_UP -> IN_TRANSIT -> OUT_FOR_DELIVERY
```

MVP priority: must build.

### CSA-04: View ETA And Delivery Window

Customer question:

- "When will it arrive?"
- "Will it arrive today?"
- "What time should I expect delivery?"

API:

The status response should include:

```json
{
  "estimatedDeliveryAt": "2026-06-30T18:00:00+08:00",
  "deliveryWindow": {
    "start": "2026-06-30T14:00:00+08:00",
    "end": "2026-06-30T18:00:00+08:00"
  }
}
```

MVP priority: must build.

### CSA-05: View Delay Or Exception Reason

Customer question:

- "Why is my package delayed?"
- "What does delivery exception mean?"
- "When will it move again?"

API:

```http
GET /api/v1/orders/{orderId}/exceptions
```

Synthetic example:

```json
{
  "hasException": true,
  "exceptionCode": "WEATHER_DELAY",
  "exceptionLabel": "Weather delay",
  "recoveryEta": "2026-07-01T18:00:00+08:00"
}
```

MVP priority: should build after status and timeline.

### CSA-06: View Failed Delivery Attempt Details

Slice status: Slice 2/later.

Customer question:

- "I missed my delivery. What happens next?"
- "Will the driver try again?"
- "Can I pick it up somewhere?"

API:

```http
GET /api/v1/orders/{orderId}/support-summary
```

Synthetic example:

```json
{
  "currentStatus": "DELIVERY_ATTEMPTED",
  "deliveryAttempts": 1,
  "nextDeliveryAttemptAt": "2026-07-01T10:00:00+08:00",
  "failedAttemptReason": "RECIPIENT_UNAVAILABLE"
}
```

MVP priority: should build after Slice 1.

### CSA-07: View Delivered But Not Found Support Facts

Slice status: Slice 2/later.

Customer question:

- "It says delivered, but I cannot find it."
- "Where was it left?"
- "Who received it?"

API:

```http
GET /api/v1/orders/{orderId}/support-summary
```

Synthetic example:

```json
{
  "currentStatus": "DELIVERED",
  "deliveredAt": "2026-06-30T15:45:00+08:00",
  "deliveryNote": "Left with reception",
  "proofOfDeliveryAvailable": true
}
```

MVP priority: should build after Slice 1.

### CSA-08: View Available Customer Actions

Customer question:

- "Can I change the address?"
- "Can I reschedule?"
- "Can I leave delivery instructions?"

API:

```http
GET /api/v1/orders/{orderId}/available-actions
```

Synthetic example:

```json
{
  "allowedCustomerActions": [
    "ADD_DELIVERY_INSTRUCTIONS"
  ],
  "blockedCustomerActions": [
    {
      "action": "CHANGE_ADDRESS",
      "reason": "SHIPMENT_ALREADY_OUT_FOR_DELIVERY"
    }
  ]
}
```

MVP priority: later. This is useful, but it can remain read-only.

### CSA-09: Get Support Summary

Slice status: Slice 2/later.

Customer service agent need:

- one compact view of the order
- current status
- ETA
- timeline summary
- latest exception
- delivery attempt details
- safe next-action flags

API:

```http
GET /api/v1/orders/{orderId}/support-summary
```

MVP priority: must build once the underlying status, timeline, and exception fields exist.

## 5. Delivery Agent Use Cases

The delivery agent updates the operational truth. This is the write path that makes the synthetic system feel real.

### DA-01: Demo Login As Driver

Driver action:

- selects or logs in as a seeded driver

API:

```http
GET /api/v1/drivers/{driverId}
```

Practical MVP approach:

- use seeded driver IDs
- avoid full authentication for the first slice
- add simple demo identity validation later if needed

MVP priority: must build for driver frontend flow.

### DA-02: Retrieve Assigned Orders

Driver question:

- "What orders are assigned to me?"
- "What is my next delivery?"
- "Which orders can I update?"

API:

```http
GET /api/v1/drivers/{driverId}/assignments
```

Synthetic example:

```text
DRV-2001
assigned orders: ORD-1001, ORD-1003, ORD-1005
```

MVP priority: must build.

### DA-03: View Delivery Details

Driver need:

- order ID
- recipient display name
- delivery address
- delivery window
- current status
- notes/instructions

API:

```http
GET /api/v1/orders/{orderId}/delivery-view
```

MVP priority: should build, or include these fields in the assignment response.

### DA-04: Mark Order As Picked Up

Driver action:

- confirms the parcel has been picked up or loaded

API:

```http
POST /api/v1/orders/{orderId}/status-events
```

Request example:

```json
{
  "driverId": "DRV-2001",
  "status": "PICKED_UP",
  "note": "Package collected from warehouse"
}
```

MVP priority: must build if the demo starts before dispatch.

### DA-05: Mark Order As Out For Delivery

Driver action:

- confirms the parcel is on the delivery route

API:

```http
POST /api/v1/orders/{orderId}/status-events
```

Request example:

```json
{
  "driverId": "DRV-2001",
  "status": "OUT_FOR_DELIVERY",
  "note": "Loaded onto delivery vehicle"
}
```

MVP priority: must build.

### DA-06: Mark Order As Delivered

Driver action:

- completes delivery

API:

```http
POST /api/v1/orders/{orderId}/status-events
```

Request example:

```json
{
  "driverId": "DRV-2001",
  "status": "DELIVERED",
  "note": "Left with reception",
  "proofOfDeliveryAvailable": true
}
```

MVP priority: must build.

### DA-07: Report Failed Delivery Attempt

Slice status: Slice 2/later.

Driver action:

- reports that delivery could not be completed

API:

```http
POST /api/v1/orders/{orderId}/delivery-attempts
```

Request example:

```json
{
  "driverId": "DRV-2001",
  "attemptStatus": "FAILED",
  "reasonCode": "RECIPIENT_UNAVAILABLE",
  "note": "No answer at door"
}
```

MVP priority: should build after Slice 1.

### DA-08: Report Operational Exception

Driver action:

- reports an issue such as address problem, access issue, or damaged package

API:

```http
POST /api/v1/orders/{orderId}/exceptions
```

Request example:

```json
{
  "driverId": "DRV-2001",
  "exceptionCode": "ADDRESS_ISSUE",
  "note": "Unit number missing"
}
```

MVP priority: later. Useful, but not needed before basic status updates.

### DA-09: Add Delivery Note

Driver action:

- adds a short operational note to the order

API:

```http
POST /api/v1/orders/{orderId}/notes
```

MVP priority: later. Can be folded into status-event notes for the first version.

## 6. Shared Order Lifecycle

The MVP should support a simple lifecycle:

```text
CREATED
CONFIRMED
PICKED_UP
IN_TRANSIT
OUT_FOR_DELIVERY
DELIVERY_ATTEMPTED
DELIVERED
```

Additional support states:

```text
DELAYED
CUSTOMS_HOLD
ON_HOLD
FAILED_DELIVERY
RETURNED
CANCELLED
```

For a solo developer, implement transition validation only for the common path first.

The table below is product research for the broader MVP. It is not the canonical Slice 1 transition table. The canonical Slice 1 table is frozen in [../archive/slice-1-design-freeze.md](../archive/slice-1-design-freeze.md).

| From | Allowed To |
|---|---|
| `CREATED` | `CONFIRMED`, `CANCELLED` |
| `CONFIRMED` | `PICKED_UP`, `CANCELLED` |
| `PICKED_UP` | `IN_TRANSIT`, `DELAYED` |
| `IN_TRANSIT` | `OUT_FOR_DELIVERY`, `DELAYED`, `ON_HOLD` |
| `OUT_FOR_DELIVERY` | `DELIVERED`, `DELIVERY_ATTEMPTED`, `DELAYED` |
| `DELIVERY_ATTEMPTED` | `OUT_FOR_DELIVERY`, `FAILED_DELIVERY`, `RETURNED` |

## 7. Synthetic Data Scenarios

The database should include enough fake records to test realistic support questions.

| Order ID | Scenario | Status | Main Actor Tested |
|---|---|---|---|
| `ORD-1001` | Normal out-for-delivery order | `OUT_FOR_DELIVERY` | Customer Service Agent |
| `ORD-1002` | Tracking not updated | `IN_TRANSIT` | Customer Service Agent |
| `ORD-1003` | Delivered order for invalid transition test | `DELIVERED` | Delivery Agent |
| `ORD-1004` | Planned failed delivery attempt | `OUT_FOR_DELIVERY` | Both, Slice 2 |
| `ORD-1005` | Weather delay | `DELAYED` | Customer Service Agent |
| `ORD-1006` | Customs hold | `CUSTOMS_HOLD` | Customer Service Agent |
| `ORD-1007` | Damaged delivery reported | `DELIVERED` | Customer Service Agent |
| `ORD-1008` | Address issue | `ON_HOLD` | Both |
| `ORD-1009` | Cancelled before dispatch | `CANCELLED` | Customer Service Agent |
| `ORD-1010` | Returned to sender | `RETURNED` | Customer Service Agent |

Driver records:

| Driver ID | Scenario |
|---|---|
| `DRV-2001` | Active driver with normal assignments |
| `DRV-2002` | Driver with failed-delivery assignment |
| `DRV-2003` | Offline/unavailable driver |

## 8. Recommended MVP Build Order

Build in this order:

1. `CSA-01` and `CSA-02`: order lookup and current status.
2. `CSA-03`: order timeline.
3. `CSA-04`: ETA and delivery window fields.
4. `DA-01`: demo driver lookup.
5. `DA-02`: driver assigned orders.
6. `DA-05` and `DA-06`: driver status updates for out-for-delivery and delivered.
7. `DA-07`: failed delivery attempt.
8. `CSA-05` and `CSA-06`: exception and failed-attempt support view.
9. `CSA-09`: support summary.

This order proves the full feedback loop without building unnecessary logistics complexity.

## 9. Deferred Scope

Defer these until the core loop works:

- claims workflow
- real proof-of-delivery images
- live GPS tracking
- route optimization
- address change execution
- payments, duties, and customs payment workflow
- real carrier integration
- real customer authentication
- advanced driver scheduling

Represent these as flags, notes, or static synthetic scenarios if they are needed for demos.

## 10. API Summary

Customer service read APIs:

```http
GET /api/v1/orders/{orderId}/status
GET /api/v1/orders/{orderId}/timeline
GET /api/v1/orders/{orderId}/support-summary
GET /api/v1/orders/{orderId}/exceptions
GET /api/v1/orders/{orderId}/available-actions
```

Delivery agent read/write APIs:

```http
GET /api/v1/drivers/{driverId}
GET /api/v1/drivers/{driverId}/assignments
GET /api/v1/orders/{orderId}/delivery-view
POST /api/v1/orders/{orderId}/status-events
POST /api/v1/orders/{orderId}/delivery-attempts
POST /api/v1/orders/{orderId}/exceptions
POST /api/v1/orders/{orderId}/notes
```

For the first slice, the minimum set is:

```http
GET /api/v1/orders/{orderId}/status
GET /api/v1/orders/{orderId}/timeline
GET /api/v1/drivers/{driverId}
GET /api/v1/drivers/{driverId}/assignments
POST /api/v1/orders/{orderId}/status-events
```

## 11. Database Implications

The database should support:

| Table / Collection | Purpose |
|---|---|
| `orders` | Base order identity, current status, ETA, delivery window. |
| `drivers` | Seeded driver profiles and availability. |
| `assignments` | Order-driver relationship. |
| `status_events` | Timeline and operational history. |
| `delivery_attempts` | Failed delivery and redelivery details. |
| `exceptions` | Delay, address issue, customs, damage, and no-update details. |
| `customer_actions` | Allowed or blocked customer actions. |
| `order_notes` | Simple operational notes, if not stored on events. |

For the MVP, keep this relational and boring. The point is not clever storage. The point is a clean contract that both Spring Boot and FastAPI can implement.
