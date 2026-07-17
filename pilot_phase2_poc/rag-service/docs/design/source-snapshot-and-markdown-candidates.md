# Source Snapshot And Markdown Candidate Plan

Status: Accepted for `RAG-DT012`
Date: 2026-07-16

This design defines how registered sources become source-derived canonical
markdown candidates for review, chunking experiments, and later ingestion.

It does not approve production scraping, final ingestion, embedding, indexing,
or retrieval eligibility.

## Scope

The Phase 2 RAG knowledge base now has a fixed folder contract from
`RAG-DT004`:

```text
knowledge_base/
  registry/
  snapshots/
  candidates/
  canonical/
  reference/
  archive/
  drop/
```

`RAG-DT012` fills the next design gap: how a source row in
`knowledge_base/registry/source_registry.yaml` becomes a reviewed snapshot and
then a cleaned markdown candidate.

## First Materialization Pass

The first pass is intentionally small. It selects sources that cover different
materialization risks without ingesting the full APAC registry.

| Document ID | Source | Namespace | Reuse mode | First-pass treatment |
|---|---|---|---|---|
| `APAC-001` | Singapore Customs import permit procedure | `regulatory` | `cite_and_summarize` | Manual snapshot metadata and cleaned markdown candidate |
| `APAC-002` | Singapore Customs export permit procedure | `regulatory` | `cite_and_summarize` | Manual snapshot metadata and cleaned markdown candidate |
| `APAC-201` | ASEAN Trade Repository overview | `regulatory` | `cite_and_summarize` | Manual snapshot metadata and cleaned markdown candidate |
| `APAC-215` | WCO HS Nomenclature 2022 Edition | `reference` | `cite_only` | Metadata-only candidate to prove license-sensitive handling |

These candidates are representative enough for `RAG-BT009` chunking
experiments because they include:

- public government procedure pages
- an intergovernmental regional index page
- a license-sensitive reference source that must not be copied into retrieval
  text

## Legacy Boundary

Legacy Phase 1 files remain historical audit input only:

```text
pilot_phase2_poc/rag-service/legacy/phase1-kb-snapshot/
```

Legacy files may be used to compare coverage gaps, document shapes, and earlier
source assumptions. They are not raw Phase 2 snapshots, and they must not become
runtime ingestion inputs unless a later task promotes the underlying authority
through the registry, snapshot, candidate, and canonical gates.

## Snapshot Policy

Snapshots represent captured source state. A raw snapshot must be immutable and
must have a row in the snapshot manifest.

Minimum snapshot metadata:

- `document_id`
- `snapshot_id`
- `source_uri`
- `source_owner`
- `snapshot_date`
- `last_verified_date`
- `source_access_pattern`
- `source_status`
- `promotion_status`
- `retrieval_eligible`
- `retrieval_namespace`
- `reuse_mode`
- `license_sensitive`
- `content_hash`
- `hash_algorithm`
- `candidate_path`, when a cleaned candidate exists

For this design pass, snapshots are represented by
`knowledge_base/snapshots/first-pass-snapshot-manifest.md`. The manifest is the
review boundary; production scraping automation is out of scope.

## Candidate Rules

Cleaned markdown candidates live under:

```text
knowledge_base/candidates/first-pass/
```

Each candidate must include:

- frontmatter with source lineage
- source URL and source owner
- snapshot ID
- candidate status
- retrieval eligibility status
- license and reuse status
- source-derived notes or metadata
- clear warning when content is metadata-only or cite-only

Candidate text must be source-derived. It can paraphrase, summarize, or point
to official source metadata according to `reuse_mode`. It must not invent
regulatory obligations, filing steps, deadlines, permit conditions, tariff
treatment, or legal conclusions.

## Copied Text Versus Source-Derived Notes

`cite_and_summarize` sources may be summarized into short review notes when the
candidate records lineage and links to the source.

`cite_only` and `do_not_ingest` sources must not have substantive source text
copied into a candidate. For those sources, candidates should be metadata-only
and should explain why the source is excluded from retrieval text.

## License-Sensitive Handling

`license_sensitive: true` requires one of these treatments:

- metadata-only candidate
- link-only reference
- explicit review before any full-text snapshot or candidate is created
- exclusion from runtime ingestion until reuse approval is recorded

The WCO and ICC classes of sources are treated conservatively. A source may be
authoritative and still not be ingestible.

## Hash Policy

The first-pass candidate files are hashed in the snapshot manifest using
SHA-256. The hash covers the local candidate file as committed, not the
upstream webpage. Later production snapshot tasks may add raw HTML/PDF hashes
once acquisition automation and storage rules are approved.

If candidate content changes, the manifest hash must be updated in the same
commit.

## Candidate Documents

The first-pass candidate files are:

```text
knowledge_base/candidates/first-pass/APAC-001-sg-import-permit.md
knowledge_base/candidates/first-pass/APAC-002-sg-export-permit.md
knowledge_base/candidates/first-pass/APAC-201-asean-trade-repository.md
knowledge_base/candidates/first-pass/APAC-215-wco-hs-nomenclature-metadata.md
```

Only the first three are cleaned markdown candidates for future review and
chunking experiments. `APAC-215` is deliberately metadata-only to test
license-sensitive exclusion behavior.

## Build Task Impact

`RAG-BT008` should keep Phase 1 material audit-only and align audit outputs with
the manifest and candidate lineage.

`RAG-BT009` should use the first-pass candidate folder as the chunking fixture
source. It must exclude metadata-only, archive, drop, reference-only, and legacy
materials from runtime chunking fixtures.

`RAG-BT012` should ingest only approved fixture candidates and must trace every
fixture back to registry and snapshot manifest metadata.

`RAG-BT013` should use chunk IDs, source IDs, candidate paths, and content
hashes from this materialization plan when building the semantic retrieval
baseline.

`RAG-BT019` should use these candidates as citation and source-lineage examples
until the golden-question task defines a broader evaluation fixture set.

## Deferred Work

- production scraping automation
- raw HTML/PDF snapshot storage
- full canonical promotion into `knowledge_base/canonical/`
- embedding and vector indexing
- legal approval for cite-only or do-not-ingest source classes
