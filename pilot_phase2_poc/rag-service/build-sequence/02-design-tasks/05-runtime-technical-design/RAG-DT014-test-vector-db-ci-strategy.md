# RAG-DT014: Test Vector DB And CI Integration Strategy

Status: Complete

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-DT014` |
| Task Name | Test Vector DB And CI Integration Strategy |
| Design Lane | 05-runtime-technical-design |
| Source Question | CI/CD vector DB integration and test environment |
| Decision / ADR | ADR-RAG-0002, ADR-RAG-0010, ADR-RAG-0011 |
| Related Planning Docs | `02-rag-db/planning/cicd-pipeline-proposal.md`, `02-rag-db/research/vector-database-selection.md` |
| Affected Build Tasks | RAG-BT010, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019, RAG-BT020 |
| Branch | `codex/rag-dt014-test-vector-db-ci-strategy` |
| Worktree Path | `C:\tmp\rag-dt014-test-vector-db-ci-strategy` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Complete |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT014-test-vector-db-ci-strategy.md` |

## 1. Task Definition

Design: define the test vector database environment and CI integration test
strategy.

Goal: make sure Qdrant/vector DB integration tests have a repeatable local and
CI test environment before ingestion and retrieval build tasks depend on it.

Output Artifact:

```text
docs/design/test-vector-db-ci-strategy.md
```

Experiment And Assessment Artifacts:

```text
docs/design/experiments/vector-db-ci-strategy/dt014-run-001/vector-db-ci-options-assessment.md
docs/design/experiments/vector-db-ci-strategy/dt014-run-001/decision-gate.md
```

Acceptance Criteria:

- chosen CI test vector DB approach is documented
- decision is made between GitHub Actions service container and Docker Compose
  test profile
- option assessment is conducted for GitHub Actions service container, Docker
  Compose test profile, and Qdrant local/in-memory mode
- decision gate is written with options, evidence, recommendation, risks, and
  owner decision status
- local developer command is documented
- CI command is documented
- exact Qdrant test modes are documented: unit/mock, local integration, and CI
  integration
- exact Qdrant environment variables are documented, including `QDRANT_URL`,
  `QDRANT_API_KEY`, `QDRANT_COLLECTION_PREFIX`,
  `QDRANT_TEST_TIMEOUT_SECONDS`, and `RUN_QDRANT_INTEGRATION`
- test collection naming and cleanup strategy are documented
- collection contract is documented, including collection name pattern, vector
  size, distance metric, embedding model/version compatibility,
  payload/schema version, source IDs, chunk IDs, content hashes, and snapshot
  fields
- DT010 vector contract is consumed: FastEmbed, `BAAI/bge-small-en`, 384
  dimensions, cosine distance, and benchmark run `dt010-run-001`
- Qdrant distance casing is clarified: design docs may say `cosine`, while
  Qdrant/client config may require `Cosine`
- seed/bootstrap step is documented
- seed/bootstrap lifecycle states whether embeddings are generated live through
  the adapter or loaded from committed static vectors
- unit tests vs integration tests are clearly separated
- pytest marker strategy is documented as `integration` and includes the
  required marker registration in `pyproject.toml`
- required environment variables are documented
- when vector DB tests become required in PR CI is documented
- health checks, failure handling, logs, and timeout expectations are
  documented with concrete values
- evidence file is created before PR and uses
  `build-sequence/00-governance/02-evidence-template.md`
- design lane index status is updated in the same PR
- affected build tasks include concrete DT014 handoff blocks

Out Of Scope:

- implementing the actual GitHub Actions workflow
- implementing the Docker Compose file
- implementing ingestion or retrieval code
- production deployment

Definition Of Gate:

A gate is the formal decision checkpoint where the available approaches are
assessed, evidence is shown, a recommendation is made, and the owner explicitly
accepts, rejects, or defers the approach before downstream build tasks depend on
it.

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt014"
$Slug = "test-vector-db-ci-strategy"
$Branch = "codex/$TaskId-$Slug"
$WorktreePath = Join-Path $WorktreeRoot "$TaskId-$Slug"

