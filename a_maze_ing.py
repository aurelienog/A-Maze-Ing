#!/usr/bin/env python3
import sys
from mazegen.config import Config, ConfigError, get_config
from mazegen.maze import MazeGenerator, MazeError, validate_maze_config


def read_file(file: str) -> list[str]:
    with open(file, "r") as f:
        content = [line.strip() for line in f]
    return content


def load_maze_config(content: list[str]) -> Config:
    config = get_config(content)
    validate_maze_config(config)
    return config


def main() -> None:
    if len(sys.argv) != 2:
        print("[ERROR] program must be run with config.txt")
        sys.exit(1)

    file: str = sys.argv[1]

    try:
        content: list[str] = read_file(file)
        config = load_maze_config(content)
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

    generator = MazeGenerator()
    maze = generator.generate_perfect_maze(config["WIDTH"], config["HEIGHT"],
                                           config["ENTRY"], config["EXIT"])
    maze.solve_maze()
    print(maze)


if __name__ == "__main__":
    main()
