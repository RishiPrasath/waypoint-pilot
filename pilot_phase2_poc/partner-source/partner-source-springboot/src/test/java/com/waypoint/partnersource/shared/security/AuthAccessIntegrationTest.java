package com.waypoint.partnersource.shared.security;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class AuthAccessIntegrationTest {
    private static final String DRIVER_2001 = "Bearer demo-driver-2001-token";
    private static final String DRIVER_2002 = "Bearer demo-driver-2002-token";
    private static final String CSA = "Bearer demo-csa-5001-token";

    @Autowired
    MockMvc mockMvc;

    @Test
    void demoDriverLoginReturnsTokenAndPrincipal() throws Exception {
        mockMvc.perform(post("/api/v1/auth/demo-login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "actorType": "DRIVER",
                                  "actorId": "DRV-2001"
                                }
                                """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.accessToken").value("demo-driver-2001-token"))
                .andExpect(jsonPath("$.tokenType").value("Bearer"))
                .andExpect(jsonPath("$.principal.role").value("DELIVERY_DRIVER"))
                .andExpect(jsonPath("$.principal.actorId").value("DRV-2001"));
    }

    @Test
    void protectedRouteWithoutTokenReturnsUnauthenticated() throws Exception {
        mockMvc.perform(get("/api/v1/orders/ORD-1001/status"))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.errorCode").value("UNAUTHENTICATED"));
    }

    @Test
    void invalidTokenReturnsUnauthenticated() throws Exception {
        mockMvc.perform(get("/api/v1/orders/ORD-1001/status")
                        .header(HttpHeaders.AUTHORIZATION, "Bearer invalid-token"))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.errorCode").value("UNAUTHENTICATED"));
    }

    @Test
    void driverCannotReadAnotherDriverResource() throws Exception {
        mockMvc.perform(get("/api/v1/drivers/DRV-2002/assignments")
                        .header(HttpHeaders.AUTHORIZATION, DRIVER_2001))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.errorCode").value("ACCESS_DENIED"));
    }

    @Test
    void driverCannotReadUnassignedOrder() throws Exception {
        mockMvc.perform(get("/api/v1/orders/ORD-1001/status")
                        .header(HttpHeaders.AUTHORIZATION, DRIVER_2002))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.errorCode").value("ACCESS_DENIED"));
    }

    @Test
    void csaCanReadOrderButCannotCreateStatusEvent() throws Exception {
        mockMvc.perform(get("/api/v1/orders/ORD-1001/status")
                        .header(HttpHeaders.AUTHORIZATION, CSA))
                .andExpect(status().isOk());

        mockMvc.perform(post("/api/v1/orders/ORD-1001/status-events")
                        .header(HttpHeaders.AUTHORIZATION, CSA)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "driverId": "DRV-2001",
                                  "status": "DELIVERED"
                                }
                                """))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.errorCode").value("ACCESS_DENIED"));
    }

    @Test
    void spoofedDriverIdReturnsAccessDeniedBeforeDomainMutation() throws Exception {
        mockMvc.perform(post("/api/v1/orders/ORD-1001/status-events")
                        .header(HttpHeaders.AUTHORIZATION, DRIVER_2001)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "driverId": "DRV-2002",
                                  "status": "DELIVERED"
                                }
                                """))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.errorCode").value("ACCESS_DENIED"));
    }

    @Test
    void matchingUnassignedDriverStillReturnsDomainDenial() throws Exception {
        mockMvc.perform(post("/api/v1/orders/ORD-1001/status-events")
                        .header(HttpHeaders.AUTHORIZATION, DRIVER_2002)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "driverId": "DRV-2002",
                                  "status": "DELIVERED"
                                }
                                """))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.errorCode").value("ORDER_NOT_ASSIGNED_TO_DRIVER"));
    }
}
