# Model Capability Review

Status: Template accepted for `RAG-DT009`
Date: 2026-07-17

## Purpose

This artifact defines the model capability review that must happen after
provider inventory and before LLM assessment. It prevents the evaluation from
blindly testing every returned model ID and gives the owner an explicit place
to decide which models are necessary for the RAG generation benchmark.

This file is a review template and decision contract. It is not a completed
live provider inventory.

## Evidence Order

Use evidence in this order:

1. `GET {LLM_BASE_URL}/models`
2. `GET {LLM_BASE_URL}/models/{model}` when the provider supports it
3. official provider docs, model cards, or model comparison pages
4. owner-approved safe probes

Unknown fields must remain `unknown`.

## Required Capability Fields

| Field | Required handling |
|---|---|
| Provider label | Use `LLM_PROVIDER_LABEL` or a non-secret owner-provided label. |
| Model ID | Preserve exact provider model ID. |
| Capability data source | Record `/models`, `/models/{model}`, provider docs, comparison page, or probe. |
| Context window | Record numeric value or `unknown`. |
| Max output | Record numeric value or `unknown`. |
| Supported inputs | Track text, image, PDF/file, audio, and voice when known. |
| Supported outputs | Track text, structured JSON, audio, and voice when known. |
| API surface | Track Responses, Chat Completions compatibility, batch, realtime, or `unknown`. |
| Tool support | Record tool/function support or `unknown`. |
| Schema/JSON suitability | Record known support, probe result, or `unknown`. |
| Known limitations | Record deprecation, quota, rate-limit, latency, cost, or modality limitations. |
| Assessment decision | `include`, `defer`, or `exclude`. |
| Rationale | Explain the decision in one or two sentences. |

## Default Review Table

Populate this table during the first provider review.

| Provider | Model ID | Sources | Context window | Max output | Inputs | Outputs | API surface | Tool support | JSON/schema | Decision | Rationale |
|---|---|---|---:|---:|---|---|---|---|---|---|---|
| `pending` | `pending` | `pending` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `defer` | Provider inventory has not been run yet. |

## Safe Probe Policy

Safe probes are allowed only after the owner confirms API-backed checks for the
provider. Probe prompts must not include secrets, private customer data, or
unapproved source material.

Default allowed probes:

1. Text response:
   - ask a short APAC regulatory summary question using supplied fixture text
2. Structured output:
   - require a JSON object with `answer`, `citations`, and `safety_notes`
3. Citation-shaped output:
   - supply one DT005 chunk and require citation fields from DT006
4. Safety/refusal:
   - use `GQ-009` through `GQ-014` without unrelated retrieval context

Do not probe PDF, image, file, audio, voice, or realtime capabilities unless
the owner explicitly approves those checks and they are required by the RAG
design.

## Shortlist Decision Rules

Include:

- text generation models with compatible API surface
- chat or instruct models suitable for grounded RAG answers
- models with known or promising schema/JSON behavior
- models with sufficient context window and max output for retrieved chunks

Defer:

- models with incomplete capability metadata but plausible RAG usefulness
- models requiring owner confirmation for cost, quota, or rate-limit risk
- models requiring approved probes to confirm JSON/citation behavior

Exclude:

- embedding-only models
- image/audio/TTS/STT/moderation/realtime-only models not needed for RAG
- deprecated models
- models with no text output support
- models with incompatible API surface
- models that fail safe schema or citation probes

## First Evaluation Candidate Set

The first model assessment should stay intentionally small:

- one fast/low-cost model if available
- one stronger quality model if available
- one fallback model only if it has a different cost, speed, or capability
  profile

The purpose is to test generation quality and fixture behavior, not to exhaust
the entire provider catalog.
