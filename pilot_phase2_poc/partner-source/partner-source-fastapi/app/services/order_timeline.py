from app.errors.exceptions import OrderNotFoundError
from app.repositories.orders import InMemoryOrderRepository
from app.repositories.status_events import InMemoryStatusEventRepository
from app.schemas.orders import OrderTimelineResponse, TimelineEventResponse


class OrderTimelineService:
    def __init__(
        self,
        order_repository: InMemoryOrderRepository,
        status_event_repository: InMemoryStatusEventRepository,
    ) -> None:
        self._order_repository = order_repository
        self._status_event_repository = status_event_repository

    def get_timeline(self, order_id: str, page: int, page_size: int) -> OrderTimelineResponse:
        order = self._order_repository.find_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)

        events = self._status_event_repository.find_by_order_id(order_id)
        start = (page - 1) * page_size
        end = start + page_size

        return OrderTimelineResponse(
            orderId=order_id,
            items=[
                TimelineEventResponse(
                    eventId=event.event_id,
                    status=event.new_status,
                    statusLabel=event.status_label,
                    occurredAt=event.occurred_at,
                    actorType=event.actor_type,
                    actorId=event.actor_id,
                )
                for event in events[start:end]
            ],
            page=page,
            pageSize=page_size,
            totalItems=len(events),
        )
