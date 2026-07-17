# RAG-DT011 Docker And Local Ops Design

Status: Accepted for review
Date: 2026-07-18

## Purpose

This document defines the local Docker and operational design for the
`rag-service`. It gives future implementation tasks a clear target without
building the Docker runtime in this design task.

The design answers:

- how the FastAPI app, local Qdrant, and developer commands should fit
  together;
- which checks stay fast and local;
- which checks require Dockerized services;
- how local health, readiness, logs, seed/bootstrap, and cleanup should work;
- which Docker and security stages belong to later implementation and CI tasks.

## Inputs

- `RAG-DT014` accepted vector DB test strategy:
  - Qdrant in-memory for fast unit/design checks;
  - local Docker/Compose Qdrant before push for real local integration proof;
  - GitHub Actions Qdrant service container as the PR/merge gate.
- `RAG-BT004` Stage 1 CI boundary:
  - Stage 1 CI does not build Docker images and does not require Dockerized
    dependencies.
- Current local environment check:
  - Docker CLI: `28.5.1`;
  - Docker Compose: `v2.40.3-desktop.1`;
  - Docker daemon: running, server `28.5.1`.
- Official references:
  - Docker Compose service `healthcheck` and dependency behavior:
    `https://docs.docker.com/reference/compose-file/services/`
  - Docker Compose startup order with `service_healthy`:
    `https://docs.docker.com/compose/how-tos/startup-order/`
  - FastAPI Docker deployment guidance:
    `https://fastapi.tiangolo.com/deployment/docker/`
  - Qdrant Docker and Compose installation guidance:
    `https://qdrant.tech/documentation/installation/`
  - Qdrant security guidance:
    `https://qdrant.tech/documentation/security/`
  - Trivy GitHub Action:
    `https://github.com/aquasecurity/trivy-action`

## Decision Summary

Use a two-profile Docker Compose design:

```text
default profile:
  qdrant only

app profile:
  rag-service API container plus qdrant

test profile:
  qdrant plus optional integration-test runner behavior
```

In practice, the first implementation should keep Compose simple:

```powershell
docker compose up -d qdrant
docker compose --profile app up --build rag-service
docker compose --profile test up -d qdrant
```

The app container is useful for local runtime and container smoke tests. The
Qdrant-only test profile is useful for local integration tests run from the host
with `uv`.

## Local Runtime Shape

The future `RAG-BT020` implementation should create:

```text
pilot_phase2_poc/rag-service/
  Dockerfile
  docker-compose.yml
  .dockerignore
  docs/ops/local-docker-run.md
```

Recommended services:

| Service | Purpose | Required Now? |
|---|---|---|
| `qdrant` | local vector database dependency | yes for integration tests |
| `rag-service` | FastAPI app container | yes for local runtime smoke |
| `rag-service-test` | optional containerized test runner | deferred unless DT016 requires CI parity |

Recommended ports:

| Service | Container Port | Host Port |
|---|---:|---:|
| `rag-service` | `8000` | `8000` |
| `qdrant` REST | `6333` | `6333` |
| `qdrant` gRPC | `6334` | `6334` |

## Dockerfile Design

The future Dockerfile should:

- use a Python 3.12 base image unless `RAG-DT016` selects a different pinned
  CI-compatible base;
- install dependencies using `uv`;
- copy only the service package and required config;
- run from the service root;
- expose port `8000`;
- start the app with Uvicorn against `app.main:app`;
- keep secrets out of image layers;
- avoid mounting or copying `legacy/phase1-kb-snapshot/` as runtime KB input.

Recommended command shape:

```text
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The exact implementation can use either installed console scripts or `uv run`
inside the image, but `RAG-BT020` must prove the image starts consistently.

## Compose Design

Recommended conceptual Compose shape:

```yaml
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/readyz"]
      interval: 5s
      timeout: 3s
      retries: 12

  rag-service:
    build:
      context: .
      dockerfile: Dockerfile
    profiles:
      - app
    ports:
      - "8000:8000"
    environment:
      RAG_ENV: local
      QDRANT_URL: http://qdrant:6333
      QDRANT_COLLECTION_PREFIX: rag_local
      QDRANT_TEST_TIMEOUT_SECONDS: "60"
    depends_on:
      qdrant:
        condition: service_healthy
