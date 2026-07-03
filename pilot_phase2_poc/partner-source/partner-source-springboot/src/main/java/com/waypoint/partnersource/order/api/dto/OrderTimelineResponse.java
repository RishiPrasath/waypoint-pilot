package com.waypoint.partnersource.order.api.dto;

import java.util.List;

public record OrderTimelineResponse(
        String orderId,
        List<TimelineEventResponse> items,
        int page,
        int pageSize,
        int totalItems
) {
}
