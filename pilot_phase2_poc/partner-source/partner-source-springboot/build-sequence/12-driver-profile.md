# 12 - Driver Profile

## Purpose

Implement `GET /api/v1/drivers/{driverId}`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `7. Seed Data`, `8. Response Shapes`, and `10. Acceptance Scenarios`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Tests To Write First

Create:

```text
src/test/java/com/waypoint/partnersource/driver/service/DriverServiceTest.java
src/test/java/com/waypoint/partnersource/driver/api/DriverControllerTest.java
```

Test cases:

- `DRV-2001` returns `availabilityStatus = AVAILABLE`.
- `DRV-2001` returns `activeAssignmentCount = 2`.
- `DRV-9999` returns `404 DRIVER_NOT_FOUND`.
- Invalid driver ID format returns `400 INVALID_REQUEST`.

## Code To Implement

DTO:

```text
driver/api/dto/DriverResponse.java
```

Service/controller:

```text
driver/service/DriverService.java
driver/service/DriverResponseMapper.java
driver/api/DriverController.java
```

## Commands To Run

```powershell
.\mvnw.cmd -Dtest=DriverServiceTest,DriverControllerTest test
.\mvnw.cmd test
```

Manual check:

```powershell
Invoke-RestMethod http://localhost:8080/api/v1/drivers/DRV-2001
```

## Done Criteria

- [ ] Success and missing-driver tests pass.
- [ ] `activeAssignmentCount` counts active assignments only.
- [ ] Error envelope is reused.

## Stop / Do Not Add

- Do not add driver creation or update endpoints.
- Do not add authentication.

