package com.waypoint.partnersource.driver.domain;

public record DeliveryDriver(
    String driverId,
    String displayName,
    DriverAvailabilityStatus availabilityStatus
) {
}
