# RAG-BT014: Add Lexical And Hybrid Retrieval

Status: Planned

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT014` |
| Task Name | Add Lexical And Hybrid Retrieval |
| Build Stage | 03-retrieval - Retrieval |
| Source Question | RAG-Q009, RAG-Q017 |
| Decision / ADR | ADR-RAG-0007, RAG-DT005, RAG-DT018, RAG-DT013 |
| Design Dependencies | RAG-DT005, RAG-DT014, RAG-DT018, RAG-DT022, RAG-DT025, RAG-DT013 |
| Depends On Build Tasks | RAG-BT013, RAG-BT023 |
| Branch | `codex/rag-bt014-lexical-hybrid-retrieval` |
| Worktree Path | `C:\tmp\rag-bt014-lexical-hybrid-retrieval` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT014-lexical-hybrid-retrieval.md` |

## 1. Task Definition

Build: lexical retriever, hybrid fusion, and reranking hook.

Goal: support controlled hybrid retrieval after semantic baseline is stable.

Module: `app/stages/stage_03_retrieval/`.

Design Gates:

- `RAG-BT013`
- `RAG-DT005`
- `RAG-DT014`
- `RAG-DT018`
- `RAG-DT013`

DT018 Retrieval Strategy And Fusion Gate:

- Before implementation, confirm `RAG-DT018` has defined lexical method,
  tokenization, normalization, candidate pool sizes, score normalization,
  fusion rule, metadata filters/boosts, tie-breaking, low-confidence behavior,
  and rerank hook input/output.
- If `RAG-DT018` is waived, `RAG-DT013` must record the waiver and accepted
  risk before this task starts.

DT018 Proposed Handoff:

- Implement a deterministic BM25-style lexical scorer over chunk text,
  `heading_path`, `document_id`, source title/owner, source URI terms, market,
  and planner vocabulary aliases.
- Use semantic top `12`, lexical top `12`, merged unique pool up to `24`, fused
  top `8`, and generation-context top `4`.
- Normalize semantic and lexical scores per query, then fuse with
  `0.65 semantic + 0.35 lexical`.
- Add capped boosts only after hard filters:
  - exact-match boost `<= 0.15`
  - metadata boost `<= 0.05`
- Use `exact_match_boosted_hybrid` for source IDs, source titles, article
  numbers, HS/tariff terms, permit names, and named procedures.
- Use `metadata_filtered_hybrid` as the default answerable public regulatory
  path.
- Keep `lexical_only_diagnostic` as a debug/test mode, not answer default.
- Implement the no-op-compatible rerank hook and preserve deterministic fused
  ordering when the hook is disabled.
- Treat hybrid ranking regression below DT010 semantic Recall@3 as a defect or
  explicit owner tradeoff.

DT014 Vector DB Test Handoff:

- Qdrant test mode: lexical scoring can be unit-tested without Qdrant; hybrid
  retrieval acceptance must run against the same service-backed Qdrant fixture
  used by semantic retrieval.
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
- Collection naming rule: `rag_test_rag_bt014_<run_id>`.
- Seed fixture: reuse BT013 semantic retrieval fixture collection or recreate
  the same BT012/DT005/DT010 seed for apples-to-apples ranking comparison.
- Payload contract: preserve semantic retrieval lineage fields plus lexical and
  hybrid score fields needed for deterministic ranking reports.
- Cleanup rule: delete any task-owned collection before/after test; do not
  delete shared fixtures unless this task created them.
- CI gate timing: required after BT013 semantic retrieval baseline is stable.

DT016 CI/CD Readiness Handoff:

- Hybrid retrieval must keep unit scoring tests in default CI.
- Service-backed hybrid comparison must run under `pytest -m integration`.
- The integration job should be required only after BT013 baseline is stable and
  Qdrant service-container CI is already proven.
- CI artifacts or logs should preserve ranking diagnostics without storing
  secrets or oversized raw corpora.

Acceptance Criteria:

- lexical retriever returns candidates
- hybrid fusion combines semantic and lexical scores
- controlled fixture ranking is deterministic
- reranking hook exists but may be no-op initially

Out Of Scope:

- LLM reranker dependency
- large-scale benchmark

DT005 Hybrid Retrieval Chunk Contract:

- Lexical and hybrid retrieval must use the same `hybrid_structure_recursive_v1` chunk IDs
  as semantic retrieval so ranking comparisons are apples-to-apples.
