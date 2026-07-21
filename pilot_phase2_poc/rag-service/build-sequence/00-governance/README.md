# RAG Service Build Governance

This folder contains the canonical rules for writing, running, reviewing, and
closing RAG service build-sequence tasks.

Start here when editing templates or auditing task hygiene:

1. `01-task-template.md`
2. `02-evidence-template.md`
3. `03-closeout-checklist.md`
4. `04-command-conventions.md`
5. `05-status-model.md`
6. `06-trunk-workflow-and-ci-gates.md`

The root `build-sequence/00-index.md` remains the execution entrypoint. This
folder defines the rules that the index and individual task files must follow.

The repository-root GitHub Actions workflow runs
`scripts/check_build_sequence_governance.py` for every RAG service PR that
touches this area. That check is the executable version of the governance rules
above.
