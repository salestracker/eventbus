from typing import Dict, List, Annotated, Optional
from collections.abc import Mapping
import dataclasses
import datetime as dt

from src.lib.utils import datetime_now, to_timestamp
from src.rpc.eventbus_pb2 import PayloadValue
import enum

type PAYLOAD_VALUE_TYPE = str | int | float


class DeliveryStatus(enum.IntEnum):
    PENDING = 0
    DELIVERED = 1
    FAILED = 2


@dataclasses.dataclass(slots=True, frozen=True)
class QueueEvent:
    event_name: str
    # payload: Mapping[str, List[PAYLOAD_VALUE_TYPE] | PAYLOAD_VALUE_TYPE]
    payload: Mapping[str, PayloadValue]
    correlation_id: str
    start_time: dt.datetime
    ttl: float


@dataclasses.dataclass(slots=True)
class EventRegistry:
    event_name: Annotated[str, QueueEvent.event_name]
    events: List[QueueEvent]
    # map subscriber IDs to a dictionary that maps correlation IDs to a delivery flag
    subscribers: Optional[Dict[str, Dict[str, DeliveryStatus]]]

    @staticmethod
    def create_event(**data):
        return QueueEvent(**data)

    @staticmethod
    def is_valid_event(queue_event: QueueEvent) -> bool:
        end_time = to_timestamp(datetime_now())
        start_time = to_timestamp(queue_event.start_time)
        if end_time - start_time > queue_event.ttl:
            return False
        return True

    def create_subscriber_map(self, /, subscriber_id: str) -> None:
        if self.subscribers:
            self.subscribers[subscriber_id] = {
                event.correlation_id: DeliveryStatus.PENDING for event in self.events
            }

    def get_subscriber_map(
        self, /, subscriber_id: str
    ) -> Dict[str, DeliveryStatus] | None:
        if self.subscribers and (subscriber_map := self.subscribers.get(subscriber_id)):
            return dict(subscriber_map)

    def set_subscriber_map(
        self, /, subscriber_id: str, queue_event: QueueEvent
    ) -> None:
        if self.subscribers:
            self.subscribers[subscriber_id][queue_event.correlation_id] = (
                DeliveryStatus.DELIVERED
            )

    def filter_undelivered_events(
        self, /, subscriber_id: str
    ) -> None | List[QueueEvent]:
        if subscriber_queue_map := self.get_subscriber_map(subscriber_id):
            return list(
                filter(
                    lambda event: not subscriber_queue_map.get(event.correlation_id),
                    self.events,
                )
            )
