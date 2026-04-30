from typing import TypedDict


class Config(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool


def parse_coordinate(value: str) -> tuple[int, int]:
    """
    Parse a coordinate string into a tuple of integers.

    The expected format is 'x,y', where both x and y are integers.

    Args:
        value (str): Coordinate string in the format 'x,y'.

    Returns:
        tuple[int, int]: A tuple containing the parsed (x, y) coordinates.

    Raises:
        ValueError: If the input is not in the correct format or cannot be parsed.
    """
    try:
        x, y = value.split(",")
        return int(x), int(y)
    except ValueError as e:
        raise ValueError(f"invalid coordinate: '{value}'") from e


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
