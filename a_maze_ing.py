#!/usr/bin/env python3
import sys
from mazegen import (Config, ConfigError, MazeError, ColorPalette,
                     read_file, load_maze_config, run_maze_app)


def main() -> None:
    if len(sys.argv) != 2:
        print(f"{ColorPalette.RED}[ERROR] program must be run with config.txt"
              f"{ColorPalette.RESET}")
        sys.exit(1)

    file: str = sys.argv[1]

    try:
        content: list[str] = read_file(file)
        config: Config = load_maze_config(content)
    except FileNotFoundError:
        print(f"{ColorPalette.RED}[ERROR] file not found{ColorPalette.RESET}")
        sys.exit(1)
    except PermissionError:
        print(f"{ColorPalette.RED}[ERROR] access denied{ColorPalette.RESET}")
        sys.exit(1)
    except OSError:
        print(f"{ColorPalette.RED}[ERROR] system error{ColorPalette.RESET}")
        sys.exit(1)
    except ConfigError as e:
        print(f"\n{ColorPalette.RED}[CONFIG ERROR] Mandatory configuration",
              f" is invalid:\n{ColorPalette.RESET}-{e}")
        sys.exit(1)
    except MazeError as e:
        print(f"\n{ColorPalette.RED}[MAZE ERROR]\n-{ColorPalette.RESET} {e}")
        sys.exit(1)

    run_maze_app(config)


if __name__ == "__main__":
    main()
