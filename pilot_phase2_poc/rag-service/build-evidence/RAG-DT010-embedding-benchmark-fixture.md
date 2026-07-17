# RAG-DT010 Evidence

Task: Define Embedding Benchmark Fixture

Branch: `codex/rag-dt010-embedding-benchmark-fixture`
Worktree: `C:\tmp\rag-dt010-embedding-benchmark-fixture`
Base: `origin/main` at `05a3a38`

## Objective

Define and run the first local embedding benchmark fixture using real Phase 2
RAG artifacts before the embedding adapter and retrieval tasks lock in a model
default.

## Inputs

- `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl`
- `docs/evaluation/golden-questions.md`
- DT012 lineage fields preserved in the DT005 chunk payloads
- FastEmbed-supported local text embedding models
- Qdrant local in-memory mode through `QdrantClient(":memory:")`

## Experiment Command

```powershell
Set-Location "C:\tmp\rag-dt010-embedding-benchmark-fixture\pilot_phase2_poc\rag-service"
uv run --with fastembed --with qdrant-client python "docs/design/experiments/embedding-benchmark/run_embedding_benchmark.py"
```

Result: completed successfully.

Notes:

- FastEmbed downloaded local ONNX model assets through Hugging Face cache.
- Hugging Face emitted a Windows symlink-cache warning because Developer Mode
  or elevated symlink support is not enabled. The benchmark still completed.
- Requests were unauthenticated to Hugging Face; no credentials were required
  or stored.

## Artifacts Created

- `docs/design/embedding-benchmark-plan.md`
- `docs/design/experiments/embedding-benchmark/run_embedding_benchmark.py`
- `docs/design/experiments/embedding-benchmark/dt010-run-001/embedding-model-inventory.json`
- `docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-fixture.jsonl`
- `docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-results.jsonl`
- `docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-summary.json`
- `docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-summary.md`

## Candidate Models Tested

| Model | Dimension | License | Size GB | Decision |
|---|---:|---|---:|---|
| `BAAI/bge-small-en` | 384 | MIT | 0.13 | Selected |
| `BAAI/bge-base-en-v1.5` | 768 | MIT | 0.21 | Deferred |
| `sentence-transformers/all-MiniLM-L6-v2` | 384 | Apache-2.0 | 0.09 | Rejected for default |

## Benchmark Result

| Model | Recall@1 | Recall@3 | Recall@5 | MRR | Source@1 | Query p50 ms | Search p50 ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| `BAAI/bge-small-en` | 0.875 | 1.000 | 1.000 | 0.917 | 1.000 | 2.78 | 0.78 |
| `BAAI/bge-base-en-v1.5` | 0.875 | 1.000 | 1.000 | 0.917 | 1.000 | 10.38 | 1.40 |
| `sentence-transformers/all-MiniLM-L6-v2` | 0.875 | 0.875 | 0.875 | 0.875 | 1.000 | 6.23 | 0.76 |

Selected first-pass model:

```text
BAAI/bge-small-en
```

Rationale:

- It tied `BAAI/bge-base-en-v1.5` on expected chunk Recall@3, Recall@5, MRR,
  and source recall.
- It was faster on query embedding in this run.
- It uses 384-dimensional vectors instead of 768-dimensional vectors, reducing
  local storage and test overhead.
- It performed better than `sentence-transformers/all-MiniLM-L6-v2` on expected
  chunk Recall@3/Recall@5.

## Affected Build Task Updates

- `RAG-BT011`: FastEmbed adapter should default to `BAAI/bge-small-en`, 384
  dimensions, cosine distance, while keeping deterministic unit tests.
- `RAG-BT012`: ingestion reports should record provider/model/dimension/distance
  and benchmark run ID.
- `RAG-BT013`: semantic retrieval should compare against DT010 benchmark
  results and initially target expected chunk Recall@3.
- `RAG-BT014`: hybrid retrieval should preserve or improve the DT010 semantic
  baseline.
- `RAG-BT019`: evaluation harness should load/report DT010 benchmark artifacts
  separately from LLM answer quality.

## Verification

Acceptance scans:

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\embedding-benchmark-plan.md" -Pattern "latency|memory|quality|model"
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\embedding-benchmark-plan.md" -Pattern "FastEmbed|qdrant-client|QdrantClient|:memory:|Recall@k|MRR|DT005|DT006|DT012|RAG-DT014"
Test-Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\experiments\embedding-benchmark\dt010-run-001"
```

Standard tests:

```powershell
uv run python -m pytest -q
```

Result:

```text
12 passed
```

## PR / CI / Merge

PR:
PR CI/CD:
Main CI/CD:
Merge commit:
Cleanup:

## Risks And Deferred Work

- DT010 used Qdrant local in-memory mode; Docker/service Qdrant remains
  assigned to `RAG-DT014`.
- FastEmbed model downloads depend on external package/model availability.
- Re-run the benchmark when the corpus expands beyond the first DT012 candidate
  set.
- `BAAI/bge-base-en-v1.5` remains a deferred comparison model if future source
  diversity requires stronger embeddings.
