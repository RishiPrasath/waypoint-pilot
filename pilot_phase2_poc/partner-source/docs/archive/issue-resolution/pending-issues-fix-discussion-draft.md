# Pending Issues And Fix Discussion Draft

## Purpose

This draft is the working place for resolving the final Phase 2 planning audit issues one by one.

Source audit:

```text
C:\Users\prasa\Documents\Github\Waypoint\phase_2\01-partner-source\16-final-plan-audit-report.md
```

Working rule:

```text
Discuss one issue at a time.
Record the decision here.
Then patch the affected planning files.
Keep this draft as the running decision log until the planning pack is clean.
```

## Pending Issues First

| ID | Priority | Status | Issue | Why It Matters | Main Files |
|---|---|---|---|---|---|
| B1 | Blocker | Proposed | Spring Boot scaffold/toolchain is not pinned. | A developer still has to decide module path, build tool, Java version, Spring Boot version, dependencies, base package, and run/test commands before coding. | `99-decisions/`, `14-cicd-pipeline-guide.md`, future scaffold |
| B2 | Blocker | Proposed | Canonical Slice 1 status transition table is inconsistent. | `StatusTransitionPolicyTest` can be written against different valid-looking transition tables. | `03-domain-model.md`, `04-api-contract.md`, `06-test-plan.md`, `15-slice-1-design-freeze.md` |
| B3 | Blocker | Proposed | Invalid-transition seed/test fixture can hit authorization before lifecycle validation. | The expected `409 INVALID_STATUS_TRANSITION` test may return `403 ORDER_NOT_ASSIGNED_TO_DRIVER` instead. | `05-data-model-and-seed-data.md`, `06-test-plan.md`, `04-api-contract.md` |
| B4 | Blocker | Proposed | FastAPI sequencing needs to match the reduced API scope. | With a smaller API surface, Spring Boot and FastAPI can be multitasked as contract-parity implementations instead of strictly sequential work. | `00-program-plan/00-index.md`, `03-implementation-sequence.md`, `ADR-0005-implementation-order.md`, `15-slice-1-design-freeze.md` |
| M1 | Major | Resolved | ADR-0001, ADR-0003, and ADR-0004 are still `Proposed` while used as binding rules. | Foundational architecture rules look provisional even though implementation depends on them. | `99-decisions/README.md`, ADR-0001, ADR-0003, ADR-0004 |
| M2 | Major | Resolved | Resolved open questions still appear as open. | Settled decisions like in-memory persistence and OpenAPI-first can be reopened accidentally. | `00-program-plan/04-open-questions.md`, `05-api-design-checklist.md`, ADR-0006, ADR-0007 |
| M3 | Major | Resolved | Older verification report still reports issues that later docs fixed. | It creates false readiness signals during final review. | `01-partner-source/10-api-design-verification-report.md`, `shared-error-contract.md` |
| M4 | Major | Resolved | Prose API contract has stale examples. | Implementers may copy `activeAssignmentCount = 3`, wrong assignment counts, or reused event IDs instead of YAML/seed values. | `01-partner-source/04-api-contract.md`, `05-data-model-and-seed-data.md`, `partner-source.v1.yaml` |
| M5 | Major | Resolved | Shared partner-source contract summary is stale. | It omits endpoints that are frozen in the YAML/design freeze. | `90-shared/contracts/partner-source.openapi.md`, `partner-source.v1.yaml`, `15-slice-1-design-freeze.md` |
| M6 | Major | Resolved | Manual `.http` checklist misses some negative paths. | Client-visible contract failures are not manually checkable yet. | `90-shared/contracts/openapi/http/partner-source-slice1.http`, `partner-source.v1.yaml` |
| M7 | Major | Resolved | Shared contract test plan is too broad to be actionable. | BFF compatibility can drift even if unit/controller tests pass. | `90-shared/evaluation/contract-test-plan.md`, `06-test-plan.md`, `shared-error-contract.md` |
| M8 | Major | Resolved | Shared acceptance gates are weaker than module done criteria. | Slice 1 could be marked accepted without all frozen behavior, manual checks, ProblemDetail, readiness, and commands. | `90-shared/evaluation/acceptance-gates.md`, `07-implementation-plan.md`, `15-slice-1-design-freeze.md` |
| M9 | Major | Resolved | Spring Boot package structure is inconsistent. | Code can start with mixed layer-based and feature-based organization. | `07-implementation-plan.md`, `12-springboot-api-fundamentals.md` |
| M10 | Major | Resolved | In-memory repository guidance conflicts with JPA-first learning examples. | Slice 1 may drift into H2/JPA setup before API behavior is stable. | `12-springboot-api-fundamentals.md`, `13-springboot-testing-playbook.md`, ADR-0006 |
| M11 | Major | Resolved | Validation taxonomy is not frozen. | `400`, `409`, and `422` mappings can drift across controller validation, service exceptions, and ProblemDetail handling. | `04-api-contract.md`, `06-test-plan.md`, `shared-error-contract.md` |
| M12 | Major | Resolved | Use cases/resource docs still read broader than Slice 1. | Deferred endpoints like delivery attempts, exceptions, support summary, and delivery view can creep into the first implementation. | `02-use-cases.md`, `09-use-case-resource-map.md`, `15-slice-1-design-freeze.md` |
| T1 | Testing | Resolved | TDD implementation order appears in multiple variants. | The first implementation pass can bounce between framework wiring and behavior tests. | `06-test-plan.md`, `07-implementation-plan.md`, `13-springboot-testing-playbook.md` |
| T2 | Testing | Resolved | `DELIVERY_ATTEMPTED` behavior is not clearly pinned down. | Implementation could reject a contract-listed enum or prematurely expose failed-delivery behavior. | `03-domain-model.md`, `04-api-contract.md`, `06-test-plan.md`, `partner-source.v1.yaml` |
| C1 | CI/CD | Resolved | CI guide assumes Maven/project root before scaffold exists. | First CI workflow may run in the wrong directory or use unreproducible commands. | `14-cicd-pipeline-guide.md`, future scaffold |
| C2 | CI/CD | Resolved | First workflow includes artifact upload too early. | Beginners may debug artifact paths before the basic test gate is stable. | `14-cicd-pipeline-guide.md`, `07-implementation-plan.md` |
| C3 | CI/CD | Resolved | Future CI roadmap is not mapped to module jobs. | FastAPI parity, RAG evaluation, BFF contracts, and frontend checks may be bolted on inconsistently later. | `14-cicd-pipeline-guide.md`, `regression-suite.md` |
| N1 | Minor | Resolved | Actuator deferral should be stated wherever health/readiness learning docs mention Actuator. | Prevents accidentally adopting Actuator in Slice 1. | `12-springboot-api-fundamentals.md`, ADR-0007 |
| N2 | Minor | Resolved | OpenAPI lint rules are too light. | Lint can pass while ProblemDetail, pagination, error response, or example drift remains. | `90-shared/contracts/openapi/`, `api-design-standards-research.md` |

