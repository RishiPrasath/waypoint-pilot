# Closeout Checklist

A task can move to `Complete` only after all required closeout facts are
recorded.

- Evidence file exists under `build-evidence/`.
- Task file links to the evidence file.
- Required artifacts are committed.
- Local checks are recorded with commands and results.
- PR URL is recorded.
- Implementation commit is recorded.
- Merge commit is recorded.
- CI or review result is recorded.
- Known issues and recovery are recorded.
- Follow-up debt is recorded or explicitly marked `N/A`.
- Lane index status matches the task file.
- Worktree cleanup is done or explicitly deferred with a reason.

If a PR is already merged but closeout facts are missing, use a small
documentation-only closeout branch.
