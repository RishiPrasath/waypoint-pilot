from app.domain.assignments import DeliveryAssignmentStatus
from app.repositories.assignments import InMemoryAssignmentRepository
from app.seed.loader import load_seed_data


def test_find_active_assignments_for_driver() -> None:
    repo = InMemoryAssignmentRepository(load_seed_data())

    assignments = repo.find_by_driver_id("DRV-2001")

    assert [assignment.assignment_id for assignment in assignments] == [
        "ASN-3001",
        "ASN-3002",
    ]
    assert [assignment.order_id for assignment in assignments] == [
        "ORD-1001",
        "ORD-1002",
    ]


def test_available_driver_with_no_assignments_returns_empty_list() -> None:
    repo = InMemoryAssignmentRepository(load_seed_data())

    assert repo.find_by_driver_id("DRV-2003") == []


def test_completed_assignment_exists_but_is_not_active_driver_work() -> None:
    repo = InMemoryAssignmentRepository(load_seed_data())

    all_assignments = repo.find_all()
    completed = [
        assignment
        for assignment in all_assignments
        if assignment.assignment_id == "ASN-3003"
    ]

    assert completed[0].status == DeliveryAssignmentStatus.COMPLETED
    assert "ASN-3003" not in [
        assignment.assignment_id
        for assignment in repo.find_by_driver_id("DRV-2001")
    ]


def test_completed_assignment_can_be_found_by_order_id_for_invalid_transition_path() -> None:
    repo = InMemoryAssignmentRepository(load_seed_data())

    assignments = repo.find_by_order_id("ORD-1003")

    assert [assignment.assignment_id for assignment in assignments] == ["ASN-3003"]
    assert assignments[0].status == DeliveryAssignmentStatus.COMPLETED
