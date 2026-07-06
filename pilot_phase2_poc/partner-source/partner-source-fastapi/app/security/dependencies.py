from fastapi import Header

from app.errors.exceptions import UnauthenticatedError
from app.security.authenticator import DemoTokenAuthenticator
from app.security.principal import AuthenticatedPrincipal


def require_principal(authorization: str | None = Header(default=None, alias="Authorization")) -> AuthenticatedPrincipal:
    if authorization is None or not authorization.startswith("Bearer "):
        raise UnauthenticatedError("Missing or invalid bearer token.")

    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise UnauthenticatedError("Missing or invalid bearer token.")

    principal = DemoTokenAuthenticator().authenticate(token)
    if principal is None:
        raise UnauthenticatedError("Missing or invalid bearer token.")
    return principal
