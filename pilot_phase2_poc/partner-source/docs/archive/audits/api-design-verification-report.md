# Partner Source API Design Verification Report

> Current status: superseded by later alignment work.
>
> This report is retained as historical design evidence. The current sources of truth are:
>
> - `01-partner-source/15-slice-1-design-freeze.md`
> - `90-shared/contracts/openapi/partner-source.v1.yaml`
> - `90-shared/contracts/shared-error-contract.md`
> - `01-partner-source/17-pending-issues-fix-discussion-draft.md`
>
> Findings below that say the shared error contract, seed data, test plan, or manual request checklist still need the older fixes may be stale.

## 1. Purpose

This report verifies the current `partner-source` API design before implementation continues.

The check is being conducted because the API design now has several connected artifacts:

- actor use cases
- resource map
- seed-data plan
- human API contract
- OpenAPI contract
- shared error contract
- test plan

The goal is to check whether the API design is coherent, realistic for synthetic data, and small enough for the one-week implementation target.

This report stays in design mode. It does not recommend adding implementation code yet.

## 2. Files Reviewed

| File | Purpose Reviewed |
|---|---|
| [../../research/use-cases.md](../../research/use-cases.md) | Actor-level use cases and synthetic support scenarios. |
| [../../support/api-contract-detail.md](../../support/api-contract-detail.md) | Human-readable Slice 1 API contract. |
| [../../support/seed-data-detail.md](../../support/seed-data-detail.md) | Synthetic seed-data plan. |
| [../../support/test-plan-detail.md](../../support/test-plan-detail.md) | Current test coverage plan. |
| [../../research/use-case-resource-map.md](../../research/use-case-resource-map.md) | Resource mapping and endpoint slicing. |
| [../../../90-shared/contracts/shared-error-contract.md](../../../90-shared/contracts/shared-error-contract.md) | Shared error contract. |
| [../../../90-shared/contracts/openapi/partner-source.v1.yaml](../../../90-shared/contracts/openapi/partner-source.v1.yaml) | Formal OpenAPI Slice 1 contract. |

## 3. Executive Summary

The current API design is usable for Slice 1, but it needs a design cleanup before implementation should continue.

The core Slice 1 API can work with synthetic data:

```text
delivery agent retrieves assigned orders
delivery agent creates status event
customer service reads updated status and timeline
```

However, three gaps should be fixed first:

1. The seed-data plan is too thin compared with the questions and fields the API is expected to support.
2. The shared error contract is inconsistent with the RFC 9457-style error format used in the human API contract and OpenAPI YAML.
3. The question-to-information-to-field verification has not been explicitly documented yet.

## 4. Does Synthetic Data Significantly Affect API Design?

### Result

Synthetic data affects API design, but it does not require us to redesign the API.

### Explanation

The API contract can stay mostly as-is because the endpoints expose realistic operational facts:

- order status
- timeline
- driver profile
- assignments
- status events

What synthetic data changes is the required seed coverage.

If the seed data is too shallow, the API will technically work but the demo will feel fake or brittle. For example, a status endpoint can return `ORD-1001`, but if there are no timeline events, no assignment, or no valid next transition, we cannot demonstrate the full loop.

### Practical Rule

Every API endpoint in Slice 1 should have at least one seed scenario that proves it.

```text
Endpoint design -> required fields -> seed record -> test case
```

## 5. Verification Checklist

| Check | Why This Check Is Needed | Result | Action |
|---|---|---|---|
| Slice 1 endpoint scope is small enough | We have one week and cannot design every logistics workflow now. | Pass | Keep Slice 1 limited to status, timeline, driver, assignments, status events, health, and readiness. |
| Actor split is clear | Customer service and delivery agents have different data needs. | Pass | Keep Customer Service Agent read-only and Delivery Agent write-capable. |
| Resource map matches use cases | Endpoints should come from resources, not ad hoc actions. | Pass | Keep `orders`, `drivers`, `assignments`, and `status-events` as Slice 1 resources. |
| Synthetic data supports Slice 1 | Demo data must prove the API behavior. | Partial | Expand seed-data plan with field-level fixtures. |
| Questions map to required information | We need proof that each customer/driver question has enough response fields. | Partial | Add explicit question-to-field matrix. |
| Human contract matches resource map | The human contract should reflect the resource decisions. | Pass | Keep current Slice 1 contract. |
| OpenAPI YAML matches human contract | The implementation will follow OpenAPI, so drift must be avoided. | Pass | Keep YAML as current contract, but continue review after seed-data fixes. |
| Shared error design is consistent | BFF and services need one error shape. | Fail | Update `shared-error-contract.md` to match RFC 9457-style problem details. |
| Test plan covers contract behavior | Tests should follow the contract, not implementation guesses. | Partial | Expand test plan to include seed-data and question-field checks. |
| Deferred endpoints are excluded | Avoid scope creep. | Pass | Keep `support-summary`, `exceptions`, and `delivery-attempts` out of Slice 1. |

