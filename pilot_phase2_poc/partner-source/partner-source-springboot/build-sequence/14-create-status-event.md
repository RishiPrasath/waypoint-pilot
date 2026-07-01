# 14 - Create Status Event

## Purpose

Implement `POST /api/v1/orders/{orderId}/status-events`, the final Slice 1 write endpoint.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `6`, `7`, `8`, `9`, and `10`
- `../../docs/active/contract-handoff.md`
- `../../docs/active/data-and-seed-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../docs/contracts/shared-error-contract.md`

## Tests To Write First

Create:

```text
src/test/java/com/waypoint/partnersource/order/service/StatusEventServiceTest.java
src/test/java/com/waypoint/partnersource/order/api/StatusEventControllerTest.java
```

Test cases:

- `DRV-2001` creates `DELIVERED` event for `ORD-1001` and receives `201`.
- Response has `previousStatus = OUT_FOR_DELIVERY`, `newStatus = DELIVERED`, `orderCurrentStatus = DELIVERED`.
- Order current status mutates to `DELIVERED`.
- Timeline appends the new event after existing events.
- `DRV-2002` on `ORD-1001` returns `403 ORDER_NOT_ASSIGNED_TO_DRIVER`.
- `DRV-9999` returns `404 DRIVER_NOT_FOUND`.
- `ORD-9999` returns `404 ORDER_NOT_FOUND`.
- `ORD-1003` with backward status returns `409 INVALID_STATUS_TRANSITION`.
- Far-future `occurredAt` returns `422 INVALID_STATUS_EVENT`.
- Malformed body returns `400 INVALID_REQUEST`.

## Code To Implement

Request/response DTOs:

```text
order/api/dto/CreateStatusEventRequest.java
order/api/dto/StatusEventResponse.java
```

Service/controller:

```text
order/service/StatusEventService.java
order/api/StatusEventController.java
```

Service order:

1. Validate order exists.
2. Validate driver exists.
3. Validate assignment authorization.
4. Validate status transition.
5. Validate event semantics, such as far-future `occurredAt`.
6. Append event.
7. Update order current status.
8. Return response.

## Commands To Run

```powershell
.\mvnw.cmd -Dtest=StatusEventServiceTest,StatusEventControllerTest test
.\mvnw.cmd test
```

Manual check:

```powershell
$body = @{
  driverId = "DRV-2001"
  status = "DELIVERED"
  occurredAt = "2026-06-30T15:45:00+08:00"
  note = "Left with reception"
  proofOfDeliveryAvailable = $true
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8080/api/v1/orders/ORD-1001/status-events `
  -ContentType "application/json" `
  -Body $body
```

## Done Criteria

- [ ] All success and negative tests pass.
- [ ] Mutation is visible through status lookup and timeline.
- [ ] Error status and `errorCode` match the shared contract.
- [ ] No extra status-event fields are invented.

## Stop / Do Not Add

- Do not add proof upload, signatures, photos, delivery-attempt flows, or external integrations.

