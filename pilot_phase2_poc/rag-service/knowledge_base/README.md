# RAG Service Knowledge Base

Status: Accepted folder contract for `RAG-DT004`
Date: 2026-07-16

This folder is the only approved Phase 2 knowledge-base root for `rag-service`.
Build tasks must not invent alternate KB paths and must not ingest the
service-root `legacy/` folder directly.

## Accepted Folder Layout

```text
knowledge_base/
  README.md
  registry/
    source_registry.yaml
    source_registry.schema.json
  snapshots/
  candidates/
  canonical/
  reference/
  archive/
  drop/
```

Only `registry/` is populated at the end of `RAG-DT004`. The other folders are
reserved paths and should be created by the task that first writes reviewed
material into them.

## Folder Contracts

| Folder | Purpose | Ingestion rule |
|---|---|---|
| `registry/` | Source metadata, schema, promotion state, retrieval eligibility, and review ownership. | Validators may read `source_registry.yaml` and `source_registry.schema.json`. |
| `snapshots/` | Immutable captured source copies with snapshot IDs, dates, hashes, and source lineage. | Ingestion may read only reviewed snapshot paths referenced by approved registry rows. |
| `candidates/` | Cleaned markdown candidates produced from reviewed snapshots before final promotion. | Chunking experiments may use candidates only when the registry row permits review use. |
| `canonical/` | Approved retrieval-ready knowledge material. | Runtime ingestion may read only canonical material with `retrieval_eligible: true`. |
| `reference/` | Supporting material useful for review, citation checks, or evaluation but not yet retrieval-ready. | Runtime ingestion must not read reference material unless a later task promotes it. |
| `archive/` | Superseded, stale, rejected, or replaced material retained for traceability. | Runtime ingestion must not read archive material. |
| `drop/` | Temporary landing area for manual review or experiments. | Runtime ingestion must never read drop material. |

## Source Registry Path

The canonical source registry is:

```text
knowledge_base/registry/source_registry.yaml
```

The registry schema is:

```text
knowledge_base/registry/source_registry.schema.json
```

Registry records control promotion. A file existing under `knowledge_base/` is
not enough to make it ingestible. Runtime ingestion also needs an approved
registry row, `retrieval_eligible: true`, a non-`audit_only` retrieval namespace,
and the required review metadata from the schema.

## Snapshot And Hash Policy

Every source promoted beyond audit-only review must be traceable to a snapshot
or documented acquisition event. Snapshot metadata must include:

- stable `document_id`
- source URI or internal acquisition path
- snapshot date or acquisition date
- content hash and hash algorithm
- source owner and review owner
- license/reuse decision
- registry row linking the snapshot to its promotion state

Snapshots are immutable. If upstream content changes, create a new snapshot ID
and update the registry record rather than overwriting the old snapshot.

## Legacy Boundary

The Phase 1 snapshot remains audit input only:

```text
pilot_phase2_poc/rag-service/legacy/phase1-kb-snapshot/
```

No ingestion, chunking, retrieval, generation, Docker volume, or evaluation task
may read `legacy/` directly as runtime KB input. Legacy files can inform audits,
coverage gaps, and source-shape review, but useful content must be promoted
through the registry, snapshot, candidate, and canonical gates before runtime
use.

## Promotion Flow

```text
legacy audit or external source discovery
-> registry row
-> reviewed snapshot
-> cleaned candidate markdown
-> canonical retrieval-ready material
```

Rejected, stale, or superseded material moves to `archive/`. Temporary manual
inputs belong in `drop/` until reviewed or discarded.
