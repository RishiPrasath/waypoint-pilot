# 15 - Integration Tests

## Purpose

Prove the FastAPI app works through the full TestClient stack.

## Source Docs To Read

- `../../docs/active/test-and-acceptance-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/15-integration-tests.md`

## Tests To Write First

Create:

```text
tests/integration/test_partner_source_flow.py
```

Test flows:

- Health and readiness return `200`.
- Read `ORD-1001` status.
- Read `ORD-1001` timeline.
- Read `DRV-2001` profile.
- Read `DRV-2001` assignments.
- Post delivered status event for `ORD-1001`.
- Read status again and confirm current status is `DELIVERED`.
- Missing order returns shared ProblemDetail.

## Code To Implement

Only add test support if needed. The app behavior should already exist from prior steps.

Possible helper:

```text
tests/helpers/json_assertions.py
```

## Commands To Run

```powershell
python -m pytest tests/integration/test_partner_source_flow.py
python -m pytest
```

## Done Criteria

- [ ] Main happy path works through HTTP.
- [ ] Representative error path returns ProblemDetail.
- [ ] Full pytest suite passes.

## Stop / Do Not Add

- Do not start external services.
- Do not add databases.

