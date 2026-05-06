def read_file(file: str) -> list[str]:
    with open(file, "r") as f:
        content = [line.strip() for line in f]
    return content
