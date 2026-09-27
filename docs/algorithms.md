# Algorithms

This document explains the three path-finding algorithms implemented in
`mazesolver.solver`. Every maze is treated as an **unweighted, 4-connected
grid**: from any open cell you may move up, down, left, or right into any
adjacent open cell, and each move costs 1.

## Breadth-First Search (BFS)

BFS explores the maze in "rings" of increasing distance from the start. It uses
a FIFO queue, so all cells at distance *d* are visited before any cell at
distance *d + 1*.

- **Shortest path:** Yes. Because it expands cells in order of distance, the
  first time it reaches the goal it has found a shortest path.
- **Memory:** High. The frontier can hold a large number of cells at once.
- **When to use:** When you need the shortest path and the maze is not huge.

```
Time:  O(V + E)
Space: O(V)
```

## Depth-First Search (DFS)

DFS dives as deep as possible along one branch before backtracking. It uses a
LIFO stack.

- **Shortest path:** No. DFS returns *a* path, not necessarily the shortest.
- **Memory:** Low. Only the current branch and visited set are held.
- **When to use:** When any valid path is acceptable, or memory is tight.

```
Time:  O(V + E)
Space: O(V)  (worst case; typically much less than BFS in practice)
```

## A* Search

A* is a best-first search guided by a heuristic. For each cell it tracks:

- `g` - the known cost from the start to that cell, and
- `h` - an estimate of the remaining cost to the goal (the heuristic).

It always expands the cell with the lowest `f = g + h`. This implementation
uses the **Manhattan distance** as the heuristic:

```
h(cell) = |cell.row - goal.row| + |cell.col - goal.col|
```

Manhattan distance is *admissible* (never overestimates the true cost) on a
4-connected grid, so A* is guaranteed to find the shortest path.

- **Shortest path:** Yes.
- **Memory:** Medium. Similar to BFS but usually expands far fewer cells
  because the heuristic steers the search toward the goal.
- **When to use:** The default choice when you want the shortest path
  efficiently.

```
Time:  O(E log V)  (priority-queue operations)
Space: O(V)
```

## Comparing efficiency

Each solver returns a `SolveResult` with an `explored` count - the number of
cells expanded. Running `--algorithm all` on the same maze is an easy way to
see the difference:

```bash
python -m mazesolver examples/simple.txt --algorithm all
```

Typically you will see A* explore the fewest cells, BFS the most, and DFS
somewhere in between (while returning a possibly longer path).
