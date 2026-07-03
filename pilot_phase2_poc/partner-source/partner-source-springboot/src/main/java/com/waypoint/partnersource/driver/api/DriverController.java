package com.waypoint.partnersource.driver.api;

import com.waypoint.partnersource.driver.api.dto.DriverResponse;
import com.waypoint.partnersource.driver.service.DriverService;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import java.util.regex.Pattern;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/drivers")
public class DriverController {
    private static final Pattern DRIVER_ID_PATTERN = Pattern.compile("^DRV-[0-9]{4}$");

    private final DriverService driverService;

    public DriverController(DriverService driverService) {
        this.driverService = driverService;
    }

    @GetMapping("/{driverId}")
    public DriverResponse getDriver(@PathVariable String driverId) {
        if (!DRIVER_ID_PATTERN.matcher(driverId).matches()) {
            throw PartnerSourceException.invalidRequest("Invalid driverId.");
        }

        return driverService.getDriver(driverId);
    }
}
