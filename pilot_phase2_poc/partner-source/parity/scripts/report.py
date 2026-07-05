from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable

from scripts.models import Mismatch, ResponseSnapshot, Scenario, ScenarioResult


def write_reports(
    parity_root: Path,
    results: list[ScenarioResult],
    *,
    spring_base_url: str,
    fastapi_base_url: str,
) -> None:
    timestamp = datetime.now().astimezone()
    latest_dir = parity_root / "reports" / "latest"
    run_dir = parity_root / "reports" / "runs" / timestamp.strftime("%Y-%m-%dT%H-%M-%S")
    latest_dir.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)

    payload = _json_payload(results, spring_base_url, fastapi_base_url, timestamp.isoformat(timespec="seconds"))
    markdown = _markdown_report(results, spring_base_url, fastapi_base_url, timestamp.isoformat(timespec="seconds"))

    for directory in (latest_dir, run_dir):
        (directory / "parity-report.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        (directory / "parity-report.md").write_text(markdown, encoding="utf-8")


def _json_payload(
    results: list[ScenarioResult],
    spring_base_url: str,
    fastapi_base_url: str,
    timestamp: str,
) -> dict:
    passed = sum(1 for result in results if result.status == "PASS")
    failed = sum(1 for result in results if result.status == "FAIL")
    return {
        "summary": {
            "timestamp": timestamp,
            "springBaseUrl": spring_base_url,
            "fastapiBaseUrl": fastapi_base_url,
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "skipped": 0,
        },
        "results": [_result_to_dict(result) for result in results],
    }


def _result_to_dict(result: ScenarioResult) -> dict:
    return {
        "scenario": _scenario_to_dict(result.scenario),
        "spring": _response_to_dict(result.spring),
        "fastapi": _response_to_dict(result.fastapi),
        "result": result.status,
        "mismatches": [_mismatch_to_dict(mismatch) for mismatch in result.mismatches],
    }


def _scenario_to_dict(scenario: Scenario) -> dict:
    data = asdict(scenario)
    data["body"] = scenario.body
    return data


def _response_to_dict(response: ResponseSnapshot) -> dict:
    return {
        "statusCode": response.status_code,
        "contentType": response.content_type,
        "body": response.body,
        "error": response.error,
    }


def _mismatch_to_dict(mismatch: Mismatch) -> dict:
    return {
        "field": mismatch.field,
        "expected": mismatch.expected,
        "spring": mismatch.spring,
        "fastapi": mismatch.fastapi,
        "message": mismatch.message,
    }


def _markdown_report(
    results: list[ScenarioResult],
    spring_base_url: str,
    fastapi_base_url: str,
    timestamp: str,
) -> str:
    passed = sum(1 for result in results if result.status == "PASS")
    failed = sum(1 for result in results if result.status == "FAIL")
    lines = [
        "# Partner Source Parity Report",
        "",
        "## Summary",
        "",
        f"- Timestamp: `{timestamp}`",
        f"- Spring Boot base URL: `{spring_base_url}`",
        f"- FastAPI base URL: `{fastapi_base_url}`",
        f"- Total scenarios: `{len(results)}`",
        f"- Passed: `{passed}`",
        f"- Failed: `{failed}`",
        "- Skipped: `0`",
        "",
        "## Scenario Results",
        "",
        "| Scenario | Use Case | Method | Path | Expected | Spring Boot | FastAPI | Result |",
        "|---|---|---|---|---:|---:|---:|---|",
    ]

    for result in results:
        scenario = result.scenario
        lines.append(
            "| {scenario} | {use_case} | {method} | `{path}` | {expected} | {spring} | {fastapi} | {status} |".format(
                scenario=scenario.id,
                use_case=scenario.use_case,
                method=scenario.method,
                path=scenario.path,
                expected=scenario.expected_status,
                spring=result.spring.status_code,
                fastapi=result.fastapi.status_code,
                status=result.status,
            )
        )

    failed_results = [result for result in results if result.status == "FAIL"]
    if failed_results:
        lines.extend(["", "## Failure Details", ""])
        for result in failed_results:
            lines.extend(_failure_lines(result))

    lines.append("")
    return "\n".join(lines)


def _failure_lines(result: ScenarioResult) -> Iterable[str]:
    scenario = result.scenario
    yield f"### {scenario.id}"
    yield ""
    yield f"- Use case: `{scenario.use_case}`"
    yield f"- Actor: `{scenario.actor}`"
    yield f"- Intent: {scenario.intent}"
    yield f"- Request: `{scenario.method} {scenario.path}`"
    yield ""
    yield "| Field | Expected | Spring Boot | FastAPI | Message |"
    yield "|---|---|---|---|---|"
    for mismatch in result.mismatches:
        yield "| `{field}` | `{expected}` | `{spring}` | `{fastapi}` | {message} |".format(
            field=mismatch.field,
            expected=_format_cell(mismatch.expected),
            spring=_format_cell(mismatch.spring),
            fastapi=_format_cell(mismatch.fastapi),
            message=mismatch.message,
        )
    yield ""


def _format_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")
