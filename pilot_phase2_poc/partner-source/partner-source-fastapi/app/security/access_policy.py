from app.domain.policies import AssignmentAuthorizationPolicy
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.orders import InMemoryOrderRepository
from app.security.principal import ActorRole, AuthenticatedPrincipal, PrincipalActorType


class AccessPolicy:
    def __init__(
        self,
        order_repository: InMemoryOrderRepository,
        assignment_repository: InMemoryAssignmentRepository,
    ) -> None:
        self._order_repository = order_repository
        self._assignment_repository = assignment_repository
        self._assignment_policy = AssignmentAuthorizationPolicy()

    def can_read_driver_resource(self, principal: AuthenticatedPrincipal, driver_id: str) -> bool:
        return (
            principal.role == ActorRole.DELIVERY_DRIVER
            and principal.actorType == PrincipalActorType.DRIVER
            and principal.actorId == driver_id
        )

    def can_read_order(self, principal: AuthenticatedPrincipal, order_id: str) -> bool:
        if principal.role == ActorRole.CUSTOMER_SERVICE_AGENT:
            return True
        if principal.role != ActorRole.DELIVERY_DRIVER:
            return False
        if self._order_repository.find_by_id(order_id) is None:
            return True
        return self._assignment_policy.can_driver_update_order(
            principal.actorId,
            order_id,
            self._assignment_repository.find_by_order_id(order_id),
        )

    def can_create_status_event(self, principal: AuthenticatedPrincipal) -> bool:
        return principal.role == ActorRole.DELIVERY_DRIVER and principal.actorType == PrincipalActorType.DRIVER

    def can_submit_driver_id(self, principal: AuthenticatedPrincipal, driver_id: str) -> bool:
        return (
            principal.role == ActorRole.DELIVERY_DRIVER
            and principal.actorType == PrincipalActorType.DRIVER
            and principal.actorId == driver_id
        )
