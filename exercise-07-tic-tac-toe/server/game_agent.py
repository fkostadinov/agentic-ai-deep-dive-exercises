from __future__ import annotations

import asyncio

from shared.a2a_types import RequestContext

from .game_state import GameState


class TicTacToeAgent:
    def __init__(self) -> None:
        self.state = GameState()
        self._current_context: RequestContext | None = None

    def set_context(self, context: RequestContext) -> None:
        self._current_context = context

    async def invoke(self) -> str:
        if self._current_context is None:
            raise RuntimeError("No request context set.")

        text = self._extract_text(self._current_context)
        await asyncio.sleep(0.1)
        return self._handle_command(text)

    def _extract_text(self, context: RequestContext) -> str:
        for part in context.message.parts:
            if part.get("type") == "text":
                return str(part.get("text", "")).strip()
        return ""

    def _handle_command(self, text: str) -> str:
        if text == "new":
            self.state.reset()
            return self.state.render()

        if text == "show":
            return self.state.render()

        if text.startswith("move "):
            parts = text.split()
            if len(parts) != 3:
                return "Usage: move <row> <col>"

            try:
                row = int(parts[1])
                col = int(parts[2])
            except ValueError:
                return "Row and column must be integers."

            message = self.state.make_move(row, col)
            return f"{message}\n\n{self.state.render()}"

        return "Unknown command. Use: new, show, move <row> <col>, exit"
