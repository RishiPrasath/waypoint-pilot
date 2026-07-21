# Final Build Task Impact Review

Status: Accepted for `RAG-DT013`
Task: `RAG-DT013`
Date: 2026-07-18

## Purpose

This review closes the design-to-build handoff for the RAG service. Its job is
to confirm that final build tasks do not begin with stale assumptions after the
source, KB, chunking, embedding, vector DB, query planner, retrieval,
generation, safeguard, CI/CD, and post-build evaluation design tasks were
completed.

## Review Method

The review used five specialist perspectives:

- RAG architecture
- Retrieval and RAG behavior
- Generation and safeguards
- Test, CI, and local ops
- Documentation and governance

The result is a build-impact matrix plus task-level handoff notes added to the
final build task files.

## Build-Start Decision

Decision: `GO_WITH_CONDITIONS`

Final build work may begin after this review is merged, but only under these
conditions:

- Build tasks must treat first-pass source/candidate material as fixture or
  review material until explicit canonical KB promotion exists.
- Runtime implementation must not ingest `legacy/phase1-kb-snapshot/` directly.
- Qdrant integration proof must use service-backed Qdrant for integration
  checks; in-memory/mocked behavior is acceptable only for fast unit or design
  checks.
- Qdrant environment variable names must be reconciled before Qdrant-backed
  implementation starts.
- Qdrant service settings may use ecosystem-standard `QDRANT_*` names, but
  runtime application settings must document the exact external variables and
  any supported `RAG_*` aliases before the owning Qdrant-backed task closes.
- Retrieval score traces must be available to API/evaluation diagnostics.
- Ambiguous-query behavior must be explicitly represented in query/API tests.
- DT017 and DT016 deferred governance/security items must be consumed by
  production-readiness review.

No unresolved design issue blocks starting the first ingestion build tasks, but
the conditional items above must be addressed by the affected build task before
that task can be considered complete.

## Impact Matrix

| design_task | decision_or_output | affected_build_task | required_update | status | owner | risk_if_not_updated |
|---|---|---|---|---|---|---|
| `RAG-DT002`, `RAG-DT003`, `RAG-DT004`, `RAG-DT008`, `RAG-DT012` | KB material is registry/snapshot/candidate gated; legacy snapshot is audit-only. | `RAG-BT007`, `RAG-BT008`, `RAG-BT012`, `RAG-BT013`, `RAG-BT014`, `RAG-BT019` | Keep source registry validation, audit outputs, and fixture ingestion separate from production canonical promotion. | Conditional | solo developer | Runtime may ingest unaudited or license-sensitive source material. |
| `RAG-DT005` | Accepted chunking strategy is `hybrid_structure_recursive_v1` with deterministic chunk IDs and lineage metadata. | `RAG-BT009`, `RAG-BT012`, `RAG-BT013`, `RAG-BT014`, `RAG-BT019` | Implement the DT005 chunk JSONL shape, required metadata, hashes, and lineage checks. | Required | solo developer | Retrieval/golden tests may compare against unstable chunks or uncitable context. |
| `RAG-DT006` | Golden questions define expected retrieval, citation, refusal, and safety scenarios. | `RAG-BT013`, `RAG-BT014`, `RAG-BT018`, `RAG-BT019` | Load golden questions as structured fixtures and report scenario outcomes separately. | Required | solo developer | Evaluation may pass generic answers while missing expected chunks or unsafe refusals. |
| `RAG-DT007` | Query planner runs before retrieval and emits inspectable planning fields. | `RAG-BT015`, `RAG-BT018`, `RAG-BT019` | Implement rules/tests from query planner artifacts; blocked classes must not call retrieval or generation. | Required | solo developer | Unsafe or irrelevant queries may reach retrieval/generation. |
| `RAG-DT009`, `RAG-DT015`, `RAG-DT019` | Default generation candidate is Groq/OpenAI-compatible `llama-3.3-70b-versatile`, injectable through `RAG_LLM_*`; eval judge uses separate `RAG_EVAL_LLM_*`. | `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, `RAG-BT019` | Keep provider calls mocked by default; separate generation and evaluation model config. | Required | solo developer | CI may require live credentials or couple generation and evaluation settings. |
| `RAG-DT010` | Accepted embedding baseline is FastEmbed `BAAI/bge-small-en`, 384 dimensions, cosine distance. | `RAG-BT011`, `RAG-BT012`, `RAG-BT013`, `RAG-BT014`, `RAG-BT019` | Record provider, model, dimension, distance, and benchmark run in vector payload/reporting. | Required | solo developer | Qdrant collection dimensions and retrieval baselines may drift. |
| `RAG-DT014` | Vector DB strategy uses mocked/unit checks, local service-backed Qdrant, and GitHub Actions Qdrant service container when promoted. | `RAG-BT012`, `RAG-BT013`, `RAG-BT014`, `RAG-BT019`, `RAG-BT020`, `RAG-BT022` | Split fast tests from `pytest -m integration`; use disposable collection prefixes and readiness checks. | Required | solo developer | In-memory checks may hide real Qdrant lifecycle and CI failures. |
| `RAG-DT016` | CI readiness exists, with some repo/security/container checks deferred to later tasks. | `RAG-BT012`, `RAG-BT013`, `RAG-BT014`, `RAG-BT018`, `RAG-BT019`, `RAG-BT020`, `RAG-BT022` | Promote Qdrant, Docker image smoke, container scan, and repo security checks at the task that owns each runtime surface. | Conditional | solo developer | CI can stay green while runtime integration or security posture remains unproven. |
| `RAG-DT017` | Architecture sufficiency review identified remaining governance/security risks and required follow-up design tasks. | All build tasks, especially `RAG-BT020`, `RAG-BT022` | Carry unresolved repo enforcement and dependency provenance risks to production readiness. | Conditional | solo developer | Build may proceed without explicit owner acceptance of governance risk. |
| `RAG-DT018` | Target retrieval is planner-led metadata-filtered hybrid retrieval with semantic baseline, lexical diagnostics, score normalization, fusion, tie-breaks, rerank hook, and low-confidence blocking. | `RAG-BT013`, `RAG-BT014`, `RAG-BT018`, `RAG-BT019` | Keep semantic-only baseline separate from final hybrid runtime; expose mode, scores, confidence, and low-confidence behavior. | Required | solo developer | Semantic baseline may be mistaken for final runtime retrieval and weak evidence may reach generation. |
| `RAG-DT019` | Generation/API contract defines `POST /api/v1/query`, prompt roles, untrusted chunks, schema validation, citations, refusals, retry/fallback, and safe-response rules. | `RAG-BT015`, `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, `RAG-BT019`, `RAG-BT021`, `RAG-BT022` | Validate against the DT019 response schema; cover every refusal/safety reason; keep retrieved context outside the user message. | Required | solo developer | API consumers may receive malformed, uncited, unsafe, or prompt-injected answers. |
| `RAG-DT020` | Post-build evaluation defines mandatory metrics, failure taxonomy, tuning playbook, and promotion/rejection gate. | `RAG-BT019`, `RAG-BT022`, and any task changed by tuning | Emit structured per-mode metrics and make production readiness consume evaluation evidence. | Required | solo developer | Evaluation becomes anecdotal and regressions do not map to remediation tasks. |

