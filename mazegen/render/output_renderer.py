from ..maze import Maze
from .translate import matrix_to_hex, path_to_directions


def export_maze(output_file: str, maze: Maze) -> None:
    grid = matrix_to_hex(maze.matrix)
    path = path_to_directions(maze.solve_maze())
    result = f"{grid}\n{maze.entry}\n{maze.exit}\n{path}"

    try:
        with open(output_file, "w") as f:
            f.write(result)
    except PermissionError:
        raise Exception("[FILE ERROR] access denied")
    except OSError as e:
        raise OSError(f"[FILE ERROR] could not write maze to {output_file}") from e
