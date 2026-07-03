package com.waypoint.partnersource.order.domain;

import java.time.OffsetDateTime;

public record DeliveryOrder(
    String orderId,
    OrderStatus currentStatus,
    String statusLabel,
    String recipientName,
    String deliveryAddressSummary,
    OffsetDateTime estimatedDeliveryAt,
    OffsetDateTime deliveryWindowStart,
    OffsetDateTime deliveryWindowEnd,
    String currentLocation,
    String assignedDriverId,
    String assignedDriverName,
    OffsetDateTime lastUpdatedAt
) {
    public DeliveryOrder withCurrentStatus(OrderStatus status, String label, OffsetDateTime updatedAt) {
        return new DeliveryOrder(
            orderId,
            status,
            label,
            recipientName,
            deliveryAddressSummary,
            estimatedDeliveryAt,
            deliveryWindowStart,
            deliveryWindowEnd,
            currentLocation,
            assignedDriverId,
            assignedDriverName,
            updatedAt
        );
    }
}
