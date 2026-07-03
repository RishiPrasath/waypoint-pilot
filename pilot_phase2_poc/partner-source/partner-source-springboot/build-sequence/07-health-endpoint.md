# 07 - Health Endpoint

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `GET /health` as a simple process liveness endpoint.

This is not Actuator. It is a small contract endpoint owned by the app.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `3. Endpoints` and `8. Response Shapes`
- `../../docs/active/contract-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Prereqs

- Spring Boot app starts.
- `shared/health` package exists.
- Do not add Actuator.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `src/test/java/com/waypoint/partnersource/shared/health/HealthControllerTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/shared/health/HealthControllerTest.java
```

Use this exact MockMvc test:

**Test Block Explanation**

- What this block does: Shows the test code to write first for Use this exact MockMvc test.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
package com.waypoint.partnersource.shared.health;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(HealthController.class)
class HealthControllerTest {

    @Autowired
    MockMvc mockMvc;

    @Test
    void healthReturnsUp() throws Exception {
        mockMvc.perform(get("/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"))
                .andExpect(jsonPath("$.service").value("partner-source"));
    }
}

```
## File Map

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `src/main/java/com/waypoint/partnersource/shared/health/HealthController.java`, `src/main/java/com/waypoint/partnersource/shared/health/HealthResponse.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
src/main/java/com/waypoint/partnersource/shared/health/HealthController.java
src/main/java/com/waypoint/partnersource/shared/health/HealthResponse.java
```

## Exact Code

Create `HealthResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `HealthResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.shared.health;

public record HealthResponse(String status, String service) {
}

```

Create `HealthController.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `HealthController.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.shared.health;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {
    @GetMapping("/health")
    public HealthResponse getHealth() {
        return new HealthResponse("UP", "partner-source");
    }
}

```

Expected JSON:

**Code Block Explanation**

- What this block does: Shows the exact JSON shape or response values for `{`, `"status": "UP",`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Use the field names and values as contract shape checks; spelling and casing matter.

```json
{
  "status": "UP",
  "service": "partner-source"
}

```

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd -Dtest=HealthControllerTest test
.\mvnw.cmd test

```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `Invoke-RestMethod http://localhost:8080/health`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod http://localhost:8080/health

```

## Done Criteria

- [x] MockMvc test passes.
- [x] Endpoint is outside `/api/v1`.
- [x] Response fields match OpenAPI.

## Common Mistakes

- Adding Spring Boot Actuator instead of a tiny controller.
- Returning `serviceName` instead of `service`.
- Putting health under `/api/v1`.

## Stop / Do Not Add

- Do not add Spring Boot Actuator.
- Do not add readiness logic here.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized and exact controller/response code added.
- Marked done after `HealthControllerTest` and the full Maven suite passed.
