from app.domain.assignments import DeliveryAssignment, DeliveryAssignmentStatus
from app.domain.policies import AssignmentAuthorizationPolicy


def test_driver_can_update_order_through_assigned_assignment() -> None:
    policy = AssignmentAuthorizationPolicy()
    assignments = [
        DeliveryAssignment(
            driver_id="DRV-2001",
            order_id="ORD-1001",
            status=DeliveryAssignmentStatus.ASSIGNED,
        )
    ]

    assert policy.can_driver_update_order(
        "DRV-2001",
        "ORD-1001",
        assignments,
    )


def test_unassigned_driver_cannot_update_order() -> None:
    policy = AssignmentAuthorizationPolicy()
    assignments = [
        DeliveryAssignment(
            driver_id="DRV-2001",
            order_id="ORD-1001",
            status=DeliveryAssignmentStatus.ASSIGNED,
        )
    ]

    assert not policy.can_driver_update_order(
        "DRV-2002",
        "ORD-1001",
        assignments,
    )


def test_completed_assignment_keeps_authorized_for_delivered_order_invalid_transition_path(
    ) -> None:
    policy = AssignmentAuthorizationPolicy()
    assignments = [
        DeliveryAssignment(
            driver_id="DRV-2001",
            order_id="ORD-1003",
            status=DeliveryAssignmentStatus.COMPLETED,
        )
    ]

    assert policy.can_driver_update_order(
        "DRV-2001",
        "ORD-1003",
        assignments,
    )


def test_cancelled_assignment_does_not_authorize_driver() -> None:
    policy = AssignmentAuthorizationPolicy()
    assignments = [
        DeliveryAssignment(
            driver_id="DRV-2001",
            order_id="ORD-1001",
            status=DeliveryAssignmentStatus.CANCELLED,
        )
    ]

    assert not policy.can_driver_update_order(
        "DRV-2001",
        "ORD-1001",
        assignments,
    )
