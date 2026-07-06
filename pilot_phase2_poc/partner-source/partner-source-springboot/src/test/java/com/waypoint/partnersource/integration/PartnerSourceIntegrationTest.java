package com.waypoint.partnersource.integration;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.http.HttpHeaders;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class PartnerSourceIntegrationTest {
    private static final String DRIVER_2001 = "Bearer demo-driver-2001-token";
    private static final String CSA = "Bearer demo-csa-5001-token";

    @Autowired
    MockMvc mockMvc;

    @Test
    void slice1HappyPathWorksThroughHttp() throws Exception {
        mockMvc.perform(get("/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));

        mockMvc.perform(get("/ready"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("READY"));

        mockMvc.perform(post("/api/v1/auth/demo-login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "actorType": "DRIVER",
                                  "actorId": "DRV-2001"
                                }
                                """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.accessToken").value("demo-driver-2001-token"));

        mockMvc.perform(get("/api/v1/orders/ORD-1001/status")
                        .header(HttpHeaders.AUTHORIZATION, DRIVER_2001))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.currentStatus").value("OUT_FOR_DELIVERY"));

        mockMvc.perform(get("/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20")
                        .header(HttpHeaders.AUTHORIZATION, DRIVER_2001))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalItems").value(5));

        mockMvc.perform(get("/api/v1/drivers/DRV-2001")
                        .header(HttpHeaders.AUTHORIZATION, DRIVER_2001))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.activeAssignmentCount").value(2));

        mockMvc.perform(get("/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20")
                        .header(HttpHeaders.AUTHORIZATION, DRIVER_2001))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalItems").value(2));

        mockMvc.perform(post("/api/v1/orders/ORD-1001/status-events")
                        .header(HttpHeaders.AUTHORIZATION, DRIVER_2001)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "driverId": "DRV-2001",
                                  "status": "DELIVERED",
                                  "occurredAt": "2026-07-02T10:30:00+08:00"
                                }
                                """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.orderCurrentStatus").value("DELIVERED"));

        mockMvc.perform(get("/api/v1/orders/ORD-1001/status")
                        .header(HttpHeaders.AUTHORIZATION, DRIVER_2001))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.currentStatus").value("DELIVERED"));

        mockMvc.perform(get("/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20")
                        .header(HttpHeaders.AUTHORIZATION, DRIVER_2001))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalItems").value(6))
                .andExpect(jsonPath("$.items[5].status").value("DELIVERED"));
    }

    @Test
    void representativeErrorPathReturnsProblemDetail() throws Exception {
        mockMvc.perform(get("/api/v1/orders/ORD-9999/status")
                        .header(HttpHeaders.AUTHORIZATION, CSA))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.errorCode").value("ORDER_NOT_FOUND"))
                .andExpect(jsonPath("$.correlationId").exists());
    }
}
