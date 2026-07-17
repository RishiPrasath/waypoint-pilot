# DT005 Chunking Experiment Comparison Report

Run ID: `dt005-run-001`
Generated: `2026-07-17T05:00:17+00:00`

## Queue Summary

| Document ID | Status | Reason |
|---|---|---|
| `APAC-001` | `reported` | chunk outputs generated |
| `APAC-002` | `reported` | chunk outputs generated |
| `APAC-201` | `reported` | chunk outputs generated |
| `APAC-215` | `skipped` | metadata-only or license-sensitive source |

## Strategy Output Counts

| Document ID | Fixed-window chunks | Structure-aware chunks | Hybrid structure-recursive chunks | Recursive split applied? |
|---|---:|---:|---:|---|
| `APAC-001` | 3 | 3 | 4 | `true` |
| `APAC-002` | 2 | 3 | 3 | `false` |
| `APAC-201` | 3 | 3 | 3 | `false` |

## Observations

- `fixed_window_baseline_v1` is deterministic and simple, but it can split candidate sections without regard to source intent.
- `structure_aware_v1` preserves heading context and keeps review notes separate from source-derived notes.
- `hybrid_structure_recursive_v1` preserves heading context and recursively splits oversized sections by paragraph/word boundaries.
- The current first-pass candidates are short; only `APAC-001` exercises the recursive fallback under the 80-word experiment cap.
- `APAC-215` is intentionally skipped because it is metadata-only and license-sensitive.

## Chosen Strategy

`hybrid_structure_recursive_v1` is the chosen strategy for `RAG-BT009` implementation.

## Rejected Alternative

`fixed_window_baseline_v1` is rejected as the default because it weakens citation precision and can detach procedural context from source lineage. `structure_aware_v1` is useful but incomplete because a single large heading section can become too broad for retrieval.

## Retrieval Impact

Hybrid structure-recursive chunks should improve retrieval precision by keeping heading paths and source lineage while preventing large sections from becoming overly broad chunks. Downstream retrieval tests should assert both semantic match and source metadata integrity.
