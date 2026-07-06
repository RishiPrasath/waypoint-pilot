from scripts.comparer import compare_scenario
from scripts.matrix import SCENARIOS
from scripts.models import ResponseSnapshot


SUCCESS_SCENARIOS = {scenario.id: scenario for scenario in SCENARIOS if scenario.expected_status < 400}


def test_success_matrix_covers_default_http_checklist_successes() -> None:
    expected_ids = {
        "service-health",
        "service-readiness",
        "AUTH-16-demo-driver-login",
        "AUTH-17-demo-csa-login",
        "CSA-02-order-status-happy-path",
        "CSA-03-order-timeline-happy-path",
        "DA-01-driver-profile-happy-path",
        "DA-02-driver-assignments-active-driver",
        "DA-02-driver-assignments-filtered-status",
        "DA-02-driver-assignments-empty-driver",
        "DA-06-status-event-delivered-happy-path",
    }

    assert set(SUCCESS_SCENARIOS) == expected_ids


def test_matching_success_response_passes() -> None:
    scenario = SUCCESS_SCENARIOS["DA-02-driver-assignments-filtered-status"]
    body = {
        "driverId": "DRV-2001",
        "items": [
            {
                "assignmentId": "ASN-3001",
                "orderId": "ORD-1001",
                "assignmentStatus": "ASSIGNED",
                "currentStatus": "OUT_FOR_DELIVERY",
            }
        ],
        "page": 1,
        "pageSize": 20,
        "totalItems": 1,
    }

    result = compare_scenario(
        scenario,
        ResponseSnapshot(status_code=200, body=body),
        ResponseSnapshot(status_code=200, body=body),
    )

    assert result.status == "PASS"
