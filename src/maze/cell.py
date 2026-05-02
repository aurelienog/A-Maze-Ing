from enum import Enum


class Direction(Enum):
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"
    LEFT = "left"


class CellError(Exception):
    pass


class Cell():
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.walls = {
            Direction.TOP: True,
            Direction.RIGHT: True,
            Direction.BOTTOM: True,
            Direction.LEFT: True
        }
        self.visited = False

    def get_neighbors(self, matrix) -> list["Cell"]:
        neighbors = []
        if self.col > 0:
            left_neighbor = matrix[self.row][self.col - 1]
            neighbors.append(left_neighbor)

        if self.col < len(matrix[0]) - 1:
            right_neighbor = matrix[self.row][self.col + 1]
            neighbors.append(right_neighbor)

        if self.row > 0:
            top_neighbor = matrix[self.row - 1][self.col]
            neighbors.append(top_neighbor)

        if self.row < len(matrix) - 1:
            bottom_neighbor = matrix[self.row + 1][self.col]
            neighbors.append(bottom_neighbor)
        return neighbors

    def get_unvisited_neighbors(self, matrix: list[list["Cell"]]) -> list["Cell"]:
        neighbors = self.get_neighbors(matrix)
        unvisited_neighbors = [n for n in neighbors if not n.visited]
        return unvisited_neighbors

    def remove_wall(self, direction: Direction) -> None:
        self.walls[direction] = False

    @staticmethod
    def get_direction(current_cell: "Cell", next_cell: "Cell") -> Direction:
        if current_cell.col == next_cell.col:
            if current_cell.row > next_cell.row:
                return Direction.BOTTOM
            else:
                return Direction.TOP
        elif current_cell.row == next_cell.row:
            if current_cell.col > next_cell.col:
                return Direction.LEFT
            else:
                return Direction.RIGHT
        else:
            raise CellError("Error while comparing position")

    @staticmethod
    def connect_cells(direction: Direction, cell1: "Cell", cell2: "Cell") -> None:
        match direction:
            case Direction.TOP:
                cell1.remove_wall(Direction.TOP)
                cell2.remove_wall(Direction.BOTTOM)
            case Direction.RIGHT:
                cell1.remove_wall(Direction.RIGHT)
                cell2.remove_wall(Direction.LEFT)
            case Direction.BOTTOM:
                cell1.remove_wall(Direction.BOTTOM)
                cell2.remove_wall(Direction.TOP)
            case Direction.LEFT:
                cell1.remove_wall(Direction.LEFT)
                cell2.remove_wall(Direction.RIGHT)
