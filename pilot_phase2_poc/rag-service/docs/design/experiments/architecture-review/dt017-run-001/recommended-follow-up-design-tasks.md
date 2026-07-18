# DT017 Recommended Follow-Up Design Tasks

Status: Accepted for RAG-DT017
Run: `dt017-run-001`
Date: 2026-07-18

DT017 requires three follow-up design tasks before `RAG-DT013`, unless the
owner explicitly waives them and accepts the related risk.

The task files already exist in the current build sequence after PR #44 and PR
#45. DT017 therefore treats the follow-up tasks as created but not completed.
`RAG-DT013` remains blocked until these tasks are completed or explicitly
waived.

## RAG-DT018: Retrieval Strategy Selection, Scoring, And Fusion Contract

Task file:

```text
build-sequence/02-design-tasks/05-runtime-technical-design/RAG-DT018-retrieval-strategy-selection-and-fusion-contract.md
```

Purpose:

Define how the RAG service selects retrieval behavior by query scenario and how
semantic, lexical, metadata-filtered, exact-match, metadata-only, no-retrieval,
and hybrid modes should work.

Why it is needed before `RAG-DT013`:

`RAG-BT013` and `RAG-BT014` currently describe semantic and hybrid retrieval
implementation, but final build review needs an accepted contract for retrieval
mode routing and scoring. Without it, retrieval, query API, and evaluation
tasks may implement incompatible ranking and confidence assumptions.

Minimum decisions:

- retrieval-mode decision matrix by scenario;
- query-planner output to retrieval-mode mapping;
- lexical method and tokenization/normalization rules;
- metadata hard filters versus metadata boosts;
- semantic, lexical, and fused candidate-pool sizes;
- score normalization strategy;
- fusion rule, such as reciprocal-rank fusion or weighted fusion;
- deterministic tie-breaking behavior;
- low-confidence retrieval behavior before generation;
- rerank hook input/output contract, even if reranking is no-op initially;
- expected assertions against DT006/DT010 fixture cases;
- how hybrid retrieval should preserve or improve the DT010 semantic baseline.

Affected build tasks:

- `RAG-BT013`
- `RAG-BT014`
- `RAG-BT018`
- `RAG-BT019`

Owner decision status:

```text
Task file created; completion pending.
```

## RAG-DT019: Generation Prompt, Safeguards, Output Schema, And Query API Contract

Task file:

```text
build-sequence/02-design-tasks/05-runtime-technical-design/RAG-DT019-generation-prompt-safeguards-output-schema-and-query-api-contract.md
```

Purpose:

Define the generation prompt/message contract, safeguard behavior, output
schema, citation schema, refusal schema, error mapping, and query API consumer
contract before final build task impact review.

Why it is needed before `RAG-DT013`:

Current query/generation tasks describe intended behavior, but the exact
contract is spread across query planning, LLM evaluation, generation, output
validation, and query API tasks. Implementation needs one accepted artifact so
`RAG-BT015`, `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, and `RAG-BT019` do not
drift.

Minimum decisions:

- generation message roles and system/developer/user content boundaries;
- retrieved-context formatting;
- explicit rule that retrieved chunks are untrusted data;
- citation instruction and citation object schema;
- safe refusal wording and refusal-code/schema behavior;
- output JSON schema and validation behavior;
- low-confidence/no-evidence behavior;
- token/context budget and truncation behavior;
- API method/path, likely `POST /api/v1/query`;
- request schema;
- response schema;
- error-envelope mapping for validation and runtime failures;
- planner classification fields exposed to callers;
- model/provider/latency metadata included or withheld;
- FastAPI dependency-override pattern for mocked endpoint tests;
- config variable naming decision for runtime LLM and provider settings.

Affected build tasks:

- `RAG-BT015`
- `RAG-BT016`
- `RAG-BT017`
- `RAG-BT018`
- `RAG-BT019`
- later BFF/chatbot frontend work

Owner decision status:

```text
Task file created; completion pending.
```

## RAG-DT020: Post-Build Evaluation And Tuning Loop

Task file:

```text
build-sequence/02-design-tasks/05-runtime-technical-design/RAG-DT020-post-build-evaluation-and-tuning-loop.md
```

Purpose:

Define what happens after the built RAG service is evaluated: how failures are
classified, how tuning experiments are recorded, how baseline changes are
approved, and how adjustments become new tasks or accepted risks.

Why it is needed before `RAG-DT013`:

`RAG-BT019` already plans an evaluation harness, but the build sequence also
needs a post-evaluation adjustment loop. Without it, the project could run
evaluation without a governed way to decide whether to change chunking,
embedding, retrieval, prompt, model, validation, API behavior, CI/CD, or corpus
materialization.

Minimum decisions:

- evaluation run types and environments;
- local, PR CI, main CI, and owner-reviewed run expectations;
- retrieval, citation, answer, refusal, safety, latency, provider-error, and
  malformed-output metrics;
- failure taxonomy;
- mapping failures to likely adjustment areas;
- tuning experiment evidence structure;
- baseline acceptance, rejection, and rollback rules;
- owner decision gates after evaluation;
- when a failed evaluation creates a new build task, design task, bugfix task,
  or owner-accepted deferral.

Affected build tasks:

- `RAG-BT019`
- `RAG-BT022`
- any retrieval, generation, API, or ingestion task whose behavior is changed
  by post-build tuning decisions

Owner decision status:

```text
Task file created; completion pending.
```

## If Owner Waives A Required Task

If the owner decides not to complete one or more of these tasks, `RAG-DT013`
must record the waiver and carry the related gap as a High deferred risk.
