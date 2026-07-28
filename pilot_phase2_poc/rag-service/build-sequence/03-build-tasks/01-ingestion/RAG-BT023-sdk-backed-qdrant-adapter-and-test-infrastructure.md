# RAG-BT023: SDK-Backed Qdrant Adapter And Disposable Test Infrastructure

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-BT023` |
| Lane | build |
| Dependencies | `RAG-BT005`, `RAG-BT010`, `RAG-BT011`, `RAG-DT014`, `RAG-DT021`, `RAG-DT023`, `RAG-DT025`, `RAG-DT013` |
| Blocks | `RAG-BT012`, `RAG-BT013`, `RAG-BT014`, `RAG-BT018`, `RAG-BT019`, dependency-aware readiness |
| Branch | `codex/rag-bt023-qdrant-adapter-test-infrastructure` |
| Worktree | `C:\tmp\rag-bt023-qdrant-adapter-test-infrastructure` |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT023-qdrant-adapter-test-infrastructure.md` |

## 1. Objective And Scope

Replace the mock-only Qdrant-shaped boundary with a locked, lifespan-managed
SDK adapter and disposable service-backed test environment before ingestion or
retrieval claims real Qdrant support.

## 2. Dependencies And Gates

The collection shape must use the accepted embedding dimension/distance and
the current corpus namespace/version contract. Local Qdrant ports must bind to
`127.0.0.1`; unauthenticated Qdrant is local-only.

## 3. Expected Artifacts

```text
app/shared/vector_db/qdrant_adapter.py
app/shared/vector_db/collection_lifecycle.py
tests/integration/vector_db/
docker-compose.test.yml
.github/workflows/rag-service-qdrant-integration.yml
build-evidence/RAG-BT023-qdrant-adapter-test-infrastructure.md
```

## 4. Acceptance Criteria

- A locked `qdrant-client` dependency is installed.
- One lifespan-managed `AsyncQdrantClient` is created and closed correctly.
- Logical chunk IDs map deterministically to Qdrant-compatible UUID/uint64 IDs
  while retaining the original `chunk_id` in payload.
- SDK-native points, filters, selectors, and query APIs are used.
- Create-or-validate collection behavior rejects incompatible vector
  size/distance and manages required payload indexes.
- TLS, API key, URL, timeout, collection, and namespace/version settings are
  environment driven and secret safe.
- Collection migration/version incompatibility has an explicit failure and
  rollback path.
- Real upsert/search/filter/delete integration tests pass against a disposable
  Qdrant service in local and required CI.
- Unique collection prefixes, readiness timeout, seed, teardown, and
  failure-cleanup are proven.

## 5. Preflight

Verify Docker/Compose availability, record whether the daemon is running, and
confirm no developer collection or volume will be targeted by tests.

## 6. Red Check

Write service-backed integration tests first. They must fail because the SDK
adapter, test Compose service, collection lifecycle, and dependency do not yet
exist. Mock-only tests are not the red check for this task.

## 7. Implementation Or Design Work

Implement the async adapter, collection lifecycle, deterministic ID mapping,
test Compose profile, integration fixtures, and CI service job. Do not move
application-image work from `RAG-BT020` into this task.

## 8. Verification Matrix

| Check | Required Result |
|---|---|
| Dependency lock | `qdrant-client` resolves from `uv.lock` |
| Collection contract | Create and validate pass; incompatible schema fails |
| Data lifecycle | Upsert, query/filter, delete, and teardown pass on real Qdrant |
| Failure cleanup | Interrupted/failed test leaves no shared collection |
| CI | Required service-backed integration job passes |
| Security | Local ports are loopback-bound and secrets are absent from logs |

## 9. PR Handoff

Include dependency/version, collection schema, local command, CI job, cleanup
proof, failure cases, and evidence path.

## 10. Merge And Closeout

Merge only after mock/unit checks and real Qdrant integration checks pass on
the PR and refreshed `main`.

## 11. Out Of Scope And Deferred Work

Production Qdrant topology, HA, and backup infrastructure remain governed by
`RAG-DT023`. Real SDK boundary correctness and disposable integration testing
are not deferrable for `RAG-BT012`.

## DT013 Final Design Handoff

- Start only after `RAG-DT013` Revision 2 returns `GO`.
- Consume the exact collection, security, reliability, CI, and cleanup
  decisions approved by DT013.
- Update this task before implementation if DT013 changes the adapter,
  collection, namespace, or test-infrastructure contract.
