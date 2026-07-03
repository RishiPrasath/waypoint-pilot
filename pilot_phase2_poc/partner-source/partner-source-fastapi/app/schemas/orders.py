from datetime import datetime

from pydantic import BaseModel

from app.domain.orders import ActorType, OrderStatus


class AssignedDriverResponse(BaseModel):
    driverId: str
    displayName: str


class DeliveryWindowResponse(BaseModel):
    start: datetime | None = None
    end: datetime | None = None


class LocationSnapshotResponse(BaseModel):
    label: str
    latitude: float | None = None
    longitude: float | None = None
    capturedAt: datetime | None = None


class OrderStatusResponse(BaseModel):
    orderId: str
    currentStatus: OrderStatus
    statusLabel: str
    estimatedDeliveryAt: datetime | None = None
    deliveryWindow: DeliveryWindowResponse
    currentLocation: LocationSnapshotResponse | None = None
    assignedDriver: AssignedDriverResponse | None = None
    lastUpdatedAt: datetime | None = None


class TimelineEventResponse(BaseModel):
    eventId: str
    status: OrderStatus
    statusLabel: str
    occurredAt: datetime
    actorType: ActorType
    actorId: str
    location: LocationSnapshotResponse | None = None
    note: str | None = None


class OrderTimelineResponse(BaseModel):
    orderId: str
    items: list[TimelineEventResponse]
    page: int
    pageSize: int
    totalItems: int


class CreateStatusEventRequest(BaseModel):
    driverId: str
    status: OrderStatus
    occurredAt: datetime | None = None
    location: LocationSnapshotResponse | None = None
    note: str | None = None
    proofOfDeliveryAvailable: bool | None = None


class StatusEventResponse(BaseModel):
    eventId: str
    orderId: str
    previousStatus: OrderStatus
    newStatus: OrderStatus
    statusLabel: str
    occurredAt: datetime
    actorType: ActorType
    actorId: str
    location: LocationSnapshotResponse | None = None
    note: str | None = None
    proofOfDeliveryAvailable: bool | None = None
    orderCurrentStatus: OrderStatus
