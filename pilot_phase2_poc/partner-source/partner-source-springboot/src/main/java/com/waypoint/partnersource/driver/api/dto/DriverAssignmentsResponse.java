package com.waypoint.partnersource.driver.api.dto;

import java.util.List;

public record DriverAssignmentsResponse(
        String driverId,
        List<DriverAssignmentItemResponse> items,
        int page,
        int pageSize,
        int totalItems
) {
}
