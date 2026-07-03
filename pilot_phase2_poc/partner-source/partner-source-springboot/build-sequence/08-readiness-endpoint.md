# 08 - Readiness Endpoint

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `GET /ready` to prove in-memory persistence and seed data are ready.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `3. Endpoints` and `8. Response Shapes`
- `../../docs/active/data-and-seed-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Prereqs

- Task 06 seed store exists.
- Task 07 health endpoint exists.
- Do not add Actuator.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `src/test/java/com/waypoint/partnersource/shared/health/ReadinessServiceTest.java`, `src/test/java/com/waypoint/partnersource/shared/health/ReadinessControllerTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/shared/health/ReadinessServiceTest.java
src/test/java/com/waypoint/partnersource/shared/health/ReadinessControllerTest.java
```

`ReadinessServiceTest.java`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `ReadinessServiceTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
package com.waypoint.partnersource.shared.health;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class ReadinessServiceTest {

    @Test
    void reportsReadyWhenSeedDataExists() {
        var service = new ReadinessService(SeedDataLoader.load());

        var response = service.check();

        assertEquals("READY", response.status());
        assertEquals("partner-source", response.service());
        assertEquals("UP", response.checks().persistence());
        assertEquals("UP", response.checks().seedData());
    }
}

```

`ReadinessControllerTest.java`:

**Test Block Explanation**

- What this block does: Shows the controller test code for `/ready`, including the ready and not-ready HTTP paths.
- Why it exists: It proves the HTTP endpoint returns the exact contract shape and uses `503` only when readiness is down.
- How to read it: The mocked service response controls the controller path; the assertions check HTTP status and JSON field names.

```java
package com.waypoint.partnersource.shared.health;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(ReadinessController.class)
class ReadinessControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    ReadinessService readinessService;

    @Test
    void readyReturnsReadyWhenSeedDataExists() throws Exception {
        when(readinessService.check())
                .thenReturn(new ReadinessResponse("READY", "partner-source", new ReadinessChecks("UP", "UP")));

        mockMvc.perform(get("/ready"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("READY"))
                .andExpect(jsonPath("$.service").value("partner-source"))
                .andExpect(jsonPath("$.checks.persistence").value("UP"))
                .andExpect(jsonPath("$.checks.seedData").value("UP"));
    }

    @Test
    void readyReturnsServiceUnavailableWhenSeedDataIsDown() throws Exception {
        when(readinessService.check())
                .thenReturn(new ReadinessResponse("NOT_READY", "partner-source", new ReadinessChecks("UP", "DOWN")));

        mockMvc.perform(get("/ready"))
                .andExpect(status().isServiceUnavailable())
                .andExpect(jsonPath("$.status").value("NOT_READY"))
                .andExpect(jsonPath("$.checks.seedData").value("DOWN"));
    }
}

```
## File Map

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `src/main/java/com/waypoint/partnersource/shared/health/ReadinessChecks.java`, `src/main/java/com/waypoint/partnersource/shared/health/ReadinessResponse.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
src/main/java/com/waypoint/partnersource/shared/health/ReadinessChecks.java
src/main/java/com/waypoint/partnersource/shared/health/ReadinessResponse.java
src/main/java/com/waypoint/partnersource/shared/health/ReadinessService.java
src/main/java/com/waypoint/partnersource/shared/health/ReadinessController.java

```

## Exact Code

Create `src/main/java/com/waypoint/partnersource/shared/health/ReadinessChecks.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `src/main/java/com/waypoint/partnersource/shared/health/ReadinessChecks.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.shared.health;

public record ReadinessChecks(String persistence, String seedData) {
}

```

Create `src/main/java/com/waypoint/partnersource/shared/health/ReadinessResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `src/main/java/com/waypoint/partnersource/shared/health/ReadinessResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Keep this as a separate file from `ReadinessChecks.java`; Java allows only one public top-level type per file.

```java
package com.waypoint.partnersource.shared.health;

public record ReadinessResponse(String status, String service, ReadinessChecks checks) {
}

```

Create `src/main/java/com/waypoint/partnersource/shared/health/ReadinessService.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `src/main/java/com/waypoint/partnersource/shared/health/ReadinessService.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.shared.health;

import com.waypoint.partnersource.shared.seed.SeedDataStore;
import org.springframework.stereotype.Service;

@Service
public class ReadinessService {
    private final SeedDataStore store;

    public ReadinessService(SeedDataStore store) {
        this.store = store;
    }

    public ReadinessResponse check() {
        boolean seedReady = !store.orders().isEmpty()
                && !store.drivers().isEmpty()
                && !store.assignments().isEmpty()
                && !store.statusEventsByOrderId().isEmpty();

        return new ReadinessResponse(
                seedReady ? "READY" : "NOT_READY",
                "partner-source",
                new ReadinessChecks("UP", seedReady ? "UP" : "DOWN")
        );
    }
}

```

Create `src/main/java/com/waypoint/partnersource/shared/health/ReadinessController.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `src/main/java/com/waypoint/partnersource/shared/health/ReadinessController.java`.
- Why it exists: It maps the readiness service result to the HTTP contract without adding Actuator or deployment-specific probes.
- How to read it: `READY` responses return `200`; any not-ready check returns `503` with the same response body shape.

```java
package com.waypoint.partnersource.shared.health;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReadinessController {
    private final ReadinessService readinessService;

    public ReadinessController(ReadinessService readinessService) {
        this.readinessService = readinessService;
    }

    @GetMapping("/ready")
    public ResponseEntity<ReadinessResponse> getReadiness() {
        ReadinessResponse response = readinessService.check();
        boolean ready = "UP".equals(response.checks().persistence())
                && "UP".equals(response.checks().seedData());

        if (ready) {
            return ResponseEntity.ok(response);
        }

        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(response);
    }
}

```

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd "-Dtest=ReadinessServiceTest,ReadinessControllerTest" test
.\mvnw.cmd test
```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `Invoke-RestMethod http://localhost:8080/ready`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod http://localhost:8080/ready
```

## Done Criteria

- [x] Readiness service tests pass.
- [x] Controller test passes.
- [x] Endpoint is outside `/api/v1`.
- [x] No Actuator dependency exists.

## Common Mistakes

- Returning top-level `UP` instead of `READY`.
- Using `seed_data` instead of `seedData`.
- Adding database readiness checks.

## Stop / Do Not Add

- Do not add database readiness checks.
- Do not add Kubernetes probes or deployment config.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized and exact readiness code direction added.
- Expanded Spring Boot implementation guidance with separate record files, exact controller code, and a Boot 4-compatible controller test using `@MockitoBean`.
- Marked done after focused readiness tests and the full Maven suite passed.
