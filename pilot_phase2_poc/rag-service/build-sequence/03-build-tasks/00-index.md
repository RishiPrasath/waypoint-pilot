# RAG Service Final Build Task Lane

Status: Blocked pending reopened design and delivery-control gates
Date: 2026-07-28

This folder contains the final implementation tasks for actual RAG behavior.

Start from `../00-index.md`, then use this lane index, then open the task
file. Task files should follow
`../00-governance/01-task-template.md`.

These tasks must run only after the relevant setup tasks and design-decision
tasks are complete or explicitly deferred.

## Build Task Template Rule

Every final build task must follow the accepted implementation task template:

1. task definition
2. worktree and branch setup
3. test code
4. implementation
5. test execution
6. branch workflow
7. merge
8. task evidence

The worktree must be created before test or implementation files are written.
Each task must follow TDD or an explicit acceptance-check-first flow.

## Design-Dependency Rule

Before starting any final build task, review the completed design tasks in:

```text
../02-design-tasks/
```

If a design decision changes the task requirements, update the final build task
file before writing tests or implementation code.

`RAG-DT013` is the final design-to-build impact review gate. It must confirm
that affected build task files are up to date before final build work begins.
`RAG-DT021` through `RAG-DT025` and reopened `RAG-DT015`, `RAG-DT018`,
`RAG-DT019`, and `RAG-DT020` must be completed before `RAG-DT013` Revision 2
can approve final build work. `RAG-DT025` must replace generic placeholders
with task-specific executable red checks and must validate the dependency DAG.

## Legacy KB Guardrail

The copied Phase 1 KB snapshot is audit input only:

```text
../../legacy/phase1-kb-snapshot/
```

Build tasks must not ingest the service-root `legacy/` folder directly. Only
audited and explicitly promoted material may become fixture, candidate, or
canonical Phase 2 KB content.

## Accepted Stage Order

Actual RAG behavior must be built in this order:

```text
01-ingestion
-> 02-query
-> 03-retrieval
-> 04-generation
-> 05-evaluation
```

Operational hardening tasks follow afterward in:

```text
06-ops-readiness
```

`RAG-BT018` is the post-generation API integration task. It lives under the
`02-query` folder because the query endpoint owns the external request/response
contract, but it intentionally runs after retrieval, generation, and output
validation are available.

## Runtime Package Naming Note

Build-sequence folders use readable stage names such as `01-ingestion`.
Runtime Python packages should use import-safe names such as:

```text
app/stages/stage_01_ingestion/
app/stages/stage_02_query/
app/stages/stage_03_retrieval/
app/stages/stage_04_generation/
app/stages/stage_05_evaluation/
```

This keeps the accepted stage numbering while avoiding Python import problems
from hyphenated folder names.

## Folder Layout

```text
03-build-tasks/
  00-index.md
  01-ingestion/
  02-query/
  03-retrieval/
  04-generation/
  05-evaluation/
  06-ops-readiness/
```

## Task List

