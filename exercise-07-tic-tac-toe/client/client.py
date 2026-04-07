from __future__ import annotations

import asyncio
from uuid import uuid4

from shared.a2a_types import RequestContext, new_text_message
from shared.transport import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    deserialize_events,
    serialize_request,
)


class A2AClient:
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
        self.host = host
        self.port = port

    async def send_text(self, text: str) -> list[object]:
        context = RequestContext(
            task_id=str(uuid4()),
            context_id=str(uuid4()),
            message=new_text_message(text),
        )
        return await self.send_request(context)

    async def send_request(self, context: RequestContext) -> list[object]:
        reader, writer = await asyncio.open_connection(self.host, self.port)
        try:
            writer.write((serialize_request(context) + "\n").encode("utf-8"))
            await writer.drain()

            raw_response = await reader.readline()
            if not raw_response:
                raise ConnectionError("Server closed the connection without a response.")

            return deserialize_events(raw_response.decode("utf-8"))
        finally:
            writer.close()
            await writer.wait_closed()
