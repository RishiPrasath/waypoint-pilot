package com.waypoint.partnersource.shared.security;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.springframework.stereotype.Component;

@Component
public class DemoTokenAuthenticator {
    private final Map<String, AuthenticatedPrincipal> principalsByToken = Map.of(
            "demo-driver-2001-token", driver("DRV-2001"),
            "demo-driver-2002-token", driver("DRV-2002"),
            "demo-driver-2003-token", driver("DRV-2003"),
            "demo-csa-5001-token", csa()
    );

    public Optional<AuthenticatedPrincipal> authenticate(String token) {
        return Optional.ofNullable(principalsByToken.get(token));
    }

    public Optional<DemoToken> tokenFor(PrincipalActorType actorType, String actorId) {
        return principalsByToken.entrySet().stream()
                .filter(entry -> entry.getValue().actorType() == actorType)
                .filter(entry -> entry.getValue().actorId().equals(actorId))
                .findFirst()
                .map(entry -> new DemoToken(entry.getKey(), entry.getValue()));
    }

    private static AuthenticatedPrincipal driver(String driverId) {
        return new AuthenticatedPrincipal(
                "driver:" + driverId,
                ActorRole.DELIVERY_DRIVER,
                PrincipalActorType.DRIVER,
                driverId,
                List.of(
                        "driver:read:self",
                        "assignment:read:self",
                        "order:read:assigned",
                        "status-event:create:assigned"
                ),
                "ORG-DEMO-1",
                "DRIVER_APP"
        );
    }

    private static AuthenticatedPrincipal csa() {
        return new AuthenticatedPrincipal(
                "user:CSA-5001",
                ActorRole.CUSTOMER_SERVICE_AGENT,
                PrincipalActorType.USER,
                "CSA-5001",
                List.of("order:read:demo-org"),
                "ORG-DEMO-1",
                "SUPPORT_CONSOLE"
        );
    }
}
