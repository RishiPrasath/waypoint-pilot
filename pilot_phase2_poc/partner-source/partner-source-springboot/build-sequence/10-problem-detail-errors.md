# 10 - ProblemDetail Errors

## Purpose

Centralize the shared error envelope for all Spring Boot API errors.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `9. Error Shape`
- `../../docs/contracts/shared-error-contract.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Tests To Write First

Create:

```text
src/test/java/com/waypoint/partnersource/shared/error/ApiExceptionHandlerTest.java
src/test/java/com/waypoint/partnersource/order/api/OrderStatusErrorContractTest.java
```

Test cases:

- Missing order returns `404`.
- Response media type is compatible with `application/problem+json`.
- Body includes `type`, `title`, `status`, `detail`, `instance`, `errorCode`, and `correlationId`.
- `errorCode = ORDER_NOT_FOUND` for `ORD-9999`.
- Invalid path ID returns `400 INVALID_REQUEST`.
- Deprecated code `ORDER_TRANSITION_INVALID` never appears.

## Code To Implement

Create:

```text
shared/error/ErrorCode.java
shared/error/PartnerSourceException.java
shared/error/ApiExceptionHandler.java
shared/error/ProblemDetailFactory.java
shared/error/CorrelationIdFilter.java
```

Map validation exceptions, missing resources, authorization failures, invalid transitions, invalid semantic events, and unknown server errors to the approved codes.

## Commands To Run

```powershell
.\mvnw.cmd -Dtest=ApiExceptionHandlerTest,OrderStatusErrorContractTest test
.\mvnw.cmd test
```

Manual missing-order check:

```powershell
try {
  Invoke-RestMethod http://localhost:8080/api/v1/orders/ORD-9999/status
} catch {
  $_.ErrorDetails.Message
}
```

## Done Criteria

- [ ] Every error response has all required fields.
- [ ] `status` field matches the HTTP status.
- [ ] `correlationId` is always present.
- [ ] `application/problem+json` is used for API errors.
- [ ] Earlier temporary error handling is removed or routed through this handler.

## Stop / Do Not Add

- Do not expose stack traces.
- Do not rename `correlationId` to `requestId`.

