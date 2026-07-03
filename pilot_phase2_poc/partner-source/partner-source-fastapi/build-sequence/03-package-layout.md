# 03 - Package Layout

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Prepare the FastAPI module layout before adding real behavior.

## Source Docs To Read

- `../../docs/support/implementation-schematic-and-task-sequence.md`
- `../../docs/active/implementation-mapping.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

No new behavior test for this task.

This is folder/package preparation. Keep the existing smoke test from task 01 unchanged:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for This is folder/package preparation. Keep the existing smoke test from task 01 unchanged.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/test_app.py
```

Run it after creating packages:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Run it after creating packages.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/test_app.py
```

Do not create placeholder tests just to fill folders.
## File Map

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/`, `__init__.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

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

## Exact Code

Create these Python package marker files:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for Create these Python package marker files.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/__init__.py
app/api/__init__.py
app/schemas/__init__.py
app/domain/__init__.py
app/repositories/__init__.py
app/services/__init__.py
app/seed/__init__.py
app/errors/__init__.py

```

Each `__init__.py` file should be empty for now.

Keep `app/main.py` as:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/main.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from fastapi import FastAPI


def create_app() -> FastAPI:
    return FastAPI(title="Waypoint Partner Source API", version="1.0.0")


app = create_app()

```

Create these test folders:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for Create these test folders.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
tests/domain/
tests/repositories/
tests/services/
tests/api/
tests/contract/

```

If Git needs to track an otherwise empty test folder, add a `.gitkeep` file in that folder. Do not put test logic in `.gitkeep`.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
New-Item -ItemType Directory -Force -Path `
  app\api,app\schemas,app\domain,app\repositories,app\services,app\seed,app\errors,`
  tests\domain,tests\repositories,tests\services,tests\api,tests\contract

```

Make sure each package folder has `__init__.py`.

Then run:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `python -m pytest`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest
```

## Done Criteria

- [x] Package layout exists.
- [x] Scaffold test still passes.
- [x] No placeholder behavior was added just to fill folders.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add routers before domain policies.
- Do not add repositories before seed data tests.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
