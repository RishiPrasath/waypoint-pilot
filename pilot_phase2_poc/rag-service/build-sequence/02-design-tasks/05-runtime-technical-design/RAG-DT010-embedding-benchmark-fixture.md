# RAG-DT010: Define Embedding Benchmark Fixture

Status: Complete

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-DT010` |
| Task Name | Define Embedding Benchmark Fixture |
| Design Lane | 05-runtime-technical-design |
| Source Question | Embedding model benchmark decision |
| Decision / ADR | ADR-RAG-0002 |
| Related Planning Docs | `02-rag-db/research/vector-database-selection.md` |
| Affected Build Tasks | RAG-BT011, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019 |
| Branch | `codex/rag-dt010-embedding-benchmark-fixture` |
| Worktree Path | `C:\tmp\rag-dt010-embedding-benchmark-fixture` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Complete |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT010-embedding-benchmark-fixture.md` |

## 1. Task Definition

Design: define local embedding benchmark fixture.

Goal: compare embedding model quality, latency, memory, and local hardware fit
before locking embedding defaults.

Experiment Method:

- use FastEmbed as the local embedding model source
- use `qdrant-client` for vector indexing and search
- use Qdrant local in-memory mode, `QdrantClient(":memory:")`, for this
  design benchmark
- use DT005 `hybrid_structure_recursive_v1` chunks as the indexed document
  fixture
- use DT006 golden questions as benchmark queries
- keep Dockerized or service-hosted Qdrant out of this task unless a finding
  proves local mode is insufficient
- defer Docker/service Qdrant CI strategy to RAG-DT014
- defer production adapter implementation to RAG-BT011

Reference Basis:

- Qdrant FastEmbed documentation: `https://qdrant.tech/documentation/fastembed/`
- Qdrant client local mode documentation:
  `https://github.com/qdrant/qdrant-client`
- Qdrant FastEmbed semantic-search tutorial:
  `https://qdrant.tech/documentation/fastembed/fastembed-semantic-search/`
- FastEmbed supported models:
  `https://qdrant.github.io/fastembed/examples/Supported_Models/`

Output Artifact:

```text
docs/design/embedding-benchmark-plan.md
```

Experiment Output Artifacts:

```text
docs/design/experiments/embedding-benchmark/dt010-run-001/embedding-model-inventory.json
docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-fixture.jsonl
docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-results.jsonl
docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-summary.md
```

Acceptance Criteria:

- candidate embedding models are listed
- local hardware constraints are documented
- model source is documented as FastEmbed-supported local text embedding models
- experiment environment is documented as Python 3.12, `uv`, FastEmbed,
  `qdrant-client`, and Qdrant local `:memory:` mode
- benchmark inputs are documented as DT005 hybrid chunks, DT006 golden
  questions, and DT012 source lineage metadata
- quality metrics are defined, including Recall@k, MRR, expected source match,
  expected chunk match, and top-k failure notes
- latency and memory measurement are defined, including chunk embedding time,
  query embedding time, Qdrant search time, model download/size notes, vector
  dimension, and local CPU fit
- benchmark artifacts are written under a run-specific folder
- benchmark summary recommends selected, deferred, and rejected candidate models
  with reasons
- model swap path is documented
- RAG-DT014 boundary is documented: real Qdrant service/Docker/CI testing is
  deferred there

Out Of Scope:

- final embedding adapter implementation
- final model lock without benchmark evidence
- production Qdrant deployment or CI service-container setup
- cloud embedding provider evaluation unless explicitly added by a later task

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt010"
$Slug = "embedding-benchmark-fixture"
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
TASK_ID="rag-dt010"
SLUG="embedding-benchmark-fixture"
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
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\embedding-benchmark-plan.md" -Pattern "latency|memory|quality|model"
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\embedding-benchmark-plan.md" -Pattern "FastEmbed|qdrant-client|QdrantClient|:memory:|Recall@k|MRR|DT005|DT006|DT012|RAG-DT014"
Test-Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\experiments\embedding-benchmark\dt010-run-001"
```

## 4. Design Work

Define benchmark fixture and measurement process.

Required design content:

1. Explain why this task uses local FastEmbed-supported embedding models.
2. Explain that Qdrant is the vector store/search layer, not the source of the
   embedding model, except where a Qdrant inference feature is explicitly
   selected by a later task.
3. Document the experiment environment:
   - Python 3.12
   - `uv`
   - `fastembed`
   - `qdrant-client`
   - Qdrant local in-memory mode, `QdrantClient(":memory:")`
4. Document the benchmark inputs:
   - `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl`
   - DT006 golden questions
   - DT012 source registry and source lineage metadata
5. Define the benchmark runner behavior:
   - load chunk fixtures
   - load golden questions and expected targets
   - create a clean in-memory Qdrant collection per candidate model
   - generate embeddings for chunks
   - upsert chunk vectors with payload metadata
   - generate embeddings for each query
   - search top-k
   - score expected source and expected chunk retrieval
   - record latency, vector dimension, failures, and hardware-fit notes
6. Define required metrics:
   - Recall@1, Recall@3, and Recall@5
   - MRR
   - expected source match
   - expected chunk match
   - chunk embedding latency
   - query embedding latency
   - Qdrant search latency
   - model size/download note
   - memory/local CPU fit note
7. Define candidate model review:
   - list candidate model name, dimension, license, model size, language scope,
     and inclusion reason
   - include at least one small baseline and one stronger candidate if local
     hardware permits
8. Write run artifacts under:

   ```text
   docs/design/experiments/embedding-benchmark/dt010-run-001/
   ```

9. Record the decision as selected, deferred, or rejected per model.
10. Document the boundary with RAG-DT014:
    - DT010 may use Qdrant local memory mode for benchmark speed and
      repeatability
    - DT014 decides Docker/service Qdrant, CI integration, pytest markers,
      seed/bootstrap, cleanup, and required PR gates

Suggested benchmark command:

```powershell
Set-Location "$WorktreePath\pilot_phase2_poc\rag-service"
uv run --with fastembed --with qdrant-client python "docs/design/experiments/embedding-benchmark/run_embedding_benchmark.py"
```

The runner may be a design artifact for this task. If the benchmark cannot be
executed because model download, network, disk, or CPU constraints block it,
record the blocker in the evidence file and still produce the fixture design.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT011, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019

Required Updates:

- Update embedding adapter interface expectations, benchmark fixture,
  retrieval quality expectations, latency/memory acceptance, model swap notes,
  collection vector size/distance expectations, and the DT014 boundary between
  local benchmark and service-backed integration testing.

Deferred Impact:

- Final embedding model lock requires benchmark evidence.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with Embedding Specialist, Retrieval Engineer, and RAG Evaluation Lead.

Verification result:

- `dt010-run-001` executed with FastEmbed and Qdrant local in-memory mode.
- `BAAI/bge-small-en` selected as the first-pass embedding model.
- Benchmark artifacts were written under
  `docs/design/experiments/embedding-benchmark/dt010-run-001/`.
- Standard service test suite passed.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt010 embedding-benchmark-fixture"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt010 embedding-benchmark-fixture"
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
## Task Evidence

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-DT010-embedding-benchmark-fixture.md`.
