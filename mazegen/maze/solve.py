from .cell import Cell
from collections import deque


def bfs(matrix: list[list[Cell]], entry: Cell, end: Cell) -> dict[Cell, Cell | None]:
    """
    Breadth-first search (BFS) is an algorithm for searching a tree data structure
    for a node that satisfies a given property.
    """
    for line in matrix:
        for cell in line:
            cell.visited = False

    start = entry
    queue = deque([start])
    start.visited = True
    came_from: dict[Cell, Cell | None] = {start: None}

    while len(queue) > 0:
        current_cell = queue.popleft()

        if current_cell == end:
            break

        neighbors = current_cell.get_valid_neighbors(matrix)
        for neighbor in neighbors:
            if not neighbor.visited:
                neighbor.visited = True
                came_from[neighbor] = current_cell
                queue.append(neighbor)
    return came_from


def reconstruct_path(came_from: dict[Cell, Cell | None], end: Cell) -> list[Cell]:
    path: list[Cell] = []
    current: Cell | None = end

    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
