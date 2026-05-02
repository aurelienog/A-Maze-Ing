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
            bottom_line = "+"

            for cell in row:
                # --- top wall
                if cell.walls[Direction.TOP]:
                    top_line += "---+"
                else:
                    top_line += "   +"

                # --- left wall
                if cell.walls[Direction.LEFT]:
                    middle_line += "|"
                else:
                    middle_line += " "
                
                middle_line += "   "

                # --- bottom wall
                if cell.walls[Direction.BOTTOM]:
                    bottom_line += "---+"
                else:
                    bottom_line += "   +"

            # close right wall
            middle_line += "|"

            maze.append(top_line)
            maze.append(middle_line)
            maze.append(bottom_line)

        return "\n".join(maze)