## Suggested Discussion Order

1. B1 - Spring Boot scaffold/toolchain
2. B2 - Canonical status transition table
3. B3 - Invalid-transition fixture
4. B4 - FastAPI sequencing
5. M1 - ADR statuses
6. M2 and M3 - stale status/open-question docs
7. M4 through M8 - contract, test, and gate alignment
8. M9 through M11 - Spring Boot implementation guidance
9. M12, T1, T2 - scope and TDD cleanup
10. C1 through C3, N1, N2 - CI/CD and polish

## Remaining Issue Groups

This section groups the issues after B1-B4. The consistency group has now been patched in one pass; the standalone group remains pending.

### Consistency Issues

Status: Resolved in the one-shot consistency pass.

These issues are mainly about making the planning pack tell one coherent story across program docs, ADRs, contracts, test plans, and implementation guides.

| ID | Issue | Why It Is A Consistency Issue |
|---|---|---|
| M1 | ADR-0001, ADR-0003, and ADR-0004 are still `Proposed` while used as binding rules. | Governance status and implementation assumptions disagree. |
| M2 | Resolved open questions still appear as open. | Later decisions exist, but older docs still ask the same questions. |
| M3 | Older verification report still reports issues that later docs fixed. | A stale readiness report conflicts with current contract/error docs. |
| M4 | Prose API contract has stale examples. | Markdown examples disagree with seed data, OpenAPI, and manual checks. |
| M5 | Shared partner-source contract summary is stale. | Shared summary omits endpoints frozen elsewhere. |
| M8 | Shared acceptance gates are weaker than module done criteria. | Shared gates do not match the design freeze and implementation done criteria. |
| M9 | Spring Boot package structure is inconsistent. | Implementation docs recommend competing package layouts. |
| M10 | In-memory repository guidance conflicts with JPA-first learning examples. | ADR-0006 says in-memory first, while learning docs can pull toward JPA too early. |
| M12 | Use cases/resource docs still read broader than Slice 1. | Older use-case language can reopen deferred endpoint scope. |
| T1 | TDD implementation order appears in multiple variants. | Test/implementation docs give different first-step sequences. |
| T2 | `DELIVERY_ATTEMPTED` behavior is not clearly pinned down. | Enum, transition, test, and deferred-scope docs do not yet say the same thing. |
| C1 | CI guide assumes Maven/project root before scaffold exists. | CI guide must align with the planning-only scaffold decision from B1. |
| C2 | First workflow includes artifact upload too early. | CI guide and implementation plan differ on the first workflow scope. |
| N1 | Actuator deferral should be stated wherever health/readiness learning docs mention Actuator. | ADR-0007 defers Actuator, but learning docs can make it seem optional for Slice 1. |

