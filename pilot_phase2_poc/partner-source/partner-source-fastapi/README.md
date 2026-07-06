# Partner Source FastAPI

FastAPI is the contract-parity implementation for Waypoint Phase 2 Partner Source.

It proves that the same operational logistics API behavior can be implemented independently in Python while staying aligned with the Spring Boot reference implementation and shared OpenAPI contract.

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
| Python | 3.12 or newer |
| Framework | FastAPI |
| Server | `uvicorn` |
| Tests | pytest, httpx, FastAPI `TestClient` |
| Dependency manager | `uv` |
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
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
uv run pytest
```

Run the service locally:

```powershell
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Default local URL:

```text
http://localhost:8000
```

## Build Book

The numbered build sequence records the implementation path and verification history:

```text
build-sequence\00-index.md
```

Task 17 is the final gate for this implementation.

## Guardrails

- Do not add SQLAlchemy, Alembic, background workers, authentication packages, Docker, deployment config, or OpenAPI server generation for Slice 1.
- Do not treat FastAPI's generated OpenAPI output as the source of truth.
- If FastAPI and Spring Boot drift, fix the implementation that drifted from the contract or reference behavior.
