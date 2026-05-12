from ..maze import MazeGenerator, MazeError
from ..maze.solve import bfs, reconstruct_path
import pytest


def test_generator_seed_is_deterministic() -> None:
    g1 = MazeGenerator(seed=42)
    g2 = MazeGenerator(seed=42)

    assert g1.seed == g2.seed


def test_validate_inputs_valid() -> None:
    MazeGenerator._validate_inputs(
        10, 10,
        (0, 0),
        (9, 9)
    )


def test_validate_inputs_negative_size() -> None:
    with pytest.raises(MazeError):
        MazeGenerator._validate_inputs(
            -1, 10,
            (0, 0),
            (1, 1)
        )


def test_validate_inputs_same_entry_exit() -> None:
    with pytest.raises(MazeError):
        MazeGenerator._validate_inputs(
            10, 10,
            (1, 1),
            (1, 1)
        )


def test_validate_inputs_out_of_bounds() -> None:
    with pytest.raises(MazeError):
        MazeGenerator._validate_inputs(
            10, 10,
            (100, 0),
            (1, 1)
        )


def test_create_matrix_dimensions() -> None:
    matrix = MazeGenerator._create_matrix(5, 7)

    assert len(matrix) == 7
    assert len(matrix[0]) == 5


def test_generate_prim_maze_is_solvable() -> None:
    gen = MazeGenerator(seed=42)

    entry = (0, 0)
    end = (9, 9)

    maze = gen.generate_perfect_maze(
        10,
        10,
        entry,
        end,
        algorithm="prim"
    )

    parent = bfs(maze.matrix, entry, end)
    path = reconstruct_path(parent, end)

    assert path
    assert path[0] == entry
    assert path[-1] == end


def test_generate_dfs_maze_is_solvable() -> None:
    gen = MazeGenerator(seed=42)

    entry = (0, 0)
    end = (9, 9)

    maze = gen.generate_perfect_maze(
        10,
        10,
        entry,
        end,
        algorithm="DFS"
    )

    parent = bfs(maze.matrix, entry, end)
    path = reconstruct_path(parent, end)

    assert path
    assert path[0] == entry
    assert path[-1] == end


def test_generate_dfs_vs_prim() -> None:
    gen = MazeGenerator(seed=123)

    maze_dfs = gen.generate_perfect_maze(
        10, 10, (0, 0), (9, 9), "DFS"
    )

    gen = MazeGenerator(seed=123)

    maze_prim = gen.generate_perfect_maze(
        10, 10, (0, 0), (9, 9), "prim"
    )

    assert maze_dfs.algorithm == "DFS"
    assert maze_prim.algorithm == "prim"


def test_generate_imperfect_maze_is_still_solvable() -> None:
    gen = MazeGenerator(seed=42)

    entry = (0, 0)
    end = (9, 9)

    maze = gen.generate_imperfect_maze(
        10, 10,
        entry,
        end,
        break_prob=0.5
    )

    parent = bfs(maze.matrix, entry, end)
    path = reconstruct_path(parent, end)

    assert path


def test_42_pattern_applied() -> None:
    gen = MazeGenerator(seed=1)

    maze = gen.generate_perfect_maze(
        15, 15,
        (0, 0),
        (14, 14)
    )

    blocked = [
        cell
        for row in maze.matrix
        for cell in row
        if cell.is42
    ]

    assert len(blocked) > 0


def test_no_42_on_small_maze() -> None:
    gen = MazeGenerator(seed=1)

    maze = gen.generate_perfect_maze(
        5, 5,
        (0, 0),
        (4, 4)
    )

    assert not any(cell.is42 for row in maze.matrix for cell in row)


def test_define_center_even_and_odd() -> None:
    assert MazeGenerator._define_center(10) == 5
    assert MazeGenerator._define_center(9) == 4
