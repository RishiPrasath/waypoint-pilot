# Partner Source Phase 2 Implementation Lane

`partner-source` is the completed Slice 1 Phase 2 implementation lane for Waypoint.

It is a synthetic logistics partner API that gives Waypoint operational data for customer-service questions such as:

- Where is my order?
- When will it arrive?
- Who is delivering it?
- What happened to my shipment?
- Can the assigned driver mark this order as delivered?

This lane proves the Phase 2 contract boundary before the BFF, chatbot frontend for customer service agents, and delivery app frontend for delivery drivers depend on it.

## Current Status

| Area | Status |
|------|--------|
| Shared Slice 1 contract | Complete; frozen locally in `docs/contracts/` and summarized in `AGREED_SPEC.md`. |
| Spring Boot reference implementation | Complete and tested. |
| FastAPI parity implementation | Complete and tested against the same behavior. |
| Local parity harness | Complete; latest report: 24 passed, 0 failed, 0 skipped. |
| Next product layer | BFF integration that consumes Partner Source and RAG services through contracts for the customer-service chatbot frontend and delivery-driver app frontend. |

## Folder Layout

```text
partner-source/
|-- README.md
|-- AGREED_SPEC.md
|-- MANUAL_BUILD_SEQUENCE.md
|-- CONTRACT_SYNC.md
|-- AGENTS.md
|-- .agents/
|-- docs/
|-- parity/
|-- partner-source-springboot/
`-- partner-source-fastapi/
```

## Source Of Truth

The local `docs/` folder and `AGREED_SPEC.md` are the source of truth for this implementation lane.

Read these first:

```text
docs\00-index.md
docs\active\contract-handoff.md
docs\active\data-and-seed-handoff.md
docs\active\test-and-acceptance-handoff.md
docs\contracts\openapi\partner-source.v1.yaml
docs\contracts\shared-error-contract.md
AGREED_SPEC.md
```

Some `docs/support`, `docs/research`, and `docs/archive` files preserve older context. When there is a conflict, follow `AGREED_SPEC.md`, `docs/active`, and `docs/contracts`.

## Implementation Folders

| Folder | Purpose | Status |
|---|---|---|
| `partner-source-springboot/` | Spring Boot reference implementation for Partner Source Slice 1. | Implemented and tested. |
| `partner-source-fastapi/` | FastAPI implementation that proves parity against the same contract behavior. | Implemented and tested. |
| `parity/` | Shared checks comparing Spring Boot and FastAPI responses. | Implemented; latest report passes 24/24 scenarios. |

## Contract Boundary

Both implementations expose the same Slice 1 API:

| Method | Path |
|---|---|
| `GET` | `/health` |
| `GET` | `/ready` |
| `GET` | `/api/v1/orders/{orderId}/status` |
| `GET` | `/api/v1/orders/{orderId}/timeline` |
| `GET` | `/api/v1/drivers/{driverId}` |
| `GET` | `/api/v1/drivers/{driverId}/assignments` |
| `POST` | `/api/v1/orders/{orderId}/status-events` |

Errors use the shared `ProblemDetail`-style envelope with `errorCode` and `correlationId`.

## Verification

```powershell
# Spring Boot
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test

# FastAPI
cd ..\partner-source-fastapi
uv run pytest

# Parity harness tests
cd ..\parity
python -m pytest
```

To generate a live parity report:

```powershell
# Terminal 1
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd spring-boot:run

# Terminal 2
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000

# Terminal 3
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\parity
python -m parity_runner
```

## Rules

- Keep Spring Boot and FastAPI separate.
- Keep the contract shared.
- Fix implementation drift in the implementation, not by weakening parity checks.
- Do not add databases, authentication, deployment, Docker, or framework extras in Slice 1 unless the plan changes deliberately.
- Use `.agents/` personas for command help, debugging, review, contract stewardship, TDD coaching, and CI checks.