New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null
git -C $RepoRoot fetch origin
git -C $RepoRoot pull --ff-only origin main
git -C $RepoRoot config core.longpaths true
git -C $RepoRoot worktree add -b $Branch $WorktreePath origin/main
git -C $WorktreePath status --short --branch
```

### Linux / macOS Bash

```bash
REPO_ROOT="$HOME/code/waypoint-pilot"
WORKTREE_ROOT="$HOME/code/waypoint-pilot-worktrees"
TASK_ID="rag-dt014"
SLUG="test-vector-db-ci-strategy"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
git -C "$REPO_ROOT" config core.longpaths true
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```

## 3. Acceptance Check

```powershell
$ServiceRoot = "$WorktreePath\pilot_phase2_poc\rag-service"

Test-Path "$ServiceRoot\docs\design\test-vector-db-ci-strategy.md"
Test-Path "$ServiceRoot\docs\design\experiments\vector-db-ci-strategy\dt014-run-001\vector-db-ci-options-assessment.md"
Test-Path "$ServiceRoot\docs\design\experiments\vector-db-ci-strategy\dt014-run-001\decision-gate.md"
Test-Path "$ServiceRoot\build-evidence\RAG-DT014-test-vector-db-ci-strategy.md"

Select-String -Path "$ServiceRoot\docs\design\test-vector-db-ci-strategy.md" -Pattern "Qdrant|GitHub Actions service container|Docker Compose|pytest -m integration|QDRANT_URL|QDRANT_COLLECTION_PREFIX|BAAI/bge-small-en|384|cosine|Cosine|readyz|timeout|cleanup|seed|payload_schema_version"
Select-String -Path "$ServiceRoot\docs\design\experiments\vector-db-ci-strategy\dt014-run-001\vector-db-ci-options-assessment.md" -Pattern "GitHub Actions service container|Docker Compose|local/in-memory|pros|cons|risk|recommendation"
Select-String -Path "$ServiceRoot\docs\design\experiments\vector-db-ci-strategy\dt014-run-001\decision-gate.md" -Pattern "Decision Gate|Option A|Option B|Option C|Recommendation|Owner Decision"
Select-String -Path "$ServiceRoot\build-sequence\02-design-tasks\00-index.md" -Pattern "RAG-DT010.*Complete|RAG-DT014.*In Review|RAG-DT014.*Complete"

uv run python -m pytest -q
git -C $WorktreePath diff --check
```

## 4. Design Work

Create a design note that answers:

- should CI run Qdrant as a GitHub Actions service container or through Docker
  Compose
- what local command starts the test vector DB
- what CI command starts the test vector DB
- what collection name pattern is used for tests
- what vector size and distance metric are used for the chosen embedding model
- which payload fields are required for filtering, source lineage, source hash,
  chunk identity, and test cleanup
- how test collections are created, seeded, and deleted
- what fixture data is used for vector DB tests
- which tests remain pure unit tests with mocks
- which tests require Dockerized Qdrant and use `pytest -m integration`
- when integration tests become required in PR CI
- whether slower tests run on PR, schedule, manual trigger, or release
- how failures are diagnosed using logs and health checks

Recommended default unless the design task finds a better reason:

```text
Use GitHub Actions service container for CI Qdrant integration tests.
Use Docker Compose profile for local developer parity.
Keep unit tests mock-based and fast.
Run Qdrant integration tests only after RAG-BT010 and the first ingestion/retrieval fixtures exist.
```

Required design sections:

1. Decision summary.
2. Test modes:
   - unit/mock mode with no Qdrant service
   - local integration mode with Docker Compose Qdrant
   - CI integration mode with GitHub Actions Qdrant service container
3. Option assessment:
   - Option A: GitHub Actions Qdrant service container
   - Option B: Docker Compose Qdrant test profile
   - Option C: Qdrant local/in-memory mode
4. Qdrant runtime environment:
   - HTTP port `6333`
   - optional gRPC port `6334`
   - local default `QDRANT_URL=http://localhost:6333`
   - local/CI test default `QDRANT_API_KEY` unset
5. Environment variable contract:
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `QDRANT_COLLECTION_PREFIX`
   - `QDRANT_TEST_TIMEOUT_SECONDS`
   - `RUN_QDRANT_INTEGRATION`
6. Collection naming and cleanup contract:
   - collections must be unique per test run
   - recommended pattern: `rag_test_<task_id>_<run_id>`
   - cleanup before seed
   - cleanup after test
   - cleanup in teardown or `finally`
