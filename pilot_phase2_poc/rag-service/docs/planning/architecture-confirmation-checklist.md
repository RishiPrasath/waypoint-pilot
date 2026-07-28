# RAG Service Architecture Confirmation Checklist

Status: Reconciled after independent external-perspective review; final build blocked
Date: 2026-07-28
Owner: Waypoint RAG service team
Related design tasks: `RAG-DT001`, `RAG-DT021` through `RAG-DT025`

## Purpose

This checklist is the current architecture source of truth for the Phase 2
service. It distinguishes implemented scaffolding, historical design evidence,
open blocking decisions, fixture-only capability, canonical-corpus capability,
and production capability.

Historical task evidence remains part of the audit trail. It does not override
a current `Blocked / reopened` decision.

## Decision Status

| Area | Decision / current position | Status | Evidence or owner |
|---|---|---|---|
| Service framework | FastAPI application under `app/` | Implemented scaffold | `app/main.py`; BT001 evidence |
| Runtime version | Python 3.12 managed with `uv` | Implemented | `.python-version`; `pyproject.toml` |
| Service stages | Ingestion, query, retrieval, generation, and evaluation packages exist | Scaffolded; most files empty | `app/stages/` |
| API foundation | `/health` is liveness; `/ready` currently always returns success | Implemented but insufficient for integration | `app/api/`; BT002/BT003 |
| Configuration | Pydantic settings with environment-driven configuration | Implemented foundation | `app/core/config.py` |
| Shared contracts | Base schemas and error envelope exist but do not match the later DT019 schema in all fields | Reconciliation required | `app/shared/`; DT019 |
| Vector database boundary | Mock-injected Qdrant-shaped wrapper exists; no SDK client or collection lifecycle exists | Scaffold only | `app/shared/vector_db/`; BT010; BT023 |
| CI quality gates | pytest, Ruff lint, Bandit, pip-audit, CodeQL, and Dependabot exist | Implemented foundation | `.github/workflows/` |
| Legacy KB usage | Phase 1 snapshot is audit input only and must not be ingested directly | Accepted | `legacy/PHASE1-KB-SNAPSHOT-AUDIT-NOTICE.md` |
| Active KB | Registry/layout exist; no source is retrieval eligible and no canonical promoted corpus exists | Blocked for canonical use | DT024; BT024 |
| Source registry | Schema and candidate inventory exist; build-time validation remains open | Accepted design / unimplemented | DT008; BT007 |
| Corpus lifecycle | Promotion, freshness, annotation isolation, revocation, deletion, and rollback are not closed | Planned blocking gate | DT024 |
| Chunking | Design-time fixture experiment exists; curator annotations must be separated before canonical ingestion | Conditional PoC evidence | DT005; DT021; DT024 |
| Evaluation | Small smoke fixture exists; independent held-out, adversarial, and statistical gates do not | Planned blocking gate | DT006; DT022 |
| Query planning | Deterministic vocabulary/rules exist; phrase matching is not a security boundary | Accepted with revision impact | DT007; DT021 |
| Embeddings | `BAAI/bge-small-en` is a design-time candidate selected on the smoke fixture | Conditional PoC evidence | DT010; DT022 |
| Generation model | Historical `llama-3.3-70b-versatile` selection is superseded; Groq schedules free/developer shutdown on 2026-08-16 | Blocked / reopened | DT015; model-selection decision |
| Retrieval fusion/confidence | Fixed weights and thresholds exist without independent calibration | Blocked / reopened | DT018; DT022 |
| Generation/API/citations | Historical contract lacks closed trust/resource controls, claim-to-span support, and runtime schema reconciliation | Blocked / reopened | DT019; DT021-DT023 |
| Model/evaluation loop | Baseline-relative design lacks absolute gates and uncertainty requirements | Blocked / reopened | DT020; DT022; DT023 |
| Security/trust | Deployment tiers, poisoning, indirect injection, API abuse, privacy/logging, and resource controls are open | Planned blocking gate | DT021 |
| Reliability/deployment | SLOs, capacity/load, timeouts/concurrency, recovery, deployment, and operations ownership are open | Planned blocking gate | DT023 |
| Docker/local operations | Local design exists; loopback binding, pinned images, real Qdrant, and dependency readiness remain open | Blocked for runtime proof | DT011; BT020; BT023 |
| Build-task executability | Planned tasks use generic placeholders and at least one invalid Markdown/pytest workflow was found | Planned blocking gate | DT025 |
| Build impact review | Historical completion is superseded; Revision 2 waits for all new/reopened gates | Blocked / reopened | DT013 |

## Build Readiness

| Build area | Readiness | Reason |
|---|---|---|
| Setup foundation | Complete as scaffold | BT000-BT006 and BT010 do not implement RAG behavior |
| All final build tasks | Blocked | DT013 Revision 2 is blocked by DT021-DT025 and reopened decisions |
| Registry/audit/chunking/embedding mechanics | Conditional after Revision 2 | May be fixture-only and cannot imply a canonical corpus |
| Real Qdrant integration (BT023) | Blocked | Requires design gates, SDK adapter, collection lifecycle, and service CI |
| Fixture ingestion (BT012) | Blocked | Must explicitly depend on BT007, BT009, BT011, and BT023 |
| Canonical corpus release (BT024) | Blocked | Requires source-owner approval and DT024 lifecycle contract |
| Retrieval (BT013/BT014) | Blocked | Requires real Qdrant and independent fusion/confidence evaluation |
| Generation (BT016/BT017) | Blocked | Requires credential rotation proof and supported default/fallback selection |
| Query API (BT018) | Blocked | Requires reconciled schemas, trust/resource controls, and dependency readiness |
| Evaluation harness (BT019) | Blocked | Requires held-out/adversarial evaluation and reproducible scoring |
| Docker/ops/readiness (BT020-BT022) | Blocked | BT022 is PoC integration readiness only; production is a separate future program |

## Critical Current Facts

- The 12 passing tests cover scaffolding/contracts, not end-to-end RAG.
- The current registry has no retrieval-eligible source.
- The previously selected Groq model has a near-term free/developer-tier
  shutdown date.
- The current `/ready` endpoint is a static success and cannot be used as
  dependency-readiness evidence.
- The current Qdrant boundary is mock-compatible but not SDK/service backed.
- The existing golden fixture remains useful as a smoke fixture, not as the
  sole model, fusion, confidence, or production-quality selection set.
- A previously supplied Groq credential was reported as exposed in chat.
  Revocation/rotation evidence is required before any further live call.

## Required Unblocking Sequence

```text
DT021 security/trust
-> DT024 corpus lifecycle
-> DT022 evaluation validity
-> DT023 reliability/deployment
-> DT015 model-selection revision
-> DT018 retrieval-calibration revision
-> DT019 generation/API revision
-> DT020 evaluation/tuning revision
-> DT025 task/DAG/source-of-truth reconciliation
-> DT013 Revision 2 GO or NO-GO
```

After a `GO`, the executable build DAG must put real Qdrant integration
(`RAG-BT023`) before fixture ingestion (`RAG-BT012`). Canonical corpus release
(`RAG-BT024`) is required before canonical retrieval or any production track.

## Scope Of A Future Production Track

`RAG-BT022` is now a PoC integration-readiness gate. A future production gate
must be separately planned after DT023 selects a deployment target and must
include deployment/IAM/TLS, canonical corpus approval, backup/restore and
recovery objectives, capacity/load/cost evidence, SLOs/alerts/on-call,
incident/rollback rehearsal, provider privacy/retention, and operational
ownership.
