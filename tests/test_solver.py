"""Tests for :mod:`mazesolver.solver`."""

import pytest

from mazesolver.maze import Maze
from mazesolver.solver import ALGORITHMS, astar, bfs, dfs, solve


SOLVABLE = "S.#\n.#.\n..E"
UNSOLVABLE = "S#E\n.#.\n.#."


@pytest.mark.parametrize("algorithm", sorted(ALGORITHMS))
def test_all_algorithms_solve_solvable_maze(algorithm):
    maze = Maze.from_string(SOLVABLE)
    result = solve(maze, algorithm)
    assert result.solved
    # Path must start at start and end at end.
    assert result.path[0] == maze.start
    assert result.path[-1] == maze.end


@pytest.mark.parametrize("algorithm", sorted(ALGORITHMS))
def test_all_algorithms_report_unsolvable(algorithm):
    maze = Maze.from_string(UNSOLVABLE)
    result = solve(maze, algorithm)
    assert not result.solved
    assert result.path is None
    assert result.length == 0


def test_bfs_and_astar_find_shortest_path():
    maze = Maze.from_string(SOLVABLE)
    bfs_result = bfs(maze)
    astar_result = astar(maze)
    # BFS and A* both guarantee the shortest path length.
    assert bfs_result.length == astar_result.length


def test_path_is_contiguous():
    maze = Maze.from_string(SOLVABLE)
    result = bfs(maze)
    for (r1, c1), (r2, c2) in zip(result.path, result.path[1:]):
        assert abs(r1 - r2) + abs(c1 - c2) == 1  # each step moves one cell


def test_dfs_returns_valid_path():
    maze = Maze.from_string(SOLVABLE)
    result = dfs(maze)
    assert result.solved
    assert result.path[0] == maze.start
    assert result.path[-1] == maze.end


def test_unknown_algorithm_raises():
    maze = Maze.from_string(SOLVABLE)
    with pytest.raises(ValueError):
        solve(maze, "dijkstra")


def test_explored_count_is_positive():
    maze = Maze.from_string(SOLVABLE)
    assert bfs(maze).explored > 0
