# RAG-BT017: Add Output Validation And Retry/Fallback

Status: Planned

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT017` |
| Task Name | Add Output Validation And Retry/Fallback |
| Build Stage | 04-generation - Generation |
| Source Question | RAG-Q015, RAG-Q016 |
| Decision / ADR | ADR-RAG-0004, RAG-DT015, RAG-DT019, RAG-DT013 |
| Design Dependencies | RAG-DT015, RAG-DT019, RAG-DT021, RAG-DT022, RAG-DT023, RAG-DT025, RAG-DT013 |
| Depends On Build Tasks | RAG-BT006, RAG-BT015, RAG-BT016 |
| Branch | `codex/rag-bt017-output-validation-retry-fallback` |
| Worktree Path | `C:\tmp\rag-bt017-output-validation-retry-fallback` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT017-output-validation-retry-fallback.md` |

## 1. Task Definition

Build: output validation, retry policy, and fallback behavior.

Goal: ensure generated answers are schema-valid, grounded, cited, and safely handled on failure.

Module: `app/stages/stage_04_generation/`.

Design Gates:

- `RAG-BT016`
- `RAG-BT006`
- `RAG-BT015`
- `RAG-DT015`
- `RAG-DT019`
- `RAG-DT013`

DT019 Output Schema And Safeguard Gate:

- Before implementation, confirm `RAG-DT019` has defined answer schema,
  citation schema, refusal schema, low-confidence/no-evidence behavior, retry
  semantics, fallback response shape, and API error-envelope mapping.
- If `RAG-DT019` is waived, `RAG-DT013` must record the waiver and accepted
  risk before this task starts.

DT019 Proposed Handoff:

- Validate every generation output against
  `docs/design/experiments/generation-api-contract/dt019-run-001/response-schema.json`.
- Reject positive answers with missing citations.
- Reject citations that do not match retrieved context lineage.
- Reject answer text generated from `license_sensitive`, `cite_only`, or
  `do_not_ingest` sources.
- Retry at most once for malformed JSON or recoverable schema failure.
- Do not retry policy-blocked, malicious, irrelevant, unsupported operational,
  or authentication-failure cases.
- Return `answer_type: error_fallback` for exhausted retry, provider failure,
  timeout, dependency unavailable, or unrecoverable malformed output.
- Preserve error `stage` and `reason_code` for evaluation.

Acceptance Criteria:

- invalid schema fails validation
- missing citations fail when citations are required
- max retry behavior is bounded
- fallback response is safe and standard

DT009 LLM Evaluation Fixture Contract:

- Use the scoring categories in
  `docs/design/llm-model-evaluation-plan.md`: schema adherence, citation
  behavior, groundedness, refusal/safety behavior, provider/model errors, and
  malformed output handling.
- Validation tests should include citation-shaped responses with DT006/DT005
  fields: `approved_source`, `document_id`, `snapshot_id`, `chunk_id`,
  `chunk_strategy`, `heading_path`, `source_uri`, and `candidate_sha256`.
- Retry/fallback behavior must be bounded and reportable so the evaluation
  harness can distinguish malformed output, provider error, timeout, and safe
  refusal.
- Unit tests must not require API keys or live provider calls.

DT015 LLM Evaluation Result Contract:

- Use DT015 evaluation failures to prioritize validation cases for malformed
  output, missing citations, schema drift, refusal behavior, and provider/model
  errors.
- DT015 selected `llama-3.3-70b-versatile`; validation tests should remain
  provider-agnostic but include fixtures compatible with that model's JSON and
  citation behavior.
- If DT015 marks model selection deferred or blocked, validation must remain
  provider-agnostic and configurable.

Out Of Scope:

- retrieval implementation
- API endpoint wiring

## 2. Worktree And Branch Setup

Create the branch and worktree before creating tests or implementation files.
Do not write task code directly on `main`.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt017"
$Slug = "output-validation-retry-fallback"
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
TASK_ID="rag-bt017"
SLUG="output-validation-retry-fallback"
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
pilot_phase2_poc/rag-service/app/stages/stage_04_generation/tests/test_output_validation.py
```

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_04_generation/tests/test_output_validation.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@(
  '# RAG-BT017 failing test placeholder',
  '# Replace this placeholder with the task-specific failing test after design gates are complete.',
  'def test_output_validation_retry_fallback():',
  '    assert False, "Implement RAG-BT017 after design dependencies are confirmed"'
) | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_04_generation/tests/test_output_validation.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
# RAG-BT017 failing test placeholder
# Replace this placeholder with the task-specific failing test after design gates are complete.
def test_output_validation_retry_fallback():
    assert False, "Implement RAG-BT017 after design dependencies are confirmed"
EOF
```

Expected initial failure:

```text
The test or acceptance check fails because output validation, retry policy, and fallback behavior is not implemented yet.
```

## 4. Implementation

Implement only after the failing test or acceptance check exists.

Target implementation artifacts:

- `pilot_phase2_poc/rag-service/app/stages/stage_04_generation/validation.py`
- `pilot_phase2_poc/rag-service/app/stages/stage_04_generation/retry.py`

### Windows PowerShell Implementation File Preparation

```powershell
$PrimaryImplPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_04_generation/validation.py"
New-Item -ItemType Directory -Force -Path (Split-Path $PrimaryImplPath) | Out-Null
# Create or update the implementation artifacts for RAG-BT017:
# pilot_phase2_poc/rag-service/app/stages/stage_04_generation/validation.py; pilot_phase2_poc/rag-service/app/stages/stage_04_generation/retry.py
```

### Linux / macOS Bash Implementation File Preparation

```bash
PRIMARY_IMPL_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_04_generation/validation.py"
mkdir -p "$(dirname "$PRIMARY_IMPL_PATH")"
# Create or update the implementation artifacts for RAG-BT017:
# pilot_phase2_poc/rag-service/app/stages/stage_04_generation/validation.py; pilot_phase2_poc/rag-service/app/stages/stage_04_generation/retry.py
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
uv run pytest "app/stages/stage_04_generation/tests/test_output_validation.py" -q
uv run pytest -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest "app/stages/stage_04_generation/tests/test_output_validation.py" -q
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
git -C $WorktreePath commit -m "build(rag): implement rag-bt017 output-validation-retry-fallback"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): implement rag-bt017 output-validation-retry-fallback"
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

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-BT017-output-validation-retry-fallback.md`.

## DT013 Final Design Handoff

- Validate all generation outputs against the DT019 response schema.
- Reject malformed JSON, missing/fabricated citations, unsafe license-sensitive text, and invalid refusal/error envelopes.
- Keep retry bounded and map fallback behavior to the standard API error/fallback response shape.