## Per-Build-Task Handoff

| build_task | final_handoff |
|---|---|
| `RAG-BT007` | Validate source registry schema, retrieval eligibility, license sensitivity, and no direct legacy ingestion assumptions. |
| `RAG-BT008` | Produce audit artifacts only; legacy snapshot remains audit input, not runtime corpus. |
| `RAG-BT009` | Implement `hybrid_structure_recursive_v1` fixtures with deterministic IDs, hashes, heading lineage, and `APAC-215` exclusion. |
| `RAG-BT011` | Default to FastEmbed `BAAI/bge-small-en`, 384-dim cosine, and record model metadata. |
| `RAG-BT012` | Ingest only approved fixture/canonical material; preserve source/chunk lineage; keep fast tests Docker-free and Qdrant integration separated. |
| `RAG-BT015` | Implement deterministic safeguards/planner before retrieval; blocked classes must not call retrieval or generation. |
| `RAG-BT013` | Build semantic retrieval as baseline only; record scores, source lineage, embedding metadata, and expected chunk presence. |
| `RAG-BT014` | Implement hybrid retrieval/fusion, metadata boosts, tie-breaks, rerank hook, and low-confidence/no-evidence behavior. |
| `RAG-BT016` | Build generation messages from DT019 roles; treat retrieved chunks as untrusted; keep provider calls injectable and mocked by default. |
| `RAG-BT017` | Enforce response schema, citations, refusal/error envelopes, bounded retry, and fallback behavior. |
| `RAG-BT018` | Implement `POST /api/v1/query`; expose planner, retrieval mode, confidence, score trace, citations, and safe responses. |
| `RAG-BT019` | Produce unit/mocked, service-backed Qdrant, API-level, and optional LLM-judge reports separately. |
| `RAG-BT020` | Prove Docker/local ops with app and Qdrant profiles, readiness checks, `.dockerignore`, and no legacy runtime mount. |
| `RAG-BT021` | Document logs, troubleshooting, runtime config, provider errors, and citation/refusal observability. |
| `RAG-BT022` | Consume DT016/DT017/DT020 evidence and accepted deferrals before readiness signoff. |

## Accepted Deferrals

| deferral | owner | unblock_condition | downstream_rule |
|---|---|---|---|
| Production canonical KB promotion | solo developer | A later source-promotion/corpus task accepts production material. | Build tasks may use explicitly marked fixtures/review candidates only. |
| Qdrant env-var naming reconciliation | solo developer | First Qdrant-backed implementation task chooses documented names or aliases. | `RAG-BT012`, `RAG-BT013`, and `RAG-BT020` must not complete with ambiguous config names. |
| Qdrant service-container CI promotion | solo developer | `RAG-BT012` and `RAG-BT013` create real seeded retrieval fixtures. | Until then, Qdrant-backed CI may be advisory but must be planned. |
| Docker image smoke/container scan | solo developer | `RAG-BT020` owns Dockerfile/Compose runtime surface. | `RAG-BT022` cannot pass readiness without proof or explicit acceptance. |
| Repo security enforcement and dependency provenance | solo developer | Security/repo settings and suspicious dependency provenance are reviewed or accepted. | `RAG-BT022` must carry this as readiness evidence. |
| Runtime LLM judge gating | solo developer | Cost, latency, reliability, and bias are assessed after evaluation harness exists. | `RAG-BT019` uses LLM judge only as optional evaluation, not runtime gating. |

## Final Gate

DT013 approves transition into final build tasks with conditions. The build lane
may start with `RAG-BT007`, but each build task must satisfy its DT013 handoff
before it can be marked complete.
