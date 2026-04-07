from __future__ import annotations
from dataclasses import dataclass, field


WIN_LINES = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]


@dataclass
class GameState:
    board: list[list[str]] = field(default_factory=lambda: [["."] * 3 for _ in range(3)])
    next_player: str = "X"
    winner: str | None = None
    draw: bool = False

    def reset(self) -> None:
        self.board = [["."] * 3 for _ in range(3)]
        self.next_player = "X"
        self.winner = None
        self.draw = False

    def render(self) -> str:
        lines = ["Board:", "  0 1 2"]
        for row_index, row in enumerate(self.board):
            lines.append(f"{row_index} " + " ".join(row))

        if self.winner:
            lines.append(f"Winner: {self.winner}")
        elif self.draw:
            lines.append("Result: draw")
        else:
            lines.append(f"Next player: {self.next_player}")

        return "\n".join(lines)

    def make_move(self, row: int, col: int) -> str:
        if self.winner or self.draw:
            return "Game is already over. Start a new game with 'new'."

        if row not in range(3) or col not in range(3):
            return "Invalid move. Row and column must be between 0 and 2."

        if self.board[row][col] != ".":
            return "Cell is already occupied."

        self.board[row][col] = self.next_player
        self._update_result()

        if not self.winner and not self.draw:
            self.next_player = "O" if self.next_player == "X" else "X"

        return "Move accepted."

    def _update_result(self) -> None:
        for line in WIN_LINES:
            symbols = [self.board[r][c] for r, c in line]
            if symbols[0] != "." and symbols.count(symbols[0]) == 3:
                self.winner = symbols[0]
                return

        if all(cell != "." for row in self.board for cell in row):
            self.draw = True
