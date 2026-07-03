package com.waypoint.partnersource.driver.service;

import com.waypoint.partnersource.assignment.repository.InMemoryAssignmentRepository;
import com.waypoint.partnersource.driver.api.dto.DriverAssignmentItemResponse;
import com.waypoint.partnersource.driver.api.dto.DriverAssignmentsResponse;
import com.waypoint.partnersource.driver.repository.InMemoryDriverRepository;
import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.order.repository.InMemoryOrderRepository;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class DriverAssignmentService {
    private final InMemoryDriverRepository driverRepository;
    private final InMemoryAssignmentRepository assignmentRepository;
    private final InMemoryOrderRepository orderRepository;
    private final DriverResponseMapper mapper;

    public DriverAssignmentService(
            InMemoryDriverRepository driverRepository,
            InMemoryAssignmentRepository assignmentRepository,
            InMemoryOrderRepository orderRepository,
            DriverResponseMapper mapper
    ) {
        this.driverRepository = driverRepository;
        this.assignmentRepository = assignmentRepository;
        this.orderRepository = orderRepository;
        this.mapper = mapper;
    }

    public DriverAssignmentsResponse listAssignments(String driverId, OrderStatus status, int page, int pageSize) {
        driverRepository.findById(driverId)
                .orElseThrow(() -> PartnerSourceException.driverNotFound(driverId));

        var items = assignmentRepository.findActiveByDriverId(driverId).stream()
                .map(assignment -> orderRepository.findById(assignment.orderId())
                        .map(order -> mapper.toAssignmentItem(assignment, order))
                        .orElseThrow(() -> PartnerSourceException.orderNotFound(assignment.orderId())))
                .filter(item -> status == null || item.currentStatus() == status)
                .toList();

        return new DriverAssignmentsResponse(driverId, page(items, page, pageSize), page, pageSize, items.size());
    }

    private static List<DriverAssignmentItemResponse> page(List<DriverAssignmentItemResponse> items, int page, int pageSize) {
        var fromIndex = Math.min((page - 1) * pageSize, items.size());
        var toIndex = Math.min(fromIndex + pageSize, items.size());
        return items.subList(fromIndex, toIndex);
    }
}
