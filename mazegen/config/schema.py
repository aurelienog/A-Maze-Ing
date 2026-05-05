from typing import TypedDict


class Config(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool


class ConfigError(Exception):
    """Custom exception raised when configuration validation fails."""
    pass
