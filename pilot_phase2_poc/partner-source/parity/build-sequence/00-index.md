# Parity Build Sequence

This build book is for shared checks after Spring Boot and FastAPI both expose meaningful Slice 1 behavior.

Do not start parity scripts before both implementations pass their own final gates.

## Read First

```text
..\..\AGREED_SPEC.md
..\..\CONTRACT_SYNC.md
..\..\docs\contracts\openapi\partner-source.v1.yaml
..\..\docs\contracts\shared-error-contract.md
..\..\docs\contracts\openapi\http\partner-source-slice1.http
..\..\partner-source-springboot\build-sequence\17-springboot-final-gate.md
..\..\partner-source-fastapi\build-sequence\17-fastapi-final-gate.md
```

## Build Order

| Step | Task | Outcome |
|---:|---|---|
| 01 | [Contract source check](01-contract-source-check.md) | Local contract inputs are present and known. |
| 02 | [Manual request matrix](02-manual-request-matrix.md) | Shared request scenarios are listed once. |
| 03 | [Spring Boot vs FastAPI response checks](03-springboot-vs-fastapi-response-checks.md) | Success response parity is checked. |
| 04 | [Error contract checks](04-error-contract-checks.md) | ProblemDetail parity is checked. |
| 05 | [Parity final gate](05-parity-final-gate.md) | Both implementations are accepted as contract-equivalent. |

## Default Local URLs

| Implementation | URL |
|---|---|
| Spring Boot | `http://localhost:8080` |
| FastAPI | `http://localhost:8000` |

## Stop Rules

- Do not create parity checks before both apps expose enough behavior.
- Do not make the parity layer invent contract behavior.
- Do not hide implementation drift by loosening checks.
