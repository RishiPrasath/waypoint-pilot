# 04 - Error Contract Checks

## Purpose

Compare error response behavior from both implementations.

## Source Docs To Read

- `../../docs/contracts/shared-error-contract.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `02-manual-request-matrix.md`

## Tests To Write First

Future automated parity test:

```text
parity/tests/test_error_response_parity.py
```

Test checks:

- HTTP status matches expected.
- Body `status` matches HTTP status.
- Required fields exist: `type`, `title`, `status`, `detail`, `instance`, `errorCode`, `correlationId`.
- `errorCode` matches expected.
- Deprecated `ORDER_TRANSITION_INVALID` never appears.
- `correlationId` is present but not necessarily identical between implementations.

## Code To Implement

Future helper:

```text
parity/scripts/error_assertions.py
```

## Commands To Run

Manual missing-order comparison:

```powershell
try {
  Invoke-RestMethod http://localhost:8080/api/v1/orders/ORD-9999/status
} catch {
  $springError = $_.ErrorDetails.Message | ConvertFrom-Json
}

try {
  Invoke-RestMethod http://localhost:8000/api/v1/orders/ORD-9999/status
} catch {
  $fastapiError = $_.ErrorDetails.Message | ConvertFrom-Json
}

$springError.errorCode
$fastapiError.errorCode
```

## Done Criteria

- [ ] All approved error codes are covered by tests or manual checks.
- [ ] Both implementations return the shared ProblemDetail shape.
- [ ] Validation maps to `400 INVALID_REQUEST`.
- [ ] Domain transition conflicts map to `409 INVALID_STATUS_TRANSITION`.
- [ ] Semantic status-event failures map to `422 INVALID_STATUS_EVENT`.

## Stop / Do Not Add

- Do not accept framework-default error shapes.
- Do not expose stack traces.
