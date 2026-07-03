# Build Sequence Status Guide

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Explain how to update Spring Boot build-sequence task status markers consistently.

## Source Docs To Read

- `00-index.md`
- `../../AGREED_SPEC.md`
- `../../docs/active/test-and-acceptance-handoff.md`

## Prereqs

- Use the same status vocabulary in every task file.
- Update the task file and `00-index.md` together.
- Only mark a task done after focused and full verification pass.

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
- add a short `Change Notes` entry if implementation drifted from the original draft

If a task is blocked, set:

- `Status: Blocked`
- describe the blocker in one sentence
- leave the original acceptance criteria intact

## Commands To Run

Run the final-gate template audit from:

**Command Block Explanation**

- What this block does: Shows the exact text commands for Run the final-gate template audit from.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
17-springboot-final-gate.md
```

## Done Criteria

- [x] Status marker rules are documented.
- [x] Required section order is documented.
- [x] The per-code-block explanation rule is explicit.
- [x] Task completion requires verification, not just code written.

## Common Mistakes

- Marking `Done` without running focused and full tests.
- Updating a task file but not the index.
- Putting explanation text inside a fenced code block instead of before the opening fence.
- Deleting acceptance criteria when blocked.

## Stop / Do Not Add

- Do not create new status names unless the whole build-sequence convention changes.
- Do not weaken done criteria to make status look better.
- Do not add code blocks without the explanation wrapper.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Normalized to the shared build-task template.
