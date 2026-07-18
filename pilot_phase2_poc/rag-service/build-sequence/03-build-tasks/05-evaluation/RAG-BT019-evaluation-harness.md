# RAG-BT019: Add Evaluation Harness

Status: Planned

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT019` |
| Task Name | Add Evaluation Harness |
| Build Stage | 05-evaluation - Evaluation |
| Source Question | RAG-Q010, RAG-Q023 |
| Decision / ADR | ADR-RAG-0008, RAG-DT004, RAG-DT005, RAG-DT006, RAG-DT009, RAG-DT012, RAG-DT015, RAG-DT018, RAG-DT019, RAG-DT020, RAG-DT013 |
| Design Dependencies | RAG-DT004, RAG-DT005, RAG-DT006, RAG-DT009, RAG-DT012, RAG-DT014, RAG-DT015, RAG-DT018, RAG-DT019, RAG-DT020, RAG-BT018, RAG-DT013 |
| Depends On Build Tasks | see section 1 and section 3 |
| Branch | `codex/rag-bt019-evaluation-harness` |
| Worktree Path | `C:\tmp\rag-bt019-evaluation-harness` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT019-evaluation-harness.md` |

## 1. Task Definition

Build: golden-question evaluation harness.

Goal: run regression checks for retrieval, citations, answer quality, irrelevant queries, and malicious queries.

Module: `app/stages/stage_05_evaluation/`.

Design Gates:

- `RAG-DT004`
- `RAG-DT005`
- `RAG-DT006`
- `RAG-DT012`
- `RAG-DT009`
- `RAG-DT014`
- `RAG-DT015`
- `RAG-DT018`
- `RAG-DT019`
- `RAG-DT020`
- `RAG-BT018`
- `RAG-DT013`

DT018/DT019/DT020 Evaluation Contract Gates:

- Before implementation, confirm `RAG-DT018` has defined retrieval modes,
  fusion/scoring fields, low-confidence behavior, and ranking metrics that the
  harness must evaluate.
- Before implementation, confirm `RAG-DT019` has defined answer schema,
  citation schema, refusal/safety behavior, and API fields that the harness
  must validate.
- Before implementation, confirm `RAG-DT020` has defined evaluation run types,
  failure taxonomy, tuning workflow, and baseline promotion/rejection rules.
- If any task is waived, `RAG-DT013` must record the waiver and accepted risk
  before this task starts.

DT019 Proposed Handoff:

- Evaluate generated/API responses against
  `docs/design/experiments/generation-api-contract/dt019-run-001/response-schema.json`.
- Report schema adherence, citation behavior, groundedness, refusal/safety
  behavior, provider/model errors, malformed output handling, retry count,
  fallback use, latency, and API response shape separately.
- Add an evaluation-only LLM judge check for whether the answer actually
  addresses the original question.
- Judge scoring must include relevance, completeness, groundedness, and
  scope-control scores on a `0`, `1`, `2` scale.
- Judge output must include `decision: pass | warn | fail` and
  `failure_reasons`.
- Judge provider/model settings must be separately injectable through
  `RAG_EVAL_LLM_PROVIDER_LABEL`, `RAG_EVAL_LLM_BASE_URL`,
  `RAG_EVAL_LLM_MODEL`, and `RAG_EVAL_LLM_API_KEY`.
- The first judge model may default to Groq `llama-3.3-70b-versatile`, but
  runtime production judge gating remains deferred.
- Verify positive answers cite supplied chunks with DT005/DT006/DT012 lineage.
- Verify no-retrieval cases do not include unrelated citations.
- Verify license-sensitive/cite-only cases do not produce answer text from
  restricted sources.
- Compare provider/model metadata to `docs/design/llm-model-selection-decision.md`.

DT018 Proposed Handoff:

- Evaluation reports must include retrieval mode as its own field.
- Report planner classification separately from retrieval ranking.
- Report semantic-only baseline and hybrid retrieval separately.
- For positive cases, record expected source rank, expected chunk Recall@3,
  Recall@5, MRR, and source lineage validity.
- For no-retrieval cases, assert retrieval was not called.
- For license-sensitive cases, assert no answer-text chunks were retrieved and
  any metadata lookup is labeled as exclusion-only.