### Standalone Issues

These issues are useful improvements or missing artifacts, but they do not mainly come from contradictory planning docs.

| ID | Status | Issue | Why It Is Standalone |
|---|---|---|---|
| M6 | Resolved | Manual `.http` checklist misses some negative paths. | Needed additional coverage cases; not primarily a cross-doc contradiction. |
| M7 | Resolved | Shared contract test plan is too broad to be actionable. | Needed a more detailed contract-test matrix. |
| M11 | Resolved | Validation taxonomy is not frozen. | Needed an explicit rule for `400`, `409`, and `422` behavior. |
| C3 | Resolved | Future CI roadmap is not mapped to module jobs. | Needed a forward-looking CI roadmap. |
| N2 | Resolved | OpenAPI lint rules are too light. | Needed stronger lint/project rules. |

## Issue Discussion Notes

### B1 - Spring Boot Scaffold/Toolchain

Status: In discussion

Decision needed:

```text
module path
build tool
Java version
Spring Boot version
dependencies
base package
local test command
local run command
first CI working directory
```

Discussion notes:

- This is a planning decision only. We are not creating the Spring Boot app yet.
- The goal is to remove ambiguity from the future implementation plan while keeping the current `phase_2` folder as planning documentation.
- Because the implementer is a beginner, prefer the standard Spring Initializr path over custom project structure decisions.
- Beginner-friendly default setup:
  - Create the future implementation as a separate `partner-source` Spring Boot project when coding begins.
  - Use Maven, not Gradle, because the existing CI/CD guide already teaches Maven and `mvn -B verify`.
  - Use Java 21 LTS.
  - Use the current supported Spring Boot line available through Spring Initializr at implementation time.
  - Use simple dependencies first: Spring Web, Validation, and Spring Boot Test.
  - Do not add database/JPA dependencies in Slice 1 because ADR-0006 chooses in-memory repositories.
  - Add springdoc/OpenAPI UI only if it helps local inspection; the hand-written OpenAPI YAML remains the contract source of truth.
- The future app should not be created under `phase_2`; `phase_2` remains the planning area.

Decision:

- Proposed: Future implementation should use a separate Spring Boot Maven project for `partner-source`, generated from Spring Initializr when coding begins, using Java 21 LTS, simple web/validation/test dependencies, and in-memory repositories for Slice 1.

Files to patch:

- Later planning patch:
  - Add `99-decisions/ADR-0008-spring-boot-scaffold-toolchain.md`.
  - Update `01-partner-source/07-implementation-plan.md`.
  - Update `01-partner-source/14-cicd-pipeline-guide.md`.
  - Update `01-partner-source/15-slice-1-design-freeze.md`.

### B2 - Canonical Slice 1 Status Transition Table

Status: In discussion

Decision needed:

```text
One transition table must govern StatusTransitionPolicyTest, service behavior, API prose, seed data, and OpenAPI notes.
```

Discussion notes:

- Current drift:
  - `02-use-cases.md` has the broadest logistics lifecycle and includes later support states such as `DELAYED`, `ON_HOLD`, `FAILED_DELIVERY`, and `RETURNED`.
  - `03-domain-model.md` has a medium Slice 1 table with cancellation paths and some `DELIVERY_ATTEMPTED` paths.
  - `04-api-contract.md` has the narrowest initial transition table.
  - `06-test-plan.md` tests only the core happy path plus terminal rejection cases.
