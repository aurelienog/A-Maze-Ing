def read_file(file: str) -> list[str]:
    """
    Read a text file and return its contents as a list of stripped lines.

    Each line is processed to remove leading and trailing whitespace,
    including newline characters.

    Args:
        file (str):
            Path to the input file to be read.

    Returns:
        list[str]:
            A list of cleaned lines from the file.

    Raises:
        FileNotFoundError:
            If the specified file does not exist.

        PermissionError:
            If the program does not have permission to read the file.

        OSError:
            For other low-level I/O related errors.
    """
    with open(file, "r") as f:
        content = [line.strip() for line in f]
    return content
