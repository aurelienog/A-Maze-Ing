import sys
from ..maze import MazeGenerator, Maze
from ..render import render_menu, animate_exit, labyrinth_renderer, ColorPalette
from ..config import Config
from ..io import export_maze


def build_and_solve_maze(config: Config,
                         seed: int | None = None,
                         generation: str | None = None) -> Maze:
    """
    Generate and solve a maze based on configuration settings.

    This function:
    - Creates a MazeGenerator instance
    - Generates either a perfect or imperfect maze
    - Solves the generated maze

    Args:
        config (Config):
            Configuration dictionary containing maze settings
            (width, height, entry, exit, output file, etc.)

        seed (int | None):
            Optional seed for deterministic generation.

        generation (str | None):
            Maze generation algorithm:
            - "DFS"
            - "prim"
            If None, default algorithm is used.

    Returns:
        Maze:
            A fully generated and solved maze instance.
    """
    generator = MazeGenerator(seed)
    if config["PERFECT"]:
        maze = generator.generate_perfect_maze(config["WIDTH"], config["HEIGHT"],
                                               config["ENTRY"], config["EXIT"],
                                               algorithm=generation)
    else:
        maze = generator.generate_imperfect_maze(config["WIDTH"], config["HEIGHT"],
                                                 config["ENTRY"], config["EXIT"],
                                                 algorithm=generation)
    maze.solve_maze()

    return maze


def run_maze_app(config: Config) -> None:
    """
    Run the interactive maze application loop.

    This function is responsible for:
    - Generating the initial maze
    - Rendering the maze
    - Displaying the interactive menu
    - Handling user input commands
    - Regenerating mazes with different options
    - Toggling visualization features
    - Exporting maze results
    - Exiting the application gracefully

    Available user actions:
    1. Generate a new maze (DFS or Prim)
    2. Toggle solution path visibility
    3. Change rendering color theme
    4. Regenerate maze with custom seed and algorithm
    5. Exit application

    Args:
        config (Config):
            Global configuration used for maze generation and output.

    Returns:
        None
    """
    is_path_visible: bool = False
    maze: Maze = build_and_solve_maze(config)
    maze_colors = ColorPalette()
    labyrinth_renderer(maze, maze_colors, is_path_visible)
    export_maze(config["OUTPUT_FILE"], maze)

    while True:
        try:
            choice: str = render_menu()
        except ValueError:
            print(f"{ColorPalette.RED}[ERROR]: Please enter a valid command (1 to 5)"
                  f"{ColorPalette.RESET}")
            continue
        except KeyboardInterrupt:
            print("\nCancelled")
            continue

        if choice == "1":
            print("Select the Maze generation algorithm:")
            print("1.DFS")
            print("2.Prim")
            builder = input("Press 1 or 2: ")
            try:
                if builder == "1":
                    maze = build_and_solve_maze(config, generation="DFS")

                elif builder == "2":
                    maze = build_and_solve_maze(config, generation="prim")

                else:
                    raise ValueError(f"{ColorPalette.RED}[ERROR]: Invalid choice: "
                                     f"'{builder}'{ColorPalette.RESET}")
                labyrinth_renderer(maze, maze_colors, is_path_visible)
            except ValueError as error:
                print(error)
                continue
            export_maze(config["OUTPUT_FILE"], maze)
            is_path_visible = False

        elif choice == "2":
            is_path_visible = not is_path_visible
            labyrinth_renderer(maze, maze_colors, is_path_visible, True)

        elif choice == "3":
            maze_colors.choose_next_color()
            labyrinth_renderer(maze, maze_colors, is_path_visible, True)

        elif choice == "4":
            seed = input("Enter a seed number: ")
            print("Select the Maze generation algorithm:")
            print("1.DFS")
            print("2.Prim")
            algorithm = input("Press 1 or 2: ")
            try:
                if algorithm == "1":
                    maze = build_and_solve_maze(config, int(seed), generation="DFS")
                elif algorithm == "2":
                    maze = build_and_solve_maze(config, int(seed), generation="prim")
                else:
                    raise ValueError("-Invalid algorithm choice")
                labyrinth_renderer(maze, maze_colors, is_path_visible)
            except ValueError as e:
                print(f'{ColorPalette.RED}[ERROR]: Invalid choice:\n'
                      f'-Seed must be an integer\n{e}'
                      f'{ColorPalette.RESET}')
                continue
            export_maze(config["OUTPUT_FILE"], maze)
            is_path_visible = False

        elif choice == "5":
            animate_exit()
            sys.exit(0)
        else:
            print(f"{ColorPalette.RED}[ERROR]: Please enter a valid command (1 to 4)"
                  f"{ColorPalette.RESET}")
