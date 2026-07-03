package com.waypoint.partnersource.shared.health;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(ReadinessController.class)
class ReadinessControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    ReadinessService readinessService;

    @Test
    void readyReturnsReadyWhenSeedDataExists() throws Exception {
        when(readinessService.check())
                .thenReturn(new ReadinessResponse("READY", "partner-source", new ReadinessChecks("UP", "UP")));

        mockMvc.perform(get("/ready"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("READY"))
                .andExpect(jsonPath("$.service").value("partner-source"))
                .andExpect(jsonPath("$.checks.persistence").value("UP"))
                .andExpect(jsonPath("$.checks.seedData").value("UP"));
    }

    @Test
    void readyReturnsServiceUnavailableWhenSeedDataIsDown() throws Exception {
        when(readinessService.check())
                .thenReturn(new ReadinessResponse("NOT_READY", "partner-source", new ReadinessChecks("UP", "DOWN")));

        mockMvc.perform(get("/ready"))
                .andExpect(status().isServiceUnavailable())
                .andExpect(jsonPath("$.status").value("NOT_READY"))
                .andExpect(jsonPath("$.checks.seedData").value("DOWN"));
    }
}
