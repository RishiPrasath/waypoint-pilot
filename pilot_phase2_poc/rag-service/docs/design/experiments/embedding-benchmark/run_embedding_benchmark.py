"""Run the RAG-DT010 local embedding benchmark.

This is a design-time runner. It uses the real DT005 chunk fixture and DT006
golden questions, embeds them with local FastEmbed models, indexes them in
Qdrant local in-memory mode, and writes non-secret result artifacts.
"""

from __future__ import annotations

import hashlib
import json
import platform
import re
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastembed import TextEmbedding
from qdrant_client import QdrantClient, models


RUN_ID = "dt010-run-001"
COLLECTION_NAME = "dt010_embedding_benchmark"
TOP_K = 5

PREFERRED_MODELS = [
    "BAAI/bge-small-en",
    "BAAI/bge-base-en-v1.5",
    "sentence-transformers/all-MiniLM-L6-v2",
]


@dataclass(frozen=True)
class GoldenCase:
    case_id: str
    question: str
    expected_source: str
    expected_chunk_ids: tuple[str, ...]
    question_type: str


def service_root() -> Path:
    return Path(__file__).resolve().parents[4]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def extract_code_block(section: str, label: str) -> str | None:
    pattern = rf"{re.escape(label)}:\s*```text\s*(.*?)\s*```"
    match = re.search(pattern, section, re.DOTALL)
    if not match:
        return None
    return match.group(1).strip()


def extract_table_value(section: str, field: str) -> str | None:
    pattern = rf"\|\s*`?{re.escape(field)}`?\s*\|\s*`?([^`|\n]+?)`?\s*\|"
    match = re.search(pattern, section)
    if not match:
        return None
    value = match.group(1).strip()
    if value.lower() in {"none", "null", ""}:
        return None
    return value


def load_golden_cases(path: Path) -> list[GoldenCase]:
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?=^### `GQ-\d+`)", text, flags=re.MULTILINE)
    cases: list[GoldenCase] = []

    for part in parts:
        heading = re.match(r"^### `(GQ-\d+)`", part)
        if not heading:
            continue
        case_id = heading.group(1)
        question = extract_code_block(part, "Question")
        expected_source = extract_table_value(
            part, "approved_source"
        ) or extract_table_value(part, "document_id")
        chunk_id = extract_table_value(part, "chunk_id")
        secondary_chunk_id = extract_table_value(part, "secondary_chunk_id")
        question_type_match = re.search(r"Question type:\s*(.+)", part)
        question_type = (
            question_type_match.group(1).strip() if question_type_match else "unknown"
        )

        expected_chunk_ids = tuple(
            chunk
            for chunk in (chunk_id, secondary_chunk_id)
            if chunk and chunk != "none"
        )

        if question and expected_source and expected_chunk_ids:
            cases.append(
                GoldenCase(
                    case_id=case_id,
                    question=question,
                    expected_source=expected_source,
                    expected_chunk_ids=expected_chunk_ids,
                    question_type=question_type,
                )
            )

    return cases


def supported_model_index() -> dict[str, dict[str, Any]]:
    supported = TextEmbedding.list_supported_models()
    return {item["model"]: item for item in supported}


def select_candidate_models(index: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for model_name in PREFERRED_MODELS:
        item = index.get(model_name)
        if item:
            selected.append(item)
    if selected:
        return selected

    text_models = [
        item
        for item in index.values()
        if "Text embeddings" in str(item.get("description", ""))
        and "English" in str(item.get("description", ""))
    ]
    return sorted(text_models, key=lambda item: float(item.get("size_in_GB") or 99.0))[
        :2
    ]


def embedding_dimension(embedding_model: TextEmbedding, sample_text: str) -> int:
    vector = next(iter(embedding_model.embed([sample_text])))
    return len(vector)


def create_collection(client: QdrantClient, vector_size: int) -> None:
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=vector_size, distance=models.Distance.COSINE
        ),
    )


def query_points(client: QdrantClient, query_vector: list[float]) -> list[Any]:
    if hasattr(client, "query_points"):
        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=TOP_K,
            with_payload=True,
        )
        return list(response.points)
    return list(
        client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=TOP_K,
            with_payload=True,
        )
    )


