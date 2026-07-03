package com.waypoint.partnersource.order.api.dto;

import com.waypoint.partnersource.order.domain.ActorType;
import com.waypoint.partnersource.order.domain.OrderStatus;
import java.time.OffsetDateTime;

public record TimelineEventResponse(
        String eventId,
        OrderStatus status,
        String statusLabel,
        OffsetDateTime occurredAt,
        ActorType actorType,
        String actorId,
        LocationSnapshotResponse location,
        String note
) {
}
