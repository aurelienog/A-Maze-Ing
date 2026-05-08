from .cell import Cell
from .solve import bfs, reconstruct_path


class MazeError(Exception):
    pass


class Maze():
    """
    Represents a maze grid with a start and end point, and supports solving
    and rendering the maze.

    The maze is composed of Cell objects arranged in a 2D grid, where each
    cell contains walls and can be traversed depending on those walls.

    Attributes:
        matrix (list[list[Cell]]): 2D grid of cells representing the maze.
        width (int): Number of columns in the maze.
        height (int): Number of rows in the maze.
        entry (tuple[int, int]): Coordinates (row, col) of the entry point.
        exit (tuple[int, int]): Coordinates (row, col) of the exit point.
        solution_path (list[tuple[int, int]]): Computed path from entry to exit.
    """
    def __init__(self, matrix: list[list[Cell]], width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int],
                 seed: int, algorithm: str) -> None:
        """
        Initialize a Maze instance.

        Args:
            matrix: 2D grid of Cell objects.
            width: Number of columns.
            height: Number of rows.
            entry: Starting coordinate (row, col).
            exit: Goal coordinate (row, col).
        """
        self.matrix: list[list[Cell]] = matrix
        self.width: int = width
        self.height: int = height
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.seed: int = seed
        self.algorithm = algorithm
        self.solution_path: list[tuple[int, int]] = []

    def solve_maze(self) -> list[tuple[int, int]]:
        """
        Solve the maze using BFS and compute the shortest path from entry to exit.

        The algorithm uses a BFS traversal on the maze grid and reconstructs
        the path using a backtracking map of coordinates.

        Side effects:
            Updates self.solution_path with the computed path.

        Returns:
            list[tuple[int, int]]: Ordered path from entry to exit.
        """
        if len(self.solution_path) > 0:
            return self.solution_path

        parent: dict[tuple[int, int], tuple[int, int] | None] = bfs(self.matrix,
                                                                    self.entry,
                                                                    self.exit)
        path = reconstruct_path(parent, self.exit)
        self.solution_path = path
        return path
