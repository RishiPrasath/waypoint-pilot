package com.waypoint.partnersource.driver.service;

import com.waypoint.partnersource.driver.api.dto.DriverAssignmentItemResponse;
import com.waypoint.partnersource.driver.api.dto.DriverResponse;
import com.waypoint.partnersource.driver.domain.DeliveryDriver;
import com.waypoint.partnersource.order.api.dto.DeliveryWindowResponse;
import com.waypoint.partnersource.order.domain.DeliveryOrder;
import com.waypoint.partnersource.assignment.domain.DeliveryAssignment;
import org.springframework.stereotype.Component;

@Component
public class DriverResponseMapper {
    public DriverResponse toDriverResponse(DeliveryDriver driver, int activeAssignmentCount) {
        return new DriverResponse(
                driver.driverId(),
                driver.displayName(),
                driver.availabilityStatus(),
                activeAssignmentCount
        );
    }

    public DriverAssignmentItemResponse toAssignmentItem(DeliveryAssignment assignment, DeliveryOrder order) {
        return new DriverAssignmentItemResponse(
                assignment.assignmentId(),
                assignment.orderId(),
                assignment.status(),
                order.currentStatus(),
                order.recipientName(),
                order.deliveryAddressSummary(),
                new DeliveryWindowResponse(order.deliveryWindowStart(), order.deliveryWindowEnd()),
                order.lastUpdatedAt()
        );
    }
}
