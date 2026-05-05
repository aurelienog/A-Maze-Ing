from collections import deque
from .cell import Cell


def bfs(
        matrix: list[list[Cell]],
        entry: tuple[int, int],
        end: tuple[int, int]
        ) -> dict[tuple[int, int], tuple[int, int] | None]:
    """
    Perform Breadth-First Search (BFS) to explore a maze and build a parent map.

    BFS explores the maze level by level starting from the entry position,
    visiting all reachable cells while tracking the shortest path tree.

    Args:
        matrix (list[list[Cell]]):
            2D grid representing the maze.
        entry (tuple[int, int]):
            Starting position as (row, column).
        end (tuple[int, int]):
            Target position as (row, column).

    Returns:
        dict[tuple[int, int], tuple[int, int] | None]:
            Mapping where each cell points to its predecessor in the BFS tree.
            The entry position maps to None.

    Notes:
        - Uses a visited set to avoid revisiting cells.
        - Only moves through valid neighbor cells (no walls).
    """
    queue: deque[tuple[int, int]] = deque([entry])
    visited: set[tuple[int, int]] = {entry}
    parent: dict[tuple[int, int], tuple[int, int] | None] = {entry: None}

    while queue:
        current = queue.popleft()

        if current == end:
            break

        r, c = current
        current_cell = matrix[r][c]

        for neighbor in current_cell.get_valid_neighbors(matrix):
            coord = (neighbor.row, neighbor.col)

            if coord not in visited:
                visited.add(coord)
                parent[coord] = current
                queue.append(coord)
    return parent


def reconstruct_path(
        parent: dict[tuple[int, int], tuple[int, int] | None],
        end: tuple[int, int]
        ) -> list[tuple[int, int]]:
    """
    Reconstruct the shortest path from BFS parent mapping.

    Args:
        parent (dict[tuple[int, int], tuple[int, int] | None]):
            Mapping of each cell to its predecessor in BFS traversal.
        end (tuple[int, int]):
            Target position as (row, column).

    Returns:
        list[tuple[int, int]]:
            Ordered path from entry to exit as coordinates.
            Returns an empty list if no path exists.

    Notes:
        - Walks backwards from end to entry using the parent map.
        - The result is reversed before returning to ensure correct order.
    """
    path: list[tuple[int, int]] = []
    current: tuple[int, int] | None = end

    if current not in parent:
        return []

    while current is not None:
        path.append(current)
        current = parent.get(current)

    path.reverse()
    return path
