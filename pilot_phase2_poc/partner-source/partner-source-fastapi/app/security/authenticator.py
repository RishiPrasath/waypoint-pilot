from app.security.demo_tokens import DEMO_TOKENS
from app.security.principal import AuthenticatedPrincipal


class DemoTokenAuthenticator:
    def authenticate(self, token: str) -> AuthenticatedPrincipal | None:
        return DEMO_TOKENS.get(token)
