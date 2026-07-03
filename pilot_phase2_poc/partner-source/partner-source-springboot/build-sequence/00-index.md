# Spring Boot Build Sequence

## Status

- Status: In Progress
- Last Updated: 2026-07-03

## Purpose

Human build book for the Spring Boot Partner Source reference implementation.

Use this folder to move task by task, test first, while keeping Spring Boot as the reference behavior for FastAPI parity.

## Source Docs To Read

**Block Explanation**

- What this block does: Lists the exact local docs to read before using this task.
- Why it exists: It anchors the task in the agreed spec and handoff docs before any implementation choice is made.
- How to read it: Open the paths in order and treat `AGREED_SPEC.md` plus active docs as the authority if older notes disagree.

```text
../../AGREED_SPEC.md
../../docs/00-index.md
../../docs/active/contract-handoff.md
../../docs/active/data-and-seed-handoff.md
../../docs/active/test-and-acceptance-handoff.md
../../docs/contracts/openapi/partner-source.v1.yaml
../../docs/contracts/shared-error-contract.md

```

## Prereqs

- Run Maven commands from `partner-source-springboot`.
- Java must be `21`.
- Keep Slice 1 in-memory only.
- Use the numbered task files as execution authority.

## Tests To Write First

Each implementation task uses this loop:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for Each implementation task uses this loop.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
read source docs
-> write focused failing test
-> run focused test and confirm failure
-> implement smallest code
-> run focused test
-> run .\mvnw.cmd test
-> update task status

```

## File Map

| Step | Task | Status | Outcome |
|---:|---|---|---|
| 01 | [Project setup](01-project-setup.md) | Done | Spring Boot scaffold and first passing test. |
| 02 | [CI pipeline](02-ci-pipeline.md) | Done | GitHub Actions runs module tests. |
| 03 | [Package layout](03-package-layout.md) | Done | Feature-based package structure exists. |
| 04 | [Status transition policy](04-status-transition-policy.md) | Done | Domain status transition policy exists with tests. |
| 05 | [Assignment authorization policy](05-assignment-authorization-policy.md) | Done | Driver/order authorization policy exists with tests. |
| 06 | [Seed store and repositories](06-seed-store-and-repositories.md) | Done | Deterministic in-memory data layer exists. |
| 07 | [Health endpoint](07-health-endpoint.md) | Done | `GET /health` returns `UP`. |
| 08 | [Readiness endpoint](08-readiness-endpoint.md) | Done | `GET /ready` proves seed readiness. |
| 09 | [Order status lookup](09-order-status-lookup.md) | Done | First contract read endpoint works. |
| 10 | [ProblemDetail errors](10-problem-detail-errors.md) | Done | Shared error envelope is centralized. |
| 11 | [Order timeline](11-order-timeline.md) | Done | Chronological timeline endpoint works. |
| 12 | [Driver profile](12-driver-profile.md) | Done | Driver profile endpoint works. |
| 13 | [Driver assignments](13-driver-assignments.md) | Done | Assignment list endpoint works. |
| 14 | [Create status event](14-create-status-event.md) | Done | Write endpoint validates, appends, and mutates status. |
| 15 | [Integration tests](15-integration-tests.md) | Done | Full Spring Boot flow is verified. |
| 16 | [Manual HTTP checklist](16-manual-http-checklist.md) | Done | Manual request matrix is covered by full-stack integration checks. |
| 17 | [Spring Boot final gate](17-springboot-final-gate.md) | Done | Reference implementation is ready for FastAPI parity. |

## Exact Code

Use this index to route humans and agents to the next task file.

Allowed task statuses:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for Allowed task statuses.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
Not Started
In Progress
Blocked
Done

```

Default command location:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Default command location.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot

```

Focused test pattern:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Focused test pattern.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd -Dtest=ClassNameTest test

```

Full test:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Full test.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd test

```

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
java -version
.\mvnw.cmd -v
.\mvnw.cmd test

```

## Done Criteria

- [ ] Every task file follows the shared 12-section template.
- [ ] Every task has concrete files, code direction, commands, and stop rules.
- [x] Index statuses match actual completed work through Task 17.
- [ ] No deferred Slice 1 technology is introduced.

## Common Mistakes

- Marking done before focused and full tests pass.
- Running Maven with Java 17 when `pom.xml` targets Java 21.
- Leaving index status stale after a task changes.

## Stop / Do Not Add

- Do not add JPA, H2, PostgreSQL, Spring Security, Actuator, Docker, deployment config, or OpenAPI server generation.
- Do not add FastAPI code here.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Normalized to the shared build-task template.
- Updated task statuses for tasks 03, 04, and 05 based on existing Spring Boot files/tests.
- Updated Task 06 to `Done` to match the verified task file.
- Updated Task 07 and Task 08 to `Done` after focused tests and the full Maven suite passed.
- Updated Task 09 to `Done` after focused tests and the full Maven suite passed.
- Updated Task 10 to `Done` after focused tests and the full Maven suite passed.
- Updated Tasks 11 through 17 to `Done` after endpoint, mutation, and integration coverage passed.
