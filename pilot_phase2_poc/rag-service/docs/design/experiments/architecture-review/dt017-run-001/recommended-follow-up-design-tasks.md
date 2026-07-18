# DT017 Recommended Follow-Up Design Tasks

Status: In Review
Run: `dt017-run-001`
Date: 2026-07-18

DT017 recommends two follow-up design tasks before `RAG-DT013`, unless the
owner explicitly waives them.

No follow-up task files were created in this branch because the DT017 task file
says not to create follow-up task files unless the owner explicitly accepts
them or the task file says they are mandatory before closeout.

## RAG-DT018: Hybrid Retrieval Scoring And Fusion Contract

Purpose:

Define the exact hybrid retrieval scoring/fusion contract before final build
task impact review.

Why it is needed before `RAG-DT013`:

`RAG-BT014` currently says hybrid retrieval should include lexical retrieval,
fusion, and a reranking hook, but it does not define the exact ranking contract.
Without that contract, semantic retrieval, hybrid retrieval, evaluation, and
query API tasks may implement incompatible ranking assumptions.

Output artifacts:

```text
docs/design/hybrid-retrieval-scoring-contract.md
docs/design/experiments/hybrid-retrieval-scoring/dt018-run-001/scoring-options.md
docs/design/experiments/hybrid-retrieval-scoring/dt018-run-001/decision-gate.md
build-evidence/RAG-DT018-hybrid-retrieval-scoring-contract.md
```

Minimum decisions:

- lexical method, for example BM25 variant or deterministic lightweight
  baseline;
- tokenization/normalization rules;
- metadata filter and boost behavior;
- candidate-pool sizes for semantic, lexical, and fused retrieval;
- score normalization strategy;
- fusion rule, such as reciprocal-rank fusion or weighted fusion;
- tie-breaking behavior;
- rerank hook input/output contract, even if reranking is deferred;
- expected assertions against DT006/DT010 fixture cases;
- how hybrid retrieval should improve or preserve the DT010 semantic baseline.

Affected build tasks:

- `RAG-BT013`
- `RAG-BT014`
- `RAG-BT018`
- `RAG-BT019`

Owner decision status:

```text
Pending
```

## RAG-DT019: Generation Prompt, Output Schema, And Query API Consumer Contract

Purpose:

Define the generation prompt/message contract, output schema, citation schema,
safe refusal schema, and query API consumer contract before final build task
impact review.

Why it is needed before `RAG-DT013`:

Current query/generation tasks describe intended behavior, but the exact
contract is spread across query planning, LLM evaluation, generation, output
validation, and query API tasks. The implementation needs one accepted artifact
so `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, and `RAG-BT019` do not drift.

Output artifacts:

```text
docs/design/generation-and-query-api-contract.md
docs/design/experiments/generation-api-contract/dt019-run-001/prompt-contract.md
docs/design/experiments/generation-api-contract/dt019-run-001/response-schema.json
docs/design/experiments/generation-api-contract/dt019-run-001/api-examples.md
docs/design/experiments/generation-api-contract/dt019-run-001/decision-gate.md
build-evidence/RAG-DT019-generation-query-api-contract.md
```

Minimum decisions:

- generation message roles and system/developer/user content boundaries;
- retrieved-context formatting;
- explicit rule that retrieved chunks are untrusted data;
- citation instruction and citation object schema;
- safe refusal wording and refusal-code schema;
- output JSON schema and validation behavior;
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
Pending
```

## If Owner Waives Either Task

If the owner decides not to create one or both follow-up tasks, `RAG-DT013`
must record the waiver and carry the related gap as a High deferred risk.

