# Final Plan Audit Report

## 1. Executive Summary

- Final verdict: not ready
- Spring Boot Slice 1 can begin only after a short planning cleanup resolves the blockers below.
- The canonical API contract is mostly sound: `90-shared/contracts/openapi/partner-source.v1.yaml`, `90-shared/contracts/shared-error-contract.md`, and `01-partner-source/15-slice-1-design-freeze.md` line up on the main Slice 1 endpoints, ProblemDetail shape, health/readiness strategy, and in-memory persistence decision.
- The planning pack is not internally clean enough for an ambiguity-free implementation handoff. Older documents still contradict the design freeze on FastAPI timing, failed-delivery scope, open questions, transition rules, examples, package structure, and acceptance gates.

Top risks:

- The first coding task, `StatusTransitionPolicyTest`, can be written against two different transition tables.
- The invalid-transition seed case may return `403 ORDER_NOT_ASSIGNED_TO_DRIVER` before reaching the expected `409 INVALID_STATUS_TRANSITION`.
- The implementation scaffold/toolchain is not pinned: module path, Maven wrapper, Spring Boot version, base package, dependencies, and exact run/test commands are still implicit.
- Stale documents can pull the first implementation back toward FastAPI parity, JPA/H2, delivery attempts, support summaries, or broader MVP scope before Spring Boot Slice 1 is stable.

Required fixes before coding:

- Add a short accepted Spring Boot scaffold/toolchain decision.
- Declare one canonical Slice 1 status transition table.
- Fix the invalid-transition fixture so authorization does not mask lifecycle validation.
- Update program sequence to make FastAPI parity follow stable Spring Boot Slice 1.
- Mark resolved open questions and stale verification reports as superseded or current.

## 2. Artifact Inventory

Reviewed target folder:

```text
C:\Users\prasa\Documents\Github\Waypoint\phase_2
```

Reviewed folder groups:

| Folder | Reviewed files |
|---|---|
| `phase_2/` | `README.md` |
| `00-program-plan/` | `00-index.md`, `01-phase-2-goals.md`, `02-module-map.md`, `03-implementation-sequence.md`, `04-open-questions.md`, `05-api-design-checklist.md`, `06-final-plan-audit-execution-prompt.md` |
| `01-partner-source/` | `00-index.md`, `01-purpose-and-scope.md`, `02-use-cases.md`, `03-domain-model.md`, `04-api-contract.md`, `05-data-model-and-seed-data.md`, `06-test-plan.md`, `07-implementation-plan.md`, `08-customer-service-use-case-research.md`, `09-use-case-resource-map.md`, `10-api-design-verification-report.md`, `11-springboot-testing-cicd-research.md`, `12-springboot-api-fundamentals.md`, `13-springboot-testing-playbook.md`, `14-cicd-pipeline-guide.md`, `15-slice-1-design-freeze.md` |
| `02-rag-db/` | `00-index.md`, `01-purpose-and-scope.md`, `02-knowledge-source-plan.md`, `03-ingestion-plan.md`, `04-retrieval-plan.md`, `05-query-planning.md`, `06-safeguards.md`, `07-evaluation-plan.md`, `08-implementation-plan.md` |
| `03-bff/` | `00-index.md`, `01-purpose-and-scope.md`, `02-client-contracts.md`, `03-service-integration-plan.md`, `04-error-and-timeout-handling.md`, `05-test-plan.md`, `06-implementation-plan.md` |
| `04-frontend/` | `00-index.md`, `01-purpose-and-scope.md`, `02-chatbot-experience.md`, `03-driver-experience.md`, `04-screens-and-flows.md`, `05-state-and-api-usage.md`, `06-test-plan.md`, `07-implementation-plan.md` |
| `90-shared/contracts/` | `README.md`, `api-design-standards-research.md`, `bff-api-contract.md`, `partner-source.openapi.md`, `rag-db.openapi.md`, `shared-error-contract.md`, `openapi/partner-source.v1.yaml`, `openapi/http/partner-source-slice1.http` |
| `90-shared/schemas/` | `README.md`, `order-status.schema.md`, `driver-assignment.schema.md`, `query-plan.schema.md`, `retrieval-result.schema.md` |
| `90-shared/evaluation/` | `acceptance-gates.md`, `contract-test-plan.md`, `regression-suite.md` |
| `99-decisions/` | `README.md`, `ADR-0001-module-boundaries.md`, `ADR-0002-partner-source-name.md`, `ADR-0003-contract-first-rule.md`, `ADR-0004-rag-db-boundary.md`, `ADR-0005-implementation-order.md`, `ADR-0006-slice-1-persistence-strategy.md`, `ADR-0007-health-readiness-strategy.md` |

