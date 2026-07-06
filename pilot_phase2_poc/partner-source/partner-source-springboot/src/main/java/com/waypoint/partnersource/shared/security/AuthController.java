package com.waypoint.partnersource.shared.security;

import com.waypoint.partnersource.shared.security.dto.DemoLoginRequest;
import com.waypoint.partnersource.shared.security.dto.DemoLoginResponse;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {
    private final DemoLoginService demoLoginService;

    public AuthController(DemoLoginService demoLoginService) {
        this.demoLoginService = demoLoginService;
    }

    @PostMapping("/demo-login")
    public DemoLoginResponse demoLogin(@Valid @RequestBody DemoLoginRequest request) {
        return demoLoginService.login(request);
    }
}
