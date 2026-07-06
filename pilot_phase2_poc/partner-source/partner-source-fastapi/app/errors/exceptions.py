class PartnerSourceError(Exception):
    def __init__(self, status_code: int, error_code: str, title: str, detail: str) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.title = title
        self.detail = detail


class InvalidRequestError(PartnerSourceError):
    def __init__(self, detail: str = "Invalid request.") -> None:
        super().__init__(400, "INVALID_REQUEST", "Invalid request", detail)


class UnauthenticatedError(PartnerSourceError):
    def __init__(self, detail: str = "Authentication is required for this route.") -> None:
        super().__init__(401, "UNAUTHENTICATED", "Unauthenticated", detail)


class AccessDeniedError(PartnerSourceError):
    def __init__(self, detail: str = "Caller is not allowed to access this resource.") -> None:
        super().__init__(403, "ACCESS_DENIED", "Access denied", detail)


class OrderNotFoundError(PartnerSourceError):
    def __init__(self, order_id: str) -> None:
        super().__init__(404, "ORDER_NOT_FOUND", "Order not found", f"No order exists for orderId {order_id}.")


class DriverNotFoundError(PartnerSourceError):
    def __init__(self, driver_id: str) -> None:
        super().__init__(404, "DRIVER_NOT_FOUND", "Driver not found", f"No driver exists for driverId {driver_id}.")


class OrderNotAssignedToDriverError(PartnerSourceError):
    def __init__(self, order_id: str, driver_id: str) -> None:
        super().__init__(
            403,
            "ORDER_NOT_ASSIGNED_TO_DRIVER",
            "Order not assigned to driver",
            f"Driver {driver_id} is not assigned to order {order_id}.",
        )


class InvalidStatusTransitionError(PartnerSourceError):
    def __init__(self, detail: str = "Invalid status transition.") -> None:
        super().__init__(409, "INVALID_STATUS_TRANSITION", "Invalid status transition", detail)


class InvalidStatusEventError(PartnerSourceError):
    def __init__(self, detail: str = "Invalid status event.") -> None:
        super().__init__(422, "INVALID_STATUS_EVENT", "Invalid status event", detail)
