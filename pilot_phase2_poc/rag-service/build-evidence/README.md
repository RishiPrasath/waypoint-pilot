# RAG Service Build Evidence

This folder is the durable closeout record for completed RAG service tasks.

Every task marked `Complete` in `build-sequence/` must have a matching evidence
file here. Task files describe the intended work; evidence files prove what was
actually run, reviewed, merged, and cleaned up.

Required evidence fields:

- task ID, branch, worktree, and starting main commit when known
- implementation or design artifact files changed
- validation commands and results
- PR URL, implementation commit, and merge commit
- CI/review result
- issues encountered and recovery
- debt or follow-up work

Do not leave required fields blank. Use `N/A - reason` or `Pending - reason`
when a value is not available yet.
