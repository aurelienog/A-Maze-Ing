from ..maze.cell import Cell, Direction

def cell_to_hex(Cell: Cell) -> str:
    """
    Convert a single maze cell into a hexadecimal character.

    Each wall of the cell is encoded as a bit:
        TOP    = 1
        RIGHT  = 2
        BOTTOM = 4
        LEFT   = 8

    The sum of active walls is used as an index in a hexadecimal
    lookup table (0-F).

    Args:
        Cell (Cell):
            Maze cell to convert.

    Returns:
        str:
            Single hexadecimal character representing the cell state.
    """
    HEX_DIGITS: str = "0123456789ABCDEF"
    total: int = 0
    if Cell.walls[Direction.TOP]:
        total += 1
    if Cell.walls[Direction.RIGHT]:
        total += 2
    if Cell.walls[Direction.BOTTOM]:
        total += 4
    if Cell.walls[Direction.LEFT]:
        total += 8
    return (HEX_DIGITS[total])


def matrix_to_hex(matrix: list[list[Cell]]) -> str:
    """
    Convert a full maze matrix into a hexadecimal string representation.

    Each cell is encoded using `cell_to_hex`, and rows are separated
    by newline characters.

    Args:
        matrix (list[list[Cell]]):
            2D maze grid.

    Returns:
        str:
            Multiline string representing the entire maze.
    """
    hex_matrix: str = ""
    for row in matrix:
        for col in row:
            hex_matrix = hex_matrix + cell_to_hex(col)
        hex_matrix = hex_matrix + "\n"
    return hex_matrix


def path_to_directions(path: list[tuple[int, int]]) -> str:
    """
    Convert a path of coordinates into a string of movement directions.

    The path is assumed to be a sequence of (row, col) coordinates.
    Consecutive steps are translated into cardinal directions:

        N = up
        S = down
        W = left
        E = right

    Args:
        path (list[tuple[int, int]]):
            Ordered list of coordinates representing the solution path.

    Returns:
        str:
            String encoding the movement directions.
    """
    result: str = ""
    for i in range(1, len(path)):
        dy = path[i - 1][0] - path[i][0]
        dx = path[i - 1][1] - path[i][1]

        if dy == 1:
            result += "N"
        elif dy == -1:
            result += "S"
        elif dx == 1:
            result += "W"
        elif dx == -1:
            result += "E"

    return (result)
