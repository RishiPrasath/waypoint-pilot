# RAG-DT004 Evidence

Status: Complete

## Identity

Task: `RAG-DT004` KB folder layout and registry storage
Branch: `codex/rag-dt004-kb-folder-layout`
Worktree: `C:\tmp\rag-dt004-kb-folder-layout`
Starting main commit: `bc79605f535670c969dc5b2aa3a24a7cb5436a38`
PR: Pending PR creation
Implementation commit: Pending local commit
Merge commit: Pending merge

## Artifacts

- `pilot_phase2_poc/rag-service/knowledge_base/README.md`
- `pilot_phase2_poc/rag-service/build-sequence/02-design-tasks/03-kb-materialization/RAG-DT004-kb-folder-layout.md`
- `pilot_phase2_poc/rag-service/build-sequence/02-design-tasks/00-index.md`
- `pilot_phase2_poc/rag-service/build-sequence/03-build-tasks/00-index.md`
- `pilot_phase2_poc/rag-service/build-sequence/03-build-tasks/01-ingestion/RAG-BT007-source-registry-validation.md`
- `pilot_phase2_poc/rag-service/build-sequence/03-build-tasks/01-ingestion/RAG-BT008-phase1-kb-audit-artifacts.md`
- `pilot_phase2_poc/rag-service/build-sequence/03-build-tasks/01-ingestion/RAG-BT009-chunking-fixture-harness.md`
- `pilot_phase2_poc/rag-service/build-sequence/03-build-tasks/01-ingestion/RAG-BT012-fixture-ingestion-pipeline.md`
- `pilot_phase2_poc/rag-service/build-sequence/03-build-tasks/05-evaluation/RAG-BT019-evaluation-harness.md`
- `pilot_phase2_poc/rag-service/build-sequence/03-build-tasks/06-ops-readiness/RAG-BT020-docker-local-run.md`

## Accepted KB Contract

- Registry: `knowledge_base/registry/source_registry.yaml`
- Registry schema: `knowledge_base/registry/source_registry.schema.json`
- Snapshots: `knowledge_base/snapshots/`
- Cleaned candidates: `knowledge_base/candidates/`
- Canonical retrieval material: `knowledge_base/canonical/`
- Review/reference material: `knowledge_base/reference/`
- Superseded or rejected material: `knowledge_base/archive/`
- Temporary untrusted intake: `knowledge_base/drop/`
- Legacy audit input only: `legacy/phase1-kb-snapshot/`

## Checks Run

- `Select-String -Path knowledge_base/README.md -Pattern "registry|canonical|reference|archive|snapshots"` -> matched required folder terms.
- `uv run python -m pytest -q` -> 12 passed in 0.76s.
- `git diff --check` -> no whitespace errors.
- `uv run python -m json.tool knowledge_base/registry/source_registry.schema.json` -> schema JSON parsed successfully.

## CI And Review

Pending PR creation.

## Issues And Recovery

- Existing `knowledge_base/README.md` was a placeholder, so this task created the first explicit KB folder contract.
- Empty reserved folders were documented but not created because Git does not preserve empty directories and later tasks should create folders when they first write reviewed material.

## Follow-ups

- `RAG-DT012` must define the first snapshot and canonical markdown candidate materialization plan.
- `RAG-DT013` must confirm all affected build task files remain aligned before runtime build work starts.
