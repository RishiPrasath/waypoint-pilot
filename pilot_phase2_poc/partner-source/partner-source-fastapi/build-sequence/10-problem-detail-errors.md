# 10 - ProblemDetail Errors

## Purpose

Centralize the shared ProblemDetail-style error envelope in FastAPI.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `9. Error Shape`
- `../../docs/contracts/shared-error-contract.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/10-problem-detail-errors.md`

## Tests To Write First

Create:

```text
tests/api/test_error_contract.py
tests/contract/test_problem_detail_shape.py
```

Test cases:

- Missing order returns `404`.
- Response media type is `application/problem+json`.
- Body includes `type`, `title`, `status`, `detail`, `instance`, `errorCode`, and `correlationId`.
- `errorCode = ORDER_NOT_FOUND` for `ORD-9999`.
- Invalid path ID returns `400 INVALID_REQUEST`.
- Deprecated code `ORDER_TRANSITION_INVALID` never appears.

## Code To Implement

Create:

```text
app/errors/exceptions.py
app/errors/handlers.py
app/schemas/errors.py
```

Update:

```text
app/main.py
```

Register exception handlers in `create_app()`.

Error handler output must match the shared contract exactly.

## Commands To Run

```powershell
python -m pytest tests/api/test_error_contract.py tests/contract/test_problem_detail_shape.py
python -m pytest
```

Manual missing-order check:

```powershell
try {
  Invoke-RestMethod http://localhost:8000/api/v1/orders/ORD-9999/status
} catch {
  $_.ErrorDetails.Message
}
```

## Done Criteria

- [ ] All error responses include required fields.
- [ ] HTTP status matches body `status`.
- [ ] `correlationId` is present.
- [ ] `application/problem+json` is used for API errors.
- [ ] FastAPI validation errors map to `400 INVALID_REQUEST`.

## Stop / Do Not Add

- Do not expose stack traces.
- Do not rename `correlationId` to `requestId`.

