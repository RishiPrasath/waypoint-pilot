from app.security.principal import ActorRole, AuthenticatedPrincipal, DemoToken, PrincipalActorType


def _driver(driver_id: str) -> AuthenticatedPrincipal:
    return AuthenticatedPrincipal(
        subject=f"driver:{driver_id}",
        role=ActorRole.DELIVERY_DRIVER,
        actorType=PrincipalActorType.DRIVER,
        actorId=driver_id,
        scopes=[
            "driver:read:self",
            "assignment:read:self",
            "order:read:assigned",
            "status-event:create:assigned",
        ],
        demoOrgId="ORG-DEMO-1",
        channel="DRIVER_APP",
    )


def _csa() -> AuthenticatedPrincipal:
    return AuthenticatedPrincipal(
        subject="user:CSA-5001",
        role=ActorRole.CUSTOMER_SERVICE_AGENT,
        actorType=PrincipalActorType.USER,
        actorId="CSA-5001",
        scopes=["order:read:demo-org"],
        demoOrgId="ORG-DEMO-1",
        channel="SUPPORT_CONSOLE",
    )


DEMO_TOKENS: dict[str, AuthenticatedPrincipal] = {
    "demo-driver-2001-token": _driver("DRV-2001"),
    "demo-driver-2002-token": _driver("DRV-2002"),
    "demo-driver-2003-token": _driver("DRV-2003"),
    "demo-csa-5001-token": _csa(),
}


def token_for(actor_type: PrincipalActorType, actor_id: str) -> DemoToken | None:
    for token, principal in DEMO_TOKENS.items():
        if principal.actorType == actor_type and principal.actorId == actor_id:
            return DemoToken(accessToken=token, principal=principal)
    return None