## 3. Review Method

I used actual sub-agents for the specialist passes requested by the execution prompt, then synthesized the final report locally.

Specialist passes used:

- Plan Consistency Agent
- API Contract Agent
- Spring Boot Architecture Agent
- Testing And TDD Agent
- CI/CD Agent
- Implementation Readiness Agent

I also performed a local read-through of the governing documents, contracts, seed data, test plans, CI/CD plan, shared acceptance gates, and ADRs. No Spring Boot implementation code was written or modified.

## 4. Consistency Matrix

| Check | Status | Evidence | Notes |
|---|---|---|---|
| goals vs implementation sequence | Fail | `01-phase-2-goals.md`, `03-implementation-sequence.md`, `07-implementation-plan.md`, `15-slice-1-design-freeze.md` | Program sequence still puts FastAPI in the first vertical slice, while the implementation plan and freeze defer it until Spring Boot Slice 1 is stable. |
| module map vs ADRs | Partial | `02-module-map.md`, `99-decisions/README.md`, ADR-0001, ADR-0003, ADR-0004 | Boundaries and contract-first rule are used as binding rules while foundational ADRs remain `Proposed`. |
| use cases vs resource map | Partial | `02-use-cases.md`, `09-use-case-resource-map.md`, `15-slice-1-design-freeze.md` | Resource map is coherent, but use-case language still presents failed delivery, exceptions, and support summaries as MVP-ish even though freeze defers them. |
| resource map vs OpenAPI paths | Pass with stale summaries | `09-use-case-resource-map.md`, `partner-source.v1.yaml`, `partner-source.openapi.md` | YAML matches Slice 1. Shared prose summary omits `GET /api/v1/drivers/{driverId}`, `/health`, and `/ready`. |
| OpenAPI schemas vs manual `.http` checklist | Partial | `partner-source.v1.yaml`, `partner-source-slice1.http` | Happy paths and core negatives are covered. Manual requests miss some contract-visible negatives: missing driver on POST, invalid status event, malformed body, and readiness `503`. |
| seed data vs OpenAPI examples | Mostly pass | `05-data-model-and-seed-data.md`, `partner-source.v1.yaml` | Seed and YAML align on `activeAssignmentCount = 2`; `04-api-contract.md` still shows `3` in prose. |
| seed data vs test plan | Fail | `05-data-model-and-seed-data.md`, `06-test-plan.md` | `ORD-1003` invalid-transition test may be blocked by completed-assignment authorization before transition validation. |
| ADR-0006 persistence decision vs readiness contract | Pass | ADR-0006, ADR-0007, `15-slice-1-design-freeze.md`, `partner-source.v1.yaml` | In-memory persistence plus seed-data readiness is consistent. Spring learning docs still need clearer "JPA later" positioning. |
| ADR-0007 health/readiness decision vs OpenAPI and `.http` | Pass with gap | ADR-0007, `partner-source.v1.yaml`, `partner-source-slice1.http` | Custom `/health` and `/ready` are aligned. `.http` should add a not-ready `503` scenario when testable. |
| test plan vs implementation plan | Partial | `06-test-plan.md`, `07-implementation-plan.md`, `13-springboot-testing-playbook.md` | Three different TDD sequences are present. Choose one canonical per-behavior loop. |
| implementation plan vs final design freeze | Mostly pass | `07-implementation-plan.md`, `15-slice-1-design-freeze.md` | Scope, endpoints, in-memory persistence, custom readiness, and FastAPI deferral align. Scaffold/toolchain details are still missing. |
| deferred scope vs checklist and design freeze docs | Partial | `05-api-design-checklist.md`, `02-use-cases.md`, `15-slice-1-design-freeze.md` | Checklist and freeze are clear, but older use-case/open-question docs remain broader. |
| shared error contract vs OpenAPI ProblemDetail examples | Pass | `shared-error-contract.md`, `partner-source.v1.yaml` | ProblemDetail fields, `correlationId`, and current error codes align. Older verification report is stale. |

