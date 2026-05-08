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
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print("4. Enter a seed")
    print("5. Quit")
    command: str = input("Choice? (1-5): ")
    if command not in valid_command:
        raise ValueError
    return command
