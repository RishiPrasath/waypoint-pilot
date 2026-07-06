from pydantic import BaseModel, Field

from app.security.principal import AuthenticatedPrincipal


class DemoLoginRequest(BaseModel):
    actorType: str = Field(min_length=1)
    actorId: str = Field(min_length=1)


class DemoLoginResponse(BaseModel):
    accessToken: str
    tokenType: str
    expiresIn: int
    principal: AuthenticatedPrincipal
