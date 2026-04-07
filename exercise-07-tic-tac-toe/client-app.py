from __future__ import annotations

import asyncio

from client import A2AClient
from shared.a2a_types import (
    Task,
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
)


def print_events(events: list[object]) -> None:
    for event in events:
        if isinstance(event, Task):
            print("[TASK] submitted")
        elif isinstance(event, TaskStatusUpdateEvent):
            message = ""
            if event.status.message:
                for part in event.status.message.parts:
                    if part.get("type") == "text":
                        message = part.get("text", "")
                        break
            suffix = f" - {message}" if message else ""
            print(f"[STATUS] {event.status.state.value}{suffix}")
        elif isinstance(event, TaskArtifactUpdateEvent):
            text = event.artifact.get("text", "")
            print(f"[ARTIFACT]\n{text}")


async def main() -> None:
    client = A2AClient()

    print("A2A Tic-Tac-Toe CLI. Start the server, then type 'new', 'show', 'move <row> <col>', or 'exit'.")

    # Listen to user inputs in the terminal.
    while True:
        user_input = input("\n> ").strip()
        if user_input == "exit":
            print("Goodbye.")
            break

        try:
            events = await client.send_text(user_input)
        except OSError:
            print("Could not reach the A2A server. Start server-app.py first.")
            continue

        print_events(events)


if __name__ == "__main__":
    asyncio.run(main())
