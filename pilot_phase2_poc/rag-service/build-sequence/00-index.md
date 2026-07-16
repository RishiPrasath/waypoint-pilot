# RAG Service Execution Sequence

Status: Accepted sequence with governed executable task files
Date: 2026-07-09

This folder is the main execution hub for `rag-service`.

Any agent starting work in this sequence should begin here, read this file
first, and then follow the relevant lane index before opening an individual
task file.

Task files should follow the canonical template in
`build-sequence/00-governance/01-task-template.md`.

It is split into three task lanes:

```text
build-sequence/
  00-governance/
  01-setup-tasks/
  02-design-tasks/
  03-build-tasks/
```

## Execution Order

The correct project order is:

```text
setup tasks
-> remaining design decisions
-> final build tasks
```

Do not treat the project as a flat build list. Some tasks are safe setup work,
but real RAG behavior depends on design decisions that are still outstanding.

## Important Rule

Design decisions may change final build tasks.

If a design task changes the expected KB layout, metadata model, source
registry, chunking strategy, query rules, embedding benchmark, LLM evaluation
fixture, or local ops scope, the affected final build task file must be updated
before implementation starts.

## Workflow Rule

Do not work directly on `main`.

Before creating any task worktree, refresh the repository from `origin/main`
and confirm the base commit is current. If a task branch or worktree was
created from an older snapshot, rebase or recreate it from the refreshed
`origin/main` before making changes.

Every task must use:

```text
updated main
-> short-lived branch
-> dedicated worktree
-> failing test or acceptance check
-> implementation or design artifact
-> local checks
-> commit
-> PR
-> PR CI/CD
-> merge
-> main CI/CD
-> worktree cleanup
-> local branch cleanup
-> remote branch cleanup when permitted
```

## CI Build And Test Strategy

CI must be added in layers.

Stage 1 CI is created during setup. It builds the Python application
environment, installs dependencies with `uv`, runs unit tests, runs linting,
and runs basic security checks. It must not require Dockerized services.

The accepted Stage 1 security baseline also includes CodeQL, Dependabot, and
GitHub secret-scanning evidence for the public repository.

Dockerized dependency tests are added later when the relevant code exists.
Qdrant integration tests should run with either a GitHub Actions service
container or a Docker Compose test profile. The selected approach is confirmed
in `RAG-DT014`; the Docker/local ops task consumes that decision for the
broader local runtime plan.

The intended CI maturity path is:

```text
Python environment build
-> unit tests and static checks
-> Dockerized Qdrant integration tests
-> Docker image build
-> container smoke tests
-> container/security scans
```

## Lane 1: Setup Tasks

Folder:

```text
01-setup-tasks/
```

Goal: set up the codebase, basic FastAPI service, CI/CD, quality gates,
configuration, shared contracts, and vector DB connection foundation.

This lane should not implement real RAG behavior.

| Order | Task | File | Gate |
|---:|---|---|---|
| 0 | Prove branch/worktree/PR workflow | `01-setup-tasks/RAG-BT000-prove-workflow.md` | Must be done before any other task. |
| 1 | Create FastAPI project skeleton | `01-setup-tasks/RAG-BT001-fastapi-skeleton.md` | Requires accepted codebase structure. |
| 2 | Add health endpoint | `01-setup-tasks/RAG-BT002-health-endpoint.md` | Requires skeleton. |
| 3 | Add readiness endpoint | `01-setup-tasks/RAG-BT003-readiness-endpoint.md` | Requires skeleton/config basics. |
| 4 | Add Stage 1 CI, CodeQL, and Dependabot | `01-setup-tasks/RAG-BT004-stage-1-ci.md` | PR and `main` CI must run. |
| 5 | Add config/settings module | `01-setup-tasks/RAG-BT005-config-settings.md` | Requires runtime config/secrets rules. |
| 6 | Add shared schemas and error envelope | `01-setup-tasks/RAG-BT006-shared-schemas.md` | Requires initial API/error contract. |
| 7 | Add Qdrant vector DB client wrapper | `01-setup-tasks/RAG-BT010-qdrant-vector-db-client.md` | Requires accepted Qdrant direction and config. |

