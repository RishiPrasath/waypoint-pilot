# 15 - Integration Tests

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Prove the Spring Boot application works through the full stack, not only isolated services and controllers.

## Source Docs To Read

- `../../docs/active/test-and-acceptance-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../docs/contracts/shared-error-contract.md`

## Prereqs

- Tasks 01 through 14 are complete.
- ProblemDetail errors are centralized.
- Tests use in-memory seed data only.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `src/test/java/com/waypoint/partnersource/integration/PartnerSourceIntegrationTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/integration/PartnerSourceIntegrationTest.java
```

Use this integration test skeleton:

**Test Block Explanation**

- What this block does: Shows the test code to write first for Use this integration test skeleton.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
package com.waypoint.partnersource.integration;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class PartnerSourceIntegrationTest {

    @Autowired
    MockMvc mockMvc;

    @Test
    void slice1HappyPathWorksThroughHttp() throws Exception {
        mockMvc.perform(get("/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));

        mockMvc.perform(get("/ready"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("READY"));

        mockMvc.perform(get("/api/v1/orders/ORD-1001/status"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.currentStatus").value("OUT_FOR_DELIVERY"));

        mockMvc.perform(post("/api/v1/orders/ORD-1001/status-events")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"driverId\":\"DRV-2001\",\"status\":\"DELIVERED\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.orderCurrentStatus").value("DELIVERED"));
    }
}

```
## File Map

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `src/test/java/com/waypoint/partnersource/integration/PartnerSourceIntegrationTest.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
src/test/java/com/waypoint/partnersource/integration/PartnerSourceIntegrationTest.java
```

Optional helper:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `src/test/java/com/waypoint/partnersource/integration/JsonAssertions.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
src/test/java/com/waypoint/partnersource/integration/JsonAssertions.java
```

## Exact Code

Create integration test skeleton:

**Code Block Explanation**

- What this block does: Shows the exact Java code for Create integration test skeleton.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
@SpringBootTest
@AutoConfigureMockMvc
class PartnerSourceIntegrationTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    void slice1HappyPathWorksThroughHttp() throws Exception {
        mockMvc.perform(get("/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));

        mockMvc.perform(get("/ready"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("READY"));

        mockMvc.perform(get("/api/v1/orders/ORD-1001/status"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.currentStatus").value("OUT_FOR_DELIVERY"));

        mockMvc.perform(post("/api/v1/orders/ORD-1001/status-events")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"driverId\":\"DRV-2001\",\"status\":\"DELIVERED\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.orderCurrentStatus").value("DELIVERED"));
    }
}

```

Add imports for `MockMvc`, `SpringBootTest`, `AutoConfigureMockMvc`, `MediaType`, `get`, `post`, `status`, and `jsonPath`.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd "-Dtest=PartnerSourceIntegrationTest" test
.\mvnw.cmd test
```

If verify is configured later:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for If verify is configured later.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd verify
```

## Done Criteria

- [x] Main happy path works through HTTP.
- [x] A representative error path returns ProblemDetail.
- [x] Full module tests pass.

## Common Mistakes

- Repeating every controller unit test inside integration tests.
- Starting external services.
- Adding Testcontainers or databases for Slice 1.

## Stop / Do Not Add

- Do not start external services.
- Do not add Testcontainers or databases.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized and exact integration test skeleton added.
- Corrected the `AutoConfigureMockMvc` import for Spring Boot 4 and marked done after focused and full Maven tests passed.