## 6. Question To Information To Field Verification

This is the check you proposed:

```text
Question asked -> information required -> fields required -> endpoint/schema support
```

### Customer Service Agent Questions

| Question | Information Required | Required Fields | Current Endpoint | Result |
|---|---|---|---|---|
| "Where is my order?" | Current status, latest update, ETA, location. | `orderId`, `currentStatus`, `statusLabel`, `currentLocation`, `estimatedDeliveryAt`, `lastUpdatedAt` | `GET /api/v1/orders/{orderId}/status` | Pass |
| "Is it out for delivery?" | Current status and status label. | `currentStatus`, `statusLabel` | `GET /api/v1/orders/{orderId}/status` | Pass |
| "When will it arrive?" | ETA and delivery window. | `estimatedDeliveryAt`, `deliveryWindow.start`, `deliveryWindow.end` | `GET /api/v1/orders/{orderId}/status` | Pass |
| "Who is delivering it?" | Assigned driver summary. | `assignedDriver.driverId`, `assignedDriver.displayName` | `GET /api/v1/orders/{orderId}/status` | Pass for demo data |
| "What happened to my shipment?" | Chronological status history. | `items[].status`, `items[].occurredAt`, `items[].actorType`, `items[].location`, `items[].note` | `GET /api/v1/orders/{orderId}/timeline` | Pass |
| "Why is it delayed?" | Delay/exception reason. | `exceptionCode`, `exceptionLabel`, `recoveryEta` | Deferred `GET /api/v1/orders/{orderId}/exceptions` | Deferred |
| "I missed my delivery. What happens next?" | Delivery attempt and next attempt details. | `deliveryAttempts`, `failedAttemptReason`, `nextDeliveryAttemptAt` | Deferred `support-summary` / `delivery-attempts` | Deferred |
| "It says delivered, but I cannot find it." | Delivery note and proof flag. | `deliveredAt`, `deliveryNote`, `proofOfDeliveryAvailable` | Partially represented by `status-events` response | Partial |

### Delivery Agent Questions And Actions

| Question / Action | Information Required | Required Fields | Current Endpoint | Result |
|---|---|---|---|---|
| "Who am I logged in as?" | Driver profile. | `driverId`, `displayName`, `availabilityStatus`, `activeAssignmentCount` | `GET /api/v1/drivers/{driverId}` | Pass |
| "What orders are assigned to me?" | Driver assignments and lightweight delivery details. | `items[].assignmentId`, `items[].orderId`, `items[].currentStatus`, `items[].deliveryWindow` | `GET /api/v1/drivers/{driverId}/assignments` | Pass |
| "Where do I deliver?" | Delivery location/address. | `deliveryAddressSummary` | `GET /api/v1/drivers/{driverId}/assignments` | Partial |
| "Can I mark this delivered?" | Assignment authorization and current status. | `driverId`, `orderId`, `currentStatus`, valid transition policy | `POST /api/v1/orders/{orderId}/status-events` | Pass, if seeded assignment exists |
| "Can I report failed delivery?" | Attempt reason and attempt record. | `reasonCode`, `note`, attempt timestamp | Deferred `POST /api/v1/orders/{orderId}/delivery-attempts` | Deferred |

## 7. Field Coverage Findings

### Pass

The current Slice 1 fields are enough for:

- basic WISMO status lookup
- ETA questions
- current driver assignment display
- order timeline display
- driver profile lookup
- assigned order list
- delivered status update

### Partial

The current fields are only partially enough for:

- driver delivery execution, because `deliveryAddressSummary` may not be enough for an actual delivery-agent screen
- delivered-but-not-found support, because proof-of-delivery is represented on status-event creation but not clearly available through `GET /status`
- missed-delivery support, because `delivery-attempts` is deferred

### Missing Or Deferred

The current Slice 1 design does not answer:

- why a package is delayed
- what redelivery attempt is scheduled
- whether address change is allowed
- customs/duties questions
- damaged or missing contents claims

This is acceptable for Slice 1 as long as these questions are explicitly out of scope.

## 8. Synthetic Data Verification

### Current Seed Plan

The seed-data plan currently lists:

| Type | IDs |
|---|---|
| Orders | `ORD-1001`, `ORD-1002`, `ORD-1003` |
| Drivers | `DRV-2001`, `DRV-2002` |
| Assignments | `ASN-3001`, `ASN-3002` |

