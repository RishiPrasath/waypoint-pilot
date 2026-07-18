# RAG Service Design Task Lane

Status: Governed executable task files under accepted sequence
Date: 2026-07-09

This folder contains the remaining design-decision tasks that must be completed
before blocked RAG build work begins.

Start from `../00-index.md`, then use this lane index, then open the task
file. Task files should follow
`../00-governance/01-task-template.md`.

Design tasks produce decisions, plans, schemas, registries, fixtures, research
evidence, and acceptance criteria. They do not produce runtime service
behavior.

Legacy Phase 1 KB material is available only as audit input at:

```text
../../legacy/phase1-kb-snapshot/
```

Do not treat the service-root `legacy/` folder as approved Phase 2 KB content.
Any useful material must be audited and explicitly promoted through the KB
design tasks before build tasks or runtime ingestion can depend on it.

Design tasks may create `docs/design/`, `docs/evaluation/`, and
`knowledge_base/` artifacts as part of their accepted output. Those folders are
not assumed to exist before the relevant task runs.

## Folder Layout

```text
02-design-tasks/
  00-index.md
  01-decision-reconciliation/
  02-source-scope-and-registry/
  03-kb-materialization/
  04-chunking-and-evaluation-design/
  05-runtime-technical-design/
  06-build-impact-review/
```

## Execution Principle

Design decisions may change final build tasks. When a design task changes the
expected KB layout, metadata model, source registry, source materialization
rules, chunking strategy, query rules, embedding benchmark, LLM evaluation
fixture, LLM model evaluation result, local ops scope, or CI/CD readiness gate,
update the affected file under:

```text
../03-build-tasks/
```

## Build Impact Rule

Every design task must include a `Build Task Impact` section before it can be
considered complete.

That section must answer:

- which build tasks are affected
- what updates those build tasks require
- what impact remains deferred
- whether `RAG-DT013` has reviewed the impact

No final build task should begin until its required design tasks are complete
and `RAG-DT013` confirms the build task file is up to date.

## Recommended Design Flow

```text
decision reconciliation
-> source scope and registry
-> KB materialization
-> chunking and evaluation design
-> runtime technical design
-> CI/CD and REST service readiness gate
-> overall architecture sufficiency review
-> required follow-up design contracts
-> final build impact review
```

## Design Task List

| Order | ID | Task | File | Status |
|---:|---|---|---|---|
| 8 | `RAG-DT001` | Reconcile architecture checklist with accepted ADRs | `01-decision-reconciliation/RAG-DT001-architecture-checklist-reconciliation.md` | Complete |
| 9 | `RAG-DT002` | Create Phase 1 KB source audit table | `02-source-scope-and-registry/RAG-DT002-phase1-kb-source-audit.md` | Complete |
| 10 | `RAG-DT008` | Define source registry schema and validation rules | `02-source-scope-and-registry/RAG-DT008-source-registry-schema.md` | Complete |
| 11 | `RAG-DT003` | Create APAC source candidate registry | `02-source-scope-and-registry/RAG-DT003-apac-source-candidate-registry.md` | Complete |
| 12 | `RAG-DT004` | Confirm KB folder layout and source registry storage location | `03-kb-materialization/RAG-DT004-kb-folder-layout.md` | Complete |
| 13 | `RAG-DT012` | Define source snapshot and canonical markdown candidate plan | `03-kb-materialization/RAG-DT012-source-snapshot-and-canonical-markdown-candidates.md` | Complete |
| 14 | `RAG-DT005` | Run chunking experiment during KB curation | `04-chunking-and-evaluation-design/RAG-DT005-chunking-experiment.md` | Complete |
| 15 | `RAG-DT006` | Define golden questions and answer rubrics | `04-chunking-and-evaluation-design/RAG-DT006-golden-questions.md` | Complete |
| 16 | `RAG-DT007` | Define query planner vocabulary and rules artifacts | `05-runtime-technical-design/RAG-DT007-query-planner-artifacts.md` | Complete |
| 17 | `RAG-DT009` | Define LLM model evaluation fixture | `05-runtime-technical-design/RAG-DT009-llm-model-evaluation-fixture.md` | Complete |
| 18 | `RAG-DT015` | Run LLM model evaluation and selection | `05-runtime-technical-design/RAG-DT015-llm-model-evaluation-run.md` | Complete |
| 19 | `RAG-DT010` | Define embedding benchmark fixture | `05-runtime-technical-design/RAG-DT010-embedding-benchmark-fixture.md` | Complete |
| 20 | `RAG-DT014` | Define test vector DB and CI integration strategy | `05-runtime-technical-design/RAG-DT014-test-vector-db-ci-strategy.md` | Complete |
| 21 | `RAG-DT011` | Define Docker/local ops design when ready | `05-runtime-technical-design/RAG-DT011-docker-local-ops-design.md` | Complete |
| 22 | `RAG-DT016` | Audit and implement CI/CD REST service readiness gate | `05-runtime-technical-design/RAG-DT016-cicd-rest-service-readiness-gate.md` | Complete |
| 23 | `RAG-DT017` | Overall architecture and design sufficiency review | `05-runtime-technical-design/RAG-DT017-architecture-sufficiency-review.md` | Planned |
| 24 | `RAG-DT018` | Retrieval strategy selection, scoring, and fusion contract | `05-runtime-technical-design/RAG-DT018-retrieval-strategy-selection-and-fusion-contract.md` | Planned |
| 25 | `RAG-DT019` | Generation prompt, safeguards, output schema, and query API contract | `05-runtime-technical-design/RAG-DT019-generation-prompt-safeguards-output-schema-and-query-api-contract.md` | Planned |
| 26 | `RAG-DT020` | Post-build evaluation and tuning loop | `05-runtime-technical-design/RAG-DT020-post-build-evaluation-and-tuning-loop.md` | Planned |
| 27 | `RAG-DT013` | Final build task impact review | `06-build-impact-review/RAG-DT013-final-build-task-impact-review.md` | Planned |

## How Design Tasks Fit The Build Sequence

The main execution sequence is:

```text
../00-index.md
```

Design tasks happen after foundation setup and CI/CD, but before actual RAG
implementation tasks such as ingestion, retrieval, generation, API integration,
or evaluation. `RAG-DT016` is the exception-shaped readiness gate: it may
implement CI/CD workflow gaps because its purpose is to prove the project
runway before architecture and final build-task review. `RAG-DT017` then
performs a multi-perspective architecture sufficiency review. `RAG-DT018`,
`RAG-DT019`, and `RAG-DT020` close the required follow-up contracts for
retrieval strategy, generation/API safeguards, and post-build evaluation tuning
before `RAG-DT013` approves final build tasks.

## Standard Design Task Sections

Each design task must contain:

1. task definition
2. worktree and branch setup
3. acceptance check
4. design work
5. build task impact
6. verification
7. branch workflow
8. merge
9. task evidence
