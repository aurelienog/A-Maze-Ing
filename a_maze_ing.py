#!/usr/bin/env python3
import sys
from mazegen.config import Config, ConfigError
from mazegen.maze import MazeError
from mazegen.render import Color
from mazegen.app import run_maze_app
from mazegen.io import read_file, load_maze_config


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
