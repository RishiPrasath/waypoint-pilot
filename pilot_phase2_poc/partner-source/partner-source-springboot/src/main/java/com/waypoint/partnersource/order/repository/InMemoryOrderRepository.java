package com.waypoint.partnersource.order.repository;

import com.waypoint.partnersource.order.domain.DeliveryOrder;
import com.waypoint.partnersource.shared.seed.SeedDataStore;
import java.util.Optional;
import org.springframework.stereotype.Repository;

@Repository
public class InMemoryOrderRepository {
    private final SeedDataStore store;

    public InMemoryOrderRepository(SeedDataStore store) {
        this.store = store;
    }

    public Optional<DeliveryOrder> findById(String orderId) {
        return Optional.ofNullable(store.orders().get(orderId));
    }

    public void save(DeliveryOrder order) {
        store.orders().put(order.orderId(), order);
    }
}
