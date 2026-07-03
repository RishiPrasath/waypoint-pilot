package com.waypoint.partnersource.driver.api;

import com.waypoint.partnersource.driver.api.dto.DriverAssignmentsResponse;
import com.waypoint.partnersource.driver.service.DriverAssignmentService;
import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import java.util.regex.Pattern;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/drivers")
public class DriverAssignmentController {
    private static final Pattern DRIVER_ID_PATTERN = Pattern.compile("^DRV-[0-9]{4}$");

    private final DriverAssignmentService driverAssignmentService;

    public DriverAssignmentController(DriverAssignmentService driverAssignmentService) {
        this.driverAssignmentService = driverAssignmentService;
    }

    @GetMapping("/{driverId}/assignments")
    public DriverAssignmentsResponse listAssignments(
            @PathVariable String driverId,
            @RequestParam(required = false) OrderStatus status,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int pageSize
    ) {
        if (!DRIVER_ID_PATTERN.matcher(driverId).matches() || page < 1 || pageSize < 1 || pageSize > 100) {
            throw PartnerSourceException.invalidRequest("Invalid driver assignment request.");
        }

        return driverAssignmentService.listAssignments(driverId, status, page, pageSize);
    }
}
