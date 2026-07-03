package com.waypoint.partnersource.order.domain;

import java.time.OffsetDateTime;

public record OrderStatusEvent(
    String eventId,
    String orderId,
    OrderStatus previousStatus,
    OrderStatus newStatus,
    String statusLabel,
    OffsetDateTime occurredAt,
    ActorType actorType,
    String actorId
) {
}
