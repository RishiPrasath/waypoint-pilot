package com.waypoint.partnersource.order.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.order.repository.InMemoryOrderRepository;
import com.waypoint.partnersource.shared.error.ErrorCode;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class OrderStatusServiceTest {

    @Test
    void returnsSeededOrderStatus() {
        var service = new OrderStatusService(
                new InMemoryOrderRepository(SeedDataLoader.load()),
                new OrderResponseMapper()
        );

        var response = service.getStatus("ORD-1001");

        assertEquals("ORD-1001", response.orderId());
        assertEquals(OrderStatus.OUT_FOR_DELIVERY, response.currentStatus());
        assertEquals("DRV-2001", response.assignedDriver().driverId());
        assertNotNull(response.deliveryWindow());
    }

    @Test
    void missingOrderThrowsDomainException() {
        var service = new OrderStatusService(
                new InMemoryOrderRepository(SeedDataLoader.load()),
                new OrderResponseMapper()
        );

        var exception = assertThrows(PartnerSourceException.class, () -> service.getStatus("ORD-9999"));

        assertEquals(404, exception.status().value());
        assertEquals(ErrorCode.ORDER_NOT_FOUND, exception.errorCode());
    }
}
