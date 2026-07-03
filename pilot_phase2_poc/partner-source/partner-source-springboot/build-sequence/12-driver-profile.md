# 12 - Driver Profile

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `GET /api/v1/drivers/{driverId}`.

This returns a seeded driver profile and active assignment count.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `7. Seed Data`, `8. Response Shapes`, and `10. Acceptance Scenarios`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Prereqs

- Task 06 driver and assignment repositories exist.
- Task 10 error handling exists.
- Driver ID validation uses `^DRV-[0-9]{4}$`.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `src/test/java/com/waypoint/partnersource/driver/service/DriverServiceTest.java`, `src/test/java/com/waypoint/partnersource/driver/api/DriverControllerTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/driver/service/DriverServiceTest.java
src/test/java/com/waypoint/partnersource/driver/api/DriverControllerTest.java
```

`DriverServiceTest.java` core test:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `DriverServiceTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
@Test
void returnsDriverProfileWithActiveAssignmentCount() {
    var store = SeedDataLoader.load();
    var service = new DriverService(
            new InMemoryDriverRepository(store),
            new InMemoryAssignmentRepository(store),
            new DriverResponseMapper()
    );

    var response = service.getDriver("DRV-2001");

    assertEquals("DRV-2001", response.driverId());
    assertEquals("A. Kumar", response.displayName());
    assertEquals(DriverAvailabilityStatus.AVAILABLE, response.availabilityStatus());
    assertEquals(2, response.activeAssignmentCount());
}

```

`DriverControllerTest.java` should assert:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `DriverControllerTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
mockMvc.perform(get("/api/v1/drivers/DRV-2001"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.driverId").value("DRV-2001"))
        .andExpect(jsonPath("$.availabilityStatus").value("AVAILABLE"))
        .andExpect(jsonPath("$.activeAssignmentCount").value(2));

```

Also add a missing-driver test for `DRV-9999 -> 404 DRIVER_NOT_FOUND`.
## File Map

DTO:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `driver/api/dto/DriverResponse.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
driver/api/dto/DriverResponse.java
```

Service/controller:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `driver/service/DriverResponseMapper.java`, `driver/service/DriverService.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
driver/service/DriverResponseMapper.java
driver/service/DriverService.java
driver/api/DriverController.java
```

## Exact Code

Create `DriverResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `DriverResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.driver.api.dto;

import com.waypoint.partnersource.driver.domain.DriverAvailabilityStatus;

public record DriverResponse(
        String driverId,
        String displayName,
        DriverAvailabilityStatus availabilityStatus,
        int activeAssignmentCount
) {
}

```

Create `DriverService.java` to load the driver, count active assignments only, and throw `DRIVER_NOT_FOUND` for missing IDs.

Create `DriverController.java` with:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for `DriverController.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
GET /api/v1/drivers/{driverId}
```

Use `@Pattern(regexp = "^DRV-[0-9]{4}$")` on `driverId`.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd "-Dtest=DriverServiceTest,DriverControllerTest" test
.\mvnw.cmd test
```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `Invoke-RestMethod http://localhost:8080/api/v1/drivers/DRV-2001`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod http://localhost:8080/api/v1/drivers/DRV-2001
```

## Done Criteria

- [x] Success and missing-driver tests pass.
- [x] `activeAssignmentCount` counts active assignments only.
- [x] Error envelope is reused.

## Common Mistakes

- Counting completed `ASN-3003` as active work.
- Returning `availability_status` instead of `availabilityStatus`.
- Adding driver create/update endpoints.

## Stop / Do Not Add

- Do not add driver creation or update endpoints.
- Do not add authentication.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized and exact driver profile DTO/service/controller guidance added.
- Implemented and marked done after focused tests and the full Maven suite passed.
