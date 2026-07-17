# RAG-DT005 Evidence: Chunking Experiment

Status: In Review
Date: 2026-07-17

## Branch And Worktree

- Branch: `codex/rag-dt005-chunking-experiment`
- Worktree: `C:\tmp\rag-dt005-chunking-experiment`
- Base commit:
  `8300ef7 Merge pull request #18 from RishiPrasath/codex/rag-dt012-source-snapshot-and-canonical-markdown-candidates`

## Red Check

The initial acceptance check should fail before implementation because the
design artifact does not exist:

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\chunking-experiment.md" -Pattern "chosen strategy|metadata|rejected|retrieval impact"
```

Result: expected missing-artifact failure before DT005 work.

## Experiment Run

- Run ID: `dt005-run-001`
- Queue: `local_design_experiment`
- Runner:
  `docs/design/experiments/chunking/dt005-run-001/run_chunking_experiment.py`
- Source manifest:
  `knowledge_base/snapshots/first-pass-snapshot-manifest.md`

Generated artifacts:

- `docs/design/experiments/chunking/dt005-run-001/queue-manifest.json`
- `docs/design/experiments/chunking/dt005-run-001/chunks-fixed-window-baseline.jsonl`
- `docs/design/experiments/chunking/dt005-run-001/chunks-structure-aware-v1.jsonl`
- `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl`
- `docs/design/experiments/chunking/dt005-run-001/comparison-report.md`

## Queue Result

| Document ID | Status | Reason |
|---|---|---|
| `APAC-001` | `reported` | chunk outputs generated |
| `APAC-002` | `reported` | chunk outputs generated |
| `APAC-201` | `reported` | chunk outputs generated |
| `APAC-215` | `skipped` | metadata-only or license-sensitive source |

## Strategy Result

| Strategy | Result |
|---|---|
| `hybrid_structure_recursive_v1` | Chosen |
| `structure_aware_v1` | Retained as structure-only comparison |
| `fixed_window_baseline_v1` | Rejected as default; retained as comparison baseline |

## Hash Verification Finding

The runner records both normalized text SHA-256 and raw checkout SHA-256.
Normalized text SHA-256 matches the DT012 manifest. Raw checkout SHA-256 can
differ on Windows because Git may check out markdown files with CRLF line
endings.

Accepted implication: future markdown ingestion hash checks should normalize
line endings before comparing against manifest hashes.

## Files Created Or Updated

- `docs/design/chunking-experiment.md`
- `docs/design/experiments/chunking/dt005-run-001/run_chunking_experiment.py`
- `docs/design/experiments/chunking/dt005-run-001/queue-manifest.json`
- `docs/design/experiments/chunking/dt005-run-001/chunks-fixed-window-baseline.jsonl`
- `docs/design/experiments/chunking/dt005-run-001/chunks-structure-aware-v1.jsonl`
- `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl`
- `docs/design/experiments/chunking/dt005-run-001/comparison-report.md`
- `build-sequence/02-design-tasks/00-index.md`
- `build-sequence/02-design-tasks/04-chunking-and-evaluation-design/RAG-DT005-chunking-experiment.md`
- `build-sequence/03-build-tasks/00-index.md`
- `build-sequence/03-build-tasks/01-ingestion/RAG-BT009-chunking-fixture-harness.md`
- `build-sequence/03-build-tasks/01-ingestion/RAG-BT012-fixture-ingestion-pipeline.md`
- `build-sequence/03-build-tasks/03-retrieval/RAG-BT013-semantic-retrieval-baseline.md`
- `build-sequence/03-build-tasks/03-retrieval/RAG-BT014-lexical-hybrid-retrieval.md`
- `build-sequence/03-build-tasks/05-evaluation/RAG-BT019-evaluation-harness.md`

## Checks Run

Passed:

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\chunking-experiment.md" -Pattern "chosen strategy|metadata|rejected|retrieval impact"
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\chunking-experiment.md" -Pattern "run_id|queue-manifest|jsonl|hash_verified"
uv run python -m json.tool docs/design/experiments/chunking/dt005-run-001/queue-manifest.json
uv run python docs/design/experiments/chunking/dt005-run-001/run_chunking_experiment.py
git -C $WorktreePath diff --check
uv run python -m pytest -q
```

Results:

- acceptance keyword checks passed
- `queue-manifest.json` is valid JSON
- `chunks-fixed-window-baseline.jsonl`: 8 valid JSONL records
- `chunks-structure-aware-v1.jsonl`: 9 valid JSONL records
- `chunks-hybrid-structure-recursive-v1.jsonl`: 10 valid JSONL records
- queue counts: 3 reported, 1 skipped
- `APAC-215` skipped as metadata-only/license-sensitive
- `git diff --check` passed
- test suite passed: `12 passed in 2.99s`
- governance status/evidence consistency check passed

## PR And Merge

- PR:
- PR CI/CD:
- Main CI/CD:
- Merge commit:
- Cleanup:

## Risks And Follow-Up

- Production queue backend remains deferred.
- Production worker process remains deferred.
- Broader table-heavy, FAQ, and bilingual examples require additional approved
  Phase 2 candidates.
