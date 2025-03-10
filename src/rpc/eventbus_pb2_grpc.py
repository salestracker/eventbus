# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""

import grpc

import src.rpc.eventbus_pb2 as eventbus__pb2

GRPC_GENERATED_VERSION = "1.70.0"
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower

    _version_not_supported = first_version_is_lower(
        GRPC_VERSION, GRPC_GENERATED_VERSION
    )
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f"The grpc package installed is at version {GRPC_VERSION},"
        + " but the generated code in eventbus_pb2_grpc.py depends on"
        + f" grpcio>={GRPC_GENERATED_VERSION}."
        + f" Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}"
        + f" or downgrade your generated code using grpcio-tools<={GRPC_VERSION}."
    )


class EventBusStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PublishEvent = channel.unary_unary(
            "/eventbus.EventBus/PublishEvent",
            request_serializer=eventbus__pb2.EventRequest.SerializeToString,
            response_deserializer=eventbus__pb2.EventResponse.FromString,
            _registered_method=True,
        )
        self.SubscribeEvent = channel.unary_unary(
            "/eventbus.EventBus/SubscribeEvent",
            request_serializer=eventbus__pb2.SubscribeEventStream.SerializeToString,
            response_deserializer=eventbus__pb2.SubscriberStreamResponse.FromString,
            _registered_method=True,
        )


class EventBusServicer(object):
    """Missing associated documentation comment in .proto file."""

    def PublishEvent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def SubscribeEvent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_EventBusServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "PublishEvent": grpc.unary_unary_rpc_method_handler(
            servicer.PublishEvent,
            request_deserializer=eventbus__pb2.EventRequest.FromString,
            response_serializer=eventbus__pb2.EventResponse.SerializeToString,
        ),
        "SubscribeEvent": grpc.unary_unary_rpc_method_handler(
            servicer.SubscribeEvent,
            request_deserializer=eventbus__pb2.SubscribeEventStream.FromString,
            response_serializer=eventbus__pb2.SubscriberStreamResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "eventbus.EventBus", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers("eventbus.EventBus", rpc_method_handlers)


# This class is part of an EXPERIMENTAL API.
class EventBus(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def PublishEvent(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(  # pyright: ignore[reportAttributeAccessIssue]
            request,
            target,
            "/eventbus.EventBus/PublishEvent",
            eventbus__pb2.EventRequest.SerializeToString,
            eventbus__pb2.EventResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def SubscribeEvent(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(  # pyright: ignore[reportAttributeAccessIssue]
            request,
            target,
            "/eventbus.EventBus/SubscribeEvent",
            eventbus__pb2.SubscribeEventStream.SerializeToString,
            eventbus__pb2.SubscriberStreamResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )
