# 10 - ProblemDetail Errors

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Centralize the shared error envelope for all Spring Boot API errors.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `9. Error Shape`
- `../../docs/contracts/shared-error-contract.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Prereqs

- At least one endpoint exists to prove error behavior.
- Do not expose stack traces.
- Use `correlationId`, not `requestId`.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `src/test/java/com/waypoint/partnersource/shared/error/ApiExceptionHandlerTest.java`, `src/test/java/com/waypoint/partnersource/order/api/OrderStatusErrorContractTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/shared/error/ApiExceptionHandlerTest.java
src/test/java/com/waypoint/partnersource/order/api/OrderStatusErrorContractTest.java
```

`OrderStatusErrorContractTest.java` MockMvc assertions:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `OrderStatusErrorContractTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
mockMvc.perform(get("/api/v1/orders/ORD-9999/status"))
        .andExpect(status().isNotFound())
        .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
        .andExpect(jsonPath("$.type").exists())
        .andExpect(jsonPath("$.title").value("Order not found"))
        .andExpect(jsonPath("$.status").value(404))
        .andExpect(jsonPath("$.detail").exists())
        .andExpect(jsonPath("$.instance").value("/api/v1/orders/ORD-9999/status"))
        .andExpect(jsonPath("$.errorCode").value("ORDER_NOT_FOUND"))
        .andExpect(jsonPath("$.correlationId").exists());

```

`ApiExceptionHandlerTest.java` should also include invalid request coverage:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `ApiExceptionHandlerTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
mockMvc.perform(get("/api/v1/orders/INVALID/status"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.errorCode").value("INVALID_REQUEST"));

```

Add this guard to either test file:

**Test Block Explanation**

- What this block does: Shows the test code to write first for Add this guard to either test file.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
mockMvc.perform(get("/api/v1/orders/ORD-9999/status"))
        .andExpect(result -> org.assertj.core.api.Assertions.assertThat(result.getResponse().getContentAsString())
                .doesNotContain("ORDER_TRANSITION_INVALID"));

```
## File Map

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `shared/error/ErrorCode.java`, `shared/error/PartnerSourceException.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
shared/error/ErrorCode.java
shared/error/PartnerSourceException.java
shared/error/ProblemDetailResponse.java
shared/error/ProblemDetailFactory.java
shared/error/CorrelationIdFilter.java
shared/error/ApiExceptionHandler.java

```

## Exact Code

Create `ErrorCode.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `ErrorCode.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.shared.error;

public enum ErrorCode {
    INVALID_REQUEST,
    ORDER_NOT_FOUND,
    DRIVER_NOT_FOUND,
    ASSIGNMENT_NOT_FOUND,
    ORDER_NOT_ASSIGNED_TO_DRIVER,
    INVALID_STATUS_TRANSITION,
    INVALID_STATUS_EVENT,
    INTERNAL_SERVER_ERROR
}

```

Create `ProblemDetailResponse.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `ProblemDetailResponse.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.shared.error;

public record ProblemDetailResponse(
        String type,
        String title,
        int status,
        String detail,
        String instance,
        ErrorCode errorCode,
        String correlationId
) {
}

```

Create `PartnerSourceException.java` with factory methods for `orderNotFound`, `driverNotFound`, `orderNotAssignedToDriver`, `invalidStatusTransition`, and `invalidStatusEvent`.

Minimum shape:

**Code Block Explanation**

- What this block does: Shows the exact Java code for Minimum shape.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
public class PartnerSourceException extends RuntimeException {
    private final HttpStatus status;
    private final ErrorCode errorCode;
    private final String title;

    public PartnerSourceException(HttpStatus status, ErrorCode errorCode, String title, String detail) {
        super(detail);
        this.status = status;
        this.errorCode = errorCode;
        this.title = title;
    }

    public static PartnerSourceException orderNotFound(String orderId) {
        return new PartnerSourceException(HttpStatus.NOT_FOUND, ErrorCode.ORDER_NOT_FOUND,
                "Order not found", "No order exists for orderId " + orderId + ".");
    }

    public HttpStatus status() { return status; }
    public ErrorCode errorCode() { return errorCode; }
    public String title() { return title; }
}

```

Create `ApiExceptionHandler.java` with `@RestControllerAdvice`, an `@ExceptionHandler(PartnerSourceException.class)`, validation exception handling, and `MediaType.APPLICATION_PROBLEM_JSON`.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd "-Dtest=ApiExceptionHandlerTest,OrderStatusErrorContractTest" test
.\mvnw.cmd test
```

Manual missing-order check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Manual missing-order check.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
try {
  Invoke-RestMethod http://localhost:8080/api/v1/orders/ORD-9999/status
} catch {
  $_.ErrorDetails.Message
}

```

## Done Criteria

- [x] Every error response has all required fields.
- [x] `status` field matches the HTTP status.
- [x] `correlationId` is always present.
- [x] `application/problem+json` is used for API errors.
- [x] Earlier temporary error handling is removed or routed through this handler.

## Common Mistakes

- Returning Spring's default error body.
- Using `requestId` instead of `correlationId`.
- Returning deprecated `ORDER_TRANSITION_INVALID`.
- Exposing stack traces.

## Stop / Do Not Add

- Do not expose stack traces.
- Do not rename `correlationId` to `requestId`.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized and exact shared error file map/code guidance added.
- Corrected the focused Maven test command so the comma-separated `-Dtest` value is quoted for PowerShell.
- Implemented Spring Boot ProblemDetail handling and marked done after focused and full Maven tests passed.