## Lane 2: Remaining Design Decisions

Folder:

```text
02-design-tasks/
```

Goal: close the outstanding design decisions that block real RAG
implementation.

Design tasks produce decisions, plans, schemas, registries, fixtures, research
evidence, and acceptance criteria. They do not produce runtime service
behavior.

Run these before final ingestion, query planning, retrieval, generation, API
integration, or evaluation build work.

| Order | Task | File | Blocks |
|---:|---|---|---|
| 8 | Reconcile architecture checklist with accepted ADRs | `02-design-tasks/01-decision-reconciliation/RAG-DT001-architecture-checklist-reconciliation.md` | All later traceability. |
| 9 | Create Phase 1 KB source audit table | `02-design-tasks/02-source-scope-and-registry/RAG-DT002-phase1-kb-source-audit.md` | KB promotion, chunking, ingestion. |
| 10 | Define source registry schema and validation rules | `02-design-tasks/02-source-scope-and-registry/RAG-DT008-source-registry-schema.md` | Registry validation, ingestion. |
| 11 | Create APAC source candidate registry | `02-design-tasks/02-source-scope-and-registry/RAG-DT003-apac-source-candidate-registry.md` | Canonical KB build. |
| 12 | Confirm KB folder layout and registry storage | `02-design-tasks/03-kb-materialization/RAG-DT004-kb-folder-layout.md` | Source registry, ingestion. |
| 13 | Define source snapshot and canonical markdown candidate plan | `02-design-tasks/03-kb-materialization/RAG-DT012-source-snapshot-and-canonical-markdown-candidates.md` | Canonical markdown candidates, chunking. |
| 14 | Run chunking experiment during KB curation | `02-design-tasks/04-chunking-and-evaluation-design/RAG-DT005-chunking-experiment.md` | Chunking harness, ingestion, retrieval. |
| 15 | Define golden questions and answer rubrics | `02-design-tasks/04-chunking-and-evaluation-design/RAG-DT006-golden-questions.md` | Evaluation harness. |
| 16 | Define query planner vocabulary and rules | `02-design-tasks/05-runtime-technical-design/RAG-DT007-query-planner-artifacts.md` | Query planning. |
| 17 | Define LLM model evaluation fixture | `02-design-tasks/05-runtime-technical-design/RAG-DT009-llm-model-evaluation-fixture.md` | Generation adapter/model choice. |
| 18 | Define embedding benchmark fixture | `02-design-tasks/05-runtime-technical-design/RAG-DT010-embedding-benchmark-fixture.md` | Embedding adapter and retrieval quality. |
| 19 | Define test vector DB and CI integration strategy | `02-design-tasks/05-runtime-technical-design/RAG-DT014-test-vector-db-ci-strategy.md` | Qdrant integration tests, seed/cleanup, CI test DB setup. |
| 20 | Define Docker/local ops design when ready | `02-design-tasks/05-runtime-technical-design/RAG-DT011-docker-local-ops-design.md` | Docker local run and ops readiness. |
| 21 | Review final build task impact | `02-design-tasks/06-build-impact-review/RAG-DT013-final-build-task-impact-review.md` | All final build tasks. |

## Lane 3: Final Build Tasks

Folder:

```text
03-build-tasks/
```

Goal: implement real RAG behavior after the relevant design gates are closed.

The accepted stage order is:

```text
01-ingestion
-> 02-query
-> 03-retrieval
-> 04-generation
-> 05-evaluation
```

Each final build task must be reviewed against the completed design tasks
before implementation starts.

