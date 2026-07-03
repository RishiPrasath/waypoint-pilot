package com.waypoint.partnersource.driver.api;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.waypoint.partnersource.driver.api.dto.DriverResponse;
import com.waypoint.partnersource.driver.domain.DriverAvailabilityStatus;
import com.waypoint.partnersource.driver.service.DriverService;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(DriverController.class)
class DriverControllerTest {
    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    DriverService driverService;

    @Test
    void getDriverReturnsContractShape() throws Exception {
        when(driverService.getDriver("DRV-2001"))
                .thenReturn(new DriverResponse("DRV-2001", "A. Kumar", DriverAvailabilityStatus.AVAILABLE, 2));

        mockMvc.perform(get("/api/v1/drivers/DRV-2001"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.driverId").value("DRV-2001"))
                .andExpect(jsonPath("$.displayName").value("A. Kumar"))
                .andExpect(jsonPath("$.availabilityStatus").value("AVAILABLE"))
                .andExpect(jsonPath("$.activeAssignmentCount").value(2));
    }

    @Test
    void missingDriverReturnsProblemDetail() throws Exception {
        when(driverService.getDriver("DRV-9999"))
                .thenThrow(PartnerSourceException.driverNotFound("DRV-9999"));

        mockMvc.perform(get("/api/v1/drivers/DRV-9999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.errorCode").value("DRIVER_NOT_FOUND"));
    }

    @Test
    void invalidDriverIdReturnsProblemDetail() throws Exception {
        mockMvc.perform(get("/api/v1/drivers/INVALID"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.errorCode").value("INVALID_REQUEST"));
    }
}
