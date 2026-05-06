#!/usr/bin/env python3
import sys
from mazegen.config import Config, ConfigError, get_config
from mazegen.maze import MazeGenerator, MazeError, validate_maze_config, Maze
from mazegen.render import export_maze, render_menu
from mazegen.render.colors import Color
from mazegen.render.maze_renderer import labyrinth_renderer


def read_file(file: str) -> list[str]:
    with open(file, "r") as f:
        content = [line.strip() for line in f]
    return content


def load_maze_config(content: list[str]) -> Config:
    config = get_config(content)
    validate_maze_config(config)
    return config


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
            print("EXIT")
            sys.exit(0)
        else:
            print(f"{Color.RED}[ERROR]: Please enter a valid command (1 to 4)"
                  f"{Color.RESET}")


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


def main() -> None:
    if len(sys.argv) != 2:
        print(f"{Color.RED}[ERROR] program must be run with config.txt{Color.RESET}")
        sys.exit(1)

    file: str = sys.argv[1]

    try:
        content: list[str] = read_file(file)
        config: Config = load_maze_config(content)
    except FileNotFoundError:
        print("[ERROR] file not found")
        sys.exit(1)
    except PermissionError:
        print("[ERROR] access denied")
        sys.exit(1)
    except OSError:
        print("[ERROR] system error")
        sys.exit(1)
    except ConfigError as e:
        print(f"\n[CONFIG ERROR] Mandatory configuration is invalid:\n- {e}")
        sys.exit(1)
    except MazeError as e:
        print(f"\n[MAZE ERROR]\n- {e}")
        sys.exit(1)

    run_maze_app(config)


if __name__ == "__main__":
    main()
