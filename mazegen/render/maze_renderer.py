from .colors import Color
from ..maze import Cell, Direction, Maze


def render_cell(maze: Maze, cell: Cell, is_path_visible: bool) -> str:
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
    if coord == maze.entry:
        return f"{Color.GREEN} E {Color.RESET}"

    elif coord == maze.exit:
        return f"{Color.RED} X {Color.RESET}"

    elif is_path_visible and (cell.row, cell.col) in maze.solution_path:
        return f"{Color.PATH_COLOR} * {Color.RESET}"

    elif cell.is42:
        return f"{Color.IS42}   {Color.RESET}"
    return "   "


def labyrinth_renderer(maze: Maze, is_path_visible: bool = False) -> None:
    """
    Generate a string representation of the entire maze.

    The maze is rendered using ASCII characters where:
    - Walls are shown using '+' and '---'
    - Paths are spaces
    - Entry, exit, and solution path are color-highlighted

    Returns:
        str: Multi-line string representing the maze.
    """
    grid: list[str] = []

    for row in maze.matrix:
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

            middle_line += render_cell(maze, cell, is_path_visible)

        middle_line += "|"

        grid.append(top_line)
        grid.append(middle_line)

    bottom = "+"
    for cell in maze.matrix[-1]:
        bottom += "---+"
    grid.append(bottom)

    print("\n".join(grid))
