# Task Closeout Checklist

## Before opening the PR

- [ ] Task branch is based on the current `origin/main`.
- [ ] Dedicated worktree is clean before implementation.
- [ ] Required dependency tasks are `Complete` or explicitly `Deferred`.
- [ ] Matching evidence file exists under `build-evidence/`.
- [ ] Red check, implementation, verification commands, and results are recorded.
- [ ] All acceptance criteria are addressed.
- [ ] No required evidence field is blank; non-applicable items include a reason.
- [ ] Diff, status, and intended file scope were reviewed.

## Before merging

- [ ] PR URL is recorded in the evidence file.
- [ ] PR CI/check results are recorded.
- [ ] Review/approval result is recorded.
- [ ] Any remaining issue is either fixed or explicitly accepted and recorded.

## After merging

- [ ] Fetch `origin` and fast-forward the local `main`.
- [ ] Confirm the merged commit contains the task and evidence changes.
- [ ] Confirm local `main` is clean.
- [ ] Leave the task worktree before removing it; close IDE terminals using it.
- [ ] Remove the task worktree, then run `git worktree prune`.
- [ ] Confirm `git worktree list` contains only intended worktrees.
- [ ] Record merged commit, clean main, cleanup, and final status in the same evidence file.
- [ ] Commit/push the post-merge evidence update before marking the task `Complete`.

If worktree removal fails, stop and inspect `git worktree list` and the worktree
metadata. Do not repeatedly rerun the same removal command or use a different
path until the recorded path is verified.
