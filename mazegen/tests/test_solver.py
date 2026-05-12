from ..maze.solve import bfs, reconstruct_path
from .utils import create_fixed_maze


def test_generated_maze_is_solvable() -> None:
    maze = create_fixed_maze()
    entry = maze.entry
    end = maze.exit

    path = reconstruct_path(
        bfs(maze.matrix, entry, end),
        end,
    )

    assert path, "Generated maze should always be solvable"
    assert path[0] == entry, "Path should start at entry"
    assert path[-1] == end, "Path should end at exit"


def test_reconstruct_path_no_solution() -> None:
    parent = {
        (0, 0): None,
        (0, 1): (0, 0),
    }

    path = reconstruct_path(parent, (5, 5))

    assert not path


def test_reconstruct_path_valid() -> None:
    parent = {
        (0, 0): None,
        (0, 1): (0, 0),
        (0, 2): (0, 1),
        (1, 2): (0, 2),
    }

    path = reconstruct_path(parent, (1, 2))

    assert path == [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
    ]
