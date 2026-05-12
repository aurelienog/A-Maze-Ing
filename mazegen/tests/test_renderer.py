from .utils import create_fixed_maze
from ..render.maze_renderer import render_cell
from ..render.colors import ColorPalette


def test_render_entry_cell() -> None:
    maze = create_fixed_maze()
    cell = maze.matrix[maze.entry[0]][maze.entry[1]]
    result = render_cell(
        maze,
        cell,
        False,
        ColorPalette()
    )

    assert "E" in result


def test_render_exit_cell() -> None:
    maze = create_fixed_maze()

    cell = maze.matrix[maze.exit[0]][maze.exit[1]]

    result = render_cell(
        maze,
        cell,
        False,
        ColorPalette()
    )

    assert "X" in result


def test_render_path_cell() -> None:
    maze = create_fixed_maze()
    maze.solve_maze()

    r, c = maze.solution_path[1]
    cell = maze.matrix[r][c]

    result = render_cell(
        maze,
        cell,
        True,
        ColorPalette()
    )

    assert "*" in result


def test_render_empty_cell() -> None:
    maze = create_fixed_maze()

    r, c = 0, 1
    cell = maze.matrix[r][c]

    result = render_cell(
        maze,
        cell,
        False,
        ColorPalette()
    )

    assert isinstance(result, str)
