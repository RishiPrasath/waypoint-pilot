package com.waypoint.partnersource.shared.seed;

import com.waypoint.partnersource.assignment.domain.DeliveryAssignment;
import com.waypoint.partnersource.driver.domain.DeliveryDriver;
import com.waypoint.partnersource.order.domain.DeliveryOrder;
import com.waypoint.partnersource.order.domain.OrderStatusEvent;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public final class SeedDataStore {
    private final Map<String, DeliveryOrder> orders;
    private final Map<String, DeliveryDriver> drivers;
    private final Map<String, DeliveryAssignment> assignments;
    private final Map<String, List<OrderStatusEvent>> statusEventsByOrderId;

    public SeedDataStore(
        Map<String, DeliveryOrder> orders,
        Map<String, DeliveryDriver> drivers,
        Map<String, DeliveryAssignment> assignments,
        Map<String, List<OrderStatusEvent>> statusEventsByOrderId
    ) {
        this.orders = new ConcurrentHashMap<>(orders);
        this.drivers = new ConcurrentHashMap<>(drivers);
        this.assignments = new ConcurrentHashMap<>(assignments);
        this.statusEventsByOrderId = new ConcurrentHashMap<>(statusEventsByOrderId);
    }

    public Map<String, DeliveryOrder> orders() {
        return orders;
    }

    public Map<String, DeliveryDriver> drivers() {
        return drivers;
    }

    public Map<String, DeliveryAssignment> assignments() {
        return assignments;
    }

    public Map<String, List<OrderStatusEvent>> statusEventsByOrderId() {
        return statusEventsByOrderId;
    }
}
