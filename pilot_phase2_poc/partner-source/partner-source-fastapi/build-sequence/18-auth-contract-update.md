# 18 - Auth Contract Update

## Status

- Status: Done
- Last Updated: 2026-07-06

## Goal

Mirror the accepted auth/access-control contract behavior from Spring Boot.

## Source Docs

```text
../../docs/active/auth-access-control-plan.md
../../partner-source-springboot/build-sequence/18-auth-contract-update.md
```

## Tests First

Add pytest coverage for:

- `401 UNAUTHENTICATED`
- `403 ACCESS_DENIED`
- demo login success and failure
- existing domain `ORDER_NOT_ASSIGNED_TO_DRIVER`

## Done Criteria

- [x] FastAPI error envelope matches Spring Boot.
- [x] Protected routes use the same access-control matrix.
- [x] Existing Slice 1 behavior remains green with auth headers.

