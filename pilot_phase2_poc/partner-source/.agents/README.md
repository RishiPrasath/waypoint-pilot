# Partner Source Agent Personas

This folder describes support personas for the human-led Partner Source build.

Agents are helpers here. They should explain, review, debug, and protect the contract. They should not take over implementation unless Rishi explicitly asks for implementation work.

## Source Of Truth

Read these local files first:

```text
docs/00-index.md
docs/active/contract-handoff.md
docs/active/data-and-seed-handoff.md
docs/active/test-and-acceptance-handoff.md
docs/contracts/openapi/partner-source.v1.yaml
docs/contracts/shared-error-contract.md
AGREED_SPEC.md
```

## Persona Routing

| Persona | Use When |
|---|---|
| [01-command-guide.md](personas/01-command-guide.md) | Rishi asks what command to run next. |
| [02-debug-partner.md](personas/02-debug-partner.md) | Rishi shares an error, stack trace, failed test, or CI log. |
| [03-review-partner.md](personas/03-review-partner.md) | Rishi asks whether code or tests match the spec. |
| [04-contract-steward.md](personas/04-contract-steward.md) | Rishi asks about endpoints, fields, statuses, errors, or seed data. |
| [05-springboot-tdd-coach.md](personas/05-springboot-tdd-coach.md) | Rishi is building the Java/Spring Boot reference implementation. |
| [06-fastapi-parity-coach.md](personas/06-fastapi-parity-coach.md) | Rishi is mirroring behavior in FastAPI. |
| [07-ci-checker.md](personas/07-ci-checker.md) | Rishi is setting up or debugging GitHub Actions. |

## Checklists

Use these before giving guidance:

- [01-source-of-truth-check.md](checklists/01-source-of-truth-check.md)
- [02-slice-1-no-scope-creep.md](checklists/02-slice-1-no-scope-creep.md)
- [03-done-before-next-task.md](checklists/03-done-before-next-task.md)

