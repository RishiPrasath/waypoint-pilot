package com.waypoint.partnersource.order.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;

class InMemoryOrderRepositoryTest {

    @Test
    void findsSeededOrder() {
        var repository = new InMemoryOrderRepository(SeedDataLoader.load());

        var order = repository.findById("ORD-1001");

        assertTrue(order.isPresent());
        assertEquals(OrderStatus.OUT_FOR_DELIVERY, order.get().currentStatus());
    }

    @Test
    void missingOrderReturnsEmpty() {
        var repository = new InMemoryOrderRepository(SeedDataLoader.load());

        assertTrue(repository.findById("ORD-9999").isEmpty());
    }
}