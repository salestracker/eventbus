from collections.abc import AsyncGenerator
from typing import Any, Dict
from src.lib.registry import EventRegistry, QueueEvent
from src.rpc.eventbus_pb2_grpc import EventBusServicer
from src.rpc.eventbus_pb2 import (
    Event,
    EventRequest,
    EventResponse,
    ResponseType,
    SubscribeEventStream,
    SubscriberResponse,
    SubscriberStreamResponse,
)
import grpc
import asyncio
import datetime as dt
import zoneinfo

type EVENT_NAME_TYPE = str
type EVENTSTORE = Dict[str, EventRegistry]
DEFAULT_TTL = 120


class EventBusAsync(EventBusServicer):
    def __init__(
        self,
        *args,
        # TODO: Future instances could any Queable
        async_publisher_queue: None | asyncio.Queue[QueueEvent] = None,
        # TODO: Future instance object could have any compatible
        # eventstore backend
        eventstore: None | EVENTSTORE = None,
        **kwargs,
    ) -> None:
        self._async_pub_queue = async_publisher_queue or asyncio.Queue()
        self._eventstore: EVENTSTORE = eventstore or {}

        self._queue_processor_task = asyncio.create_task(
            self.enqueue_to_eventstore(self._async_pub_queue, self._eventstore)
        )
        # Lock to protect shared data structures mutation
        self._lock = asyncio.Lock()
        # TODO: add done callback on shutdown
        # self._queue_processor_task.add_done_callback
        super().__init__(*args, **kwargs)

    async def PublishEvent(
        self, request: EventRequest, context: grpc.aio.ServicerContext
    ) -> EventResponse:
        event = request.event
        event_data = dict(
            event_name=event.event_name,
            payload=event.payload,
            correlation_id=event.correlation_id,
            start_time=dt.datetime.now(zoneinfo.ZoneInfo("UTC")),
            ttl=event.ttl,
        )
        queue_event = EventRegistry.create_event(**event_data)
        await self._put_queue(queue_event)

        context.set_code(grpc.StatusCode.OK)
        return EventResponse(response=ResponseType(success=True))

    async def SubscribeEvent(
        self, request: SubscribeEventStream, context: grpc.aio.ServicerContext
    ) -> AsyncGenerator[Any, SubscriberStreamResponse]:
        subscriber_id = request.subscriber_id
        event_name = request.event_name
        registry: EventRegistry | None = None

        # Ensure the events list isn’t concurrently modified
        async with self._lock:
            if event_name not in self._eventstore:
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                return
            registry = self._eventstore[event_name]

            if not registry.subscribers:
                registry.subscribers = {}
                registry.subscribers[subscriber_id] = {}

            if registry.subscribers and subscriber_id not in registry.subscribers:
                registry.create_subscriber_map(subscriber_id)

        while registry.subscribers and subscriber_id in registry.subscribers:
            # Take a snapshot copy of registry.events
            # under lock and iterate over a copy.
            async with self._lock:
                registry = self._eventstore[event_name]
                queue_events = registry.filter_undelivered_events(subscriber_id) or []

            for queue_event in queue_events:
                event = Event(
                    event_name=queue_event.event_name,
                    payload=queue_event.payload,
                    correlation_id=queue_event.correlation_id,
                    ttl=int(queue_event.ttl),
                )
                response = SubscriberStreamResponse(
                    response=SubscriberResponse(
                        event=event, subscriber_id=subscriber_id
                    )
                )
                async with self._lock:
                    registry.set_subscriber_map(subscriber_id, queue_event)
                yield response

                await self._put_queue(queue_event)

            # TODO: Implement a way to flush() obsolete
            # correlation keys in registry.

    async def enqueue_to_eventstore(
        self, queue: asyncio.Queue[QueueEvent], eventstore: EVENTSTORE
    ) -> None:
        while queue_event := await queue.get():
            await self.process_queue(queue_event, eventstore)
            queue.task_done()

    async def process_queue(
        self, queue_event: QueueEvent, eventstore: EVENTSTORE
    ) -> None:
        if not queue_event:
            return
        # Remove event from queue upon TTL expiry
        if not EventRegistry.is_valid_event(queue_event) and (
            registry := eventstore.get(queue_event.event_name)
        ):
            async with self._lock:
                registry.events.remove(queue_event)
            return
        if (event_name := queue_event.event_name) and event_name not in eventstore:
            async with self._lock:
                eventstore[event_name] = EventRegistry(
                    event_name=event_name, events=[], subscribers={}
                )
        async with self._lock:
            registry = eventstore[event_name]
            registry.events += [queue_event]

    async def _put_queue(self, event: QueueEvent):
        try:
            self._async_pub_queue.put_nowait(event)
        except asyncio.QueueFull:
            await self._async_pub_queue.put(event)
