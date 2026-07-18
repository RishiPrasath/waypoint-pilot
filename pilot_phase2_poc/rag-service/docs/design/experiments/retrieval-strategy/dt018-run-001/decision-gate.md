# DT018 Decision Gate

Status: Accepted
Run: `dt018-run-001`
Task: `RAG-DT018`

## Gate Question

Is the retrieval strategy contract sufficient for build tasks `RAG-BT013`,
`RAG-BT014`, `RAG-BT018`, and `RAG-BT019` to proceed after final build impact
review?

## Decision

```text
Pass - accept planner-led metadata-filtered hybrid retrieval as the first-pass
runtime target, while preserving semantic-only retrieval as the baseline and
lexical-only retrieval as a diagnostic mode.
```

## Accepted Decisions

1. Query planner output drives retrieval mode selection.
2. No-retrieval classifications are blocked before retrieval.
3. License-sensitive and cite-only sources can be used only for metadata
   exclusion explanations unless later reuse approval is recorded.
4. Default positive retrieval mode is metadata-filtered hybrid retrieval.
5. Exact source/procedure/article/tariff/HS terms use exact-match boosted
   hybrid retrieval.
6. Semantic baseline remains `BAAI/bge-small-en`, 384 dimensions, cosine.
7. Lexical retrieval uses deterministic BM25-style scoring.
8. Fusion uses normalized weighted scores:
   `0.65 semantic + 0.35 lexical`, plus capped exact/metadata boosts.
9. Reranking is a hook only; no-op initially.
10. Low-confidence results stop generation or force cautious clarification.

## Evidence Reviewed

| Artifact | Finding |
|---|---|
| `docs/evaluation/golden-questions.md` | Provides positive, boundary, operational, partner-source, irrelevant, malicious, and license-sensitive cases. |
| `docs/design/query-planning/query_planner_rules.yaml` | Defines pre-retrieval classifications and retrieval allowance. |
| `docs/design/query-planning/query_planner_tests.yaml` | Provides deterministic planner fixtures `QP-001` through `QP-020`. |
| `docs/design/chunking-experiment.md` | Selects `hybrid_structure_recursive_v1` chunks and required metadata lineage. |
| `docs/design/embedding-benchmark-plan.md` | Selects `BAAI/bge-small-en` semantic baseline with accepted retrieval metrics. |
| `docs/design/source-snapshot-and-markdown-candidates.md` | Defines candidate source eligibility, reuse mode, and license-sensitive treatment. |
| `docs/design/test-vector-db-ci-strategy.md` | Defines in-memory/unit, local Docker Qdrant, and GitHub Actions Qdrant service testing roles. |
| `docs/design/architecture-sufficiency-review.md` | Identifies retrieval-mode and fusion contract as a required follow-up before `RAG-DT013`. |

## Risks And Controls

| Risk | Control |
|---|---|
| Hybrid fusion worsens the semantic baseline. | `RAG-BT014` must compare hybrid against `RAG-BT013`/`RAG-DT010` and treat Recall@3 regression as defect or owner tradeoff. |
| Exact boosts surface excluded material. | Hard source/reuse/license filters run before boosts. |
| Low-confidence retrieval feeds weak evidence to generation. | Contract requires a confidence gate before generation. |
| API hides retrieval routing decisions. | `RAG-BT018` must expose or trace retrieval mode, scores, and confidence behavior. |
| Evaluation mixes retrieval and generation failures. | `RAG-BT019` must report planner, retrieval, citation, answer, refusal, and low-confidence categories separately. |

## Build Impact

`RAG-BT013` may implement semantic-only baseline.

`RAG-BT014` may implement lexical/hybrid retrieval with this score contract.

`RAG-BT018` must preserve routing, score, citation, and low-confidence fields
through the API layer.

`RAG-BT019` must evaluate retrieval mode and fusion behavior separately from
generation quality.

## Gate Result

Accepted for PR review. Final status becomes complete only after merge closeout
updates the task file, design index, and evidence metadata.
