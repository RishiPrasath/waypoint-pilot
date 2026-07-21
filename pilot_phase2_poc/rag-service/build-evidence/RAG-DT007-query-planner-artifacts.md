# RAG-DT007 Evidence

Status: Complete
Task: Define Query Planner Vocabulary And Rules

Branch: `codex/rag-dt007-query-planner-artifacts`
Worktree: `C:\tmp\rag-dt007-query-planner-artifacts`
Base: `origin/main` at `99cf8a3`

## Red Check

Initial acceptance check failed because the required query-planning folder did
not exist:

```powershell
Get-ChildItem "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\query-planning"
```

Observed failure:

```text
Cannot find path ...\docs\design\query-planning because it does not exist.
```

## Inputs Reviewed

- `build-sequence/02-design-tasks/05-runtime-technical-design/RAG-DT007-query-planner-artifacts.md`
- `docs/evaluation/golden-questions.md`
- `docs/evaluation/golden-question-research-findings.md`
- `knowledge_base/registry/source_registry.yaml`
- `docs/design/source-registry-schema.md`
- `build-sequence/03-build-tasks/02-query/RAG-BT015-query-planning.md`
- `build-sequence/03-build-tasks/02-query/RAG-BT018-query-api-endpoint.md`
- `build-sequence/03-build-tasks/05-evaluation/RAG-BT019-evaluation-harness.md`

## Planning Doc Gap

The task references these planning docs:

```text
02-rag-db/active/05-query-planning.md
02-rag-db/active/06-safeguards.md
```

They were not present in this checkout. The task was completed from the
repo-local source of truth: DT007 task instructions, DT006 golden questions,
the source registry, registry schema guidance, and affected build-task files.

## Artifacts Created

- `docs/design/query-planning/planner_vocabulary.json`
- `docs/design/query-planning/query_planner_rules.yaml`
- `docs/design/query-planning/query_planner_tests.yaml`

## Affected Build Task Updates

- `RAG-BT015`: added DT007 artifact contract for vocabulary, rules, tests,
  `QueryPlan` required fields, deterministic rule order, and LLM-planner
  boundary.
- `RAG-BT018`: added API contract for planner classifications, safe responses,
  positive planner fields, and pre-retrieval blocking.
- `RAG-BT019`: added evaluation contract for planner fixture tests and separate
  planner classification reporting.

## Verification

Final acceptance check passed.

```powershell
Get-ChildItem "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\query-planning"
```

Observed artifacts:

```text
planner_vocabulary.json
query_planner_rules.yaml
query_planner_tests.yaml
```

Machine parse checks passed:

```text
json ok
yaml ok: docs/design/query-planning/query_planner_rules.yaml
yaml ok: docs/design/query-planning/query_planner_tests.yaml
```

Content checks confirmed:

- key logistics terms
- country/market aliases
- Incoterms detection terms
- relevance and out-of-scope rules
- unsupported operational, partner-source, irrelevant, malicious, ambiguous,
  and license-sensitive classifications
- DT006-derived positive and negative test cases
- affected build-task handoff updates

## PR / CI / Merge

PR: https://github.com/RishiPrasath/waypoint-pilot/pull/22
PR CI/CD: pending
Main CI/CD:
Merge commit:
Cleanup:

## Risks And Deferred Work

- Planner runtime code remains out of scope for this design task.
- LLM planner behavior remains out of scope unless later approved.
- Incoterms and WCO/ICC content are detected for safety boundaries only until
  license-sensitive source promotion is explicitly approved.
