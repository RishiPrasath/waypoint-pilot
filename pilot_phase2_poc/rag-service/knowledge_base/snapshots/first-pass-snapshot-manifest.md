# First-Pass Snapshot Manifest

Status: Accepted for RAG-DT012
Date: 2026-07-16
Task: `RAG-DT012`

This manifest records the manual first-pass source snapshots and cleaned
markdown candidates selected for review and chunking experiments.

| Document ID | Snapshot ID | Source URI | Candidate path | Reuse mode | License sensitive | Retrieval eligible | Candidate SHA-256 |
|---|---|---|---|---|---|---|---|
| `APAC-001` | `snap-20260716-apac-001` | `https://www.customs.gov.sg/doing-business/import-operations/import-procedures/obtain-a-customs-import-permit/` | `knowledge_base/candidates/first-pass/APAC-001-sg-import-permit.md` | `cite_and_summarize` | `false` | `false` | `4ea671e4bd08e5de9f65fef1365011c7555246f6bc4c8ef357c65a0f3ed20b77` |
| `APAC-002` | `snap-20260716-apac-002` | `https://www.customs.gov.sg/doing-business/export-operations/export-procedures/obtain-customs-export-permit/` | `knowledge_base/candidates/first-pass/APAC-002-sg-export-permit.md` | `cite_and_summarize` | `false` | `false` | `1ec8a84cf995db694ab27dc71ec85ef9957908b8aeb26e5b51c17b66987f106b` |
| `APAC-201` | `snap-20260716-apac-201` | `https://atr.asean.org/read/about-asean-trade-repository/22` | `knowledge_base/candidates/first-pass/APAC-201-asean-trade-repository.md` | `cite_and_summarize` | `false` | `false` | `ca3a74acc66d99c78630656fca6ebd0ac6367d4cebeecee602a4800cbd189d8e` |
| `APAC-215` | `snap-20260716-apac-215` | `https://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs-nomenclature-2022-edition/hs-nomenclature-2022-edition.aspx` | `knowledge_base/candidates/first-pass/APAC-215-wco-hs-nomenclature-metadata.md` | `cite_only` | `true` | `false` | `e62b88ffc8b9f0a6dd8b53b6f4f358f95beddc2383e9b0e14db628c19580c4a6` |

## Notes

- `retrieval_eligible` remains `false` for every first-pass source.
- This manifest hashes local candidate files, not upstream source pages.
- Raw upstream page capture is deferred until production snapshot automation is
  approved.
- `APAC-215` is metadata-only and must not be chunked as source text.
