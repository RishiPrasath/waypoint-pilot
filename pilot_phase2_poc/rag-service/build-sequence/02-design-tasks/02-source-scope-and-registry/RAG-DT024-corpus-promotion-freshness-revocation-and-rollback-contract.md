# RAG-DT024: Corpus Promotion, Freshness, Revocation, And Rollback Contract

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-DT024` |
| Lane | design |
| Dependencies | `RAG-DT002`, `RAG-DT003`, `RAG-DT004`, `RAG-DT008`, `RAG-DT012`, `RAG-DT021` |
| Blocks | `RAG-DT013`, `RAG-DT022`, non-fixture `RAG-BT009`, non-fixture `RAG-BT012`, non-fixture `RAG-BT013`, `RAG-BT019`, `RAG-BT022` |
| Responsible | Knowledge-base curator |
| Accountable approver | Corpus/data-governance owner |
| Required reviewers | Domain SME, legal/reuse reviewer |
| Branch | `codex/rag-dt024-corpus-lifecycle` |
| Worktree | `C:\tmp\rag-dt024-corpus-lifecycle` |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT024-corpus-lifecycle.md` |

## 1. Objective And Scope

Turn the candidate-source inventory into a governed corpus lifecycle. The
current registry has no retrieval-eligible source, so it cannot support a
runtime-ready or production-ready claim.

Fixtures may continue only in an explicitly named test namespace with
non-authoritative provenance.

## 2. Dependencies And Gates

Use the source audit, registry schema, folder layout, snapshot plan, and
security/trust contract. Any mismatch between API examples, fixtures, and the
registry must be reconciled against the registry as the source of truth.

## 3. Expected Artifacts

```text
docs/design/corpus-promotion-freshness-revocation-and-rollback-contract.md
knowledge_base/registry/promotion-policy.yaml
knowledge_base/registry/corpus-release-manifest.schema.json
knowledge_base/registry/annotation-sidecar.schema.json
docs/operations/corpus-lifecycle-dry-run.md
build-evidence/RAG-DT024-corpus-lifecycle.md
```

## 4. Acceptance Criteria

- Candidate, fixture, canonical, quarantined, revoked, and expired states are
  distinct and machine-validatable.
- Promotion requires source owner, reviewer, provenance, reuse/legal status,
  upstream URI, content hash, effective date, jurisdiction, and quality checks.
- Curator notes, review notes, and workflow metadata are stored separately and
  cannot become answerable chunks or generation context; the annotation
  sidecar is non-chunkable and its exclusion is tested.
- Freshness/reverification SLA, change detection, expiry, revocation, and
  emergency quarantine are defined.
- Corpus releases are immutable/versioned and support rollback and deletion
  from Qdrant plus audit evidence.
- Namespace/collection rules prevent fixture or candidate data from appearing
  as canonical runtime provenance.
- The design-complete gate requires a reviewed lifecycle contract and an
  executed fixture-only promotion/revocation/rollback dry run.
- The non-fixture authorization gate is separate: it requires a reviewed
  `RAG-BT024` corpus release with immutable source hashes, annotation-exclusion
  proof, release manifest, Qdrant deletion/revocation proof, and rollback
  evidence. A design document or dry-run specification alone cannot authorize
  non-fixture ingestion.

## 5. Preflight

Count registry entries by lifecycle and `retrieval_eligible` state. Verify
whether canonical content exists. Search examples and fixtures for eligibility
claims that contradict the registry.

## 6. Red Check

```powershell
Test-Path knowledge_base/registry/promotion-policy.yaml
Test-Path knowledge_base/registry/corpus-release-manifest.schema.json
Test-Path knowledge_base/registry/annotation-sidecar.schema.json
```

Both results must be `False` before implementation.

## 7. Implementation Or Design Work

1. Define lifecycle states and authority.
2. Separate immutable source snapshots, answerable source text, and a
   non-chunkable curator/policy annotation sidecar.
3. Define promotion evidence and dual-review rules.
4. Define freshness, change, expiry, quarantine, and revocation behavior.
5. Define versioned releases, Qdrant namespace/collection mapping, rollback,
   and deletion.
6. Execute and retain evidence for a fixture-only promotion/revocation/rollback
   dry run.
7. Reconcile contradictory examples and fixtures.
7. Update ingestion, retrieval, evaluation, and readiness tasks.

## 8. Verification Matrix

| Check | Required Result |
|---|---|
| Registry truth | Examples and fixtures cannot override lifecycle state |
| Annotation isolation | Curator/review notes cannot become answerable chunks |
| Design gate | Reviewed contract plus executed fixture-only lifecycle dry run exists |
| Non-fixture gate | BT024 release evidence, deletion/revocation, and rollback are reviewed |
| Release | Manifest identifies exact sources, hashes, chunks, embedding, and collection |
| Revocation | Source can be removed from retrieval with audit evidence |
| Rollback | Previous corpus release can be restored deterministically |

## 9. PR Handoff

Report lifecycle states, promotion authority, freshness policy, annotation
isolation, release/version rules, dry-run evidence, and whether the separate
non-fixture authorization gate remains closed.

## 10. Merge And Closeout

Do not mark this complete until candidate-only, fixture-only, and canonical
paths are unambiguous in both documentation and machine-readable artifacts and
the fixture-only dry run has been executed. Completion does not itself open the
separate non-fixture authorization gate.

## 11. Out Of Scope And Deferred Work

Automated crawling and production refresh scheduling may remain deferred.
Corpus authority, annotation isolation, revocation, and rollback may not be
deferred for non-fixture indexing.
