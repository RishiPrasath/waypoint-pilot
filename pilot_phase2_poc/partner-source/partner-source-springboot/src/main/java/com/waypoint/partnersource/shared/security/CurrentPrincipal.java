package com.waypoint.partnersource.shared.security;

import com.waypoint.partnersource.shared.error.PartnerSourceException;
import jakarta.servlet.http.HttpServletRequest;

public final class CurrentPrincipal {
    public static final String ATTRIBUTE = "authenticatedPrincipal";

    private CurrentPrincipal() {
    }

    public static AuthenticatedPrincipal from(HttpServletRequest request) {
        var principal = request.getAttribute(ATTRIBUTE);
        if (principal instanceof AuthenticatedPrincipal authenticatedPrincipal) {
            return authenticatedPrincipal;
        }
        throw PartnerSourceException.unauthenticated("Authentication is required for this route.");
    }
}
