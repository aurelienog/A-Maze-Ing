from typing import TypedDict


class Config(TypedDict):
    """
    Typed dictionary representing the maze configuration.

    This structure defines all parameters required to generate,
    solve, and export a maze.

    Attributes:
        WIDTH (int):
            Number of columns in the maze grid.

        HEIGHT (int):
            Number of rows in the maze grid.

        ENTRY (tuple[int, int]):
            Starting cell coordinates in the format (row, col).

        EXIT (tuple[int, int]):
            Goal cell coordinates in the format (row, col).

        OUTPUT_FILE (str):
            Path or filename where the maze will be exported.

        PERFECT (bool):
            If True, generates a perfect maze (no cycles).
            If False, generates an imperfect maze (with loops allowed).
    """
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool


class ConfigError(Exception):
    """Custom exception raised when configuration validation fails."""
    pass
