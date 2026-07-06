from scripts.comparer import compare_scenario
from scripts.matrix import PROBLEM_DETAIL_FIELDS, SCENARIOS
from scripts.models import ResponseSnapshot


ERROR_SCENARIOS = {scenario.id: scenario for scenario in SCENARIOS if scenario.expected_status >= 400}


def test_error_matrix_covers_default_http_checklist_errors() -> None:
    expected_ids = {
        "CSA-01-order-status-missing-order",
        "CSA-01-order-status-invalid-id",
        "CSA-03-order-timeline-missing-order",
        "CSA-03-order-timeline-invalid-page",
        "AUTH-01-missing-token-order-status",
        "AUTH-02-invalid-token-order-status",
        "AUTH-04-driver-other-profile-denied",
        "AUTH-06-driver-other-assignments-denied",
        "AUTH-11-driver-spoofed-body-driver-denied",
        "AUTH-13-csa-status-event-write-denied",
        "AUTH-18-unknown-driver-login",
        "DA-01-driver-profile-invalid-id",
        "DA-02-driver-assignments-invalid-status-filter",
        "DA-02-driver-assignments-invalid-page",
        "DA-05-status-event-unassigned-driver",
        "DA-05-status-event-invalid-transition",
        "DA-05-status-event-future-occurred-at",
        "DA-05-status-event-missing-order",
        "DA-05-status-event-malformed-body",
    }

    assert set(ERROR_SCENARIOS) == expected_ids


def test_error_scenarios_require_problem_detail_shape() -> None:
    for scenario in ERROR_SCENARIOS.values():
        assert scenario.required_paths == PROBLEM_DETAIL_FIELDS


def test_matching_error_response_passes() -> None:
    scenario = ERROR_SCENARIOS["CSA-01-order-status-missing-order"]
    body = {
        "type": "https://waypoint.local/problems/order-not-found",
        "title": "Order not found",
        "status": 404,
        "detail": "No order exists for orderId ORD-9999.",
        "instance": "/api/v1/orders/ORD-9999/status",
        "errorCode": "ORDER_NOT_FOUND",
        "correlationId": "local-dev",
    }

    result = compare_scenario(
        scenario,
        ResponseSnapshot(status_code=404, body=body),
        ResponseSnapshot(status_code=404, body=body),
    )

    assert result.status == "PASS"
