# EventBus

**A simple, gRPC-based event queuing bus for Python**

For a lack of better name, just eventbus.

*Note: Work In Progress. Currently unstable and rapidly evolving.*

## Overview

EventBus is a lightweight, event-driven messaging system built in Python using gRPC and asyncio. It is designed to:

- **Broadcast Events Efficiently:**  
  Every published event is mapped to all subscribers that register an interest, using a centralized ephemeral consumer queue.

- **Manage Redelivery:**  
  With a per-subscriber delivery flag and a TTL (time-to-live) mechanism, each event is delivered only once per subscriber (or redelivered up to a configurable limit).

- **Support Asynchronous Processing:**  
  Leveraging Python’s `asyncio` and `grpc.aio`, EventBus enables non-blocking I/O, ensuring scalability even with hundreds of subscribers.

- **Centralized Event Store:**  
  Events are stored in an `EventRegistry` per event type, along with a mapping of subscriber IDs to their delivery status.


### Why another event driven queue?

Use this if:

- Kafka is expensive to setup and run in terms of infrastructure if you just want to test something quickly. There are managed versions but if you want to even avoid that and prototype something.
- Redis is great but you want to avoid the setup overhead on your local as well. With or without docker.
- Celery exists but if you don't want too many API references and dig into it's know-how.
- You don't want to invest in cloud infrastructure and deal with mid-data, not big-data.
- You don't care about persistence. Not yet, although support for decoupled eventstore and external queueing system is planned but persistence is not your primary motive.

---

## Usage

### Publishing Events

Publishers call the unary RPC PublishEvent with an EventRequest. The server enqueues the event and maps it to all relevant subscribers in a centralized ephemeral queue.

### Subscribing to Events

Subscribers call the streaming RPC SubscribeEvent with a SubscribeEventStream message. The service:

	•	Maintains a per-subscriber mapping (a dictionary mapping event correlation IDs to a delivery flag).
	•	Iterates over the event store (using snapshot copies) and yields only events not yet delivered.
	•	Marks an event as delivered once it is streamed to the subscriber.
	•	Optionally requeues events for redelivery until their TTL exceeds the maximum.

### Redelivery

Each event’s TTL is incremented upon delivery. If an event exceeds the maximum TTL, it is dropped and not redelivered.

---

## Getting Started

### Prerequisites

- Python 3.12+
- Poetry for dependency management and project scaffolding
- gRPC and related packages:

```bash
poetry add grpcio grpcio-tools
```

Run it like:
```bash
 GRPC_VERBOSITY=debug [poetry run] python -m src.main
 ```

---

## Architecture

### High-Level Components

1. **Publish Phase (Unary RPC):**
   - Publishers call the `PublishEvent` RPC to send an event.
   - The event is enqueued in a persistent `publish_events_queue`.
   - The service checks its subscription registry (mapping of event types to subscriber IDs) and adds an entry `(subscriber_id, event)` to a centralized ephemeral consumer queue for each matching subscriber.
   - Each event starts with a TTL counter value set. The TTL value is checked asynchronously in another coroutine whether to retire the event from eventstore.

2. **Consumption Phase (Server Streaming RPC):**
   - Subscribers call the `SubscribeEvent` RPC with their subscriber ID and a list of event types.
   - The EventBus service delivers events from the ephemeral consumer queue that have not yet been delivered to that subscriber.
   - When an event is delivered, it is marked as delivered for that subscriber. If the TTL exceeds a configurable maximum, the event is dropped; otherwise, it is requeued for redelivery in the same eventstore.

3. **Redelivery Mechanism & Delivery Flags:**
   - Each subscriber’s delivery state is maintained in a dictionary mapping each event’s correlation ID to a boolean flag.
   - Only events not yet marked as delivered are streamed to the subscriber.
   - After streaming, the event is marked as delivered (ensuring no duplicate delivery), or optionally requeued for redelivery until it expires.

### Concurrency & Consistency

- **Asynchronous Locks:**  
  Shared data structures (such as the event store and subscriber mappings) are protected using an `asyncio.Lock` to prevent race conditions when multiple coroutines modify state concurrently.

- **Snapshot Iteration:**  
  The code uses snapshot copies (e.g. `tuple(registry.events)`) to safely iterate over events while preventing inconsistencies from concurrent modifications.

- **Delivery Tracking:**  
  In the subscription loop, only events that are not yet marked as delivered (i.e. with a delivery flag set to `False`) are yielded. Immediately after yielding, the flag is set to `True`.

---

## Developing
### Building the Protobuf Files

Run the following command from your project root:
```bash
python -m grpc_tools.protoc -I./proto --python_out=./src/rpc  --pyi_out=./src/rpc  --grpc_python_out=./src/rpc  --dependency_out=./src/rpc/proto_dependency --include_imports  ./src/proto/eventbus.proto
```

This will generate:

    - eventbus_pb2.py – the message classes.
    - eventbus_pb2_grpc.py – the gRPC stub and servicer classes.