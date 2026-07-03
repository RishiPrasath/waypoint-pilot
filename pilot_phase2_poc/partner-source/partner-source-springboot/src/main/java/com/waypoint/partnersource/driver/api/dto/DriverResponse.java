package com.waypoint.partnersource.driver.api.dto;

import com.waypoint.partnersource.driver.domain.DriverAvailabilityStatus;

public record DriverResponse(
        String driverId,
        String displayName,
        DriverAvailabilityStatus availabilityStatus,
        int activeAssignmentCount
) {
}
