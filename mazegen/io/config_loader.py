from ..config import Config, get_config
from ..maze import validate_maze_config


def load_maze_config(content: list[str]) -> Config:
    """
    Parse and validate maze configuration from raw file content.

    This function is responsible for:
    - Extracting configuration values from input text
    - Validating that all required fields are present
    - Ensuring values are within valid ranges and formats

    It acts as the main entry point for converting a raw configuration
    file into a structured `Config` object.

    Args:
        content (list[str]):
            Raw lines read from the configuration file.

    Returns:
        Config:
            A validated configuration object ready for maze generation.

    Raises:
        ConfigError:
            If the configuration is missing required fields or contains
            invalid values.
    """
    config = get_config(content)
    validate_maze_config(config)
    return config
