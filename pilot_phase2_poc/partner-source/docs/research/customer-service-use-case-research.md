# Customer Service And Delivery Agent Use Case Research For Partner Source

## 1. Purpose

This report identifies realistic delivery-support use cases for `partner-source` and splits them by actor:

- Customer Service Agent: answers customer questions about deliveries.
- Delivery Agent: updates operational delivery status.

The project constraint is important:

- We do not have access to real logistics-company internal systems.
- We are creating a mock partner data source with synthetic orders, drivers, assignments, timelines, locations, and exceptions.
- The API, database, and data creation process are expected to support repeatable demo data.

Therefore, the goal is not to model every real carrier process. The goal is to create enough synthetic operational truth for Waypoint to demonstrate realistic support and delivery workflows.

## 2. Research Sources Reviewed

| Source | What It Contributes |
|---|---|
| [Salesforce WISMO guide](https://www.salesforce.com/commerce/wismo/) | WISMO as a high-volume customer-service pattern across email, phone, chat, and social channels. |
| [DHL eCommerce tracking and shipment FAQ](https://www.dhl.com/us-en/home/customer-service/ecommerce-tracking-faq.html) | Common questions around tracking, unchanged status, delivery delays, address/date changes, customs, damaged/missing contents, and claims. |
| [UPS tracking support](https://www.ups.com/us/en/support/tracking-support) | Tracking, missed delivery, delivery changes, customs/import fees, claims, delivered-but-not-found, and ETA questions. |
| [FedEx customer support](https://www.fedex.com/en-us/customer-support.html) | Tracking, tracing, lost/damaged/missing items, delivery management, delivery exceptions, address changes, returns, and billing/customs support. |
| [FedEx missed delivery FAQ](https://www.fedex.com/en-us/customer-support/faqs/receiving/tracking-questions/missed-delivery.html) | Missed delivery and pickup-hold behavior. |
| [USPS missing mail guidance](https://www.usps.com/help/missing-mail.htm) | Missing package workflow: check current status, submit search request, provide tracking and package details, claim/refund paths. |
| [Gorgias ShipBob support action docs](https://docs.gorgias.com/en-US/support-actions-connect-ai-agent-to-shipbob-937575) | Support agent/AI agent use case: retrieve order information from fulfillment data for WISMO-style answers. |
| [AfterShip Zendesk integration docs](https://support.aftership.com/en/tracking/articles/15441758-connect-zendesk-with-aftership-tracking) | Agent-side support workflow: tracking number, carrier, delivery status, and tracking details surfaced inside a ticketing system. |

## 3. Research Synthesis

Customer-service questions around shipping are not only "Where is my order?"

The recurring categories are:

| Category | Customer Question Examples | Partner Source Data Needed |
|---|---|---|
| Current status / WISMO | "Where is my order?", "Has it shipped?", "Is it out for delivery?" | order ID, current status, status label, latest event, ETA |
| ETA / delivery window | "When will it arrive?", "Will it arrive today?", "How late can it be delivered?" | estimated delivery time, service level, delivery window, latest status |
| Tracking not updating | "Why has tracking not changed?", "Is my package stuck?" | last scan time, last scan location, milestone history, no-update reason |
| Delayed shipment | "Why is it late?", "What caused the delay?" | delay reason, exception code, expected recovery ETA, latest event |
| Delivered but not found | "It says delivered but I cannot find it." | delivery timestamp, delivery note, proof-of-delivery flag |
| Missed delivery | "I missed the driver. What happens now?" | delivery attempt count, failed reason, next attempt date, pickup/hold note |
| Address/date change | "Can I change the address?", "Can I reschedule delivery?" | shipment change eligibility, current shipment stage, allowed actions |
| Customs/duties | "Why is customs holding it?", "Do I need to pay duties?" | customs status, required action, duties/taxes flag |
| Damaged/missing contents | "My package arrived damaged.", "Something is missing." | delivery status, damage flag, claim eligibility marker |
| Return / cancellation | "Can I cancel?", "Where is my return?" | fulfillment stage, cancellation eligibility, return tracking ID |

The second actor is the delivery agent. This person is not answering customers. They create the operational events that customer service later reads.

## 4. Practical Actor Model

| Actor | Main Intent | Data Direction | Practical MVP Role |
|---|---|---|---|
| Customer Service Agent | Answer customer questions. | Reads order facts. | Searches by order ID and reads status, timeline, ETA, exceptions, attempts, and support summary. |
| Delivery Agent | Report delivery progress. | Reads assignments and writes events. | Retrieves assigned orders and updates status or failed-attempt details. |

This split keeps the prototype realistic:

- Customer service does not magically know real-time operational facts unless the system has stored them.
- Delivery agents are the main source of new operational status updates.
- The BFF can expose different views for chatbot, support agent, and driver frontend without changing the underlying partner-source contract.

## 5. What Partner Source Should Own

`partner-source` should own operational facts.

It should expose:

- order records
- driver records
- assignment records
- current order/shipment status
- status timeline
- delivery attempts
- current/last known location snapshot
- estimated delivery time
- exception flags
- allowed next actions
- synthetic claim/return/customs eligibility flags

It should not own:

- chatbot wording
- final customer-facing tone
- RAG policy explanations
- support-agent narrative generation
- frontend rendering
- real authentication beyond demo identity checks
- route optimization
- live GPS tracking
- real claims processing

The BFF should turn partner-source facts into frontend-specific responses.

## 6. Customer Service Agent Use Cases

### CSA-01: Look Up Order By Order ID

Customer asks:

- "Can you check my order?"
- "Where is `ORD-1001`?"

API:

```http
GET /api/v1/orders/{orderId}/status
```

Priority: must build.

### CSA-02: View Current Order Status

Customer asks:

- "Where is my order?"
- "Has my order shipped?"
- "Is my package out for delivery?"

API:

```http
GET /api/v1/orders/{orderId}/status
```

Synthetic scenario:

```text
ORD-1001
status: OUT_FOR_DELIVERY
eta: 2026-06-30T18:00:00+08:00
latest location: Tampines Delivery Hub
latest event: Loaded onto delivery vehicle
```

Priority: must build.

### CSA-03: View Order Timeline

Customer asks:

- "What happened to my shipment?"
- "When was it picked up?"
- "Why does it show in transit?"

API:

```http
GET /api/v1/orders/{orderId}/timeline
```

Synthetic scenario:

```text
CREATED -> CONFIRMED -> PICKED_UP -> IN_TRANSIT -> OUT_FOR_DELIVERY
```

Priority: must build.

### CSA-04: View ETA And Delivery Window

Customer asks:

- "When will it arrive?"
- "Will it come today?"
- "What time should I expect delivery?"

API need:

```json
{
  "estimatedDeliveryAt": "2026-06-30T18:00:00+08:00",
  "deliveryWindow": {
    "start": "2026-06-30T14:00:00+08:00",
    "end": "2026-06-30T18:00:00+08:00"
  }
}
```

Priority: must build for WISMO quality.

### CSA-05: View Delay Or Exception Reason

Customer asks:

- "Why is my package delayed?"
- "What does exception mean?"
- "When will it move again?"

API:

```http
GET /api/v1/orders/{orderId}/exceptions
```

Synthetic scenario:

```json
{
  "hasException": true,
  "exceptionCode": "WEATHER_DELAY",
  "exceptionLabel": "Weather delay",
  "recoveryEta": "2026-07-01T18:00:00+08:00"
}
```

Priority: should build after status and timeline.

### CSA-06: View Failed Delivery Attempt Details

Customer asks:

- "I missed my delivery. What happens next?"
- "Will the driver try again?"
- "Can I pick it up somewhere?"

API:

```http
GET /api/v1/orders/{orderId}/support-summary
```

Synthetic scenario:

```json
{
  "currentStatus": "DELIVERY_ATTEMPTED",
  "deliveryAttempts": 1,
  "failedAttemptReason": "RECIPIENT_UNAVAILABLE",
  "nextDeliveryAttemptAt": "2026-07-01T10:00:00+08:00"
}
```

Priority: should build.

### CSA-07: View Delivered But Not Found Facts

Customer asks:

- "It says delivered, but I cannot find it."
- "Where was it left?"
- "Who received it?"

API:

```http
GET /api/v1/orders/{orderId}/support-summary
```

Synthetic scenario:

```json
{
  "currentStatus": "DELIVERED",
  "deliveredAt": "2026-06-30T15:45:00+08:00",
  "deliveryNote": "Left with reception",
  "proofOfDeliveryAvailable": true
}
```

Priority: should build because this is a common support escalation.

### CSA-08: View Available Customer Actions

Customer asks:

- "Can I change the address?"
- "Can I reschedule?"
- "Can I leave delivery instructions?"

API:

```http
GET /api/v1/orders/{orderId}/available-actions
```

Priority: later. Keep this read-only first.

### CSA-09: Get Support Summary

Agent need:

- one compact order view
- current status
- ETA
- timeline summary
- latest exception
- delivery attempt details
- allowed/blocked customer actions

API:

```http
GET /api/v1/orders/{orderId}/support-summary
```

Priority: must build after status, timeline, and exception foundations exist.

## 7. Delivery Agent Use Cases

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
- add simple demo identity checks later if required

Priority: must build for the driver frontend.

### DA-02: Retrieve Assigned Orders

Driver asks:

- "What orders are assigned to me?"
- "What is my next delivery?"
- "Which orders can I update?"

API:

```http
GET /api/v1/drivers/{driverId}/assignments
```

Priority: must build.

### DA-03: View Delivery Details

Driver needs:

- order ID
- recipient display name
- delivery address
- delivery window
- current status
- simple delivery instructions

API:

```http
GET /api/v1/orders/{orderId}/delivery-view
```

Priority: should build, or include these fields in the assignment response.

### DA-04: Mark Order As Picked Up

Driver action:

- confirms package pickup or loading

API:

```http
POST /api/v1/orders/{orderId}/status-events
```

Priority: must build if the demo begins before dispatch.

### DA-05: Mark Order As Out For Delivery

Driver action:

- confirms package is on the delivery route

API:

```http
POST /api/v1/orders/{orderId}/status-events
```

Priority: must build.

### DA-06: Mark Order As Delivered

Driver action:

- completes delivery

API:

```http
POST /api/v1/orders/{orderId}/status-events
```

Example:

```json
{
  "driverId": "DRV-2001",
  "status": "DELIVERED",
  "note": "Left with reception",
  "proofOfDeliveryAvailable": true
}
```

Priority: must build.

### DA-07: Report Failed Delivery Attempt

Driver action:

- reports that delivery could not be completed

API:

```http
POST /api/v1/orders/{orderId}/delivery-attempts
```

Example:

```json
{
  "driverId": "DRV-2001",
  "attemptStatus": "FAILED",
  "reasonCode": "RECIPIENT_UNAVAILABLE",
  "note": "No answer at door"
}
```

Priority: should build.

### DA-08: Report Operational Exception

Driver action:

- reports an issue such as address problem, access issue, or damaged package

API:

```http
POST /api/v1/orders/{orderId}/exceptions
```

Priority: later. Useful, but not needed before basic status updates.

### DA-09: Add Delivery Note

Driver action:

- adds a short operational note

API:

```http
POST /api/v1/orders/{orderId}/notes
```

Priority: later. Fold this into `status-events.note` for the first version.

## 8. Synthetic Data Scenarios

The synthetic database should not contain only happy-path records. It should contain representative support and driver-operation cases.

| Order ID | Scenario | Status | Why It Exists |
|---|---|---|---|
| `ORD-1001` | Normal out-for-delivery order | `OUT_FOR_DELIVERY` | Basic WISMO happy path |
| `ORD-1002` | Tracking not updated | `IN_TRANSIT` | "Why is tracking stuck?" |
| `ORD-1003` | Failed delivery attempt | `DELIVERY_ATTEMPTED` | Missed delivery/redelivery |
| `ORD-1004` | Delivered but not found | `DELIVERED` | Delivered-location support |
| `ORD-1005` | Weather delay | `DELAYED` | Exception explanation |
| `ORD-1006` | Customs hold | `CUSTOMS_HOLD` | International shipping issue |
| `ORD-1007` | Damaged delivery reported | `DELIVERED` | Claim/damage support |
| `ORD-1008` | Address issue | `ON_HOLD` | Customer action required |
| `ORD-1009` | Cancelled before dispatch | `CANCELLED` | Cancellation eligibility |
| `ORD-1010` | Returned to sender | `RETURNED` | Failed delivery lifecycle |

Driver records:

| Driver ID | Scenario |
|---|---|
| `DRV-2001` | Active driver with normal assignments |
| `DRV-2002` | Driver with failed-delivery assignment |
| `DRV-2003` | Offline/unavailable driver |

## 9. Recommended Status Model

Recommended statuses:

```text
CREATED
CONFIRMED
PICKED_UP
IN_TRANSIT
OUT_FOR_DELIVERY
DELIVERY_ATTEMPTED
DELAYED
CUSTOMS_HOLD
ON_HOLD
DELIVERED
FAILED_DELIVERY
RETURNED
CANCELLED
```

Recommended exception codes:

```text
WEATHER_DELAY
CUSTOMS_HOLD
DUTIES_PAYMENT_REQUIRED
ADDRESS_ISSUE
RECIPIENT_UNAVAILABLE
DAMAGED_REPORTED
MISSING_CONTENTS_REPORTED
OPERATIONAL_BACKLOG
NO_RECENT_SCAN
```

## 10. Recommended MVP Build Order

Build in this order:

1. `CSA-01` and `CSA-02`: order lookup and current status.
2. `CSA-03`: order timeline.
3. `CSA-04`: ETA and delivery window fields.
4. `DA-01`: demo driver lookup.
5. `DA-02`: driver assigned orders.
6. `DA-05` and `DA-06`: driver status updates.
7. `DA-07`: failed delivery attempt.
8. `CSA-05` and `CSA-06`: exception and failed-attempt support views.
9. `CSA-09`: support summary.

This sequence proves the practical loop:

```text
driver update -> stored status event -> customer/support lookup -> BFF-shaped answer
```

## 11. Deferred Scope

Defer:

- real authentication
- real customer identity
- live GPS
- route optimization
- address change execution
- claims workflow
- customs payment workflow
- proof-of-delivery image upload
- carrier integrations
- advanced driver scheduling

These deferred cases can still exist as synthetic flags or static scenarios, but the API does not need full workflow support yet.

## 12. Database Implications

The database should support:

| Table / Collection | Purpose |
|---|---|
| `orders` | Base order identity, current status, ETA, delivery window. |
| `drivers` | Driver profiles and availability. |
| `assignments` | Order-driver assignment. |
| `status_events` | Timeline and status history. |
| `delivery_attempts` | Missed delivery and redelivery data. |
| `exceptions` | Delay, customs, damage, no-scan, failed-delivery details. |
| `customer_actions` | Available/blocked customer actions. |
| `order_notes` | Optional operational notes if not stored on status events. |

For the first implementation, these can be seeded relational tables.

## 13. Final Recommendation

Use two practical actor lanes:

- Customer Service Agent: read operational facts to answer customer questions.
- Delivery Agent: create operational facts by updating delivery progress.

The first useful version should answer:

- Where is my order?
- When will it arrive?
- What happened in the timeline?
- Why is it delayed?
- What orders are assigned to this driver?
- Can this driver update the status?
- Did the driver deliver it or report a failed attempt?

That is enough to support the BFF and frontend demo without pretending to have a real logistics-company backend.