## 5. Best-Practice Assessment

### API design

Strengths:

- Contract-first design is explicit.
- `/api/v1` versioning is used for domain APIs.
- Resource-oriented URLs are used instead of action-style endpoints.
- OpenAPI defines stable request/response DTOs, pagination parameters for list-like reads, status codes, and ProblemDetail errors.
- Deferred endpoints are explicit in the design freeze.

Gaps:

- Stale prose examples in `04-api-contract.md` can mislead implementation.
- `partner-source.openapi.md` is stale compared with the YAML.
- Manual `.http` coverage needs a few more negative paths.
- Spectral/local linting is too light to catch project-specific drift.

### Spring Boot architecture

Strengths:

- Controller/service/repository/domain/DTO/error boundaries are planned.
- DTOs are kept separate from internal domain/storage objects.
- Domain policies are named for status transitions and assignment authorization.
- Centralized ProblemDetail error handling is expected.
- In-memory repositories behind interfaces are explicitly chosen for Slice 1.
- Custom `/health` and `/ready` are intentionally chosen over Actuator for the first slice.

Gaps:

- Package structure is inconsistent: `07-implementation-plan.md` recommends layer folders, while `12-springboot-api-fundamentals.md` recommends feature-based packages.
- Spring fundamentals still foreground JPA entities and `JpaRepository`, which conflicts with the in-memory-first decision.
- Scaffold/toolchain decision is missing.
- Validation taxonomy needs to be frozen before controller work starts.

### Testing and TDD

Strengths:

- Test levels are well named: domain, service, controller, repository behavior, integration, contract, and manual checks.
- Domain-policy tests are correctly proposed first.
- ProblemDetail assertions, timeline ordering, assignment authorization, and seed-backed tests are planned.
- Manual `.http` file has expected status and field comments for the main flows.

Gaps:

- Invalid-transition fixture is ambiguous because assignment authorization may fire first.
- Three TDD ordering variants exist across the docs.
- Contract test plan is too broad to be actionable.
- Negative-path coverage is incomplete for missing driver on POST, invalid status event, malformed body, and readiness `503`.
- `DELIVERY_ATTEMPTED` is in the enum and transition notes, but the test plan does not clearly pin it down.

### CI/CD

Strengths:

- GitHub Actions is correctly recommended first.
- First pipeline is appropriately small in concept: checkout, setup Java, run tests.
- Deployment is deferred.
- `mvn -B verify` is a reasonable first command once Maven is confirmed.
- CI growth plan stages OpenAPI validation later.

Gaps:

- Maven/project root/wrapper are not pinned yet.
- Artifact upload appears in the beginner workflow even though the module has not been scaffolded.
- Acceptance gates do not yet include local `mvn -B verify`, GitHub Actions passing, OpenAPI validation, or future contract/regression jobs.

## 6. Specialist Findings

### Plan Consistency Agent

