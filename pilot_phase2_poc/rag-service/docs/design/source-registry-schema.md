# Source Registry Schema

Status: Draft for `RAG-DT008`; updated by `RAG-DT003` for source-owner
capture and standards-body authority classification.
Schema artifact: `knowledge_base/registry/source_registry.schema.json`

## Purpose

The source registry schema defines the minimum record contract for Phase 2 RAG
source review. It allows legacy Phase 1 audit material to be tracked without
making that material ingestible or retrievable by default.

The registry is a governance boundary, not a content promotion decision. A
record may exist for traceability while `retrieval_eligible` remains `false`.

## Required fields

| Field | Meaning |
|---|---|
| `document_id` | Stable source ID used for audits, citations, chunks, and promotion decisions. |
| `source_uri` | Canonical source URL, legacy path, internal path, or acquisition note. |
| `title` | Human-readable source title. |
| `source_owner` | Organization responsible for publishing or owning the source. This is separate from `review_owner`, which is the internal approval owner. |
| `source_type` | Source classification, such as regulatory, reference, carrier candidate, internal, metadata, or derivative. |
| `authority_level` | Trust class used to identify review requirements and source precedence. |
| `source_status` | Lifecycle state of the source record. |
| `promotion_status` | Whether the source has passed source-review promotion gates. |
| `retrieval_eligible` | Explicit gate controlling whether ingestion and retrieval may use the source. |
| `retrieval_namespace` | Retrieval namespace for promoted material, or `audit_only` for non-ingestible records. |
| `jurisdiction` | Jurisdiction or scope, such as `SG`, `ASEAN`, `Global`, or `Internal`. |
| `language` | Source language code. |
| `source_access_pattern` | How the source is acquired or refreshed. |
| `translation_review_required` | Whether translation review is required before promotion. |
| `dynamic_lookup_snapshot` | Whether the source is a snapshot of normally dynamic data. |
| `legal_disclaimer` | Required disclaimer or safety note for use in answers. |
| `license_sensitive` | Whether copyright, licensing, or publisher terms constrain reuse. |
| `reuse_mode` | Allowed reuse pattern for ingestion, summarization, and citations. |

## Allowed statuses

`authority_level` includes government, intergovernmental, standards-body,
carrier, internal, secondary-reference, metadata-only, and unverified authority
classes. `standards_body` is used for official standards publishers such as ICC
where the source is authoritative for its own standard but is not a government
or intergovernmental source.

`source_status` values:

- `audit_only`
- `candidate`
- `under_review`
- `approved`
- `blocked`
- `rejected`
- `replaced`
- `stale`

`promotion_status` values:

- `legacy_audit`
- `candidate`
- `needs_review`
- `approved`
- `rejected`
- `superseded`

## Retrieval eligibility rules

A source may set `retrieval_eligible` to `true` only when all of the following
are true:

- `source_status` is `approved`
- `promotion_status` is `approved`
- `retrieval_namespace` is not `audit_only`
- `reuse_mode` allows ingestion and summarization
- `snapshot_date` is present
- `last_verified_date` is present
- `review_owner` is present

The schema rejects retrieval eligibility for audit-only, candidate, under-review,
blocked, rejected, replaced, or stale source records.

The schema also rejects retrieval eligibility for `legacy_audit`,
`candidate`, `needs_review`, `rejected`, or `superseded` promotion records.

## Promotion gates

Promotion requires explicit review evidence. A registry record should not be
approved until the source has:

- stable source ID
- verified authority
- verified currentness or snapshot date
- source URL or documented acquisition path
- source owner
- review owner
- jurisdiction and language metadata
- reuse and licensing decision
- namespace decision

Legacy rows from `legacy/phase1-kb-snapshot/` must default to
`retrieval_eligible: false` until later source review and KB materialization
tasks promote them.

## Carrier boundary

Carrier sources are represented as `public_carrier_candidate` records. They may
only use `audit_only` or `carrier_reference` namespaces.

Carrier records must not answer live shipment status, assignment, ETA, timeline,
or delivery-event questions. Those facts belong to `partner-source` through the
future orchestration layer, not this RAG registry.

Carrier content may become retrievable only after an explicit static
carrier-reference use case is approved and provenance, freshness, citation, and
non-operational-answer boundaries are recorded.

## Validation failure behavior

Runtime validator code is out of scope for `RAG-DT008`, but future validators
must treat schema failures as hard failures for ingestion. Validation reports
should include:

- `document_id`, when available
- JSON path of the failing field
- failed rule or enum
- clear failure message

Records that fail validation, contain unknown required values, or cannot be
parsed must be treated as `retrieval_eligible: false`.

## Validation examples

Valid examples are embedded in the schema:

- legacy regulatory candidate, non-retrieval-eligible
- legacy carrier audit row, non-retrieval-eligible
- approved regulatory source, retrieval-eligible

Invalid examples verified during design:

- candidate source with `retrieval_eligible: true`
- carrier source assigned to `regulatory` namespace
