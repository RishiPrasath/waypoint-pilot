# 04 - Contract Steward

## Role

Protect the shared API contract, seed data, status lifecycle, and error envelope.

## Canonical Local Files

```text
docs/active/contract-handoff.md
docs/active/data-and-seed-handoff.md
docs/active/test-and-acceptance-handoff.md
docs/contracts/openapi/partner-source.v1.yaml
docs/contracts/shared-error-contract.md
AGREED_SPEC.md
```

## Decisions To Preserve

- Endpoints are exactly the Slice 1 endpoints.
- IDs remain deterministic: `ORD-*`, `DRV-*`, `ASN-*`, `EVT-*`.
- Errors use the shared ProblemDetail-style envelope.
- `correlationId` is the request trace field.
- `DELIVERY_ATTEMPTED` is an enum value but does not add Slice 1 delivery-attempt behavior.
- In-memory repositories are the only Slice 1 persistence.

## Do Not

- Invent fields, endpoints, statuses, or seed records.
- Rename error codes.
- Treat FastAPI's generated OpenAPI as canonical.

