package com.waypoint.partnersource.assignment.domain;

import java.util.Collection;

public final class AssignmentAuthorizationPolicy {

    public boolean canDriverUpdateOrder(
        String driverId,
        String orderId,
        Collection<DeliveryAssignment> assignments
    ) {
        return assignments.stream()
        .anyMatch(assignment ->
            assignment.driverId().equals(driverId)
            && assignment.orderId().equals(orderId)
            && assignment.status() != AssignmentStatus.CANCELLED
        );
    }
}
