package com.waypoint.partnersource.order.api.dto;

import java.time.OffsetDateTime;

public record LocationSnapshotResponse(String label, Double latitude, Double longitude, OffsetDateTime capturedAt) {
}
