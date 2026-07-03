package com.waypoint.partnersource.driver.service;

import com.waypoint.partnersource.assignment.repository.InMemoryAssignmentRepository;
import com.waypoint.partnersource.driver.api.dto.DriverResponse;
import com.waypoint.partnersource.driver.repository.InMemoryDriverRepository;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import org.springframework.stereotype.Service;

@Service
public class DriverService {
    private final InMemoryDriverRepository driverRepository;
    private final InMemoryAssignmentRepository assignmentRepository;
    private final DriverResponseMapper mapper;

    public DriverService(
            InMemoryDriverRepository driverRepository,
            InMemoryAssignmentRepository assignmentRepository,
            DriverResponseMapper mapper
    ) {
        this.driverRepository = driverRepository;
        this.assignmentRepository = assignmentRepository;
        this.mapper = mapper;
    }

    public DriverResponse getDriver(String driverId) {
        var driver = driverRepository.findById(driverId)
                .orElseThrow(() -> PartnerSourceException.driverNotFound(driverId));
        var activeAssignmentCount = assignmentRepository.findActiveByDriverId(driverId).size();
        return mapper.toDriverResponse(driver, activeAssignmentCount);
    }
}