- Severity: blocker
- Area: Implementation sequence
- Evidence: `03-implementation-sequence.md` includes FastAPI in the first vertical slice; `07-implementation-plan.md` and `15-slice-1-design-freeze.md` defer FastAPI until Spring Boot Slice 1 is stable.
- Issue: The program-level sequence contradicts the final partner-source implementation plan.
- Why it matters: Work can split into a second runtime before the primary Spring Boot behavior is stable.
- Recommended fix: Update `00-program-plan/00-index.md`, `03-implementation-sequence.md`, and ADR-0005 so the order is: Spring Boot full Slice 1 -> automated/manual tests -> first CI -> FastAPI parity later.

- Severity: major
- Area: ADR status
- Evidence: `02-module-map.md` and `07-implementation-plan.md` rely on module boundaries and contract-first rules; ADR-0001, ADR-0003, and ADR-0004 remain `Proposed`.
- Issue: Foundational boundaries are used as binding even though their ADR status is not accepted.
- Why it matters: Governance status conflicts with implementation readiness.
- Recommended fix: Accept ADR-0001, ADR-0003, and ADR-0004 or mark the design freeze as conditional on them.

- Severity: major
- Area: Deferred scope
- Evidence: `02-use-cases.md` keeps delivery attempts, support summaries, and exceptions in practical/MVP language; `15-slice-1-design-freeze.md` defers them.
- Issue: Older use-case language conflicts with the frozen Slice 1 boundary.
- Why it matters: Scope creep can enter during implementation.
- Recommended fix: Rewrite use cases with explicit `Slice 1`, `Slice 2`, and `later` labels.

### API Contract Agent

- Severity: major
- Area: Seed/example alignment
- Evidence: `04-api-contract.md` shows `activeAssignmentCount: 3`; seed data, OpenAPI, test plan, and `.http` expect `2`.
- Issue: The prose API contract example is stale.
- Why it matters: Implementers can copy the wrong expected value.
- Recommended fix: Normalize all examples to `activeAssignmentCount = 2`, two assignment items, and `totalItems = 2`.

- Severity: major
- Area: Deferred endpoint clarity
- Evidence: `02-use-cases.md` includes delivery attempts, exceptions, and support summaries in broad MVP scope; `partner-source.v1.yaml` and `15-slice-1-design-freeze.md` exclude them from Slice 1.
- Issue: Product/use-case docs read broader than the executable contract.
- Why it matters: Implementation may add endpoints not present in OpenAPI.
- Recommended fix: Make the API summary distinguish backlog endpoints from the Slice 1 minimum.

- Severity: minor
- Area: OpenAPI quality gate
- Evidence: Current linting is lighter than the project-specific rules implied by `shared-error-contract.md`, `06-test-plan.md`, and `partner-source.v1.yaml`.
- Issue: Lint can pass while error envelope, pagination, or example/seed drift remains.
- Why it matters: CI may give false confidence.
- Recommended fix: Extend OpenAPI linting with project rules for ProblemDetail, pagination, required error responses, and examples.

### Spring Boot Architecture Agent

- Severity: blocker
- Area: Status transition policy
- Evidence: `03-domain-model.md` allows broader transitions, including cancellation paths; `04-api-contract.md` has a narrower initial transition table; `15-slice-1-design-freeze.md` says domain rules are frozen.
- Issue: The canonical `StatusTransitionPolicy` matrix is not singular.
- Why it matters: The first domain-policy test can be written two different ways.
- Recommended fix: Declare the canonical Slice 1 transition table in `15-slice-1-design-freeze.md` and align domain, API contract, tests, seed cases, and OpenAPI notes to it.

- Severity: major
- Area: Repository/persistence boundary
- Evidence: ADR-0006 chooses repository interfaces with in-memory implementations; `12-springboot-api-fundamentals.md` foregrounds JPA entities and `JpaRepository`.
- Issue: Beginner-facing guidance can pull Slice 1 toward JPA too early.
- Why it matters: It undermines the intended contract/domain-first focus.
- Recommended fix: State clearly that Slice 1 uses plain repository interfaces plus in-memory adapters; move JPA guidance to a later H2/PostgreSQL section.

