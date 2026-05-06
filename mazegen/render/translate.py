from ..maze.cell import Cell, Direction

base: list[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8",
                        "9", "A", "B", "C", "D", "E", "F"]


def cell_to_hex(Cell: Cell) -> str:
    total: int = 0
    if Cell.walls[Direction.TOP]:
        total += 1
    if Cell.walls[Direction.RIGHT]:
        total += 2
    if Cell.walls[Direction.BOTTOM]:
        total += 4
    if Cell.walls[Direction.LEFT]:
        total += 8
    return (base[total])


def matrix_to_hex(matrix: list[list[Cell]]) -> str:
    hex_matrix: str = ""
    for row in matrix:
        for col in row:
            hex_matrix = hex_matrix + cell_to_hex(col)
        hex_matrix = hex_matrix + "\n"
    return hex_matrix


def path_to_directions(path: list[tuple[int, int]]) -> str:
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
