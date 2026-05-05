from collections import deque
from .cell import Cell


def bfs(
        matrix: list[list[Cell]],
        entry: tuple[int, int],
        end: tuple[int, int]
        ) -> dict[tuple[int, int], tuple[int, int] | None]:

    queue = deque([entry])
    visited = {entry}
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {entry: None}

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
                came_from[coord] = current
                queue.append(coord)
    return came_from


def reconstruct_path(
        came_from: dict[tuple[int, int], tuple[int, int] | None],
        end: tuple[int, int]
        ) -> list[tuple[int, int]]:
    """
    Reconstruct the path from the BFS result.

    Args:
        matrix (list[list[Cell]]): Maze grid.
        came_from (dict): Mapping of each cell coordinate to its predecessor.
        end (Cell): Target cell.

    Returns:
        list[tuple[int, int]]: Path from entry to exit as list[tuple[int, int]].
        Returns empty list if no path exists.
    """
    path: list[tuple[int, int]] = []
    current: tuple[int, int] | None = end

    if current not in came_from:
        return []

    while current is not None:
        path.append(current)
        current = came_from.get(current)

    path.reverse()
    return path
