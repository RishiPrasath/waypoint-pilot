# RAG-DT009 Evidence

Status: Complete
Task: Define LLM Model Evaluation Fixture

Branch: `codex/rag-dt009-llm-model-evaluation-fixture`
Worktree: `C:\tmp\rag-dt009-llm-model-evaluation-fixture`
Base: `origin/main` at `659b81d`

## Red Check

Initial acceptance checks failed because the required DT009 artifacts did not
exist:

```text
docs/design/llm-model-evaluation-plan.md
docs/design/experiments/llm-model-evaluation/model-inventory.schema.json
docs/design/experiments/llm-model-evaluation/model-capability-review.md
docs/design/experiments/llm-model-evaluation/model-evaluation-runbook.md
```

## Inputs Reviewed

- `build-sequence/00-index.md`
- `build-sequence/02-design-tasks/00-index.md`
- `build-sequence/02-design-tasks/05-runtime-technical-design/RAG-DT009-llm-model-evaluation-fixture.md`
- `docs/evaluation/golden-questions.md`
- `docs/design/experiments/chunking/dt005-run-001/comparison-report.md`
- `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl`
- `docs/design/query-planning/planner_vocabulary.json`
- `docs/design/source-snapshot-and-markdown-candidates.md`
- affected build tasks `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, and `RAG-BT019`

## Artifacts Created

- `docs/design/llm-model-evaluation-plan.md`
- `docs/design/experiments/llm-model-evaluation/model-inventory.schema.json`
- `docs/design/experiments/llm-model-evaluation/model-capability-review.md`
- `docs/design/experiments/llm-model-evaluation/model-evaluation-runbook.md`

## Design Decisions

- Provider endpoint and API key collection must happen before API-backed
  discovery and must use environment variables only.
- `/models` inventory is required but is not treated as sufficient capability
  evidence.
- A model capability/specification review must happen before model assessment.
- Unknown model capabilities remain `unknown` until backed by provider metadata,
  docs, model cards, comparison pages, or owner-approved probes.
- The first assessment should use a small include/defer/exclude shortlist,
  rather than testing every provider model ID.
- DT006 golden questions, DT005 hybrid chunks, DT007 planner classifications,
  and DT012 lineage form the required fixture basis.
- Final model lock remains out of scope until evaluation evidence exists.

## Affected Build Task Updates

- `RAG-BT016`: must implement adapter settings around DT009 inventory,
  shortlist, timeout, and no-secrets provider configuration assumptions.
- `RAG-BT017`: must validate schema, citation, retry/fallback, and safety
  behavior in line with the DT009 scoring rubric.
- `RAG-BT018`: must preserve planner, retrieval, generation, citation, and
  safety fields needed by DT009 evaluation.
- `RAG-BT019`: must implement the evaluation harness from DT009 fixture design.

## Verification

Acceptance checks passed:

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\llm-model-evaluation-plan.md" -Pattern "quality|latency|schema|citation"
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\llm-model-evaluation-plan.md" -Pattern "LLM_BASE_URL|LLM_API_KEY|/models|inventory|shortlist|redact"
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\llm-model-evaluation-plan.md" -Pattern "capability|context window|supported inputs|supported outputs|max output|modalities|unknown"
Test-Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\experiments\llm-model-evaluation\model-inventory.schema.json"
Test-Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\experiments\llm-model-evaluation\model-capability-review.md"
Test-Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\experiments\llm-model-evaluation\model-evaluation-runbook.md"
```

Additional checks:

- `model-inventory.schema.json` parsed as valid JSON.
- content checks confirmed no committed API key placeholders other than
  environment-variable names.
- `git diff --check` passed.

## PR / CI / Merge

PR: https://github.com/RishiPrasath/waypoint-pilot/pull/24
PR CI/CD: no checks reported at PR creation time
Main CI/CD:
Merge commit:
Cleanup:

## Risks And Deferred Work

- Live provider inventory is deferred until the owner supplies
  `LLM_BASE_URL`, `LLM_API_KEY`, and optional `LLM_PROVIDER_LABEL`.
- Model capability values remain unknown until provider-specific metadata,
  official docs, or approved probes are collected.
- Multimodal PDF/image/audio/voice evaluation is out of scope unless later
  required by the RAG design.
- Final model lock is explicitly deferred until `RAG-BT019` or a later
  evaluation run produces evidence.
