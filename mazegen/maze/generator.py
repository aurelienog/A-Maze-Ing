from .maze import Maze, MazeError
from .cell import Cell
import random


class MazeGenerator():
    """
    Generates mazes using different algorithms.

    Currently supports generation of perfect mazes using
    Depth-First Search (DFS).
    """

    def __init__(self, seed: int | None = None) -> None:
        self.rng = random.Random(seed)

    def generate_perfect_maze(
            self, width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int]
            ) -> Maze:
        """
        Generate a perfect maze using Depth-First Search (DFS).

        A perfect maze has exactly one unique path between any two cells.

        Args:
            width (int): Number of columns in the maze.
            height (int): Number of rows in the maze.
            entry (tuple[int, int]): Coordinates (row, col) of the entry cell.
            exit (tuple[int, int]): Coordinates (row, col) of the exit cell.

        Returns:
            Maze: A generated maze instance.

        Raises:
            MazeError: If dimensions are invalid or entry/exit are incorrect.
        """

        self._validate_inputs(width, height, entry, exit)
        matrix = self._create_matrix(width, height)
        self._build_42_centered(width, height, matrix)
        valid_cells = [cell for row in matrix for cell in row if not cell.is42]
        start = self.rng.choice(valid_cells)
        self._dfs_build(start, matrix)

        return Maze(matrix, width, height, entry, exit)

    def generate_imperfect_maze(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            break_prob: float = 0.3
            ) -> Maze:

        maze = self.generate_perfect_maze(width, height, entry, exit)

        for row in maze.matrix:
            for cell in row:

                if sum(cell.walls.values()) == 3:

                    if self.rng.random() > break_prob:
                        continue

                    neighbors = cell.get_neighbors(maze.matrix)
                    self.rng.shuffle(neighbors)

                    for neighbor in neighbors:
                        direction = cell.get_direction(neighbor)

                        if not cell.walls[direction]:
                            continue

                        if sum(neighbor.walls.values()) == 3:
                            cell.connect_cells(neighbor)
                            break
        return maze

    # ----------------- helpers -----------------
    @staticmethod
    def _validate_inputs(width: int, height: int,
                         entry: tuple[int, int],
                         exit: tuple[int, int]) -> None:
        """
        Validate maze dimensions and entry/exit coordinates.

        Args:
            width (int): Maze width.
            height (int): Maze height.
            entry (tuple[int, int]): Entry coordinates.
            exit (tuple[int, int]): Exit coordinates.

        Raises:
            MazeError: If dimensions are non-positive, entry equals exit,
                       or coordinates are out of bounds.
        """
        if width <= 0 or height <= 0:
            raise MazeError("Invalid maze dimensions")

        if entry == exit:
            raise MazeError("Entry and exit cannot be the same")

        for x, y in (entry, exit):
            if x < 0 or x >= height or y < 0 or y >= width:
                raise MazeError("Entry or exit out of bounds")

    @staticmethod
    def _create_matrix(width: int, height: int) -> list[list[Cell]]:
        """
        Create a grid (matrix) of cells.

        Args:
            width (int): Number of columns.
            height (int): Number of rows.

        Returns:
            list[list[Cell]]: 2D list of Cell objects.
        """
        matrix: list[list[Cell]] = [[Cell(row, col) for col in range(width)]
                                    for row in range(height)]
        return matrix

    def _dfs_build(self, current_cell: Cell, matrix: list[list[Cell]]) -> None:
        """
        Carve passages in the maze using recursive Depth-first search algorithm.

        This method visits cells recursively, removing walls between
        the current cell and randomly chosen unvisited neighbors.

        Args:
            current_cell (Cell): Current cell being processed.
            matrix (list[list[Cell]]): Maze grid.

        Returns:
            None
        """
        current_cell.visited = True
        unvisited_neighbors = [
            n for n in current_cell.get_neighbors(matrix)
            if not n.visited and not n.is42
        ]
        self.rng.shuffle(unvisited_neighbors)

        for neighbor in unvisited_neighbors:
            if not neighbor.visited:
                current_cell.connect_cells(neighbor)
                self._dfs_build(neighbor, matrix)

    @staticmethod
    def _define_center(max: int) -> int:
        if (max % 2) == 0:
            return (round(max / 2))
        else:
            return (round((max - 1) / 2))

    @staticmethod
    def _draw_line_for_42(start: int, height: int,
                          matrix: list[list[Cell]]) -> None:
        for i in range(3):
            temp: Cell = matrix[height][start + i]
            temp.is42 = True

    @staticmethod
    def _draw_column_for_42(start: int, width: int,
                            matrix: list[list[Cell]]) -> None:
        for i in range(3):
            temp: Cell = matrix[start + i][width]
            temp.is42 = True

    def _build_42_centered(self, width: int, height: int,
                           matrix: list[list[Cell]]) -> None:
        middle_height: int = self._define_center(height)
        middle_width: int = self._define_center(width)

        if width < 9 or height < 9:
            print("\n[INFO] Maze too small to build 42 pattern")
            return
        self._draw_line_for_42(middle_width - 3, middle_height, matrix)
        self._draw_line_for_42(middle_width + 1, middle_height, matrix)
        self._draw_line_for_42(middle_width + 1, middle_height - 2, matrix)
        self._draw_line_for_42(middle_width + 1, middle_height + 2, matrix)
        self._draw_column_for_42(middle_height, middle_width - 1, matrix)
        self._draw_column_for_42(middle_height - 2, middle_width + 3, matrix)
        self._draw_column_for_42(middle_height, middle_width + 1, matrix)
        self._draw_column_for_42(middle_height - 2, middle_width - 3, matrix)
