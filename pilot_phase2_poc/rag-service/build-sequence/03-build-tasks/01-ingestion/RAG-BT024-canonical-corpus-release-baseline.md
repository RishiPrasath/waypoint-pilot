# RAG-BT024: Canonical Corpus Release Baseline

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-BT024` |
| Lane | build |
| Dependencies | `RAG-BT007`, `RAG-BT008`, `RAG-DT021`, `RAG-DT024`, `RAG-DT025`, `RAG-DT013` |
| Blocks | non-fixture ingestion/retrieval, canonical evaluation, any production-readiness program |
| Branch | `codex/rag-bt024-canonical-corpus-release` |
| Worktree | `C:\tmp\rag-bt024-canonical-corpus-release` |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT024-canonical-corpus-release.md` |

## 1. Objective And Scope

Promote an owner-approved, immutable, versioned corpus release from audited
candidate sources. This task is not required for explicitly labeled
fixture-only plumbing, but it is mandatory before real/canonical retrieval or
any production-readiness claim.

## 2. Dependencies And Gates

Follow `RAG-DT024` lifecycle rules and `RAG-DT021` source-trust controls. The
registry remains authoritative; examples and test fixtures cannot silently set
`retrieval_eligible=true`.

## 3. Expected Artifacts

```text
knowledge_base/releases/<release-id>/manifest.yaml
knowledge_base/releases/<release-id>/sources/
knowledge_base/registry/source_registry.yaml
docs/reviews/corpus-release-<release-id>.md
build-evidence/RAG-BT024-canonical-corpus-release.md
```

## 4. Acceptance Criteria

- Every promoted source has domain/data-owner review, provenance, reuse/legal
  status, hash, effective date, jurisdiction, and freshness decision.
- Curator/review annotations are excluded from answerable content.
- The immutable release manifest identifies exact source versions, chunks,
  embedding contract, and target Qdrant namespace/collection.
- Machine validation fails on unapproved, expired, revoked, duplicate, or
  annotation-only content.
- Promotion, revocation, Qdrant deletion, and rollback to the prior release are
  dry-run tested with evidence.
- The release is separately labeled from all fixture/candidate namespaces.

## 5. Preflight

Confirm the current registry has no accidentally eligible source and inventory
all example/fixture contradictions before changing lifecycle state.

## 6. Red Check

Write registry/release validation tests first. They must fail because no
approved release manifest and no canonical promoted corpus currently exist.

## 7. Implementation Or Design Work

Perform source-owner review, content normalization with annotation separation,
registry transition, immutable release generation, validation, and
promotion/revocation/rollback dry runs.

## 8. Verification Matrix

| Check | Required Result |
|---|---|
| Approval | Every source has named owner/reviewer and reuse decision |
| Integrity | Source and release hashes validate |
| Isolation | No curator notes or fixture provenance enter the release |
| Lifecycle | Promote, revoke/delete, and rollback dry runs pass |
| Traceability | Release maps sources through chunks to Qdrant namespace |

## 9. PR Handoff

List promoted sources, approvals, exclusions, release ID, hashes, lifecycle
test evidence, and unresolved source gaps.

## 10. Merge And Closeout

Require domain/data-owner and RAG/data review. Do not infer approval from file
presence or earlier candidate status.

## 11. Out Of Scope And Deferred Work

Automated crawling and scheduled refresh may be separate tasks. A canonical
release and rollback evidence are not optional for a production-readiness
program.

## DT013 Final Design Handoff

- Start only after `RAG-DT013` Revision 2 returns `GO`.
- Consume the exact lifecycle, approval, security, namespace, and release
  decisions approved by DT013.
- Update this task before implementation if DT013 changes corpus authority,
  promotion, revocation, or rollback requirements.
