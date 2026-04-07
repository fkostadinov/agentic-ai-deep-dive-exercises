from __future__ import annotations

import asyncio

from shared.a2a_types import EventQueue, RequestContext
from shared.transport import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    deserialize_request,
    serialize_events,
)
from .executor import AgentExecutor
from .game_agent import TicTacToeAgent


class A2AServer:
    def __init__(self, executor: AgentExecutor) -> None:
        self.executor = executor

    async def handle_request(self, context: RequestContext) -> list[object]:
        queue = EventQueue()
        await self.executor.execute(context, queue)
        return queue.events


class A2ATcpServer:
    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
    ) -> None:
        agent = TicTacToeAgent()
        executor = AgentExecutor(agent)
        self.app_server = A2AServer(executor)
        self.host = host
        self.port = port

    async def run(self) -> None:
        server = await asyncio.start_server(
            self._handle_connection,
            host=self.host,
            port=self.port,
        )

        async with server:
            await server.serve_forever()

    async def _handle_connection(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        try:
            raw_request = await reader.readline()
            if not raw_request:
                return

            context = deserialize_request(raw_request.decode("utf-8"))
            events = await self.app_server.handle_request(context)
            writer.write((serialize_events(events) + "\n").encode("utf-8"))
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()
