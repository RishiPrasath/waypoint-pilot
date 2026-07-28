# LLM Model Selection Decision

Status: Superseded; `RAG-DT015` reopened
Date: 2026-07-17
Reopened: 2026-07-28

## Current Decision

No default generation model is currently accepted.

Groq announced that `llama-3.3-70b-versatile` will shut down for
free/developer-tier usage on 2026-08-16. The provider recommends
`openai/gpt-oss-120b` or `qwen/qwen3.6-27b`.

Official notice:

```text
https://console.groq.com/docs/deprecations
```

`RAG-DT015` is blocked until the previously exposed credential is confirmed
rotated/revoked and currently supported default/fallback candidates are
re-evaluated under `RAG-DT022`.

## Historical Decision

The 2026-07-17 design-time run selected:

```text
llama-3.3-70b-versatile
```

Provider:

```text
groq
```

Provider endpoint:

```text
https://api.groq.com/openai/v1
```

This is a design-time model selection for the first Groq/OpenAI-compatible
generation adapter implementation. It is not a permanent production lock.
The adapter must keep model configuration injectable so later evaluation runs
can swap models without code changes.

## Evidence

Run folder:

```text
docs/design/experiments/llm-model-evaluation/runs/dt015-run-001/
```

Run artifacts:

- `model-inventory.json`
- `model-capabilities.json`
- `model-shortlist.json`
- `fixture-cases.jsonl`
- `model-results.jsonl`
- `evaluation-summary.md`

## Models Evaluated

```text
llama-3.1-8b-instant
llama-3.3-70b-versatile
openai/gpt-oss-20b
openai/gpt-oss-120b
```

## Result Summary

| Model | Cases | Completed | Errors | Malformed | Overall avg | p50 latency ms | p95 latency ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| `llama-3.3-70b-versatile` | 14 | 14 | 0 | 0 | 1.966 | 645.84 | 2930.83 |
| `openai/gpt-oss-120b` | 14 | 14 | 0 | 0 | 1.966 | 5541.01 | 11627.09 |
| `llama-3.1-8b-instant` | 14 | 14 | 0 | 0 | 1.966 | 5593.15 | 14239.75 |
| `openai/gpt-oss-20b` | 14 | 14 | 0 | 0 | 1.915 | 5080.82 | 11613.90 |

The scoring scale was `0`, `1`, or `2` per category. The first-pass heuristic
scored answer quality, groundedness, schema adherence, citation behavior,
refusal/safety behavior, latency, provider/model errors, and malformed output
handling.

## Rationale

`llama-3.3-70b-versatile` tied for the highest aggregate score while producing
the best latency profile among the tied models. It completed all 14 fixture
cases with no provider errors and no malformed JSON outputs.

`openai/gpt-oss-120b` matched the top aggregate score, but had materially
higher latency in this run.

`llama-3.1-8b-instant` also matched the top aggregate score, but this run showed
higher p50 and p95 latency than `llama-3.3-70b-versatile`.

`openai/gpt-oss-20b` performed well but had lower groundedness and citation
scores because at least one expected citation was not fully met.

## Superseded Implementation Guidance

`RAG-BT016` must not use `llama-3.3-70b-versatile` as its default. Keep the
adapter model-agnostic and blocked from live calls until the replacement and
fallback decision is accepted.

Do not hard-code the model in a way that prevents future swaps. The runtime
configuration should allow overriding the provider base URL, API key, provider
label, model ID, timeout, and max tokens.

Recommended default configuration names:

```text
RAG_LLM_PROVIDER_LABEL=groq
RAG_LLM_BASE_URL=https://api.groq.com/openai/v1
RAG_LLM_MODEL=llama-3.3-70b-versatile
RAG_GROQ_API_KEY=<secret, local only>
```

## Historical Deferred Models

This list records the 2026-07-17 run only. It is not a current supported-model
inventory and must not seed runtime defaults without the reopened DT015
provider/deprecation check.

The following models remain available for later comparison if the selected
model fails implementation or regression checks:

- `openai/gpt-oss-120b`
- `llama-3.1-8b-instant`
- `openai/gpt-oss-20b`
- `qwen/qwen3-32b`
- `qwen/qwen3.6-27b`

Agentic systems such as `groq/compound` and `groq/compound-mini` remain
deferred because their built-in tool behavior can contaminate a clean
source-grounded RAG evaluation.

## Safety And Secret Handling

- API key was read from local environment / ignored `.env`.
- API key was not written into committed artifacts.
- Negative and malicious cases were evaluated without unrelated retrieval
  context.
- The provided API key should be rotated after this evaluation because it was
  pasted into chat during setup.

## Caveat

This run used a deterministic design-time heuristic scorer. `RAG-BT019` should
implement a repeatable evaluation harness and can rerun these cases to confirm
or revise this selection.
