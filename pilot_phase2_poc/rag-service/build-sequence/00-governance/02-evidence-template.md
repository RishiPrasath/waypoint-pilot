# Evidence Template

Create the evidence file in the same branch as the task implementation before
opening a PR. The evidence must be complete enough to review and merge in that
same PR.

Do not create a second closeout PR only to add merge commit, main CI links, or
post-merge metadata. GitHub is the source of truth for those facts after merge.
If the PR URL must be recorded in the evidence file, update the evidence on the
same task branch before merge.

```markdown
# RAG-$TaskId Evidence

Status: In Progress / In Review / Ready for Merge / Complete / Blocked

## Identity

Task:
Branch:
Worktree:
Starting main commit:
PR: Pending until opened; update in this branch before merge if required.
Implementation commit:

## Artifacts

## Checks Run

## CI And Review

GitHub PR checks are the source of truth for PR CI. Main-branch CI and the merge
commit are read from the merged PR/run records after merge; they are not
required committed evidence fields.

## Issues And Recovery

## Follow-ups
```

Blank fields are not allowed. Use `Pending - reason` before PR creation, and
`N/A - reason` when a field truly does not apply.
