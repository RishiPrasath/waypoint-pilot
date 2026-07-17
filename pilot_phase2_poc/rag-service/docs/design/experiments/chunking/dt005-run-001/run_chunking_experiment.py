from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable


RUN_ID = "dt005-run-001"
QUEUE_NAME = "local_design_experiment"
FIXED_WINDOW_WORDS = 80
FIXED_WINDOW_OVERLAP = 15
HYBRID_MAX_SECTION_WORDS = 80
HYBRID_OVERLAP_WORDS = 15


@dataclass(frozen=True)
class ManifestRow:
    document_id: str
    snapshot_id: str
    source_uri: str
    candidate_path: str
    reuse_mode: str
    license_sensitive: bool
    retrieval_eligible: bool
    candidate_sha256: str


def service_root() -> Path:
    return Path(__file__).resolve().parents[5]


def clean_cell(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def parse_manifest(path: Path) -> list[ManifestRow]:
    rows: list[ManifestRow] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `APAC-"):
            continue
        cells = [clean_cell(cell) for cell in line.strip("|").split("|")]
        rows.append(
            ManifestRow(
                document_id=cells[0],
                snapshot_id=cells[1],
                source_uri=cells[2],
                candidate_path=cells[3],
                reuse_mode=cells[4],
                license_sensitive=cells[5].lower() == "true",
                retrieval_eligible=cells[6].lower() == "true",
                candidate_sha256=cells[7],
            )
        )
    return rows


def sha256_file_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_file_normalized_text(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def parse_frontmatter_and_body(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    _, frontmatter, body = text.split("---", 2)
    metadata: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata, body.strip()


def normalize_words(text: str) -> list[str]:
    return re.findall(r"\S+", text)


def chunk_text_from_words(words: list[str], size: int, overlap: int) -> Iterable[str]:
    if not words:
        return
    start = 0
    while start < len(words):
        end = min(start + size, len(words))
        yield " ".join(words[start:end])
        if end == len(words):
            break
        start = max(end - overlap, start + 1)


def heading_blocks(markdown: str) -> list[tuple[list[str], str]]:
    blocks: list[tuple[list[str], list[str]]] = []
    heading_path: list[str] = []
    current_lines: list[str] = []

    for line in markdown.splitlines():
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            if current_lines and heading_path:
                blocks.append((heading_path.copy(), current_lines))
                current_lines = []
            level = len(heading.group(1))
            title = heading.group(2).strip()
            heading_path = heading_path[: level - 1] + [title]
            current_lines.append(line)
        else:
            current_lines.append(line)

    if current_lines and heading_path:
        blocks.append((heading_path.copy(), current_lines))

    return [(path, "\n".join(lines).strip()) for path, lines in blocks if "\n".join(lines).strip()]


def base_chunk_record(row: ManifestRow, frontmatter: dict[str, str], strategy: str, index: int) -> dict[str, object]:
    return {
        "run_id": RUN_ID,
        "queue": QUEUE_NAME,
        "job_type": "chunk_candidate",
        "document_id": row.document_id,
        "snapshot_id": row.snapshot_id,
        "source_uri": row.source_uri,
        "candidate_path": row.candidate_path,
        "candidate_sha256": row.candidate_sha256,
        "chunk_strategy": strategy,
        "chunk_index": index,
        "reuse_mode": row.reuse_mode,
        "license_sensitive": row.license_sensitive,
        "retrieval_eligible": row.retrieval_eligible,
        "retrieval_namespace": frontmatter.get("retrieval_namespace", "unknown"),
        "language": frontmatter.get("language", "unknown"),
        "source_lineage": frontmatter.get("source_lineage", "unknown"),
    }


def fixed_window_chunks(row: ManifestRow, frontmatter: dict[str, str], body: str) -> list[dict[str, object]]:
    chunks = []
    for index, text in enumerate(
        chunk_text_from_words(normalize_words(body), FIXED_WINDOW_WORDS, FIXED_WINDOW_OVERLAP),
        start=1,
    ):
        record = base_chunk_record(row, frontmatter, "fixed_window_baseline_v1", index)
        record.update(
            {
                "chunk_id": f"{row.document_id}-{row.snapshot_id}-fw-{index:03d}",
                "heading_path": [],
                "text": text,
                "word_count": len(normalize_words(text)),
            }
        )
        chunks.append(record)
    return chunks


def structure_aware_chunks(row: ManifestRow, frontmatter: dict[str, str], body: str) -> list[dict[str, object]]:
    chunks = []
    for index, (path, text) in enumerate(heading_blocks(body), start=1):
        record = base_chunk_record(row, frontmatter, "structure_aware_v1", index)
        record.update(
            {
                "chunk_id": f"{row.document_id}-{row.snapshot_id}-sa-{index:03d}",
                "heading_path": path,
                "text": text,
                "word_count": len(normalize_words(text)),
            }
        )
        chunks.append(record)
    return chunks


def split_large_section_recursively(text: str, max_words: int, overlap: int) -> list[str]:
    words = normalize_words(text)
    if len(words) <= max_words:
        return [text]

    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()]
    chunks: list[str] = []
    current: list[str] = []

    def current_word_count() -> int:
        return len(normalize_words("\n\n".join(current)))

    for paragraph in paragraphs:
        paragraph_words = normalize_words(paragraph)
        if len(paragraph_words) > max_words:
            if current:
                chunks.append("\n\n".join(current))
                current = []
            chunks.extend(chunk_text_from_words(paragraph_words, max_words, overlap))
            continue

        if current and current_word_count() + len(paragraph_words) > max_words:
            chunks.append("\n\n".join(current))
            current = []

        current.append(paragraph)

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def hybrid_structure_recursive_chunks(row: ManifestRow, frontmatter: dict[str, str], body: str) -> list[dict[str, object]]:
    chunks = []
    chunk_index = 1
    for path, text in heading_blocks(body):
        section_parts = split_large_section_recursively(
            text,
            max_words=HYBRID_MAX_SECTION_WORDS,
            overlap=HYBRID_OVERLAP_WORDS,
        )
        for part_index, part in enumerate(section_parts, start=1):
            record = base_chunk_record(row, frontmatter, "hybrid_structure_recursive_v1", chunk_index)
            record.update(
                {
                    "chunk_id": f"{row.document_id}-{row.snapshot_id}-hsr-{chunk_index:03d}",
                    "heading_path": path,
                    "section_part_index": part_index,
                    "section_part_count": len(section_parts),
                    "recursive_split_applied": len(section_parts) > 1,
                    "max_section_words": HYBRID_MAX_SECTION_WORDS,
                    "overlap_words": HYBRID_OVERLAP_WORDS,
                    "text": part,
                    "word_count": len(normalize_words(part)),
                }
            )
            chunks.append(record)
            chunk_index += 1
    return chunks


def write_jsonl(path: Path, records: Iterable[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def comparison_report(
    queue_items: list[dict[str, object]],
    fixed_chunks: list[dict[str, object]],
    structure_chunks: list[dict[str, object]],
    hybrid_chunks: list[dict[str, object]],
) -> str:
    fixed_by_doc: dict[str, list[dict[str, object]]] = {}
    structure_by_doc: dict[str, list[dict[str, object]]] = {}
    hybrid_by_doc: dict[str, list[dict[str, object]]] = {}
    for chunk in fixed_chunks:
        fixed_by_doc.setdefault(str(chunk["document_id"]), []).append(chunk)
    for chunk in structure_chunks:
        structure_by_doc.setdefault(str(chunk["document_id"]), []).append(chunk)
    for chunk in hybrid_chunks:
        hybrid_by_doc.setdefault(str(chunk["document_id"]), []).append(chunk)

    lines = [
        "# DT005 Chunking Experiment Comparison Report",
        "",
        f"Run ID: `{RUN_ID}`",
        f"Generated: `{datetime.now(UTC).isoformat(timespec='seconds')}`",
        "",
        "## Queue Summary",
        "",
        "| Document ID | Status | Reason |",
        "|---|---|---|",
    ]
    for item in queue_items:
        lines.append(
            f"| `{item['document_id']}` | `{item['status']}` | {item['reason']} |"
        )

    lines.extend(
        [
            "",
            "## Strategy Output Counts",
            "",
            "| Document ID | Fixed-window chunks | Structure-aware chunks | Hybrid structure-recursive chunks | Recursive split applied? |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for document_id in sorted(set(fixed_by_doc) | set(structure_by_doc) | set(hybrid_by_doc)):
        hybrid_doc_chunks = hybrid_by_doc.get(document_id, [])
        recursive_applied = any(chunk.get("recursive_split_applied") for chunk in hybrid_doc_chunks)
        lines.append(
            f"| `{document_id}` | {len(fixed_by_doc.get(document_id, []))} | {len(structure_by_doc.get(document_id, []))} | {len(hybrid_doc_chunks)} | `{str(recursive_applied).lower()}` |"
        )

    lines.extend(
        [
            "",
            "## Observations",
            "",
            "- `fixed_window_baseline_v1` is deterministic and simple, but it can split candidate sections without regard to source intent.",
            "- `structure_aware_v1` preserves heading context and keeps review notes separate from source-derived notes.",
            "- `hybrid_structure_recursive_v1` preserves heading context and recursively splits oversized sections by paragraph/word boundaries.",
            "- The current first-pass candidates are short; only `APAC-001` exercises the recursive fallback under the 80-word experiment cap.",
            "- `APAC-215` is intentionally skipped because it is metadata-only and license-sensitive.",
            "",
            "## Chosen Strategy",
            "",
            "`hybrid_structure_recursive_v1` is the chosen strategy for `RAG-BT009` implementation.",
            "",
            "## Rejected Alternative",
            "",
            "`fixed_window_baseline_v1` is rejected as the default because it weakens citation precision and can detach procedural context from source lineage. `structure_aware_v1` is useful but incomplete because a single large heading section can become too broad for retrieval.",
            "",
            "## Retrieval Impact",
            "",
            "Hybrid structure-recursive chunks should improve retrieval precision by keeping heading paths and source lineage while preventing large sections from becoming overly broad chunks. Downstream retrieval tests should assert both semantic match and source metadata integrity.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    root = service_root()
    run_dir = Path(__file__).resolve().parent
    manifest_path = root / "knowledge_base" / "snapshots" / "first-pass-snapshot-manifest.md"
    rows = parse_manifest(manifest_path)

    queue_items: list[dict[str, object]] = []
    fixed_chunks: list[dict[str, object]] = []
    structure_chunks: list[dict[str, object]] = []
    hybrid_chunks: list[dict[str, object]] = []

    for row in rows:
        candidate_path = root / row.candidate_path
        raw_checkout_hash = sha256_file_bytes(candidate_path)
        normalized_text_hash = sha256_file_normalized_text(candidate_path)
        hash_verified = normalized_text_hash == row.candidate_sha256
        status = "queued"
        reason = "ready for chunking"
        if not hash_verified:
            status = "failed"
            reason = "candidate SHA-256 does not match manifest"
        elif row.license_sensitive or row.reuse_mode == "cite_only":
            status = "skipped"
            reason = "metadata-only or license-sensitive source"

        queue_item = {
            "run_id": RUN_ID,
            "queue": QUEUE_NAME,
            "job_type": "chunk_candidate",
            "document_id": row.document_id,
            "snapshot_id": row.snapshot_id,
            "candidate_path": row.candidate_path,
            "candidate_sha256": row.candidate_sha256,
            "raw_checkout_sha256": raw_checkout_hash,
            "normalized_text_sha256": normalized_text_hash,
            "hash_verified": hash_verified,
            "reuse_mode": row.reuse_mode,
            "license_sensitive": row.license_sensitive,
            "retrieval_eligible": row.retrieval_eligible,
            "status": status,
            "reason": reason,
        }
        queue_items.append(queue_item)

        if status != "queued":
            continue

        queue_item["status"] = "loaded"
        text = candidate_path.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter_and_body(text)
        queue_item["status"] = "hash_verified"
        queue_item["status"] = "parsed"
        fixed_chunks.extend(fixed_window_chunks(row, frontmatter, body))
        structure_chunks.extend(structure_aware_chunks(row, frontmatter, body))
        hybrid_chunks.extend(hybrid_structure_recursive_chunks(row, frontmatter, body))
        queue_item["status"] = "reported"
        queue_item["reason"] = "chunk outputs generated"

    (run_dir / "queue-manifest.json").write_text(
        json.dumps(queue_items, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    write_jsonl(run_dir / "chunks-fixed-window-baseline.jsonl", fixed_chunks)
    write_jsonl(run_dir / "chunks-structure-aware-v1.jsonl", structure_chunks)
    write_jsonl(run_dir / "chunks-hybrid-structure-recursive-v1.jsonl", hybrid_chunks)
    (run_dir / "comparison-report.md").write_text(
        comparison_report(queue_items, fixed_chunks, structure_chunks, hybrid_chunks),
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
