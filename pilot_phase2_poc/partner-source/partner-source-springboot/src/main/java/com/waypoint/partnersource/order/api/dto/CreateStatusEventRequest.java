package com.waypoint.partnersource.order.api.dto;

import com.waypoint.partnersource.order.domain.OrderStatus;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import java.time.OffsetDateTime;

public record CreateStatusEventRequest(
        @NotBlank @Pattern(regexp = "^DRV-[0-9]{4}$") String driverId,
        @NotNull OrderStatus status,
        OffsetDateTime occurredAt,
        LocationSnapshotResponse location,
        @Size(max = 500) String note,
        Boolean proofOfDeliveryAvailable
) {
}
