from .cell import Direction, Cell
from .colors import Color
from .solve import bfs, reconstruct_path


class MazeError(Exception):
    pass


class Maze():
    def __init__(self, matrix: list[list[Cell]], width: int, height: int,
                 entry: Cell, exit: Cell) -> None:
        self.matrix: list[list[Cell]] = matrix
        self.width: int = width
        self.height: int = height
        self.entry: Cell = entry
        self.exit: Cell = exit
        self.solution_path: list[Cell] = []

    def render_cell(self, cell: Cell) -> str:
        if cell == self.entry:
            return f"{Color.GREEN} E {Color.RESET}"

        elif cell == self.exit:
            return f"{Color.RED} X {Color.RESET}"

        elif cell in self.solution_path:
            return f"{Color.PATH_COLOR} o {Color.RESET}"
        return "   "

    def __repr__(self) -> str:
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

    def solve_maze(self) -> list[Cell]:
        came_from: dict[Cell, Cell | None] = bfs(self.matrix, self.entry, self.exit)
        path = reconstruct_path(came_from, self.exit)
        self.solution_path = path
        return path
