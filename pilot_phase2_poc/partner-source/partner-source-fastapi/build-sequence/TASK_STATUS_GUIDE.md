# Build Sequence Status Guide

## Status

- Status: Active
- Last Updated: 2026-07-03

## Purpose

Use this guide to keep the FastAPI build book readable for humans and agents.

Every file in this folder should follow the shared task template so agents can find status, prereqs, tests, file ownership, exact implementation hints, verification commands, and stop rules without guessing.

## Source Docs To Read

- `00-index.md`
- `../../AGREED_SPEC.md`
- `../../docs/active/test-and-acceptance-handoff.md`

## Prereqs

- Check the task's current `## Status` block before giving implementation guidance.
- Check the task's `## Done Criteria` before marking it complete.
- Keep this guide aligned with the section template used by the task files.

## Tests To Write First

No automated tests.

This is a documentation governance file.

The verification for this file is the build-sequence template audit in task 17.

## File Map

Every markdown file in this folder must use this section order:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for Every markdown file in this folder must use this section order.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
Status
Purpose
Source Docs To Read
Prereqs
Tests To Write First
File Map
Exact Code
Commands To Run
Done Criteria
Common Mistakes
Stop / Do Not Add
Change Notes

```

## Exact Code

Every fenced block must be introduced by a short explanation wrapper with:

- `What this block does`
- `Why it exists`
- `How to read it`

This applies to code, tests, commands, file maps, expected failures, and response examples. The wrapper belongs before the opening fence, never inside the fenced block.

When a task starts, set:

- `Status: In Progress`
- `Last Updated` to today's date

When a task is finished and verified, set:

- `Status: Done`
- check off the done criteria
- add a short `Change Notes` entry if the implementation drifted from the original draft

If a task is blocked, set:

- `Status: Blocked`
- describe the blocker in one sentence
- leave the original acceptance criteria intact

## Commands To Run

Use this PowerShell check from the build-sequence folder to inspect template headings:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Use this PowerShell check from the build-sequence folder to inspect template headings.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Get-ChildItem -Filter *.md | ForEach-Object {
  $_.Name
  Select-String -Path $_.FullName -Pattern '^## ' | ForEach-Object { $_.Line }
}

```

## Done Criteria

- [x] The required section order is listed in this guide.
- [x] The status update rules are explicit.
- [x] The per-code-block explanation rule is explicit.
- [x] The guide explains how to check the folder structure.

## Common Mistakes

- Skipping `## File Map` and forcing agents to infer paths.
- Skipping `## Exact Code` and leaving the next implementation step unclear.
- Putting explanation text inside a fenced code block instead of before the opening fence.
- Updating the index while leaving a task file stale.
- Asking for confirmation when a task is clearly complete and verified.

## Stop / Do Not Add

- Do not create new status names unless the index legend is updated too.
- Do not mark a task done without focused and full verification.
- Do not weaken done criteria to make a task look complete.
- Do not add code blocks without the explanation wrapper.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Normalized this guide to the same template required for every file in this folder.