7. Vector contract from DT010:
   - provider: `fastembed`
   - model: `BAAI/bge-small-en`
   - dimension: `384`
   - distance: `cosine` in design prose and `Cosine` where required by Qdrant/client config
   - benchmark run: `dt010-run-001`
8. Payload schema contract. Required fields include:
   - `payload_schema_version`
   - `document_id`
   - `source_id` or equivalent approved source identifier
   - `source_uri`
   - `snapshot_id`
   - `candidate_sha256`
   - `chunk_id`
   - `chunk_strategy`
   - `heading_path`
   - `section_part_index`
   - `recursive_split_applied`
   - `retrieval_eligible`
   - `content_hash`
   - `embedding_provider`
   - `embedding_model`
   - `embedding_dimension`
   - `benchmark_run_id`
9. Seed/bootstrap lifecycle:
   - read DT005/DT012 chunks
   - generate embeddings through the BT011 adapter once available
   - create collection
   - upsert points
   - run retrieval assertions
   - delete collection
   - state whether live embeddings or static committed vectors are used
10. Pytest marker and command contract:

    ```toml
    [tool.pytest.ini_options]
    markers = [
      "integration: tests requiring external local services such as Qdrant",
    ]
    ```

    ```powershell
    uv run python -m pytest -q
    uv run python -m pytest -m integration -q
    uv run python -m pytest -m "not integration" -q
    ```

11. Skip behavior:
    - local integration tests may skip with a clear message if Qdrant is not
      available
    - CI integration tests must fail if the service container is expected but
      unavailable
12. CI gating phases:
    - before BT012/BT013: integration tests are manual, scheduled, or advisory
    - after BT012 and BT013: Qdrant ingestion/retrieval integration tests become
      required in PR CI
    - after BT020: Docker Compose/container smoke tests may join CI or release
      checks
13. Health checks and diagnostics:
    - readiness endpoint: `http://localhost:6333/readyz`
    - local readiness timeout recommendation: 30 seconds
    - CI readiness timeout recommendation: 60 seconds
    - diagnostics include `docker ps`, `docker logs`, readiness response,
      collection name, seed count, top-k result IDs, and pytest output
14. Security and secrets:
    - local/CI test Qdrant is unauthenticated only when isolated to the test
      runner/local host
    - never print `QDRANT_API_KEY` or any secret value
    - production Qdrant authentication/deployment remains out of scope
15. Downstream build-task handoffs.

Required experiment/assessment report:

```text
docs/design/experiments/vector-db-ci-strategy/dt014-run-001/vector-db-ci-options-assessment.md
```

The report must compare each option against:

- repeatability
- CI suitability
- local developer usability
- startup complexity
- health-check support
- cleanup safety
- ingestion/retrieval compatibility
- security/secrets risk
- deferred work

Required decision gate artifact:

```text
docs/design/experiments/vector-db-ci-strategy/dt014-run-001/decision-gate.md
```

The gate must include:

- Option A: GitHub Actions Qdrant service container
- Option B: Docker Compose Qdrant test profile
- Option C: Qdrant local/in-memory mode
- recommendation
- evidence summary
- risks and mitigations
- owner decision status: `Pending`, `Accepted`, `Rejected`, or `Deferred`
- downstream tasks blocked until the gate is accepted

Owner accepted the gate on 2026-07-17:

```text
Use GitHub Actions service container for CI integration tests.
Use Docker Compose profile for local developer parity.
Use Qdrant local/in-memory only for unit/design benchmarks, not service-backed
integration proof.
```

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT010, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019, RAG-BT020

Required Updates:

- Update vector DB client smoke-test expectations, ingestion integration tests,
  semantic retrieval integration tests, hybrid retrieval integration tests,
  evaluation test requirements, Docker/local run acceptance checks, CI marker
  usage, seed/bootstrap commands, and cleanup rules.
- Concrete DT014 handoff blocks were added to each affected build task:

  ```text
  DT014 Vector DB Test Handoff:

  - Qdrant test mode:
  - Local command:
  - CI command:
  - Pytest marker:
  - Required environment variables:
  - Collection naming rule:
  - Seed fixture:
  - Payload contract:
  - Cleanup rule:
  - CI gate timing:
  ```

