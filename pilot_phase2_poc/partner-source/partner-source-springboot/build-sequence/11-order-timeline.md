# 11 - Order Timeline

## Purpose

Implement `GET /api/v1/orders/{orderId}/timeline`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `8. Response Shapes` and `10. Acceptance Scenarios`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../docs/active/data-and-seed-handoff.md`

## Tests To Write First

Create:

```text
src/test/java/com/waypoint/partnersource/order/service/OrderTimelineServiceTest.java
src/test/java/com/waypoint/partnersource/order/api/OrderTimelineControllerTest.java
```

Test cases:

- `ORD-1001` returns five events.
- Events are chronological from `EVT-4001` to `EVT-4005`.
- Response includes `page`, `pageSize`, and `totalItems`.
- Missing order returns `404 ORDER_NOT_FOUND`.
- Invalid `page` or `pageSize` returns `400 INVALID_REQUEST`.

## Code To Implement

DTOs:

```text
order/api/dto/OrderTimelineResponse.java
order/api/dto/TimelineEventResponse.java
```

Service/controller:

```text
order/service/OrderTimelineService.java
order/api/OrderTimelineController.java
```

Reuse existing location DTOs and mapper where sensible.

## Commands To Run

```powershell
.\mvnw.cmd -Dtest=OrderTimelineServiceTest,OrderTimelineControllerTest test
.\mvnw.cmd test
```

Manual check:

```powershell
Invoke-RestMethod "http://localhost:8080/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"
```

## Done Criteria

- [ ] Timeline is chronological.
- [ ] Pagination fields match OpenAPI.
- [ ] Error envelope is reused.
- [ ] No mutation happens in this endpoint.

## Stop / Do Not Add

- Do not implement delivery-attempt behavior.
- Do not add sorting query parameters not in the contract.

