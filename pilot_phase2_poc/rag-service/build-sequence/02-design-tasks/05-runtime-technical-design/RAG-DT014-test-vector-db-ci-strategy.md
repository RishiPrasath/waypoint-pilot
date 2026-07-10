# RAG-DT014: Test Vector DB And CI Integration Strategy

Status: Draft

| Field | Value |
|---|---|
| Task ID | `RAG-DT014` |
| Task Name | Test Vector DB And CI Integration Strategy |
| Design Lane | 05-runtime-technical-design |
| Source Question | CI/CD vector DB integration and test environment |
| Decision / ADR | ADR-RAG-0002, ADR-RAG-0010, ADR-RAG-0011 |
| Related Planning Docs | `02-rag-db/planning/cicd-pipeline-proposal.md`, `02-rag-db/research/vector-database-selection.md` |
| Affected Build Tasks | RAG-BT010, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019, RAG-BT020 |
| Branch | `codex/rag-dt014-test-vector-db-ci-strategy` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-dt014-test-vector-db-ci-strategy` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Draft |

## 1. Task Definition

Design: define the test vector database environment and CI integration test
strategy.

Goal: make sure Qdrant/vector DB integration tests have a repeatable local and
CI test environment before ingestion and retrieval build tasks depend on it.

Output Artifact:

```text
docs/design/test-vector-db-ci-strategy.md
```

Acceptance Criteria:

- chosen CI test vector DB approach is documented
- decision is made between GitHub Actions service container and Docker Compose
  test profile
- local developer command is documented
- CI command is documented
- test collection naming and cleanup strategy are documented
- collection contract is documented, including collection name pattern, vector
  size, distance metric, embedding model/version compatibility,
  payload/schema version, source IDs, chunk IDs, content hashes, and snapshot
  fields
- seed/bootstrap step is documented
- unit tests vs integration tests are clearly separated
- pytest marker strategy is documented, such as `integration`
- required environment variables are documented
- when vector DB tests become required in PR CI is documented
- failure handling and timeout expectations are documented

Out Of Scope:

- implementing the actual GitHub Actions workflow
- implementing the Docker Compose file
- implementing ingestion or retrieval code
- production deployment

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-dt014"
$Slug = "test-vector-db-ci-strategy"
$Branch = "codex/$TaskId-$Slug"
$WorktreePath = Join-Path $WorktreeRoot "$TaskId-$Slug"

New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null
git -C $RepoRoot fetch origin
git -C $RepoRoot worktree add -b $Branch $WorktreePath origin/main
git -C $WorktreePath status --short --branch
```

### Linux / macOS Bash

```bash
REPO_ROOT="$HOME/code/waypoint-pilot"
WORKTREE_ROOT="$HOME/code/waypoint-pilot-worktrees"
TASK_ID="rag-dt014"
SLUG="test-vector-db-ci-strategy"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```

## 3. Acceptance Check

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\test-vector-db-ci-strategy.md" -Pattern "Qdrant|service container|Docker Compose|integration|seed|cleanup|pytest"
```

## 4. Design Work

Create a design note that answers:

- should CI run Qdrant as a GitHub Actions service container or through Docker
  Compose
- what local command starts the test vector DB
- what CI command starts the test vector DB
- what collection name pattern is used for tests
- what vector size and distance metric are used for the chosen embedding model
- which payload fields are required for filtering, source lineage, source hash,
  chunk identity, and test cleanup
- how test collections are created, seeded, and deleted
- what fixture data is used for vector DB tests
- which tests remain pure unit tests with mocks
- which tests require Dockerized Qdrant and use `pytest -m integration`
- when integration tests become required in PR CI
- whether slower tests run on PR, schedule, manual trigger, or release
- how failures are diagnosed using logs and health checks

Recommended default unless the design task finds a better reason:

```text
Use GitHub Actions service container for CI Qdrant integration tests.
Use Docker Compose profile for local developer parity.
Keep unit tests mock-based and fast.
Run Qdrant integration tests only after RAG-BT010 and the first ingestion/retrieval fixtures exist.
```

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT010, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019, RAG-BT020

Required Updates:

- Update vector DB client smoke-test expectations, ingestion integration tests,
  semantic retrieval integration tests, hybrid retrieval integration tests,
  evaluation test requirements, Docker/local run acceptance checks, CI marker
  usage, seed/bootstrap commands, and cleanup rules.

Deferred Impact:

- Production deployment remains out of scope.
- The exact production Qdrant deployment model remains deferred.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with RAG Architect, CI/CD Engineer, Test Engineer, and Security Reviewer.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt014 test-vector-db-ci-strategy"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt014 test-vector-db-ci-strategy"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to main.

Required PR checks:

- CI pipeline runs
- CI passes
- AI scans the design artifact and affected build-task updates
- human owner reviews the PR
- accepted findings are fixed

## 8. Merge

Merge only after CI passes and the PR is reviewed. Record PR URL, CI result,
merge commit, unresolved risks, and follow-up debt entries if any. Then clean up
the worktree.

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

## 9. Task Evidence

Branch:
Worktree:
PR:
Commit:

Design Artifact:

Affected Build Tasks:

Files Changed:
-

Checks Run:
-

CI Result:

AI Review Findings:
-

Human Review Notes:
-

Issues Encountered:
-

Resolution:
-

Debt / Follow-Ups:
-
