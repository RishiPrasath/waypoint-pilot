# RAG-DT012 Evidence: Source Snapshot And Canonical Markdown Candidates

Status: In Review
Date: 2026-07-16

## Branch And Worktree

- Branch: `codex/rag-dt012-source-snapshot-and-canonical-markdown-candidates`
- Worktree:
  `C:\tmp\rag-dt012-source-snapshot-and-canonical-markdown-candidates`
- Base commit:
  `d448ce0 Merge pull request #17 from RishiPrasath/codex/rag-dt004-kb-folder-layout`

## Red Check

The initial acceptance check failed because the design artifact did not exist:

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\source-snapshot-and-markdown-candidates.md" -Pattern "snapshot|candidate|lineage|license|hash"
```

Result: expected failure before implementation.

## Source Verification

Official or authoritative source pages used for the first-pass candidates:

- Singapore Customs import permit:
  `https://www.customs.gov.sg/doing-business/import-operations/import-procedures/obtain-a-customs-import-permit/`
- Singapore Customs export permit:
  `https://www.customs.gov.sg/doing-business/export-operations/export-procedures/obtain-customs-export-permit/`
- ASEAN Trade Repository overview:
  `https://atr.asean.org/read/about-asean-trade-repository/22`
- WCO HS Nomenclature 2022 metadata:
  `https://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs-nomenclature-2022-edition/hs-nomenclature-2022-edition.aspx`

## Artifacts Created Or Updated

- `docs/design/source-snapshot-and-markdown-candidates.md`
- `knowledge_base/snapshots/README.md`
- `knowledge_base/snapshots/first-pass-snapshot-manifest.md`
- `knowledge_base/candidates/README.md`
- `knowledge_base/candidates/first-pass/APAC-001-sg-import-permit.md`
- `knowledge_base/candidates/first-pass/APAC-002-sg-export-permit.md`
- `knowledge_base/candidates/first-pass/APAC-201-asean-trade-repository.md`
- `knowledge_base/candidates/first-pass/APAC-215-wco-hs-nomenclature-metadata.md`
- `build-sequence/02-design-tasks/00-index.md`
- `build-sequence/02-design-tasks/03-kb-materialization/RAG-DT012-source-snapshot-and-canonical-markdown-candidates.md`
- `build-sequence/03-build-tasks/00-index.md`
- `build-sequence/03-build-tasks/01-ingestion/RAG-BT008-phase1-kb-audit-artifacts.md`
- `build-sequence/03-build-tasks/01-ingestion/RAG-BT009-chunking-fixture-harness.md`
- `build-sequence/03-build-tasks/01-ingestion/RAG-BT012-fixture-ingestion-pipeline.md`
- `build-sequence/03-build-tasks/03-retrieval/RAG-BT013-semantic-retrieval-baseline.md`
- `build-sequence/03-build-tasks/05-evaluation/RAG-BT019-evaluation-harness.md`

## Candidate Hashes

| Candidate | SHA-256 |
|---|---|
| `APAC-001-sg-import-permit.md` | `4ea671e4bd08e5de9f65fef1365011c7555246f6bc4c8ef357c65a0f3ed20b77` |
| `APAC-002-sg-export-permit.md` | `1ec8a84cf995db694ab27dc71ec85ef9957908b8aeb26e5b51c17b66987f106b` |
| `APAC-201-asean-trade-repository.md` | `ca3a74acc66d99c78630656fca6ebd0ac6367d4cebeecee602a4800cbd189d8e` |
| `APAC-215-wco-hs-nomenclature-metadata.md` | `e62b88ffc8b9f0a6dd8b53b6f4f358f95beddc2383e9b0e14db628c19580c4a6` |

## Checks Run

Passed:

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\source-snapshot-and-markdown-candidates.md" -Pattern "snapshot|candidate|lineage|license|hash"
rg -n "PENDING_HASH" $ServiceRoot
git -C $WorktreePath diff --check
uv run python -m json.tool "$ServiceRoot\knowledge_base\registry\source_registry.schema.json"
uv run python -m pytest -q
```

Results:

- acceptance keyword check returned the DT012 design artifact content
- no `PENDING_HASH` markers remain
- `git diff --check` passed
- source registry schema parsed as valid JSON
- test suite passed: `12 passed in 2.62s`
- governance status/evidence consistency check passed

## PR And Merge

- PR:
- PR CI/CD:
- Main CI/CD:
- Merge commit:
- Cleanup:

## Risks And Follow-Up

- Raw automated page capture remains deferred; DT012 records manual snapshot IDs
  and candidate hashes only.
- `APAC-215` remains metadata-only and must not be chunked or retrieved as
  domain source text.
