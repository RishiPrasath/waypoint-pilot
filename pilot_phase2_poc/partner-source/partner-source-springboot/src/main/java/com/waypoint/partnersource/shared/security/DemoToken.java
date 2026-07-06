package com.waypoint.partnersource.shared.security;

public record DemoToken(
        String accessToken,
        AuthenticatedPrincipal principal
) {
}
