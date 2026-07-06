# 18 - Auth Contract Update

## Status

- Status: Done
- Last Updated: 2026-07-06

## Goal

Update the Partner Source contract expectations for the auth/access-control slice before relying on protected routes.

## Source Docs

```text
../../docs/active/auth-access-control-plan.md
../../docs/contracts/openapi/partner-source.v1.yaml
../../docs/contracts/shared-error-contract.md
```

## Tests First

Add or update tests that expect:

- `401 UNAUTHENTICATED` for missing or invalid bearer token.
- `403 ACCESS_DENIED` for authenticated callers without route/resource access.
- `403 ORDER_NOT_ASSIGNED_TO_DRIVER` remains the domain denial for unassigned driver status-event writes.

## Implementation Notes

- Add a demo-only `POST /api/v1/auth/demo-login` route.
- Keep `/health` and `/ready` public for this slice.
- Keep Spring Security out of this slice unless deliberately accepted later.

## Done Criteria

- [x] Spring Boot exposes the new error codes.
- [x] Demo login returns deterministic bearer tokens.
- [x] Protected routes use the access-control matrix.
- [x] Existing Slice 1 behavior remains green with auth headers.