- Report score fields separately:
  - semantic normalized score
  - lexical normalized score
  - exact-match boost
  - metadata boost
  - final fused score
- Report low-confidence/no-evidence cases separately from answer-quality
  failures.

DT014 Vector DB Test Handoff:

- Qdrant test mode: evaluation unit tests may use committed/mock retrieval
  results; Qdrant-backed retrieval evaluation must run against service-backed
  Qdrant.
- Local command: `docker compose --profile test up -d qdrant`, then
  `uv run python -m pytest -m integration -q`, then
  `docker compose --profile test down`.
- CI command: GitHub Actions Qdrant service container plus
  `uv run python -m pytest -m integration -q`.
- Pytest marker: `integration`.
- Required environment variables: `QDRANT_URL`,
  `QDRANT_COLLECTION_PREFIX`, `QDRANT_TEST_TIMEOUT_SECONDS`,
  `RUN_QDRANT_INTEGRATION`; `QDRANT_API_KEY` optional and unset for isolated
  local/CI containers.
- Collection naming rule: `rag_test_rag_bt019_<run_id>`.
- Seed fixture: retrieval fixture from BT012/BT013/BT014 using DT006 golden
  questions and DT010 embeddings.
- Payload contract: evaluation reports must separate mocked/unit retrieval
  results from Qdrant-backed retrieval results and preserve source/chunk
  lineage.
- Cleanup rule: delete task-owned collections and report cleanup status in the
  evaluation artifact.
- CI gate timing: required once Qdrant-backed retrieval evaluation is promoted
  to PR regression coverage.

DT016 CI/CD Readiness Handoff:

- Evaluation harness unit tests must run in default CI without Docker or
  external providers.
- Qdrant-backed evaluation must run under `pytest -m integration`.
- Any generated reports committed as artifacts must avoid secrets and oversized
  raw source dumps.
- CI should clearly separate mocked/unit evaluation results from Qdrant-backed
  integration evaluation results.

Acceptance Criteria:

- golden question fixture exists
- runner produces pass/fail report
- citation validity is checked
- irrelevant and malicious query cases are included
- legacy examples are not expected sources unless promoted

Out Of Scope:

- large-scale evaluation suite
- manual domain signoff

Legacy KB Guardrail:

```text
legacy/phase1-kb-snapshot is audit input only.
It must not be ingested directly.
Only audited/promoted material may become fixture, candidate, or canonical KB content.
```

DT004 KB Path Contract:

- Golden answers and citation checks must cite approved `canonical/` material or explicitly scoped `reference/` review material.
- Evaluation fixtures may use legacy files only as coverage-gap examples, never as expected runtime sources.
- Evaluation reports must flag any answer that cites `legacy/`, `drop/`, or `archive/` material as a source.

DT012 Evaluation Source Contract:

- Golden-question citations may reference DT012 source-derived candidates only
  when the fixture explicitly records candidate provenance from
  `knowledge_base/snapshots/first-pass-snapshot-manifest.md`.
- Citation validity checks must compare returned source lineage against
  `document_id`, `snapshot_id`, source URI, reuse mode, license sensitivity,
  retrieval eligibility, and candidate SHA-256.
- License-sensitive metadata-only candidates such as `APAC-215` may be used to
  test exclusion behavior, not expected answer content.

DT005 Evaluation Chunk Contract:

- Evaluation fixtures should expect citations to resolve to `hybrid_structure_recursive_v1`
  chunk IDs and heading paths.
- Citation checks must validate `chunk_strategy`, `heading_path`,
  `candidate_sha256`, `document_id`, `snapshot_id`, `section_part_index`, and
  `recursive_split_applied`.
- Evaluation may include one negative case proving `APAC-215` is skipped as
  metadata-only and license-sensitive source text.

DT006 Golden Question Contract:

- Load the first evaluation fixture from
  `docs/evaluation/golden-questions.md`.
- Preserve the research and candidate-assessment rationale from
  `docs/evaluation/golden-question-research-findings.md` as the benchmark
  design record.
- Report retrieval score, answer score, citation validity, refusal behavior,
  irrelevant-query behavior, malicious prompt-injection behavior, and
  metadata-only exclusion behavior as separate result categories.