The only fully described order is:

```text
ORD-1001
status: OUT_FOR_DELIVERY
driver: DRV-2001
eta: today 18:00
location: Tampines Delivery Hub
```

### Result

Partial.

This is enough to start Slice 1, but not enough to verify all Slice 1 behaviors properly.

### Missing Seed Requirements

| Required Scenario | Why It Is Needed | Suggested Seed |
|---|---|---|
| Valid status update | Proves driver can update status. | `ORD-1001` assigned to `DRV-2001`, current status `OUT_FOR_DELIVERY`, allowed transition to `DELIVERED`. |
| Timeline with multiple events | Proves timeline endpoint. | `ORD-1001` has `CREATED`, `CONFIRMED`, `PICKED_UP`, `IN_TRANSIT`, `OUT_FOR_DELIVERY`. |
| Missing order test | Proves `ORDER_NOT_FOUND`. | Query `ORD-9999`, do not seed it. |
| Driver with assignments | Proves assignment list. | `DRV-2001` assigned to `ORD-1001` and `ORD-1002`. |
| Driver with no assignments | Proves empty list behavior. | `DRV-2002` or `DRV-2003` with no active assignments. |
| Driver not assigned to order | Proves authorization-style validation. | `DRV-2002` attempts to update `ORD-1001`. |
| Invalid transition | Proves transition policy. | `ORD-1003` current status `DELIVERED`, request `OUT_FOR_DELIVERY`. |

## 9. Recommended Slice 1 Seed Matrix

Use a small but deliberate seed set:

| ID | Type | Scenario | Required Fields |
|---|---|---|---|
| `ORD-1001` | Order | Out for delivery, assigned to active driver. | status, ETA, location, driver, delivery window. |
| `ORD-1002` | Order | In transit, assigned to same driver. | status, ETA, timeline, assignment. |
| `ORD-1003` | Order | Delivered, used for invalid transition tests. | delivered status, completed timeline. |
| `DRV-2001` | Driver | Active driver with assignments. | profile, availability, assignment count. |
| `DRV-2002` | Driver | Valid driver not assigned to `ORD-1001`. | profile, zero/other assignments. |
| `ASN-3001` | Assignment | `DRV-2001` -> `ORD-1001`. | assigned status, delivery window. |
| `ASN-3002` | Assignment | `DRV-2001` -> `ORD-1002`. | assigned status, delivery window. |
| `EVT-4001` to `EVT-4005` | Status events | Timeline for `ORD-1001`. | status, actor, occurredAt, location/note. |

This is small enough for one week and strong enough to test the core API.

## 10. API Design Impact From Synthetic Data

### Does Synthetic Data Force New Endpoints?

No.

The current Slice 1 endpoints are still appropriate.

### Does Synthetic Data Force New Fields?

Some small adjustments should be considered:

| Field | Current Status | Recommendation |
|---|---|---|
| `deliveryAddressSummary` | Present in assignments. | Keep for Slice 1. Add full address only if driver UI requires it. |
| `proofOfDeliveryAvailable` | Present in status-event response/request. | Decide whether it should also appear in `GET /status` after delivered. |
| `activeAssignmentCount` | Present in driver response. | Ensure seed data matches this value. |
| `assignedDriver` | Present in order status. | Ensure it can be `null` for unassigned orders if needed. |
| `currentLocation` | Nullable in OpenAPI. | Ensure examples cover both location and no-location cases later. |

## 11. Error Contract Verification

### Result

Fail.

The shared error contract currently uses this shape:

```json
{
  "errorCode": "ORDER_NOT_FOUND",
  "message": "Order was not found.",
  "requestId": "req-123"
}
```

The human API contract and OpenAPI YAML use this shape:

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

### Recommendation

Update [../../../90-shared/contracts/shared-error-contract.md](../../../90-shared/contracts/shared-error-contract.md) to match the RFC 9457-style problem detail format.

Also standardize the naming:

- use `correlationId`
- do not use `requestId` unless we deliberately choose that name everywhere
- use `INVALID_STATUS_TRANSITION`
- do not use the older `ORDER_TRANSITION_INVALID`

## 12. Status Code And Error Code Verification

