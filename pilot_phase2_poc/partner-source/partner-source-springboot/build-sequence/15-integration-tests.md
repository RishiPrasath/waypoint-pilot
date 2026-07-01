# 15 - Integration Tests

## Purpose

Prove the Spring Boot application works through the full stack, not only isolated services and controllers.

## Source Docs To Read

- `../../docs/active/test-and-acceptance-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../docs/contracts/shared-error-contract.md`

## Tests To Write First

Create:

```text
src/test/java/com/waypoint/partnersource/integration/PartnerSourceIntegrationTest.java
```

Use `@SpringBootTest` plus `MockMvc` or a random-port client.

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

Only add integration test support if needed. The app behavior should already exist from prior steps.

Possible test support:

```text
src/test/java/com/waypoint/partnersource/integration/JsonAssertions.java
```

## Commands To Run

```powershell
.\mvnw.cmd -Dtest=PartnerSourceIntegrationTest test
.\mvnw.cmd test
```

If integration tests are bound to verify later:

```powershell
.\mvnw.cmd verify
```

## Done Criteria

- [ ] Main happy path works through HTTP.
- [ ] A representative error path returns ProblemDetail.
- [ ] Full module tests pass.

## Stop / Do Not Add

- Do not start external services.
- Do not add Testcontainers or databases.