- Treat `GQ-001` through `GQ-008` as positive or source-boundary positive
  cases; treat `GQ-009` through `GQ-014` as negative, irrelevant, malicious,
  or exclusion cases.

DT007 Query Planner Artifact Contract:

- Include planner-level evaluation using
  `docs/design/query-planning/query_planner_tests.yaml`.
- Report planner classification separately from retrieval score, answer score,
  citation validity, and refusal behavior.
- Validate that malicious, license-sensitive, unsupported operational,
  partner-source, irrelevant, and ambiguous cases do not proceed to retrieval.
- Validate that positive and source-boundary cases produce the expected market,
  intent, retrieval allowance, and source-hint behavior before downstream
  retrieval/generation checks run.

DT009 LLM Model Evaluation Fixture Contract:

- Implement the fixture flow from `docs/design/llm-model-evaluation-plan.md`
  and `docs/design/experiments/llm-model-evaluation/model-evaluation-runbook.md`.
- Provider inventory must read `LLM_BASE_URL`, `LLM_API_KEY`, and optional
  `LLM_PROVIDER_LABEL` from environment variables only and must not write API
  keys to evidence or reports.
- Inventory output should validate against
  `docs/design/experiments/llm-model-evaluation/model-inventory.schema.json`.
- Model assessment must happen only after
  `docs/design/experiments/llm-model-evaluation/model-capability-review.md`
  has produced include/defer/exclude decisions.
- Evaluation reports must separate answer quality, groundedness, schema
  adherence, citation behavior, refusal/safety behavior, latency,
  provider/model errors, and malformed output handling.
- Final model lock remains out of scope unless a later task explicitly accepts
  evaluation evidence.

DT015 LLM Evaluation Result Contract:

- Treat DT015 as the design-time LLM evaluation run.
- DT015 selected `llama-3.3-70b-versatile` as the first-pass Groq generation
  model, with `openai/gpt-oss-120b`, `llama-3.1-8b-instant`, and
  `openai/gpt-oss-20b` retained as comparison candidates.
- `RAG-BT019` should implement a repeatable evaluation harness that can rerun
  and regress the DT015 cases, not invent a separate first model-selection
  process.
- The harness should be able to compare future runs against
  `docs/design/llm-model-selection-decision.md` and the DT015 run summary.

DT010 Embedding Benchmark Result Contract:

- Treat DT010 as the design-time embedding benchmark run.
- DT010 selected `BAAI/bge-small-en` as the first-pass local FastEmbed
  embedding model.
- The evaluation harness should be able to load and report against:
  - `docs/design/embedding-benchmark-plan.md`
  - `docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-fixture.jsonl`
  - `docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-results.jsonl`
  - `docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-summary.md`
- Evaluation reporting should separate embedding/retrieval baseline quality
  from LLM answer quality. DT010 metrics include Recall@k, MRR, source recall,
  query embedding latency, and Qdrant search latency.
- If later runs change the embedding model, the evaluation harness should
  compare them against the DT010 selected baseline before accepting a new
  default.

## 2. Worktree And Branch Setup

Create the branch and worktree before creating tests or implementation files.
Do not write task code directly on `main`.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt019"
$Slug = "evaluation-harness"
$Branch = "codex/$TaskId-$Slug"
$WorktreePath = Join-Path $WorktreeRoot "$TaskId-$Slug"

New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null
git -C $RepoRoot fetch origin
git -C $RepoRoot pull --ff-only origin main
git -C $RepoRoot config core.longpaths true
git -C $RepoRoot worktree add -b $Branch $WorktreePath origin/main
git -C $WorktreePath status --short --branch
```

### Linux / macOS Bash

```bash
REPO_ROOT="$HOME/code/waypoint-pilot"
WORKTREE_ROOT="$HOME/code/waypoint-pilot-worktrees"
TASK_ID="rag-bt019"
SLUG="evaluation-harness"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
git -C "$REPO_ROOT" config core.longpaths true
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```

## 3. Test Code

Write the failing test or acceptance check first. If a design dependency changes
this task, update this section before implementation starts.

Primary test or acceptance path:

```text
pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/tests/test_evaluation_runner.py
```

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/tests/test_evaluation_runner.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@(
  '# RAG-BT019 failing test placeholder',
  '# Replace this placeholder with the task-specific failing test after design gates are complete.',
  'def test_evaluation_harness():',
  '    assert False, "Implement RAG-BT019 after design dependencies are confirmed"'
) | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/tests/test_evaluation_runner.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
# RAG-BT019 failing test placeholder
# Replace this placeholder with the task-specific failing test after design gates are complete.
def test_evaluation_harness():
    assert False, "Implement RAG-BT019 after design dependencies are confirmed"
EOF
```

