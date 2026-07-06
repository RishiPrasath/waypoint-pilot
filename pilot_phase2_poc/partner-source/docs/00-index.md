# Partner Source Index

`partner-source` is the synthetic logistics partner API for Waypoint.

It has two planned implementation tracks:

- Spring Boot: primary beginner/reference implementation.
- FastAPI: contract-parity implementation against the same shared API truth.

This folder is the local source of truth for the Partner Source implementation lane. It is not a generated codebase.

## Read First

| File | Purpose |
|---|---|
| [active/module-blueprint.md](active/module-blueprint.md) | What Partner Source is, what Slice 1 includes, and what is deferred. |
| [active/contract-handoff.md](active/contract-handoff.md) | Human-readable contract guidance linked to the shared OpenAPI and error contract. |
| [active/data-and-seed-handoff.md](active/data-and-seed-handoff.md) | Seed records and scenarios both implementations must share. |
| [active/test-and-acceptance-handoff.md](active/test-and-acceptance-handoff.md) | Test levels, acceptance scenarios, and contract gates. |
| [active/implementation-overview.md](active/implementation-overview.md) | How Spring Boot and FastAPI relate without duplicating the API design. |
| [active/implementation-mapping.md](active/implementation-mapping.md) | Side-by-side mapping from the same API behavior to Spring Boot classes and FastAPI files/functions. |
| [active/auth-access-control-plan.md](active/auth-access-control-plan.md) | Draft next-slice plan for authentication, access control, TDD implementation, and parity checks. |
| [active/springboot-implementation-handoff.md](active/springboot-implementation-handoff.md) | Spring Boot-specific setup, package direction, test order, and first CI/CD pipeline. |
| [active/fastapi-implementation-handoff.md](active/fastapi-implementation-handoff.md) | FastAPI-specific parity rules, timing, tests, and separate CI/CD pipeline. |

## Support

| File | Purpose |
|---|---|
| [support/domain-model-detail.md](support/domain-model-detail.md) | Detailed domain model source absorbed into the module blueprint. |
| [support/api-contract-detail.md](support/api-contract-detail.md) | Detailed human-readable API contract notes. Shared OpenAPI remains canonical. |
| [support/seed-data-detail.md](support/seed-data-detail.md) | Detailed seed data source absorbed into the seed handoff. |
| [support/test-plan-detail.md](support/test-plan-detail.md) | Detailed test plan source absorbed into the test handoff. |
| [support/implementation-plan-detail.md](support/implementation-plan-detail.md) | Earlier implementation plan split into active overview plus implementation handoffs. |
| [support/implementation-schematic-and-task-sequence.md](support/implementation-schematic-and-task-sequence.md) | Reference schematic and code shapes. Numbered build books remain execution authority. |
| [support/springboot-api-fundamentals.md](support/springboot-api-fundamentals.md) | Beginner Spring Boot API learning guide. |
| [support/springboot-testing-playbook.md](support/springboot-testing-playbook.md) | Beginner Spring Boot testing guide. |
| [support/fastapi-api-fundamentals.md](support/fastapi-api-fundamentals.md) | Placeholder for beginner FastAPI API learning guide. |
| [support/fastapi-testing-playbook.md](support/fastapi-testing-playbook.md) | Placeholder for beginner FastAPI testing guide. |
| [support/cicd-pipeline-guide.md](support/cicd-pipeline-guide.md) | Beginner CI/CD guide for separate module pipelines. |

## Research

| File | Purpose |
|---|---|
| [research/use-cases.md](research/use-cases.md) | Use-case thinking that shaped the API. |
| [research/customer-service-use-case-research.md](research/customer-service-use-case-research.md) | Customer-service research behind Partner Source scenarios. |
| [research/use-case-resource-map.md](research/use-case-resource-map.md) | Mapping from actor use cases to API resources. |
| [research/springboot-testing-cicd-research.md](research/springboot-testing-cicd-research.md) | Research hub for Spring Boot testing and CI/CD support. |

## Archive

| File | Purpose |
|---|---|
| [archive/purpose-and-scope-source.md](archive/purpose-and-scope-source.md) | Earlier short scope source absorbed into active docs. |
| [archive/slice-1-design-freeze.md](archive/slice-1-design-freeze.md) | Frozen Slice 1 scope source absorbed into active handoff docs. |
| [archive/audits/api-design-verification-report.md](archive/audits/api-design-verification-report.md) | API design verification audit. |
| [archive/audits/final-plan-audit-report.md](archive/audits/final-plan-audit-report.md) | Final planning audit report. |
| [archive/issue-resolution/pending-issues-fix-discussion-draft.md](archive/issue-resolution/pending-issues-fix-discussion-draft.md) | Issue-by-issue discussion and fix history. |

## Shared Contract Sources

- OpenAPI: [contracts/openapi/partner-source.v1.yaml](contracts/openapi/partner-source.v1.yaml)
- Shared errors: [contracts/shared-error-contract.md](contracts/shared-error-contract.md)
- Manual HTTP checklist: [contracts/openapi/http/partner-source-slice1.http](contracts/openapi/http/partner-source-slice1.http)

## Build Execution Books

- Spring Boot: [../partner-source-springboot/build-sequence/00-index.md](../partner-source-springboot/build-sequence/00-index.md)
- FastAPI: [../partner-source-fastapi/build-sequence/00-index.md](../partner-source-fastapi/build-sequence/00-index.md)
- Parity: [../parity/build-sequence/00-index.md](../parity/build-sequence/00-index.md)
