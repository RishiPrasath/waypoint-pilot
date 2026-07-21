# Status Model

Allowed task statuses:

```text
Planned
Ready
In Progress
In Review
Merged
Complete
Blocked
Deferred
```

Rules:

- `Complete` means the task branch contains the implementation/design artifact,
  linked evidence, recorded local checks, and PR-ready handoff material needed
  to merge the task in one PR.
- `Ready for Merge` is an allowed evidence status for work that is fully
  reviewed locally and waiting on PR CI or human merge.
- `Merged` is legacy/recovery wording. Do not use it for normal new task flow.
- `Blocked` requires the blocker, owner, and next unblock condition.
- `Deferred` requires a reason and the task that is allowed to proceed without
  it.
- `Draft` is legacy wording and should not be used for new task records.
- Merge commit, post-merge main CI, and worktree cleanup are verified from
  GitHub/local git after merge; they do not require a second committed closeout
  PR.