- Beginner-friendly direction:
  - Use the narrow table as the canonical Slice 1 policy.
  - Treat broader lifecycle states as Slice 2/later design material.
  - Keep the first `StatusTransitionPolicyTest` small and easy to reason about.
- Proposed canonical Slice 1 table:

| Current Status | Allowed Next Statuses |
|---|---|
| `CREATED` | `CONFIRMED`, `CANCELLED` |
| `CONFIRMED` | `PICKED_UP`, `CANCELLED` |
| `PICKED_UP` | `IN_TRANSIT` |
| `IN_TRANSIT` | `OUT_FOR_DELIVERY` |
| `OUT_FOR_DELIVERY` | `DELIVERED` |
| `DELIVERY_ATTEMPTED` | none in Slice 1 unless B3/T2 explicitly reopens it |
| `DELIVERED` | none |
| `CANCELLED` | none |

- Rationale:
  - This proves the core path: created -> confirmed -> picked up -> in transit -> out for delivery -> delivered.
  - It still allows cancellation before physical movement begins.
  - It avoids making `DELIVERY_ATTEMPTED` active behavior before the `delivery-attempts` endpoint exists.
  - It keeps failed delivery, redelivery, delays, holds, returns, and exceptions out of Slice 1.

Decision:

- Proposed: Adopt the narrow core delivery table above as the only canonical Slice 1 transition policy. Mark broader lifecycle tables as future/Slice 2 reference material.

Files to patch:

- Later planning patch:
  - `01-partner-source/03-domain-model.md`
  - `01-partner-source/04-api-contract.md`
  - `01-partner-source/06-test-plan.md`
  - `01-partner-source/15-slice-1-design-freeze.md`
  - possibly `01-partner-source/02-use-cases.md`

### B3 - Invalid-Transition Fixture

Status: In discussion

Decision needed:

```text
Either allow completed assignment ASN-3003 to authorize the invalid-transition check,
or add a dedicated active assigned delivered-order fixture for the 409 test.
```

Discussion notes:

- Current conflict:
  - `ORD-1003` is the delivered order used for invalid transition tests.
  - `ASN-3003` links `DRV-2001` to `ORD-1003`, but its assignment status is `COMPLETED`.
  - The test plan also says completed assignments do not count as active work unless deliberately allowed.
  - If the status-event endpoint checks active assignment before transition policy, the invalid transition request can return `403 ORDER_NOT_ASSIGNED_TO_DRIVER` instead of `409 INVALID_STATUS_TRANSITION`.
- Beginner-friendly rule:
  - Keep authorization and lifecycle validation tests separate.
  - A test for invalid lifecycle transition should use a driver/order pair that passes assignment authorization first.
  - A test for unassigned driver should separately prove `403 ORDER_NOT_ASSIGNED_TO_DRIVER`.
- Proposed fixture approach:
  - Keep `ASN-3003` as `COMPLETED` for assignment-history and "completed assignments are not active" tests.
  - Add or designate a separate active assigned delivered-order fixture for invalid transition testing.
  - Example future fixture:

```text
ORD-1005
currentStatus: DELIVERED
assignedDriver: DRV-2001
assignment: ASN-3005
assignmentStatus: ASSIGNED
scenario: active assigned delivered order used only to prove DELIVERED -> OUT_FOR_DELIVERY returns 409
```

- Alternative if we want fewer seed records:
  - Change `ASN-3003` to `ASSIGNED`, but then it no longer proves completed assignment behavior cleanly.
  - This is less clear for a beginner because one fixture would carry two meanings.

Decision:

- Proposed: Keep `ASN-3003` completed, and add a dedicated active assigned delivered-order fixture for `INVALID_STATUS_TRANSITION`.

Files to patch:

- Later planning patch:
  - `01-partner-source/05-data-model-and-seed-data.md`
  - `01-partner-source/06-test-plan.md`
  - `90-shared/contracts/openapi/http/partner-source-slice1.http`
  - possibly `01-partner-source/15-slice-1-design-freeze.md`

### B4 - FastAPI Sequencing

Status: In discussion