| Order | Task | File | Gate |
|---:|---|---|---|
| 22 | Add source registry schema validation | `03-build-tasks/01-ingestion/RAG-BT007-source-registry-validation.md` | Requires `RAG-DT004`, `RAG-DT008`, `RAG-DT013`. |
| 23 | Add Phase 1 KB audit artifacts | `03-build-tasks/01-ingestion/RAG-BT008-phase1-kb-audit-artifacts.md` | Requires `RAG-DT002`, `RAG-DT003`, `RAG-DT013`. |
| 24 | Add chunking rules and fixture harness | `03-build-tasks/01-ingestion/RAG-BT009-chunking-fixture-harness.md` | Requires `RAG-DT002`, `RAG-DT005`, `RAG-DT012`, `RAG-DT013`. |
| 25 | Add embedding adapter | `03-build-tasks/01-ingestion/RAG-BT011-embedding-adapter.md` | Requires `RAG-DT010`, `RAG-DT013`. |
| 26 | Add fixture ingestion pipeline | `03-build-tasks/01-ingestion/RAG-BT012-fixture-ingestion-pipeline.md` | Requires KB, chunking, Qdrant, embedding gates, `RAG-DT012`, `RAG-DT014`, `RAG-DT013`. |
| 27 | Add query safeguards and deterministic query planning | `03-build-tasks/02-query/RAG-BT015-query-planning.md` | Requires `RAG-DT007`, `RAG-DT013`. |
| 28 | Add semantic retrieval baseline | `03-build-tasks/03-retrieval/RAG-BT013-semantic-retrieval-baseline.md` | Requires ingestion fixture data, `RAG-DT014`, and `RAG-DT013`. |
| 29 | Add lexical/hybrid retrieval | `03-build-tasks/03-retrieval/RAG-BT014-lexical-hybrid-retrieval.md` | Requires semantic baseline, `RAG-DT014`, and `RAG-DT013`. |
| 30 | Add Groq/OpenAI-compatible generation adapter | `03-build-tasks/04-generation/RAG-BT016-generation-adapter.md` | Requires `RAG-DT009`, `RAG-DT013`. |
| 31 | Add output validation and retry/fallback | `03-build-tasks/04-generation/RAG-BT017-output-validation-retry-fallback.md` | Requires shared schemas, safeguards, `RAG-DT013`. |
| 32 | Add query API endpoint | `03-build-tasks/02-query/RAG-BT018-query-api-endpoint.md` | Requires query, retrieval, generation, validation, `RAG-DT013`. |
| 33 | Add evaluation harness | `03-build-tasks/05-evaluation/RAG-BT019-evaluation-harness.md` | Requires `RAG-DT006`, test DB strategy, query API, `RAG-DT014`, `RAG-DT013`. |
| 34 | Add Docker local run | `03-build-tasks/06-ops-readiness/RAG-BT020-docker-local-run.md` | Requires `RAG-DT011`, `RAG-DT014`, `RAG-DT013`, or explicit defer/approval. |
| 35 | Add observability and ops notes | `03-build-tasks/06-ops-readiness/RAG-BT021-observability-ops-notes.md` | Requires query flow, logging decisions, `RAG-DT013`. |
| 36 | Production-readiness review | `03-build-tasks/06-ops-readiness/RAG-BT022-production-readiness-review.md` | Requires all required tasks done or deferred. |

## Standard Paths

```text
Repo root:
C:\Users\prasa\Documents\Github\waypoint-pilot

Service root:
C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\rag-service

Execution hub:
C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\rag-service\build-sequence

Worktree root:
C:\tmp
```

## Standard Branch Setup

Every task file should customize only `$TaskId` and `$Slug`.

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt000"
$Slug = "short-name"
$Branch = "codex/$TaskId-$Slug"
$WorktreePath = Join-Path $WorktreeRoot "$TaskId-$Slug"

New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null
git -C $RepoRoot fetch origin
git -C $RepoRoot pull --ff-only origin main
git -C $RepoRoot config core.longpaths true
git -C $RepoRoot worktree add -b $Branch $WorktreePath origin/main
git -C $WorktreePath status --short --branch
```

## Agent Start Path

Recommended entry order for any task:

```text
build-sequence/00-index.md
-> lane index
-> task file
```

