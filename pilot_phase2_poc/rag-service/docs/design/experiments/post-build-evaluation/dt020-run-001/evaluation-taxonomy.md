# Evaluation Taxonomy

## 1) Retrieval Failures

- `Missing top chunks`: expected source chunks do not appear in ranked list.
- `Wrong chunk surfaced`: ranking returns semantically distant chunks.
- `Noisy retrieval`: high score but low relevance chunk noise.
- `Metadata-only allowed but content leaked`: unsafe retrieval source handling failure.

## 2) Generation Failures

- `Schema invalid`: JSON parse/validation errors.
- `No citation`: answer returned without valid citations.
- `Hallucination`: answer claims unsupported facts.
- `Relevance mismatch`: answer does not address user question.
- `Over-refusal`: safe inputs answered with false refusal.

## 3) API/Protocol Failures

- `Contract mismatch`: malformed `/api/v1/query` response format.
- `Wrong status behavior`: safety failures mapped to wrong status/shape.
- `Retry storm`: excessive retries or unstable loop behavior.

## 4) Operational Failures

- `Startup failures`: local or Docker startup fails.
- `Provider errors`: provider API key/model availability failures.
- `Latency spikes`: sustained latency breaches.
- `CI mismatch`: checks pass locally but fail in CI due to environment assumptions.

## Mapping to Remediation Area

- Retrieval failures -> `chunking`, `embedding`, `qdrant-index`, `retrieval strategy`.
- Generation failures -> `prompt`, `schema`, `guardrails`, `RAG-BT019 flow`.
- API/protocol failures -> `RAG-BT018`, API contract, validation layer.
- Operational failures -> CI/local ops setup and runtime environment variables.

## Severity Bands

- `P0`: security/safety regression, malformed answer on supported user path.
- `P1`: blocking core retrieval/generation function.
- `P2`: measurable quality regression in specific scenario.
- `P3`: non-user-visible process friction.

Runbook action should match severity.
