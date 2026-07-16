# RAG Service Architecture Confirmation Checklist

Status: Reconciled against the current `main` implementation and build sequence
Date: 2026-07-16
Owner: Waypoint RAG service team
Related design task: `RAG-DT001`

## Purpose

This checklist is the Phase 2 architecture source of truth while the original
ADR/checklist paths referenced by `RAG-DT001` are unavailable in this checkout.
Each row is backed by current repository evidence, an explicit design task, or
an explicit deferral. No legacy Phase 1 material is treated as active Phase 2
knowledge-base content.

## Decision status

| Area | Decision / current position | Status | Evidence or owner |
|---|---|---|---|
| Service framework | FastAPI application under `app/` | Implemented | `app/main.py`; BT001 evidence |
| Runtime version | Python 3.12 managed with `uv` | Accepted / implemented | `.python-version`; `pyproject.toml`; BT001 evidence |
| Service stages | Separate Python-safe packages for ingestion, query, retrieval, generation, and evaluation | Accepted / scaffolded | `app/stages/`; BT001 evidence |
| API foundation | `/health` and `/ready` endpoints | Implemented | `app/api/`; BT002 and BT003 evidence |
| Configuration | Pydantic settings with environment-driven runtime configuration | Implemented | `app/core/config.py`; BT005 evidence |
| Shared contracts | Shared base schemas and error envelope | Implemented | `app/shared/`; BT006 evidence |
| Vector database boundary | Qdrant-style wrapper with deterministic mocked operations for Stage 1 | Implemented with deferred integration | `app/shared/vector_db/`; BT010 evidence |
| CI quality gates | pytest, Ruff, Bandit, pip-audit, CodeQL, and Dependabot | Implemented | `.github/workflows/`; BT004 evidence |
| Branch workflow | Task branches/worktrees, PR review, CI, merge, and cleanup | Accepted / proven | BT000 evidence; current DT001 worktree |
| Active KB location | Phase 2 `knowledge_base/` root; exact promoted layout and registry location pending | Pending | `RAG-DT004` |
| Legacy KB usage | Phase 1 snapshot is audit input only and must not be ingested directly | Accepted | `legacy/PHASE1-KB-SNAPSHOT-AUDIT-NOTICE.md`; `RAG-DT002`, `RAG-DT003` |
| Source scope | APAC source candidates and promotion criteria pending explicit registry decision | Pending | `RAG-DT002`, `RAG-DT003`, `RAG-DT008` |
| Source registry | Schema, required metadata, validation, and storage pending | Pending | `RAG-DT008` |
| Canonical source materialization | Snapshot and canonical Markdown candidate rules pending | Pending | `RAG-DT012` |
| Chunking | Chunk boundaries, overlap, metadata, and fixture results pending experiment | Pending | `RAG-DT005` |
| Evaluation set | Golden questions, rubrics, and pass criteria pending | Pending | `RAG-DT006` |
| Query planning | Vocabulary, safeguards, out-of-scope handling, and deterministic planning pending | Pending | `RAG-DT007` |
| Embeddings | Model and benchmark acceptance pending | Pending | `RAG-DT010` |
| Generation model | Provider/model fixture and selection criteria pending | Pending | `RAG-DT009` |
| Vector DB integration tests | Test Qdrant lifecycle, seed data, cleanup, and CI strategy pending | Pending | `RAG-DT014` |
| Docker/local operations | Deferred until the integration-test strategy and local runtime scope are decided | Explicitly deferred | `RAG-DT011` |
| Build impact review | Final design-to-build dependency review not yet performed | Pending / gate | `RAG-DT013` |

## Build readiness

| Build area | Readiness | Reason |
|---|---|---|
| Setup foundation | Unblocked and complete | BT000–BT006 and BT010 evidence exists; BT004 and BT010 task-file status metadata is stale and should be corrected separately |
| Source registry validation (BT007) | Blocked | Requires DT004, DT008, and DT013 |
| Phase 1 KB audit artifacts (BT008) | Blocked | Requires DT002, DT003, and DT013 |
| Chunking and fixture harness (BT009) | Blocked | Requires DT002, DT005, DT012, and DT013 |
| Embedding adapter (BT011) | Blocked | Requires DT010 and DT013 |
| Fixture ingestion (BT012) | Blocked | Requires promoted KB, chunking, embedding, Qdrant test strategy, DT012, DT014, and DT013 |
| Query planning (BT015) | Blocked | Requires DT007 and DT013 |
| Retrieval (BT013/BT014) | Blocked | Requires ingestion fixtures, DT014, and DT013 |
| Generation (BT016/BT017) | Blocked | Requires DT009 and DT013, plus query safeguards for validation flow |
| Query API (BT018) | Blocked | Requires query, retrieval, generation, validation, and DT013 |
| Evaluation harness (BT019) | Blocked | Requires DT006, test DB strategy, query API, DT014, and DT013 |
| Docker/ops/readiness (BT020–BT022) | Blocked or deferred | Requires DT011/DT014/DT013 and completed runtime flow |

## Traceability notes

- The historical paths `02-rag-db/planning/architecture-confirmation-checklist.md`
  and `02-rag-db/adrs/` referenced by the task file are not present in the
  current repository. This checklist records that absence rather than treating
  undocumented decisions as accepted.
- The existing stage modules are scaffolds and contracts only; their presence
  does not indicate that ingestion, retrieval, generation, or evaluation
  behavior is complete.
- The Qdrant wrapper is intentionally a Stage 1 boundary. Real SDK-backed
  integration remains follow-up work governed by `RAG-DT014` and later build
  tasks.

## Unblocking sequence

The design lane should continue in this order:

```text
DT002 -> DT008 -> DT003 -> DT004 -> DT012 -> DT005 -> DT006
-> DT007 -> DT009 -> DT010 -> DT014 -> DT011 -> DT013
```

`DT001` establishes traceability. It does not approve the pending decisions or
authorize final RAG implementation by itself.
