# FastAPI Build Sequence

This is the human build book for the FastAPI Partner Source parity implementation.

FastAPI must match the same local contract and the Spring Boot reference behavior. It must not become a second API design.

## Read First

```text
..\..\AGREED_SPEC.md
..\..\docs\00-index.md
..\..\docs\active\contract-handoff.md
..\..\docs\active\data-and-seed-handoff.md
..\..\docs\active\test-and-acceptance-handoff.md
..\..\docs\contracts\openapi\partner-source.v1.yaml
..\..\docs\contracts\shared-error-contract.md
..\..\partner-source-springboot\build-sequence\00-index.md
```

## Build Order

| Step | Task | Outcome |
|---:|---|---|
| 01 | [Project setup](01-project-setup.md) | FastAPI scaffold and first passing pytest. |
| 02 | [CI pipeline](02-ci-pipeline.md) | GitHub Actions runs pytest. |
| 03 | [Package layout](03-package-layout.md) | App modules are ready. |
| 04 | [Status transition policy](04-status-transition-policy.md) | Domain policy mirrors Spring Boot. |
| 05 | [Assignment authorization policy](05-assignment-authorization-policy.md) | Authorization rule mirrors Spring Boot. |
| 06 | [Seed store and repositories](06-seed-store-and-repositories.md) | Deterministic in-memory data layer exists. |
| 07 | [Health endpoint](07-health-endpoint.md) | `GET /health` returns `UP`. |
| 08 | [Readiness endpoint](08-readiness-endpoint.md) | `GET /ready` proves seed readiness. |
| 09 | [Order status lookup](09-order-status-lookup.md) | First contract read endpoint works. |
| 10 | [ProblemDetail errors](10-problem-detail-errors.md) | Shared error envelope is centralized. |
| 11 | [Order timeline](11-order-timeline.md) | Chronological timeline endpoint works. |
| 12 | [Driver profile](12-driver-profile.md) | Driver profile endpoint works. |
| 13 | [Driver assignments](13-driver-assignments.md) | Assignment list endpoint works. |
| 14 | [Create status event](14-create-status-event.md) | Write endpoint validates, appends, and mutates status. |
| 15 | [Integration tests](15-integration-tests.md) | Full FastAPI flow is verified. |
| 16 | [Manual HTTP checklist](16-manual-http-checklist.md) | Human request matrix passes locally. |
| 17 | [FastAPI final gate](17-fastapi-final-gate.md) | Implementation is ready for parity checks. |

## Per-Task Rule

```text
read source docs and Spring Boot behavior
-> write the failing pytest
-> run the focused pytest and confirm the failure
-> implement the smallest code
-> run focused pytest
-> run python -m pytest
-> update the tracker
```

## Default Commands

Run commands from:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
```

If using `uv`:

```powershell
uv run pytest
uv run uvicorn app.main:app --reload
```

If using a virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest
python -m uvicorn app.main:app --reload
```

## Stop Rules

- Do not add SQLAlchemy, Alembic, auth packages, background workers, Docker, deployment config, or OpenAPI server generation.
- Do not treat FastAPI's generated OpenAPI as canonical.
- Do not add behavior that Spring Boot and the agreed spec do not have.

