# RAG-DT022: Evaluation Validity And Adversarial Test Contract

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-DT022` |
| Lane | design |
| Dependencies | `RAG-DT005`, `RAG-DT006`, `RAG-DT010`, `RAG-DT017`, `RAG-DT021`, `RAG-DT024` |
| Blocks | `RAG-DT013`, reopened `RAG-DT015`, reopened `RAG-DT018`, reopened `RAG-DT019`, reopened `RAG-DT020`, `RAG-BT013`, `RAG-BT014`, `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, `RAG-BT019`, `RAG-BT022` |
| Responsible | Evaluation/QA owner |
| Accountable approver | Service owner |
| Required reviewers | Independent domain adjudicator, RAG lead |
| Branch | `codex/rag-dt022-evaluation-validity` |
| Worktree | `C:\tmp\rag-dt022-evaluation-validity` |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT022-evaluation-validity.md` |

## 1. Objective And Scope

Replace the current smoke-fixture evidence with a statistically defensible,
reproducible evaluation contract for retrieval, generation, citation support,
refusal behavior, safety, latency, and reliability.

The existing 10-chunk, 8-positive-query / 14-total-case evidence remains useful
as a development smoke fixture. It must not be used alone to claim that a
model, fusion strategy, confidence threshold, or end-to-end service is ready.

## 2. Dependencies And Gates

This task consumes the corpus lifecycle and security contracts. The historical
DT015/DT018/DT019/DT020 artifacts are review inputs, not gating dependencies.
This task's result must drive their reopened revisions.

## 3. Expected Artifacts

```text
docs/design/evaluation-validity-and-adversarial-test-contract.md
docs/evaluation/dataset-manifest.yaml
docs/evaluation/scoring-and-adjudication-rubric.md
docs/evaluation/statistical-acceptance-gates.yaml
tools/evaluation/run_reproducibility.py
tests/evaluation/test_reproducibility_contract.py
docs/evaluation/runs/<run-id>/run-manifest.yaml
docs/evaluation/runs/<run-id>/raw-results.jsonl
docs/evaluation/runs/<run-id>/scores.jsonl
docs/evaluation/runs/<run-id>/adjudication.jsonl
docs/evaluation/runs/<run-id>/report.md
build-evidence/RAG-DT022-evaluation-validity.md
```

## 4. Acceptance Criteria

- Development, calibration, and held-out sets are separate, versioned, and
  split at source/document-family level to prevent leakage.
- Dataset coverage includes paraphrases, near-negatives, mixed intent,
  multilingual/APAC variants, stale/conflicting sources, missing evidence,
  indirect injection, poisoned chunks, and malformed provider output.
- Human adjudication guidance defines answer correctness, claim support,
  citation precision/recall, false refusal, unsafe answer, and ambiguity.
- Claim-to-evidence evaluation uses claim IDs and supporting chunk/span
  references; document identity alone is not accepted as factual support.
- LLM judges, if used, are calibrated against humans, version-pinned, and not
  the sole judge of their own model family.
- Repeated runs, sample sizes, seeds/temperature, uncertainty/confidence
  reporting, and failure handling are explicit.
- Absolute pass/fail gates are pre-registered before tuning; a relative
  baseline may be reported but cannot be the only criterion.
- Retrieval comparison covers semantic-only, lexical-only, RRF/DBSF, and
  weighted fusion; tuning uses calibration data and final measurement uses
  held-out data.
- Confidence calibration uses absolute evidence and source agreement, not only
  per-query normalized ranks.
- The canonical loader, scorer, and their tests have declared paths and a run
  manifest records dataset hashes, split version, prompt/model versions,
  parameters, seeds, raw outputs, scores, adjudication, and report inputs.

## 5. Preflight

Inventory every case reused by DT010, DT015, DT018, and DT020. Record all
sources, chunks, prompts, scorers, model versions, and selection decisions that
have already seen those cases.

## 6. Red Check

```powershell
Test-Path docs/evaluation/dataset-manifest.yaml
Test-Path docs/evaluation/statistical-acceptance-gates.yaml
```

Both results must be `False` before implementation.

## 7. Implementation Or Design Work

1. Label the existing golden set as a smoke/development fixture.
2. Define independent dataset splits and source-level leakage controls.
3. Declare the canonical loader/scorer/test locations, then define adjudication
   and judge-calibration procedures.
4. Define component and end-to-end metrics with absolute gates.
5. Add adversarial, poisoned, stale, conflicting, and multilingual coverage.
6. Define repeated-run and uncertainty reporting.
7. Execute a small reproducibility run and retain its immutable manifest,
   outputs, scores, adjudication, and report.
8. Re-run or reopen the decisions that were selected on the smoke fixture.

## 8. Verification Matrix

| Check | Required Result |
|---|---|
| Leakage audit | No held-out source or case informed tuning/selection |
| Reproducibility | Dataset, scorer, prompt, model, parameters, and seed are versioned |
| Executable reproduction | `uv run pytest tests/evaluation/test_reproducibility_contract.py -q`; `uv run python tools/evaluation/run_reproducibility.py --run-id <run-id>` | Both pass and generate the retained run artifacts |
| Run evidence | Immutable manifest links hashes, raw output, scores, adjudication, and report |
| Attribution | Claim-to-span support is measurable |
| Adversarial coverage | Indirect injection and poisoning have explicit success-rate gates |
| Statistical gate | Sample size and uncertainty are reported with absolute thresholds |

## 9. PR Handoff

Report dataset composition, leakage controls, judge calibration, absolute
gates, reopened decisions, and task impact.

## 10. Merge And Closeout

Do not close this task on schema presence alone. Require a small reproducibility
run that demonstrates the declared dataset loader, scorer, tests, and report
format, with the expected run artifacts retained.

## 11. Out Of Scope And Deferred Work

Large-scale online evaluation may remain deferred. Held-out validity,
adversarial coverage, and reproducible scoring may not be waived for an
end-to-end readiness claim.
