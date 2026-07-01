# Partner Source Parity Checks

This folder is reserved for future checks that compare the Spring Boot and FastAPI implementations against the same contract.

Do not add parity scripts yet.

Start here only after both implementations have meaningful endpoint behavior.

Use the numbered parity build book when that time comes:

```text
build-sequence\00-index.md
```

## Future Purpose

The parity checks should eventually:

- start or target Spring Boot on one base URL
- start or target FastAPI on another base URL
- run the same request matrix against both
- compare HTTP status codes
- compare required JSON fields
- compare enum values
- compare error envelope shape
- compare `errorCode`
- compare health and readiness behavior

## Future Inputs

Use these canonical sources:

```text
..\docs\contracts\openapi\partner-source.v1.yaml
..\docs\contracts\openapi\http\partner-source-slice1.http
..\docs\contracts\shared-error-contract.md
```

## Stop Rule

Do not claim FastAPI parity until the same manual checklist passes against both implementations.