- Severity: major
- Area: Package boundaries
- Evidence: `07-implementation-plan.md` recommends layer packages; `12-springboot-api-fundamentals.md` recommends feature-based packages.
- Issue: Two package structures are presented as recommended.
- Why it matters: Code can start disorganized on day one.
- Recommended fix: Pick one structure. Recommended: feature-based packages under `order`, `driver`, and `assignment`, plus `shared.error`, `shared.config`, and `seed`.

- Severity: major
- Area: Validation and exception handling
- Evidence: `shared-error-contract.md` separates malformed request shape from semantic failures; `06-test-plan.md` still allows missing `driverId` to be `400` or `422`.
- Issue: Validation boundary is not frozen.
- Why it matters: `@Valid`, enum binding, domain exceptions, and `@RestControllerAdvice` mappings can drift.
- Recommended fix: Add validation taxonomy: malformed path/query/body = `400 INVALID_REQUEST`; semantically invalid event = `422 INVALID_STATUS_EVENT`; lifecycle violation = `409 INVALID_STATUS_TRANSITION`.

### Testing And TDD Agent

- Severity: blocker
- Area: Seed-backed negative tests
- Evidence: `05-data-model-and-seed-data.md` makes `ASN-3003` a completed assignment for `ORD-1003`; `06-test-plan.md` says completed assignments do not count as active unless deliberately allowed; `04-api-contract.md` validates assignment before transition.
- Issue: The invalid-transition test for `ORD-1003 -> OUT_FOR_DELIVERY` may return `403 ORDER_NOT_ASSIGNED_TO_DRIVER` before `409 INVALID_STATUS_TRANSITION`.
- Why it matters: A core lifecycle negative test may fail for the wrong reason.
- Recommended fix: Define whether completed assignments authorize historical corrections, or add an active assigned delivered-order fixture dedicated to the invalid-transition test.

- Severity: major
- Area: Contract tests
- Evidence: `90-shared/evaluation/contract-test-plan.md` lists broad boundaries; `06-test-plan.md` and `shared-error-contract.md` define concrete schema/error assertions.
- Issue: Contract test plan is not actionable enough.
- Why it matters: BFF compatibility can drift while unit/controller tests pass.
- Recommended fix: Add endpoint-by-endpoint contract checks for success schema, error schema, status code, enum values, ProblemDetail, `correlationId`, and OpenAPI validation.

- Severity: major
- Area: Negative paths and manual requests
- Evidence: OpenAPI defines POST errors for `400`, `403`, `404`, `409`, `422`; `.http` covers only a subset.
- Issue: Missing manual/planned coverage for missing driver on status-event creation, invalid status event, malformed body, invalid assignment query, and readiness `503`.
- Why it matters: These are client-visible contract failures.
- Recommended fix: Add `.http`, controller, service, and integration coverage for those cases.

- Severity: major
- Area: TDD implementation order
- Evidence: `06-test-plan.md`, `07-implementation-plan.md`, and `13-springboot-testing-playbook.md` present different orderings.
- Issue: The implementation path is not canonical.
- Why it matters: Work can bounce between framework wiring and behavior tests.
- Recommended fix: Use one loop: OpenAPI/controller red test -> domain/service red test -> repository/seed behavior -> integration -> contract check.

### CI/CD Agent

- Severity: major
- Area: Java setup and test command
- Evidence: `14-cicd-pipeline-guide.md` assumes Maven, JDK 21, and `mvn -B verify`; no implementation scaffold, `pom.xml`, Maven wrapper, or `.github` workflow exists yet.
- Issue: CI guidance is correct in shape but not anchored to a real project entrypoint.
- Why it matters: First CI run may fail from the wrong directory or unreproducible local assumptions.
- Recommended fix: After scaffold decision, document exact entrypoint, wrapper command, Java release, and cache path.

