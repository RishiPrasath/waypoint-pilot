# RAG-DT014 Test Vector DB And CI Integration Strategy

Status: Accepted
Run: `dt014-run-001`

## Decision Summary

This strategy defines how the RAG service should test Qdrant-backed vector
database behavior without confusing three different environments:

1. unit/mock tests with no real Qdrant service
2. local integration tests against a local Docker Qdrant service
3. CI integration tests against a GitHub Actions Qdrant service container

The recommended gate decision is:

```text
Use GitHub Actions service container for CI integration tests.
Use Docker Compose profile for local developer parity.
Use Qdrant local/in-memory mode only for unit/design benchmarks, not
service-backed integration proof.
```

Owner decision status is recorded in:

```text
docs/design/experiments/vector-db-ci-strategy/dt014-run-001/decision-gate.md
```

## Reference Basis

- GitHub service containers:
  `https://docs.github.com/actions/tutorials/communicating-with-docker-service-containers`
- GitHub service container health-check pattern:
  `https://docs.github.com/actions/guides/creating-postgresql-service-containers`
- Qdrant local quickstart:
  `https://qdrant.tech/documentation/quickstart/`
- Qdrant Docker/installation guidance:
  `https://qdrant.tech/documentation/installation/`
- Qdrant monitoring and health endpoints:
  `https://qdrant.tech/documentation/ops-monitoring/monitoring/`

## Test Modes

| Mode | Qdrant service? | Intended command | Purpose | Gate status |
|---|---|---|---|---|
| Unit/mock | No | `uv run python -m pytest -q` | Fast PR-safe unit checks with mocked vector DB boundary. | Always required. |
| Local integration | Yes, Docker Compose Qdrant | `uv run python -m pytest -m integration -q` after local Qdrant starts | Developer parity with service-backed Qdrant. | Manual/advisory until BT012/BT013 exist. |
| CI integration | Yes, GitHub Actions service container | `uv run python -m pytest -m integration -q` | PR CI proof against real Qdrant service. | Required after BT012 + BT013. |

## Qdrant Runtime Contract

| Field | Value |
|---|---|
| Docker image | `qdrant/qdrant` |
| REST/HTTP port | `6333` |
| Optional gRPC port | `6334` |
| Local default URL | `http://localhost:6333` |
| Readiness endpoint | `http://localhost:6333/readyz` |
| Local readiness timeout | 30 seconds |
| CI readiness timeout | 60 seconds |
| Test authentication | `QDRANT_API_KEY` unset by default for isolated local/CI test services |

Qdrant exposes `/healthz`, `/livez`, and `/readyz`; use `/readyz` as the
readiness gate before integration tests run.

## Environment Variable Contract

| Variable | Required? | Default | Purpose |
|---|---|---|---|
| `QDRANT_URL` | yes for integration | `http://localhost:6333` | Qdrant service URL. |
| `QDRANT_API_KEY` | optional | unset | API key only if a secured Qdrant test service is intentionally configured. |
| `QDRANT_COLLECTION_PREFIX` | yes | `rag_test` | Prefix for unique disposable test collections. |
| `QDRANT_TEST_TIMEOUT_SECONDS` | yes | `60` | Upper bound for readiness/test waits in CI. |
| `RUN_QDRANT_INTEGRATION` | yes for local opt-in | unset/`0` locally, `1` in CI integration job | Prevent accidental local integration runs when Qdrant is unavailable. |

Never print `QDRANT_API_KEY` or any secret value in evidence, logs, test
failure details, or CI summaries.

## Vector Contract From DT010

The vector DB integration tests must align with the accepted DT010 embedding
benchmark result:

```text
embedding_provider = fastembed
embedding_model = BAAI/bge-small-en
embedding_dimension = 384
embedding_distance = cosine
benchmark_run_id = dt010-run-001
```

Design prose may say `cosine`; Qdrant/client code should use `Cosine` if the
SDK enum or config expects title case.

## Collection Naming And Cleanup

Collections must be disposable and unique per test run.

Recommended pattern:

```text
rag_test_<task_id>_<run_id>
```

Examples:

```text
rag_test_bt010_smoke_<uuid>
rag_test_bt012_fixture_ingestion_<uuid>
rag_test_bt013_semantic_retrieval_<uuid>
rag_test_bt014_hybrid_retrieval_<uuid>
```

Rules:

- cleanup before seed
- cleanup after test
- cleanup in fixture teardown or `finally`
- never reuse shared permanent collection names for tests
- print collection name in failure diagnostics
- do not delete collections without the configured `QDRANT_COLLECTION_PREFIX`

## Payload Schema Contract

Every test point payload should preserve enough lineage for retrieval and
evaluation assertions:

```json
{
  "payload_schema_version": "v1",
  "document_id": "APAC-001",
  "source_id": "APAC-001",
  "source_uri": "https://example.invalid/source",
  "snapshot_id": "snap-20260716-apac-001",
  "candidate_sha256": "sha256...",
  "chunk_id": "APAC-001-snap-20260716-apac-001-hsr-002",
  "chunk_strategy": "hybrid_structure_recursive_v1",
  "heading_path": ["Singapore Customs Import Permit Candidate", "Source-Derived Notes"],
  "section_part_index": 1,
  "recursive_split_applied": true,
  "retrieval_eligible": true,
  "content_hash": "sha256...",
  "embedding_provider": "fastembed",
  "embedding_model": "BAAI/bge-small-en",
  "embedding_dimension": 384,
  "benchmark_run_id": "dt010-run-001"
}
```

## Seed And Bootstrap Lifecycle

Initial integration tests should generate live embeddings through the runtime
adapter once BT011 exists. Do not commit large static vector dumps unless a
later debugging task explicitly needs them.

Lifecycle:

1. Load approved DT005/DT012 chunk fixture rows.
2. Generate embeddings through the BT011 adapter.
3. Create a unique Qdrant test collection.
4. Upsert points with payload metadata.
5. Run retrieval assertions.
6. Record seed count, collection name, and top-k IDs on failure.
7. Delete the test collection in teardown.

Seed fixture source:

```text
docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl
```

Golden retrieval assertions should use:

```text
docs/evaluation/golden-questions.md
docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-results.jsonl
```

## Pytest Marker And Commands

Add marker registration when integration tests are implemented:

```toml
[tool.pytest.ini_options]
markers = [
  "integration: tests requiring external local services such as Qdrant",
]
```

Commands:

```powershell
uv run python -m pytest -q
uv run python -m pytest -m "not integration" -q
uv run python -m pytest -m integration -q
```

Local integration tests may skip with a clear message if
`RUN_QDRANT_INTEGRATION` is not set or Qdrant is unavailable. CI integration
tests must fail if the Qdrant service container is expected but unavailable.

## Local Docker Compose Shape

DT014 does not implement the Compose file. It defines the expected shape for
BT020 or the later Docker/local ops task.

Expected local profile:

```yaml
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    profiles:
      - test
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/readyz"]
      interval: 5s
      timeout: 3s
      retries: 12
```

Expected local commands:

```powershell
docker compose --profile test up -d qdrant
uv run python -m pytest -m integration -q
docker compose --profile test down
```

Current local check for this run:

```text
docker --version -> Docker version 28.5.1
docker compose version -> Docker Compose version v2.40.3-desktop.1
docker info -> initially unavailable; Docker Desktop launched from command line
docker info -> Docker daemon ready, server version 28.5.1
qdrant/qdrant:latest -> disposable container started as rag-dt014-qdrant-test
http://localhost:6333/readyz -> 200, all shards are ready
http://localhost:6333/healthz -> 200, healthz check passed
http://localhost:6333/livez -> 200, healthz check passed
qdrant version from logs -> 1.18.3
cleanup -> container removed; no rag-dt014-qdrant-test container remained
```

That means local Docker integration is viable on this machine after Docker
Desktop starts. DT014 validated the local Qdrant service path with `docker run`;
the durable Compose profile remains a later implementation task.

## GitHub Actions Service Container Shape

DT014 does not implement the workflow. It defines the expected shape for the
future CI change.

```yaml
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - 6333:6333
      - 6334:6334
    options: >-
      --health-cmd "curl -f http://localhost:6333/readyz || exit 1"
      --health-interval 5s
      --health-timeout 3s
      --health-retries 12
```

Expected CI command:

```powershell
uv run python -m pytest -m integration -q
```

Expected CI env:

```text
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_PREFIX=rag_test
QDRANT_TEST_TIMEOUT_SECONDS=60
RUN_QDRANT_INTEGRATION=1
```

## CI Gating Phases

| Phase | Gate |
|---|---|
| Before BT012/BT013 | PR CI runs unit tests only. Qdrant integration tests may be manual, scheduled, or advisory. |
| After BT012 + BT013 | Qdrant ingestion/retrieval integration tests become required in PR CI. |
| After BT020 | Docker Compose/container smoke tests may join CI or release checks. |

## Failure Handling And Diagnostics

On integration failure, report:

- `QDRANT_URL` without credentials
- collection name
- collection count when available
- seed count
- top-k result IDs
- readiness response
- pytest output
- `docker ps`
- `docker logs <qdrant-container>` when running locally

Never print API keys or secret environment variable values.

## Security Boundary

Unauthenticated Qdrant is acceptable only for isolated local test containers and
GitHub Actions ephemeral service containers. Production Qdrant authentication,
networking, backups, and deployment remain out of scope for DT014.

## Downstream Build Task Handoff

Downstream tasks should receive this contract after owner decision acceptance:

```text
DT014 Vector DB Test Handoff:

- Qdrant test mode: unit/mock by default; service-backed integration under pytest marker.
- Local command: docker compose --profile test up -d qdrant; uv run python -m pytest -m integration -q.
- CI command: GitHub Actions service container plus uv run python -m pytest -m integration -q.
- Pytest marker: integration.
- Required env vars: QDRANT_URL, QDRANT_COLLECTION_PREFIX, QDRANT_TEST_TIMEOUT_SECONDS, RUN_QDRANT_INTEGRATION; QDRANT_API_KEY optional.
- Collection naming rule: rag_test_<task_id>_<run_id>.
- Seed fixture: DT005 hybrid chunks plus DT010 selected embedding model.
- Payload contract: payload_schema_version v1 plus DT005/DT012/DT010 lineage fields.
- Cleanup rule: before seed, after test, and in teardown/finally.
- CI gate timing: required after BT012 + BT013.
```

## Accepted Recommendation

The owner accepted this recommendation on 2026-07-17:

```text
Accept Option A for CI: GitHub Actions Qdrant service container.
Accept Option B for local developer parity: Docker Compose Qdrant test profile.
Limit Option C to unit/design benchmark usage: Qdrant local/in-memory mode.
```

This keeps local developer testing practical while giving CI a repeatable,
isolated, service-backed integration proof.
