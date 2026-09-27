"""Command-line interface for the maze solver.

Usage examples::

    python -m mazesolver examples/simple.txt
    python -m mazesolver examples/simple.txt --algorithm astar
    python -m mazesolver examples/simple.txt --algorithm all
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .maze import Maze, MazeError
from .solver import ALGORITHMS, solve


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="mazesolver",
        description="Solve a text maze using BFS, DFS, or A* search.",
    )
    parser.add_argument("maze", help="Path to a maze text file.")
    parser.add_argument(
        "-a",
        "--algorithm",
        default="bfs",
        choices=sorted(ALGORITHMS) + ["all"],
        help="Algorithm to use (default: bfs). Use 'all' to compare them.",
    )
    parser.add_argument(
        "--no-render",
        action="store_true",
        help="Do not print the solved maze, only statistics.",
    )
    return parser


def _run_one(maze: Maze, algorithm: str, render: bool) -> None:
    """Solve with a single algorithm and print the outcome."""
    result = solve(maze, algorithm)
    print(f"== {algorithm.upper()} ==")
    if result.solved:
        print(f"Solved! Path length: {result.length}, cells explored: {result.explored}")
        if render:
            print(maze.render(result.path))
    else:
        print(f"No path found. Cells explored: {result.explored}")
    print()


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point. Returns a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        maze = Maze.from_file(args.maze)
    except FileNotFoundError:
        print(f"Error: file not found: {args.maze}", file=sys.stderr)
        return 2
    except MazeError as exc:
        print(f"Error: invalid maze: {exc}", file=sys.stderr)
        return 2

    algorithms = sorted(ALGORITHMS) if args.algorithm == "all" else [args.algorithm]
    for algorithm in algorithms:
        _run_one(maze, algorithm, render=not args.no_render)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
