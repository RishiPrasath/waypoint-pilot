# 11 - Order Timeline

## Purpose

Implement `GET /api/v1/orders/{orderId}/timeline`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `8. Response Shapes` and `10. Acceptance Scenarios`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/11-order-timeline.md`

## Tests To Write First

Create:

```text
tests/services/test_order_timeline_service.py
tests/api/test_order_timeline_api.py
```

Test cases:

- `ORD-1001` returns five events.
- Events are chronological from `EVT-4001` to `EVT-4005`.
- Response includes `page`, `pageSize`, and `totalItems`.
- Missing order returns `404 ORDER_NOT_FOUND`.
- Invalid `page` or `pageSize` returns `400 INVALID_REQUEST`.

## Code To Implement

Extend:

```text
app/schemas/orders.py
app/services/order_timeline.py
app/api/orders.py
```

Use existing repository and error handling.

## Commands To Run

```powershell
python -m pytest tests/services/test_order_timeline_service.py tests/api/test_order_timeline_api.py
python -m pytest
```

Manual check:

```powershell
Invoke-RestMethod "http://localhost:8000/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"
```

## Done Criteria

- [ ] Timeline is chronological.
- [ ] Pagination fields match OpenAPI.
- [ ] Error envelope is reused.

## Stop / Do Not Add

- Do not add uncontracted sorting filters.
- Do not add delivery-attempt behavior.

