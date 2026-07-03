package com.waypoint.partnersource.order.api.dto;

import java.time.OffsetDateTime;

public record DeliveryWindowResponse(OffsetDateTime start, OffsetDateTime end) {
}
