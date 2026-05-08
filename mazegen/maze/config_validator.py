from ..config.schema import Config
from .maze import MazeError


def validate_maze_config(config: Config) -> list[str]:
    errors: list[str] = []

    if config["WIDTH"] <= 0:
        errors.append("WIDTH must be > 0")

    if config["HEIGHT"] <= 0:
        errors.append("HEIGHT must be > 0")

    if config["ENTRY"] == config["EXIT"]:
        errors.append("ENTRY and EXIT cannot be the same")

    y, x = config["ENTRY"]
    if not (0 <= x < config["WIDTH"] and 0 <= y < config["HEIGHT"]):
        errors.append("ENTRY is out of bounds")

    y, x = config["EXIT"]
    if not (0 <= x < config["WIDTH"] and 0 <= y < config["HEIGHT"]):
        errors.append("EXIT is out of bounds")

    if len(errors) > 0:
        raise MazeError("\n- ".join(errors))
    return errors
