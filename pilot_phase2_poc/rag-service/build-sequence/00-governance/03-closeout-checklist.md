# PR Handoff And Closeout Checklist

A task PR must include all committed evidence needed to review and merge the
task in one PR.

- Evidence file exists under `build-evidence/`.
- Task file links to the evidence file.
- Required artifacts are committed.
- Local checks are recorded with commands and results.
- PR URL is recorded if the evidence file is updated after PR creation; if not,
  the PR itself is the source of truth.
- Implementation commit is recorded.
- PR CI or review result is recorded in the PR and may be summarized in the
  evidence before merge.
- Known issues and recovery are recorded.
- Follow-up debt is recorded or explicitly marked `N/A`.
- Lane index status matches the task file.
- After merge, pull fresh main and prune the task worktree.

Do not create a documentation-only closeout PR solely to record merge commit,
main CI, cleanup, or other facts already available from GitHub. Use a follow-up
PR only when a substantive task record is wrong, missing required evidence, or
would mislead the next build task.
