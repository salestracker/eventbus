from typing import Dict, List, Annotated, Optional
from collections.abc import Mapping
import dataclasses
import datetime as dt

from src.lib.utils import datetime_now, to_timestamp
from src.rpc.eventbus_pb2 import PayloadValue

type PAYLOAD_VALUE_TYPE = str | int | float


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
    subscribers: Optional[Dict[str, Dict[str, bool]]]

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