- Severity: major
- Area: Staged quality gates
- Evidence: `90-shared/evaluation/acceptance-gates.md` has only four partner-source behavior bullets; implementation done criteria require all endpoints, seed scenarios, manual `.http`, ProblemDetail, readiness, and commands.
- Issue: Shared acceptance gates are weaker than module done criteria.
- Why it matters: Slice 1 could be accepted without being merge-safe.
- Recommended fix: Add staged gates for local test command, PR GitHub Actions pass, OpenAPI validation, and later contract/regression jobs.

- Severity: minor
- Area: First pipeline scope
- Evidence: `07-implementation-plan.md` says first workflow should be checkout/setup-java/run tests; `14-cicd-pipeline-guide.md` also uploads artifacts.
- Issue: The beginner workflow includes packaging artifact work before the jar path is confirmed.
- Why it matters: It adds avoidable early CI debugging.
- Recommended fix: Make workflow v1 only checkout, setup Java, and run tests; add artifact upload after packaging is stable.

### Implementation Readiness Agent

- Severity: blocker
- Area: Spring Boot scaffold/toolchain
- Evidence: `phase_2/README.md` is planning-only; no implementation module, `pom.xml`, wrapper, or `src/main` tree is defined; CI guide says "Assuming Maven".
- Issue: The implementation target is not concretely defined.
- Why it matters: A developer still has to decide module path, Maven vs Gradle, Java version, Spring Boot version, dependencies, base package, and commands before coding.
- Recommended fix: Add a short accepted scaffold decision: module path, Java 21, Maven, Spring Boot version, dependencies, base package, `./mvnw test`, and `./mvnw spring-boot:run`.

- Severity: major
- Area: Stale open questions
- Evidence: `04-open-questions.md` still asks in-memory vs H2 and OpenAPI-first questions; ADR-0006 and the checklist already resolve them.
- Issue: Resolved decisions are still presented as open.
- Why it matters: Settled choices may be reopened.
- Recommended fix: Replace open questions with resolved/deferred statuses and decision links.

- Severity: major
- Area: Evaluation gates
- Evidence: `acceptance-gates.md` is much smaller than `07-implementation-plan.md` done criteria.
- Issue: Shared gates do not enforce all frozen Slice 1 behavior.
- Why it matters: Governance can mark the slice complete too early.
- Recommended fix: Sync acceptance gates to the design freeze and done criteria.

## 7. Blockers

1. Spring Boot scaffold/toolchain is not pinned.

Required decision:

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

2. Canonical Slice 1 status transition table is inconsistent.

Required decision:

```text
One status transition table must govern StatusTransitionPolicyTest, service behavior, API prose, seed data, and OpenAPI notes.
```

3. Invalid-transition seed/test fixture can hit the wrong error first.

Required decision:

```text
Either allow completed assignment ASN-3003 to authorize the invalid-transition check,
or add a dedicated active assigned delivered-order fixture for the 409 test.
```

4. Program sequence still contradicts the design freeze on FastAPI timing.

Required decision:

```text
Spring Boot Slice 1 must complete before FastAPI parity starts, unless the design freeze is deliberately reopened.
```

## 8. Major Improvements

- Accept or make binding ADR-0001, ADR-0003, and ADR-0004.
- Update `00-program-plan/04-open-questions.md` with resolved/deferred statuses.
- Refresh or supersede `01-partner-source/10-api-design-verification-report.md`.
- Fix stale examples in `01-partner-source/04-api-contract.md`, especially `activeAssignmentCount`, assignment counts, and created event IDs.
- Update `90-shared/contracts/partner-source.openapi.md` so it points to the canonical YAML or lists all Slice 1 endpoints.
- Add missing manual `.http` negative requests.
- Expand `90-shared/evaluation/contract-test-plan.md`.
- Expand `90-shared/evaluation/acceptance-gates.md`.
- Pick one Spring Boot package structure.
- Clarify in-memory repository testing vs later `@DataJpaTest`.
- Add validation taxonomy for `400`, `409`, and `422`.

