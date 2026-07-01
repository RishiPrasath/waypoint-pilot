# Spring Boot Build Sequence

This is the human build book for the Spring Boot Partner Source reference implementation.

Build the app by hand, test first, and keep every step aligned with the local source of truth.

## Read First

```text
..\..\AGREED_SPEC.md
..\..\docs\00-index.md
..\..\docs\active\contract-handoff.md
..\..\docs\active\data-and-seed-handoff.md
..\..\docs\active\test-and-acceptance-handoff.md
..\..\docs\contracts\openapi\partner-source.v1.yaml
..\..\docs\contracts\shared-error-contract.md
```

## Build Order

| Step | Task | Outcome |
|---:|---|---|
| 01 | [Project setup](01-project-setup.md) | Spring Boot scaffold and first passing test. |
| 02 | [CI pipeline](02-ci-pipeline.md) | GitHub Actions runs the module tests. |
| 03 | [Package layout](03-package-layout.md) | Feature-based package structure is ready. |
| 04 | [Status transition policy](04-status-transition-policy.md) | First real domain rule is TDD-built. |
| 05 | [Assignment authorization policy](05-assignment-authorization-policy.md) | Driver/order authorization rule is TDD-built. |
| 06 | [Seed store and repositories](06-seed-store-and-repositories.md) | Deterministic in-memory data layer exists. |
| 07 | [Health endpoint](07-health-endpoint.md) | `GET /health` returns `UP`. |
| 08 | [Readiness endpoint](08-readiness-endpoint.md) | `GET /ready` proves seed readiness. |
| 09 | [Order status lookup](09-order-status-lookup.md) | First contract read endpoint works. |
| 10 | [ProblemDetail errors](10-problem-detail-errors.md) | Shared error envelope is centralized. |
| 11 | [Order timeline](11-order-timeline.md) | Chronological timeline endpoint works. |
| 12 | [Driver profile](12-driver-profile.md) | Driver profile endpoint works. |
| 13 | [Driver assignments](13-driver-assignments.md) | Assignment list endpoint works. |
| 14 | [Create status event](14-create-status-event.md) | Write endpoint validates, appends, and mutates status. |
| 15 | [Integration tests](15-integration-tests.md) | Full Spring Boot flow is verified. |
| 16 | [Manual HTTP checklist](16-manual-http-checklist.md) | Human request matrix passes locally. |
| 17 | [Final gate](17-springboot-final-gate.md) | Reference implementation is ready for FastAPI parity. |

## Per-Task Rule

```text
read source docs
-> write the failing test
-> run the focused test and confirm the failure
-> implement the smallest code
-> run the focused test
-> run .\mvnw.cmd test
-> update the tracker
```

## Default Commands

Run commands from:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
```

Focused test:

```powershell
.\mvnw.cmd -Dtest=StatusTransitionPolicyTest test
```

Full module test:

```powershell
.\mvnw.cmd test
```

Run app after endpoints exist:

```powershell
.\mvnw.cmd spring-boot:run
```

## Stop Rules

- Do not add JPA, H2, PostgreSQL, Spring Security, Actuator, Docker, deployment config, or OpenAPI server generation.
- Do not add FastAPI parity behavior here.
- Do not start a later endpoint before the current task's focused and full tests pass.

