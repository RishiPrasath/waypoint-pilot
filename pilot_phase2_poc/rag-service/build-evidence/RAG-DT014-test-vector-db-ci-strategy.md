# RAG-DT014 Evidence

Status: In Review - owner decision accepted

## Identity

Task: RAG-DT014 - Test Vector DB And CI Integration Strategy
Branch: `codex/rag-dt014-test-vector-db-ci-strategy`
Worktree: `C:\tmp\rag-dt014-test-vector-db-ci-strategy`
Starting main commit: `fb7ef0e`
PR: https://github.com/RishiPrasath/waypoint-pilot/pull/30
Implementation commit: Current branch HEAD in PR #30
Merge commit: Pending - PR #30 has not been merged yet

## Artifacts

- `docs/design/test-vector-db-ci-strategy.md`
- `docs/design/experiments/vector-db-ci-strategy/dt014-run-001/vector-db-ci-options-assessment.md`
- `docs/design/experiments/vector-db-ci-strategy/dt014-run-001/decision-gate.md`
- `build-sequence/02-design-tasks/05-runtime-technical-design/RAG-DT014-test-vector-db-ci-strategy.md`
- `build-sequence/02-design-tasks/00-index.md`
- `build-sequence/01-setup-tasks/RAG-BT010-qdrant-vector-db-client.md`
- `build-sequence/03-build-tasks/01-ingestion/RAG-BT012-fixture-ingestion-pipeline.md`
- `build-sequence/03-build-tasks/03-retrieval/RAG-BT013-semantic-retrieval-baseline.md`
- `build-sequence/03-build-tasks/03-retrieval/RAG-BT014-lexical-hybrid-retrieval.md`
- `build-sequence/03-build-tasks/05-evaluation/RAG-BT019-evaluation-harness.md`
- `build-sequence/03-build-tasks/06-ops-readiness/RAG-BT020-docker-local-run.md`

## Checks Run

Internet/source checks:

- GitHub Actions service container documentation reviewed.
- Qdrant Docker/local quickstart and installation documentation reviewed.
- Qdrant monitoring documentation reviewed for `/healthz`, `/livez`, and `/readyz`.

Local environment checks:

```powershell
docker --version
docker compose version
docker info --format '{{.ServerVersion}}'
Start-Process -FilePath "C:\Program Files\Docker\Docker\Docker Desktop.exe" -WindowStyle Hidden
docker run -d --name rag-dt014-qdrant-test -p 6333:6333 -p 6334:6334 qdrant/qdrant
Invoke-WebRequest http://localhost:6333/readyz
Invoke-WebRequest http://localhost:6333/healthz
Invoke-WebRequest http://localhost:6333/livez
docker logs rag-dt014-qdrant-test --tail 40
docker rm -f rag-dt014-qdrant-test
docker ps -a --filter "name=rag-dt014-qdrant-test"
```

Result:

```text
docker --version: Docker version 28.5.1, build e180ab8
docker compose version: Docker Compose version v2.40.3-desktop.1
initial docker info: Docker daemon not running
Docker Desktop launch: process started from command line
post-launch docker info: Docker daemon ready, server version 28.5.1
Qdrant image: qdrant/qdrant:latest pulled and started
Qdrant container: rag-dt014-qdrant-test
Qdrant container id: bd4e7cef170eabfd68dcd1dcec3812bdedc8d3c13087d218329901e04fa3718c
readyz: HTTP 200, all shards are ready
healthz: HTTP 200, healthz check passed
livez: HTTP 200, healthz check passed
Qdrant version from logs: 1.18.3
REST port: 6333
gRPC port: 6334
cleanup: docker rm -f succeeded; no rag-dt014-qdrant-test container remained
```

Acceptance checks:

```powershell
Test-Path "$ServiceRoot\docs\design\test-vector-db-ci-strategy.md"
Test-Path "$ServiceRoot\docs\design\experiments\vector-db-ci-strategy\dt014-run-001\vector-db-ci-options-assessment.md"
Test-Path "$ServiceRoot\docs\design\experiments\vector-db-ci-strategy\dt014-run-001\decision-gate.md"
Test-Path "$ServiceRoot\build-evidence\RAG-DT014-test-vector-db-ci-strategy.md"
Select-String -Path "$ServiceRoot\build-sequence\01-setup-tasks\RAG-BT010-qdrant-vector-db-client.md" -Pattern "DT014 Vector DB Test Handoff"
Select-String -Path "$ServiceRoot\build-sequence\03-build-tasks\01-ingestion\RAG-BT012-fixture-ingestion-pipeline.md" -Pattern "DT014 Vector DB Test Handoff"
Select-String -Path "$ServiceRoot\build-sequence\03-build-tasks\03-retrieval\RAG-BT013-semantic-retrieval-baseline.md" -Pattern "DT014 Vector DB Test Handoff"
Select-String -Path "$ServiceRoot\build-sequence\03-build-tasks\03-retrieval\RAG-BT014-lexical-hybrid-retrieval.md" -Pattern "DT014 Vector DB Test Handoff"
Select-String -Path "$ServiceRoot\build-sequence\03-build-tasks\05-evaluation\RAG-BT019-evaluation-harness.md" -Pattern "DT014 Vector DB Test Handoff"
Select-String -Path "$ServiceRoot\build-sequence\03-build-tasks\06-ops-readiness\RAG-BT020-docker-local-run.md" -Pattern "DT014 Vector DB Test Handoff"
```

Result: all four required artifact paths returned `True`, and all six
affected build tasks contain the `DT014 Vector DB Test Handoff` block.

Standard checks:

```powershell
uv run python -m pytest -q
git -C $WorktreePath diff --check
```

Result:

```text
git diff --check -> passed
uv run python -m pytest -q -> 12 passed
```

## CI And Review

PR CI: Pending - draft PR has no required checks reported yet
Human review: Accepted owner decision on 2026-07-17
AI review: Completed initial subagent review before adjustment; accepted findings were incorporated into this gate run.

## Issues And Recovery

- The owner accepted the decision gate on 2026-07-17.
- DT014 is not marked `Complete` until the PR is merged, main is refreshed, and
  the worktree is cleaned up.
- Downstream build-task handoff files were updated after owner gate acceptance.
- Docker Desktop was initially stopped. It was launched from the command line,
  the daemon became ready, and a disposable Qdrant container smoke test passed.
- Docker Compose itself was not implemented in this task. DT014 only proves the
  local Docker/Qdrant runtime path and recommends a later durable Compose test
  profile implementation.
- Recovery note: an accidental repo-root pytest invocation collected unrelated
  Phase 1 and partner-source tests and failed due out-of-scope dependencies and
  import paths. The correct service-root command was rerun:

  ```powershell
  Set-Location "C:\tmp\rag-dt014-test-vector-db-ci-strategy\pilot_phase2_poc\rag-service"
  uv run python -m pytest -q
  ```

  Result:

  ```text
  12 passed
  ```

## Follow-ups

- Merge PR #30 after final review.
- Pull `origin/main` after merge.
- Remove/prune the DT014 worktree.
- Mark post-merge closeout in evidence if a follow-up closeout commit is needed.
