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
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class PartnerSourceIntegrationTest {

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

        mockMvc.perform(get("/api/v1/orders/ORD-1001/status"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.currentStatus").value("OUT_FOR_DELIVERY"));

        mockMvc.perform(get("/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalItems").value(5));

        mockMvc.perform(get("/api/v1/drivers/DRV-2001"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.activeAssignmentCount").value(2));

        mockMvc.perform(get("/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalItems").value(2));

        mockMvc.perform(post("/api/v1/orders/ORD-1001/status-events")
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

        mockMvc.perform(get("/api/v1/orders/ORD-1001/status"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.currentStatus").value("DELIVERED"));

        mockMvc.perform(get("/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalItems").value(6))
                .andExpect(jsonPath("$.items[5].status").value("DELIVERED"));
    }

    @Test
    void representativeErrorPathReturnsProblemDetail() throws Exception {
        mockMvc.perform(get("/api/v1/orders/ORD-9999/status"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.errorCode").value("ORDER_NOT_FOUND"))
                .andExpect(jsonPath("$.correlationId").exists());
    }
}
