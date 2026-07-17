# RAG-DT010 Embedding Benchmark Plan

Status: Accepted for `RAG-DT010`
Run: `dt010-run-001`

## Purpose

This plan defines the first local embedding benchmark fixture for the Phase 2
RAG service. The goal is to choose a practical first-pass embedding model and
define the measurement contract that later ingestion, retrieval, vector DB, and
evaluation build tasks can reuse.

The benchmark uses real project fixtures rather than synthetic sample text:

- DT005 `hybrid_structure_recursive_v1` chunks
- DT006 golden questions
- DT012 source lineage metadata carried in the chunks
- Qdrant local in-memory mode for repeatable design-time search

## Environment

The benchmark is designed to run locally with:

```text
Python 3.12
uv
fastembed
qdrant-client
QdrantClient(":memory:")
```

Qdrant is used as the vector store and search layer. It is not treated as the
model source for this task. Embedding models come from FastEmbed-supported local
text embedding models.

The DT010 benchmark intentionally avoids Dockerized or service-hosted Qdrant.
That CI/service integration boundary remains assigned to `RAG-DT014`.

## Inputs

| Input | Path | Use |
|---|---|---|
| Chunk fixture | `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl` | Indexed document chunks. |
| Golden questions | `docs/evaluation/golden-questions.md` | Query fixture and expected retrieval targets. |
| Source lineage | chunk payload fields from DT012 registry/snapshot work | Citation and metadata-preservation expectations. |

Only DT006 positive/source-boundary cases with explicit expected chunk IDs are
used for the embedding benchmark. Negative, irrelevant, malicious,
license-sensitive, and unsupported operational cases remain evaluation/API
behavior checks for later tasks.

## Candidate Models

The first run tested these local FastEmbed-supported models:

| Model | Dimension | License | Size GB | Role |
|---|---:|---|---:|---|
| `BAAI/bge-small-en` | 384 | MIT | 0.13 | Small baseline and selected first-pass model. |
| `BAAI/bge-base-en-v1.5` | 768 | MIT | 0.21 | Stronger BGE comparison candidate. |
| `sentence-transformers/all-MiniLM-L6-v2` | 384 | Apache-2.0 | 0.09 | Common lightweight baseline. |

The benchmark runner records the live FastEmbed model inventory in:

```text
docs/design/experiments/embedding-benchmark/dt010-run-001/embedding-model-inventory.json
```

## Runner Behavior

The runner:

1. Loads DT005 hybrid chunks.
2. Parses DT006 positive golden cases and expected chunk/source targets.
3. Creates one clean in-memory Qdrant collection per candidate model.
4. Embeds all chunks with the candidate model.
5. Upserts chunk vectors and payload metadata into Qdrant.
6. Embeds each golden question.
7. Searches top 5 results.
8. Scores expected chunk/source retrieval.
9. Records latency, vector dimension, model size, and ranking details.

Command:

```powershell
Set-Location "C:\tmp\rag-dt010-embedding-benchmark-fixture\pilot_phase2_poc\rag-service"
uv run --with fastembed --with qdrant-client python "docs/design/experiments/embedding-benchmark/run_embedding_benchmark.py"
```

## Metrics

The benchmark records:

- Recall@1, Recall@3, Recall@5 for expected chunks
- MRR for expected chunks
- Source Recall@1, Source Recall@3, Source Recall@5
- Source MRR
- chunk embedding total and average latency
- query embedding latency
- Qdrant search latency
- vector dimension
- model size
- license
- top-k chunk IDs, source IDs, headings, and scores

## Run Result

`dt010-run-001` selected:

```text
BAAI/bge-small-en
```

Summary:

| Model | Recall@1 | Recall@3 | Recall@5 | MRR | Source@1 | Query p50 ms | Search p50 ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| `BAAI/bge-small-en` | 0.875 | 1.000 | 1.000 | 0.917 | 1.000 | 2.78 | 0.78 |
| `BAAI/bge-base-en-v1.5` | 0.875 | 1.000 | 1.000 | 0.917 | 1.000 | 10.38 | 1.40 |
| `sentence-transformers/all-MiniLM-L6-v2` | 0.875 | 0.875 | 0.875 | 0.875 | 1.000 | 6.23 | 0.76 |

`BAAI/bge-small-en` and `BAAI/bge-base-en-v1.5` tied on expected chunk
retrieval quality. The smaller model was selected because it had the same
Recall@3, Recall@5, MRR, and source recall while being smaller, lower
dimension, and faster on query embedding in this run.

`sentence-transformers/all-MiniLM-L6-v2` is rejected for the first-pass adapter
default because it missed the expected chunk in the top five for one of the
eight benchmark cases.

## Decision

| Model | Decision | Rationale |
|---|---|---|
| `BAAI/bge-small-en` | Selected | Best quality/latency/size tradeoff in `dt010-run-001`; 384 dimensions simplify local storage and tests. |
| `BAAI/bge-base-en-v1.5` | Deferred | Same retrieval quality as selected model, but slower and larger. Keep as comparison candidate if later corpus complexity requires it. |
| `sentence-transformers/all-MiniLM-L6-v2` | Rejected for default | Lightweight, but lower Recall@3/Recall@5 and MRR on this fixture. |

## Build Task Handoff

`RAG-BT011` should implement the embedding adapter with a deterministic unit-test
adapter and a configurable FastEmbed-backed adapter. The first-pass real model
configuration should use:

```text
embedding_provider = fastembed
embedding_model_name = BAAI/bge-small-en
embedding_dimension = 384
embedding_distance = cosine
```

`RAG-BT012` should preserve the selected model name, version/source, dimension,
distance metric, and chunk lineage in ingestion reports.

`RAG-BT013` should use the DT006 positive expected chunks and selected embedding
model as the semantic retrieval baseline.

`RAG-BT014` should compare hybrid retrieval against the same DT006 expected
chunks and should not replace the selected embedding model without benchmark
evidence.

`RAG-DT014` should still decide Docker/service Qdrant and CI behavior. DT010
only proves the local benchmark fixture.

`RAG-BT019` should ingest the DT010 run artifacts as the embedding/retrieval
baseline evidence for later evaluation reporting.

## Artifacts

```text
docs/design/experiments/embedding-benchmark/run_embedding_benchmark.py
docs/design/experiments/embedding-benchmark/dt010-run-001/embedding-model-inventory.json
docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-fixture.jsonl
docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-results.jsonl
docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-summary.json
docs/design/experiments/embedding-benchmark/dt010-run-001/benchmark-summary.md
```

## Deferred Work

- Confirm service-backed Qdrant behavior in `RAG-DT014`.
- Implement the runtime adapter in `RAG-BT011`.
- Re-run embedding benchmarks when the source corpus expands beyond the first
  DT012 candidate set.
- Reconsider `BAAI/bge-base-en-v1.5` if later source diversity creates
  measurable retrieval gaps.
