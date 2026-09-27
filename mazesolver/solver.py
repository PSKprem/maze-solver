"""Path-finding algorithms for :class:`~mazesolver.maze.Maze`.

Three classic algorithms are provided:

* :func:`bfs` - Breadth-first search. Guarantees the shortest path (in number
  of steps) on an unweighted grid.
* :func:`dfs` - Depth-first search. Fast and low-memory but does **not**
  guarantee the shortest path.
* :func:`astar` - A* search with the Manhattan-distance heuristic. Guarantees
  the shortest path and usually explores fewer cells than BFS.

Every function returns a :class:`SolveResult` so callers can compare cost and
efficiency across algorithms.
"""

from __future__ import annotations

import heapq
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional

from .maze import Coord, Maze


@dataclass
class SolveResult:
    """The outcome of a solve attempt.

    Attributes:
        path: Ordered list of coordinates from start to end, or ``None`` if
            the goal is unreachable.
        explored: Number of cells expanded during the search. Useful for
            comparing algorithm efficiency.
    """

    path: Optional[List[Coord]]
    explored: int

    @property
    def solved(self) -> bool:
        """``True`` if a path to the goal was found."""
        return self.path is not None

    @property
    def length(self) -> int:
        """Number of cells in the path (0 if unsolved)."""
        return len(self.path) if self.path else 0


def _reconstruct(came_from: Dict[Coord, Coord], start: Coord, end: Coord) -> List[Coord]:
    """Rebuild the path from ``start`` to ``end`` using the ``came_from`` map."""
    path: List[Coord] = [end]
    node = end
    while node != start:
        node = came_from[node]
        path.append(node)
    path.reverse()
    return path


def bfs(maze: Maze) -> SolveResult:
    """Solve ``maze`` with breadth-first search (shortest path guaranteed)."""
    start, end = maze.start, maze.end
    frontier: deque[Coord] = deque([start])
    came_from: Dict[Coord, Coord] = {}
    visited = {start}
    explored = 0

    while frontier:
        current = frontier.popleft()
        explored += 1
        if current == end:
            return SolveResult(_reconstruct(came_from, start, end), explored)
        for nxt in maze.neighbors(current):
            if nxt not in visited:
                visited.add(nxt)
                came_from[nxt] = current
                frontier.append(nxt)

    return SolveResult(None, explored)


def dfs(maze: Maze) -> SolveResult:
    """Solve ``maze`` with depth-first search (path not guaranteed shortest)."""
    start, end = maze.start, maze.end
    stack: List[Coord] = [start]
    came_from: Dict[Coord, Coord] = {}
    visited = {start}
    explored = 0

    while stack:
        current = stack.pop()
        explored += 1
        if current == end:
            return SolveResult(_reconstruct(came_from, start, end), explored)
        for nxt in maze.neighbors(current):
            if nxt not in visited:
                visited.add(nxt)
                came_from[nxt] = current
                stack.append(nxt)

    return SolveResult(None, explored)


def _manhattan(a: Coord, b: Coord) -> int:
    """Manhattan distance between two grid coordinates."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(maze: Maze) -> SolveResult:
    """Solve ``maze`` with A* search using the Manhattan heuristic."""
    start, end = maze.start, maze.end
    # The priority queue holds (f_score, tie_breaker, coord).
    counter = 0
    frontier: List[tuple] = [(0, counter, start)]
    came_from: Dict[Coord, Coord] = {}
    g_score: Dict[Coord, int] = {start: 0}
    explored = 0

    while frontier:
        _, _, current = heapq.heappop(frontier)
        explored += 1
        if current == end:
            return SolveResult(_reconstruct(came_from, start, end), explored)
        for nxt in maze.neighbors(current):
            tentative = g_score[current] + 1
            if tentative < g_score.get(nxt, float("inf")):
                came_from[nxt] = current
                g_score[nxt] = tentative
                counter += 1
                f_score = tentative + _manhattan(nxt, end)
                heapq.heappush(frontier, (f_score, counter, nxt))

    return SolveResult(None, explored)


#: Mapping of algorithm names to their solver functions.
ALGORITHMS = {
    "bfs": bfs,
    "dfs": dfs,
    "astar": astar,
}


def solve(maze: Maze, algorithm: str = "bfs") -> SolveResult:
    """Solve ``maze`` using the named ``algorithm``.

    Args:
        maze: The maze to solve.
        algorithm: One of ``"bfs"``, ``"dfs"``, or ``"astar"``.

    Returns:
        A :class:`SolveResult`.

    Raises:
        ValueError: If ``algorithm`` is not recognised.
    """
    key = algorithm.lower()
    if key not in ALGORITHMS:
        valid = ", ".join(sorted(ALGORITHMS))
        raise ValueError(f"Unknown algorithm {algorithm!r}. Choose from: {valid}.")
    return ALGORITHMS[key](maze)
