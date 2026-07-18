# RAG-DT019 Evidence

Status: Complete
Task: `RAG-DT019`
Branch: `codex/rag-dt019-generation-prompt-safeguards-output-schema-and-query-api-contract`
Worktree: `C:\tmp\rag-dt019-generation-prompt-safeguards-output-schema-and-query-api-contract`
Date: 2026-07-18

## Objective

Define the generation prompt, safeguards, output schema, query API contract,
validation/retry/fallback behavior, and runtime LLM/provider config names before
generation and API build tasks start.

## Artifacts Created

```text
docs/design/generation-and-query-api-contract.md
docs/design/experiments/generation-api-contract/dt019-run-001/prompt-contract.md
docs/design/experiments/generation-api-contract/dt019-run-001/response-schema.json
docs/design/experiments/generation-api-contract/dt019-run-001/api-examples.md
docs/design/experiments/generation-api-contract/dt019-run-001/decision-gate.md
build-evidence/RAG-DT019-generation-prompt-safeguards-output-schema-and-query-api-contract.md
```

## Inputs Reviewed

```text
docs/evaluation/golden-questions.md
docs/design/query-planning/query_planner_rules.yaml
docs/design/query-planning/query_planner_tests.yaml
docs/design/llm-model-evaluation-plan.md
docs/design/llm-model-selection-decision.md
docs/design/retrieval-strategy-and-fusion-contract.md
build-sequence/03-build-tasks/02-query/RAG-BT015-query-planning.md
build-sequence/03-build-tasks/04-generation/RAG-BT016-generation-adapter.md
build-sequence/03-build-tasks/04-generation/RAG-BT017-output-validation-retry-fallback.md
build-sequence/03-build-tasks/02-query/RAG-BT018-query-api-endpoint.md
build-sequence/03-build-tasks/05-evaluation/RAG-BT019-evaluation-harness.md
```

## Red Check

Command:

```powershell
$ServiceRoot = Join-Path $WorktreePath "pilot_phase2_poc/rag-service"
Test-Path "$ServiceRoot\docs\design\generation-and-query-api-contract.md"
```

Result before implementation:

```text
False
```

## Decisions Recorded

- Query endpoint path: `POST /api/v1/query`.
- Prompt roles: system, developer, user, retrieved context package.
- Retrieved chunks are untrusted data.
- Generation output must validate against `response-schema.json`.
- Positive answers require source citations.
- No-retrieval planner cases return safe responses before retrieval/generation.
- License-sensitive/cite-only requests must not retrieve or generate answer text.
- Runtime config names prefer `RAG_LLM_*` plus `RAG_GROQ_API_KEY`.
- Default generation candidate remains `llama-3.3-70b-versatile` on Groq.
- Provider/model settings remain injectable.
- Retry is bounded to at most one retry for malformed JSON or recoverable schema
  failure.
- Fallback output uses standard `error_fallback`.
- Code-level validators are necessary but not sufficient for answer quality.
- `RAG-BT019` must add an evaluation-only LLM judge for answer relevance,
  completeness, groundedness, and scope-control checks.
- Judge model configuration must be separate from generation configuration via
  `RAG_EVAL_LLM_*`.
- Production runtime judge gating is deferred until cost, latency, model-bias,
  and reliability are assessed.

## Verification Commands

Completed before PR handoff:

```powershell
Set-Location "C:\tmp\rag-dt019-generation-prompt-safeguards-output-schema-and-query-api-contract\pilot_phase2_poc\rag-service"
Test-Path "docs/design/generation-and-query-api-contract.md"
Test-Path "docs/design/experiments/generation-api-contract/dt019-run-001/prompt-contract.md"
Test-Path "docs/design/experiments/generation-api-contract/dt019-run-001/response-schema.json"
Test-Path "docs/design/experiments/generation-api-contract/dt019-run-001/api-examples.md"
Select-String -Path "docs/design/generation-and-query-api-contract.md" -Pattern "RAG-BT015|RAG-BT016|RAG-BT017|RAG-BT018|RAG-BT019"
uv run python -m pytest -q
git diff --check
```

Results:

```text
contract_exists=True
prompt_contract_exists=True
schema_exists=True
examples_exists=True
evidence_exists=True
python -m json.tool response-schema.json -> passed
Select-String build-impact references -> RAG-BT015, RAG-BT016, RAG-BT017, RAG-BT018, RAG-BT019 present
$env:RAG_GROQ_API_KEY = $null; uv run python -m pytest -q -> 12 passed in 2.96s
git diff --check -> passed
```

## PR And Merge

PR:
https://github.com/RishiPrasath/waypoint-pilot/pull/49

PR CI/CD:
Passed before merge:

- RAG Service CI: success
- RAG Service CodeQL / Analyze Python: success
- CodeQL: success

Main CI/CD:
Passed after merge commit `a6c4e8270ad2ff12d22db787c677f2cdb46c9887`:

- RAG Service CI: success
- RAG Service CodeQL / Analyze Python: success

Merge commit:
`a6c4e8270ad2ff12d22db787c677f2cdb46c9887`

Merged at:
`2026-07-18T10:41:59Z`

Cleanup:

- Local `main` refreshed to merge commit `a6c4e82`.
- DT019 implementation worktree removed:
  `C:\tmp\rag-dt019-generation-prompt-safeguards-output-schema-and-query-api-contract`
- Local branch deleted:
  `codex/rag-dt019-generation-prompt-safeguards-output-schema-and-query-api-contract`
- Remote branch deleted:
  `codex/rag-dt019-generation-prompt-safeguards-output-schema-and-query-api-contract`

Closeout note:
This metadata closeout is recorded on branch `codex/rag-dt019-closeout`.
