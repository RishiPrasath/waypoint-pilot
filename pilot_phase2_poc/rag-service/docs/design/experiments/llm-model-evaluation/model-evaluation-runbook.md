# Model Evaluation Runbook

Status: Accepted for `RAG-DT009`
Date: 2026-07-17

## Purpose

This runbook defines the proposed code shape and command contract for provider
model inventory, model capability review, shortlisting, fixture construction,
model evaluation, and report generation.

It is a design runbook. Runtime implementation belongs to later build tasks,
especially `RAG-BT016`, `RAG-BT017`, and `RAG-BT019`.

## Environment Contract

Required only for API-backed discovery or evaluation:

```powershell
$env:LLM_BASE_URL = "https://provider.example.com/openai/v1"
$env:LLM_API_KEY = "<secret value from owner>"
$env:LLM_PROVIDER_LABEL = "provider-label"
```

Never commit or print `LLM_API_KEY`.

## Proposed Code Layout

```text
app/stages/stage_05_evaluation/
  model_inventory.py
  model_capabilities.py
  model_shortlist.py
  fixture_builder.py
  model_runner.py
  report_writer.py
```

The build task may adjust names, but it must preserve the command contracts
and no-secrets behavior.

## Command Contract

### 1. Provider Inventory

```powershell
uv run python -m app.stages.stage_05_evaluation.model_inventory `
  --base-url $env:LLM_BASE_URL `
  --provider-label $env:LLM_PROVIDER_LABEL `
  --out docs/design/experiments/llm-model-evaluation/runs/<run-id>/model-inventory.json
```

Behavior:

- read API key from `LLM_API_KEY`
- call `GET {LLM_BASE_URL}/models`
- redact authorization headers
- validate output against `model-inventory.schema.json`
- mark run `failed` rather than writing partial secret-bearing data

### 2. Capability Review

```powershell
uv run python -m app.stages.stage_05_evaluation.model_capabilities `
  --inventory docs/design/experiments/llm-model-evaluation/runs/<run-id>/model-inventory.json `
  --review docs/design/experiments/llm-model-evaluation/model-capability-review.md `
  --out docs/design/experiments/llm-model-evaluation/runs/<run-id>/model-capabilities.json
```

Behavior:

- enrich inventory with `/models/{model}` metadata when supported
- allow manual enrichment from provider docs/model cards
- mark unavailable capability fields as `unknown`
- do not infer modalities or context windows from model names
- require explicit owner approval before probes

### 3. Model Shortlist

```powershell
uv run python -m app.stages.stage_05_evaluation.model_shortlist `
  --capabilities docs/design/experiments/llm-model-evaluation/runs/<run-id>/model-capabilities.json `
  --out docs/design/experiments/llm-model-evaluation/runs/<run-id>/model-shortlist.json
```

Behavior:

- include, defer, or exclude each model
- keep rationale for every decision
- default to a small candidate set for the first assessment

### 4. Fixture Construction

```powershell
uv run python -m app.stages.stage_05_evaluation.fixture_builder `
  --golden docs/evaluation/golden-questions.md `
  --chunks docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl `
  --planner-tests docs/design/query-planning/query_planner_tests.yaml `
  --lineage docs/design/source-snapshot-and-markdown-candidates.md `
  --out docs/design/experiments/llm-model-evaluation/runs/<run-id>/fixture-cases.jsonl
```

Behavior:

- use `GQ-001` through `GQ-008` as positive/source-boundary cases
- use `GQ-009` through `GQ-014` as negative, irrelevant, malicious, and
  license-sensitive cases
- attach DT005 chunk context only where retrieval is expected
- preserve citation fields: `approved_source`, `document_id`, `snapshot_id`,
  `chunk_id`, `chunk_strategy`, `heading_path`, `source_uri`, and
  `candidate_sha256`
- mark APAC-215 as metadata-only and license-sensitive

### 5. Model Evaluation Run

```powershell
uv run python -m app.stages.stage_05_evaluation.model_runner `
  --shortlist docs/design/experiments/llm-model-evaluation/runs/<run-id>/model-shortlist.json `
  --fixture docs/design/experiments/llm-model-evaluation/runs/<run-id>/fixture-cases.jsonl `
  --out docs/design/experiments/llm-model-evaluation/runs/<run-id>/model-results.jsonl
```

Behavior:

- run only included models
- record latency per case
- record provider/model errors without crashing the full run
- classify malformed output separately from answer-quality failure
- do not send negative cases with unrelated retrieval context

### 6. Report Generation

```powershell
uv run python -m app.stages.stage_05_evaluation.report_writer `
  --results docs/design/experiments/llm-model-evaluation/runs/<run-id>/model-results.jsonl `
  --out docs/design/experiments/llm-model-evaluation/runs/<run-id>/evaluation-summary.md
```

Behavior:

- report aggregate scores by model and category
- separate planner, retrieval, answer, citation, refusal, latency, and error
  outcomes
- recommend continue, defer, or reject
- do not make final production model lock

## Evaluation Case Shape

Each fixture case should contain:

```json
{
  "case_id": "GQ-001",
  "question": "What public workflow does Singapore Customs describe for obtaining an import permit?",
  "question_type": "positive",
  "expected_intent": "regulatory_explanation",
  "retrieval_expected": true,
  "expected_sources": ["APAC-001"],
  "context_chunks": [],
  "reference_answer": "...",
  "scoring": {
    "answer_quality": true,
    "groundedness": true,
    "schema_adherence": true,
    "citation_behavior": true,
    "refusal_safety": false,
    "latency": true
  }
}
```

## Result Shape

Each model result row should contain:

```json
{
  "run_id": "dt009-run-001",
  "provider_label": "provider-label",
  "model_id": "model-id",
  "case_id": "GQ-001",
  "status": "passed",
  "latency_ms": 0,
  "scores": {
    "answer_quality": 0,
    "groundedness": 0,
    "schema_adherence": 0,
    "citation_behavior": 0,
    "refusal_safety": null
  },
  "error_type": null,
  "notes": []
}
```

## Safety And Redaction Checklist

- Do not store API keys.
- Do not store authorization headers.
- Do not store full environment dumps.
- Do not store private provider account metadata.
- Redact endpoint query strings if present.
- Keep raw model outputs only if they do not contain secrets or private data.
- Store negative prompt-injection outputs only to demonstrate safety behavior.

## Completion Criteria For A Future Live Run

A live run is complete only when:

- provider inventory is written and schema-valid
- capability review records include/defer/exclude decisions
- shortlist is owner-reviewable
- fixture cases are built from DT005, DT006, DT007, and DT012 inputs
- model results include scores and latency
- report separates quality, grounding, schema, citation, refusal, and errors
- evidence records PR/CI status and no-secrets handling
