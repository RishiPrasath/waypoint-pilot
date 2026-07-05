import json

from scripts.comparer import compare_scenario
from scripts.matrix import SCENARIOS
from scripts.models import ResponseSnapshot
from scripts.report import write_reports


def test_report_writer_creates_latest_markdown_and_json(tmp_path) -> None:
    scenario = next(item for item in SCENARIOS if item.id == "service-health")
    body = {"status": "UP", "service": "partner-source"}
    result = compare_scenario(
        scenario,
        ResponseSnapshot(status_code=200, body=body),
        ResponseSnapshot(status_code=200, body=body),
    )

    write_reports(
        tmp_path,
        [result],
        spring_base_url="http://localhost:8080",
        fastapi_base_url="http://localhost:8000",
    )

    markdown_path = tmp_path / "reports" / "latest" / "parity-report.md"
    json_path = tmp_path / "reports" / "latest" / "parity-report.json"

    assert markdown_path.exists()
    assert json_path.exists()
    assert "service-health" in markdown_path.read_text(encoding="utf-8")

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["summary"]["total"] == 1
    assert payload["summary"]["passed"] == 1
    assert payload["summary"]["failed"] == 0
