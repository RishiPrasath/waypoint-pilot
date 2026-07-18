# DT018 Scoring Options

Status: Proposed
Run: `dt018-run-001`

## Options Reviewed

| Option | Description | Pros | Cons | Decision |
|---|---|---|---|---|
| Semantic-only | Dense retrieval with `BAAI/bge-small-en` only. | Already benchmarked in DT010; simple; strong first-pass quality. | Can blur exact identifiers, article numbers, titles, and procedure names. | Keep as `RAG-BT013` baseline and diagnostic comparison. |
| Lexical-only | BM25-style ranking over chunk text and metadata. | Strong for exact terms and source names; deterministic; easy to debug. | Weak for paraphrases and broader natural-language questions. | Keep as diagnostic, not answer default. |
| Weighted-score hybrid | Normalize semantic and lexical scores, then combine with fixed weights. | Simple, transparent, implementable locally; supports deterministic tests. | Requires careful normalization and thresholds. | Selected first-pass fusion method. |
| Reciprocal-rank fusion | Combine ranked lists by reciprocal rank rather than raw scores. | Robust when raw scores are hard to compare. | Less direct score interpretability for API/evaluation; harder to set low-confidence thresholds. | Deferred as comparison if weighted scoring is unstable. |
| Cross-encoder/LLM reranking | Re-rank fused candidates with another model. | Can improve ordering for complex queries. | Adds latency, dependency, cost, and another model-selection task. | Hook only; no-op initially. |

## Selected Scoring Contract

Use weighted-score hybrid:

```text
base_fused_score = (0.65 * semantic_norm) + (0.35 * lexical_norm)
final_score = min(1.0, base_fused_score + exact_match_boost + metadata_boost)
```

Boost caps:

```text
exact_match_boost <= 0.15
metadata_boost <= 0.05
```

## Why This Is The Right First Pass

The DT010 embedding benchmark found the selected semantic model already performs
well on the first-pass fixture. The service should not throw that away. Lexical
scoring is added because this corpus has regulatory document identifiers,
article numbers, source names, procedure names, and jurisdiction terms where
exact matching matters.

The selected method is intentionally boring in the good way: deterministic,
explainable, locally testable, and easy to compare against the semantic
baseline.

## Normalization Rules

Semantic scores:

- use Qdrant/client cosine similarity when already normalized;
- otherwise min-max normalize over returned semantic candidates;
- missing semantic candidate score is `0.0`.

Lexical scores:

- BM25 scores are min-max normalized over returned lexical candidates;
- missing lexical candidate score is `0.0`;
- if every positive lexical match has the same score, assign positive matches
  `1.0` and non-matches `0.0`.

Boosts:

- exact boosts apply to source IDs, title tokens, article numbers, permit names,
  HS/tariff-like terms, and named procedures;
- metadata boosts apply to source hint, market, source owner, and heading path
  matches;
- boosts are impossible when a source is excluded by hard filter.

## Tie-Breaking

Tie-break order:

1. exact-match count;
2. source-hint or hard-filter match;
3. semantic normalized score;
4. lexical normalized score;
5. `document_id`;
6. `chunk_index`;
7. `chunk_id`.

## Low-Confidence Thresholds

| Signal | Action |
|---|---|
| no eligible candidates | no-evidence safe response |
| top fused score `< 0.45` | no-evidence safe response |
| top fused score `0.45-0.60` and no exact/source hint | cautious answer or clarification |
| only cite-only/license-sensitive metadata match | exclusion explanation only |
| expected market/source has no eligible result | say approved evidence is missing |

## Candidate Pool Sizes

| Pool | Size |
|---|---:|
| semantic retrieval | 12 |
| lexical retrieval | 12 |
| merged unique pool | up to 24 |
| fused pre-rerank | 8 |
| generation context | 4 |

These sizes are intentionally modest because the current fixture corpus is
small. Later corpus expansion can tune them in `RAG-DT020` evaluation cycles.
