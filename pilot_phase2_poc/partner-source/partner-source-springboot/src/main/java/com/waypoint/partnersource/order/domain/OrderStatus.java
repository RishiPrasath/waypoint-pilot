package com.waypoint.partnersource.order.domain;

public enum OrderStatus {
    CREATED,
    CONFIRMED,
    PICKED_UP,
    IN_TRANSIT,
    OUT_FOR_DELIVERY,
    DELIVERY_ATTEMPTED,
    DELIVERED,
    CANCELLED
}
