# Post-Build Evaluation And Tuning Loop

Status: Accepted for `RAG-DT020`

## Purpose

This design defines the post-build quality gate for the RAG service. The goal is to make `RAG-BT019`, `RAG-BT022`, and eventual final build tasks safe to start by forcing a structured evaluation cycle whenever a major build or configuration change is available.

## Evaluation Environments

Use the following progression before considering production baseline promotion:

1. Developer local checks (fast): unit, formatting, and mocked-component checks.
2. Local integration checks with Qdrant-in-memory: parser/chunking/embedding/retrieval query path exercised with local vector store.
3. Local Docker integration checks: end-to-end compose-style containerized service run for query endpoint and retrieval service health.
4. Post-change comparison checks: rerun the same query set before and after each candidate change.
5. Optional LLM-backed judge checks: only when `RAG_EVAL_LLM_API_KEY` is intentionally supplied.

## Predefined Run Types

### Run 1: Regression Baseline
- Objective: detect immediately visible regressions.
- Inputs: `docs/evaluation/golden-questions.md`.
- Owners: `RAG-BT019` + design owner.
- Artifacts required: pass/fail by scenario and metric list.

### Run 2: Retrieval-Contract Run
- Objective: verify retrieval output stability and ranking quality.
- Inputs: golden questions + retrieval corpus candidates.
- Focus: Recall@K, chunk presence, rerank behavior, and metadata-only exclusions.

### Run 3: Generation and Safety Run
- Objective: verify answer quality and safety.
- Inputs: golden questions filtered by safeguard categories.
- Focus: citation validity, refusal correctness, malformed outputs handling.

### Run 4: API and Failure-mode Run
- Objective: validate `POST /api/v1/query` contract behavior under normal, malformed, and refusal scenarios.
- Focus: response schema adherence, status/error behavior, planner block path behavior.

### Run 5: LLM-evaluator Run
- Objective: quality score checks beyond regex/JSON validation.
- Focus: relevance, completeness, groundedness, and prompt-boundary adherence.

## Baseline Strategy

- `baseline_accepted` starts as the merged `main` baseline.
- Any change must produce an equal-or-better score for all mandatory metrics, with explicit owner exceptions for approved cost/latency tradeoffs.
- If no exception is granted, the change is rejected.

## Decision Rules (Minimum)

Mandatory metrics and rules:

- Retrieval Recall@K: not below baseline.
- Expected chunk presence: not below baseline.
- Ranking quality (MRR or nearest equivalent): not below baseline.
- Citation coverage/correctness: must remain valid and non-empty for non-blocked answers.
- Answer groundedness: must pass judge/automated fallback criteria.
- Refusal/safety behavior: must not regress.
- Relevance and malformed-response behavior: must pass mandatory checks.
- Latency: must not exceed approved SLA budget set by owner.
- Provider/model error rate: must remain in approved range.

Any hard failure in mandatory rules requires follow-up action in one of:

- `Design adjustment task`
- `Build task`
- `Risk acceptance` (with explicit owner and expiry)

## Failure Taxonomy and Mapping

- `Chunking mismatch` → affects source chunking assumptions and candidate docs.
- `Embedding mismatch` → affects embedding model and vectorization policy.
- `Vector DB mismatch` → affects Qdrant schema, payload keys, indexes, or memory mode choice.
- `Retrieval mismatch` → affects `RAG-DT018` assumptions and strategy routing.
- `Planner mismatch` → affects `query_planner_rules.yaml` and planner tests.
- `Prompt/output mismatch` → affects `RAG-DT019` safeguards and schema enforcement.
- `API mismatch` → affects `RAG-BT018` and query API consumer contract.
- `CI mismatch` → affects `RAG-DT014` and `RAG-DT016` CI readiness decisions.

## Tuning Workflow

For each incident of regression:

1. Capture baseline and candidate run outputs for each scenario.
2. Assign likely root-cause bucket from taxonomy.
3. Propose one controlled experiment.
4. Record experiment config, results, and interpretation.
5. Re-run relevant run type before making a final call.
6. Promote or reject baseline using decision gate.

Only one variable should change per tuning run until causality is clear.

## Outputs to Produce Per Run

- Metrics JSON with named version and timestamp.
- Scenario-wise result table.
- Failure-to-remediation link with owner.
- `PASS`, `PASS_WITH_WARNING`, `HOLD`, or `REJECT` status.

## Owner Gate Policy

Before any downstream build task starts after this task, owner review is required when:

- a metric regresses against mandatory threshold;
- a new failure class appears;
- or any `HOLD` state is entered for safety/quality.

## Integration with Build Tasks

- `RAG-BT019` should consume metric buckets by category and report structured pass/fail per mode.
- `RAG-BT022` should include gating evidence for production-readiness posture.
- All build tasks from `RAG-BT019` onward must use this playbook for post-change checks.

## Out of Scope

- Production observability and live traffic replay.
- Auto-rollback in production (deferred).
- Model replacement without explicit follow-up design work.