```

Important implementation note: verify whether the selected Qdrant image
contains `curl` before using a container-internal healthcheck command. If not,
`RAG-BT020` should use a tiny sidecar/check script, host-level readiness wait,
or another command available in the image. The readiness endpoint remains
`/readyz`.

## Local Commands

Default fast checks, no Docker:

```powershell
Set-Location pilot_phase2_poc/rag-service
uv run python -m pytest -q
```

Start only Qdrant for host-run integration tests:

```powershell
docker compose --profile test up -d qdrant
$env:RUN_QDRANT_INTEGRATION = "1"
$env:QDRANT_URL = "http://localhost:6333"
$env:QDRANT_COLLECTION_PREFIX = "rag_test"
$env:QDRANT_TEST_TIMEOUT_SECONDS = "60"
uv run python -m pytest -m integration -q
docker compose --profile test down
```

Run app and Qdrant together:

```powershell
docker compose --profile app up --build
Invoke-WebRequest http://localhost:8000/health
Invoke-WebRequest http://localhost:8000/ready
Invoke-WebRequest http://localhost:6333/readyz
docker compose --profile app down
```

Container smoke test shape:

```powershell
docker compose --profile app up -d --build
Invoke-WebRequest http://localhost:8000/health
Invoke-WebRequest http://localhost:8000/ready
docker compose --profile app logs --tail 100 rag-service
docker compose --profile app down
```

## Test Mode Separation

| Mode | Docker Required? | Command | Purpose |
|---|---|---|---|
| Unit/API smoke | no | `uv run python -m pytest -q` | Fast feedback for app, schemas, config, pure logic. |
| In-memory vector checks | no | task-specific benchmark/test command | Fast vector logic/design checks. |
| Local Qdrant integration | yes, Qdrant only | `docker compose --profile test up -d qdrant`; `uv run python -m pytest -m integration -q` | Real local Qdrant proof before push. |
| Local app runtime smoke | yes, app + Qdrant | `docker compose --profile app up --build` | Prove FastAPI container boots and health/readiness works. |
| CI Qdrant integration | GitHub Actions service container | `uv run python -m pytest -m integration -q` | PR/merge-gate proof after BT012/BT013. |

## Environment Variables

| Variable | Scope | Required? | Default/Local Value | Notes |
|---|---|---|---|---|
| `RAG_ENV` | app | yes | `local` | Distinguishes local/dev/test behavior. |
| `LOG_LEVEL` | app | optional | `INFO` | Must not expose secrets. |
| `HOST` | app | optional | `0.0.0.0` in container | Host binding for container runtime. |
| `PORT` | app | optional | `8000` | App port. |
| `QDRANT_URL` | integration/app | yes when using Qdrant | host: `http://localhost:6333`; container: `http://qdrant:6333` | Use service DNS inside Compose. |
| `QDRANT_API_KEY` | integration/app | optional | unset | Do not use for isolated local test Qdrant unless intentionally securing it. |
| `QDRANT_COLLECTION_PREFIX` | integration/app | yes | `rag_local` or `rag_test` | Prevent collection collisions. |
| `QDRANT_TEST_TIMEOUT_SECONDS` | tests | yes for integration | `60` | Upper bound for readiness waits. |
| `RUN_QDRANT_INTEGRATION` | tests | yes for integration | unset/`0` locally, `1` when opted in | Prevent accidental Docker dependency in fast tests. |

## Health And Readiness

FastAPI app:

- `/health` proves the API process is alive.
- `/ready` should remain lightweight and eventually check required runtime
  dependencies.
- Container smoke must call both endpoints after app boot.

Qdrant:

- `/readyz` is the readiness gate before integration tests.
- `/healthz` and `/livez` are useful diagnostics.
- Use a 30-second local wait and 60-second CI wait unless a later task proves a
  better value.

Readiness failure diagnostics must include:

