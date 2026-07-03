from datetime import datetime

from pydantic import BaseModel

from app.domain.assignments import DeliveryAssignmentStatus
from app.domain.drivers import DriverAvailabilityStatus
from app.domain.orders import OrderStatus
from app.schemas.orders import DeliveryWindowResponse


class DriverResponse(BaseModel):
    driverId: str
    displayName: str
    availabilityStatus: DriverAvailabilityStatus
    activeAssignmentCount: int


class DriverAssignmentItem(BaseModel):
    assignmentId: str
    orderId: str
    assignmentStatus: DeliveryAssignmentStatus
    currentStatus: OrderStatus
    recipientName: str
    deliveryAddressSummary: str
    deliveryWindow: DeliveryWindowResponse
    lastUpdatedAt: datetime | None = None


class DriverAssignmentsResponse(BaseModel):
    driverId: str
    items: list[DriverAssignmentItem]
    page: int
    pageSize: int
    totalItems: int
