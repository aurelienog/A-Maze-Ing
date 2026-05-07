from ..config import Config, get_config
from ..maze import validate_maze_config


def load_maze_config(content: list[str]) -> Config:
    config = get_config(content)
    validate_maze_config(config)
    return config
