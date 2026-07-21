"""Validate RAG service build-sequence governance invariants.

This script is intentionally lightweight and stdlib-only so it can run in local
checks and GitHub Actions before task PRs are merged.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


SERVICE_ROOT = Path(__file__).resolve().parents[1]
TASK_ROOTS = (
    SERVICE_ROOT / "build-sequence" / "01-setup-tasks",
    SERVICE_ROOT / "build-sequence" / "02-design-tasks",
    SERVICE_ROOT / "build-sequence" / "03-build-tasks",
)
BUILD_TASK_ROOT = SERVICE_ROOT / "build-sequence" / "03-build-tasks"
DESIGN_ROOT = SERVICE_ROOT / "docs" / "design"
NESTED_GITHUB_ROOT = SERVICE_ROOT / ".github"

STATUS_RE = re.compile(r"^Status:\s*(?P<status>.+?)\s*$", re.MULTILINE)
EVIDENCE_RE = re.compile(r"\|\s*Evidence\s*\|\s*`(?P<path>[^`]+)`\s*\|")
SERVICE_REL_PREFIX = "pilot_phase2_poc/rag-service/"
MERGE_READY_EVIDENCE_STATUSES = {"Complete", "Ready for Merge"}


def first_status(markdown: str) -> str | None:
    match = STATUS_RE.search(markdown)
    if match is None:
        return None
    return match.group("status").strip()


def evidence_path(markdown: str) -> Path | None:
    match = EVIDENCE_RE.search(markdown)
    if match is None:
        return None

    raw_path = match.group("path").replace("\\", "/")
    if raw_path.startswith(SERVICE_REL_PREFIX):
        raw_path = raw_path.removeprefix(SERVICE_REL_PREFIX)
    return SERVICE_ROOT / raw_path


def task_files() -> list[Path]:
    files: list[Path] = []
    for root in TASK_ROOTS:
        files.extend(
            path for path in root.rglob("*.md") if not path.name.startswith("00-")
        )
    return sorted(files)


def validate_completed_task_evidence(errors: list[str]) -> None:
    for task_path in task_files():
        task_markdown = task_path.read_text(encoding="utf-8")
        if first_status(task_markdown) != "Complete":
            continue

        evidence = evidence_path(task_markdown)
        rel_task = task_path.relative_to(SERVICE_ROOT)

        if evidence is None:
            errors.append(f"{rel_task}: Complete task has no Evidence row.")
            continue

        rel_evidence = evidence.relative_to(SERVICE_ROOT)
        if not evidence.exists():
            errors.append(f"{rel_task}: evidence file does not exist: {rel_evidence}")
            continue

        evidence_markdown = evidence.read_text(encoding="utf-8")
        evidence_status = first_status(evidence_markdown)
        if evidence_status not in MERGE_READY_EVIDENCE_STATUSES:
            errors.append(
                f"{rel_task}: evidence {rel_evidence} status is "
                f"{evidence_status!r}, expected one of "
                f"{sorted(MERGE_READY_EVIDENCE_STATUSES)!r}."
            )


def validate_final_build_handoffs(errors: list[str]) -> None:
    for task_path in sorted(BUILD_TASK_ROOT.rglob("RAG-BT*.md")):
        markdown = task_path.read_text(encoding="utf-8")
        if "## DT013 Final Design Handoff" not in markdown:
            rel_task = task_path.relative_to(SERVICE_ROOT)
            errors.append(f"{rel_task}: missing DT013 Final Design Handoff.")


def validate_no_nested_github_workflows(errors: list[str]) -> None:
    if not NESTED_GITHUB_ROOT.exists():
        return

    nested_files = sorted(
        path for path in NESTED_GITHUB_ROOT.rglob("*") if path.is_file()
    )
    for nested_file in nested_files:
        rel_file = nested_file.relative_to(SERVICE_ROOT)
        errors.append(
            f"{rel_file}: service-local .github files are inert; "
            "use the repository-root .github directory instead."
        )


def validate_completed_tasks_do_not_keep_placeholder_tests(
    errors: list[str],
) -> None:
    placeholder_patterns = (
        "failing test placeholder",
        "assert False",
    )

    for task_path in task_files():
        markdown = task_path.read_text(encoding="utf-8")
        status = first_status(markdown)
        if status not in {"In Review", "Complete"}:
            continue

        for pattern in placeholder_patterns:
            if pattern in markdown:
                rel_task = task_path.relative_to(SERVICE_ROOT)
                errors.append(f"{rel_task}: {status} task still contains {pattern!r}.")
                break


def validate_design_docs_not_proposed(errors: list[str]) -> None:
    for design_path in sorted(DESIGN_ROOT.rglob("*.md")):
        markdown = design_path.read_text(encoding="utf-8")
        if first_status(markdown) == "Proposed":
            rel_design = design_path.relative_to(SERVICE_ROOT)
            errors.append(f"{rel_design}: design document is still Proposed.")


def main() -> int:
    errors: list[str] = []

    validate_completed_task_evidence(errors)
    validate_final_build_handoffs(errors)
    validate_no_nested_github_workflows(errors)
    validate_completed_tasks_do_not_keep_placeholder_tests(errors)
    validate_design_docs_not_proposed(errors)

    if errors:
        print("Build-sequence governance check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Build-sequence governance check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
