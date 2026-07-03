from app.domain.orders import OrderStatus
from app.domain.policies import StatusTransitionPolicy


def test_out_for_delivery_can_transition_to_delivered() -> None:
    policy = StatusTransitionPolicy()
    assert policy.can_transition(
        OrderStatus.OUT_FOR_DELIVERY,
        OrderStatus.DELIVERED,
    ) is True


def test_delivered_cannot_transition_back_to_out_for_delivery() -> None:
    policy = StatusTransitionPolicy()
    assert policy.can_transition(
        OrderStatus.DELIVERED,
        OrderStatus.OUT_FOR_DELIVERY,
    ) is False


def test_confirmed_can_transition_to_picked_up() -> None:
    policy = StatusTransitionPolicy()
    assert policy.can_transition(
        OrderStatus.CONFIRMED,
        OrderStatus.PICKED_UP,
    ) is True


def test_delivery_attempted_cannot_transition_to_out_for_delivery() -> None:
    policy = StatusTransitionPolicy()
    assert policy.can_transition(
        OrderStatus.DELIVERY_ATTEMPTED,
        OrderStatus.OUT_FOR_DELIVERY,
    ) is False


def test_terminal_statuses_have_no_outgoing_transitions() -> None:
    policy = StatusTransitionPolicy()

    assert policy.can_transition(
        OrderStatus.DELIVERED,
        OrderStatus.CANCELLED,
    ) is False

    assert policy.can_transition(
        OrderStatus.CANCELLED,
        OrderStatus.CREATED,
    ) is False

def test_created_cannot_be_delivered() -> None:
    policy = StatusTransitionPolicy()

    assert policy.can_transition(
        OrderStatus.CREATED,
        OrderStatus.DELIVERED
    ) is False