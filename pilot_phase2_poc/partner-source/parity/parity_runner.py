from __future__ import annotations

import os
import sys
from pathlib import Path

from scripts.comparer import compare_scenario
from scripts.http_client import request_scenario
from scripts.matrix import SCENARIOS
from scripts.report import write_reports


DEFAULT_SPRING_BASE_URL = "http://localhost:8080"
DEFAULT_FASTAPI_BASE_URL = "http://localhost:8000"


def run() -> int:
    spring_base_url = os.environ.get("SPRING_BASE_URL", DEFAULT_SPRING_BASE_URL)
    fastapi_base_url = os.environ.get("FASTAPI_BASE_URL", DEFAULT_FASTAPI_BASE_URL)

    results = []
    for scenario in SCENARIOS:
        spring_response = request_scenario(spring_base_url, scenario)
        fastapi_response = request_scenario(fastapi_base_url, scenario)
        results.append(compare_scenario(scenario, spring_response, fastapi_response))

    write_reports(
        Path(__file__).resolve().parent,
        results,
        spring_base_url=spring_base_url,
        fastapi_base_url=fastapi_base_url,
    )

    failed = [result for result in results if result.status == "FAIL"]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run())
