# Partner Source Phase 2 Implementation Lane

This folder is the fresh implementation lane for the Waypoint Phase 2 Partner Source API.

You will build the code by hand from scratch. Agents are support tools only: use them for command help, explanation, debugging, or review when you ask.

## Folder Layout

```text
partner-source/
|-- README.md
|-- AGREED_SPEC.md
|-- MANUAL_BUILD_SEQUENCE.md
|-- CONTRACT_SYNC.md
|-- AGENTS.md
|-- .gitignore
|-- .agents/
|-- docs/
|-- parity/
|-- partner-source-springboot/
`-- partner-source-fastapi/
```

## Implementation Folders

| Folder | Purpose | Status |
|---|---|---|
| `partner-source-springboot/` | Spring Boot reference implementation. Build this first. | fresh, scaffold-ready |
| `partner-source-fastapi/` | FastAPI parity implementation. Build after the first Spring Boot proof path. | fresh, scaffold-ready |
| `parity/` | Future shared contract/parity checks for comparing both APIs. | docs only |

## Source Of Truth

The local `docs/` folder and `AGREED_SPEC.md` are the source of truth for this implementation lane.

Read these first:

```text
docs\00-index.md
docs\active\contract-handoff.md
docs\active\data-and-seed-handoff.md
docs\active\test-and-acceptance-handoff.md
docs\contracts\openapi\partner-source.v1.yaml
docs\contracts\shared-error-contract.md
AGREED_SPEC.md
```

Some `docs/support`, `docs/research`, and `docs/archive` files preserve older context. When there is a conflict, follow `AGREED_SPEC.md` and the files under `docs/active` and `docs/contracts`.

## Manual Build Path

Start here for the agreed behavior:

```text
AGREED_SPEC.md
```

Then use the numbered build books:

```text
partner-source-springboot\build-sequence\00-index.md
partner-source-fastapi\build-sequence\00-index.md
parity\build-sequence\00-index.md
```

Use the short tracker only as a progress dashboard:

```text
MANUAL_BUILD_SEQUENCE.md
```

The build order is:

```text
read agreed spec
-> check tools
-> Spring Boot scaffold
-> Spring Boot tiny test
-> Spring Boot CI proof
-> FastAPI scaffold
-> FastAPI tiny test
-> FastAPI CI proof
-> first real TDD slice
-> every endpoint in spec order
-> manual HTTP checklist
-> contract/parity checks
```

Older long-form manuals are archived under `docs\archive\manuals\` for history only. They are not execution authority.

## First Commands

Check the current folder:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source
Get-ChildItem -Force
```

When you are ready to scaffold Spring Boot, move into:

```powershell
cd .\partner-source-springboot
```

When you are ready to scaffold FastAPI, move into:

```powershell
cd .\partner-source-fastapi
```

## Rules

- Build by hand.
- Write tests before real behavior.
- Keep Spring Boot and FastAPI separate.
- Keep the contract shared.
- Do not add databases, authentication, deployment, Docker, or framework extras in Slice 1 unless the plan changes deliberately.
- Use `.agents/` personas for command help, debugging, review, contract stewardship, TDD coaching, and CI checks.
- Ask for help when a step is unclear or blocked.
