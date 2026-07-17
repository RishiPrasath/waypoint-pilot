# RAG-DT006 Evidence

Task: Define Golden Questions And Answer Rubrics

Branch: `codex/rag-dt006-golden-questions`
Worktree: `C:\tmp\rag-dt006-golden-questions`
Base: `origin/main` at `166f1b8`

## Red Check

Initial acceptance checks failed because the required files did not exist:

```text
docs/evaluation/golden-question-research-findings.md
docs/evaluation/golden-questions.md
```

## Research References

- https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/
- https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/
- https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/
- https://docs.langchain.com/langsmith/evaluate-rag-tutorial
- https://docs.langchain.com/langsmith/evaluation-approaches
- https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/rag-evaluators
- https://www.braintrust.dev/articles/what-is-rag-evaluation
- https://qdrant.tech/blog/rag-evaluation-guide/

## Source Inputs Reviewed

- `docs/design/source-snapshot-and-markdown-candidates.md`
- `docs/design/chunking-experiment.md`
- `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl`
- `knowledge_base/candidates/first-pass/APAC-001-sg-import-permit.md`
- `knowledge_base/candidates/first-pass/APAC-002-sg-export-permit.md`
- `knowledge_base/candidates/first-pass/APAC-201-asean-trade-repository.md`
- `knowledge_base/candidates/first-pass/APAC-215-wco-hs-nomenclature-metadata.md`
- `build-sequence/03-build-tasks/05-evaluation/RAG-BT019-evaluation-harness.md`
- `build-sequence/03-build-tasks/03-retrieval/RAG-BT013-semantic-retrieval-baseline.md`
- `build-sequence/03-build-tasks/03-retrieval/RAG-BT014-lexical-hybrid-retrieval.md`
- `build-sequence/03-build-tasks/02-query/RAG-BT018-query-api-endpoint.md`

## Artifacts Created

- `docs/evaluation/golden-question-research-findings.md`
- `docs/evaluation/golden-questions.md`

## Affected Build Task Updates

- `RAG-BT013`: semantic retrieval should use selected positive golden questions as fixture expectations.
- `RAG-BT014`: lexical/hybrid retrieval should use the same expected chunks for parity.
- `RAG-BT018`: query API should validate safe responses for negative golden cases.
- `RAG-BT019`: evaluation harness should load the golden question file and report retrieval, answer, citation, refusal, irrelevant, and malicious-case results separately.

## Verification

Final acceptance checks passed.

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\evaluation\golden-question-research-findings.md" -Pattern "retrieval|answer quality|groundedness|citation|refusal|malicious|candidate assessment"
```

Matched required research, retrieval, answer quality, groundedness, citation,
refusal, malicious, and candidate assessment terms.

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\evaluation\golden-questions.md" -Pattern "rubric|citation|approved_source|order status|partner-source|malicious"
```

Matched required rubric, citation, approved_source, order status,
partner-source, and malicious terms.

Additional scan confirmed:

- selected positive cases `GQ-001` through `GQ-008`
- required negative/exclusion cases `GQ-009` through `GQ-014`
- source coverage for `APAC-001`, `APAC-002`, `APAC-201`, and `APAC-215`
- `hybrid_structure_recursive_v1` chunk strategy expectations
- legacy/drop/archive citation guardrail

## PR / CI / Merge

PR: https://github.com/RishiPrasath/waypoint-pilot/pull/21
PR CI/CD: pending
Main CI/CD:
Merge commit:
Cleanup:

## Risks And Deferred Work

- The first golden set is intentionally small and limited to first-pass DT012 candidates.
- `APAC-215` is metadata-only and must remain an exclusion case, not answer content.
- Broader APAC source and country-specific legal/tariff questions should wait for additional approved source materialization.
