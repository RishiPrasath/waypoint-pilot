# FastAPI Build Sequence

## Status

- Status: Active
- Last Updated: 2026-07-06

## Purpose

This is the human build book for the FastAPI Partner Source parity implementation.

FastAPI must match the same local contract and the Spring Boot reference behavior. It must not become a second API design.

## Source Docs To Read

**Block Explanation**

- What this block does: Lists the exact local docs to read before using this task.
- Why it exists: It anchors the task in the agreed spec and handoff docs before any implementation choice is made.
- How to read it: Open the paths in order and treat `AGREED_SPEC.md` plus active docs as the authority if older notes disagree.

```text
..\..\AGREED_SPEC.md
..\..\docs\00-index.md
..\..\docs\active\contract-handoff.md
..\..\docs\active\data-and-seed-handoff.md
..\..\docs\active\test-and-acceptance-handoff.md
..\..\docs\active\auth-access-control-plan.md
..\..\docs\contracts\openapi\partner-source.v1.yaml
..\..\docs\contracts\shared-error-contract.md
..\..\partner-source-springboot\build-sequence\00-index.md

```

## Prereqs

- Use this index only as the quick scan view.
- Treat each numbered task file as the source of truth for that task's status.
- If this index and a task file disagree, update the index after checking the task file.

## Tests To Write First

No test file is written for this index. Verification is a documentation consistency check.

## File Map

| Step | Task | Status | Outcome |
|---:|---|---|---|
| 01 | [Project setup](01-project-setup.md) | Done | FastAPI scaffold and first passing pytest. |
| 02 | [CI pipeline](02-ci-pipeline.md) | Done | GitHub Actions runs pytest. |
| 03 | [Package layout](03-package-layout.md) | Done | FastAPI package/test layout exists and `python -m pytest` passes. |
| 04 | [Status transition policy](04-status-transition-policy.md) | Done | Domain `OrderStatus` and transition policy implemented; transition tests and full suite pass. |
| 05 | [Assignment authorization policy](05-assignment-authorization-policy.md) | Done | Authorization rule mirrors Spring Boot and focused/full tests pass. |
| 06 | [Seed store and repositories](06-seed-store-and-repositories.md) | Done | Deterministic in-memory data layer exists. |
| 07 | [Health endpoint](07-health-endpoint.md) | Done | `GET /health` returns `UP`. |
| 08 | [Readiness endpoint](08-readiness-endpoint.md) | Done | `GET /ready` proves seed readiness. |
| 09 | [Order status lookup](09-order-status-lookup.md) | Done | First contract read endpoint works. |
| 10 | [ProblemDetail errors](10-problem-detail-errors.md) | Done | Shared error envelope is centralized. |
| 11 | [Order timeline](11-order-timeline.md) | Done | Chronological timeline endpoint works. |
| 12 | [Driver profile](12-driver-profile.md) | Done | Driver profile endpoint works. |
| 13 | [Driver assignments](13-driver-assignments.md) | Done | Assignment list endpoint works. |
| 14 | [Create status event](14-create-status-event.md) | Done | Write endpoint validates, appends, and mutates status. |
| 15 | [Integration tests](15-integration-tests.md) | Done | Full FastAPI flow is verified. |
| 16 | [Manual HTTP checklist](16-manual-http-checklist.md) | Done | Manual request matrix is covered by full-stack integration checks. |
| 17 | [FastAPI final gate](17-fastapi-final-gate.md) | Done | Implementation is ready for parity checks. |
| 18 | [Auth contract update](18-auth-contract-update.md) | Done | Auth errors, demo login, and protected-route expectations. |
| 19 | [Demo login and principal](19-demo-login-and-principal.md) | Done | Deterministic bearer-token login and principal model. |
| 20 | [Access policy and route guards](20-access-policy-and-route-guards.md) | Done | Protected routes enforce the access-control matrix. |
| 21 | [Status event principal migration](21-status-event-principal-migration.md) | Done | Status-event `driverId` cannot spoof another driver. |
| 22 | [Auth final gate](22-auth-final-gate.md) | Done | Full FastAPI auth slice verification. |

## Exact Code

Use this index to route agents and humans to the next task file.

Status legend:

| Status | Meaning |
|---|---|
| Not Started | Task has not begun yet. |
| In Progress | Work has started, but the task is not finished. |
| Blocked | The task cannot move forward yet. |
| Done | The task is complete and verified. |

Per-task rule:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for Per-task rule.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
read source docs and Spring Boot behavior
-> write the failing pytest
-> run the focused pytest and confirm the failure
-> implement the smallest code
-> run focused pytest
-> run python -m pytest
-> update the tracker

```

## Commands To Run

Run commands from:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Run commands from.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
```

If using `uv`:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `uv`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
uv run pytest
uv run uvicorn app.main:app --reload
```

If using a virtual environment:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for If using a virtual environment.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest
python -m uvicorn app.main:app --reload
```

## Done Criteria

- [x] Build order lists every numbered FastAPI task.
- [x] Task statuses mirror completed work through Task 22.
- [x] Default commands are PowerShell-friendly.
- [x] The index points to local source-of-truth docs.

## Common Mistakes

- Updating this index without updating the numbered task file.
- Treating FastAPI-generated OpenAPI as canonical.
- Marking a task done before focused and full tests pass.
- Adding behavior that Spring Boot and the agreed spec do not have.

## Stop / Do Not Add

- Do not add SQLAlchemy, Alembic, auth packages, background workers, Docker, deployment config, or OpenAPI server generation.
- Do not treat FastAPI's generated OpenAPI as canonical.
- Do not add behavior that Spring Boot and the agreed spec do not have.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Normalized this index to the shared build-sequence task template.
- Restored Tasks 03, 04, and 05 to `Done` based on verified implementation and passing tests.
- Updated Task 06 to `Done` to match the verified task file.
- Updated Tasks 07 and 08 to `Done` after focused and full FastAPI tests passed.
- Updated Tasks 09 through 17 to `Done` after focused, integration, and full FastAPI tests passed.
- Added Tasks 18 through 22 for the auth/access-control implementation slice.
- Updated Tasks 18 through 22 to `Done` after the full pytest suite and auth parity checks passed.
