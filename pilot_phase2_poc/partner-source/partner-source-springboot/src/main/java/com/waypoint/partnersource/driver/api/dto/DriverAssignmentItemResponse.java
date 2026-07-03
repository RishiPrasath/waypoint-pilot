package com.waypoint.partnersource.driver.api.dto;

import com.waypoint.partnersource.assignment.domain.AssignmentStatus;
import com.waypoint.partnersource.order.api.dto.DeliveryWindowResponse;
import com.waypoint.partnersource.order.domain.OrderStatus;
import java.time.OffsetDateTime;

public record DriverAssignmentItemResponse(
        String assignmentId,
        String orderId,
        AssignmentStatus assignmentStatus,
        OrderStatus currentStatus,
        String recipientName,
        String deliveryAddressSummary,
        DeliveryWindowResponse deliveryWindow,
        OffsetDateTime lastUpdatedAt
) {
}
