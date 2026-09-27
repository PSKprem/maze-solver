"""mazesolver - a small, well-documented maze solving library.

Public API:

    >>> from mazesolver import Maze, solve
    >>> maze = Maze.from_string("S.#\\n.#.\\n..E")
    >>> result = solve(maze, "astar")
    >>> result.solved
    True
"""

from .maze import Maze, MazeError, Coord
from .solver import SolveResult, solve, bfs, dfs, astar, ALGORITHMS

__all__ = [
    "Maze",
    "MazeError",
    "Coord",
    "SolveResult",
    "solve",
    "bfs",
    "dfs",
    "astar",
    "ALGORITHMS",
]

__version__ = "1.0.0"
