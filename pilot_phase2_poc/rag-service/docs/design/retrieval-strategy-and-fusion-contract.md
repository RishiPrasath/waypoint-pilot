# Retrieval Strategy And Fusion Contract

Status: Superseded historical contract; `RAG-DT018` calibration revision blocked
Run: `dt018-run-001`
Date: 2026-07-18

## Purpose

This contract defines how the Phase 2 RAG service chooses retrieval behavior
after deterministic query planning and before generation. It closes the gap
identified by `RAG-DT017`: the project had semantic, lexical, hybrid, source,
and evaluation tasks, but no accepted contract for when each retrieval mode
should run or how scores should be combined.

The contract is grounded in:

- `docs/evaluation/golden-questions.md`
- `docs/design/query-planning/query_planner_rules.yaml`
- `docs/design/query-planning/query_planner_tests.yaml`
- `docs/design/chunking-experiment.md`
- `docs/design/embedding-benchmark-plan.md`
- `docs/design/source-snapshot-and-markdown-candidates.md`
- `docs/design/test-vector-db-ci-strategy.md`
- `docs/design/architecture-sufficiency-review.md`

## Accepted Default

Use planner-led retrieval routing.

```text
user query
-> deterministic query planner
-> retrieval eligibility and source policy check
-> retrieval mode selection
-> semantic and/or lexical candidate retrieval
-> metadata hard filters
-> score normalization and fusion
-> deterministic tie-break
-> optional rerank hook
-> low-confidence gate
-> generation or safe response
```

The first-pass default for answerable public regulatory questions is:

```text
metadata-filtered hybrid retrieval
```

The semantic side uses the `RAG-DT010` selected embedding baseline:

```text
embedding_provider = fastembed
embedding_model_name = BAAI/bge-small-en
embedding_dimension = 384
embedding_distance = cosine
```

The lexical side uses a deterministic BM25-style scorer over the same
`hybrid_structure_recursive_v1` chunks selected by `RAG-DT005`.

## Retrieval Modes

| Mode | Meaning | Initial use |
|---|---|---|
| `no_retrieval_safe_response` | Planner blocks retrieval and returns a safe response class. | malicious, irrelevant, unsupported operational, partner-source, ambiguous, license-sensitive reproduction |
| `metadata_only_exclusion_lookup` | Lookup source metadata only, without retrieving answer text. | cite-only/license-sensitive exclusion explanation such as `APAC-215` |
| `semantic_only_baseline` | Dense vector search only. | `RAG-BT013` baseline and diagnostics |
| `lexical_only_diagnostic` | Lexical search only. | `RAG-BT014` diagnostics and exact-token failure analysis |
| `exact_match_boosted_hybrid` | Hybrid retrieval with lexical boosts for exact identifiers, source titles, article numbers, HS/tariff terms, and procedure names. | exact document/title/source, HS code/article/tariff/permit/named-procedure queries |
| `metadata_filtered_hybrid` | Hybrid retrieval with hard source filters from planner output. | market/source-scoped public regulatory questions |
| `fused_hybrid` | Hybrid retrieval without a narrow hard source hint, but still limited to approved retrieval-eligible content. | broad in-scope public regulatory questions |
| `rerank_hook_candidate_set` | Stable input/output shape for a future reranker; no-op initially. | optional after fused candidate set exists |

## Scenario Decision Matrix

