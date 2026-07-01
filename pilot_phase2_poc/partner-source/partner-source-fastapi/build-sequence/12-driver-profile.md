# 12 - Driver Profile

## Purpose

Implement `GET /api/v1/drivers/{driverId}`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `7. Seed Data`, `8. Response Shapes`, and `10. Acceptance Scenarios`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/12-driver-profile.md`

## Tests To Write First

Create:

```text
tests/services/test_driver_profile_service.py
tests/api/test_drivers_api.py
```

Test cases:

- `DRV-2001` returns `availabilityStatus = AVAILABLE`.
- `DRV-2001` returns `activeAssignmentCount = 2`.
- `DRV-9999` returns `404 DRIVER_NOT_FOUND`.
- Invalid driver ID format returns `400 INVALID_REQUEST`.

## Code To Implement

Schemas:

```text
app/schemas/drivers.py
```

Service/router:

```text
app/services/driver_profile.py
app/api/drivers.py
```

Update `app/main.py` to register the drivers router.

## Commands To Run

```powershell
python -m pytest tests/services/test_driver_profile_service.py tests/api/test_drivers_api.py
python -m pytest
```

Manual check:

```powershell
Invoke-RestMethod http://localhost:8000/api/v1/drivers/DRV-2001
```

## Done Criteria

- [ ] Success and missing-driver tests pass.
- [ ] `activeAssignmentCount` counts active assignments only.
- [ ] Error envelope is reused.

## Stop / Do Not Add

- Do not add driver create/update endpoints.
- Do not add authentication.

