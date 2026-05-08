from .schema import Config, ConfigError
from .parser import parse_config, parse_coordinate
from .validator import get_validation_errors


def cast_config(config: dict[str, str]) -> Config:
    """
    Cast configuration values to their appropriate data types.

    Converts string-based configuration values into properly typed values:
    - WIDTH and HEIGHT to integers
    - ENTRY and EXIT to (int, int) tuples
    - PERFECT to a boolean

    Args:
        config (dict): Configuration dictionary with string values.

    Returns:
        Config: A configuration object with correctly typed values.
    """
    return {
        "WIDTH": int(config["WIDTH"]),
        "HEIGHT": int(config["HEIGHT"]),
        "ENTRY": parse_coordinate(config["ENTRY"]),
        "EXIT": parse_coordinate(config["EXIT"]),
        "OUTPUT_FILE": config["OUTPUT_FILE"],
        "PERFECT": config["PERFECT"].lower() == "true",
    }


def get_config(content: list[str]) -> Config:
    """
    Parse and validate configuration content.

    Combines parsing and validation steps. Raises an exception if any
    errors are found.

    Args:
        content (list[str]): List of raw configuration lines.

    Returns:
        Config: A configuration object with correctly typed values.

    Raises:
        ConfigError: If parsing or validation errors are encountered.
    """
    raw_config, errors = parse_config(content)
    errors += get_validation_errors(raw_config)

    if errors:
        raise ConfigError("\n- ".join(errors))
    config = cast_config(raw_config)

    return config
