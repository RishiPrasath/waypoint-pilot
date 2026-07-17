# RAG-BT018: Add Query API Endpoint

Status: Planned

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT018` |
| Task Name | Add Query API Endpoint |
| Build Stage | 02-query - Query |
| Source Question | RAG-Q018, RAG-Q020 |
| Decision / ADR | ADR-RAG-0001, ADR-RAG-0004, RAG-DT015, RAG-DT013 |
| Design Dependencies | RAG-BT015, RAG-BT013, RAG-BT014, RAG-BT016, RAG-BT017, RAG-DT015, RAG-DT013 |
| Depends On Build Tasks | see section 1 and section 3 |
| Branch | `codex/rag-bt018-query-api-endpoint` |
| Worktree Path | `C:\tmp\rag-bt018-query-api-endpoint` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT018-query-api-endpoint.md` |

## 1. Task Definition

Build: query API endpoint wiring.

Goal: connect query safeguards, retrieval, generation, citations, and output validation behind a FastAPI endpoint.

Module: `app/api/ and app/stages/stage_02_query/`.

Design Gates:

- `RAG-BT015`
- `RAG-BT013`
- `RAG-BT014`
- `RAG-BT016`
- `RAG-BT017`
- `RAG-DT015`
- `RAG-DT013`

Acceptance Criteria:

- endpoint accepts query request schema
- mocked pipeline returns valid answer response
- irrelevant question returns standard safe response
- endpoint uses shared error envelope for invalid input

DT006 Golden Question Contract:

- Use `docs/evaluation/golden-questions.md` to shape API-level mocked response
  cases after retrieval and generation tasks are wired.
- Positive API examples should preserve `approved_source`, `document_id`,
  `snapshot_id`, `chunk_id`, and citation metadata from the selected DT006
  cases.
- Negative API examples must include order status, driver assignment,
  partner-source operational procedure, irrelevant, malicious prompt-injection,
  and license-sensitive metadata-only exclusion behavior.
- The endpoint should return a safe response for unsupported cases rather than
  hallucinating operational state or citing unrelated regulatory sources.

DT007 Query Planner Artifact Contract:

- API-level mocked pipeline tests should include planner classifications from
  `docs/design/query-planning/query_planner_tests.yaml`.
- The endpoint should expose safe behavior for DT007 classifications:
  `unsupported_operational`, `partner_source_required`, `irrelevant`,
  `malicious`, `license_sensitive`, and `ambiguous`.
- Positive mocked responses should preserve planner output fields such as
  relevance classification, intent, markets, source filters, and retrieval
  allowance before retrieval/generation output is assembled.
- Malicious and license-sensitive requests must be blocked or safely refused
  before retrieval.

DT009 LLM Evaluation Fixture Contract:

- Query API tests should preserve fields required by
  `docs/design/llm-model-evaluation-plan.md` so `RAG-BT019` can evaluate
  generation quality, schema adherence, citation behavior, refusal behavior,
  latency, and provider/model errors.
- Positive responses should expose enough citation metadata to validate DT005
  chunk lineage and DT006 golden-question expectations.
- Negative responses should expose safe refusal classification without sending
  unrelated retrieval context to generation.
- API tests must mock generation behavior; live provider calls and final model
  selection remain out of scope.

DT015 LLM Evaluation Result Contract:

- Preserve any response fields needed by the DT015 evaluation summary,
  especially selected/deferred model metadata, latency, citation validation,
  and provider/model error classification.
- If DT015 deferred or blocked model selection, query API tests must keep
  generation mocked and model configuration injectable.

Out Of Scope:

- real provider calls in API tests
- production auth

## 2. Worktree And Branch Setup

Create the branch and worktree before creating tests or implementation files.
Do not write task code directly on `main`.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt018"
$Slug = "query-api-endpoint"
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
TASK_ID="rag-bt018"
SLUG="query-api-endpoint"
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
pilot_phase2_poc/rag-service/app/api/tests/test_query_endpoint.py
```

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/api/tests/test_query_endpoint.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@(
  '# RAG-BT018 failing test placeholder',
  '# Replace this placeholder with the task-specific failing test after design gates are complete.',
  'def test_query_api_endpoint():',
  '    assert False, "Implement RAG-BT018 after design dependencies are confirmed"'
) | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/api/tests/test_query_endpoint.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
# RAG-BT018 failing test placeholder
# Replace this placeholder with the task-specific failing test after design gates are complete.
def test_query_api_endpoint():
    assert False, "Implement RAG-BT018 after design dependencies are confirmed"
EOF
```

Expected initial failure:

```text
The test or acceptance check fails because query API endpoint wiring is not implemented yet.
```

## 4. Implementation

Implement only after the failing test or acceptance check exists.

Target implementation artifacts:

- `pilot_phase2_poc/rag-service/app/api/query.py`
- `pilot_phase2_poc/rag-service/app/api/schemas.py`

### Windows PowerShell Implementation File Preparation

```powershell
$PrimaryImplPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/api/query.py"
New-Item -ItemType Directory -Force -Path (Split-Path $PrimaryImplPath) | Out-Null
# Create or update the implementation artifacts for RAG-BT018:
# pilot_phase2_poc/rag-service/app/api/query.py; pilot_phase2_poc/rag-service/app/api/schemas.py
```

### Linux / macOS Bash Implementation File Preparation

```bash
PRIMARY_IMPL_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/api/query.py"
mkdir -p "$(dirname "$PRIMARY_IMPL_PATH")"
# Create or update the implementation artifacts for RAG-BT018:
# pilot_phase2_poc/rag-service/app/api/query.py; pilot_phase2_poc/rag-service/app/api/schemas.py
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
uv run pytest "app/api/tests/test_query_endpoint.py" -q
uv run pytest -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest "app/api/tests/test_query_endpoint.py" -q
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
git -C $WorktreePath commit -m "build(rag): implement rag-bt018 query-api-endpoint"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): implement rag-bt018 query-api-endpoint"
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

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-BT018-query-api-endpoint.md`.
