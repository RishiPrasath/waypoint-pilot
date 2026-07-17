# RAG-DT010 Embedding Benchmark Summary

Run ID: `dt010-run-001`
Generated: `2026-07-17T13:32:12.774514+00:00`

## Outcome

Selected first-pass embedding model: `BAAI/bge-small-en`.

The decision is based on expected chunk retrieval first, then expected
source retrieval, then local latency and model-size fit.

## Model Results

| Model | Recall@1 | Recall@3 | Recall@5 | MRR | Source@1 | Query p50 ms | Search p50 ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| BAAI/bge-small-en | 0.875 | 1.000 | 1.000 | 0.917 | 1.000 | 2.78 | 0.78 |
| BAAI/bge-base-en-v1.5 | 0.875 | 1.000 | 1.000 | 0.917 | 1.000 | 10.38 | 1.40 |
| sentence-transformers/all-MiniLM-L6-v2 | 0.875 | 0.875 | 0.875 | 0.875 | 1.000 | 6.23 | 0.76 |

## Fixture

- Chunks indexed: `10`
- Golden retrieval cases: `8`
- Query source: `docs/evaluation/golden-questions.md`
- Chunk source: `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl`

## Notes

- Qdrant ran in local in-memory mode through `QdrantClient(":memory:")`.
- This run does not replace RAG-DT014 service-backed Qdrant CI strategy.
- All source records remain candidate/review material until later KB promotion.