Expected initial failure:

```text
The test or acceptance check fails because golden-question evaluation harness is not implemented yet.
```

## 4. Implementation

Implement only after the failing test or acceptance check exists.

Target implementation artifacts:

- `pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/runner.py`
- `pilot_phase2_poc/rag-service/docs/evaluation/golden-questions.md`

### Windows PowerShell Implementation File Preparation

```powershell
$PrimaryImplPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/runner.py"
New-Item -ItemType Directory -Force -Path (Split-Path $PrimaryImplPath) | Out-Null
# Create or update the implementation artifacts for RAG-BT019:
# pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/runner.py; pilot_phase2_poc/rag-service/docs/evaluation/golden-questions.md
```

### Linux / macOS Bash Implementation File Preparation

```bash
PRIMARY_IMPL_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/runner.py"
mkdir -p "$(dirname "$PRIMARY_IMPL_PATH")"
# Create or update the implementation artifacts for RAG-BT019:
# pilot_phase2_poc/rag-service/app/stages/stage_05_evaluation/runner.py; pilot_phase2_poc/rag-service/docs/evaluation/golden-questions.md
```

Implementation Notes:

- Keep the change limited to this task's module and directly required shared files.
- Keep tests inside the module they verify.
- Update docs when behavior, configuration, schema, or operational evidence changes.
- Record any accepted shortcut in the task evidence and backlog/follow-up notes.

## 5. Test Execution

Run the module-local test first, then the service-level checks available at that
point in the build sequence.

### Windows PowerShell

```powershell
Set-Location "$WorktreePath\pilot_phase2_poc\rag-service"
uv run pytest "app/stages/stage_05_evaluation/tests/test_evaluation_runner.py" -q
uv run pytest -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest "app/stages/stage_05_evaluation/tests/test_evaluation_runner.py" -q
uv run pytest -q
```

Record:

- command run
- initial failing result
- fix applied
- final passing result
- any skipped or deferred check with reason

## 6. Branch Workflow

Use the task branch created at the start. Keep the PR small and task-sized.

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "build(rag): implement rag-bt019 evaluation-harness"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): implement rag-bt019 evaluation-harness"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a pull request to `main`.

Required PR checks:

- CI pipeline runs
- CI passes
- AI scans the diff or PR for bugs, missing tests, security risks, design drift, and unclear code
- human owner reviews the PR
- accepted findings are fixed

## 7. Merge

Merge only after CI passes and the PR is reviewed. After merge, confirm `main`
CI/CD also runs successfully, then clean up the worktree, delete the merged
local branch, and delete the merged remote branch when permitted.

### Windows PowerShell

```powershell
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" worktree remove $WorktreePath
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" worktree prune
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" fetch origin
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" pull --ff-only origin main
```

### Linux / macOS Bash

```bash
git -C "$REPO_ROOT" worktree remove "$WORKTREE_PATH"
git -C "$REPO_ROOT" worktree prune
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
```

Record:

- PR URL
- CI result before merge
- merge commit
- `main` CI/CD result after merge
- unresolved risks
- follow-up debt entries, if any

## Task Evidence

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-BT019-evaluation-harness.md`.

## DT013 Final Design Handoff

- Report unit/mocked, service-backed Qdrant, API-level, and optional LLM-judge evaluation results separately.
- Use golden questions to report retrieval, citation, refusal, safety, relevance, groundedness, latency, provider errors, and malformed output handling.
- Apply DT020 baseline promotion/rejection and failure-taxonomy mapping in evaluation reports.
