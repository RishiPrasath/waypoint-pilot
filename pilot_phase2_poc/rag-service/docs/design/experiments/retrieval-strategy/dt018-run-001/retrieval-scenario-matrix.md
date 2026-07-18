# DT018 Retrieval Scenario Matrix

Status: Proposed
Run: `dt018-run-001`

## Purpose

This matrix turns the `RAG-DT007` planner classifications and `RAG-DT006`
golden questions into concrete retrieval modes. The goal is to prevent every
query from blindly using the same retrieval path.

## Scenario Matrix

| Scenario | Example cases | Planner output | Retrieval mode | Why |
|---|---|---|---|---|
| Public import permit workflow | `GQ-001`, `GQ-002`, `QP-001`, `QP-002` | `in_scope` / `regulatory_explanation` | `exact_match_boosted_hybrid` | The query contains exact source/procedure terms such as Singapore Customs, import permit, Declaring Agent, and TradeNet. |
| Public export permit workflow | `GQ-004`, `QP-004` | `in_scope` / `regulatory_explanation` | `exact_match_boosted_hybrid` | Exact procedure terms should lift the expected `APAC-002` chunk while semantic retrieval preserves wording flexibility. |
| Boundary import/export questions | `GQ-003`, `GQ-005`, `QP-003`, `QP-005` | `in_scope_with_boundary` | `metadata_filtered_hybrid` | The service should retrieve boundary notes, then answer conservatively without operational/legal/fee inference. |
| ASEAN regional-index questions | `GQ-006`, `GQ-007`, `QP-006`, `QP-007` | `in_scope` / market `ASEAN` | `metadata_filtered_hybrid`; exact boost when article terms appear | The market filter should keep retrieval inside ASEAN-level material; exact terms such as `ATIGA Article 13` should help rank the expected chunk. |
| ASEAN country-specific limitation | `GQ-008`, `QP-008` | `in_scope_with_boundary` / market `ASEAN` | `metadata_filtered_hybrid` | Retrieval should find the review-note limitation and avoid claiming final country-specific obligations. |
| Live order/shipment status | `GQ-009`, `QP-009`, `QP-018` | `unsupported_operational` | `no_retrieval_safe_response` | Public regulatory chunks cannot answer live operational state. |
| Driver assignment/action request | `GQ-010`, `QP-010` | `unsupported_operational` | `no_retrieval_safe_response` | RAG explains source material; it does not dispatch, book, assign, submit, or pay. |
| Partner-source internal SOP | `GQ-011`, `QP-011` | `partner_source_required` | `no_retrieval_safe_response` | Internal procedures are outside the approved public corpus. |
| Irrelevant question | `GQ-012`, `QP-012` | `irrelevant` | `no_retrieval_safe_response` | Do not retrieve APAC regulatory chunks for unrelated questions. |
| Prompt injection / secret exfiltration | `GQ-013`, `QP-013` | `malicious` | `no_retrieval_safe_response` | Block before retrieval to avoid using source text as an attack surface. |
| License-sensitive reproduction | `GQ-014`, `QP-014`, `QP-015` | `license_sensitive` | `metadata_only_exclusion_lookup` or `no_retrieval_safe_response` | Metadata may explain exclusion, but answer text must not be retrieved or reproduced. |
| Ambiguous short query | `QP-019` | `ambiguous` | `no_retrieval_safe_response` | Ask for a scoped APAC customs/trade question instead of guessing a source. |
| New in-scope market/source hint | `QP-016`, `QP-017`, `QP-020` | `in_scope` | `metadata_filtered_hybrid` | Use hard market/source filters when approved source material exists; otherwise report missing evidence. |

## Mode Coverage Check

| Required mode | Covered? | Cases |
|---|---|---|
| `no_retrieval_safe_response` | yes | `GQ-009` through `GQ-013`, `QP-009` through `QP-013`, `QP-018`, `QP-019` |
| `metadata_only_exclusion_lookup` | yes | `GQ-014`, `QP-014`, `QP-015` |
| `semantic_only_baseline` | yes | `RAG-BT013` acceptance baseline |
| `lexical_only_diagnostic` | yes | `RAG-BT014` diagnostics |
| `exact_match_boosted_hybrid` | yes | import/export permit, source-title, article, HS/tariff/procedure terms |
| `metadata_filtered_hybrid` | yes | market/source-bound positive and boundary questions |
| `fused_hybrid` | yes | broad in-scope questions with no narrow source hint |
| `rerank_hook_candidate_set` | yes | no-op initially after fused top 8 |

## Observation

The planner already knows whether retrieval is allowed. The missing DT018 layer
is the retrieval strategy selector: it decides whether allowed retrieval should
be semantic baseline, metadata-filtered hybrid, exact-match boosted hybrid, or
metadata-only exclusion lookup.