- Minimum affected files to update:
  - `build-sequence/01-setup-tasks/RAG-BT010-qdrant-vector-db-client.md`
  - `build-sequence/03-build-tasks/01-ingestion/RAG-BT012-fixture-ingestion-pipeline.md`
  - `build-sequence/03-build-tasks/03-retrieval/RAG-BT013-semantic-retrieval-baseline.md`
  - `build-sequence/03-build-tasks/03-retrieval/RAG-BT014-lexical-hybrid-retrieval.md`
  - `build-sequence/03-build-tasks/05-evaluation/RAG-BT019-evaluation-harness.md`
  - `build-sequence/03-build-tasks/06-ops-readiness/RAG-BT020-docker-local-run.md`

Expected downstream meaning:

- `RAG-BT010`: optional live Qdrant smoke test is marked `integration`.
- `RAG-BT012`: fixture ingestion tests own collection seed/bootstrap and teardown.
- `RAG-BT013`: semantic retrieval integration tests assert expected source rank
  1 and expected chunk within top 3 for DT006 positive cases.
- `RAG-BT014`: hybrid retrieval preserves or improves the semantic baseline.
- `RAG-BT019`: evaluation reports Qdrant-backed retrieval separately from
  mocked/unit retrieval.
- `RAG-BT020`: Docker/local run implements the Compose shape chosen or deferred
  by DT014.

Deferred Impact:

- Production deployment remains out of scope.
- The exact production Qdrant deployment model remains deferred.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with RAG Architect, CI/CD Engineer, Test Engineer, and Security Reviewer.

Status and index requirements:

- Set this task file to `In Review` before opening the PR.
- Update `build-sequence/02-design-tasks/00-index.md` in the same PR.
- Confirm `RAG-DT010` is marked `Complete` in the design lane index.
- Set this task to `Complete` only when the strategy artifact, assessment
  report, decision gate, evidence file, build-task handoffs, checks, PR, merge,
  and cleanup are verified.

Evidence gate:

- Create `build-evidence/RAG-DT014-test-vector-db-ci-strategy.md` before opening
  the PR.
- Evidence must follow
  `build-sequence/00-governance/02-evidence-template.md`.
- Blank evidence fields are not allowed.
- Use `Pending - reason` before PR/merge where necessary.
- Use `N/A - reason` only when a field truly does not apply.
- The PR must include the evidence file.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt014 test-vector-db-ci-strategy"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt014 test-vector-db-ci-strategy"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to main.

Required PR checks:

- CI pipeline runs
- CI passes
- AI scans the design artifact and affected build-task updates
- human owner reviews the PR
- accepted findings are fixed

## 8. Merge

Merge only after CI passes and the PR is reviewed. Record PR URL, CI result,
merge commit, unresolved risks, and follow-up debt entries if any. Then clean up
the worktree.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$ServiceRoot = Join-Path $RepoRoot "pilot_phase2_poc\rag-service"

git -C $RepoRoot fetch origin
git -C $RepoRoot pull --ff-only origin main
git -C $RepoRoot status --short --branch
git -C $RepoRoot worktree remove $WorktreePath
git -C $RepoRoot worktree prune
git -C $RepoRoot worktree list

Test-Path "$ServiceRoot\docs\design\test-vector-db-ci-strategy.md"
Test-Path "$ServiceRoot\docs\design\experiments\vector-db-ci-strategy\dt014-run-001\decision-gate.md"
Test-Path "$ServiceRoot\build-evidence\RAG-DT014-test-vector-db-ci-strategy.md"
```

### Linux / macOS Bash

```bash
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
git -C "$REPO_ROOT" status --short --branch
git -C "$REPO_ROOT" worktree remove "$WORKTREE_PATH"
git -C "$REPO_ROOT" worktree prune
git -C "$REPO_ROOT" worktree list

test -f "$REPO_ROOT/pilot_phase2_poc/rag-service/docs/design/test-vector-db-ci-strategy.md"
test -f "$REPO_ROOT/pilot_phase2_poc/rag-service/docs/design/experiments/vector-db-ci-strategy/dt014-run-001/decision-gate.md"
test -f "$REPO_ROOT/pilot_phase2_poc/rag-service/build-evidence/RAG-DT014-test-vector-db-ci-strategy.md"
```

## Task Evidence

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-DT014-test-vector-db-ci-strategy.md`.