def percentile(values: list[float], percent: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    if len(values) == 1:
        return values[0]
    rank = (len(values) - 1) * percent
    lower = int(rank)
    upper = min(lower + 1, len(values) - 1)
    weight = rank - lower
    return values[lower] * (1 - weight) + values[upper] * weight


def score_case(case: GoldenCase, hits: list[Any]) -> dict[str, Any]:
    hit_payloads = [hit.payload or {} for hit in hits]
    hit_chunk_ids = [payload.get("chunk_id") for payload in hit_payloads]
    hit_sources = [payload.get("document_id") for payload in hit_payloads]
    expected_chunks = set(case.expected_chunk_ids)

    first_expected_rank = None
    first_source_rank = None
    for index, payload in enumerate(hit_payloads, start=1):
        if first_expected_rank is None and payload.get("chunk_id") in expected_chunks:
            first_expected_rank = index
        if (
            first_source_rank is None
            and payload.get("document_id") == case.expected_source
        ):
            first_source_rank = index

    return {
        "case_id": case.case_id,
        "question": case.question,
        "question_type": case.question_type,
        "expected_source": case.expected_source,
        "expected_chunk_ids": list(case.expected_chunk_ids),
        "top_k_chunk_ids": hit_chunk_ids,
        "top_k_sources": hit_sources,
        "expected_chunk_rank": first_expected_rank,
        "expected_source_rank": first_source_rank,
        "expected_chunk_match_at_1": first_expected_rank == 1,
        "expected_chunk_match_at_3": bool(
            first_expected_rank and first_expected_rank <= 3
        ),
        "expected_chunk_match_at_5": bool(
            first_expected_rank and first_expected_rank <= 5
        ),
        "expected_source_match_at_1": first_source_rank == 1,
        "expected_source_match_at_3": bool(
            first_source_rank and first_source_rank <= 3
        ),
        "expected_source_match_at_5": bool(
            first_source_rank and first_source_rank <= 5
        ),
        "reciprocal_rank": 1 / first_expected_rank if first_expected_rank else 0.0,
        "source_reciprocal_rank": 1 / first_source_rank if first_source_rank else 0.0,
        "top_hits": [
            {
                "rank": index,
                "score": getattr(hit, "score", None),
                "chunk_id": payload.get("chunk_id"),
                "document_id": payload.get("document_id"),
                "heading_path": payload.get("heading_path"),
                "source_uri": payload.get("source_uri"),
            }
            for index, (hit, payload) in enumerate(zip(hits, hit_payloads), start=1)
        ],
    }


def summarize_model(model_name: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    case_rows = [row for row in rows if row["model_name"] == model_name]
    count = len(case_rows) or 1
    query_latencies = [row["query_embedding_ms"] for row in case_rows]
    search_latencies = [row["qdrant_search_ms"] for row in case_rows]
    return {
        "model_name": model_name,
        "case_count": len(case_rows),
        "recall_at_1": sum(row["expected_chunk_match_at_1"] for row in case_rows)
        / count,
        "recall_at_3": sum(row["expected_chunk_match_at_3"] for row in case_rows)
        / count,
        "recall_at_5": sum(row["expected_chunk_match_at_5"] for row in case_rows)
        / count,
        "source_recall_at_1": sum(
            row["expected_source_match_at_1"] for row in case_rows
        )
        / count,
        "source_recall_at_3": sum(
            row["expected_source_match_at_3"] for row in case_rows
        )
        / count,
        "source_recall_at_5": sum(
            row["expected_source_match_at_5"] for row in case_rows
        )
        / count,
        "mrr": sum(row["reciprocal_rank"] for row in case_rows) / count,
        "source_mrr": sum(row["source_reciprocal_rank"] for row in case_rows) / count,
        "query_embedding_p50_ms": percentile(query_latencies, 0.50),
        "query_embedding_p95_ms": percentile(query_latencies, 0.95),
        "qdrant_search_p50_ms": percentile(search_latencies, 0.50),
        "qdrant_search_p95_ms": percentile(search_latencies, 0.95),
    }


def write_summary(path: Path, payload: dict[str, Any]) -> None:
    model_summaries = payload["model_summaries"]
    selected = payload["selected_model"]
    lines = [
        "# RAG-DT010 Embedding Benchmark Summary",
        "",
        f"Run ID: `{RUN_ID}`",
        f"Generated: `{payload['generated_at']}`",
        "",
        "## Outcome",
        "",
        f"Selected first-pass embedding model: `{selected}`.",
        "",
        "The decision is based on expected chunk retrieval first, then expected",
        "source retrieval, then local latency and model-size fit.",
        "",
        "## Model Results",
        "",
        "| Model | Recall@1 | Recall@3 | Recall@5 | MRR | Source@1 | Query p50 ms | Search p50 ms |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in model_summaries:
        lines.append(
            "| {model_name} | {recall_at_1:.3f} | {recall_at_3:.3f} | {recall_at_5:.3f} | "
            "{mrr:.3f} | {source_recall_at_1:.3f} | {query_embedding_p50_ms:.2f} | "
            "{qdrant_search_p50_ms:.2f} |".format(**item)
        )
    lines.extend(
        [
            "",
            "## Fixture",
            "",
            f"- Chunks indexed: `{payload['chunk_count']}`",
            f"- Golden retrieval cases: `{payload['case_count']}`",
            "- Query source: `docs/evaluation/golden-questions.md`",
            "- Chunk source: `docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl`",
            "",
            "## Notes",
            "",
            '- Qdrant ran in local in-memory mode through `QdrantClient(":memory:")`.',
            "- This run does not replace RAG-DT014 service-backed Qdrant CI strategy.",
            "- All source records remain candidate/review material until later KB promotion.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    root = service_root()
    run_dir = root / "docs/design/experiments/embedding-benchmark" / RUN_ID
    chunk_path = (
        root
        / "docs/design/experiments/chunking/dt005-run-001/chunks-hybrid-structure-recursive-v1.jsonl"
    )
    golden_path = root / "docs/evaluation/golden-questions.md"

    chunks = read_jsonl(chunk_path)
    cases = load_golden_cases(golden_path)
    supported_index = supported_model_index()
    candidates = select_candidate_models(supported_index)

    if not chunks:
        raise RuntimeError(f"No chunks found: {chunk_path}")
    if not cases:
        raise RuntimeError(f"No benchmarkable golden cases found: {golden_path}")
    if not candidates:
        raise RuntimeError("No FastEmbed candidate models were found")

    inventory = {
        "run_id": RUN_ID,
        "generated_at": datetime.now(UTC).isoformat(),
        "environment": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "qdrant_mode": "local_in_memory",
            "qdrant_client": 'QdrantClient(":memory:")',
        },
        "preferred_models": PREFERRED_MODELS,
        "candidate_models": candidates,
        "available_supported_model_count": len(supported_index),
    }
    write_json(run_dir / "embedding-model-inventory.json", inventory)

    fixture_rows = [
        {
            "run_id": RUN_ID,
            "case_id": case.case_id,
            "question": case.question,
            "question_type": case.question_type,
            "expected_source": case.expected_source,
            "expected_chunk_ids": list(case.expected_chunk_ids),
        }
        for case in cases
    ]
    write_jsonl(run_dir / "benchmark-fixture.jsonl", fixture_rows)

    result_rows: list[dict[str, Any]] = []
    chunk_texts = [chunk["text"] for chunk in chunks]

    for candidate in candidates:
        model_name = candidate["model"]
        embedding_model = TextEmbedding(model_name=model_name)
        dimension = embedding_dimension(embedding_model, chunk_texts[0])
        client = QdrantClient(":memory:")
        create_collection(client, dimension)

        start = time.perf_counter()
        chunk_vectors = [list(vector) for vector in embedding_model.embed(chunk_texts)]
        chunk_embedding_ms = (time.perf_counter() - start) * 1000

        points = [
            models.PointStruct(
                id=index,
                vector=vector,
                payload={
                    "chunk_id": chunk["chunk_id"],
                    "document_id": chunk["document_id"],
                    "snapshot_id": chunk["snapshot_id"],
                    "heading_path": chunk["heading_path"],
                    "chunk_strategy": chunk["chunk_strategy"],
                    "candidate_sha256": chunk["candidate_sha256"],
                    "source_uri": chunk["source_uri"],
                    "source_lineage": chunk["source_lineage"],
                    "retrieval_namespace": chunk["retrieval_namespace"],
                    "reuse_mode": chunk["reuse_mode"],
                    "license_sensitive": chunk["license_sensitive"],
                    "text_hash": hashlib.sha256(
                        chunk["text"].encode("utf-8")
                    ).hexdigest(),
                },
            )
            for index, (chunk, vector) in enumerate(zip(chunks, chunk_vectors), start=1)
        ]
        client.upsert(collection_name=COLLECTION_NAME, points=points)

        for case in cases:
            query_start = time.perf_counter()
            query_vector = list(next(iter(embedding_model.embed([case.question]))))
            query_embedding_ms = (time.perf_counter() - query_start) * 1000

            search_start = time.perf_counter()
            hits = query_points(client, query_vector)
            qdrant_search_ms = (time.perf_counter() - search_start) * 1000

            score = score_case(case, hits)
            result_rows.append(
                {
                    "run_id": RUN_ID,
                    "model_name": model_name,
                    "model_dimension": dimension,
                    "model_size_in_gb": candidate.get("size_in_GB"),
                    "model_license": candidate.get("license"),
                    "chunk_embedding_total_ms": chunk_embedding_ms,
                    "chunk_embedding_avg_ms": chunk_embedding_ms / len(chunks),
                    "query_embedding_ms": query_embedding_ms,
                    "qdrant_search_ms": qdrant_search_ms,
                    **score,
                }
            )

    write_jsonl(run_dir / "benchmark-results.jsonl", result_rows)

    model_summaries = [
        summarize_model(candidate["model"], result_rows) for candidate in candidates
    ]
    model_summaries = sorted(
        model_summaries,
        key=lambda item: (
            item["recall_at_1"],
            item["recall_at_3"],
            item["recall_at_5"],
            item["mrr"],
            item["source_recall_at_1"],
            -item["query_embedding_p50_ms"],
        ),
        reverse=True,
    )
    selected_model = model_summaries[0]["model_name"]

    summary_payload = {
        "run_id": RUN_ID,
        "generated_at": datetime.now(UTC).isoformat(),
        "selected_model": selected_model,
        "model_summaries": model_summaries,
        "chunk_count": len(chunks),
        "case_count": len(cases),
    }
    write_json(run_dir / "benchmark-summary.json", summary_payload)
    write_summary(run_dir / "benchmark-summary.md", summary_payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
