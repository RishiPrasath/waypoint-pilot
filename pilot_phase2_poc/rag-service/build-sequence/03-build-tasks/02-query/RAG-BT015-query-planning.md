# RAG-BT015: Add Query Safeguards And Deterministic Query Planning

Status: Planned

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT015` |
| Task Name | Add Query Safeguards And Deterministic Query Planning |
| Build Stage | 02-query - Query |
| Source Question | RAG-Q014, RAG-Q010, RAG-Q017 |
| Decision / ADR | ADR-RAG-0004, RAG-DT007, RAG-DT019, RAG-DT013 |
| Design Dependencies | RAG-DT007, RAG-DT019, RAG-DT013 |
| Depends On Build Tasks | see section 1 and section 3 |
| Branch | `codex/rag-bt015-query-safeguards-planning` |
| Worktree Path | `C:\tmp\rag-bt015-query-safeguards-planning` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT015-query-planning.md` |

## 1. Task Definition

Build: query safeguards and deterministic query planner.

Goal: classify queries and emit inspectable query plans before retrieval.

Module: `app/stages/stage_02_query/`.

Design Gates:

- `RAG-DT007`
- `RAG-DT019`
- `RAG-DT013`

DT019 Safeguard/API Contract Gate:

- Before implementation, confirm `RAG-DT019` has defined the planner fields,
  safe-response fields, refusal behavior, and API-visible classification data
  this task must emit.
- If `RAG-DT019` is waived, `RAG-DT013` must record the waiver and accepted
  risk before this task starts.

DT019 Proposed Handoff:

- Emit planner fields required by the query API response:
  `relevance_classification`, `intent`, `retrieval_allowed`,
  `safe_response_id`, `markets`, `source_filters`, and `reasons`.
- Map blocked planner classifications to DT019 reason codes:
  `irrelevant`, `unsupported_operational`, `partner_source_required`,
  `malicious_prompt_injection`, `license_sensitive`, and `ambiguous`.
- Ensure blocked classifications do not call retrieval or generation.
- Provide enough metadata for the API response `planner` object in
  `docs/design/experiments/generation-api-contract/dt019-run-001/response-schema.json`.

Acceptance Criteria:

- planner emits QueryPlan
- relevance classification exists
- query safeguard classifies relevant, irrelevant, malicious, and ambiguous queries
- irrelevant questions return the standard safe response path
- malicious or prompt-injection-like questions are blocked before retrieval
- country/incoterm/entity extraction uses deterministic rules first

DT007 Query Planner Artifact Contract:

- Load deterministic vocabulary from
  `docs/design/query-planning/planner_vocabulary.json`.
- Load relevance, out-of-scope, safe-response, source-filter, and rule-order
  behavior from `docs/design/query-planning/query_planner_rules.yaml`.
- Use `docs/design/query-planning/query_planner_tests.yaml` as the first
  implementation fixture set for query safeguards and planner behavior.
- Emit a `QueryPlan` shape compatible with the DT007
  `query_plan_contract.required_fields`.
- Apply rule order before retrieval:
  malicious prompt injection, license-sensitive reproduction, unsupported
  operational action/status, partner-source/internal procedure, irrelevant,
  in-scope boundary, in-scope retrieval, and ambiguous fallback.
- Keep LLM planner behavior out of scope; deterministic rules run first.

Out Of Scope:

- LLM generation
- retrieval execution

## 2. Worktree And Branch Setup

Create the branch and worktree before creating tests or implementation files.
Do not write task code directly on `main`.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt015"
$Slug = "query-safeguards-planning"
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
TASK_ID="rag-bt015"
SLUG="query-safeguards-planning"
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
pilot_phase2_poc/rag-service/app/stages/stage_02_query/tests/test_query_safeguards_and_planner.py
```

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_02_query/tests/test_query_safeguards_and_planner.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@(
  '# RAG-BT015 failing test placeholder',
  '# Replace this placeholder with the task-specific failing test after design gates are complete.',
  'def test_query_safeguards_planning():',
  '    assert False, "Implement RAG-BT015 after design dependencies are confirmed"'
) | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_02_query/tests/test_query_safeguards_and_planner.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
# RAG-BT015 failing test placeholder
# Replace this placeholder with the task-specific failing test after design gates are complete.
def test_query_safeguards_planning():
    assert False, "Implement RAG-BT015 after design dependencies are confirmed"
EOF
```

Expected initial failure:

```text
The test or acceptance check fails because query safeguards and deterministic query planner is not implemented yet.
```

## 4. Implementation

Implement only after the failing test or acceptance check exists.

Target implementation artifacts:

- `pilot_phase2_poc/rag-service/app/stages/stage_02_query/safeguards.py`
- `pilot_phase2_poc/rag-service/app/stages/stage_02_query/planner.py`
- `pilot_phase2_poc/rag-service/app/stages/stage_02_query/schemas.py`

### Windows PowerShell Implementation File Preparation

```powershell
$PrimaryImplPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_02_query/safeguards.py"
New-Item -ItemType Directory -Force -Path (Split-Path $PrimaryImplPath) | Out-Null
# Create or update the implementation artifacts for RAG-BT015:
# pilot_phase2_poc/rag-service/app/stages/stage_02_query/safeguards.py; pilot_phase2_poc/rag-service/app/stages/stage_02_query/planner.py; pilot_phase2_poc/rag-service/app/stages/stage_02_query/schemas.py
```

### Linux / macOS Bash Implementation File Preparation

```bash
PRIMARY_IMPL_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_02_query/safeguards.py"
mkdir -p "$(dirname "$PRIMARY_IMPL_PATH")"
# Create or update the implementation artifacts for RAG-BT015:
# pilot_phase2_poc/rag-service/app/stages/stage_02_query/safeguards.py; pilot_phase2_poc/rag-service/app/stages/stage_02_query/planner.py; pilot_phase2_poc/rag-service/app/stages/stage_02_query/schemas.py
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
uv run pytest "app/stages/stage_02_query/tests/test_query_safeguards_and_planner.py" -q
uv run pytest -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest "app/stages/stage_02_query/tests/test_query_safeguards_and_planner.py" -q
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
git -C $WorktreePath commit -m "build(rag): implement rag-bt015 query-safeguards-planning"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): implement rag-bt015 query-safeguards-planning"
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

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-BT015-query-planning.md`.
