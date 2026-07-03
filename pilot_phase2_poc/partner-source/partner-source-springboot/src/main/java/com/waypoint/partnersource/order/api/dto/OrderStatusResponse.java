package com.waypoint.partnersource.order.api.dto;

import com.waypoint.partnersource.order.domain.OrderStatus;
import java.time.OffsetDateTime;

public record OrderStatusResponse(
        String orderId,
        OrderStatus currentStatus,
        String statusLabel,
        LocationSnapshotResponse currentLocation,
        OffsetDateTime estimatedDeliveryAt,
        DeliveryWindowResponse deliveryWindow,
        AssignedDriverSummaryResponse assignedDriver,
        OffsetDateTime lastUpdatedAt
) {
}
