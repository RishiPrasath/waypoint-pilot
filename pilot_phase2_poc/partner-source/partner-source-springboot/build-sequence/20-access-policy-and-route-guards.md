# 20 - Access Policy And Route Guards

## Status

- Status: Done
- Last Updated: 2026-07-06

## Goal

Protect Spring Boot `/api/v1/**` routes with the local access-control matrix.

## Tests First

```powershell
.\mvnw.cmd "-Dtest=AuthAccessIntegrationTest" test
```

Expected coverage:

- missing token -> `401 UNAUTHENTICATED`
- invalid token -> `401 UNAUTHENTICATED`
- driver reads own resources -> `200`
- driver reads another driver's resources -> `403 ACCESS_DENIED`
- driver reads unassigned order -> `403 ACCESS_DENIED`
- CSA can read order status/timeline
- CSA cannot create driver status events

## Implementation Files

```text
src/main/java/com/waypoint/partnersource/shared/security/AuthenticationFilter.java
src/main/java/com/waypoint/partnersource/shared/security/SecurityFilterConfig.java
src/main/java/com/waypoint/partnersource/shared/security/AccessPolicy.java
src/main/java/com/waypoint/partnersource/shared/security/CurrentPrincipal.java
```

## Done Criteria

- [x] Protected routes require a valid bearer token.
- [x] Access denials use shared ProblemDetail.
- [x] `/health` and `/ready` remain public.

