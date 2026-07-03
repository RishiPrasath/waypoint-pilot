package com.waypoint.partnersource.shared.health;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReadinessController {
    private final ReadinessService readinessService;

    public ReadinessController(ReadinessService readinessService) {
        this.readinessService = readinessService;
    }

    @GetMapping("/ready")
    public ResponseEntity<ReadinessResponse> getReadiness() {
        ReadinessResponse response = readinessService.check();
        boolean ready = "UP".equals(response.checks().persistence())
                && "UP".equals(response.checks().seedData());

        if (ready) {
            return ResponseEntity.ok(response);
        }

        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(response);
    }
}
