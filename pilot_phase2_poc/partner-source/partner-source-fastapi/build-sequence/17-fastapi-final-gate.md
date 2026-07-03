# 17 - FastAPI Final Gate

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Confirm the FastAPI parity implementation is complete enough for shared parity checks.

## Source Docs To Read

- `../../AGREED_SPEC.md`
- `../../CONTRACT_SYNC.md`
- `../../docs/active/test-and-acceptance-handoff.md`
- `../../partner-source-springboot/build-sequence/17-springboot-final-gate.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

No new feature test by default.

This task runs the complete test suite and documentation audits.

If the final review exposes a concrete behavior gap, add a focused test in the matching earlier test folder first:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for If the final review exposes a concrete behavior gap, add a focused test in the matching earlier test folder first.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/domain/
tests/repositories/
tests/services/
tests/api/
tests/integration/

```

Then run:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `python -m pytest`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest

```
## File Map

No new code. Only fix proven gaps with tests first.

## Exact Code

No new feature code should be created in this task.

Run this final local gate from `partner-source-fastapi`:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `partner-source-fastapi`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest
```

Run this doc/template audit from `partner-source`:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `partner-source`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
$root = "C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi\build-sequence"
$expected = @(
  "Status",
  "Purpose",
  "Source Docs To Read",
  "Prereqs",
  "Tests To Write First",
  "File Map",
  "Exact Code",
  "Commands To Run",
  "Done Criteria",
  "Common Mistakes",
  "Stop / Do Not Add",
  "Change Notes"
)

Get-ChildItem -LiteralPath $root -Filter "*.md" | Sort-Object Name | ForEach-Object {
  $heads = @(Select-String -Path $_.FullName -Pattern "^## " | ForEach-Object { $_.Line -replace "^## ", "" })
  if ($heads.Count -ne $expected.Count) {
    throw "$($_.Name) has $($heads.Count) sections, expected $($expected.Count)"
  }
  for ($i = 0; $i -lt $expected.Count; $i++) {
    if ($heads[$i] -ne $expected[$i]) {
      throw "$($_.Name) section $($i + 1) expected '$($expected[$i])' but got '$($heads[$i])'"
    }
  }
}

```

Run this placeholder audit:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Run this placeholder audit.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
$patterns = @(
  "Use the file map " + "above",
  "implementation " + "target",
  "Keep the first implementation small " + "enough"
)

foreach ($pattern in $patterns) {
  rg --fixed-strings $pattern partner-source-fastapi/build-sequence
}

```

Expected result:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for `No matches.`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
No matches.

```

Run this Git check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Run this Git check.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
git diff --name-only -- partner-source-fastapi

```

Review every changed file before marking the FastAPI track complete.

## Commands To Run

Run from `partner-source-fastapi`:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `partner-source-fastapi`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
python -m pytest
```

Run from `partner-source`:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `partner-source`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source
$root = "C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi\build-sequence"
$expected = @("Status","Purpose","Source Docs To Read","Prereqs","Tests To Write First","File Map","Exact Code","Commands To Run","Done Criteria","Common Mistakes","Stop / Do Not Add","Change Notes")
Get-ChildItem -LiteralPath $root -Filter "*.md" | Sort-Object Name | ForEach-Object {
  $heads = @(Select-String -Path $_.FullName -Pattern "^## " | ForEach-Object { $_.Line -replace "^## ", "" })
  if ($heads.Count -ne $expected.Count) { throw "$($_.Name) has wrong section count" }
  for ($i = 0; $i -lt $expected.Count; $i++) {
    if ($heads[$i] -ne $expected[$i]) { throw "$($_.Name) section $($i + 1) is wrong" }
  }
}

```

Run from `partner-source` after reviewing intentional diffs:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `partner-source`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
git diff --name-only -- partner-source-fastapi

```

## Done Criteria

FastAPI is ready when this statement is true:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for FastAPI is ready when this statement is true.
- Why it exists: It keeps the task deterministic and prevents agents from filling gaps with invented behavior.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
The FastAPI implementation matches the Partner Source Slice 1 contract and Spring Boot reference behavior.
```

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add new endpoints here.
- Do not add deployment, Docker, databases, security, or auth.
- Do not create parity scripts until both implementations expose enough behavior and the planning decision changes.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Added explicit final-gate commands and stop boundaries.
- Marked done after all FastAPI Slice 1 endpoints were implemented and `python -m pytest` passed.
