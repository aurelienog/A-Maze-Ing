from .cell import Direction


class Maze():
    def __init__(self, matrix, width: int, height: int) -> None:
        self.matrix = matrix
        self.width = width
        self.height = height
        # self.entry = entry
        # self.exit = exit

    def __repr__(self):
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

                middle_line += "   "

            # close right wall
            middle_line += "|"

            maze.append(top_line)
            maze.append(middle_line)

        # bottom line of maze
        bottom = "+"
        for cell in self.matrix[-1]:
            bottom += "---+"
        maze.append(bottom)

        return "\n".join(maze)