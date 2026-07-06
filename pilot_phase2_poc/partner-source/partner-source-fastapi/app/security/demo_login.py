from app.errors.exceptions import DriverNotFoundError, InvalidRequestError
from app.repositories.drivers import InMemoryDriverRepository
from app.schemas.auth import DemoLoginRequest, DemoLoginResponse
from app.security.demo_tokens import token_for
from app.security.principal import PrincipalActorType


class DemoLoginService:
    def __init__(self, driver_repository: InMemoryDriverRepository) -> None:
        self._driver_repository = driver_repository

    def login(self, request: DemoLoginRequest) -> DemoLoginResponse:
        try:
            actor_type = PrincipalActorType(request.actorType)
        except ValueError as exc:
            raise InvalidRequestError("Unsupported actorType.") from exc

        if actor_type == PrincipalActorType.DRIVER and self._driver_repository.find_by_id(request.actorId) is None:
            raise DriverNotFoundError(request.actorId)

        token = token_for(actor_type, request.actorId)
        if token is None:
            raise InvalidRequestError("Unsupported demo login identity.")

        return DemoLoginResponse(
            accessToken=token.accessToken,
            tokenType="Bearer",
            expiresIn=3600,
            principal=token.principal,
        )
