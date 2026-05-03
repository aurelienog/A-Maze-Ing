from .cell import Direction, Cell
from .colors import Color


class Maze():
    def __init__(self, matrix: list[list[Cell]], width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self.matrix = matrix
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit

    def render_cell(self, cell: Cell) -> str:
        if (cell.row, cell.col) == self.entry:
            return f"{Color.GREEN} E {Color.RESET}"

        elif (cell.row, cell.col) == self.exit:
            return f"{Color.RED} X {Color.RESET}"
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
