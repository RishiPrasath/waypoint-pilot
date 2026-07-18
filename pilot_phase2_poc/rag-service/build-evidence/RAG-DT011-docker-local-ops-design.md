# RAG-DT011 Evidence

Status: Complete

## Identity

Task: RAG-DT011 - Define Docker And Local Ops Design
Branch: `codex/rag-dt011-docker-local-ops-design`
Worktree: `C:\tmp\rag-dt011-docker-local-ops-design`
Starting main commit: `0484a83`
PR: https://github.com/RishiPrasath/waypoint-pilot/pull/34
Implementation commit: `708c853`
Merge commit: `c5525d8`

## Artifacts

- `docs/design/docker-local-ops.md`
- `build-sequence/02-design-tasks/05-runtime-technical-design/RAG-DT011-docker-local-ops-design.md`
- `build-sequence/02-design-tasks/00-index.md`
- `build-sequence/01-setup-tasks/RAG-BT004-stage-1-ci.md`
- `build-sequence/03-build-tasks/06-ops-readiness/RAG-BT020-docker-local-run.md`
- `build-sequence/03-build-tasks/06-ops-readiness/RAG-BT021-observability-ops-notes.md`
- `build-sequence/03-build-tasks/06-ops-readiness/RAG-BT022-production-readiness-review.md`

## Checks Run

Source checks:

- Docker Compose service `healthcheck` and service dependency documentation reviewed.
- Docker Compose startup-order documentation reviewed for `service_healthy`.
- FastAPI Docker deployment documentation reviewed.
- Qdrant Docker/Compose installation documentation reviewed.
- Qdrant security documentation reviewed.
- Trivy GitHub Action documentation reviewed.

Baseline local checks:

```powershell
Get-ChildItem "$WorktreePath\.github\workflows" -Filter "*.yml"
uv run python -m pytest -q
docker --version
docker compose version
docker info --format '{{.ServerVersion}}'
```

Result:

```text
workflow files observed:
- .github/workflows/ingestion.yml
- .github/workflows/partner-source-fastapi-ci.yml
- .github/workflows/partner-source-springboot-ci.yml

uv run python -m pytest -q -> 12 passed
docker --version -> Docker version 28.5.1, build e180ab8
docker compose version -> Docker Compose version v2.40.3-desktop.1
docker info -> 28.5.1
```

## Design Result

Accepted local ops design:

- Dockerfile and Compose implementation belongs to `RAG-BT020`.
- Default tests remain Docker-free.
- Local Qdrant integration uses Docker Compose `test` profile.
- Local app runtime smoke uses Docker Compose `app` profile.
- Qdrant readiness uses `/readyz`.
- App smoke uses `/health` and `/ready`.
- Seed/bootstrap remains owned by ingestion/retrieval/evaluation tasks.
- Production deployment, Kubernetes, managed Qdrant, and backups remain out of
  scope.
- CI/CD implementation and proof remain owned by `RAG-DT016`.

## Build Task Impact

- `RAG-BT004`: Stage 1 CI boundary remains Docker-free; Docker stages move to
  DT016/BT020.
- `RAG-BT020`: must implement Dockerfile, Compose profiles, local app smoke,
  Qdrant test profile, `.dockerignore`, and docs.
- `RAG-BT021`: must implement/log the local diagnostics and redaction rules.
- `RAG-BT022`: must require Docker/local evidence if Docker remains in scope.

Handoff blocks were added to:

- `build-sequence/01-setup-tasks/RAG-BT004-stage-1-ci.md`
- `build-sequence/03-build-tasks/06-ops-readiness/RAG-BT020-docker-local-run.md`
- `build-sequence/03-build-tasks/06-ops-readiness/RAG-BT021-observability-ops-notes.md`
- `build-sequence/03-build-tasks/06-ops-readiness/RAG-BT022-production-readiness-review.md`

## CI And Review

PR CI: No required checks reported before merge
Human review: Completed by merge of PR #34
AI review: Completed during task execution

## Issues And Recovery

- The repo currently contains workflow files whose names are not obviously a
  dedicated `rag-service` CI workflow. This is recorded for `RAG-DT016` to audit
  and fix if necessary.
- DT011 intentionally does not implement Dockerfile, Compose, CI workflow jobs,
  Trivy scan, or runtime code.

## Follow-ups

- DT011 is complete.
- Next planned task is `RAG-DT016`.
