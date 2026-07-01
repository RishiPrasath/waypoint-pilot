# FastAPI Testing Playbook

This is a support guide for the FastAPI Partner Source tests.

Use `../../partner-source-fastapi/build-sequence/00-index.md` as the execution authority.

## Purpose

Use this file to explain beginner FastAPI testing concepts during the FastAPI parity build.

This file is not the acceptance source of truth. The source of truth is:

- `../active/test-and-acceptance-handoff.md`
- `../contracts/evaluation/contract-test-plan.md`
- `../contracts/openapi/http/partner-source-slice1.http`

## Topics To Expand As Needed

- domain/policy tests
- service tests
- API route tests
- validation and error tests
- seed fixture tests
- readiness tests
- OpenAPI/contract checks
- CI/CD test command

## Guardrail

FastAPI tests should prove parity with the shared contract, not create a separate interpretation of Partner Source.
