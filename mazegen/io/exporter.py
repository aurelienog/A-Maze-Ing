from ..maze import Maze
from ..render.translate import matrix_to_hex, path_to_directions


def export_maze(output_file: str, maze: Maze) -> None:
    """
    Export a generated maze to a file.

    The exported format includes:
    - Hex representation of the maze grid
    - Entry coordinates
    - Exit coordinates
    - Solution path encoded as movement directions

    The maze is first transformed into a serializable format using:
    - matrix_to_hex(): converts the maze grid into a compact string form
    - path_to_directions(): converts the solution path into directions

    Args:
        output_file (str):
            Path of the file where the maze will be saved.

        maze (Maze):
            The maze instance to export.

    Returns:
        None

    Raises:
        Exception:
            If file writing fails due to permission issues.

        OSError:
            If the system fails while attempting to write the file.
    """
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
