package com.waypoint.partnersource.shared.health;

public record ReadinessResponse(String status, String service, ReadinessChecks checks) {
}