Decision needed:

```text
Decide whether FastAPI is strictly deferred or multitasked with Spring Boot after reducing API scope.
```

Discussion notes:

- Revised context:
  - We reduced the API scope to a narrow Slice 1.
  - Because the surface area is smaller, FastAPI parity no longer needs to wait until the entire Spring Boot slice is complete.
  - FastAPI can be multitasked as a contract-parity implementation, not as a separate product expansion.
- Beginner-friendly guardrails:
  - Spring Boot remains the primary learning path.
  - FastAPI must follow the same frozen OpenAPI contract and seed scenarios.
  - FastAPI should not introduce new endpoints, fields, statuses, persistence, or behavior beyond the shared contract.
  - If multitasking becomes confusing, pause FastAPI and continue Spring Boot first.
- Proposed sequence:

```text
1. Finalize partner-source contract and planning cleanup.
2. Start Spring Boot and FastAPI partner-source Slice 1 in parallel against the same OpenAPI contract.
3. Keep Spring Boot as the primary learning/reference implementation.
4. Use FastAPI as the parity implementation for the same endpoints, DTOs, seed data, error codes, and manual .http checks.
5. Add tests and first CI around the shared contract.
6. Continue to rag-db, BFF, and frontend work after partner-source parity is stable.
```

Decision:

- Proposed: Because API scope is reduced, multitask Spring Boot and FastAPI for Slice 1 after the contract is frozen. Spring Boot remains the primary beginner/reference implementation; FastAPI must stay contract-bound and cannot expand scope.

Files to patch:

- Later planning patch:
  - `00-program-plan/00-index.md`
  - `00-program-plan/03-implementation-sequence.md`
  - `99-decisions/ADR-0005-implementation-order.md`

### M1 - ADR Statuses

Status: Resolved

Discussion notes:

- ADR-0001, ADR-0003, and ADR-0004 are used as binding planning rules, so keeping them `Proposed` created false uncertainty.

Decision:

- Mark ADR-0001, ADR-0003, and ADR-0004 as `Accepted` and align the ADR index.

Files to patch:

- `99-decisions/ADR-0001-module-boundaries.md`
- `99-decisions/ADR-0003-contract-first-rule.md`
- `99-decisions/ADR-0004-rag-db-boundary.md`
- `99-decisions/README.md`

### M2 - Resolved Open Questions

Status: Resolved

Discussion notes:

- Some settled setup decisions still appeared as open questions.

Decision:

- Convert the open-questions doc into a decision-status view with resolved and deferred sections.

Files to patch:

- `00-program-plan/04-open-questions.md`

### M3 - Stale Verification Report

Status: Resolved

Discussion notes:

- The older verification report is still useful history, but it should not be read as the current readiness state.

Decision:

- Add a superseded/current-source-of-truth notice at the top of the verification report.

Files to patch:

- `01-partner-source/10-api-design-verification-report.md`

### M4 - Stale Prose API Examples

Status: Resolved

Discussion notes:

- Prose examples drifted from seed data and the OpenAPI contract.

Decision:

- Align the prose examples with the current driver assignment count, assignment list, and status-event example IDs.

Files to patch:

- `01-partner-source/04-api-contract.md`

### M5 - Stale Shared Partner-Source Contract Summary

Status: Resolved

Discussion notes:

- The shared contract summary omitted frozen Slice 1 endpoints.

Decision:

- Update the shared summary to point to the canonical OpenAPI YAML and list the full Slice 1 endpoint set.

Files to patch:

- `90-shared/contracts/partner-source.openapi.md`

### M6 - Missing Manual Negative Paths

Status: Resolved

Discussion notes:

- The manual `.http` checklist already covered the main happy paths and several core negatives.
- The audit still identified contract-visible gaps: missing driver on status-event creation, invalid status event, malformed body, invalid assignment query, and readiness `503`.
- This issue was about manual coverage only. The exact validation taxonomy for `400`, `409`, and `422` was resolved separately in `M11`.

Decision:

- Add manual requests for the missing contract-backed negative paths without expanding Slice 1 behavior.

Files to patch:

- `90-shared/contracts/openapi/http/partner-source-slice1.http`

### M7 - Broad Contract Test Plan

Status: Resolved

Discussion notes:

- The old shared contract test plan named high-level boundaries but did not define exact Partner Source Slice 1 checks.
- BFF compatibility needs explicit protection for HTTP statuses, required fields, enum values, pagination shape, and shared `ProblemDetail`.
- Spring Boot and FastAPI should eventually pass the same contract matrix.

Decision:

- Replace the broad plan with a concrete Partner Source Slice 1 contract matrix, shared error assertions, Spring Boot/FastAPI parity rules, and a beginner-friendly CI growth path.

Files to patch:

- `90-shared/evaluation/contract-test-plan.md`

### M8 - Weak Shared Acceptance Gates

Status: Resolved

Discussion notes:

- Shared gates were weaker than the design-freeze done criteria.

Decision:

- Expand Partner Source acceptance gates to include frozen behavior, errors, health/readiness, manual checks, automated checks, CI, and Spring Boot/FastAPI contract parity.

Files to patch:

- `90-shared/evaluation/acceptance-gates.md`

### M9 - Package Structure

Status: Resolved

Discussion notes:

- Implementation docs were split between layer-based and feature-based package structures.

Decision:

- Use feature-based packages for Spring Boot: `order`, `driver`, `assignment`, `shared`, and `seed`, with `api/domain/repository/service` inside the feature packages.

Files to patch:

- `01-partner-source/07-implementation-plan.md`
- `01-partner-source/12-springboot-api-fundamentals.md`

### M10 - In-Memory Repository Guidance

Status: Resolved

Discussion notes:

- Learning docs introduced JPA examples too early for a Slice 1 in-memory implementation.

Decision:

- Teach plain repository interfaces plus in-memory implementations for Slice 1. Keep JPA, H2, and PostgreSQL as later persistence topics.

Files to patch:

- `01-partner-source/12-springboot-api-fundamentals.md`
- `01-partner-source/13-springboot-testing-playbook.md`

### M11 - Validation Taxonomy

Status: Resolved

Discussion notes:

- Missing required fields, bad enum values, malformed JSON, unknown fields, invalid date-time formats, and invalid path/query values are request-shape failures.
- Lifecycle conflicts are different from request validation and should stay under the status transition policy.
- `422` should be reserved for a syntactically valid status event whose business meaning is unacceptable.

Decision:

- Freeze taxonomy as: `400 INVALID_REQUEST` for invalid request shape, `409 INVALID_STATUS_TRANSITION` for illegal lifecycle moves, and `422 INVALID_STATUS_EVENT` for valid-shaped but semantically invalid status events.

Files to patch:

- `90-shared/contracts/shared-error-contract.md`
- `01-partner-source/04-api-contract.md`
- `01-partner-source/06-test-plan.md`
- `90-shared/contracts/openapi/http/partner-source-slice1.http`

### M12 - Slice 1 Scope Labels

Status: Resolved

Discussion notes:

- Use-case and resource-map docs now label broader product ideas as Slice 2/later unless reopened.
- The design freeze remains the source of truth for Slice 1.

Decision:

- Add explicit Slice 1 status notes to broader planning docs instead of deleting useful future-scope research.

Files to patch:

- `02-use-cases.md`
- `09-use-case-resource-map.md`
- `15-slice-1-design-freeze.md`

### T1 - Canonical TDD Order

Status: Resolved

Discussion notes:

- Multiple docs had similar but different test-first sequences.
- The canonical order now starts with business behavior and seed data before framework-heavy checks.

Decision:

- Use this order: domain policy tests -> seed/repository behavior tests -> service tests -> error handling tests -> controller tests -> integration/manual checks -> contract checks.

Files to patch:

- `06-test-plan.md`
- `07-implementation-plan.md`
- `13-springboot-testing-playbook.md`

### T2 - DELIVERY_ATTEMPTED Behavior

Status: Resolved

Discussion notes:

- `DELIVERY_ATTEMPTED` can remain a known enum value, but Slice 1 should not create failed-delivery behavior early.

Decision:

- Keep `DELIVERY_ATTEMPTED` as a contract-visible enum, but do not include it as a valid Slice 1 transition or required behavior until the delivery-attempts slice.

Files to patch:

- `04-api-contract.md`
- `15-slice-1-design-freeze.md`

### C1 - CI Project Root And Test Command

Status: Resolved

Discussion notes:

- CI guidance assumed a Maven project before a scaffold exists.
- This is still a planning area, so CI must describe the future scaffold path rather than pretend it exists today.

