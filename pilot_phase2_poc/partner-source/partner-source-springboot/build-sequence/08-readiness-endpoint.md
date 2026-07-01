# 08 - Readiness Endpoint

## Purpose

Implement `GET /ready` to prove in-memory persistence and seed data are ready.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `3. Endpoints` and `8. Response Shapes`
- `../../docs/active/data-and-seed-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Tests To Write First

Create:

```text
src/test/java/com/waypoint/partnersource/shared/health/ReadinessControllerTest.java
src/test/java/com/waypoint/partnersource/shared/health/ReadinessServiceTest.java
```

Test cases:

- Service reports ready when seed data has orders, drivers, assignments, and events.
- `GET /ready` returns `200`.
- Body includes `status = READY`, `service = partner-source`, `checks.persistence = UP`, and `checks.seedData = UP`.

## Code To Implement

Create:

```text
shared/health/ReadinessController.java
shared/health/ReadinessService.java
shared/health/ReadinessResponse.java
shared/health/ReadinessChecks.java
```

Use existing in-memory seed/repository wiring from step 06.

## Commands To Run

```powershell
.\mvnw.cmd -Dtest=ReadinessServiceTest,ReadinessControllerTest test
.\mvnw.cmd test
```

Manual check:

```powershell
Invoke-RestMethod http://localhost:8080/ready
```

## Done Criteria

- [ ] Readiness service tests pass.
- [ ] Controller test passes.
- [ ] Endpoint is outside `/api/v1`.
- [ ] No Actuator dependency exists.

## Stop / Do Not Add

- Do not add database readiness checks.
- Do not add Kubernetes probes or deployment config.

