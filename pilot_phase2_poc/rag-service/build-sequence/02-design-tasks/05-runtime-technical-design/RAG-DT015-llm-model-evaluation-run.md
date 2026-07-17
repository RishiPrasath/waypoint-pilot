# RAG-DT015: Run LLM Model Evaluation And Selection

Status: Planned

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-DT015` |
| Task Name | Run LLM Model Evaluation And Selection |
| Design Lane | 05-runtime-technical-design |
| Source Question | LLM model selection process |
| Decision / ADR | ADR-RAG-0003 |
| Related Planning Docs | `docs/design/llm-model-evaluation-plan.md` |
| Affected Build Tasks | RAG-BT016, RAG-BT017, RAG-BT018, RAG-BT019 |
| Branch | `codex/rag-dt015-llm-model-evaluation-run` |
| Worktree Path | `C:\tmp\rag-dt015-llm-model-evaluation-run` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT015-llm-model-evaluation-run.md` |

## 1. Task Definition

Design experiment: run the actual LLM model inventory, capability review,
shortlist, evaluation, and selection recommendation using the `RAG-DT009`
fixture.

Goal: select or defer the generation model using evidence before generation
adapter implementation begins.

Output Artifacts:

```text
docs/design/experiments/llm-model-evaluation/runs/<run-id>/model-inventory.json
docs/design/experiments/llm-model-evaluation/runs/<run-id>/model-capabilities.json
docs/design/experiments/llm-model-evaluation/runs/<run-id>/model-shortlist.json
docs/design/experiments/llm-model-evaluation/runs/<run-id>/fixture-cases.jsonl
docs/design/experiments/llm-model-evaluation/runs/<run-id>/model-results.jsonl
docs/design/experiments/llm-model-evaluation/runs/<run-id>/evaluation-summary.md
docs/design/llm-model-selection-decision.md
```

Acceptance Criteria:

- owner supplies provider configuration through environment variables only
- API keys are never committed, printed, or written into evidence
- OpenAI-compatible `/models` inventory is run or explicitly blocked with
  reason
- model capability/specification review is completed before evaluation
- include/defer/exclude shortlist is recorded with rationale
- evaluation fixture uses DT006 golden questions, DT005 hybrid chunks, DT007
  planner expectations, and DT012 source lineage
- candidate models are evaluated for quality, groundedness, schema adherence,
  citation behavior, refusal/safety behavior, latency, provider/model errors,
  and malformed output handling
- model selection decision is recorded as selected, deferred, or blocked
- affected build tasks are updated with the selected model or explicit
  deferral rule

Out Of Scope:

- production generation adapter implementation
- hidden or unreviewed model calls
- multimodal PDF, image, audio, voice, or realtime evaluation unless explicitly
  approved for this RAG design

## 2. Worktree And Branch Setup

Create the branch and worktree before running the experiment or editing
artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt015"
$Slug = "llm-model-evaluation-run"
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
TASK_ID="rag-dt015"
SLUG="llm-model-evaluation-run"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
git -C "$REPO_ROOT" config core.longpaths true
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```

## 3. Acceptance Check

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\llm-model-selection-decision.md" -Pattern "selected|deferred|blocked|model|rationale|evidence"
Test-Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\experiments\llm-model-evaluation\runs"
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\build-evidence\RAG-DT015-llm-model-evaluation-run.md" -Pattern "LLM_BASE_URL|LLM_API_KEY|redacted|inventory|capability|shortlist|evaluation"
```

## 4. Design Experiment Work

Run the process defined by `RAG-DT009`:

1. Ask the owner for:
   - OpenAI-compatible base URL in `LLM_BASE_URL`
   - API key in `LLM_API_KEY`
   - optional provider label in `LLM_PROVIDER_LABEL`
2. Confirm no API key will be written to repo files, evidence, logs, or PR text.
3. Run provider inventory with `GET {LLM_BASE_URL}/models`.
4. Enrich capability/specification metadata using:
   - `/models`
   - `/models/{model}` when supported
   - provider model docs or model cards
   - owner-approved safe probes
5. Record include/defer/exclude model shortlist.
6. Build fixture cases from:
   - `docs/evaluation/golden-questions.md`
   - `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl`
   - `docs/design/query-planning/query_planner_tests.yaml`
   - `docs/design/source-snapshot-and-markdown-candidates.md`
7. Evaluate shortlisted models.
8. Write a summary with:
   - model scores
   - failure modes
   - latency observations
   - schema/citation behavior
   - refusal/safety behavior
   - final selected/deferred/blocked decision

If the owner cannot provide credentials or provider access, mark the task
blocked with a concrete reason. Do not fabricate model inventory or evaluation
results.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT016, RAG-BT017, RAG-BT018, RAG-BT019

Required Updates:

- Update generation adapter default model candidate, timeout assumptions,
  schema/citation validation expectations, query API response metadata, and
  evaluation harness fixture wiring according to the DT015 result.

Deferred Impact:

- If model selection is blocked or deferred, final generation adapter model
  lock remains deferred and build tasks must use configurable model settings.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with LLM Integration Engineer and RAG Evaluation Lead.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt015 llm-model-evaluation-run"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt015 llm-model-evaluation-run"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to main.

Required PR checks:

- CI pipeline runs
- CI passes
- AI scans the design experiment artifacts and affected build-task updates
- human owner reviews the PR
- accepted findings are fixed

## 8. Merge

Merge only after CI passes and the PR is reviewed. Record PR URL, CI result,
merge commit, unresolved risks, and follow-up debt entries if any. Then clean
up the worktree.

### Windows PowerShell

```powershell
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" worktree remove $WorktreePath
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" worktree prune
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" pull --ff-only origin main
```

### Linux / macOS Bash

```bash
git -C "$REPO_ROOT" worktree remove "$WORKTREE_PATH"
git -C "$REPO_ROOT" worktree prune
git -C "$REPO_ROOT" pull --ff-only origin main
```

## Task Evidence

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-DT015-llm-model-evaluation-run.md`.
