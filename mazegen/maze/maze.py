from .cell import Cell
from .solve import bfs, reconstruct_path


class MazeError(Exception):
    """
    Exception raised for maze generation, validation,
    or solving related errors.
    """
    pass


class Maze():
    """
    Represents a maze composed of interconnected cells.

    The maze stores a 2D grid of Cell objects together with
    metadata such as dimensions, entry/exit points,
    generation settings, and cached solution paths.

    Attributes:
        matrix (list[list[Cell]]): 2D grid representing the maze.
        width (int): Number of columns in the maze.
        height (int): Number of rows in the maze.
        entry (tuple[int, int]): Entry coordinates as (row, col).
        exit (tuple[int, int]): Exit coordinates as (row, col).
        seed (int): Random seed used during maze generation.
        algorithm (str): Name of the generation algorithm used.
        solution_path (list[tuple[int, int]]): Cached solution path
            from entry to exit.
    """
    def __init__(self, matrix: list[list[Cell]], width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int],
                 seed: int, algorithm: str) -> None:
        """
        Initialize a maze instance.

        Args:
            matrix (list[list[Cell]]): Maze cell grid.
            width (int): Number of columns.
            height (int): Number of rows.
            entry (tuple[int, int]): Entry coordinates (row, col).
            exit (tuple[int, int]): Exit coordinates (row, col).
            seed (int): Random seed used for generation.
            algorithm (str): Generation algorithm identifier.
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
        Compute and cache a path from entry to exit.

        The maze is solved using a breadth-first search traversal,
        ensuring the returned path is the shortest path in terms
        of movement steps.

        Returns:
            list[tuple[int, int]]: Ordered coordinates representing
            the path from entry to exit.
        """

        parent: dict[tuple[int, int], tuple[int, int] | None] = bfs(self.matrix,
                                                                    self.entry,
                                                                    self.exit)
        path = reconstruct_path(parent, self.exit)
        self.solution_path = path
        return path
