from __future__ import annotations

import asyncio

from server import A2ATcpServer


async def main() -> None:
    server = A2ATcpServer()
    print("A2A Tic-Tac-Toe server listening on 127.0.0.1:8765")
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
