# Partner Source Implementation Overview

This file explains how the two Partner Source implementations should relate to each other.

## Current Position

The implementation lane is ready for manual development.

Do not scaffold code from the active docs directly. Use the numbered build books as execution authority:

- `../../partner-source-springboot/build-sequence/00-index.md`
- `../../partner-source-fastapi/build-sequence/00-index.md`
- `../../parity/build-sequence/00-index.md`

## Implementation Tracks

| Track | Role | Pipeline |
|---|---|---|
| Spring Boot | Primary beginner/reference implementation. Build this first. | Separate Spring Boot CI/CD pipeline. |
| FastAPI | Contract-parity implementation. Start after Spring Boot has enough reference behavior to mirror. | Separate FastAPI CI/CD pipeline. |

## Shared Rules

Both tracks must follow:

- `contract-handoff.md`
- `data-and-seed-handoff.md`
- `test-and-acceptance-handoff.md`
- `implementation-mapping.md`
- `../support/implementation-schematic-and-task-sequence.md`
- `../contracts/openapi/partner-source.v1.yaml`
- `../contracts/shared-error-contract.md`
- `../contracts/openapi/http/partner-source-slice1.http`

## What Spring Boot Owns

Spring Boot owns the first reference implementation path:

- Java/Spring learning anchor.
- TDD implementation order.
- package structure and service boundaries.
- first module CI/CD pipeline.
- first proof that the contract is practical.

## What FastAPI Owns

FastAPI owns a second implementation of the same API behavior:

- Python/FastAPI learning path.
- parity with the shared OpenAPI contract.
- same seed scenarios and error behavior.
- its own pipeline when implementation starts.

FastAPI must not add endpoints, fields, statuses, persistence, or behavior just because it is easy in FastAPI.

## Pipeline Decision

Keep one CI/CD pipeline per codebase for now.

Do not create a merged application pipeline until:

1. Spring Boot Partner Source has meaningful tests.
2. FastAPI Partner Source has parity tests.
3. RAG, BFF, and frontend module boundaries are stable enough to justify cross-module checks.

## Supporting File

CI/CD guidance lives in `../support/cicd-pipeline-guide.md`.

The side-by-side implementation map lives in `implementation-mapping.md`.

The reference implementation schematic lives in `../support/implementation-schematic-and-task-sequence.md`.

The numbered build books are the ordered task list.
