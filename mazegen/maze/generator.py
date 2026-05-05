from .maze import Maze, MazeError
from .cell import Cell
import random


class MazeGenerator():
    def __init__(self, seed: int | None = None) -> None:
        self.rng = random.Random(seed)

    def generate_perfect_maze(
            self, width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int]
            ) -> Maze:
        """
        Generate and show a maze, using the simple Depth-first search algorithm.

        Start at a random cell.
        Mark the current cell as visited, and get a list of its neighbors. For each
        neighbor, starting with a randomly selected neighbor:

        If that neighbor hasn't been visited, remove the wall between this cell and
        that neighbor, and then recurse with that neighbor as the current cell.
        """
        self._validate_inputs(width, height, entry, exit)
        matrix = self._create_matrix(width, height)
        entry_cell, exit_cell = self._find_cells(matrix, entry, exit)
        start = self._random_start(matrix)
        self._dfs_build(start, matrix)

        return Maze(matrix, width, height, entry_cell, exit_cell)

    # ----------------- helpers -----------------
    @staticmethod
    def _validate_inputs(width: int, height: int,
                         entry: tuple[int, int],
                         exit: tuple[int, int]) -> None:
        if width <= 0 or height <= 0:
            raise MazeError("Invalid maze dimensions")

        if entry == exit:
            raise MazeError("Entry and exit cannot be the same")

        for x, y in (entry, exit):
            if x < 0 or x >= height or y < 0 or y >= width:
                raise MazeError("Entry or exit out of bounds")

    @staticmethod
    def _create_matrix(width: int, height: int) -> list[list[Cell]]:
        matrix: list[list[Cell]] = [[Cell(row, col) for col in range(width)]
                                    for row in range(height)]
        return matrix

    @staticmethod
    def _find_cells(matrix: list[list[Cell]],
                    entry: tuple[int, int],
                    exit: tuple[int, int]) -> tuple[Cell, Cell]:
        entry_cell = None
        exit_cell = None

        for row in matrix:
            for cell in row:
                if (cell.row, cell.col) == entry:
                    entry_cell = cell
                elif (cell.row, cell.col) == exit:
                    exit_cell = cell

        if entry_cell is None or exit_cell is None:
            raise MazeError("Entry or exit coordinates do not match any cell")

        return (entry_cell, exit_cell)

    def _random_start(self, matrix: list[list[Cell]]) -> Cell:
        line = self.rng.choice(matrix)
        current_cell = self.rng.choice(line)
        return current_cell

    def _dfs_build(self, current_cell: Cell, matrix: list[list[Cell]]) -> None:
        current_cell.visited = True
        unvisited_neighbors = current_cell.get_unvisited_neighbors(matrix)
        self.rng.shuffle(unvisited_neighbors)

        for neighbor in unvisited_neighbors:
            if not neighbor.visited:
                current_cell.connect_cells(neighbor)
                self._dfs_build(neighbor, matrix)