Decision:

- Future CI should run from the generated Spring Boot Maven scaffold working directory, currently documented as `partner-source/` unless the scaffold uses a different folder.

Files to patch:

- `14-cicd-pipeline-guide.md`

### C2 - First Workflow Scope

Status: Resolved

Discussion notes:

- Artifact upload is useful later, but it creates early path/debugging noise before the first build/test gate is stable.

Decision:

- First GitHub Actions workflow should checkout, set up JDK 21, and run Maven verification from the scaffold directory. Add artifact upload only after packaging path is known.

Files to patch:

- `14-cicd-pipeline-guide.md`

### C3 - Future CI Roadmap

Status: Resolved

Discussion notes:

- Each codebase should have its own CI/CD pipeline first.
- Spring Boot Partner Source API is the first module and gets the first pipeline.
- FastAPI Partner Source API should get its own separate pipeline when that codebase starts.
- RAG/retriever, BFF, chatbot frontend, and mobile delivery frontend should also be treated as separate modules with separate pipelines.
- A collective full-application pipeline can be discussed later after the separate module pipelines are stable.

Decision:

- Use separate CI/CD pipelines per codebase for now. Do not merge module checks into one collective application pipeline yet.

Files to patch:

- `01-partner-source/14-cicd-pipeline-guide.md`
- `90-shared/evaluation/regression-suite.md`

### N1 - Actuator Deferral Notes

Status: Resolved

Discussion notes:

- Health/readiness must exist in Slice 1, but Actuator is intentionally deferred.

Decision:

- Use custom `/health` and `/ready` endpoints for Slice 1. Do not add Actuator just for health checks.

Files to patch:

- `12-springboot-api-fundamentals.md`

### N2 - OpenAPI Lint Rules

Status: Resolved

Discussion notes:

- The existing `.spectral.yaml` checked operation metadata and basic success responses only.
- OpenAPI can be syntactically valid while still drifting on `ProblemDetail`, examples, pagination, enum values, or schema closure.
- This should remain planning/tooling guidance for now; automation belongs in each module pipeline when that codebase starts.

Decision:

- Strengthen the OpenAPI lint rule set and document the minimum contract-quality checks: operation metadata, success responses, shared `ProblemDetail`, error examples, success examples, required fields, pagination, enums, `additionalProperties`, and status consistency.

Files to patch:

- `90-shared/contracts/openapi/.spectral.yaml`
- `90-shared/contracts/api-design-standards-research.md`

## Running Fix Log

| Date | Issues | Change |
|---|---|---|
| 2026-07-01 | M1, M2, M3, M4, M5, M8, M9, M10, M12, T1, T2, C1, C2, N1 | Resolved consistency issues in one pass across ADR status, open questions, verification status, API examples, shared contract summary, acceptance gates, scope labels, package structure, in-memory/JPA guidance, TDD order, `DELIVERY_ATTEMPTED`, CI scaffold assumptions, artifact upload timing, and Actuator deferral. |
| 2026-07-01 | M6 | Added manual `.http` negative-path coverage for readiness not-ready, invalid ID formats, missing timeline order, invalid assignment filters/pages, missing driver on status-event creation, invalid status event, missing order on POST, and malformed status-event body. |
| 2026-07-01 | M7 | Replaced the broad shared contract test plan with a concrete Partner Source Slice 1 matrix covering endpoint success checks, error checks, shared ProblemDetail assertions, Spring Boot/FastAPI parity, and CI growth order. |
| 2026-07-01 | M11 | Froze validation taxonomy: `400 INVALID_REQUEST` for invalid request shape, `409 INVALID_STATUS_TRANSITION` for lifecycle conflicts, and `422 INVALID_STATUS_EVENT` for valid-shaped but semantically invalid status events. |
| 2026-07-01 | C3 | Recorded separate CI/CD pipelines per codebase: Spring Boot Partner Source first, FastAPI Partner Source separately later, then RAG/retriever, BFF, chatbot frontend, and mobile delivery frontend as separate module pipelines; collective application CI deferred. |
| 2026-07-01 | N2 | Strengthened OpenAPI lint planning and `.spectral.yaml` checks for ProblemDetail references, response examples, object schema closure, and ProblemDetail required fields; documented the broader lint checklist and future automation path. |
