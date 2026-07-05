from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from scripts.models import ResponseSnapshot, Scenario


def request_scenario(base_url: str, scenario: Scenario, timeout: float = 10.0) -> ResponseSnapshot:
    url = urljoin(base_url.rstrip("/") + "/", scenario.path.lstrip("/"))
    data = None
    headers = {
        "Accept": "application/json, application/problem+json",
        "X-Correlation-Id": "local-dev",
    }

    if scenario.body is not None:
        data = json.dumps(scenario.body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(url=url, data=data, headers=headers, method=scenario.method)

    try:
        with urlopen(request, timeout=timeout) as response:
            raw_body = response.read().decode("utf-8")
            return ResponseSnapshot(
                status_code=response.status,
                body=_parse_body(raw_body),
                content_type=response.headers.get("Content-Type", ""),
            )
    except HTTPError as error:
        raw_body = error.read().decode("utf-8")
        return ResponseSnapshot(
            status_code=error.code,
            body=_parse_body(raw_body),
            content_type=error.headers.get("Content-Type", ""),
        )
    except URLError as error:
        return ResponseSnapshot(
            status_code=0,
            body={"error": str(error.reason)},
            error=str(error.reason),
        )


def _parse_body(raw_body: str):
    if not raw_body:
        return None
    try:
        return json.loads(raw_body)
    except json.JSONDecodeError:
        return raw_body
