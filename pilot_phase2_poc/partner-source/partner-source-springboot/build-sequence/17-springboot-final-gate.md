# 17 - Spring Boot Final Gate

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Confirm the Spring Boot reference implementation is complete enough for FastAPI parity work.

This is a verification task, not a feature task.

## Source Docs To Read

- `../../AGREED_SPEC.md`
- `../../docs/active/test-and-acceptance-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../docs/contracts/shared-error-contract.md`

## Prereqs

- Tasks 01 through 16 are done.
- Manual checklist passes.
- GitHub Actions is green.

## Tests To Write First

No new feature test by default.

This task runs the complete test suite and documentation audits.

If final review exposes a behavior gap, add a focused test in the matching earlier test package first:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for If final review exposes a behavior gap, add a focused test in the matching earlier test package first.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/order/
src/test/java/com/waypoint/partnersource/driver/
src/test/java/com/waypoint/partnersource/assignment/
src/test/java/com/waypoint/partnersource/shared/
src/test/java/com/waypoint/partnersource/integration/

```

Then run:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `.\mvnw.cmd test`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd test

```
## File Map

No new application files.

Review:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `src/main/java/com/waypoint/partnersource/`, `src/test/java/com/waypoint/partnersource/`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
src/main/java/com/waypoint/partnersource/
src/test/java/com/waypoint/partnersource/
build-sequence/
.github/workflows/partner-source-springboot-ci.yml

```

## Exact Code

Run final local tests:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Run final local tests.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test
```

Run template audit from `partner-source`:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `partner-source`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
$root = "C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot\build-sequence"
$expected = @("Status","Purpose","Source Docs To Read","Prereqs","Tests To Write First","File Map","Exact Code","Commands To Run","Done Criteria","Common Mistakes","Stop / Do Not Add","Change Notes")
Get-ChildItem -LiteralPath $root -Filter "*.md" | Sort-Object Name | ForEach-Object {
  $heads = @(Select-String -Path $_.FullName -Pattern "^## " | ForEach-Object { $_.Line -replace "^## ", "" })
  if ($heads.Count -ne $expected.Count) { throw "$($_.Name) has wrong section count" }
  for ($i = 0; $i -lt $expected.Count; $i++) {
    if ($heads[$i] -ne $expected[$i]) { throw "$($_.Name) section $($i + 1) is wrong" }
  }
}

```

Run placeholder audit:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Run placeholder audit.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
$patterns = @("Use the file map " + "above", "implementation " + "target", "Keep the first implementation small " + "enough", "Code To " + "Implement")
foreach ($pattern in $patterns) { rg --fixed-strings $pattern partner-source-springboot/build-sequence }

```

Expected result: no matches.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd test
```

If verify is configured later:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for If verify is configured later.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd verify
```

## Done Criteria

- [x] All Slice 1 endpoints exist.
- [x] All response fields match OpenAPI.
- [x] All required seed scenarios exist.
- [x] Status transition policy matches the agreed table.
- [x] Assignment authorization matches agreed behavior.
- [x] Errors use ProblemDetail with `errorCode` and `correlationId`.
- [x] Manual HTTP checklist passes through automated integration coverage.
- [x] Local module tests are green.
- [x] No out-of-scope dependencies were added.

## Common Mistakes

- Treating this as a feature task.
- Skipping the manual checklist.
- Letting Spring Boot and FastAPI drift before parity checks.

## Stop / Do Not Add

- Do not add new endpoints here.
- Do not add deployment, Docker, databases, security, or Actuator.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized and final audit commands added.
- Marked done after all Spring Boot Slice 1 endpoints were implemented and `.\mvnw.cmd test` passed.