| Scenario | Planner classification | Retrieval mode | Filter behavior | Generation behavior |
|---|---|---|---|---|
| In-scope natural language regulatory question | `in_scope` | `metadata_filtered_hybrid` when market/source hint exists; otherwise `fused_hybrid` | Hard filter to approved, retrieval-eligible namespace; market filter when detected | Generate only from returned chunks with citations |
| Exact document, title, source, procedure, permit, article, tariff, or HS-code question | `in_scope` or `in_scope_with_boundary` | `exact_match_boosted_hybrid` | Hard source/market filters when planner emits them; lexical boosts for exact terms | Generate only when retrieved context passes confidence gate |
| Market-constrained question | `in_scope` | `metadata_filtered_hybrid` | Hard jurisdiction filter for detected market; do not substitute another market unless explicitly asked | If no matching source, say evidence is missing |
| Source-boundary question | `in_scope_with_boundary` | `metadata_filtered_hybrid` or `exact_match_boosted_hybrid` | Retrieve source-boundary chunks; preserve review-note chunks when expected | Answer conservatively with limits and citations |
| Ambiguous question | `ambiguous` | `no_retrieval_safe_response` | None | Ask for a specific APAC customs/trade question |
| Irrelevant question | `irrelevant` | `no_retrieval_safe_response` | None | Explain out-of-scope; no citations |
| Operational/live-status question | `unsupported_operational` | `no_retrieval_safe_response` | None | Refuse operational action/status; no unrelated citations |
| Partner-source/internal procedure question | `partner_source_required` | `no_retrieval_safe_response` | None | State public RAG corpus does not contain partner SOPs |
| Malicious/prompt-injection question | `malicious` | `no_retrieval_safe_response` | None | Refuse before retrieval |
| License-sensitive reproduction request | `license_sensitive` | `metadata_only_exclusion_lookup` only when metadata explains the boundary; otherwise `no_retrieval_safe_response` | Source metadata only; no answer-content chunks | Do not reproduce protected content |

## Query Planner To Retrieval Mapping

| Planner output | Retrieval allowed? | Retrieval mode | Notes |
|---|---:|---|---|
| `in_scope`, source hint present | yes | `metadata_filtered_hybrid` | Prefer expected source candidates such as `APAC-001`, `APAC-002`, `APAC-201`. |
| `in_scope`, exact identifier/title/procedure terms present | yes | `exact_match_boosted_hybrid` | Use lexical boosts for exact terms while retaining semantic recall. |
| `in_scope`, no source hint | yes | `fused_hybrid` | Search approved retrieval-eligible corpus; use top fused evidence only. |
| `in_scope_with_boundary` | yes | `metadata_filtered_hybrid` or `exact_match_boosted_hybrid` | Retrieve boundary notes and answer with limits. |
| `unsupported_operational` | no | `no_retrieval_safe_response` | Do not cite unrelated regulatory chunks. |
| `partner_source_required` | no | `no_retrieval_safe_response` | Future partner-source layer may change this. |
| `irrelevant` | no | `no_retrieval_safe_response` | No retrieval. |
| `malicious` | no | `no_retrieval_safe_response` | Block before retrieval. |
| `license_sensitive` | no answer-text retrieval | `metadata_only_exclusion_lookup` | Metadata may explain cite-only or license-sensitive exclusion. |
| `ambiguous` | no | `no_retrieval_safe_response` | Ask for clarification. |

## Source Eligibility And Metadata Policy

Retrieval must respect the source registry and candidate lineage.

Hard filters:

- `retrieval_eligible` must be true for answer-content chunks.
- `reuse_mode` must allow summarization or answer use.
- `license_sensitive: true` content must not be used as answer text unless a
  later task records explicit reuse approval.
- `legacy/`, `drop/`, and `archive/` paths must not be runtime retrieval
  sources.
- Planner market filters must be hard filters when a market is detected.
- Source hints from planner tests should become hard filters when they identify
  a specific approved source.

Metadata boosts:

- exact `document_id`, source title, source owner, market, heading token, or
  procedure-name match may boost rank inside the eligible filtered set;
- boost must never override a hard exclusion;
- boost must be reported in debug/evaluation output.

## Lexical Tokenization And Normalization

Use a deterministic BM25-style lexical scorer over chunk text plus selected
metadata fields.

Normalize query and indexed text by:

- Unicode NFKC normalization;
- lowercasing;
- converting common punctuation/hyphen variants to spaces except inside useful
  identifiers;
- preserving alphanumeric identifiers such as `APAC-001`, `WP-12345`,
  `ATIGA Article 13`, HS-like numeric terms, source IDs, and permit names;
