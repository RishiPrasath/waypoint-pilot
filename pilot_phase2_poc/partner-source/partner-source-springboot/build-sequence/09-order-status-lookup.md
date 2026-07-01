# 09 - Order Status Lookup

## Purpose

Implement the first contract data endpoint: `GET /api/v1/orders/{orderId}/status`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `8. Response Shapes` and `10. Acceptance Scenarios`
- `../../docs/active/contract-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Tests To Write First

Create:

```text
src/test/java/com/waypoint/partnersource/order/service/OrderStatusServiceTest.java
src/test/java/com/waypoint/partnersource/order/api/OrderStatusControllerTest.java
```

Test cases:

- Service returns `ORD-1001` with `currentStatus = OUT_FOR_DELIVERY`.
- Response includes `assignedDriver.driverId = DRV-2001`.
- Missing `ORD-9999` maps to an order-not-found exception.
- Controller returns `200` for `ORD-1001`.
- Controller rejects invalid ID format with `400 INVALID_REQUEST`.

## Code To Implement

DTOs:

```text
order/api/dto/OrderStatusResponse.java
order/api/dto/LocationSnapshotResponse.java
order/api/dto/DeliveryWindowResponse.java
order/api/dto/AssignedDriverSummaryResponse.java
```

Service and mapper:

```text
order/service/OrderStatusService.java
order/service/OrderResponseMapper.java
```

Controller:

```text
order/api/OrderStatusController.java
```

Temporary error handling is acceptable for the first negative path, but step 10 must centralize the full ProblemDetail envelope.

## Commands To Run

```powershell
.\mvnw.cmd -Dtest=OrderStatusServiceTest,OrderStatusControllerTest test
.\mvnw.cmd test
```

Manual check:

```powershell
Invoke-RestMethod http://localhost:8080/api/v1/orders/ORD-1001/status
```

## Done Criteria

- [ ] Success service test passes.
- [ ] Success controller test passes.
- [ ] Missing order test exists.
- [ ] Invalid path ID test exists.
- [ ] JSON field names match OpenAPI exactly.

## Stop / Do Not Add

- Do not implement timeline here.
- Do not add status-event mutation here.

