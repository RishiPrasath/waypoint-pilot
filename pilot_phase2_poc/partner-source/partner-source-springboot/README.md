# Partner Source Spring Boot

Spring Boot is the reference implementation for Waypoint Phase 2 Partner Source.

It proves the Slice 1 operational logistics contract in Java before later layers, such as the BFF, depend on the service.

## Current Status

| Area | Status |
|------|--------|
| Project scaffold | Complete. |
| Domain policies | Implemented and tested. |
| In-memory seed store and repositories | Implemented and tested. |
| Health and readiness endpoints | Implemented and tested. |
| Order and driver read endpoints | Implemented and tested. |
| Status event write endpoint | Implemented and tested. |
| Shared error envelope | Implemented and tested. |
| Integration and final gate | Complete. |

## Stack

| Area | Choice |
|---|---|
| Java | 21 |
| Build | Maven with Maven Wrapper |
| Package | `com.waypoint.partnersource` |
| Dependencies | Spring Web, Spring Validation, Spring Boot Test |
| Persistence | In-memory repositories only |
| Health | Custom `/health` and `/ready` |

## Contract Scope

The implementation follows the shared Partner Source Slice 1 contract:

```text
..\docs\contracts\openapi\partner-source.v1.yaml
..\docs\contracts\shared-error-contract.md
..\AGREED_SPEC.md
```

It exposes:

```text
GET  /health
GET  /ready
GET  /api/v1/orders/{orderId}/status
GET  /api/v1/orders/{orderId}/timeline
GET  /api/v1/drivers/{driverId}
GET  /api/v1/drivers/{driverId}/assignments
POST /api/v1/orders/{orderId}/status-events
```

## Verification

Run from this folder:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test
```

Run the service locally:

```powershell
.\mvnw.cmd spring-boot:run
```

Default local URL:

```text
http://localhost:8080
```

## Build Book

The numbered build sequence records the implementation path and verification history:

```text
build-sequence\00-index.md
```

Task 17 is the final gate for this implementation.

## Guardrails

- Do not add JPA, H2, PostgreSQL, Spring Security, Actuator, Docker, deployment config, or OpenAPI server generation for Slice 1.
- Do not let Spring Boot redefine the shared contract.
- If Spring Boot and FastAPI drift, fix the implementation that drifted from the contract or reference behavior.