| Order | ID | Task | File | Gates |
|---:|---|---|---|---|
| 33 | `RAG-BT007` | Add Source Registry Schema Validation | `01-ingestion/RAG-BT007-source-registry-validation.md` | RAG-DT004, RAG-DT008, RAG-DT021, RAG-DT025, RAG-DT013 |
| 34 | `RAG-BT008` | Add Phase 1 KB Audit Artifacts | `01-ingestion/RAG-BT008-phase1-kb-audit-artifacts.md` | RAG-DT002, RAG-DT003, RAG-DT004, RAG-DT012, RAG-DT025, RAG-DT013 |
| 35 | `RAG-BT009` | Add Chunking Rules And Fixture Harness | `01-ingestion/RAG-BT009-chunking-fixture-harness.md` | RAG-BT007, RAG-DT002, RAG-DT004, RAG-DT005, RAG-DT012, RAG-DT021, RAG-DT025, RAG-DT013 |
| 36 | `RAG-BT011` | Add Embedding Adapter | `01-ingestion/RAG-BT011-embedding-adapter.md` | RAG-DT010, RAG-DT025, RAG-DT013 |
| 37 | `RAG-BT023` | Add SDK-Backed Qdrant Adapter And Disposable Test Infrastructure | `01-ingestion/RAG-BT023-sdk-backed-qdrant-adapter-and-test-infrastructure.md` | RAG-BT005, RAG-BT010, RAG-BT011, RAG-DT014, RAG-DT021, RAG-DT023, RAG-DT025, RAG-DT013 |
| 38 | `RAG-BT012` | Add Fixture Ingestion Pipeline | `01-ingestion/RAG-BT012-fixture-ingestion-pipeline.md` | RAG-BT007, RAG-BT009, RAG-BT011, RAG-BT023, RAG-DT004, RAG-DT005, RAG-DT008, RAG-DT012, RAG-DT014, RAG-DT021, RAG-DT025, RAG-DT013 |
| 39 | `RAG-BT024` | Add Canonical Corpus Release Baseline | `01-ingestion/RAG-BT024-canonical-corpus-release-baseline.md` | RAG-BT007, RAG-BT008, RAG-DT021, RAG-DT024, RAG-DT025, RAG-DT013; required only for canonical/production claims |
| 40 | `RAG-BT015` | Add Query Safeguards And Deterministic Query Planning | `02-query/RAG-BT015-query-planning.md` | RAG-DT007, RAG-DT019, RAG-DT021, RAG-DT025, RAG-DT013 |
| 41 | `RAG-BT013` | Add Semantic Retrieval Baseline | `03-retrieval/RAG-BT013-semantic-retrieval-baseline.md` | RAG-BT012, RAG-BT023, RAG-DT005, RAG-DT012, RAG-DT014, RAG-DT018, RAG-DT022, RAG-DT025, RAG-DT013 |
| 42 | `RAG-BT014` | Add Lexical And Hybrid Retrieval | `03-retrieval/RAG-BT014-lexical-hybrid-retrieval.md` | RAG-BT013, RAG-BT023, RAG-DT005, RAG-DT014, RAG-DT018, RAG-DT022, RAG-DT025, RAG-DT013 |
| 43 | `RAG-BT016` | Add Groq/OpenAI-Compatible Generation Adapter | `04-generation/RAG-BT016-generation-adapter.md` | RAG-DT009, RAG-DT015, RAG-DT019, RAG-DT021, RAG-DT022, RAG-DT023, RAG-DT025, RAG-DT013; credential rotation verified |
| 44 | `RAG-BT017` | Add Output Validation And Retry/Fallback | `04-generation/RAG-BT017-output-validation-retry-fallback.md` | RAG-BT006, RAG-BT015, RAG-BT016, RAG-DT015, RAG-DT019, RAG-DT021, RAG-DT022, RAG-DT023, RAG-DT025, RAG-DT013 |
| 45 | `RAG-BT018` | Add Query API Endpoint | `02-query/RAG-BT018-query-api-endpoint.md` | RAG-BT015, RAG-BT013, RAG-BT014, RAG-BT016, RAG-BT017, RAG-DT015, RAG-DT018, RAG-DT019, RAG-DT021, RAG-DT022, RAG-DT023, RAG-DT025, RAG-DT013 |
| 46 | `RAG-BT019` | Add Evaluation Harness | `05-evaluation/RAG-BT019-evaluation-harness.md` | RAG-BT018, RAG-BT023, RAG-DT004, RAG-DT005, RAG-DT006, RAG-DT009, RAG-DT012, RAG-DT014, RAG-DT015, RAG-DT018, RAG-DT019, RAG-DT020, RAG-DT021, RAG-DT022, RAG-DT023, RAG-DT024, RAG-DT025, RAG-DT013 |
| 47 | `RAG-BT020` | Add Docker Local Run | `06-ops-readiness/RAG-BT020-docker-local-run.md` | RAG-BT023, RAG-DT004, RAG-DT011, RAG-DT014, RAG-DT021, RAG-DT023, RAG-DT025, RAG-DT013 |
| 48 | `RAG-BT021` | Add Observability And Ops Notes | `06-ops-readiness/RAG-BT021-observability-ops-notes.md` | RAG-BT018, RAG-DT019, RAG-DT021, RAG-DT023, RAG-DT025, RAG-DT013 |
| 49 | `RAG-BT022` | PoC Integration Readiness Review | `06-ops-readiness/RAG-BT022-production-readiness-review.md` | required PoC build tasks, RAG-BT023, RAG-DT020 through RAG-DT025, RAG-DT013; RAG-BT024 for canonical claims |

## Main Sequence

The overall execution sequence is:

```text
../00-index.md
```

Do not treat this folder as a flat backlog. Use the lane order in the main
execution hub: setup tasks, then design tasks, then final build tasks.
