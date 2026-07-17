# RAG-DT014 Vector DB CI Options Assessment

Run: `dt014-run-001`
Status: Accepted

## Options Assessed

| Option | Name | Summary |
|---|---|---|
| A | GitHub Actions Qdrant service container | CI runner starts a temporary `qdrant/qdrant` container for integration tests. |
| B | Docker Compose Qdrant test profile | Developer machine starts local Qdrant through a Compose `test` profile. |
| C | Qdrant local/in-memory mode | Python process uses Qdrant client local/in-memory mode without a Qdrant server. |

## Assessment Matrix

| Criterion | Option A: GitHub Actions service container | Option B: Docker Compose test profile | Option C: local/in-memory |
|---|---|---|---|
| Repeatability | Strong in CI because service is rebuilt per workflow run. | Good locally if Docker Desktop is running and Compose file is stable. | Strong for isolated design/unit checks, but not service-backed. |
| CI suitability | Best fit. GitHub Actions officially supports service containers and port mapping. | Possible but heavier inside CI and overlaps with Docker/local ops. | Weak for CI integration proof because it avoids real Qdrant service behavior. |
| Local developer usability | Not local; only available through PR/CI or local Actions emulation. | Best local parity path, assuming Docker daemon is running. | Easiest local path; no Docker required. |
| Startup complexity | Moderate; requires workflow service definition and readiness. | Moderate; requires Compose file/profile and local Docker. | Low. |
| Health-check support | Good; service `options` can define health checks. | Good; Compose healthcheck can use `/readyz`. | Not applicable as service readiness proof. |
| Cleanup safety | Good if tests use unique prefixed collections and teardown. | Good if tests use unique prefixed collections and teardown. | Good, because memory mode disappears with process. |
| Ingestion/retrieval compatibility | Strong. Proves real Qdrant API path. | Strong. Proves real Qdrant API path locally. | Partial. Useful for fast logic tests but not service/network behavior. |
| Security/secrets risk | Low if ephemeral and unauthenticated, with no secrets logged. | Low if bound locally and unauthenticated. | Very low; no networked service. |
| Deferred work | Workflow implementation later. | Compose implementation later. | Already used by DT010; no new service work. |

## Option A: GitHub Actions Qdrant Service Container

### Pros

- Best CI integration fit.
- Ephemeral service container is created and destroyed per workflow run.
- Matches the project need for PR-time service-backed Qdrant verification.
- Does not require a production Qdrant instance or cloud Qdrant account.
- GitHub Actions supports service containers, port mapping, and Docker health
  options.

### Cons

- Not a local developer command.
- Requires CI workflow work in a later implementation task.
- Debugging service startup failures requires CI logs and diagnostics.

### Risks

- Service readiness race if tests begin before Qdrant is ready.
- Hidden flakiness if collection cleanup is weak.
- Workflow could become slow if integration tests run too early in the build
  sequence.

### Mitigations

- Use `/readyz` health checks.
- Use 60-second CI readiness timeout.
- Use unique `rag_test_<task_id>_<run_id>` collections.
- Keep integration tests advisory/manual until BT012 + BT013 exist.

### Assessment

Recommended for CI integration tests.

## Option B: Docker Compose Qdrant Test Profile

### Pros

- Best local parity with a real Qdrant service.
- Gives developers a repeatable command to reproduce CI-style failures.
- Keeps broader Docker app runtime separate from this vector DB test strategy.

### Cons

- Requires Docker Desktop/daemon to be running.
- Requires a Compose profile to be implemented later.
- Can overlap with DT011/BT020 unless the boundary is clear.

### Local Check

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

This machine has Docker Desktop and can run a real local Qdrant service after
Docker Desktop starts. The DT014 smoke test used `docker run` rather than a
durable Compose profile, so the recommended Compose implementation is still a
future build task, but the local service-backed path is proven feasible.

### Risks

- Local runs fail with confusing errors if Docker daemon is stopped.
- Developers may accidentally leave containers or test collections behind.

### Mitigations

- Use `RUN_QDRANT_INTEGRATION=1` opt-in for local integration tests.
- Document startup/teardown commands.
- Use collection prefix cleanup.
- Print clear skip messages when local Qdrant is unavailable.

### Assessment

Recommended for local developer parity after the Compose profile exists.

## Option C: Qdrant Local/In-Memory Mode

### Pros

- Fastest and simplest local mode.
- No Docker required.
- Useful for design benchmarks and unit-ish tests.
- Already proven in DT010 embedding benchmark.

### Cons

- Does not prove real Qdrant server startup, network, HTTP/gRPC, Docker, or CI
  service behavior.
- Not sufficient as the only integration-test strategy.

### Risks

- If treated as the integration strategy, it could hide failures that only
  happen against a real Qdrant service.

### Mitigations

- Keep local/in-memory mode for unit/design benchmarks only.
- Use service-backed Qdrant for actual ingestion/retrieval integration gates.

### Assessment

Recommended only for unit/design benchmarks, not service-backed integration
proof.

## Recommendation

Use the accepted hybrid decision:

```text
Option A accepted for CI integration tests.
Option B accepted for local developer parity.
Option C limited to unit/design benchmark usage.
```

This gives the project:

- fast unit tests
- local reproduction path
- CI service-backed proof
- no production/cloud Qdrant dependency

## Evidence Basis

- GitHub Actions supports Docker service containers and port mapping.
- Qdrant provides official Docker/local startup guidance.
- Qdrant exposes `/healthz`, `/livez`, and `/readyz` readiness/liveness
  endpoints.
- DT010 already used Qdrant local/in-memory mode successfully for design-time
  embedding benchmark work, but that does not replace service-backed Qdrant.
