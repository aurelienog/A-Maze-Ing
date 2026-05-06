import sys
from ..maze import MazeGenerator, Maze
from ..render import render_menu, animate_exit, labyrinth_renderer, Color
from ..config import Config
from ..io import export_maze


def build_and_solve_maze(config: Config) -> Maze:
    generator = MazeGenerator()
    if config["PERFECT"]:
        maze = generator.generate_perfect_maze(config["WIDTH"], config["HEIGHT"],
                                               config["ENTRY"], config["EXIT"])
    else:
        maze = generator.generate_imperfect_maze(config["WIDTH"], config["HEIGHT"],
                                                 config["ENTRY"], config["EXIT"])
    maze.solve_maze()

    return maze


def run_maze_app(config: Config) -> None:
    is_path_visible: bool = False
    maze: Maze = build_and_solve_maze(config)

    while True:
        labyrinth_renderer(maze, is_path_visible)

        try:
            choice: str = render_menu()
        except ValueError:
            print(f"{Color.RED}[ERROR]: Please enter a valid command (1 to 4)"
                  f"{Color.RESET}")
            continue

        if choice == "1":
            maze = build_and_solve_maze(config)
            export_maze(config["OUTPUT_FILE"], maze)
            is_path_visible = False

        elif choice == "2":
            is_path_visible = not is_path_visible

        elif choice == "3":
            continue
        elif choice == "4":
            animate_exit()
            sys.exit(0)
        else:
            print(f"{Color.RED}[ERROR]: Please enter a valid command (1 to 4)"
                  f"{Color.RESET}")