```powershell
docker compose ps
docker compose logs --tail 100 qdrant
docker compose logs --tail 100 rag-service
Invoke-WebRequest http://localhost:6333/readyz
Invoke-WebRequest http://localhost:8000/ready
```

## Seed And Bootstrap

`RAG-DT011` does not create ingestion seed data. It defines the runtime shape
that future tasks must use.

Bootstrap sequence for future integration tasks:

1. Start Qdrant.
2. Wait for `/readyz`.
3. Create a unique collection using `QDRANT_COLLECTION_PREFIX`.
4. Seed fixture data from the owning task:
   - BT012 owns fixture ingestion;
   - BT013 owns semantic retrieval seed expectations;
   - BT014 owns hybrid retrieval comparison;
   - BT019 owns evaluation reports.
5. Run assertions.
6. Delete task-owned collections in teardown/finally.
7. Stop Compose services.

Do not seed from `legacy/phase1-kb-snapshot/` unless a completed design task
explicitly promoted the material.

## Logs And Local Diagnostics

Minimum local diagnostics:

- `docker compose ps`
- `docker compose logs --tail 100 rag-service`
- `docker compose logs --tail 100 qdrant`
- readiness responses from app and Qdrant
- pytest output
- collection cleanup result for integration tests

Logs must not print:

- API keys;
- raw external provider credentials;
- full environment dumps;
- unredacted future user queries if they contain sensitive content.

`RAG-BT021` should turn this into an ops checklist and logging/redaction
implementation.

## CI/CD Boundary

`RAG-DT011` does not implement CI/CD workflows. It defines what later CI/CD
tasks should prove.

CI maturity recommendation:

| Stage | Owner | Required Now? |
|---|---|---|
| Stage 1 Python tests/lint/security | BT004 | already owned by setup |
| Qdrant service-container integration | DT014/BT012/BT013/DT016 | required after ingestion + retrieval exist |
| Docker image build | BT020/DT016 | required once Dockerfile exists |
| Container smoke test | BT020/DT016 | required once Dockerfile and health/readiness are stable |
| Trivy image scan | BT020/DT016 or BT022 | recommended after image build exists |
| Production readiness review | BT022 | final review only |

DT016 must audit and implement the CI/CD gaps. DT011 only sets the Docker/local
runtime target.

## Security And Data Governance

- Local unauthenticated Qdrant is acceptable only for isolated developer and CI
  test containers.
- Production Qdrant authentication, TLS, backups, and deployment topology remain
  out of scope.
- Compose must not mount `legacy/phase1-kb-snapshot/` as runtime KB input.
- Runtime KB mounts must use approved `knowledge_base/` paths only.
- `.dockerignore` must exclude `.venv`, caches, local secrets, `.env` files,
  and unrelated repo material.
- If an `.env.example` is added later, it must contain names and safe defaults,
  not secrets.

## Build Task Handoff

```text
DT011 Docker/Local Ops Handoff:

- Dockerfile owner: RAG-BT020.
- Compose owner: RAG-BT020.
- Default fast command: uv run python -m pytest -q.
- Local Qdrant command: docker compose --profile test up -d qdrant.
- Local integration command: RUN_QDRANT_INTEGRATION=1 plus uv run python -m pytest -m integration -q.
- Local app runtime command: docker compose --profile app up --build.
- Health endpoints: app /health and /ready; Qdrant /readyz.
- Logs: docker compose logs --tail 100 rag-service and qdrant.
- Seed/bootstrap: owned by BT012/BT013/BT014/BT019, not DT011.
- Security: no secrets in image layers, logs, or committed env files.
- CI boundary: DT016 decides and implements workflow gaps; DT011 defines the local runtime target.
```

## Decision

Accepted for review:

- implement Dockerfile and Compose local runtime in `RAG-BT020`;
- keep Docker out of default unit tests;
- use Qdrant-only Compose profile for local integration tests;
- use app+Qdrant Compose profile for local runtime smoke;
- defer production deployment, Kubernetes, managed Qdrant, and backup design;
- let `RAG-DT016` own CI/CD implementation and proof.
