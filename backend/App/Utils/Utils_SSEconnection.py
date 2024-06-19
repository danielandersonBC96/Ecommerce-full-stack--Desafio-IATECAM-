from typing import Generator, List
from fastapi import Request, Response
from starlette.responses import StreamingResponse
import asyncio

class SSEManager:
    def __init__(self):
        self.event_generators: List[str] = []
        self.sse_connections: List[StreamingResponse] = []

    async def event_generator(self) -> Generator[str, None, None]:
        """
        Async generator that yields SSE formatted data periodically.
        """
        while True:
            await asyncio.sleep(1)
            if self.sse_connections:
                for event_data in self.event_generators:
                    yield f"data: {event_data}\n\n"

    async def sse_endpoint(self) -> Response:
        """
        Returns a StreamingResponse for SSE connections.
        """
        response = StreamingResponse(self.event_generator(), media_type="text/event-stream")
        self.sse_connections.append(response)
        return response

    def send_event(self, event_data: str):
        """
        Sends an SSE event to all connected clients.
        """
        for connection in self.sse_connections:
            try:
                connection.body.write(f"data: {event_data}\n\n".encode("utf-8"))
                connection.body.flush()
            except RuntimeError:
                self.sse_connections.remove(connection)

    def register_event_data(self, event_data: str):
        """
        Registers new event data to be included in SSE broadcasts.
        """
        self.event_generators.append(event_data)

    def get_event_data(self) -> List[str]:
        """
        Returns all registered event data.
        """
        return self.event_generators

    def remove_connection(self, connection: StreamingResponse):
        """
        Removes a closed SSE connection.
        """
        if connection in self.sse_connections:
            self.sse_connections.remove(connection)

sse_manager = SSEManager()
