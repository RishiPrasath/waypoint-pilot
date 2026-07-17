# DT015 LLM Model Evaluation Summary

Run ID: `dt015-run-001`
Generated: `2026-07-17T08:14:24.505115+00:00`
Provider: `groq`

## Scope

This live design evaluation ran the first-pass Groq model shortlist against the 14 DT006 golden-question fixture cases built from DT005 chunks, DT007 planner expectations, and DT012 source lineage.

## Models Evaluated

- `llama-3.1-8b-instant`
- `llama-3.3-70b-versatile`
- `openai/gpt-oss-120b`
- `openai/gpt-oss-20b`

## Aggregate Results

| Model | Cases | Completed | Errors | Malformed | Overall avg | Answer | Grounded | Schema | Citation | Refusal | p50 ms | p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `llama-3.3-70b-versatile` | 14 | 14 | 0 | 0 | 1.966 | 1.929 | 2.0 | 2.0 | 2.0 | 1.889 | 645.84 | 2930.83 |
| `openai/gpt-oss-120b` | 14 | 14 | 0 | 0 | 1.966 | 1.929 | 2.0 | 2.0 | 2.0 | 1.889 | 5541.01 | 11627.09 |
| `llama-3.1-8b-instant` | 14 | 14 | 0 | 0 | 1.966 | 1.929 | 2.0 | 2.0 | 2.0 | 1.889 | 5593.15 | 14239.75 |
| `openai/gpt-oss-20b` | 14 | 14 | 0 | 0 | 1.915 | 1.929 | 1.75 | 2.0 | 1.857 | 2.0 | 5080.82 | 11613.9 |

## Initial Selection Recommendation

Initial selected model: `llama-3.3-70b-versatile`

Rationale: it produced the strongest aggregate heuristic score in this fixture run while completing all cases. This selection should be treated as a design-time recommendation, not a production lock, because scoring is still heuristic and later build tasks must implement repeatable evaluator code.

## Observed Failure Modes

- `llama-3.3-70b-versatile`: answer_quality_not_full_score
- `openai/gpt-oss-120b`: answer_quality_not_full_score
- `llama-3.1-8b-instant`: answer_quality_not_full_score
- `openai/gpt-oss-20b`: answer_quality_not_full_score, citation_expectation_not_fully_met

## Artifacts

- `model-inventory.json`
- `model-capabilities.json`
- `model-shortlist.json`
- `fixture-cases.jsonl`
- `model-results.jsonl`

## Safety And Secret Handling

- API key was read from local environment / ignored `.env`.
- API key was not written into run artifacts.
- Negative cases were run without unrelated retrieval context.
- Raw parsed outputs are stored in `model-results.jsonl`; no secrets were supplied in prompts.

## Follow-Up

- Create `docs/design/llm-model-selection-decision.md` with selected/deferred/blocked decision.
- Update DT015 evidence and affected build-task handoffs with the selected model or deferral rule.
- Treat this run as design evidence until `RAG-BT019` implements a repeatable harness.
