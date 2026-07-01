# Spring Boot Implementation Handoff

This file is the Spring Boot-specific handoff for Partner Source.

## Role

Spring Boot is the primary beginner/reference implementation for Partner Source Slice 1.

Build this first so the project has one clear implementation path before comparing it with FastAPI.

## Planned Setup

When coding begins, create a separate Spring Boot codebase or module for Partner Source. Do not create it from this planning folder.

Recommended starting choices:

- Java 21 LTS.
- Maven.
- Spring Web.
- Spring Validation.
- Spring Boot Test.
- In-memory repositories for Slice 1.
- Custom `/health` and `/ready`.

## Package Direction

Use feature-oriented packages with small internal layers.

```text
partner_source
  order
    api
    domain
    repository
    service
  driver
    api
    domain
    repository
    service
  assignment
    domain
    repository
    service
  shared
    error
    health
    seed
```

The exact package names can change when the real codebase is created, but keep the idea: controllers and DTOs at the edge, domain rules in domain classes, repositories behind services.

## First Tests

Start with:

1. `StatusTransitionPolicyTest`
2. `AssignmentAuthorizationPolicyTest`

Then add seed repository tests, service tests, controller tests, integration tests, and contract checks.

## First CI/CD Pipeline

Create a separate Spring Boot pipeline after meaningful tests exist.

First version should stay small:

- checkout code
- set up Java 21
- run Maven test/verify command
- fail on test failure

Avoid artifact upload, deployment, environment promotion, and merged app checks in the first pipeline.

## Must Follow

- Contract handoff: `contract-handoff.md`
- Seed handoff: `data-and-seed-handoff.md`
- Test handoff: `test-and-acceptance-handoff.md`
- Side-by-side implementation map: `implementation-mapping.md`
- Implementation schematic and task sequence reference: `../support/implementation-schematic-and-task-sequence.md`
- CI/CD support: `../support/cicd-pipeline-guide.md`
- Persistence ADR: `../../99-decisions/ADR-0006-slice-1-persistence-strategy.md`
- Health/readiness ADR: `../../99-decisions/ADR-0007-health-readiness-strategy.md`
