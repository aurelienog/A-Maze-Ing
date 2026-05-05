def parse_config(content: list[str]) -> tuple[dict[str, str], list[str]]:
    """
    Parse raw configuration lines into a dictionary.

    Ignores empty lines and comments. Validates basic syntax such as:
    - Presence of '=' separator
    - Non-empty keys and values
    - No duplicate keys

    Args:
        content (list[str]): List of raw configuration lines.

    Returns:
        tuple[dict[str, str], list[str]]:
            - Parsed configuration dictionary
            - List of parsing error messages
    """
    config: dict[str, str] = {}
    errors: list[str] = []

    for line in content:
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            errors.append(f"[SYNTAX ERROR] '{line}' is invalid."
                          " Expected format: 'key=value'")
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            errors.append(f"[SYNTAX ERROR] Missing key for '{line}'")
            continue

        if not value:
            errors.append(f"[SYNTAX ERROR] Missing value for '{line}'")
            continue

        if key in config:
            errors.append(f"[SYNTAX ERROR] Duplicate key: '{line}'")
            continue

        config[key] = value

    return config, errors


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
        y, x = value.split(",")
        return int(x), int(y)
    except ValueError as e:
        raise ValueError(f"invalid coordinate: '{value}'") from e
