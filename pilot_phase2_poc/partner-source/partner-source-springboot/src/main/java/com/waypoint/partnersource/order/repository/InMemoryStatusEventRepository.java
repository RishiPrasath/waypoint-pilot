package com.waypoint.partnersource.order.repository;

import com.waypoint.partnersource.order.domain.OrderStatusEvent;
import com.waypoint.partnersource.shared.seed.SeedDataStore;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import org.springframework.stereotype.Repository;

@Repository
public class InMemoryStatusEventRepository {
    private final SeedDataStore store;

    public InMemoryStatusEventRepository(SeedDataStore store) {
        this.store = store;
    }

    public List<OrderStatusEvent> findByOrderId(String orderId) {
        return store.statusEventsByOrderId().getOrDefault(orderId, List.of()).stream()
            .sorted(Comparator.comparing((OrderStatusEvent event) -> event.occurredAt()))
            .toList();
    }

    public void append(OrderStatusEvent event) {
        store.statusEventsByOrderId()
            .computeIfAbsent(event.orderId(), ignored -> new ArrayList<>())
            .add(event);
    }
}
