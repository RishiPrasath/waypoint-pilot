# DT019 Decision Gate

Status: Accepted
Run: `dt019-run-001`
Task: `RAG-DT019`

## Gate Question

Is the generation prompt, safeguard behavior, output schema, and query API
contract sufficient for `RAG-BT015`, `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, and
`RAG-BT019` to proceed after final build impact review?

## Decision

```text
Pass - accept the DT019 generation and query API contract for implementation
handoff.
```

## Accepted Decisions

1. Use `POST /api/v1/query` as the first query endpoint path.
2. Use OpenAI-compatible chat-style roles: system, developer, user, retrieved
   context package.
3. Treat retrieved chunks as untrusted data, never as instructions.
4. Require JSON output matching `response-schema.json`.
5. Require citations for positive source-grounded answers.
6. Block no-retrieval planner cases before retrieval/generation.
7. Preserve metadata-only/license-sensitive boundaries.
8. Use `RAG_LLM_*` runtime config names and `RAG_GROQ_API_KEY` for the first
   Groq adapter secret.
9. Default generation candidate remains Groq `llama-3.3-70b-versatile`, but
   model/provider config must be injectable.
10. Use bounded retry: at most one retry for malformed JSON or recoverable
    schema failure.
11. Return a standard `error_fallback` response for exhausted retries or
    unavailable providers.
12. Add an evaluation-only LLM judge for answer relevance, completeness,
    groundedness, and scope control.
13. Keep judge provider/model configuration separate with `RAG_EVAL_LLM_*`.
14. Defer production runtime judge gating until cost, latency, model-bias, and
    reliability are assessed.

## Evidence Reviewed

| Artifact | Finding |
|---|---|
| `docs/evaluation/golden-questions.md` | Defines positive, boundary, refusal, malicious, and license-sensitive answer expectations. |
| `docs/design/query-planning/query_planner_rules.yaml` | Defines planner classifications and safe-response IDs before retrieval/generation. |
| `docs/design/query-planning/query_planner_tests.yaml` | Provides deterministic planner fixtures for API/safeguard examples. |
| `docs/design/llm-model-evaluation-plan.md` | Defines provider inventory, schema/citation/refusal scoring, and secret-handling rules. |
| `docs/design/llm-model-selection-decision.md` | Selects Groq `llama-3.3-70b-versatile` as first-pass generation model candidate. |
| `docs/design/retrieval-strategy-and-fusion-contract.md` | Defines retrieval modes, low-confidence gate, metadata filters, and retrieval fields the API must expose. |
| `RAG-BT015` to `RAG-BT019` task files | Confirm downstream tasks need prompt, schema, safe-response, retry, and API fields before implementation. |

## Risks And Controls

| Risk | Control |
|---|---|
| Model output drifts from schema. | Validate output and retry once before safe fallback. |
| Model fabricates citations. | Validate citations against retrieved context lineage. |
| Retrieved chunk contains prompt injection. | Prompt contract marks chunks as untrusted data. |
| Safe-response cases accidentally call retrieval/generation. | Planner block cases return standard safe response before retrieval. |
| API hides debugging fields needed for evaluation. | Response includes planner, retrieval, generation, safety, citation, and error sections. |
| Secret leakage in logs/evidence. | Config values are injectable; API keys and auth headers must never be echoed or committed. |
| Structurally valid answer does not answer the question. | `RAG-BT019` must run an evaluation-only LLM judge relevance/completeness check. |
| Judge model is biased because it matches the generation model. | First-pass judge may reuse the selected model, but judge config is separate and swappable. |

## Build Impact

- `RAG-BT015`: implement planner fields and safe-response reason mapping.
- `RAG-BT016`: implement configurable Groq/OpenAI-compatible generation adapter.
- `RAG-BT017`: implement schema/citation validation, bounded retry, and fallback.
- `RAG-BT018`: implement `POST /api/v1/query` response shape and error envelope.
- `RAG-BT019`: evaluate schema, citation, groundedness, refusal, provider error,
  malformed output, latency, API response behavior, and LLM judge relevance /
  completeness scoring.

## Gate Result

Accepted for PR review. Final status becomes complete only after merge closeout
updates the task file, design index, and evidence metadata.
