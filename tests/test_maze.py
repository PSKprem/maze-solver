"""Tests for :mod:`mazesolver.maze`."""

import pytest

from mazesolver.maze import Maze, MazeError


def test_parse_basic_maze():
    maze = Maze.from_string("S.\n.E")
    assert maze.rows == 2
    assert maze.cols == 2
    assert maze.start == (0, 0)
    assert maze.end == (1, 1)


def test_missing_start_raises():
    with pytest.raises(MazeError):
        Maze.from_string("..\n.E")


def test_missing_end_raises():
    with pytest.raises(MazeError):
        Maze.from_string("S.\n..")


def test_empty_maze_raises():
    with pytest.raises(MazeError):
        Maze.from_string("   \n  ")


def test_duplicate_start_raises():
    with pytest.raises(MazeError):
        Maze.from_string("SS\n.E")


def test_unknown_character_raises():
    with pytest.raises(MazeError):
        Maze.from_string("SX\n.E")


def test_ragged_rows_padded_with_walls():
    maze = Maze.from_string("S..\n.E")
    assert maze.cols == 3
    # The short second row should be padded with a wall.
    assert maze.grid[1][2] == "#"


def test_neighbors_are_walkable_and_in_order():
    maze = Maze.from_string("S.\n.E")
    neighbors = list(maze.neighbors((0, 0)))
    # From top-left: down then right (up/left are out of bounds).
    assert neighbors == [(1, 0), (0, 1)]


def test_is_walkable_respects_walls_and_bounds():
    maze = Maze.from_string("S#\n.E")
    assert maze.is_walkable((0, 0)) is True
    assert maze.is_walkable((0, 1)) is False  # wall
    assert maze.is_walkable((5, 5)) is False  # out of bounds


def test_render_overlays_path():
    maze = Maze.from_string("S.\n.E")
    rendered = maze.render([(0, 0), (0, 1), (1, 1)])
    assert "*" in rendered  # the (0,1) cell becomes a path marker
