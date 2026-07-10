# Phase 1 KB Snapshot Audit Notice

The copied snapshot is stored at:

```text
pilot_phase2_poc/rag-service/legacy/phase1-kb-snapshot/
```

It was copied from:

```text
C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase1_poc\05_evaluation\kb
```

It exists so Phase 2 design tasks can inspect the earlier KB for source quality,
scope fit, metadata shape, chunking behavior, and evaluation examples.

Rules:

- Treat `phase1-kb-snapshot/` as legacy audit input only.
- Do not treat any file in the snapshot as canonical Phase 2 retrieval content.
- Do not point ingestion tasks or runtime code at the snapshot.
- Do not promote carrier marketing, synthetic SOPs, or unreviewed PDF extracts
  into the canonical KB without explicit audit evidence.
- Any useful material must be reviewed through the source audit and promoted
  into the new Phase 2 KB structure by a design decision.

Primary design tasks that may use this snapshot:

- `RAG-DT002`: Phase 1 KB source audit
- `RAG-DT004`: KB folder layout and legacy boundary confirmation
- `RAG-DT005`: chunking experiment source-shape review
- `RAG-DT006`: golden question and expected-source review
- `RAG-DT008`: source registry schema examples
- `RAG-DT012`: source snapshot and canonical markdown candidate plan
- `RAG-DT013`: final build task impact review

