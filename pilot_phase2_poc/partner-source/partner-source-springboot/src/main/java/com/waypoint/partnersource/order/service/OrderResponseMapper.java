package com.waypoint.partnersource.order.service;

import com.waypoint.partnersource.order.api.dto.AssignedDriverSummaryResponse;
import com.waypoint.partnersource.order.api.dto.DeliveryWindowResponse;
import com.waypoint.partnersource.order.api.dto.LocationSnapshotResponse;
import com.waypoint.partnersource.order.api.dto.OrderStatusResponse;
import com.waypoint.partnersource.order.domain.DeliveryOrder;
import org.springframework.stereotype.Component;

@Component
public class OrderResponseMapper {

    public OrderStatusResponse toStatusResponse(DeliveryOrder order) {
        AssignedDriverSummaryResponse assignedDriver = null;
        if (order.assignedDriverId() != null && order.assignedDriverName() != null) {
            assignedDriver = new AssignedDriverSummaryResponse(
                    order.assignedDriverId(),
                    order.assignedDriverName()
            );
        }

        DeliveryWindowResponse deliveryWindow = new DeliveryWindowResponse(
                order.deliveryWindowStart(),
                order.deliveryWindowEnd()
        );

        LocationSnapshotResponse currentLocation = null;
        if (order.currentLocation() != null) {
            currentLocation = new LocationSnapshotResponse(order.currentLocation(), null, null, null);
        }

        return new OrderStatusResponse(
                order.orderId(),
                order.currentStatus(),
                order.statusLabel(),
                currentLocation,
                order.estimatedDeliveryAt(),
                deliveryWindow,
                assignedDriver,
                order.lastUpdatedAt()
        );
    }
}
