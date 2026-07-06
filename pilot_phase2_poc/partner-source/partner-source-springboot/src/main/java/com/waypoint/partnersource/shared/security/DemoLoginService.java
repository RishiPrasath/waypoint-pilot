package com.waypoint.partnersource.shared.security;

import com.waypoint.partnersource.driver.repository.InMemoryDriverRepository;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import com.waypoint.partnersource.shared.security.dto.DemoLoginRequest;
import com.waypoint.partnersource.shared.security.dto.DemoLoginResponse;
import com.waypoint.partnersource.shared.security.dto.PrincipalResponse;
import org.springframework.stereotype.Service;

@Service
public class DemoLoginService {
    private static final int EXPIRES_IN_SECONDS = 3600;

    private final DemoTokenAuthenticator authenticator;
    private final InMemoryDriverRepository driverRepository;

    public DemoLoginService(DemoTokenAuthenticator authenticator, InMemoryDriverRepository driverRepository) {
        this.authenticator = authenticator;
        this.driverRepository = driverRepository;
    }

    public DemoLoginResponse login(DemoLoginRequest request) {
        var actorType = parseActorType(request.actorType());

        if (actorType == PrincipalActorType.DRIVER) {
            driverRepository.findById(request.actorId())
                    .orElseThrow(() -> PartnerSourceException.driverNotFound(request.actorId()));
        }

        var token = authenticator.tokenFor(actorType, request.actorId())
                .orElseThrow(() -> PartnerSourceException.invalidRequest("Unsupported demo login identity."));
        var principal = token.principal();

        return new DemoLoginResponse(
                token.accessToken(),
                "Bearer",
                EXPIRES_IN_SECONDS,
                new PrincipalResponse(
                        principal.subject(),
                        principal.role(),
                        principal.actorType(),
                        principal.actorId(),
                        principal.scopes(),
                        principal.demoOrgId(),
                        principal.channel()
                )
        );
    }

    private PrincipalActorType parseActorType(String actorType) {
        try {
            return PrincipalActorType.valueOf(actorType);
        } catch (IllegalArgumentException exception) {
            throw PartnerSourceException.invalidRequest("Unsupported actorType.");
        }
    }
}
