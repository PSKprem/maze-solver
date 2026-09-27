# Maze Solver

A small, well-documented Python library and command-line tool for solving text
mazes using three classic path-finding algorithms:

- **BFS** (Breadth-First Search) - guarantees the shortest path.
- **DFS** (Depth-First Search) - fast and memory-light, but the path may not be shortest.
- **A\*** (A-star) - guarantees the shortest path and usually explores fewer cells than BFS.

## Features

- Clean, documented API (`Maze`, `solve`, `bfs`, `dfs`, `astar`).
- A CLI that can run one algorithm or compare all three.
- Renders the solved path back onto the maze.
- Reports how many cells each algorithm explored, so you can compare efficiency.
- Full unit-test suite.

## Maze format

Mazes are plain text files using these symbols:

| Symbol | Meaning              |
|--------|----------------------|
| `#`    | Wall (impassable)    |
| `.`    | Open path (walkable) |
| `S`    | Start position       |
| `E`    | End / goal position  |

Example (`examples/small.txt`):

```
S.#
.#.
..E
```

## Installation

Clone the repository and (optionally) install the test dependency:

```bash
git clone https://github.com/PSKprem/maze-solver.git
cd maze-solver
pip install -r requirements.txt   # only needed to run the tests
```

The library itself has **no runtime dependencies** beyond the Python standard
library (Python 3.8+).

## Usage

### Command line

```bash
# Solve with the default algorithm (BFS)
python -m mazesolver examples/simple.txt

# Choose an algorithm
python -m mazesolver examples/simple.txt --algorithm astar

# Compare all three algorithms
python -m mazesolver examples/simple.txt --algorithm all

# Only show statistics, no rendered maze
python -m mazesolver examples/simple.txt --no-render
```

Sample output:

```
== ASTAR ==
Solved! Path length: 3, cells explored: 4
S*#
.#*
..E
```

### As a library

```python
from mazesolver import Maze, solve

maze = Maze.from_file("examples/small.txt")
result = solve(maze, "astar")

if result.solved:
    print(f"Path length: {result.length}")
    print(maze.render(result.path))
else:
    print("No path found.")
```

## Running the tests

```bash
pip install -r requirements.txt
pytest
```

## Project layout

```
maze-solver/
├── mazesolver/          # the library
│   ├── __init__.py      # public API
│   ├── __main__.py      # CLI entry point
│   ├── maze.py          # maze representation & parser
│   └── solver.py        # BFS / DFS / A* algorithms
├── examples/            # sample maze files
├── tests/               # unit tests
├── docs/                # extra documentation
├── README.md
├── LICENSE
└── requirements.txt
```

## How the algorithms compare

| Algorithm | Shortest path? | Memory | Notes                                   |
|-----------|----------------|--------|-----------------------------------------|
| BFS       | Yes            | High   | Explores all cells at each depth first. |
| DFS       | No             | Low    | Dives deep; good when any path will do. |
| A\*       | Yes            | Medium | Uses a heuristic to search toward goal. |

See [`docs/algorithms.md`](docs/algorithms.md) for a deeper explanation.

## License

Released under the MIT License. See [LICENSE](LICENSE).
