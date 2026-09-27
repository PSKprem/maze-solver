"""Maze representation and parsing utilities.

A maze is stored as a 2D grid of characters. The parser understands the
following symbols:

===== ==================================================
Char  Meaning
===== ==================================================
``#``   Wall (impassable)
``.``   Open path (walkable)
``S``   Start position
``E``   End / goal position
===== ==================================================

Any whitespace-only lines are ignored. All rows are padded to the width of
the widest row so the grid is always rectangular.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, List, Optional, Tuple

# A coordinate is a (row, column) pair.
Coord = Tuple[int, int]

WALL = "#"
OPEN = "."
START = "S"
END = "E"


class MazeError(ValueError):
    """Raised when a maze cannot be parsed or is invalid."""


@dataclass
class Maze:
    """An immutable-ish grid maze.

    Attributes:
        grid: The 2D list of single-character cells.
        start: The ``(row, col)`` of the start cell.
        end: The ``(row, col)`` of the goal cell.
    """

    grid: List[List[str]]
    start: Coord
    end: Coord
    rows: int = field(init=False)
    cols: int = field(init=False)

    def __post_init__(self) -> None:
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.grid else 0

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------
    @classmethod
    def from_string(cls, text: str) -> "Maze":
        """Build a :class:`Maze` from a multi-line string.

        Args:
            text: The maze layout as text.

        Returns:
            A parsed :class:`Maze`.

        Raises:
            MazeError: If the maze has no start, no end, or is empty.
        """
        lines = [line for line in text.splitlines() if line.strip() != ""]
        if not lines:
            raise MazeError("Maze is empty.")

        width = max(len(line) for line in lines)
        grid: List[List[str]] = []
        start: Optional[Coord] = None
        end: Optional[Coord] = None

        for r, line in enumerate(lines):
            # Pad short rows with walls so the grid is rectangular.
            padded = line.ljust(width, WALL)
            row: List[str] = []
            for c, ch in enumerate(padded):
                if ch == " ":
                    ch = OPEN
                if ch not in (WALL, OPEN, START, END):
                    raise MazeError(
                        f"Unknown character {ch!r} at row {r}, column {c}."
                    )
                if ch == START:
                    if start is not None:
                        raise MazeError("Maze has more than one start (S).")
                    start = (r, c)
                elif ch == END:
                    if end is not None:
                        raise MazeError("Maze has more than one end (E).")
                    end = (r, c)
                row.append(ch)
            grid.append(row)

        if start is None:
            raise MazeError("Maze has no start (S).")
        if end is None:
            raise MazeError("Maze has no end (E).")

        return cls(grid=grid, start=start, end=end)

    @classmethod
    def from_file(cls, path: str) -> "Maze":
        """Load a maze from a text file (UTF-8)."""
        with open(path, "r", encoding="utf-8") as handle:
            return cls.from_string(handle.read())

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def in_bounds(self, coord: Coord) -> bool:
        """Return ``True`` if ``coord`` lies inside the grid."""
        r, c = coord
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_walkable(self, coord: Coord) -> bool:
        """Return ``True`` if ``coord`` is inside the grid and not a wall."""
        if not self.in_bounds(coord):
            return False
        r, c = coord
        return self.grid[r][c] != WALL

    def neighbors(self, coord: Coord) -> Iterator[Coord]:
        """Yield the walkable 4-connected neighbours of ``coord``.

        Neighbours are yielded in a stable order: up, down, left, right.
        """
        r, c = coord
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            candidate = (r + dr, c + dc)
            if self.is_walkable(candidate):
                yield candidate

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def render(self, path: Optional[List[Coord]] = None) -> str:
        """Render the maze as text, optionally overlaying a ``path``.

        Cells on the path (excluding start/end) are drawn with ``*``.

        Args:
            path: An ordered list of coordinates from start to end.

        Returns:
            The rendered maze string.
        """
        path_set = set(path or [])
        out_rows: List[str] = []
        for r in range(self.rows):
            chars: List[str] = []
            for c in range(self.cols):
                cell = self.grid[r][c]
                if (r, c) in path_set and cell not in (START, END):
                    chars.append("*")
                else:
                    chars.append(cell)
            out_rows.append("".join(chars))
        return "\n".join(out_rows)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.render()
