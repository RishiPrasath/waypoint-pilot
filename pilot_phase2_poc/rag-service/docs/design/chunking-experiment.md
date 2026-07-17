# RAG-DT005 Chunking Experiment

Status: Accepted for `RAG-DT005`
Date: 2026-07-17

## Purpose

This design task selects the chunking strategy that later ingestion and
retrieval build tasks should implement. It uses a lightweight local experiment
runner so the decision is based on pipeline-shaped artifacts rather than prose
only.

The experiment mirrors the future ingestion flow:

```text
snapshot manifest -> queue item -> candidate loader -> hash verification
-> markdown parser -> chunking strategy -> JSONL chunk records -> report
```

## Experiment Run

Run ID:

```text
dt005-run-001
```

Artifact folder:

```text
docs/design/experiments/chunking/dt005-run-001/
```

Generated artifacts:

```text
queue-manifest.json
chunks-fixed-window-baseline.jsonl
chunks-structure-aware-v1.jsonl
chunks-hybrid-structure-recursive-v1.jsonl
comparison-report.md
run_chunking_experiment.py
```

## Source Inputs

The queue is built from:

```text
knowledge_base/snapshots/first-pass-snapshot-manifest.md
```

Chunked candidates:

```text
knowledge_base/candidates/first-pass/APAC-001-sg-import-permit.md
knowledge_base/candidates/first-pass/APAC-002-sg-export-permit.md
knowledge_base/candidates/first-pass/APAC-201-asean-trade-repository.md
```

Excluded candidate:

```text
knowledge_base/candidates/first-pass/APAC-215-wco-hs-nomenclature-metadata.md
```

`APAC-215` is skipped because it is metadata-only and license-sensitive.

## Queue Semantics

Each candidate is represented as a local design-experiment queue item with:

- `run_id`
- `queue`
- `job_type`
- `document_id`
- `snapshot_id`
- `candidate_path`
- `candidate_sha256`
- `normalized_text_sha256`
- `raw_checkout_sha256`
- `hash_verified`
- `reuse_mode`
- `license_sensitive`
- `retrieval_eligible`
- `status`
- `reason`

The local status sequence is:

```text
queued -> loaded -> hash_verified -> parsed -> reported
```

Skipped or failed candidates remain visible in `queue-manifest.json`.

## Hash Verification Finding

The runner verifies `candidate_sha256` against a normalized text SHA-256. This
is intentional because Windows checkout may use CRLF even when the manifest was
created from canonical LF text. The raw checkout SHA-256 is still recorded as
diagnostic evidence.

This makes the future ingestion contract explicit:

- content identity checks should normalize line endings for markdown text
- raw byte hashes may still be retained for local checkout diagnostics
- hash verification must happen before chunking

## Strategies Compared

### `fixed_window_baseline_v1`

This baseline chunks by approximate word windows with overlap.

Parameters:

- target window: 80 words
- overlap: 15 words

This strategy is deterministic and simple, but it can split candidate sections
without respecting source shape, headings, or review warnings.

### `structure_aware_v1`

This strategy parses markdown frontmatter and heading blocks. It emits chunks
by heading-aware sections while preserving lineage metadata on every chunk.

Each output chunk carries:

- `chunk_id`
- `run_id`
- `queue`
- `job_type`
- `document_id`
- `snapshot_id`
- `source_uri`
- `candidate_path`
- `candidate_sha256`
- `chunk_strategy`
- `chunk_index`
- `heading_path`
- `word_count`
- `reuse_mode`
- `license_sensitive`
- `retrieval_eligible`
- `retrieval_namespace`
- `language`
- `source_lineage`
- `text`

### `hybrid_structure_recursive_v1`

This strategy first uses the same markdown heading structure as
`structure_aware_v1`. Then it checks each heading section against an experiment
word cap. If the section is too large, it recursively splits the section by
paragraph boundaries first and word windows only as a final fallback.

Experiment parameters:

- max section size: 80 words
- fallback overlap: 15 words

Each output chunk carries the same lineage metadata as `structure_aware_v1`,
plus:

- `section_part_index`
- `section_part_count`
- `recursive_split_applied`
- `max_section_words`
- `overlap_words`

## Results

| Document ID | Fixed-window chunks | Structure-aware chunks | Hybrid structure-recursive chunks | Recursive split applied? |
|---|---:|---:|---:|---|
| `APAC-001` | 3 | 3 | 4 | `true` |
| `APAC-002` | 2 | 3 | 3 | `false` |
| `APAC-201` | 3 | 3 | 3 | `false` |
| `APAC-215` | 0 | 0 | 0 | `false` |

`APAC-215` appears in the queue as skipped, not failed.

## Chosen Strategy

`hybrid_structure_recursive_v1` is the chosen strategy.

Reasons:

- it preserves heading paths for citation and debugging
- it keeps source-derived notes separate from review notes
- it carries manifest lineage and candidate hash into every chunk
- it keeps small sections intact but prevents large heading sections from
  becoming overly broad retrieval units
- it is deterministic enough for fixture tests
- it cleanly excludes metadata-only and license-sensitive sources

## Rejected Alternative

`fixed_window_baseline_v1` is rejected as the default strategy.

Reasons:

- it can detach procedural context from source headings
- it can blend review warnings with source-derived notes
- it weakens citation precision
- it is less useful for metadata-filtered retrieval tests

`structure_aware_v1` is rejected as the final default strategy but retained as
an important comparison. It preserves headings well, but a single long heading
section can still become one oversized chunk.

The fixed-window output remains useful as a regression baseline and as evidence
that the chosen strategy was compared against a simpler alternative.

## Metadata Contract

`RAG-BT009` should implement chunk metadata compatible with
`chunks-hybrid-structure-recursive-v1.jsonl`.

Minimum required fields:

```text
chunk_id
document_id
snapshot_id
source_uri
candidate_path
candidate_sha256
chunk_strategy
chunk_index
heading_path
word_count
section_part_index
section_part_count
recursive_split_applied
reuse_mode
license_sensitive
retrieval_eligible
retrieval_namespace
language
source_lineage
text
```

Chunk IDs should be deterministic:

```text
{document_id}-{snapshot_id}-sa-{chunk_index:03d}
```

The accepted hybrid implementation should use:

```text
{document_id}-{snapshot_id}-hsr-{chunk_index:03d}
```

## Retrieval Impact

The chosen strategy should improve retrieval precision because retrieved chunks
carry section context, source lineage, and manifest hash evidence. Retrieval
tests should assert both semantic match and metadata integrity.

Expected downstream effects:

- `RAG-BT009` implements `hybrid_structure_recursive_v1`.
- `RAG-BT012` reads manifest-backed candidates, verifies normalized text hashes,
  then emits chunk records matching this metadata contract.
- `RAG-BT013` seeds semantic retrieval from structure-aware chunks.
- `RAG-BT014` uses the same chunk IDs for lexical and hybrid retrieval parity.
- `RAG-BT019` validates citations against chunk metadata and source lineage.

## Legacy Boundary

Legacy Phase 1 KB material remains audit-only:

```text
pilot_phase2_poc/rag-service/legacy/phase1-kb-snapshot/
```

It was not used as a runtime chunking input for this experiment.

## Deferred Work

- production ingestion queue backend
- production worker process
- embedding model lock
- vector DB indexing
- broader table-heavy, FAQ, and bilingual candidate expansion after more
  approved Phase 2 source candidates exist
