from .maze import Maze, MazeError
from .cell import Cell, Direction
import random


class MazeGenerator():
    """
    Generates mazes using different algorithms.

    The generator can create:

    - Perfect mazes:
        Mazes with exactly one unique path between any two cells.
        Generated using DFS or randomized Prim's algorithm.

    - Imperfect mazes:
        Perfect mazes modified by removing additional walls in order
        to create loops while preventing fully open 2x2 areas.

    The generator also supports:
    - deterministic generation through seeds
    """

    def __init__(self, seed: int | None = None) -> None:
        """
        Initialize the maze generator.

        Args:
            seed (int | None):
                Random seed used for deterministic maze generation.
                If None, a random seed is generated automatically.
        """
        if seed is None:
            seed = random.randrange(0, 2**32)  # o secrets.randbits(32)
        self.seed = seed
        self.rng = random.Random(seed)

    def generate_perfect_maze(
            self, width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            algorithm: str | None = "prim"
            ) -> Maze:
        """
        Generate a perfect maze using a chosen algorithm.

        By default, the maze is generated using Prim's algorithm.

        Supported algorithms:
        - "prim": default algorithm (randomized frontier-based growth)
        - "DFS": recursive depth-first search

        A perfect maze has exactly one unique path between any two cells.

        Args:
            width (int): Number of columns.
            height (int): Number of rows.
            entry (tuple[int, int]): Entrance coordinates (row, col).
            exit (tuple[int, int]): Exit coordinates (row, col).
            algorithm (str | None): "prim" or "DFS". Defaults to "prim".

        Returns:
            Maze: Generated perfect maze.

        Raises:
            MazeError: If inputs are invalid.
        """
        if algorithm == "DFS":
            builder = "DFS"
        else:
            builder = "prim"

        self._validate_inputs(width, height, entry, exit)
        matrix = self._create_matrix(width, height)
        self._build_42_centered(width, height, matrix)
        valid_cells = [cell for row in matrix for cell in row if not cell.is42]
        start = self.rng.choice(valid_cells)
        if algorithm == "DFS":
            self._dfs_build(start, matrix)
        else:
            self._prim_build(start, matrix)

        return Maze(matrix, width, height, entry, exit, self.seed, builder)

    def generate_imperfect_maze(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            break_prob: float = 0.3,
            algorithm: str | None = None
            ) -> Maze:
        """
        Generate an imperfect maze.

        The maze is first generated as a perfect maze and then
        additional walls may be removed randomly to create loops.

        Extra wall removals are restricted in order to prevent
        the creation of fully open 2x2 areas, preserving
        one-cell-wide corridors.

        Args:
            width (int):
                Number of columns in the maze.

            height (int):
                Number of rows in the maze.

            entry (tuple[int, int]):
                Coordinates (row, col) of the maze entry.

            exit (tuple[int, int]):
                Coordinates (row, col) of the maze exit.

            break_prob (float):
                Probability of removing an eligible wall.

            algorithm (str | None):
                Base perfect-maze generation algorithm.

        Returns:
            Maze:
                Generated imperfect maze.
        """
        maze = self.generate_perfect_maze(width, height, entry, exit, algorithm)

        for row in maze.matrix:
            for cell in row:
                if cell.is42:
                    continue
                if sum(cell.walls.values()) >= 2:

                    if self.rng.random() > break_prob:
                        continue

                    neighbors = [n for n in cell.get_neighbors(maze.matrix)
                                 if not n.is42]
                    self.rng.shuffle(neighbors)

                    for neighbor in neighbors:
                        direction = cell.get_direction(neighbor)

                        if not cell.walls[direction]:
                            continue

                        if sum(neighbor.walls.values()) == 3:
                            if not self.would_create_2x2(cell, neighbor, maze):
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

    def _prim_build(self, current_cell: Cell, matrix: list[list[Cell]]) -> None:
        """
        Generate a perfect maze using randomized Prim's algorithm.

        The algorithm grows the maze incrementally by connecting
        frontier cells to already visited cells.

        Args:
            current_cell (Cell):
                Initial starting cell.

            matrix (list[list[Cell]]):
                Maze matrix.
        """
        current_cell.visited = True
        frontier: list[Cell] = current_cell.get_unvisited_neighbors(matrix)
        while frontier:
            current_cell = self.rng.choice(frontier)
            frontier.remove(current_cell)
            current_cell.visited = True
            neighbor: Cell | None = self.get_visited_neighbor(current_cell, matrix)
            if neighbor:
                current_cell.connect_cells(neighbor)
            for cell in current_cell.get_unvisited_neighbors(matrix):
                if not cell.visited and cell not in frontier and not cell.is42:
                    frontier.append(cell)

    @staticmethod
    def _define_center(max: int) -> int:
        """
        Compute the center coordinate of an axis.

        Args:
            max (int):
                Axis size.

        Returns:
            int:
                Central coordinate.
        """
        if (max % 2) == 0:
            return (round(max / 2))
        else:
            return (round((max - 1) / 2))

    @staticmethod
    def _draw_line_for_42(start: int, height: int,
                          matrix: list[list[Cell]]) -> None:
        """
        Draw a horizontal segment of the centered 42 pattern.

        Marks three consecutive cells as blocked.

        Args:
            start (int):
                Starting column index.

            height (int):
                Target row index.

            matrix (list[list[Cell]]):
                Maze matrix.
        """
        for i in range(3):
            temp: Cell = matrix[height][start + i]
            temp.is42 = True

    @staticmethod
    def _draw_column_for_42(start: int, width: int,
                            matrix: list[list[Cell]]) -> None:
        """
        Draw a vertical segment of the centered 42 pattern.

        Marks three consecutive cells as blocked.

        Args:
            start (int):
                Starting row index.

            width (int):
                Target column index.

            matrix (list[list[Cell]]):
                Maze matrix.
        """
        for i in range(3):
            temp: Cell = matrix[start + i][width]
            temp.is42 = True

    def _build_42_centered(self, width: int, height: int,
                           matrix: list[list[Cell]]) -> None:
        """
        Build a centered blocking pattern representing "42".

        This pattern is always applied when the maze size allows it.
        If the maze is too small, the method exits without effect.

        The pattern is used to reserve fixed obstacles in the maze
        layout and is independent of the generation algorithm.

        Args:
            width (int): Maze width.
            height (int): Maze height.
            matrix (list[list[Cell]]): Maze grid.
        """
        from ..render import ColorPalette

        middle_height: int = self._define_center(height)
        middle_width: int = self._define_center(width)

        if width < 9 or height < 9:
            print(f"\n{ColorPalette.YELLOW}[INFO] Maze too small to build 42 pattern"
                  f"{ColorPalette.RESET}")
            return
        self._draw_line_for_42(middle_width - 3, middle_height, matrix)
        self._draw_line_for_42(middle_width + 1, middle_height, matrix)
        self._draw_line_for_42(middle_width + 1, middle_height - 2, matrix)
        self._draw_line_for_42(middle_width + 1, middle_height + 2, matrix)
        self._draw_column_for_42(middle_height, middle_width - 1, matrix)
        self._draw_column_for_42(middle_height - 2, middle_width + 3, matrix)
        self._draw_column_for_42(middle_height, middle_width + 1, matrix)
        self._draw_column_for_42(middle_height - 2, middle_width - 3, matrix)

    @staticmethod
    def would_create_2x2(cell: Cell, neighbor: Cell, maze: Maze) -> bool:
        """
        Check whether connecting two cells would create
        a fully open 2x2 area.

        The connection is simulated temporarily and reverted
        before returning.

        Args:
            cell (Cell):
                First cell.

            neighbor (Cell):
                Adjacent cell to connect.

            maze (Maze):
                Maze being modified.

        Returns:
            bool:
                True if the connection would create a 2x2 open area,
                False otherwise.
        """
        direction = cell.get_direction(neighbor)

        cell.walls[direction] = False

        opposite = {
            Direction.TOP: Direction.BOTTOM,
            Direction.BOTTOM: Direction.TOP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }

        neighbor.walls[opposite[direction]] = False

        for r in range(maze.height - 1):
            for c in range(maze.width - 1):

                A = maze.matrix[r][c]
                B = maze.matrix[r][c + 1]
                C = maze.matrix[r + 1][c]
                D = maze.matrix[r + 1][c + 1]

                if (
                    A.is_connected(B)
                    and A.is_connected(C)
                    and B.is_connected(D)
                    and C.is_connected(D)
                ):

                    cell.walls[direction] = True
                    neighbor.walls[opposite[direction]] = True

                    return True

        cell.walls[direction] = True
        neighbor.walls[opposite[direction]] = True

        return False

    def get_visited_neighbor(self, current_cell: Cell,
                             matrix: list[list[Cell]]) -> Cell | None:
        """
        Select a random visited neighbor of a cell.

        Args:
            current_cell (Cell):
                Current cell.

            matrix (list[list[Cell]]):
                Maze matrix.

        Returns:
            Cell | None:
                Random visited neighbor if available,
                otherwise None.
        """
        possibilities: list[Cell] = list(set(current_cell.get_neighbors(matrix))
                                         - set(current_cell.get_unvisited_neighbors(
                                             matrix)))
        if not possibilities:
            return None
        result = self.rng.choice(possibilities)
        return result
