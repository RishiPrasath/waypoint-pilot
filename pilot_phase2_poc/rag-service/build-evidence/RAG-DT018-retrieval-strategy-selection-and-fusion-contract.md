# RAG-DT018 Evidence

Status: Complete
Task: `RAG-DT018`
Branch: `codex/rag-dt018-retrieval-strategy-selection-and-fusion-contract`
Worktree: `C:\tmp\rag-dt018-retrieval-strategy-selection-and-fusion-contract`
Date: 2026-07-18

## Objective

Define the retrieval strategy selection, scoring, and fusion contract required
before `RAG-DT013` can approve retrieval, query API, and evaluation build tasks.

## Artifacts Created

```text
docs/design/retrieval-strategy-and-fusion-contract.md
docs/design/experiments/retrieval-strategy/dt018-run-001/retrieval-scenario-matrix.md
docs/design/experiments/retrieval-strategy/dt018-run-001/scoring-options.md
docs/design/experiments/retrieval-strategy/dt018-run-001/decision-gate.md
build-evidence/RAG-DT018-retrieval-strategy-selection-and-fusion-contract.md
```

## Inputs Reviewed

```text
docs/design/chunking-experiment.md
docs/evaluation/golden-questions.md
docs/design/query-planning/query_planner_rules.yaml
docs/design/query-planning/query_planner_tests.yaml
docs/design/embedding-benchmark-plan.md
docs/design/test-vector-db-ci-strategy.md
docs/design/source-snapshot-and-markdown-candidates.md
docs/design/architecture-sufficiency-review.md
build-sequence/03-build-tasks/03-retrieval/RAG-BT013-semantic-retrieval-baseline.md
build-sequence/03-build-tasks/03-retrieval/RAG-BT014-lexical-hybrid-retrieval.md
build-sequence/03-build-tasks/02-query/RAG-BT018-query-api-endpoint.md
build-sequence/03-build-tasks/05-evaluation/RAG-BT019-evaluation-harness.md
```

## Red Check

Command:

```powershell
$ServiceRoot = Join-Path $WorktreePath "pilot_phase2_poc/rag-service"
Test-Path "$ServiceRoot\docs\design\retrieval-strategy-and-fusion-contract.md"
```

Result before implementation:

```text
False
```

## Decisions Recorded

- Planner output drives retrieval-mode selection.
- No-retrieval planner classes block retrieval before source search.
- Metadata-only/license-sensitive cases do not retrieve answer text.
- Default answerable retrieval path is metadata-filtered hybrid retrieval.
- Exact identifiers, procedure names, article numbers, tariff/HS terms, source
  titles, and source IDs use exact-match boosted hybrid retrieval.
- Semantic baseline remains `BAAI/bge-small-en`, 384 dimensions, cosine.
- Lexical retrieval uses deterministic BM25-style scoring.
- Fusion uses normalized weighted scoring:
  `0.65 semantic + 0.35 lexical`, plus capped exact and metadata boosts.
- Rerank hook is required but no-op initially.
- Low-confidence retrieval blocks generation or produces cautious clarification.

## Verification Commands

Completed before PR handoff:

```powershell
Set-Location "C:\tmp\rag-dt018-retrieval-strategy-selection-and-fusion-contract\pilot_phase2_poc\rag-service"
Test-Path "docs/design/retrieval-strategy-and-fusion-contract.md"
Test-Path "docs/design/experiments/retrieval-strategy/dt018-run-001/retrieval-scenario-matrix.md"
Test-Path "docs/design/experiments/retrieval-strategy/dt018-run-001/decision-gate.md"
Select-String -Path "docs/design/retrieval-strategy-and-fusion-contract.md" -Pattern "RAG-BT013|RAG-BT014|RAG-BT018|RAG-BT019"
uv run python -m pytest -q
git diff --check
```

Results:

```text
contract_exists=True
matrix_exists=True
decision_gate_exists=True
evidence_exists=True
Select-String build-impact references -> RAG-BT013, RAG-BT014, RAG-BT018, RAG-BT019 present
$env:RAG_GROQ_API_KEY = $null; uv run python -m pytest -q -> 12 passed in 0.34s
git diff --check -> passed
```

Note:

```text
The first pytest run was executed while a local Groq key was present in the
shell environment, causing the existing "missing Groq key" configuration test
to fail because the key was intentionally available. The verification rerun
cleared RAG_GROQ_API_KEY and passed.
```

## PR And Merge

PR:
https://github.com/RishiPrasath/waypoint-pilot/pull/47

PR CI/CD:
Passed before merge:

- RAG Service CI: success
- RAG Service CodeQL / Analyze Python: success
- CodeQL: success

Main CI/CD:
Passed after merge commit `7fa1e207698e76da7b5df7ca8340d0a993deb123`:

- RAG Service CI: success
- RAG Service CodeQL / Analyze Python: success

Merge commit:
`7fa1e207698e76da7b5df7ca8340d0a993deb123`

Merged at:
`2026-07-18T07:37:03Z`

Cleanup:

- Local `main` refreshed to merge commit `7fa1e20`.
- DT018 implementation worktree removed:
  `C:\tmp\rag-dt018-retrieval-strategy-selection-and-fusion-contract`
- Local branch deleted:
  `codex/rag-dt018-retrieval-strategy-selection-and-fusion-contract`
- Remote branch deleted:
  `codex/rag-dt018-retrieval-strategy-selection-and-fusion-contract`

Closeout note:
This metadata closeout is recorded on branch `codex/rag-dt018-closeout`.
