# RAG-DT014 Decision Gate: Vector DB Test Strategy

Status: Accepted
Run: `dt014-run-001`

## Gate Definition

This gate is the formal decision checkpoint for the vector database integration
test strategy. Downstream build tasks should not depend on real Qdrant
integration behavior until this gate is accepted.

## Options

### Option A: GitHub Actions Qdrant Service Container

Use `qdrant/qdrant` as an ephemeral service container in GitHub Actions for CI
integration tests.

Decision status: Recommended for CI.

### Option B: Docker Compose Qdrant Test Profile

Use a local Docker Compose `test` profile to start Qdrant for developer
integration tests.

Decision status: Recommended for local developer parity.

### Option C: Qdrant Local/In-Memory Mode

Use Qdrant client local/in-memory mode for fast tests and design benchmarks.

Decision status: Recommended only for unit/design benchmark use, not as the
service-backed integration strategy.

## Recommendation

Accept the hybrid strategy:

```text
CI integration tests:
  GitHub Actions Qdrant service container

Local developer integration tests:
  Docker Compose Qdrant test profile

Unit/design benchmark tests:
  Qdrant local/in-memory mode
```

## Why This Recommendation

- It keeps normal unit tests fast and local.
- It gives developers a local real-Qdrant path when Docker is running.
- It gives PR CI a repeatable real-Qdrant service-backed integration proof.
- It avoids cloud/production Qdrant for tests.
- It preserves DT010’s local/in-memory mode for design benchmarking without
  pretending that it proves real service behavior.

## Proposed Contract If Accepted

```text
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=<unset for isolated local/CI tests>
QDRANT_COLLECTION_PREFIX=rag_test
QDRANT_TEST_TIMEOUT_SECONDS=60
RUN_QDRANT_INTEGRATION=1 for integration jobs
```

```text
embedding_provider=fastembed
embedding_model=BAAI/bge-small-en
embedding_dimension=384
embedding_distance=cosine/Cosine
benchmark_run_id=dt010-run-001
```

Required readiness check:

```text
http://localhost:6333/readyz
```

Required pytest marker:

```text
integration
```

## Evidence Summary

- GitHub Actions supports service containers for CI dependencies.
- Qdrant supports Docker/local operation.
- Qdrant exposes `/healthz`, `/livez`, and `/readyz` endpoints.
- DT010 proved Qdrant local/in-memory mode for embedding benchmark work.
- Local machine check during DT014:
  - Docker CLI installed: Docker version 28.5.1
  - Docker Compose installed: v2.40.3-desktop.1
  - Docker Desktop launched from command line
  - Docker daemon became ready: server version 28.5.1
  - Disposable `qdrant/qdrant:latest` container started as `rag-dt014-qdrant-test`
  - `/readyz`, `/healthz`, and `/livez` returned HTTP 200
  - Qdrant version from logs: 1.18.3
  - Container cleanup verified

## Risks And Mitigations

| Risk | Mitigation |
|---|---|
| CI test starts before Qdrant is ready | Use `/readyz` health check and 60-second CI readiness timeout. |
| Local developer Docker is not running | Integration tests skip locally unless `RUN_QDRANT_INTEGRATION=1`; docs tell user to start Docker Desktop. |
| Test collections collide or leak | Use unique `rag_test_<task_id>_<run_id>` collection names and cleanup before/after tests. |
| API keys leak in logs | Do not print `QDRANT_API_KEY`; default local/CI test Qdrant is unauthenticated and isolated. |
| Integration tests become required too early | Keep them advisory until BT012 + BT013 exist. |

## Downstream Tasks Released By Gate Acceptance

- `RAG-BT010`: live Qdrant smoke-test contract
- `RAG-BT012`: fixture ingestion into Qdrant
- `RAG-BT013`: semantic retrieval against seeded Qdrant
- `RAG-BT014`: hybrid retrieval against seeded Qdrant
- `RAG-BT019`: Qdrant-backed retrieval evaluation reporting
- `RAG-BT020`: Docker Compose/local runtime implementation

## Owner Decision

Status: Accepted

Decision choices:

```text
Accepted recommendation
Reject recommendation
Defer decision
Request changes
```

Owner notes:

```text
Accepted by owner on 2026-07-17. Lock the hybrid vector DB CI strategy:
Qdrant in-memory for fast unit/design checks, local Docker/Compose Qdrant
before push for service-backed local verification, and GitHub Actions Qdrant
service container as the PR/merge gate.
```
