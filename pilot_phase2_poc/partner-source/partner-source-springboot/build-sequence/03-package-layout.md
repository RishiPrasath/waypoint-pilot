# 03 - Package Layout

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Prepare the feature-based package structure before adding endpoint behavior.

## Source Docs To Read

- `../../docs/support/implementation-schematic-and-task-sequence.md`
- `../../docs/active/implementation-mapping.md`

## Prereqs

- Task 01 scaffold exists.
- Task 02 CI is green or locally reproducible.
- Package root remains `com.waypoint.partnersource`.

## Tests To Write First

No new behavior test for this task.

This is folder/package preparation. Keep the scaffold test from task 01 unchanged and run:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for This is folder/package preparation. Keep the scaffold test from task 01 unchanged and run.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd test
```

Do not create fake Java tests just to fill empty folders.
## File Map

Main folders under `src/main/java/com/waypoint/partnersource/`:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `src/main/java/com/waypoint/partnersource/`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
order/api/dto
order/domain
order/repository
order/service
driver/api/dto
driver/domain
driver/repository
driver/service
assignment/domain
assignment/repository
shared/error
shared/health
shared/seed

```

Test folders under `src/test/java/com/waypoint/partnersource/`:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `src/test/java/com/waypoint/partnersource/`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
order/domain
order/repository
order/service
order/api
driver/repository
driver/service
driver/api
assignment/domain
shared/health
shared/error
integration

```

## Exact Code

No Java behavior classes are required for this task.

PowerShell folder creation command:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for PowerShell folder creation command.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
New-Item -ItemType Directory -Force -Path `
  src\main\java\com\waypoint\partnersource\order\api\dto,`
  src\main\java\com\waypoint\partnersource\order\domain,`
  src\main\java\com\waypoint\partnersource\order\repository,`
  src\main\java\com\waypoint\partnersource\order\service,`
  src\main\java\com\waypoint\partnersource\driver\api\dto,`
  src\main\java\com\waypoint\partnersource\driver\domain,`
  src\main\java\com\waypoint\partnersource\driver\repository,`
  src\main\java\com\waypoint\partnersource\driver\service,`
  src\main\java\com\waypoint\partnersource\assignment\domain,`
  src\main\java\com\waypoint\partnersource\assignment\repository,`
  src\main\java\com\waypoint\partnersource\shared\error,`
  src\main\java\com\waypoint\partnersource\shared\health,`
  src\main\java\com\waypoint\partnersource\shared\seed

```

Empty folders may not be tracked by Git. Do not add fake classes just to preserve empty folders.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test
```

## Done Criteria

- [x] Main package structure exists.
- [x] Scaffold test still passes.
- [x] No placeholder behavior classes were added just to fill folders.

## Common Mistakes

- Creating packages under the wrong root.
- Adding placeholder classes just to make folders visible to Git.
- Putting assignment domain code under `order/domain`.

## Stop / Do Not Add

- Do not add controllers before domain policies.
- Do not add repository implementations before seed data tests.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Status marked done because the main package structure exists.
