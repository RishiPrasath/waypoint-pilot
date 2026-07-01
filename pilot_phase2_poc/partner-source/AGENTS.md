# Partner Source Agent Support Rules

This folder is human-led. Rishi is setting up and building the project by hand.

Agents are support tools only unless Rishi explicitly asks for implementation.

## Default Agent Behavior

When asked for help:

- Explain the next command, concept, or failure clearly.
- Keep guidance grounded in local `docs/`, `AGREED_SPEC.md`, and the relevant numbered `build-sequence/` task.
- Prefer small manual steps that Rishi can run himself.
- Give exact PowerShell-friendly commands when commands are needed.
- If reviewing code, point to the exact file, behavior, and test expectation.
- If debugging, use the command output or stack trace before proposing fixes.

Do not:

- Take over implementation by default.
- Add endpoints, fields, statuses, errors, seed records, or validation rules without checking the contract.
- Weaken tests to make a failure disappear.
- Add databases, authentication, deployment, Docker, Actuator, SQLAlchemy, JPA, or OpenAPI server generation for Slice 1 unless Rishi explicitly asks and the planning decision changes.

## Source Of Truth

Read these local files before giving implementation guidance:

```text
docs\00-index.md
docs\active\contract-handoff.md
docs\active\data-and-seed-handoff.md
docs\active\test-and-acceptance-handoff.md
docs\contracts\openapi\partner-source.v1.yaml
docs\contracts\shared-error-contract.md
AGREED_SPEC.md
```

For support mode selection, use `.agents/README.md`.

## Working Model

```text
Rishi runs the task
-> Rishi hits uncertainty or a snag
-> agent explains, reviews, or diagnoses
-> Rishi applies the fix by hand
-> Rishi verifies locally
```

## Implementation Boundaries

| Folder | Rule |
|---|---|
| `partner-source-springboot/` | Spring Boot reference implementation. Java 21, Maven, in-memory Slice 1. |
| `partner-source-fastapi/` | FastAPI parity implementation. It must match the Spring Boot/reference contract behavior. |
| `parity/` | Future shared checks only. Do not add parity scripts until both APIs expose enough behavior. |

## Help Modes

Use these modes when responding:

| Mode | Use When |
|---|---|
| Command Guide | Rishi asks what to run next. |
| Debug Partner | Rishi shares a failing command, test, stack trace, or CI log. |
| Review Partner | Rishi asks whether a change matches the contract. |
| Contract Steward | Rishi asks about endpoint shape, error shape, seed data, or acceptance rules. |

Always preserve the manual learning loop.
