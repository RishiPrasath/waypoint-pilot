# 03 - Package Layout

## Purpose

Prepare the FastAPI module layout before adding real behavior.

## Source Docs To Read

- `../../docs/support/implementation-schematic-and-task-sequence.md`
- `../../docs/active/implementation-mapping.md`

## Tests To Write First

No behavior test. This is folder preparation after scaffold pytest and CI proof are green.

## Code To Implement

Create:

```text
app/
  __init__.py
  main.py
  api/__init__.py
  schemas/__init__.py
  domain/__init__.py
  repositories/__init__.py
  services/__init__.py
  seed/__init__.py
  errors/__init__.py
tests/
  domain/
  repositories/
  services/
  api/
  contract/
```

## Commands To Run

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
New-Item -ItemType Directory -Force -Path `
  app\api,app\schemas,app\domain,app\repositories,app\services,app\seed,app\errors,`
  tests\domain,tests\repositories,tests\services,tests\api,tests\contract
```

Make sure each package folder has `__init__.py`.

Then run:

```powershell
python -m pytest
```

## Done Criteria

- [ ] Package layout exists.
- [ ] Scaffold test still passes.
- [ ] No placeholder behavior was added just to fill folders.

## Stop / Do Not Add

- Do not add routers before domain policies.
- Do not add repositories before seed data tests.
