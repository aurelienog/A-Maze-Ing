from .parser import parse_coordinate


def validate_structure(config: dict[str, str]) -> list[str]:
    """
    Validate the structure of the configuration dictionary.

    Ensures that all required keys are present and that no invalid keys exist.

    Args:
        config (dict): Configuration dictionary with key-value pairs.

    Returns:
        list[str]: A list of error messages describing missing or invalid keys.
    """
    required_keys: set[str] = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                               "PERFECT"}
    errors: list[str] = []

    missing = required_keys - config.keys()
    for key in missing:
        errors.append(f"[STRUCTURE ERROR] Missing required key: {key}")

    for key in config.keys():
        if key not in required_keys:
            errors.append(f"[STRUCTURE ERROR] Invalid key: {key}")
            continue
    return errors


def validate_values(config: dict[str, str]) -> list[str]:
    """
    Validate the values of the configuration dictionary.

    Checks that:
    - OUTPUT_FILE ends with '.txt'
    - PERFECT is either 'true' or 'false'
    - WIDTH and HEIGHT are integers
    - ENTRY and EXIT are valid coordinates in 'x,y' format

    Args:
        config (dict): Configuration dictionary with key-value pairs.

    Returns:
        list[str]: A list of error messages describing invalid values.
    """
    errors: list[str] = []

    for key, value in config.items():

        if key == "OUTPUT_FILE":
            if not value.endswith(".txt"):
                errors.append(f"[FORMAT ERROR] {key}='{value}' must be a .txt file")

        elif key == "PERFECT":
            if value.lower() not in {"true", "false"}:
                errors.append("[FORMAT ERROR] PERFECT must be 'true' or 'false'")

        elif key in {"WIDTH", "HEIGHT"}:
            try:
                int(value)
            except ValueError:
                errors.append(f"[FORMAT ERROR] {key} must be a number")
        elif key in {"ENTRY", "EXIT"}:
            try:
                parse_coordinate(value)
            except ValueError:
                errors.append(f"[FORMAT ERROR] {key} must be a coordinate 'x,y'")
    return errors


def get_validation_errors(config: dict[str, str]) -> list[str]:
    """
    Aggregate all validation errors for a configuration.

    Combines structural and value validation errors into a single list.

    Args:
        config (dict): Configuration dictionary.

    Returns:
        list[str]: A list of all validation error messages.
    """
    errors: list[str] = []
    errors += validate_structure(config)
    errors += validate_values(config)
    return errors
