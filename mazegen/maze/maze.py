from .cell import Direction, Cell
from .colors import Color
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
                 entry: tuple[int, int], exit: tuple[int, int]) -> None:
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
        self.solution_path: list[tuple[int, int]] = []

    def render_cell(self, cell: Cell) -> str:
        """
        Render a single cell as a string for maze visualization.

        The cell is styled depending on whether it is:
        - The entry point (green)
        - The exit point (red)
        - Part of the solution path (highlighted color)

        Args:
            cell: Cell to render.

        Returns:
            str: Formatted string representation of the cell.
        """
        coord = (cell.row, cell.col)
        if coord == self.entry:
            return f"{Color.GREEN} E {Color.RESET}"

        elif coord == self.exit:
            return f"{Color.RED} X {Color.RESET}"

        elif (cell.row, cell.col) in self.solution_path:
            return f"{Color.PATH_COLOR} * {Color.RESET}"
        return "   "

    def __repr__(self) -> str:
        """
        Generate a string representation of the entire maze.

        The maze is rendered using ASCII characters where:
        - Walls are shown using '+' and '---'
        - Paths are spaces
        - Entry, exit, and solution path are color-highlighted

        Returns:
            str: Multi-line string representing the maze.
        """
        maze: list[str] = []

        for row in self.matrix:
            top_line = "+"
            middle_line = ""

            for cell in row:
                if cell.walls[Direction.TOP]:
                    top_line += "---+"
                else:
                    top_line += "   +"

                if cell.walls[Direction.LEFT]:
                    middle_line += "|"
                else:
                    middle_line += " "

                middle_line += self.render_cell(cell)

            middle_line += "|"

            maze.append(top_line)
            maze.append(middle_line)

        bottom = "+"
        for cell in self.matrix[-1]:
            bottom += "---+"
        maze.append(bottom)

        return "\n".join(maze)

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
        parent: dict[tuple[int, int], tuple[int, int] | None] = bfs(self.matrix,
                                                                    self.entry,
                                                                    self.exit)
        path = reconstruct_path(parent, self.exit)
        self.solution_path = path
        return path
