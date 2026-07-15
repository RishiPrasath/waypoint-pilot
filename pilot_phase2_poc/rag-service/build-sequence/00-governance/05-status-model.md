# Task Status Model

Use only these statuses:

```text
Draft -> Planned -> Ready -> In Progress -> In Review -> Merged -> Complete
In Progress -> Blocked
Planned -> Deferred
```

- `Draft`: legacy/unreviewed record only; no new task should remain here.
- `Planned`: task is defined and dependencies are known.
- `Ready`: dependencies and acceptance criteria are confirmed.
- `In Progress`: implementation work is active in its dedicated worktree.
- `In Review`: pre-PR evidence gate passed and a PR is open.
- `Merged`: PR merged; post-merge closeout is still pending.
- `Complete`: merged evidence, clean `main`, and worktree cleanup are verified.
- `Blocked`: work cannot proceed; the blocking condition is recorded.
- `Deferred`: intentionally postponed with a reason and successor/condition.

Do not mark a task `Complete` merely because tests pass or a PR is open. A task
cannot enter `In Progress` until all dependencies are `Complete` or explicitly
`Deferred`.
