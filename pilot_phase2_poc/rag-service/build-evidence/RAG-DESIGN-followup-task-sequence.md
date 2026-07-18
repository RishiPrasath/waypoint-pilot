# RAG Design Follow-Up Task Sequence Evidence

Status: In Review
Date: 2026-07-18

Branch: `codex/rag-design-followup-task-sequence`
Worktree: `C:\tmp\rag-design-followup-task-sequence`

## Scope

Planning-only sequence update to create the owner-accepted follow-up design
tasks before `RAG-DT013` final build task impact review:

- `RAG-DT018`: Retrieval strategy selection, scoring, and fusion contract.
- `RAG-DT019`: Generation prompt, safeguards, output schema, and query API
  contract.
- `RAG-DT020`: Post-build evaluation and tuning loop.

## Files Added

- `pilot_phase2_poc/rag-service/build-sequence/02-design-tasks/05-runtime-technical-design/RAG-DT018-retrieval-strategy-selection-and-fusion-contract.md`
- `pilot_phase2_poc/rag-service/build-sequence/02-design-tasks/05-runtime-technical-design/RAG-DT019-generation-prompt-safeguards-output-schema-and-query-api-contract.md`
- `pilot_phase2_poc/rag-service/build-sequence/02-design-tasks/05-runtime-technical-design/RAG-DT020-post-build-evaluation-and-tuning-loop.md`

## Enforcement Updates

- Main build sequence now places `RAG-DT018`, `RAG-DT019`, and `RAG-DT020`
  after `RAG-DT017` and before `RAG-DT013`.
- Design lane index includes the three new planned tasks.
- `RAG-DT013` now explicitly requires the new tasks to be complete or waived
  before final build approval.
- Affected build-task files now reference the relevant gates:
  - retrieval tasks depend on `RAG-DT018`;
  - query/generation/API/ops tasks depend on `RAG-DT019`;
  - evaluation and production-readiness tasks depend on `RAG-DT020`.

## Local Checks

```text
$env:RAG_GROQ_API_KEY = $null
uv run python -m pytest -q
12 passed in 0.33s
```

Note: the test suite was run with `RAG_GROQ_API_KEY` cleared inside the local
command so it matches CI behavior for missing-secret checks without printing or
persistently changing local credentials.

Additional sequence checks confirmed:

- all three new task files exist;
- main index references `RAG-DT018`, `RAG-DT019`, and `RAG-DT020`;
- design lane index references `RAG-DT018`, `RAG-DT019`, and `RAG-DT020`;
- `RAG-DT013` references all three new gates;
- affected build-task files reference their required new gates;
- index-local markdown task references resolve to existing files.

## PR / CI

PR: pending branch push.
PR CI/CD: pending.
Main CI/CD: pending merge.
Cleanup: pending merge.
