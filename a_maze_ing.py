#!/usr/bin/env python3
import sys
from src.validation import ConfigError, Config, get_config


def read_file(file: str) -> list[str]:
    with open(file, "r") as f:
        content = [line.strip() for line in f]
    return content


def main() -> None:
    if len(sys.argv) != 2:
        print("[ERROR] program must be run with config.txt")
        sys.exit(1)

    file: str = sys.argv[1]

    try:
        content: list[str] = read_file(file)
        config: Config = get_config(content)
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
        print(f"\n[CONFIG ERROR] Mandatory configuration is invalid:\n{e}")
        sys.exit(1)

    print(config)


if __name__ == "__main__":
    main()
