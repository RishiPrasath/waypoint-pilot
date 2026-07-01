# 13 - Driver Assignments

## Purpose

Implement `GET /api/v1/drivers/{driverId}/assignments`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `7. Seed Data`, `8. Response Shapes`, and `10. Acceptance Scenarios`
- `../../docs/active/data-and-seed-handoff.md`
- `../../partner-source-springboot/build-sequence/13-driver-assignments.md`

## Tests To Write First

Create:

```text
tests/services/test_driver_assignments_service.py
tests/api/test_driver_assignments_api.py
```

Test cases:

- `DRV-2001` returns two active assignment items.
- Items include `ORD-1001` and `ORD-1002`.
- `DRV-2003` returns empty `items` and `totalItems = 0`.
- Missing driver returns `404 DRIVER_NOT_FOUND`.
- Optional `status` filter accepts valid `OrderStatus` values.
- Invalid `status`, `page`, or `pageSize` returns `400 INVALID_REQUEST`.

## Code To Implement

Extend:

```text
app/schemas/drivers.py
app/services/driver_assignments.py
app/api/drivers.py
```

Use order and assignment repositories to enrich assignment items.

## Commands To Run

```powershell
python -m pytest tests/services/test_driver_assignments_service.py tests/api/test_driver_assignments_api.py
python -m pytest
```

Manual check:

```powershell
Invoke-RestMethod "http://localhost:8000/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20"
```

## Done Criteria

- [ ] Active assignment list is correct.
- [ ] Empty assignment list returns `items: []`.
- [ ] Pagination fields match OpenAPI.
- [ ] Missing driver and validation errors use ProblemDetail.

## Stop / Do Not Add

- Do not add assignment creation endpoints.
- Do not include completed `ASN-3003` as active work.

