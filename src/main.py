import asyncio
from concurrent import futures
import grpc
from src.rpc.eventbus_pb2_grpc import add_EventBusServicer_to_server
from src.service import EventBusAsync


# TODO: fix RuntimeWarning: coroutine 'AioServer.shutdown' was never awaited
async def serve():
    with futures.ThreadPoolExecutor() as exc:
        server = grpc.aio.server(
            migration_thread_pool=exc, compression=grpc.Compression.Gzip
        )

        # Create an instance of EventBusAsync
        event_bus_servicer = EventBusAsync()

        # Register the servicer with the server
        add_EventBusServicer_to_server(event_bus_servicer, server)

        # Configure the ALTS credentials
        # alts_channel_creds = grpc.alts_server_credentials()

        # # Bind the server to localhost or a specific IP address and port
        # server.add_secure_port('localhost:50051', alts_channel_creds)

        # Start the server
        await server.start()
        print("Server started on localhost:50051")

        # Wait for the server to stop
        await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
