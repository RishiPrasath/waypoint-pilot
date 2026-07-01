# FastAPI Implementation Handoff

This file is the FastAPI-specific handoff for Partner Source.

## Role

FastAPI is a contract-parity implementation of the Partner Source API.

It exists to prove the same API design can be implemented in Python without changing the contract.

## Timing

FastAPI can be multitasked because the Partner Source API scope is intentionally small. It should begin only after the shared contract, seed data, and manual HTTP expectations are frozen.

## Must Match Spring Boot

FastAPI must match Spring Boot on:

- endpoint paths and HTTP methods
- JSON request and response fields
- status enum values
- seed records and scenarios
- error status codes and error codes
- ProblemDetail-style error shape
- `/health` and `/ready` behavior
- manual HTTP checklist outcomes
- contract test expectations

## Must Not Add Independently

FastAPI must not independently add:

- extra endpoints
- extra fields
- extra status values
- different validation rules
- a different seed set
- database persistence
- BFF-specific response shapes
- deployment assumptions

## Expected Future Setup

When coding begins, the FastAPI codebase should have its own small structure, its own tests, and its own CI/CD pipeline.

Do not over-design this yet. The first planning goal is parity with the shared Partner Source contract.

Likely future testing direction:

- domain/policy tests for transition and authorization rules
- API tests using a FastAPI-compatible HTTP test client
- contract checks against the shared OpenAPI behavior
- manual request checks using the shared `.http` file

## First CI/CD Pipeline

Create a separate FastAPI pipeline only after meaningful FastAPI tests exist.

First version should stay small:

- checkout code
- set up Python
- install project dependencies
- run tests
- fail on test failure

Do not merge this with the Spring Boot pipeline yet.

## Must Follow

- Contract handoff: `contract-handoff.md`
- Seed handoff: `data-and-seed-handoff.md`
- Test handoff: `test-and-acceptance-handoff.md`
- Side-by-side implementation map: `implementation-mapping.md`
- Implementation schematic and task sequence reference: `../support/implementation-schematic-and-task-sequence.md`
- OpenAPI: `../contracts/openapi/partner-source.v1.yaml`
- Shared errors: `../contracts/shared-error-contract.md`
- Contract test plan: `../contracts/evaluation/contract-test-plan.md`
- FastAPI fundamentals support: `../support/fastapi-api-fundamentals.md`
- FastAPI testing support: `../support/fastapi-testing-playbook.md`
