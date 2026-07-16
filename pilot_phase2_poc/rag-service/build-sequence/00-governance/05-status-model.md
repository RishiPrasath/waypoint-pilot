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

- `Complete` requires merged artifacts, passing required checks, evidence, and
  closeout metadata.
- `Merged` means the PR has landed but post-merge closeout is not finished.
- `Blocked` requires the blocker, owner, and next unblock condition.
- `Deferred` requires a reason and the task that is allowed to proceed without
  it.
- `Draft` is legacy wording and should not be used for new task records.
