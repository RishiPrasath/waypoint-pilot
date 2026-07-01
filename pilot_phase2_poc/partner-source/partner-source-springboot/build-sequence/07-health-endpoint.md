# 07 - Health Endpoint

## Purpose

Implement the first tiny HTTP endpoint: `GET /health`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `3. Endpoints` and `8. Response Shapes`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Tests To Write First

Create:

```text
src/test/java/com/waypoint/partnersource/shared/health/HealthControllerTest.java
```

Test with MockMvc:

- `GET /health` returns `200`.
- Body includes `status = UP`.
- Body includes `service = partner-source`.

## Code To Implement

Create:

```text
src/main/java/com/waypoint/partnersource/shared/health/HealthController.java
src/main/java/com/waypoint/partnersource/shared/health/HealthResponse.java
```

Response shape:

```json
{
  "status": "UP",
  "service": "partner-source"
}
```

## Commands To Run

```powershell
.\mvnw.cmd -Dtest=HealthControllerTest test
.\mvnw.cmd test
```

Optional manual check after running the app:

```powershell
.\mvnw.cmd spring-boot:run
Invoke-RestMethod http://localhost:8080/health
```

## Done Criteria

- [ ] MockMvc test passes.
- [ ] Endpoint is outside `/api/v1`.
- [ ] Response fields match OpenAPI.

## Stop / Do Not Add

- Do not add Spring Boot Actuator.
- Do not add readiness logic here.