- splitting on whitespace and punctuation boundaries;
- dropping a short project stopword list for common English filler words;
- keeping domain terms such as `permit`, `customs`, `tariff`, `origin`,
  `TradeNet`, `Declaring Agent`, `ATIGA`, `WCO`, `ASEAN`;
- adding phrase tokens for known vocabulary aliases from the planner vocabulary
  when available.

Lexical indexed fields:

```text
chunk.text
heading_path
document_id
source_title
source_owner
source_uri host/path terms
market/jurisdiction
known aliases from planner vocabulary
```

## Candidate Pools

Initial first-pass candidate sizes:

| Stage | Size | Purpose |
|---|---:|---|
| semantic query to Qdrant | top 12 | enough dense recall for small corpus and future growth |
| lexical query | top 12 | enough exact-token recall for source/title/procedure cases |
| merged pool before fusion | up to 24 unique chunks | union by stable `chunk_id` |
| fused output before rerank | top 8 | compact candidate set for optional rerank/context packing |
| generation context | top 4 chunks by default | concise context with citation coverage |

`RAG-BT013` may use semantic top 5 for baseline parity with `RAG-DT010`, but
the runtime contract above is the target once hybrid retrieval exists.

## Score Normalization And Fusion

Normalize scores per query before fusion:

- semantic cosine similarity: map to `[0, 1]` as supplied by Qdrant/client when
  possible; otherwise min-max normalize over returned semantic candidates;
- lexical BM25: min-max normalize over returned lexical candidates; if all
  lexical scores are equal, assign `1.0` to positive matches and `0.0` to
  missing matches;
- exact-match boost: add a capped boost after base fusion, never exceeding
  final score `1.0`;
- metadata boost: add a smaller capped boost after base fusion, never exceeding
  final score `1.0`.

Initial fusion formula:

```text
base_fused_score = (0.65 * semantic_norm) + (0.35 * lexical_norm)
final_score = min(1.0, base_fused_score + exact_match_boost + metadata_boost)
```

Boost caps:

```text
exact_match_boost <= 0.15
metadata_boost <= 0.05
```

For `exact_match_boosted_hybrid`, the same formula is used, but exact-match
boosts are enabled for source IDs, title/source terms, article numbers,
permit/procedure names, and HS/tariff terms.

Rationale:

- the selected embedding benchmark already proved strong semantic baseline
  quality on the first-pass fixture;
- lexical ranking is added to protect exact tokens, source names, and procedure
  terms that dense retrieval can blur;
- modest boost caps prevent metadata or exact-token matches from defeating
  hard source policy or obviously better semantic evidence.

## Deterministic Tie-Breaking

When two chunks have the same final score, sort by:

1. higher exact-match count;
2. higher hard-filter/source-hint match;
3. higher semantic normalized score;
4. higher lexical normalized score;
5. lower `document_id`;
6. lower `chunk_index`;
7. lower `chunk_id`.

Every retrieval report should include enough fields to reproduce this order.

## Rerank Hook Contract

Reranking is not required as a runtime dependency in the first implementation,
but `RAG-BT014` must expose a no-op-compatible hook.

Input:

```json
{
  "query": "string",
  "normalized_query": "string",
  "planner": {
    "relevance_classification": "string",
    "intent": "string",
    "markets": ["string"],
    "source_filters": ["string"]
  },
  "candidates": [
    {
      "chunk_id": "string",
      "document_id": "string",
      "heading_path": "string",
      "text": "string",
      "semantic_score": 0.0,
      "lexical_score": 0.0,
      "fused_score": 0.0,
      "metadata": {}
    }
  ]
}
```

Output:

```json
{
  "rerank_applied": false,
  "reranker_id": "noop_v1",
  "candidates": []
}
```

The no-op implementation must preserve deterministic fused ordering.

## Low-Confidence Behavior

Low confidence is evaluated after fusion and before generation.

Initial thresholds:

| Condition | Behavior |
|---|---|
| no candidates after filters | safe no-evidence response |
| top fused score `< 0.45` | safe no-evidence response |
| top score `0.45-0.60` and no exact/source hint match | cautious response or clarification; do not over-answer |
| expected market/source hard filter has no result | say the approved source set lacks evidence for that market/source |
| license-sensitive or cite-only candidate is the only match | explain exclusion boundary; no answer-text generation |