- Fixture ranking assertions should include `heading_path`, `document_id`,
  `snapshot_id`, `candidate_sha256`, and `recursive_split_applied` metadata.
- Fixed-window chunks may be used only for diagnostic comparison, not as the
  accepted fixture corpus.

DT006 Golden Question Contract:

- Use the same positive DT006 expected chunks as `RAG-BT013` so semantic,
  lexical, and hybrid retrieval rankings are compared against the same
  `hybrid_structure_recursive_v1` fixture corpus.
- Hybrid parity checks should include at least one import case (`GQ-001` or
  `GQ-002`), one export case (`GQ-004` or `GQ-005`), and one ASEAN Trade
  Repository case (`GQ-006`, `GQ-007`, or `GQ-008`).
- `APAC-215` must remain an exclusion test and must not become a retrievable
  lexical or hybrid content chunk.

DT010 Embedding Benchmark Contract:

- Use the DT010 selected semantic embedding baseline as the dense side of
  hybrid retrieval:
  - provider: `fastembed`
  - model name: `BAAI/bge-small-en`
  - vector dimension: `384`
  - distance metric: `cosine`
- Hybrid retrieval should compare against the same positive DT006 expected
  chunks used in
  `docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-results.jsonl`.
- Hybrid fusion should improve or preserve the DT010 semantic baseline; any
  ranking regression below expected chunk Recall@3 must be recorded as a
  defect or accepted tradeoff.
- `BAAI/bge-base-en-v1.5` remains a deferred comparison model, not the default.

## 2. Worktree And Branch Setup

Create the branch and worktree before creating tests or implementation files.
Do not write task code directly on `main`.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt014"
$Slug = "lexical-hybrid-retrieval"
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
TASK_ID="rag-bt014"
SLUG="lexical-hybrid-retrieval"
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
pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/tests/test_hybrid_retrieval.py
```

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/tests/test_hybrid_retrieval.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@(
  '# RAG-BT014 failing test placeholder',
  '# Replace this placeholder with the task-specific failing test after design gates are complete.',
  'def test_lexical_hybrid_retrieval():',
  '    assert False, "Implement RAG-BT014 after design dependencies are confirmed"'
) | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/tests/test_hybrid_retrieval.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
# RAG-BT014 failing test placeholder
# Replace this placeholder with the task-specific failing test after design gates are complete.
def test_lexical_hybrid_retrieval():
    assert False, "Implement RAG-BT014 after design dependencies are confirmed"
EOF
```

Expected initial failure:

```text
The test or acceptance check fails because lexical retriever, hybrid fusion, and reranking hook is not implemented yet.
```

## 4. Implementation

Implement only after the failing test or acceptance check exists.

Target implementation artifacts:

- `pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/lexical.py`
- `pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/fusion.py`

### Windows PowerShell Implementation File Preparation

```powershell
$PrimaryImplPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/lexical.py"
New-Item -ItemType Directory -Force -Path (Split-Path $PrimaryImplPath) | Out-Null
# Create or update the implementation artifacts for RAG-BT014:
# pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/lexical.py; pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/fusion.py
```

### Linux / macOS Bash Implementation File Preparation

```bash
PRIMARY_IMPL_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/lexical.py"
mkdir -p "$(dirname "$PRIMARY_IMPL_PATH")"
# Create or update the implementation artifacts for RAG-BT014:
# pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/lexical.py; pilot_phase2_poc/rag-service/app/stages/stage_03_retrieval/fusion.py
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
uv run pytest "app/stages/stage_03_retrieval/tests/test_hybrid_retrieval.py" -q
uv run pytest -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest "app/stages/stage_03_retrieval/tests/test_hybrid_retrieval.py" -q
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
git -C $WorktreePath commit -m "build(rag): implement rag-bt014 lexical-hybrid-retrieval"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): implement rag-bt014 lexical-hybrid-retrieval"
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

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-BT014-lexical-hybrid-retrieval.md`.

## DT013 Final Design Handoff

- Implement planner-led hybrid retrieval with semantic and lexical scoring, metadata filters/boosts, score normalization, fusion, deterministic tie-breaks, and a no-op rerank hook.
- Expose retrieval mode, score trace, confidence, and low-confidence/no-evidence decisions for API and evaluation consumers.
- Treat lexical-only as diagnostic and semantic-only as baseline unless a later decision changes runtime strategy.
