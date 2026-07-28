# RAG Service Execution Sequence

Status: External review gates open; final build lane blocked
Date: 2026-07-28

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
completed setup foundation
-> new security/corpus/evaluation/reliability design gates
-> reopened model/retrieval/generation/evaluation decisions
-> executable-task and source-of-truth reconciliation
-> RAG-DT013 Revision 2 GO or NO-GO
-> conditional final build tasks
```

Do not treat the project as a flat build list. The 2026-07-28 independent
review found blocking design, dependency, and evidence-validity gaps. No final
build task is currently authorized by the earlier `RAG-DT013` completion.

## Important Rule

Design decisions may change final build tasks.

If a design task changes the expected KB layout, metadata model, source
registry, chunking strategy, query rules, embedding benchmark, LLM evaluation
fixture, LLM model evaluation result, or local ops scope, the affected final
build task file must be updated before implementation starts.

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

Before final build-task impact review, `RAG-DT016` must audit the whole CI/CD
and REST-service readiness environment, implement any missing CI/CD gates that
are required before real RAG implementation begins, and prove those gates work.
After that, `RAG-DT017` must perform an overall architecture sufficiency review
across design specs, completed design decisions, setup code, CI/CD posture, and
planned build tasks. `RAG-DT018`, `RAG-DT019`, and `RAG-DT020` must then close
the required follow-up contracts for retrieval strategy, generation/API
safeguards, and post-build evaluation tuning before `RAG-DT013` is allowed to
approve the final build task set.

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
| 17 | Define LLM model evaluation fixture | `02-design-tasks/05-runtime-technical-design/RAG-DT009-llm-model-evaluation-fixture.md` | LLM evaluation run. |
| 18 | Run LLM model evaluation and selection | `02-design-tasks/05-runtime-technical-design/RAG-DT015-llm-model-evaluation-run.md` | Generation adapter/model choice. |
| 19 | Define embedding benchmark fixture | `02-design-tasks/05-runtime-technical-design/RAG-DT010-embedding-benchmark-fixture.md` | Embedding adapter and retrieval quality. |
| 20 | Define test vector DB and CI integration strategy | `02-design-tasks/05-runtime-technical-design/RAG-DT014-test-vector-db-ci-strategy.md` | Qdrant integration tests, seed/cleanup, CI test DB setup. |
| 21 | Define Docker/local ops design when ready | `02-design-tasks/05-runtime-technical-design/RAG-DT011-docker-local-ops-design.md` | Docker local run and ops readiness. |
| 22 | Audit and implement CI/CD REST service readiness gate | `02-design-tasks/05-runtime-technical-design/RAG-DT016-cicd-rest-service-readiness-gate.md` | CI/CD gaps, REST service checks, GitHub Actions proof before final impact review. |
| 23 | Review overall architecture and design sufficiency | `02-design-tasks/05-runtime-technical-design/RAG-DT017-architecture-sufficiency-review.md` | Multi-expert architecture review and follow-up design task recommendations before final impact review. |
| 24 | Define retrieval strategy selection, scoring, and fusion contract | `02-design-tasks/05-runtime-technical-design/RAG-DT018-retrieval-strategy-selection-and-fusion-contract.md` | Retrieval mode routing, scoring, fusion, rerank hook, retrieval evaluation assumptions. |
| 25 | Define generation prompt, safeguards, output schema, and query API contract | `02-design-tasks/05-runtime-technical-design/RAG-DT019-generation-prompt-safeguards-output-schema-and-query-api-contract.md` | Generation adapter, output validation, query API, safeguards, frontend/BFF contract. |
| 26 | Define post-build evaluation and tuning loop | `02-design-tasks/05-runtime-technical-design/RAG-DT020-post-build-evaluation-and-tuning-loop.md` | Evaluation harness, tuning decisions, baseline promotion, production-readiness review. |
| 27 | Define security, trust, and abuse-resistance contract | `02-design-tasks/05-runtime-technical-design/RAG-DT021-security-trust-and-abuse-resistance-contract.md` | Ingestion, planning, generation, API, evaluation, readiness. |
| 28 | Define corpus promotion, freshness, revocation, and rollback | `02-design-tasks/02-source-scope-and-registry/RAG-DT024-corpus-promotion-freshness-revocation-and-rollback-contract.md` | Non-fixture corpus, evaluation, readiness. |
| 29 | Define evaluation validity and adversarial tests | `02-design-tasks/05-runtime-technical-design/RAG-DT022-evaluation-validity-and-adversarial-test-contract.md` | Reopened model/retrieval/generation/evaluation decisions. |
| 30 | Define runtime reliability, SLO, capacity, and deployment | `02-design-tasks/05-runtime-technical-design/RAG-DT023-runtime-reliability-slo-capacity-and-deployment-contract.md` | Provider, API, Docker, operations, readiness. |
| 31 | Reconcile build-task executability and sources of truth | `02-design-tasks/06-build-impact-review/RAG-DT025-build-task-executability-and-source-of-truth-reconciliation.md` | Every final build task. |
| 32 | Re-run final build task impact review, Revision 2 | `02-design-tasks/06-build-impact-review/RAG-DT013-final-build-task-impact-review.md` | All final build tasks. |

`RAG-DT015`, `RAG-DT018`, `RAG-DT019`, and `RAG-DT020` are reopened. Their
historical evidence remains available, but their current status is `Blocked`
until the new contracts are complete.

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
| 33 | Add source registry schema validation | `03-build-tasks/01-ingestion/RAG-BT007-source-registry-validation.md` | Requires new/reopened design gates and `RAG-DT013` Revision 2. |
| 34 | Add Phase 1 KB audit artifacts | `03-build-tasks/01-ingestion/RAG-BT008-phase1-kb-audit-artifacts.md` | Requires new/reopened design gates and `RAG-DT013` Revision 2. |
| 35 | Add chunking rules and fixture harness | `03-build-tasks/01-ingestion/RAG-BT009-chunking-fixture-harness.md` | Adds explicit `RAG-BT007` dependency. |
| 36 | Add embedding adapter | `03-build-tasks/01-ingestion/RAG-BT011-embedding-adapter.md` | Requires `RAG-DT010`, `RAG-DT025`, and `RAG-DT013` Revision 2. |
| 37 | Add SDK-backed Qdrant adapter and disposable test infrastructure | `03-build-tasks/01-ingestion/RAG-BT023-sdk-backed-qdrant-adapter-and-test-infrastructure.md` | Required before real ingestion/retrieval integration. |
| 38 | Add fixture ingestion pipeline | `03-build-tasks/01-ingestion/RAG-BT012-fixture-ingestion-pipeline.md` | Adds explicit `RAG-BT007`, `RAG-BT009`, and `RAG-BT023` dependencies. |
| 39 | Add canonical corpus release baseline | `03-build-tasks/01-ingestion/RAG-BT024-canonical-corpus-release-baseline.md` | Required for canonical or production claims; not fixture-only plumbing. |
| 40 | Add query safeguards and deterministic query planning | `03-build-tasks/02-query/RAG-BT015-query-planning.md` | Requires revised security and API contracts. |
| 41 | Add semantic retrieval baseline | `03-build-tasks/03-retrieval/RAG-BT013-semantic-retrieval-baseline.md` | Requires real Qdrant and valid evaluation gates. |
| 42 | Add lexical/hybrid retrieval | `03-build-tasks/03-retrieval/RAG-BT014-lexical-hybrid-retrieval.md` | Requires calibrated fusion and confidence. |
| 43 | Add Groq/OpenAI-compatible generation adapter | `03-build-tasks/04-generation/RAG-BT016-generation-adapter.md` | Requires supported model/fallback selection and credential-rotation proof. |
| 44 | Add output validation and retry/fallback | `03-build-tasks/04-generation/RAG-BT017-output-validation-retry-fallback.md` | Requires revised security, evaluation, reliability, and API contracts. |
| 45 | Add query API endpoint | `03-build-tasks/02-query/RAG-BT018-query-api-endpoint.md` | Requires reconciled API/error, trust, resource-limit, and readiness behavior. |
| 46 | Add evaluation harness | `03-build-tasks/05-evaluation/RAG-BT019-evaluation-harness.md` | Requires independent/held-out/adversarial evaluation and real Qdrant. |
| 47 | Add Docker local run | `03-build-tasks/06-ops-readiness/RAG-BT020-docker-local-run.md` | Requires loopback-bound Qdrant, pinned images, and real integration evidence. |
| 48 | Add observability and ops notes | `03-build-tasks/06-ops-readiness/RAG-BT021-observability-ops-notes.md` | Requires reliability/SLO and security/logging contracts. |
| 49 | PoC integration-readiness review | `03-build-tasks/06-ops-readiness/RAG-BT022-production-readiness-review.md` | Cannot issue a production-ready verdict; canonical claims also require `RAG-BT024`. |

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

