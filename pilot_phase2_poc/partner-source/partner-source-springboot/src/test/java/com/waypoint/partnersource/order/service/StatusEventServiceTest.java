package com.waypoint.partnersource.order.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.waypoint.partnersource.assignment.domain.AssignmentAuthorizationPolicy;
import com.waypoint.partnersource.assignment.repository.InMemoryAssignmentRepository;
import com.waypoint.partnersource.driver.repository.InMemoryDriverRepository;
import com.waypoint.partnersource.order.api.dto.CreateStatusEventRequest;
import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.order.domain.StatusTransitionPolicy;
import com.waypoint.partnersource.order.repository.InMemoryOrderRepository;
import com.waypoint.partnersource.order.repository.InMemoryStatusEventRepository;
import com.waypoint.partnersource.shared.error.ErrorCode;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import java.time.OffsetDateTime;
import org.junit.jupiter.api.Test;

class StatusEventServiceTest {
    @Test
    void assignedDriverCanCreateDeliveredStatusEvent() {
        var store = SeedDataLoader.load();
        var statusEventRepository = new InMemoryStatusEventRepository(store);
        var orderRepository = new InMemoryOrderRepository(store);
        var service = service(orderRepository, statusEventRepository, store);

        var response = service.createStatusEvent(
                "ORD-1001",
                request("DRV-2001", OrderStatus.DELIVERED, OffsetDateTime.now().minusMinutes(1))
        );

        assertEquals(OrderStatus.OUT_FOR_DELIVERY, response.previousStatus());
        assertEquals(OrderStatus.DELIVERED, response.newStatus());
        assertEquals(OrderStatus.DELIVERED, response.orderCurrentStatus());
        assertEquals(OrderStatus.DELIVERED, orderRepository.findById("ORD-1001").orElseThrow().currentStatus());
        assertEquals(6, statusEventRepository.findByOrderId("ORD-1001").size());
    }

    @Test
    void unassignedDriverReturnsOrderNotAssigned() {
        var exception = assertThrows(PartnerSourceException.class,
                () -> service().createStatusEvent("ORD-1001",
                        request("DRV-2002", OrderStatus.DELIVERED, OffsetDateTime.now().minusMinutes(1))));

        assertEquals(ErrorCode.ORDER_NOT_ASSIGNED_TO_DRIVER, exception.errorCode());
    }

    @Test
    void missingDriverReturnsDriverNotFound() {
        var exception = assertThrows(PartnerSourceException.class,
                () -> service().createStatusEvent("ORD-1001",
                        request("DRV-9999", OrderStatus.DELIVERED, OffsetDateTime.now().minusMinutes(1))));

        assertEquals(ErrorCode.DRIVER_NOT_FOUND, exception.errorCode());
    }

    @Test
    void missingOrderReturnsOrderNotFound() {
        var exception = assertThrows(PartnerSourceException.class,
                () -> service().createStatusEvent("ORD-9999",
                        request("DRV-2001", OrderStatus.DELIVERED, OffsetDateTime.now().minusMinutes(1))));

        assertEquals(ErrorCode.ORDER_NOT_FOUND, exception.errorCode());
    }

    @Test
    void deliveredOrderCannotMoveBackward() {
        var exception = assertThrows(PartnerSourceException.class,
                () -> service().createStatusEvent("ORD-1003",
                        request("DRV-2001", OrderStatus.OUT_FOR_DELIVERY, OffsetDateTime.now().minusMinutes(1))));

        assertEquals(ErrorCode.INVALID_STATUS_TRANSITION, exception.errorCode());
    }

    @Test
    void farFutureOccurredAtReturnsInvalidStatusEvent() {
        var exception = assertThrows(PartnerSourceException.class,
                () -> service().createStatusEvent("ORD-1001",
                        request("DRV-2001", OrderStatus.DELIVERED, OffsetDateTime.now().plusDays(2))));

        assertEquals(ErrorCode.INVALID_STATUS_EVENT, exception.errorCode());
    }

    private CreateStatusEventRequest request(String driverId, OrderStatus status, OffsetDateTime occurredAt) {
        return new CreateStatusEventRequest(driverId, status, occurredAt, null, null, null);
    }

    private StatusEventService service() {
        var store = SeedDataLoader.load();
        return service(new InMemoryOrderRepository(store), new InMemoryStatusEventRepository(store), store);
    }

    private StatusEventService service(
            InMemoryOrderRepository orderRepository,
            InMemoryStatusEventRepository statusEventRepository,
            com.waypoint.partnersource.shared.seed.SeedDataStore store
    ) {
        return new StatusEventService(
                orderRepository,
                new InMemoryDriverRepository(store),
                new InMemoryAssignmentRepository(store),
                statusEventRepository,
                new AssignmentAuthorizationPolicy(),
                new StatusTransitionPolicy()
        );
    }
}
