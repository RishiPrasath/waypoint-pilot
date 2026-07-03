package com.waypoint.partnersource.shared.seed;

import com.waypoint.partnersource.assignment.domain.AssignmentStatus;
import com.waypoint.partnersource.assignment.domain.DeliveryAssignment;
import com.waypoint.partnersource.driver.domain.DeliveryDriver;
import com.waypoint.partnersource.driver.domain.DriverAvailabilityStatus;
import com.waypoint.partnersource.order.domain.ActorType;
import com.waypoint.partnersource.order.domain.DeliveryOrder;
import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.order.domain.OrderStatusEvent;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public final class SeedDataLoader {
    private SeedDataLoader() {
    }

    public static SeedDataStore load() {
        var drivers = Map.of(
            "DRV-2001", new DeliveryDriver("DRV-2001", "A. Kumar", DriverAvailabilityStatus.AVAILABLE),
            "DRV-2002", new DeliveryDriver("DRV-2002", "B. Santos", DriverAvailabilityStatus.UNAVAILABLE),
            "DRV-2003", new DeliveryDriver("DRV-2003", "C. Lee", DriverAvailabilityStatus.AVAILABLE)
        );

        var orders = Map.of(
            "ORD-1001", new DeliveryOrder(
                "ORD-1001",
                OrderStatus.OUT_FOR_DELIVERY,
                "Out for delivery",
                "Jamie Tan",
                "Tampines, Singapore",
                null,
                null,
                null,
                null,
                "DRV-2001",
                "A. Kumar",
                at("2026-07-02T09:00:00")
            ),
            "ORD-1002", new DeliveryOrder(
                "ORD-1002",
                OrderStatus.IN_TRANSIT,
                "In transit",
                "Priya Nair",
                "Jurong East, Singapore",
                null,
                null,
                null,
                null,
                "DRV-2001",
                "A. Kumar",
                at("2026-07-02T08:30:00")
            ),
            "ORD-1003", new DeliveryOrder(
                "ORD-1003",
                OrderStatus.DELIVERED,
                "Delivered",
                "Mei Wong",
                "Woodlands, Singapore",
                null,
                null,
                null,
                null,
                "DRV-2001",
                "A. Kumar",
                at("2026-07-01T18:00:00")
            ),
            "ORD-1004", new DeliveryOrder(
                "ORD-1004",
                OrderStatus.OUT_FOR_DELIVERY,
                "Out for delivery",
                "Reserved Slice 2",
                "Singapore",
                null,
                null,
                null,
                null,
                "DRV-2001",
                "A. Kumar",
                at("2026-07-02T10:00:00")
            )
        );

        var assignments = Map.of(
            "ASN-3001", new DeliveryAssignment("ASN-3001", "ORD-1001", "DRV-2001", AssignmentStatus.ASSIGNED),
            "ASN-3002", new DeliveryAssignment("ASN-3002", "ORD-1002", "DRV-2001", AssignmentStatus.ASSIGNED),
            "ASN-3003", new DeliveryAssignment("ASN-3003", "ORD-1003", "DRV-2001", AssignmentStatus.COMPLETED),
            "ASN-3004", new DeliveryAssignment("ASN-3004", "ORD-1004", "DRV-2001", AssignmentStatus.ASSIGNED)
        );

        Map<String, List<OrderStatusEvent>> statusEventsByOrderId = Map.of(
            "ORD-1001", new ArrayList<>(List.of(
                new OrderStatusEvent("EVT-4001", "ORD-1001", null, OrderStatus.CREATED, "Created", at("2026-07-02T05:00:00"), ActorType.SYSTEM, "system"),
                new OrderStatusEvent("EVT-4002", "ORD-1001", OrderStatus.CREATED, OrderStatus.CONFIRMED, "Confirmed", at("2026-07-02T06:00:00"), ActorType.SYSTEM, "system"),
                new OrderStatusEvent("EVT-4003", "ORD-1001", OrderStatus.CONFIRMED, OrderStatus.PICKED_UP, "Picked up", at("2026-07-02T07:00:00"), ActorType.DRIVER, "DRV-2001"),
                new OrderStatusEvent("EVT-4004", "ORD-1001", OrderStatus.PICKED_UP, OrderStatus.IN_TRANSIT, "In transit", at("2026-07-02T08:00:00"), ActorType.DRIVER, "DRV-2001"),
                new OrderStatusEvent("EVT-4005", "ORD-1001", OrderStatus.IN_TRANSIT, OrderStatus.OUT_FOR_DELIVERY, "Out for delivery", at("2026-07-02T09:00:00"), ActorType.DRIVER, "DRV-2001")
            )),
            "ORD-1002", new ArrayList<>(List.of(
                new OrderStatusEvent("EVT-4101", "ORD-1002", null, OrderStatus.CREATED, "Created", at("2026-07-02T05:30:00"), ActorType.SYSTEM, "system"),
                new OrderStatusEvent("EVT-4102", "ORD-1002", OrderStatus.CREATED, OrderStatus.CONFIRMED, "Confirmed", at("2026-07-02T06:30:00"), ActorType.SYSTEM, "system"),
                new OrderStatusEvent("EVT-4103", "ORD-1002", OrderStatus.CONFIRMED, OrderStatus.PICKED_UP, "Picked up", at("2026-07-02T07:30:00"), ActorType.DRIVER, "DRV-2001"),
                new OrderStatusEvent("EVT-4104", "ORD-1002", OrderStatus.PICKED_UP, OrderStatus.IN_TRANSIT, "In transit", at("2026-07-02T08:30:00"), ActorType.DRIVER, "DRV-2001")
            )),
            "ORD-1003", new ArrayList<>(List.of(
                new OrderStatusEvent("EVT-4201", "ORD-1003", null, OrderStatus.CREATED, "Created", at("2026-07-01T15:00:00"), ActorType.SYSTEM, "system"),
                new OrderStatusEvent("EVT-4202", "ORD-1003", OrderStatus.CREATED, OrderStatus.OUT_FOR_DELIVERY, "Out for delivery", at("2026-07-01T17:00:00"), ActorType.DRIVER, "DRV-2001"),
                new OrderStatusEvent("EVT-4203", "ORD-1003", OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED, "Delivered", at("2026-07-01T18:00:00"), ActorType.DRIVER, "DRV-2001")
            ))
        );

        return new SeedDataStore(orders, drivers, assignments, statusEventsByOrderId);
    }

    private static OffsetDateTime at(String value) {
        return OffsetDateTime.parse(value + "+08:00");
    }
}
