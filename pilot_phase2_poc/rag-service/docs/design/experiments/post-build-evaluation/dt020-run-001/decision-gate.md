# Decision Gate: Post-Build Evaluation and Tuning (DT020)

## Gate Inputs

- Run artifacts from `dt020-run-001` and all required metrics.
- Failure taxonomy classification.
- Remediation mapping and next-task outputs.

## Pass Criteria

- No mandatory metric regression.
- No unresolved P0/P1 safety or correctness failure.
- `RAG-BT019`, `RAG-BT022` report expectations are mapped into artifacts.
- Decision is recorded as one of:
  - `GO` (Baseline accepted)
  - `GO_WITH_CONDITIONAL` (explicit risk acceptance required)
  - `HOLD` (follow-up work required before build impact review)

## Gate Decisions

- `GO`: proceed to build-impact review planning (DT013) with updated references.
- `GO_WITH_CONDITIONAL`: proceed with documented owner-signed risk and a date for recheck.
- `HOLD`: stop progression and create a follow-up task before final build work can begin.

## RAG-BT019 and RAG-BT022 Linkage

- `RAG-BT019` must produce:
  - unit-mocked metrics,
  - qdrant-backed metrics,
  - LLM-judge metrics (if key configured).
- `RAG-BT022` must consume and confirm readiness posture before declaring production-readiness gating closed.
