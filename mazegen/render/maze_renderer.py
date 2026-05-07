from .colors import ColorPalette
from ..maze import Cell, Direction, Maze
import time


def render_cell(maze: Maze, cell: Cell, is_path_visible: bool,
                color: ColorPalette) -> str:
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
        return f"{color.entry} E {color.RESET}"

    elif coord == maze.exit:
        return f"{color.exit} X {color.RESET}"

    elif is_path_visible and (cell.row, cell.col) in maze.solution_path:
        return f"{color.path_color} * {color.RESET}"

    elif cell.is42:
        return f"{color.is42}   {color.RESET}"
    return "   "


def labyrinth_renderer(maze: Maze, maze_colors: ColorPalette,
                       is_path_visible: bool = False) -> None:
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
        top_line = f"{maze_colors.walls}+"
        middle_line = ""

        for cell in row:
            if cell.walls[Direction.TOP]:
                top_line += "---+"
            else:
                top_line += "   +"

            if cell.walls[Direction.LEFT]:
                middle_line += f"{maze_colors.walls}|"
            else:
                middle_line += " "

            middle_line += render_cell(maze, cell, is_path_visible, maze_colors)

        middle_line += f"{maze_colors.walls}|"

        grid.append(top_line)
        grid.append(middle_line)

    bottom = f"{maze_colors.walls}+"
    for cell in maze.matrix[-1]:
        bottom += f"{maze_colors.walls}---+"
    grid.append(bottom)
    '\n'.join(grid)
    for lines in grid:
        print(f"{lines}{maze_colors.RESET}")
        if not is_path_visible:
            time.sleep(0.04)
    print("seed:", maze.seed)