| Case | Current Contract | Result | Note |
|---|---|---|---|
| Missing order | `404 ORDER_NOT_FOUND` | Pass | Good. |
| Missing driver | `404 DRIVER_NOT_FOUND` | Pass | Good. |
| Driver not assigned | `403 ORDER_NOT_ASSIGNED_TO_DRIVER` | Pass | Good for demo authorization boundary. |
| Invalid transition | `409 INVALID_STATUS_TRANSITION` | Pass | Better than generic validation error. |
| Invalid status event | `422 INVALID_STATUS_EVENT` | Pass | Good for semantic payload errors. |
| Invalid request shape | `400 INVALID_REQUEST` | Pass | Good. |
| Shared naming consistency | Mixed names | Fail | Align shared error contract. |

## 13. Test Plan Verification

### Current Test Plan

The current test plan covers:

1. existing order returns current status
2. missing order returns `ORDER_NOT_FOUND`
3. driver can retrieve assigned orders
4. valid status transition is accepted
5. invalid status transition returns `ORDER_TRANSITION_INVALID`
6. timeline returns chronological events

### Result

Partial.

The test plan is directionally correct, but it is now behind the current API contract.

### Missing Test Design

Add tests for:

- `GET /api/v1/drivers/{driverId}` returns driver profile
- missing driver returns `DRIVER_NOT_FOUND`
- driver not assigned returns `ORDER_NOT_ASSIGNED_TO_DRIVER`
- invalid status value returns `INVALID_STATUS_EVENT`
- valid status event updates current order status
- valid status event appears in timeline
- pagination validation for timeline and assignments
- shared error shape follows `ProblemDetail`

Also rename:

```text
ORDER_TRANSITION_INVALID -> INVALID_STATUS_TRANSITION
```

## 14. OpenAPI Verification

### Result

Pass for Slice 1 structure.

The OpenAPI YAML includes the expected paths:

```http
GET /api/v1/orders/{orderId}/status
GET /api/v1/orders/{orderId}/timeline
GET /api/v1/drivers/{driverId}
GET /api/v1/drivers/{driverId}/assignments
POST /api/v1/orders/{orderId}/status-events
GET /health
GET /ready
```

It also defines the expected schemas:

- `OrderStatusResponse`
- `OrderTimelineResponse`
- `DriverResponse`
- `DriverAssignmentsResponse`
- `CreateStatusEventRequest`
- `StatusEventResponse`
- `ProblemDetail`
- `HealthResponse`
- `ReadinessResponse`

### Concern

The OpenAPI contract includes examples that assume richer seed data than currently documented.

Example:

- `DriverResponse.activeAssignmentCount` is `3`
- seed-data plan currently has only two assignments

This is easy to fix by aligning seed fixtures with OpenAPI examples.

## 15. Manual Request Verification

### Result

Partial.

The manual `.http` file is useful, but it should include expected results as comments.

Recommended pattern:

```http
### Get current order status
# Expected: 200 OK
# Expected field: currentStatus = OUT_FOR_DELIVERY
GET {{baseUrl}}/api/v1/orders/{{orderId}}/status
Accept: application/json
```

This turns the file into a human-readable checklist, not just a request list.

## 16. Final Verification Result

| Area | Result |
|---|---|
| Endpoint scope | Pass |
| Actor-to-resource mapping | Pass |
| Question-to-field coverage | Partial |
| Synthetic seed-data support | Partial |
| Human API contract | Pass |
| OpenAPI contract | Pass |
| Shared error contract | Fail |
| Test plan | Partial |
| Manual requests | Partial |

## 17. What We Have Missed

The biggest missed item is not an endpoint. It is seed-data intentionality.

The API design assumes that synthetic records will support the questions. The seed-data plan does not yet prove that.

We should not treat synthetic data as an implementation detail. For this project, synthetic data is part of the API design because it determines:

- which questions can be answered
- which fields are required
- which scenarios are testable
- whether the demo feels real

## 18. Recommended Design-Only Next Steps

Do these before implementation resumes:

1. Update [../../support/seed-data-detail.md](../../support/seed-data-detail.md) with the Slice 1 seed matrix.
2. Update [shared-error-contract.md](../../../90-shared/contracts/shared-error-contract.md) to match the `ProblemDetail` format.
3. Update [../../support/test-plan-detail.md](../../support/test-plan-detail.md) to match current error codes and add missing test cases.
4. Update [partner-source-slice1.http](../../../90-shared/contracts/openapi/http/partner-source-slice1.http) with expected outcomes.
5. Re-review [partner-source.v1.yaml](../../../90-shared/contracts/openapi/partner-source.v1.yaml) after seed-data alignment.

## 19. Decision Recommendation

We can keep the current Slice 1 API design.

Do not add more endpoints right now.

Instead, strengthen the design by making the synthetic data, expected questions, required fields, and test cases line up.

The next design task should be:

```text
Update the seed-data plan using the question-to-field verification matrix.
```
