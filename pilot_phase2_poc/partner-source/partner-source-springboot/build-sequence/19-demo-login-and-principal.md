# 19 - Demo Login And Principal

## Status

- Status: Done
- Last Updated: 2026-07-06

## Goal

Add a deterministic demo login flow and request principal model for Spring Boot.

## Tests First

```powershell
.\mvnw.cmd "-Dtest=AuthAccessIntegrationTest" test
```

Expected coverage:

- driver login returns `demo-driver-2001-token`
- CSA login returns `demo-csa-5001-token`
- unknown driver login returns `DRIVER_NOT_FOUND`
- protected routes reject missing/invalid tokens

## Implementation Files

```text
src/main/java/com/waypoint/partnersource/shared/security/AuthController.java
src/main/java/com/waypoint/partnersource/shared/security/DemoLoginService.java
src/main/java/com/waypoint/partnersource/shared/security/DemoTokenAuthenticator.java
src/main/java/com/waypoint/partnersource/shared/security/AuthenticatedPrincipal.java
src/main/java/com/waypoint/partnersource/shared/security/dto/DemoLoginRequest.java
src/main/java/com/waypoint/partnersource/shared/security/dto/DemoLoginResponse.java
```

## Done Criteria

- [x] Demo login is public.
- [x] Login does not create server-side sessions.
- [x] Token maps to the same conceptual principal used by FastAPI.

