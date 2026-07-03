package com.waypoint.partnersource.order.domain;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

public class StatusTransitionPolicyTest {

    @Test
    void outForDeliveryCanTransitionToDelivered() {
        var policy = new StatusTransitionPolicy();
        assertTrue(policy.canTransition(OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED));
    }

    @Test
    void deliveredCannotTransitionToOutForDelivery(){
        var policy = new StatusTransitionPolicy();
        assertFalse(policy.canTransition(OrderStatus.DELIVERED,OrderStatus.OUT_FOR_DELIVERY));
    }

    @Test
    void confirmedCanTransitionToPickedUp() {
        var policy = new StatusTransitionPolicy();
        assertTrue(policy.canTransition(OrderStatus.CONFIRMED, OrderStatus.PICKED_UP));
    }

    @Test
    void deliveryAttemptedCannotTransitionToOutForDelivery() {
        var policy = new StatusTransitionPolicy();
        assertFalse(policy.canTransition(OrderStatus.DELIVERY_ATTEMPTED, OrderStatus.OUT_FOR_DELIVERY));
    }

    @Test
    void terminalStatusesHaveNoOutgoingTransitions() {
        var policy = new StatusTransitionPolicy();
        assertFalse(policy.canTransition(OrderStatus.DELIVERED, OrderStatus.CANCELLED));
        assertFalse(policy.canTransition(OrderStatus.CANCELLED, OrderStatus.CREATED));
    }
}
