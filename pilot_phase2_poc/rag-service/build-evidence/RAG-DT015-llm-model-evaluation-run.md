# RAG-DT015 Evidence

Task: Run LLM Model Evaluation And Selection

Branch: `codex/rag-dt015-llm-model-evaluation-execution`
Worktree: `C:\tmp\rag-dt015-llm-model-evaluation-execution`
Base: `origin/main` at `5a70edf`

## Credential Gate

Provider configuration was set locally through environment variables and an
ignored `.env` file:

```text
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_PROVIDER_LABEL=groq
LLM_API_KEY=<present-redacted>
RAG_GROQ_API_KEY=<present-redacted>
```

The `.env` file is ignored by git:

```text
!! pilot_phase2_poc/rag-service/.env
```

The API key was not written into committed artifacts. Because the key was
pasted into chat during setup, it should be rotated after this evaluation.

## Inputs Reviewed

- `docs/design/llm-model-evaluation-plan.md`
- `docs/design/experiments/llm-model-evaluation/model-evaluation-runbook.md`
- `docs/evaluation/golden-questions.md`
- `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl`
- `docs/design/query-planning/query_planner_tests.yaml`
- `docs/design/source-snapshot-and-markdown-candidates.md`
- Groq supported models documentation

## Provider Inventory

The OpenAI-compatible `/models` endpoint was tested with the OpenAI Python SDK
and returned successfully.

Inventory artifact:

```text
docs/design/experiments/llm-model-evaluation/runs/dt015-run-001/model-inventory.json
```

Observed:

```text
provider: groq
model_count: 17
initial_candidate_count: 10
initial_excluded_count: 7
```

## Capability Review And Shortlist

Artifacts:

```text
docs/design/experiments/llm-model-evaluation/runs/dt015-run-001/model-capabilities.json
docs/design/experiments/llm-model-evaluation/runs/dt015-run-001/model-shortlist.json
```

Shortlisted models:

```text
llama-3.1-8b-instant
llama-3.3-70b-versatile
openai/gpt-oss-20b
openai/gpt-oss-120b
```

## Fixture Cases

Artifact:

```text
docs/design/experiments/llm-model-evaluation/runs/dt015-run-001/fixture-cases.jsonl
```

Observed:

```text
case_count: 14
positive_or_boundary_with_context: 8
negative_or_exclusion_without_context: 6
total_context_chunks: 9
```

## Live Model Evaluation

Artifact:

```text
docs/design/experiments/llm-model-evaluation/runs/dt015-run-001/model-results.jsonl
```

The live run executed 56 model-case calls:

```text
4 shortlisted models x 14 fixture cases = 56 calls
```

All 56 calls completed without provider errors or malformed JSON.

## Summary And Decision

Artifacts:

```text
docs/design/experiments/llm-model-evaluation/runs/dt015-run-001/evaluation-summary.md
docs/design/llm-model-selection-decision.md
```

Selected model:

```text
llama-3.3-70b-versatile
```

Rationale:

- tied for highest aggregate score
- completed all cases
- no malformed outputs
- materially lower p50 and p95 latency than the tied alternatives

## Verification

Validation checks completed:

- provider credentials tested through OpenAI Python SDK
- inventory JSON parsed successfully
- capability and shortlist JSON parsed successfully
- fixture JSONL parsed successfully
- model results JSONL parsed successfully
- narrowed secret-token scan returned no matches for committed run artifacts
- `uv run python -m pytest -q` passed with local ignored `.env`
  temporarily moved aside, because the config test intentionally verifies the
  missing-key failure path

## PR / CI / Merge

PR:
PR CI/CD:
Main CI/CD:
Merge commit:
Cleanup:

## Risks And Deferred Work

- The API key should be rotated because it was pasted into chat during setup.
- Scoring is a deterministic design-time heuristic; `RAG-BT019` should
  implement a repeatable harness and may revise the decision.
- `groq/compound` and `groq/compound-mini` remain deferred because agentic tool
  behavior can contaminate source-grounded RAG evaluation.
- Preview and multimodal models remain deferred until the RAG design requires
  them.
