from enum import Enum
from pydantic import BaseModel


class ActorRole(str, Enum):
    DELIVERY_DRIVER = "DELIVERY_DRIVER"
    CUSTOMER_SERVICE_AGENT = "CUSTOMER_SERVICE_AGENT"


class PrincipalActorType(str, Enum):
    DRIVER = "DRIVER"
    USER = "USER"


class AuthenticatedPrincipal(BaseModel):
    subject: str
    role: ActorRole
    actorType: PrincipalActorType
    actorId: str
    scopes: list[str]
    demoOrgId: str
    channel: str


class DemoToken(BaseModel):
    accessToken: str
    principal: AuthenticatedPrincipal
