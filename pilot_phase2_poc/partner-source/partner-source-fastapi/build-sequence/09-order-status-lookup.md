# 09 - Order Status Lookup

## Purpose

Implement `GET /api/v1/orders/{orderId}/status`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `8. Response Shapes` and `10. Acceptance Scenarios`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/09-order-status-lookup.md`

## Tests To Write First

Create:

```text
tests/services/test_order_status_service.py
tests/api/test_orders_api.py
```

Test cases:

- Service returns `ORD-1001` with `currentStatus = OUT_FOR_DELIVERY`.
- Response includes `assignedDriver.driverId = DRV-2001`.
- Missing `ORD-9999` raises a Partner Source error.
- API returns `200` for `ORD-1001`.
- Invalid ID format returns `400 INVALID_REQUEST`.

## Code To Implement

Schemas:

```text
app/schemas/orders.py
app/schemas/shared.py
```

Service/router:

```text
app/services/order_status.py
app/api/orders.py
```

Update:

```text
app/main.py
```

Register the orders router.

## Commands To Run

```powershell
python -m pytest tests/services/test_order_status_service.py tests/api/test_orders_api.py
python -m pytest
```

Manual check:

```powershell
Invoke-RestMethod http://localhost:8000/api/v1/orders/ORD-1001/status
```

## Done Criteria

- [ ] Success service and API tests pass.
- [ ] Missing order test exists.
- [ ] Invalid path ID test exists.
- [ ] JSON uses OpenAPI field names, such as `orderId` and `currentStatus`.

## Stop / Do Not Add

- Do not implement timeline here.
- Do not implement status-event mutation.

