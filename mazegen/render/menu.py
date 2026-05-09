valid_command: list[str] = ["1", "2", "3", "4", "5"]


def render_menu() -> str:
    """
    Terminal menu system for the maze application.

    This module provides a simple text-based interface that allows
    the user to interact with the maze generator at runtime.

    It handles:
    - Displaying available commands
    - Reading user input
    - Validating selected options
    """
    print("\n=== A-MAZE-ING ===")
    print("1. Generate new maze")
    print("2. Show / hide solution path")
    print("3. Rotate color theme")
    print("4. Generate maze using custom seed")
    print("5. Exit")
    command: str = input("\nChoice? (1-5): ")
    if command not in valid_command:
        raise ValueError
    return command
