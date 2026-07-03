package com.waypoint.partnersource.assignment.domain;

public record DeliveryAssignment(
    String assignmentId,
    String orderId,
    String driverId,
    AssignmentStatus status
) {
}
