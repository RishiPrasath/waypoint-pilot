# RAG Service Build Governance

These files are mandatory for every task under `build-sequence/`.

- `01-task-template.md` defines the task record and execution contract.
- `02-evidence-template.md` defines the single durable execution record.
- `03-closeout-checklist.md` defines the pre-PR, merge, and post-merge gates.
- `04-command-conventions.md` defines the Windows/Git/Python command rules.
- `05-status-model.md` defines the allowed lifecycle states.

The task record describes intent and acceptance criteria. The matching file under
`build-evidence/` records what actually happened. Do not open a PR until the
pre-PR evidence gate is complete and no required evidence field is blank.

A task is `Complete` only after the PR is merged, `main` is clean and current,
the task worktree is removed, and the post-merge closeout is recorded in the
merged evidence file.