Generation may proceed when:

- planner allows retrieval;
- at least one eligible chunk survives filters;
- top evidence passes the confidence gate;
- citation metadata is complete enough for response validation.

## Golden Question And Planner Mapping

| Golden / planner cases | Expected mode |
|---|---|
| `GQ-001`, `GQ-002`, `QP-001`, `QP-002` | `exact_match_boosted_hybrid` with hard source hint `APAC-001` |
| `GQ-003`, `QP-003` | `metadata_filtered_hybrid`, boundary answer, source hint `APAC-001` |
| `GQ-004`, `QP-004` | `exact_match_boosted_hybrid` with hard source hint `APAC-002` |
| `GQ-005`, `QP-005` | `metadata_filtered_hybrid`, boundary answer, source hint `APAC-002` |
| `GQ-006`, `GQ-007`, `QP-006`, `QP-007` | `metadata_filtered_hybrid` with market `ASEAN` and source hint `APAC-201`; exact boost when `ATIGA Article 13` appears |
| `GQ-008`, `QP-008` | `metadata_filtered_hybrid`, boundary answer, source hint `APAC-201` |
| `GQ-009`, `GQ-010`, `QP-009`, `QP-010`, `QP-018` | `no_retrieval_safe_response` |
| `GQ-011`, `QP-011` | `no_retrieval_safe_response` |
| `GQ-012`, `QP-012` | `no_retrieval_safe_response` |
| `GQ-013`, `QP-013` | `no_retrieval_safe_response` |
| `GQ-014`, `QP-014`, `QP-015` | `metadata_only_exclusion_lookup` or `no_retrieval_safe_response` |
| `QP-016`, `QP-017`, `QP-020` | `metadata_filtered_hybrid`; source hint if source exists in approved fixture/corpus |
| `QP-019` | `no_retrieval_safe_response` with clarification |

## Evaluation Expectations

`RAG-BT019` must report retrieval separately from generation:

- planner classification accuracy;
- retrieval mode chosen;
- expected source at rank 1;
- expected chunk Recall@3 and Recall@5;
- MRR;
- source lineage validity;
- citation metadata completeness;
- low-confidence/no-evidence behavior;
- negative cases that correctly perform no retrieval;
- license-sensitive cases that do not retrieve answer text.

Hybrid retrieval should preserve the `RAG-DT010` semantic baseline:

```text
positive expected chunk Recall@3 must not regress below the DT010 accepted run
unless the regression is recorded as a defect or accepted owner tradeoff.
```

## Build Task Impact

`RAG-BT013`:

- implement `semantic_only_baseline`;
- use `BAAI/bge-small-en`, 384 dimensions, cosine distance;
- seed from `hybrid_structure_recursive_v1` chunks;
- assert source lineage and semantic baseline Recall@k;
- expose scores and metadata needed for later hybrid comparison.

`RAG-BT014`:

- implement lexical scorer, hybrid fusion, exact-match boosts, metadata boosts,
  deterministic tie-breaking, and no-op rerank hook;
- compare hybrid output against semantic baseline;
- reject retrieval of `APAC-215` answer text;
- keep lexical-only as diagnostic, not the default answer path.

`RAG-BT018`:

- expose or trace retrieval mode, planner class, candidate counts, score fields,
  low-confidence decision, and citation metadata through the query API contract;
- do not require live Qdrant or LLM in default API tests;
- block no-retrieval cases before retrieval/generation.

`RAG-BT019`:

- evaluate planner classification, retrieval mode, retrieval quality, citation
  lineage, answer quality, refusal behavior, and low-confidence behavior as
  separate categories;
- compare semantic and hybrid retrieval results against the same DT006 fixture;
- separate mock/unit evaluation from service-backed Qdrant evaluation.

## Deferred Work

- production-scale benchmark after corpus expansion;
- LLM reranker selection;
- partner-source/internal retrieval;
- external search integration;
- final production corpus promotion.
