package com.waypoint.partnersource.order.api.dto;

import com.waypoint.partnersource.order.domain.ActorType;
import com.waypoint.partnersource.order.domain.OrderStatus;
import java.time.OffsetDateTime;

public record StatusEventResponse(
        String eventId,
        String orderId,
        OrderStatus previousStatus,
        OrderStatus newStatus,
        String statusLabel,
        OffsetDateTime occurredAt,
        ActorType actorType,
        String actorId,
        LocationSnapshotResponse location,
        String note,
        Boolean proofOfDeliveryAvailable,
        OrderStatus orderCurrentStatus
) {
}
