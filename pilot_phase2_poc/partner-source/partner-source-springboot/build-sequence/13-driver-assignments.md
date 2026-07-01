# 13 - Driver Assignments

## Purpose

Implement `GET /api/v1/drivers/{driverId}/assignments`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `7. Seed Data`, `8. Response Shapes`, and `10. Acceptance Scenarios`
- `../../docs/active/data-and-seed-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Tests To Write First

Create:

```text
src/test/java/com/waypoint/partnersource/driver/service/DriverAssignmentServiceTest.java
src/test/java/com/waypoint/partnersource/driver/api/DriverAssignmentControllerTest.java
```

Test cases:

- `DRV-2001` returns two active assignment items.
- Items include `ORD-1001` and `ORD-1002`.
- `DRV-2003` returns empty `items` and `totalItems = 0`.
- Missing driver returns `404 DRIVER_NOT_FOUND`.
- Optional `status` filter accepts valid `OrderStatus` values.
- Invalid `status`, `page`, or `pageSize` returns `400 INVALID_REQUEST`.

## Code To Implement

DTOs:

```text
driver/api/dto/DriverAssignmentsResponse.java
driver/api/dto/DriverAssignmentItemResponse.java
```

Service/controller:

```text
driver/service/DriverAssignmentService.java
driver/api/DriverAssignmentController.java
```

Use order and assignment repositories to enrich assignment items.

## Commands To Run

```powershell
.\mvnw.cmd -Dtest=DriverAssignmentServiceTest,DriverAssignmentControllerTest test
.\mvnw.cmd test
```

Manual check:

```powershell
Invoke-RestMethod "http://localhost:8080/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20"
```

## Done Criteria

- [ ] Active assignment list is correct.
- [ ] Empty assignment list is represented as `items: []`.
- [ ] Pagination fields match OpenAPI.
- [ ] Missing driver and validation errors use ProblemDetail.

## Stop / Do Not Add

- Do not add assignment creation endpoints.
- Do not include completed `ASN-3003` as active work.