## 9. Minor Improvements

- Add a note that Spring Boot Actuator is intentionally deferred even though learning docs mention health controllers or Actuator.
- Add a note to CI guide that artifact upload is phase 2 after test workflow is stable.
- Add a future CI roadmap table for partner-source Java, OpenAPI lint, FastAPI parity, RAG evaluation, BFF contracts, and frontend tests.
- Add project-specific OpenAPI lint rules for ProblemDetail, pagination, required error responses, and example coverage.
- Decide whether `DELIVERY_ATTEMPTED` should be explicitly tested in Slice 1 or marked enum-only/backlog behavior.

## 10. Implementation Readiness Verdict

Spring Boot Slice 1 should not begin as a clean final handoff yet.

The best current verdict is:

```text
Behavioral plan: close.
Canonical OpenAPI contract: usable.
Final planning pack: not ready.
Implementation handoff: blocked by scaffold, transition-policy, fixture, and sequence cleanup.
```

After the blockers are fixed, the first coding step should be:

```text
1. Create the Spring Boot scaffold using the accepted toolchain decision.
2. Write StatusTransitionPolicyTest.
3. Write AssignmentAuthorizationPolicyTest.
4. Continue with one behavior loop:
   OpenAPI/controller red test
   -> domain/service red test
   -> repository/seed behavior
   -> integration test
   -> contract/manual check
```

## 11. Recommended Patch Plan

Do not apply these automatically unless explicitly requested.

1. Patch `00-program-plan/03-implementation-sequence.md`.
   - Make Spring Boot full Slice 1 the first implementation milestone.
   - Move FastAPI parity after Spring Boot tests, manual checks, and first CI.

2. Patch ADR status and implementation-order governance.
   - Accept ADR-0001, ADR-0003, and ADR-0004 or state they are binding for Slice 1.
   - Update ADR-0005 to match FastAPI deferral.

3. Add a scaffold/toolchain decision document.
   - Suggested path: `99-decisions/ADR-0008-spring-boot-scaffold-toolchain.md`.
   - Include Java 21, Maven, Spring Boot version, wrapper usage, module path, base package, dependencies, and commands.

4. Patch `15-slice-1-design-freeze.md`.
   - Add the canonical transition table.
   - Clarify `DELIVERY_ATTEMPTED` behavior.
   - Link the scaffold decision.

5. Patch `03-domain-model.md`, `04-api-contract.md`, and `06-test-plan.md`.
   - Align the transition table.
   - Fix the invalid-transition fixture.
   - Normalize stale examples.
   - Freeze validation taxonomy.

6. Patch `05-data-model-and-seed-data.md`.
   - Ensure the invalid-transition seed case reaches `INVALID_STATUS_TRANSITION`.
   - Keep failed delivery on `ORD-1004` or Slice 2.

7. Patch `02-use-cases.md` and `09-use-case-resource-map.md`.
   - Label each use case/resource as Slice 1, Slice 2, or later.
   - Keep deferred endpoints out of the first implementation surface.

8. Patch shared contract/evaluation docs.
   - Update `partner-source.openapi.md`.
   - Expand `contract-test-plan.md`.
   - Expand `acceptance-gates.md`.
   - Add missing manual `.http` cases.

9. Patch Spring Boot learning docs.
   - Choose feature-based or layer-based packages.
   - Move JPA/`JpaRepository`/`@DataJpaTest` to the later persistence migration path.

10. Patch CI/CD guide after scaffold decision.
    - Use exact module path and wrapper command.
    - Keep workflow v1 to checkout/setup-java/test.
    - Add OpenAPI lint and artifact upload as staged follow-ups.
